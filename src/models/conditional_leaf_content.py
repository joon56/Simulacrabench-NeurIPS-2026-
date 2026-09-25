"""E057: honest visible-row selection and refit of UNHCR leaf content.

Only GIVEN features enter trees. Diagnostics are optional local callbacks;
the normal predict contract returns probability vectors only.
"""

from time import perf_counter

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from threadpoolctl import threadpool_limits

from src.eval.logloss import floor_mix
from src.models.supervised_retrieval import predict as incumbent_predict

MARKER = 's3_11_intent_return_12m_lbl'
SHARES = (0., .25, .5)
SPLIT_SEED = 5701
TREE_PARAMETERS = dict(max_iter=40, max_leaf_nodes=15, learning_rate=.1,
                       l2_regularization=1., early_stopping=False,
                       random_state=0, max_bins=255)


def layout(schema):
    records = schema['items']
    predicted = [n for n, r in records.items() if r['class'] == 'PREDICT']
    parents = {r['gate']['parent'] for r in records.values() if r.get('gate')}
    leaves = [n for n in predicted if records[n].get('gate') and n not in parents]
    given = [n for n, r in records.items() if r['class'] == 'GIVEN']
    return predicted, leaves, given


def split_visible(visible):
    shuffled = np.random.default_rng(SPLIT_SEED).permutation(visible)
    count = min(1200, len(visible) // 5)
    return (np.sort(shuffled[2 * count:]), np.sort(shuffled[:count]),
            np.sort(shuffled[count:2 * count]))


def features(frame, schema, given):
    if not given or any(len(schema['items'][n]['values']) > 255 for n in given):
        return None
    values = np.column_stack([frame[n].map({v: i for i, v in enumerate(schema['items'][n]['values'])})
                              .to_numpy(dtype=float) for n in given])
    return values if np.isfinite(values).all() else None


def fit_trees(masked, schema, query, leaves):
    predicted, _, given = layout(schema)
    missing = masked[predicted].isna().to_numpy()
    if not np.array_equal(np.flatnonzero(missing.any(1)), query) or not missing[query].all():
        raise ValueError('Whole non-fit target block masking required')
    visible = np.flatnonzero(~missing.any(1))
    x = features(masked, schema, given)
    if x is None:
        raise ValueError('Unsupported GIVEN vocabulary')
    result, details = {}, {}
    with threadpool_limits(limits=2):
        for name in leaves:
            options = schema['items'][name]['values']
            asked = visible[masked.iloc[visible][name].ne(schema['gated_value']).to_numpy()]
            encoded = masked.iloc[asked][name].map({v: i for i, v in enumerate(options)})
            if encoded.isna().any():
                raise ValueError(f'Invalid answer code: {name}')
            labels = encoded.to_numpy(dtype=int)
            counts = np.bincount(labels, minlength=len(options))
            trained = len(asked) >= 100 and np.count_nonzero(counts) >= 2
            details[name] = {'asked_rows': len(asked), 'observed_classes': int(np.count_nonzero(counts)),
                             'trained': bool(trained)}
            if not trained:
                result[name] = None
                continue
            tree = HistGradientBoostingClassifier(**TREE_PARAMETERS, categorical_features=[True] * len(given))
            tree.fit(x[asked], labels)
            probability = np.zeros((len(query), len(options)))
            probability[:, np.asarray(tree.classes_, dtype=int)] = tree.predict_proba(x[query])
            result[name] = .99 * probability + .01 * (counts + 1) / (counts.sum() + len(options))
    return result, details


def mix_content(p, q, alpha):
    if alpha == 0 or q is None:
        return p
    mass = p[:, :-1].sum(1)
    changed = p.copy()
    rows = mass > 0
    changed[rows, :-1] = (1 - alpha) * p[rows, :-1] + alpha * mass[rows, None] * q[rows]
    return changed


def validate_vectors(raw, predicted, query, records):
    if len(raw) != len(predicted) * len(query):
        raise ValueError('Output length or schema order contract failed')
    for j, name in enumerate(predicted):
        width = len(records[name]['values']) + bool(records[name].get('gate'))
        p = np.asarray(raw[j::len(predicted)], dtype=float)
        if p.shape != (len(query), width) or not np.isfinite(p).all() or (p < 0).any() or (p.sum(1) <= 0).any():
            raise ValueError(f'Invalid probability vectors: {name}')


def apply_policy(raw, predicted, query, trees, shares):
    if not any(a and trees.get(n) is not None for n, a in shares.items()):
        return raw
    output = list(raw)
    for name, alpha in shares.items():
        q = trees.get(name)
        if alpha == 0 or q is None:
            continue
        j = predicted.index(name)
        p = np.stack(raw[j::len(predicted)])
        changed = mix_content(p, q, alpha)
        np.testing.assert_array_equal(p[:, -1], changed[:, -1])
        np.testing.assert_allclose(p.sum(1), changed.sum(1), atol=1e-12, rtol=0)
        for i in np.flatnonzero(p[:, :-1].sum(1) > 0):
            output[int(i) * len(predicted) + j] = changed[i]
    return output


def mean_se(difference):
    return (float(np.mean(difference)),
            float(np.std(difference, ddof=1) / np.sqrt(len(difference))))


def choose_shares(base, trees, frame, schema, positions, query_index, leaves):
    shares, diagnostics = {}, {}
    at = query_index[positions]
    for name in leaves:
        q = trees[name]
        if q is None:
            shares[name] = 0.
            diagnostics[name] = {'reason': 'sparse_or_constant'}
            continue
        options = list(schema['items'][name]['values']) + [schema['gated_value']]
        labels = frame.iloc[positions][name].map({v: i for i, v in enumerate(options)}).to_numpy(dtype=int)
        p = base[name][at]
        logs = [np.log(floor_mix(mix_content(p, q[at], a))[np.arange(len(at)), labels]) for a in SHARES]
        choice = int(np.argmax([v.mean() for v in logs]))
        gain, se = mean_se(logs[choice] - logs[0])
        shares[name] = SHARES[choice] if gain > 0 and gain > 2 * se else 0.
        diagnostics[name] = {'proposed': SHARES[choice], 'gain_log': gain, 'se': se}
    return shares, diagnostics


def validate_policy(base, trees, shares, frame, schema, positions, query_index, predicted):
    at = query_index[positions]
    difference = np.zeros(len(at))
    for name, alpha in shares.items():
        if alpha == 0:
            continue
        options = list(schema['items'][name]['values']) + [schema['gated_value']]
        labels = frame.iloc[positions][name].map({v: i for i, v in enumerate(options)}).to_numpy(dtype=int)
        p = base[name][at]
        before = floor_mix(p)
        after = floor_mix(mix_content(p, trees[name][at], alpha))
        difference += np.log(after[np.arange(len(at)), labels]) - np.log(before[np.arange(len(at)), labels])
    u = np.mean([np.log(len(schema['items'][n]['values']) + bool(schema['items'][n].get('gate'))) for n in predicted])
    difference /= len(predicted) * u
    gain, se = mean_se(difference)
    return {'gain_skill': gain, 'se_skill': se, 'accepted': bool(gain > 0 and gain > 2 * se),
            'rows': len(positions), 'paired_difference': difference}


def predict(frame, schema, *, base_predict=None, observer=None):
    base_predict = incumbent_predict if base_predict is None else base_predict

    def emit(event, payload):
        if observer is not None:
            observer(event, payload)

    def fit_call(stage, function, *args):
        started = perf_counter()
        emit('fit_start', {'stage': stage})
        try:
            return function(*args)
        finally:
            emit('fit_end', {'stage': stage, 'seconds': perf_counter() - started})

    def fallback(reason):
        emit('fallback', {'reason': reason})
        return fit_call('final_base', base_predict, frame, schema)

    predicted, leaves, given = layout(schema)
    if MARKER not in schema['items']:
        return fallback('other_instrument')
    if not leaves:
        return fallback('no_gated_leaf')
    work = frame.reset_index(drop=True).copy()
    missing = work[predicted].isna().to_numpy()
    query = np.flatnonzero(missing.any(1))
    visible = np.flatnonzero(~missing.any(1))
    if not len(query) or not missing[query].all():
        return fallback('unsupported_missingness')
    if features(work, schema, given) is None:
        return fallback('unsupported_given')
    fit, selection, validation = split_visible(visible)
    if len(visible) < 2000 or min(len(selection), len(validation)) < 200:
        return fallback('small_visible_sample')
    shadow = work.copy()
    shadow_query = np.setdiff1d(np.arange(len(work)), fit)
    shadow.loc[shadow_query, predicted] = np.nan
    emit('split', {'fit': fit, 'selection': selection, 'validation': validation, 'query': query,
                   'shadow_query': shadow_query, 'masked_frame': shadow})
    raw_shadow = fit_call('shadow_base', base_predict, shadow, schema)
    validate_vectors(raw_shadow, predicted, shadow_query, schema['items'])
    trees, shadow_details = fit_call('shadow_trees', fit_trees, shadow, schema, shadow_query, leaves)
    base = {name: np.stack(raw_shadow[j::len(predicted)]) for j, name in enumerate(predicted)}
    emit('shadow_frozen', {'base': base, 'trees': trees, 'query': shadow_query, 'details': shadow_details})
    query_index = np.full(len(work), -1, dtype=int)
    query_index[shadow_query] = np.arange(len(shadow_query))
    shares, selection_details = choose_shares(base, trees, work, schema, selection, query_index, leaves)
    emit('selection_frozen', {'shares': shares.copy(), 'details': selection_details})
    if any(shares.values()):
        validation_result = validate_policy(base, trees, shares, work, schema, validation, query_index, predicted)
        emit('validation_scored', validation_result)
        if not validation_result['accepted']:
            shares = dict.fromkeys(leaves, 0.)
    emit('policy_frozen', {'shares': shares.copy()})
    # The independent-validation decision is now fixed. Refit sees all visible
    # labels, including selection/validation; it never changes these shares.
    raw_full = fit_call('final_base', base_predict, work, schema)
    validate_vectors(raw_full, predicted, query, schema['items'])
    full_trees, full_details = fit_call('refit_trees', fit_trees, work, schema, query, leaves)
    emit('refit_frozen', {'base': raw_full, 'trees': full_trees, 'query': query, 'details': full_details,
                          'shadow_query_index': query_index[query]})
    output = apply_policy(raw_full, predicted, query, full_trees, shares)
    validate_vectors(output, predicted, query, schema['items'])
    emit('final', {'base': raw_full, 'output': output, 'shares': shares.copy()})
    return output
