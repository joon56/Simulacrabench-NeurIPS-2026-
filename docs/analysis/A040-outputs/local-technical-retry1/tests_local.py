"""Named one-shot engineering checks; no existing baseline execution."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


def raises(kind, call):
    try:
        call()
    except kind:
        return
    raise AssertionError(f"Expected {kind.__name__}")


def fixture(schema, destination):
    rng = np.random.Generator(np.random.PCG64(4000))
    given = [k for k, v in schema['items'].items() if v['class'] == 'GIVEN']
    heads = [k for k, v in schema['items'].items() if v['class'] == 'PREDICT']
    options = {k: v['values'] + ([schema['gated_value']] if v.get('gate') else [])
               for k, v in schema['items'].items() if v['class'] in ('GIVEN', 'PREDICT')}
    frame = pd.DataFrame({k: rng.choice(options[k], 54).astype(object) for k in given})
    for j, name in enumerate(heads):
        frame[name] = np.asarray(options[name], dtype=object)[(np.arange(54) + j) % len(options[name])]
    singleton = heads[0]
    absent = next(k for k in heads[1:] if len(options[k]) == 3)
    frame.loc[:44, singleton] = options[singleton][0]
    frame.loc[:44, absent] = np.asarray(options[absent], dtype=object)[2 * (np.arange(45) % 2)]
    frame.loc[45, given[0]] = '__A040_UNSEEN__'
    frame.loc[46, given[1]] = np.nan
    frame.loc[51:, heads] = np.nan
    text = frame.to_json(orient='split', force_ascii=False)
    destination.write_text(text, encoding='utf-8')
    return frame, given, heads, options, singleton, absent, hashlib.sha256(text.encode()).hexdigest()


def run_tests(p, schema, torch, event, root, counters):
    frame, given, heads, options, singleton, absent, digest = fixture(
        schema, root / 'tmp/a040-local-technical-retry1/fixture.json')
    roles = p.RoleViews(frame, schema, range(45), range(45, 48), range(48, 51), range(51, 54))
    event('fixture', sha256=digest, F=45, S=3, E=3, Q=3, seed=4000)
    assert len(given) == 17 and len(heads) == 213
    assert sum(map(len, (options[k] for k in heads))) == 834
    assert max(len(options[k]) for k in heads) == 15
    assert roles.shadow.loc[45:, heads].isna().all().all()
    assert roles.shadow.loc[:44, heads].equals(frame.loc[:44, heads])
    raises(PermissionError, roles.evaluation)
    raises(PermissionError, lambda: roles.fit_input(heads[0], [45]))
    raises(PermissionError, lambda: roles.fit_input(heads[0], list(range(44)) + [48]))
    event('role_masking', passed=True)

    base = np.array([[.3, .7], [2., 3.]])
    assert p.mix(base, None, 0) is base
    assert p.align(np.array([[.7, .3]]), np.array([2, 0]), 3).tolist() == [[.3, 0., .7]]
    assert np.array_equal(p.floored(np.array([[1., 0., 0.]])), [[.998, .001, .001]])
    for bad in (np.array([[np.nan, 1.]]), np.array([[-.1, 1.1]]), np.array([[0., 0.]])):
        raises(ValueError, lambda bad=bad: p.mix(bad, None, 0))
    raises(ValueError, lambda: p.align(np.array([[1.]]), np.array([3]), 3))
    assert np.array_equal(p.empty_fallback(base), base)

    # Complete-distribution arrays, manufactured independently of neural outputs.
    r = {k: np.full((3, len(options[k])), 1 / len(options[k])) for k in heads}
    q = {k: np.eye(len(options[k]))[np.zeros(3, dtype=int)] for k in heads}
    truth = {k: np.zeros(3, dtype=int) for k in heads}
    assert p.select_alpha(r, r, truth) == 0
    assert p.select_alpha(r, q, truth) == .5
    assert p.independent_check(r, q, truth, .5)[0]
    wrong = {k: np.ones(3, dtype=int) for k in heads}
    assert not p.independent_check(r, q, wrong, .5)[0]
    stage_probe = p.RoleViews(frame, schema, range(45), range(45, 48), range(48, 51), range(51, 54))
    stage_probe.selection()
    stage_probe.freeze(.25)
    assert stage_probe.evaluation()[heads[0]].shape == (3,)
    raises(PermissionError, lambda: stage_probe.freeze(.5))
    event('arithmetic_and_selection', passed=True, actual_E041_executed=False)

    def state_hash(model):
        h = hashlib.sha256()
        for name, value in model.state_dict().items():
            h.update(name.encode())
            h.update(value.detach().cpu().contiguous().numpy().tobytes())
        return h.hexdigest()

    before = state_hash(p.SHARED_MODEL)
    query = roles.shadow.loc[roles.query_rows, given]
    a = next(k for k in heads if len(options[k]) == 15)
    b = next(k for k in heads if len(options[k]) == 11)
    xa, ya = roles.fit_input(a)
    stock = p.TabICLClassifier(**p.OPTIONS)
    stock.fit(xa, ya)
    expected = p.align(stock.predict_proba(query), stock.classes_, len(options[a]))
    adapter_a, actual = p.predict_head(roles, a)
    diff = float(np.max(np.abs(expected - actual)))
    event('stock_adapter', max_abs_diff=diff, exact=bool(np.array_equal(expected, actual)))
    assert np.array_equal(expected, actual), 'Stock/adapter mismatch or nondeterminism'
    del stock
    adapter_b, _ = p.predict_head(roles, b)
    replay = p.align(adapter_a.predict_proba(query), adapter_a.classes_, len(options[a]))
    assert np.array_equal(actual, replay), 'Shared model state contamination'
    fresh, replay2 = p.predict_head(roles, a)
    assert np.array_equal(actual, replay2), 'Fresh-head reproducibility failure'
    assert adapter_a.model_ is adapter_b.model_ is fresh.model_ is p.SHARED_MODEL
    assert adapter_a.X_encoder_ is not adapter_b.X_encoder_
    assert adapter_a.ensemble_generator_ is not adapter_b.ensemble_generator_
    assert adapter_a.model_kv_cache_ is None and adapter_b.model_kv_cache_ is None
    assert adapter_a.ensemble_generator_.y_.shape == (45,)
    event('shared_state_isolation', passed=True)
    del adapter_a, adapter_b, fresh

    predictions = {}
    for name in heads:
        estimator, values = p.predict_head(roles, name)
        assert values.shape == (9, len(options[name]))
        p.valid(values)
        assert np.allclose(values.sum(axis=1), 1, rtol=0, atol=1e-6)
        if name == absent:
            assert np.all(values[:, 1] == 0), 'Unobserved class was not raw zero'
        if name == singleton:
            assert estimator is None and np.all(values[:, 0] == 1)
        if len(options[name]) > 10:
            assert estimator.n_classes_ == len(options[name])
            event('many_class_head', head_name=name, classes=estimator.n_classes_)
        predictions[name] = values
        del estimator
    reordered = roles.shadow.loc[:, list(reversed(roles.shadow.columns))]
    output = p.flatten(reordered, schema, predictions, roles.query_rows)
    assert len(output) == 9 * 213
    assert output[:213] == [predictions[k][0].tolist() for k in heads]
    assert output[-213:] == [predictions[k][-1].tolist() for k in heads]
    selected = p.select_alpha(r, {k: predictions[k][:3] for k in heads}, roles.selection())
    roles.freeze(selected)
    checked, _ = p.independent_check(r, {k: predictions[k][3:6] for k in heads},
                                     roles.evaluation(), selected)
    event('fake_only_decision', alpha=selected, guard_accepted=bool(checked), efficacy_evidence=False)
    assert before == state_hash(p.SHARED_MODEL), 'Frozen model changed'
    assert counters['fits'] == 216 and counters['predicts'] == 217, counters
    assert counters['loads'] == 2, counters
    assert p.COUNTS['adapter_injections'] == 215
    assert p.COUNTS['singleton'] == 1 and p.COUNTS['empty'] == 1
    event('complete_schema_and_frozen_weights', passed=True, targets=213, vectors=len(output))
    return {'heads':213, 'query_rows':9, 'output_vectors':len(output),
            'fixture_sha256':digest, 'stock_adapter_max_abs_diff':diff,
            'frozen_state_sha256':before, 'actual_E041_control_parity':False,
            'arithmetic_control_parity':True, 'counts':dict(counters),
            'prototype_counts':dict(p.COUNTS)}
