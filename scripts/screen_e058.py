"""E058 diagnostic only: one fixed donor-pair library, staged label access."""

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import pickle
import subprocess
import sys
import threading
import time
from types import FunctionType

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.check_e057 import MemoryTree

OUT = ROOT / 'docs/analysis/E058-outputs'
LOCAL = ROOT / 'external/e058'
SOURCE = ROOT / 'external/sipp-2023/a014-month12-restricted.parquet'
REGISTRATION = ROOT / 'docs/experiments/E058-donor-pair-interactions.md'
SHARES = (0., .25, .5)
DEADLINE = datetime(2026, 9, 26, 11, 36, tzinfo=timezone.utc).timestamp()


def load_numerical():
    global np, pd, ds, softmax, minimize, retrieval, hh_cap, cached_renderer, floor_mix
    for name in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
        os.environ[name] = '2'
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    import numpy as np
    import pandas as pd
    import pyarrow.dataset as ds
    from scipy.special import softmax
    from scipy.optimize import minimize
    import torch
    torch.set_num_threads(2)
    from src.models import supervised_retrieval as retrieval, hh_cap
    from src.eval.recursive_candidates import cached_renderer
    from src.eval.logloss import floor_mix


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)


def blob(path, value):
    with Path(path).open('xb') as stream:
        pickle.dump(value, stream, protocol=5)
    return sha(path)


def key_filter(keys):
    expression = None
    for pnum, block in keys.groupby('PNUM', sort=True):
        term = (ds.field('PNUM') == pnum) & ds.field('SSUID').isin(block.SSUID.tolist())
        expression = term if expression is None else expression | term
    if expression is None:
        raise ValueError('Empty permitted key set')
    return expression


def load_rows(keys, responses):
    from scripts.audit_a014_sipp import FIELDS, GIVEN
    columns = FIELDS if responses else ['SSUID', 'PNUM'] + GIVEN
    # Exact pair filtering occurs inside the scan; never return other roles'
    # responses into Python and then discard them after reading.
    raw = ds.dataset(SOURCE, format='parquet').to_table(columns=columns, filter=key_filter(keys)).to_pandas()
    index = pd.MultiIndex.from_frame(raw[['SSUID', 'PNUM']])
    wanted = pd.MultiIndex.from_frame(keys[['SSUID', 'PNUM']])
    if not index.is_unique or set(index) != set(wanted):
        raise ValueError('Response/key boundary mismatch')
    return raw.set_index(['SSUID', 'PNUM']).loc[wanted].reset_index()


def query_frame(raw):
    from scripts.screen_e055 import GIVEN_VOCAB, TARGETS
    frame = raw[list(GIVEN_VOCAB)].copy()
    for name in ('EEDUC', 'EMS'):
        frame[name] = frame[name].replace('', 'MISSING')
    for name, vocabulary in GIVEN_VOCAB.items():
        if not frame[name].isin(vocabulary).all():
            raise ValueError('Invalid query GIVEN vocabulary')
    for name in TARGETS:
        frame[name] = np.nan
    return frame.reset_index(drop=True)


def partition(frame, predicted):
    missing = frame[predicted].isna().to_numpy()
    query = np.flatnonzero(missing.any(1))
    if not len(query) or not missing[query].all():
        raise ValueError('Whole query block masking required')
    return np.flatnonzero(~missing.any(1)), query


def check_donors(donors, visible):
    if not np.isin(donors, visible).all():
        raise ValueError('Hidden response entered donor bank')


def pair_features(features):
    return np.stack([features[..., j] * features[..., k]
                     for j in range(features.shape[-1]) for k in range(j + 1, features.shape[-1])], axis=-1)


def posterior(features, weights, beta):
    scores = np.einsum('qkd,d->qk', features, weights)
    scores = scores + np.einsum('qkb,b->qk', pair_features(features), beta)
    return softmax(scores, axis=1)


def objective(beta, features, matches, prior, sizes, weights, share):
    pairs = pair_features(features)
    post = posterior(features, weights, beta)
    evidence = np.einsum('qk,qki->qi', post, matches)
    scale = 1 - .001 * np.asarray(sizes)
    p = .001 + scale * ((1 - share) * prior + share * evidence)
    value = -np.log(p).mean() + .01 * np.sum(beta ** 2)
    derivative = -scale / p / p.size
    donor_gradient = np.einsum('qi,qki->qk', share * derivative, matches)
    score_gradient = post * (donor_gradient - (post * donor_gradient).sum(1, keepdims=True))
    gradient = np.einsum('qk,qkb->b', score_gradient, pairs) + .02 * beta
    return float(value), gradient


def capture_layer(frame, schema, model, state):
    predicted = [n for n, rec in schema['items'].items() if rec['class'] == 'PREDICT']
    visible, query = partition(frame, predicted)
    if state:
        raise ValueError('Second first-stage fit forbidden')
    state.update(visible=visible, query=query, predicted=predicted, donor_calls=[])
    namespace = retrieval.supervised_layer.__globals__.copy()
    namespace['LAST_DIAGNOSTICS'] = {}

    def saved(name, function):
        def call(*args, **kwargs):
            if name in state:
                raise ValueError('Repeated first-stage component')
            value = function(*args, **kwargs)
            state[name] = deepcopy(value)
            if name == 'sections':
                state['metric_arguments'] = deepcopy(args)
            return value
        return call

    def guarded_candidates(kind):
        def call(codes, weights, queries, bank, **kwargs):
            check_donors(bank, visible)
            donors = retrieval.candidate_indices(codes, weights, queries, bank, **kwargs)
            check_donors(donors, visible)
            if np.any(donors == np.asarray(queries)[:, None]):
                raise ValueError('Self donor')
            state['donor_calls'].append({'kind': kind, 'query': np.array(queries), 'bank': np.array(bank), 'donors': donors.copy()})
            return donors
        return call

    metric_ns = retrieval.fit_sections.__globals__.copy()
    metric_ns['candidate_indices'] = guarded_candidates('metric')
    metric = FunctionType(retrieval.fit_sections.__code__, metric_ns, argdefs=retrieval.fit_sections.__defaults__)
    replace_ns = retrieval._replace_evidence.__globals__.copy()
    replace_ns['candidate_indices'] = guarded_candidates('section')
    namespace['_replace_evidence'] = FunctionType(retrieval._replace_evidence.__code__, replace_ns,
                                                 argdefs=retrieval._replace_evidence.__defaults__)
    namespace['_sig_data_all'] = saved('signature', namespace['_sig_data_all'])
    namespace['estimate_weights'] = saved('initial', namespace['estimate_weights'])
    namespace['fit_sections'] = saved('sections', metric)
    layer = FunctionType(retrieval.supervised_layer.__code__, namespace, argdefs=retrieval.supervised_layer.__defaults__)
    legacy, lambdas = layer(frame, schema, model)
    state.update(legacy=legacy, lambdas=lambdas, diagnostics=deepcopy(namespace['LAST_DIAGNOSTICS']))
    state['active'] = state['sections'][1]
    args = state['metric_arguments']
    if any(not np.isin(args[i], visible).all() for i in (2, 3, 4)) or (args[1][query] != -1).any():
        raise ValueError('Hidden labels reached metric fitting')
    return legacy, lambdas


def fit_beta(state):
    codes, labels, bank, fit, select, initial, sizes, groups = state['metric_arguments']
    calls = [d for d in state['donor_calls'] if d['kind'] == 'metric']
    if len(calls) != 1:
        raise ValueError('Metric candidate call count changed')
    np.testing.assert_array_equal(calls[0]['query'], np.concatenate([fit, select]))
    donors = calls[0]['donors'][:len(fit)]
    features = (codes[fit, None] == codes[donors]).astype(float)
    if donors.shape[1] != 32 or features.shape[-1] != 6:
        raise ValueError('Registered K32/GIVEN6 family mismatch')
    result, details = {}, {}
    for group in state['active']:
        ix = np.asarray(groups[group])
        matches = (labels[donors][:, :, ix] == labels[fit][:, None, ix]).astype(float)
        prior = []
        for j in ix:
            counts = np.bincount(labels[bank, j], minlength=sizes[j]) + .5
            prior.append((counts / counts.sum())[labels[fit, j]])
        weights = state['sections'][0][group]
        share = state['sections'][2][group]['new_share']
        solution = minimize(objective, np.zeros(15), args=(features, matches, np.stack(prior, axis=1),
            np.asarray(sizes)[ix], weights, share), jac=True, method='L-BFGS-B', bounds=[(-2., 2.)] * 15,
            options={'maxiter': 50, 'ftol': 1e-7})
        if not np.isfinite(solution.x).all() or not np.isfinite(solution.fun) or np.max(np.abs(solution.x)) > 2:
            raise ValueError('Invalid beta optimizer output')
        result[group] = solution.x.copy()
        details[str(group)] = {'beta': solution.x.tolist(), 'iterations': int(solution.nit),
            'optimizer_success': bool(solution.success), 'message': str(solution.message),
            'fixed_share': float(share), 'fixed_weights': weights.tolist(), 'fit_rows': len(fit)}
    return result, details


def replace_evidence(frame, schema, state, betas):
    if not state['active'] or not state['legacy']:
        return state['legacy']
    records, items, options = retrieval._layout(frame, schema)
    query = state['query']
    calls = [d for d in state['donor_calls'] if d['kind'] == 'section' and np.array_equal(d['query'], query)]
    if len(calls) != 1:
        raise ValueError('Missing frozen query donor32 set')
    donors = calls[0]['donors']
    check_donors(donors, state['visible'])
    codes = state['signature'][0]
    features = (codes[query, None] == codes[donors]).astype(float)
    changed = deepcopy(state['legacy'])
    groups = state['metric_arguments'][7]
    for group in state['active']:
        names = [state['predicted'][j] for j in groups[group]]
        post = posterior(features, state['sections'][0][group], betas[group])
        values = retrieval._evidence(frame, names, records, options, list(zip(donors, post)), query)
        for i, row in enumerate(query):
            # Retain original availability and concentration; no dormant activation.
            if int(row) in changed:
                changed[int(row)][0].update({n: values[n][i] for n in names})
    return changed


def mix(base, candidate, alpha):
    return base if alpha == 0 else {n: (1 - alpha) * p + alpha * candidate[n] for n, p in base.items()}


def log_rows(vectors, labels):
    return np.column_stack([np.log(floor_mix(p)[np.arange(len(p)), labels[n]]) for n, p in vectors.items()]).mean(1)


def cluster_mean_se(difference, groups):
    _, inverse = np.unique(groups, return_inverse=True)
    counts = np.bincount(inverse)
    sums = np.bincount(inverse, weights=difference)
    mean = float(np.mean(difference))
    se = np.sqrt(len(counts) / (len(counts) - 1) * np.sum((sums - counts * mean)**2) / len(difference)**2) if len(counts) >= 2 else np.inf
    return mean, float(se)


def choose(logs, groups):
    index = int(np.argmax(logs.mean(1)))
    gain, se = cluster_mean_se(logs[index] - logs[0], groups)
    alpha = SHARES[index] if gain > 0 and gain > 2 * se else 0.
    return {'alpha': alpha, 'proposed_alpha': SHARES[index], 'paired_log_gain': gain, 'cluster_se': se,
            'gate': 'AUDIT' if alpha else 'STOP_NO_INTERVENTION'}


def bootstrap(delta, groups):
    _, inverse = np.unique(groups, return_inverse=True)
    counts = np.bincount(inverse)
    sums = np.bincount(inverse, weights=delta)
    draws = np.random.default_rng(5801).integers(0, len(counts), (2000, len(counts)))
    values = sums[draws].sum(1) / counts[draws].sum(1)
    return np.quantile(values, [.025, .975])


def allow_stage(stage, prior):
    if stage in ('selection', 'audit') and prior.get('oracle', {}).get('gate') != 'SELECT':
        raise ValueError('Oracle did not authorize selection')
    if stage == 'audit' and prior.get('selection', {}).get('alpha', 0) == 0:
        raise ValueError('Zero policy cannot open audit')


def preflight():
    if OUT.exists() or LOCAL.exists():
        raise FileExistsError('Existing E058 artifacts')
    audit = read(ROOT / 'docs/analysis/A019-outputs/entry-audit.json')
    assert audit['status'] == 'PASS' and sha(SOURCE) == audit['source_sha256']
    for name, expected in audit['local_key_hashes'].items():
        assert sha(ROOT / 'external/a019' / name) == expected
    snapshot = ROOT / 'submissions/2026-09-19-E041/main.py'
    assert sha(snapshot) == '22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073'
    prior_sources = read(ROOT / 'docs/analysis/E056-outputs/manifest.json')['source_code_sha256']
    for path, expected in prior_sources.items():
        assert sha(ROOT / path) == expected, path
    files = list((ROOT / 'src').rglob('*.py')) + [Path(__file__), ROOT / 'scripts/screen_e055.py',
        ROOT / 'scripts/audit_a014_sipp.py', ROOT / 'scripts/check_e057.py', ROOT / 'tests/test_e058_interactions.py', snapshot]
    OUT.mkdir(parents=True)
    LOCAL.mkdir(parents=True)
    save(OUT / 'preflight.json', {'source_hashes': {p.relative_to(ROOT).as_posix(): sha(p) for p in files},
        'data_sha256': sha(SOURCE), 'audit_sha256': sha(ROOT / 'docs/analysis/A019-outputs/entry-audit.json'),
        'key_hashes': audit['local_key_hashes'], 'registration_sha256': sha(REGISTRATION),
        'research_deadline_utc': '2026-09-26T11:36:00Z', 'first_stage_cache_reused': False,
        'verified_prior_source_count': len(prior_sources)})
    (OUT / 'registration.md').write_bytes(REGISTRATION.read_bytes())
    print('Preflight PASS; no labels or fits')


def validate_preflight():
    manifest = read(OUT / 'preflight.json')
    for path, expected in manifest['source_hashes'].items():
        assert sha(ROOT / path) == expected, path
    assert sha(SOURCE) == manifest['data_sha256']
    for name, expected in manifest['key_hashes'].items():
        assert sha(ROOT / 'external/a019' / name) == expected
    assert sha(OUT / 'registration.md') == manifest['registration_sha256']
    return manifest


def freeze(monitor):
    from scripts.screen_e055 import make_adapter, TARGETS
    from src.eval.recursive_candidates import _mapped
    fit_keys = pd.read_parquet(ROOT / 'external/a019/fit-keys.parquet')
    evaluation = pd.read_parquet(ROOT / 'external/a019/evaluation-keys.parquet')
    assert len(fit_keys) == 5922 and len(evaluation) == 5999
    assert not set(fit_keys.SSUID) & set(evaluation.SSUID)
    fit_frame, schema = make_adapter(load_rows(fit_keys, responses=True))
    hidden = query_frame(load_rows(evaluation, responses=False))
    frame = pd.concat([fit_frame, hidden], ignore_index=True)
    visible, query = partition(frame, TARGETS)
    np.testing.assert_array_equal(visible, np.arange(5922))
    masked_hash = blob(LOCAL / 'masked-frame.pkl', (schema, frame))
    render, state = cached_renderer(), {}
    monitor['fit_start'] = time.perf_counter()
    before = time.perf_counter()
    baseline = render(frame, schema, layer_fn=lambda f, s, m: capture_layer(f, s, m, state), configs=hh_cap.CONFIGS)
    monitor['fit_seconds'] += time.perf_counter() - before
    monitor['fit_start'] = None
    first_stage_hash = blob(LOCAL / 'first-stage.pkl', {'state': state, 'baseline': baseline})
    zeros = {g: np.zeros(15) for g in state['active']}
    zero_evidence = replace_evidence(frame, schema, state, zeros)
    zero = render(frame, schema, layer_fn=lambda *a: (zero_evidence, state['lambdas']), configs=hh_cap.CONFIGS)
    if len(zero) != len(baseline) or not all(np.array_equal(a, b) for a, b in zip(zero, baseline)):
        raise ValueError('beta=0 raw endpoint parity failed')
    monitor['fit_start'] = time.perf_counter()
    before = time.perf_counter()
    betas, beta_details = fit_beta(state)
    monitor['fit_seconds'] += time.perf_counter() - before
    monitor['fit_start'] = None
    changed_evidence = replace_evidence(frame, schema, state, betas)
    candidate = render(frame, schema, layer_fn=lambda *a: (changed_evidence, state['lambdas']), configs=hh_cap.CONFIGS)
    base, new, endpoint = (_mapped(raw, TARGETS, query) for raw in (baseline, candidate, zero))
    for raw in (base, new, endpoint):
        for name, p in raw.items():
            width = 2 if name == TARGETS[0] else 3
            assert p.shape == (5999, width) and np.isfinite(p).all() and (p >= 0).all() and (p.sum(1) > 0).all()
    before_bucket = [v[1] for v in state['legacy'].values()]
    assert before_bucket == [v[1] for v in changed_evidence.values()]
    arrays = {f'{prefix}/{n}': p for prefix, obj in [('base', base), ('candidate', new), ('zero', endpoint)] for n, p in obj.items()}
    arrays.update(roles=evaluation.role.to_numpy(dtype=str), groups=evaluation.SSUID.to_numpy(dtype=str))
    with (LOCAL / 'library.npz').open('xb') as stream:
        np.savez_compressed(stream, **arrays)
    result = {'library_sha256': sha(LOCAL / 'library.npz'), 'masked_sha256': masked_hash,
        'first_stage_sha256': first_stage_hash, 'fit_rows': len(visible), 'query_rows': len(query),
        'predicted': TARGETS, 'schema': schema, 'active_sections': [int(g) for g in state['active']],
        'section_diagnostics': state['diagnostics'], 'beta_details': beta_details,
        'beta0_raw_exact': True, 'vectors': len(baseline), 'changed_candidate_vectors': sum(int(np.any(base[n] != new[n], axis=1).sum()) for n in TARGETS),
        'concentration_counts': {'diffuse': before_bucket.count(False), 'concentrated': before_bucket.count(True)},
        'frozen_lambdas': state['lambdas'], 'new_e041_fits': 1, 'fit_seconds': monitor['fit_seconds'],
        'versions': {'python': sys.version, 'numpy': np.__version__, 'pandas': pd.__version__},
        'evaluation_labels_read': False}
    save(OUT / 'library.json', result)
    print(json.dumps({k: result[k] for k in ('active_sections', 'beta_details', 'vectors', 'changed_candidate_vectors', 'fit_seconds')}), flush=True)


def evaluate(stage):
    from scripts.screen_e055 import make_adapter
    prior = {name: read(OUT / f'{name}.json') for name in ('oracle', 'selection') if (OUT / f'{name}.json').exists()}
    allow_stage(stage, prior)
    manifest = read(OUT / 'library.json')
    assert sha(LOCAL / 'library.npz') == manifest['library_sha256']
    keys = pd.read_parquet(ROOT / 'external/a019/evaluation-keys.parquet')
    selected_keys = keys.loc[keys.role.eq(stage)]
    take = np.flatnonzero(keys.role.eq(stage))
    with np.load(LOCAL / 'library.npz', allow_pickle=False) as library:
        np.testing.assert_array_equal(library['roles'], keys.role.to_numpy(dtype=str))
        np.testing.assert_array_equal(library['groups'], keys.SSUID.to_numpy(dtype=str))
        base = {n: library[f'base/{n}'][take] for n in manifest['predicted']}
        candidate = {n: library[f'candidate/{n}'][take] for n in manifest['predicted']}
    save(LOCAL / f'{stage}-opened.json', {'library_sha256': manifest['library_sha256'], 'role': stage})
    frame, schema = make_adapter(load_rows(selected_keys, responses=True))
    labels = {n: frame[n].map({v: i for i, v in enumerate(schema['items'][n]['values'] +
        ([schema['gated_value']] if schema['items'][n].get('gate') else []))}).to_numpy(dtype=int) for n in base}
    shares = (0., prior['selection']['alpha']) if stage == 'audit' else SHARES
    logs = np.stack([log_rows(mix(base, candidate, alpha), labels) for alpha in shares])
    groups = selected_keys.SSUID.to_numpy(dtype=str)
    with (LOCAL / f'{stage}-scores.npz').open('xb') as stream:
        np.savez_compressed(stream, logs=logs, shares=np.asarray(shares), groups=groups)
    u = float(np.mean([np.log(p.shape[1]) for p in base.values()]))
    if stage == 'oracle':
        gain = float((logs.mean(1).max() - logs[0].mean()) / u)
        result = {'delta_skill': gain, 'best_alpha': SHARES[int(np.argmax(logs.mean(1)))],
            'baseline_skill': float(1 + logs[0].mean() / u), 'arm_skills': (1 + logs.mean(1) / u).tolist(),
            'gate': 'SELECT' if gain > 1e-10 else 'STOP_FINITE_LIBRARY'}
    elif stage == 'selection':
        result = choose(logs, groups)
    else:
        delta = (logs[1] - logs[0]) / u
        interval = bootstrap(delta, groups)
        chosen = mix(base, candidate, shares[1])
        changed = sum(int(np.any(base[n] != chosen[n], axis=1).sum()) for n in base)
        result = {'alpha': shares[1], 'delta_skill': float(delta.mean()), 'bootstrap_95': interval.tolist(),
            'bootstrap_seed': 5801, 'bootstrap_draws': 2000, 'baseline_skill': float(1 + logs[0].mean() / u),
            'selected_skill': float(1 + logs[1].mean() / u), 'changed_vectors': changed,
            'changed_fraction': changed / (len(take) * 7),
            'gate': 'FOLLOWUP_UNHCR_RESEARCH' if delta.mean() > 0 and interval[0] > 0 else 'STOP_NONPOSITIVE_OR_INCONCLUSIVE'}
    result.update(role=stage, persons=len(take), ssuids=len(np.unique(groups)), uniform_reference=u,
        library_sha256=manifest['library_sha256'], scores_sha256=sha(LOCAL / f'{stage}-scores.npz'))
    save(OUT / f'{stage}.json', result)
    print(json.dumps(result), flush=True)


def worker(stage):
    start = time.perf_counter()
    memory = MemoryTree(os.getpid())
    peak = memory.sample()
    state = {'fit_seconds': 0., 'fit_start': None}
    done = threading.Event()
    def watch():
        while not done.wait(.2):
            try:
                for name, amount in memory.sample().items():
                    peak[name] = max(peak[name], amount)
                fit = state['fit_seconds'] + (time.perf_counter() - state['fit_start'] if state['fit_start'] else 0)
                reason = 'memory' if max(peak.values()) >= 8 * 1024**3 else 'fit' if fit >= 1200 else 'wall' if time.time() >= DEADLINE or time.perf_counter()-start >= 3600 else None
            except Exception as error:
                reason = 'monitor_' + type(error).__name__
            if reason:
                save(OUT / f'{stage}-abort.json', {'reason': reason, 'seconds': time.perf_counter()-start, 'fit': state['fit_seconds'], 'memory': peak})
                os._exit(3)
    threading.Thread(target=watch, daemon=True).start()
    try:
        load_numerical()
        validate_preflight()
        if stage == 'library':
            freeze(state)
        else:
            evaluate(stage)
    finally:
        done.set()
        if state['fit_start'] is not None:
            state['fit_seconds'] += time.perf_counter() - state['fit_start']
            state['fit_start'] = None
        for name, amount in memory.sample().items():
            peak[name] = max(peak[name], amount)
        save(OUT / f'{stage}-resources.json', {'worker_seconds': time.perf_counter()-start,
            'fit_seconds': state['fit_seconds'], 'peak_bytes': peak})


def run(stage):
    if (LOCAL / f'{stage}-started.json').exists() or (OUT / f'{stage}.json').exists():
        raise FileExistsError('Refusing repeated stage')
    save(LOCAL / f'{stage}-started.json', {'stage': stage, 'start_utc': datetime.now(timezone.utc).isoformat()})
    start = time.perf_counter()
    reason = 'COMPLETE'
    peak = {'rss': 0, 'commitment': 0}
    with (OUT / f'{stage}-run.log').open('x', encoding='utf-8') as log:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), 'worker', stage], cwd=ROOT,
            stdout=log, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            memory = MemoryTree(os.getpid())  # Include parent harness and all descendants.
        except Exception:
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
            process.wait(timeout=10)
            save(OUT / f'{stage}-runtime.json', {'reason': 'MONITOR_INIT_FAILURE', 'exit_code': process.returncode})
            raise
        while process.poll() is None:
            try:
                for name, amount in memory.sample().items():
                    peak[name] = max(peak[name], amount)
            except OSError:
                if process.poll() is None:
                    reason = 'MONITOR_FAILURE'
            if max(peak.values()) >= 8 * 1024**3:
                reason = 'MEMORY_CAP'
            if time.time() >= DEADLINE or time.perf_counter()-start >= 3600:
                reason = 'TIME_CAP'
            if reason != 'COMPLETE':
                subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
                break
            time.sleep(.2)
        code = process.wait(timeout=10)
    result = {'parent_inclusive_seconds': time.perf_counter()-start, 'peak_tree_bytes': peak, 'reason': reason, 'exit_code': code}
    save(OUT / f'{stage}-runtime.json', result)
    print(json.dumps(result))
    if code or reason != 'COMPLETE':
        raise SystemExit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('preflight', 'run', 'worker'))
    parser.add_argument('stage', nargs='?', choices=('library', 'oracle', 'selection', 'audit'))
    args = parser.parse_args()
    if args.mode == 'preflight':
        preflight()
    elif args.mode == 'run':
        run(args.stage)
    else:
        worker(args.stage)
