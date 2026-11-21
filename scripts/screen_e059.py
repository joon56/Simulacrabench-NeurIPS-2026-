"""E059 fixed-lambda research only; zero base fits, one beta fit, staged labels."""
import argparse
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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.check_e057 import MemoryTree

OUT = ROOT / 'docs/analysis/E059-outputs'
LOCAL = ROOT / 'external/e059'
OLD = ROOT / 'docs/analysis/E058-outputs'
SOURCE = ROOT / 'external/sipp-2023/a014-month12-restricted.parquet'
DEADLINE = datetime(2026, 9, 26, 13, 10, tzinfo=timezone.utc).timestamp()
NAMES = ['HOSPITALIZED', 'EHREAS_DT', 'EHREAS_BIR', 'EHREAS_OS', 'EHREAS_NST', 'EHREAS_OTH', 'EHREAS_COR']
EXPECTED_LAMBDAS = {'EHREAS_BIR': (.1, .1), 'EHREAS_OTH': (0., .1), 'EHREAS_COR': (0., .1)}
ARMS = ('R', 'A_half', 'B_half')


def numerical():
    global np, pd, minimize, pair_features, posterior, objective, cluster_mean_se, key_filter, floor_mix
    for name in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
        os.environ[name] = '2'
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    import numpy as np
    import pandas as pd
    from scipy.optimize import minimize
    from scripts import screen_e058 as previous
    previous.load_numerical()  # Imports only; never invoke an E058 stage or fit.
    pair_features, posterior, objective = previous.pair_features, previous.posterior, previous.objective
    cluster_mean_se, key_filter = previous.cluster_mean_se, previous.key_filter
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


def valid(vectors):
    for name, p in vectors.items():
        if p.ndim != 2 or not np.isfinite(p).all() or (p < 0).any() or (p.sum(1) <= 0).any():
            raise ValueError(f'Invalid raw probability: {name}')


def leaf_replace(base, legacy, replacement, lambdas, bucket):
    result = {n: p.copy() for n, p in base.items()}
    for n, pair in lambdas.items():
        lam = np.asarray(pair)[np.asarray(bucket, dtype=int)]
        take = lam > 0
        result[n][take] = base[n][take] + lam[take, None] * (replacement[n][take] - legacy[n][take])
    valid(result)
    return result


def evidence(labels, donors, post, sizes, visible):
    if not np.isin(donors, visible).all() or (labels[donors] < 0).any():
        raise ValueError('Hidden label or donor outside visible bank')
    result = []
    rows = np.repeat(np.arange(len(donors)), donors.shape[1])
    for j, size in enumerate(sizes):
        if (labels[donors, j] >= size).any():
            raise ValueError('Donor option outside schema')
        p = np.zeros((len(donors), size))
        np.add.at(p, (rows, labels[donors, j].ravel()), post.ravel())
        result.append(p)
    return result


def constant_pairs(features):
    pairs = pair_features(features)
    return bool(np.all(pairs == pairs[:, :1, :]))


def contrasts(logs):
    return np.stack([logs[2] - logs[0], logs[2] - logs[1]])


def upper_bounds(arms):
    names = list(arms['R'])
    u = float(np.mean([np.log(arms['R'][n].shape[1]) for n in names]))
    result = []
    for comparator in ('R', 'A_half'):
        values = [np.max(np.log(floor_mix(arms['B_half'][n]) / floor_mix(arms[comparator][n])), axis=1) for n in names]
        result.append(float(np.column_stack(values).mean() / u))
    return result


def selection_gate(differences, groups):
    stats = [cluster_mean_se(d, groups) for d in differences]
    return {'paired_log_means': [m for m, s in stats], 'cluster_se': [s for m, s in stats],
            'gate': 'AUDIT' if all(m > 0 and m > 2*s for m, s in stats) else 'STOP_SELECTION'}


def bootstrap(differences, groups):
    _, inverse = np.unique(groups, return_inverse=True)
    counts = np.bincount(inverse)
    draws = np.random.default_rng(5801).integers(0, len(counts), (2000, len(counts)))
    return np.stack([np.quantile(np.bincount(inverse, weights=d)[draws].sum(1) / counts[draws].sum(1),
                                 [.0125, .9875], method='linear') for d in differences])


def allow_stage(stage, prior):
    required = {'fit': [('preflight', 'FIT')], 'oracle': [('fit', 'ORACLE')],
                'selection': [('fit', 'ORACLE'), ('oracle', 'SELECT')],
                'audit': [('fit', 'ORACLE'), ('oracle', 'SELECT'), ('selection', 'AUDIT')]}
    for name, gate in required.get(stage, []):
        if prior.get(name, {}).get('gate') != gate:
            raise ValueError(f'{stage} blocked by {name}')


def provenance():
    entry = read(OUT / 'entry.json')
    for path in ('docs/analysis/E059-outputs/registration.md', 'docs/analysis/E059-outputs/user-protocol.txt',
                 'docs/analysis/A020-outputs/verification.json'):
        assert sha(ROOT/path) == entry['hashes'][path], path
    old = read(OLD / 'preflight.json')
    assert len(old['source_hashes']) == 59
    for path, expected in old['source_hashes'].items():
        assert sha(ROOT/path) == expected, path
    check = read(ROOT / 'docs/analysis/A020-outputs/verification.json')
    assert len(check['artifact_checks']) == 5
    for record in check['artifact_checks']:
        assert sha(ROOT/record['path']) == record['sha256'], record['path']
    assert sha(SOURCE) == old['data_sha256']
    assert sha(OLD/'registration.md') == old['registration_sha256']
    if (OUT/'preflight.json').exists():
        for path, expected in read(OUT/'preflight.json')['execution_hashes'].items():
            assert sha(ROOT/path) == expected, path
    return old, check


def preflight(monitor):
    old, check = provenance()  # No cache deserialization before all hashes pass.
    from src.models import supervised_retrieval as retrieval
    from src.eval.retrieval_oracle import candidate_indices
    schema, frame = pickle.loads((ROOT/'external/e058/masked-frame.pkl').read_bytes())
    first = pickle.loads((ROOT/'external/e058/first-stage.pkl').read_bytes())
    state = first['state']
    record = read(OLD/'library.json')
    keys = pd.read_parquet(ROOT/'external/a019/evaluation-keys.parquet')
    fit_keys = pd.read_parquet(ROOT/'external/a019/fit-keys.parquet')
    assert schema == record['schema'] and len(frame) == 11921
    records, items, options = retrieval._layout(frame, schema)
    names = [n for n in items if records[n]['class'] == 'PREDICT']
    given = [n for n in items if records[n]['class'] == 'GIVEN']
    assert names == NAMES == state['predicted'] and len(given) == 6
    assert [len(options[n]) for n in names] == [2, 3, 3, 3, 3, 3, 3]
    assert records[NAMES[0]].get('gate') is None
    assert all(records[n]['gate'] == {'parent': NAMES[0], 'observed_if': ['1']} for n in names[1:])
    assert not any(r.get('gate', {}).get('parent') in EXPECTED_LAMBDAS for r in records.values())
    visible, query = state['visible'], state['query']
    np.testing.assert_array_equal(visible, np.arange(5922))
    np.testing.assert_array_equal(query, np.arange(5922, 11921))
    assert len(keys) == 5999 and len(fit_keys) == 5922
    assert not set(keys.SSUID) & set(fit_keys.SSUID)
    assert not keys.duplicated(['SSUID', 'PNUM']).any() and not fit_keys.duplicated(['SSUID', 'PNUM']).any()
    assert keys.groupby('SSUID').role.nunique().max() == 1
    assert frame.iloc[query][names].isna().all().all() and frame.iloc[visible][names].notna().all().all()
    assert frame[given].notna().all().all()
    counts = {r: [int(keys.role.eq(r).sum()), int(keys.loc[keys.role.eq(r), 'SSUID'].nunique())]
              for r in ('oracle', 'selection', 'audit')}
    assert counts == {'oracle': [1918, 1124], 'selection': [2007, 1130], 'audit': [2074, 1177]}
    codes, labels, bank, fit, select, initial, sizes, groups = state['metric_arguments']
    assert groups == [list(range(7))] and state['active'] == state['sections'][1] == []
    assert state['lambdas'] == EXPECTED_LAMBDAS
    np.testing.assert_array_equal(codes, state['signature'][0])
    actual_codes, _ = retrieval._sig_data_all(frame, records, items)
    np.testing.assert_array_equal(codes, actual_codes)
    encoded = np.column_stack([frame[n].map({v: i for i, v in enumerate(options[n])}).fillna(-1).to_numpy(dtype=int) for n in names])
    np.testing.assert_array_equal(labels, encoded)
    assert (labels[query] == -1).all()
    shuffled = np.random.default_rng(4101).permutation(visible)
    np.testing.assert_array_equal(fit, shuffled[:1184])
    np.testing.assert_array_equal(select, shuffled[1184:1776])
    np.testing.assert_array_equal(bank, shuffled[2368:])
    assert len(shuffled[1776:2368]) == 592
    np.testing.assert_array_equal(initial, state['initial'][0])
    weights = state['sections'][0][0]
    share = state['sections'][2][0]['new_share']
    assert np.isfinite(weights).all() and weights.shape == (6,) and np.isfinite(share) and 0 <= share <= 1
    assert np.isfinite(initial).all() and np.all(initial >= 0)
    assert state['sections'][2] == record['section_diagnostics']['sections']
    calls = state['donor_calls']
    assert len(calls) == 1 and calls[0]['kind'] == 'metric'
    np.testing.assert_array_equal(calls[0]['query'], np.concatenate([fit, select]))
    np.testing.assert_array_equal(calls[0]['bank'], bank)
    metric_donors = calls[0]['donors'][:1184].copy()
    assert metric_donors.shape == (1184, 32) and np.isin(metric_donors, bank).all()
    assert not np.any(metric_donors == fit[:, None])
    assert len(state['legacy']) == len(query)
    buckets = np.array([state['legacy'][int(i)][1] for i in query], dtype=bool)
    assert int(buckets.sum()) == 1720
    legacy = {n: np.stack([state['legacy'][int(i)][0][n] for i in query]) for n in names}
    with np.load(ROOT/'external/e058/library.npz', allow_pickle=False) as previous:
        np.testing.assert_array_equal(previous['roles'], keys.role.to_numpy(dtype=str))
        np.testing.assert_array_equal(previous['groups'], keys.SSUID.to_numpy(dtype=str))
        base = {n: previous[f'base/{n}'].copy() for n in names}
        assert len(first['baseline']) == 41993
        for j, n in enumerate(names):
            np.testing.assert_array_equal(base[n], np.stack(first['baseline'][j::7]))
            np.testing.assert_array_equal(base[n], previous[f'zero/{n}'])
            np.testing.assert_array_equal(base[n], previous[f'candidate/{n}'])
            assert base[n].shape == (5999, sizes[j])
    valid(base)
    valid(legacy)
    # Exactly one new GIVEN-only query donor construction; shared by A and B.
    query_donors = candidate_indices(codes, initial, query, visible, k=32)
    assert query_donors.shape == (5999, 32) and np.isin(query_donors, visible).all()
    assert not np.any(query_donors == query[:, None])
    features = (codes[query, None] == codes[query_donors]).astype(float)
    invariant = constant_pairs(features)  # BIR lambda is positive for every query.
    prepared = dict(base=base, legacy=legacy, buckets=buckets, lambdas=state['lambdas'],
                    labels=labels, visible=visible, query=query, bank=bank, fit=fit,
                    query_donors=query_donors, metric_donors=metric_donors,
                    features=features, metric_features=(codes[fit, None] == codes[metric_donors]).astype(float),
                    weights=weights.copy(), share=share, sizes=sizes, schema=schema,
                    roles=keys.role.to_numpy(dtype=str), groups=keys.SSUID.to_numpy(dtype=str))
    frozen_hash = blob(LOCAL/'prepared.pkl', prepared)
    result = {'gate': 'STOP_PAIR_CONSTANT' if invariant else 'FIT', 'source_hashes_checked': 59,
              'artifact_hashes_checked': 5, 'roles': counts, 'active_original': [],
              'lambdas': state['lambdas'], 'learned_weights': weights.tolist(), 'retrieval_share': float(share),
              'pair_features_all_constant': invariant, 'prepared_sha256': frozen_hash,
              'query_donors_sha256': hashlib.sha256(query_donors.tobytes()).hexdigest(),
              'metric_donors_sha256': hashlib.sha256(metric_donors.tobytes()).hexdigest(),
              'execution_hashes': {p: sha(ROOT/p) for p in ('scripts/screen_e059.py', 'tests/test_e059_interactions.py')},
              'registration_sha256': sha(OUT/'registration.md'), 'data_sha256': old['data_sha256'],
              'artifact_hashes': check['artifact_checks'], 'base_fits': 0, 'beta_fits': 0,
              'new_evaluation_labels_read': False}
    save(OUT/'preflight.json', result)
    print(json.dumps(result), flush=True)


def fit_library(monitor):
    provenance()
    pre = read(OUT/'preflight.json')
    assert sha(LOCAL/'prepared.pkl') == pre['prepared_sha256']
    p = pickle.loads((LOCAL/'prepared.pkl').read_bytes())
    labels, donors, fit, bank = p['labels'], p['metric_donors'], p['fit'], p['bank']
    matches = (labels[donors] == labels[fit, None]).astype(float)
    prior = []
    for j, size in enumerate(p['sizes']):
        counts = np.bincount(labels[bank, j], minlength=size) + .5
        prior.append((counts / counts.sum())[labels[fit, j]])
    save(LOCAL/'beta-started.json', {'start_utc': datetime.now(timezone.utc).isoformat(), 'maximum_calls': 1})
    monitor['fit_start'] = time.perf_counter()
    try:
        solution = minimize(objective, np.zeros(15), args=(p['metric_features'], matches, np.stack(prior, 1),
                            p['sizes'], p['weights'], p['share']), jac=True, method='L-BFGS-B',
                            bounds=[(-2., 2.)]*15, options={'maxiter': 50, 'ftol': 1e-7})
    finally:
        monitor['fit_seconds'] += time.perf_counter() - monitor['fit_start']
        monitor['fit_start'] = None
    assert monitor['fit_seconds'] < 120
    if not np.isfinite(solution.x).all() or not np.isfinite(solution.fun) or np.max(np.abs(solution.x)) > 2:
        raise ValueError('Invalid beta optimizer result')
    if not solution.success and not (solution.status == 1 and solution.nit == 50):
        raise ValueError('Optimizer error outside permitted finite maxiter termination')
    def render(beta):
        post = posterior(p['features'], p['weights'], beta)
        ev = dict(zip(NAMES, evidence(p['labels'], p['query_donors'], post, p['sizes'], p['visible'])))
        return leaf_replace(p['base'], p['legacy'], ev, p['lambdas'], p['buckets']), ev
    additive, ev_a = render(np.zeros(15))
    beta0, _ = render(np.zeros(15))
    pair, ev_b = render(solution.x)
    identity = leaf_replace(p['base'], p['legacy'], p['legacy'], p['lambdas'], p['buckets'])
    max_error = 0.
    for n in NAMES:
        np.testing.assert_array_equal(additive[n], beta0[n])
        np.testing.assert_array_equal(identity[n], p['base'][n])
        if n not in p['lambdas']:
            np.testing.assert_array_equal(additive[n], p['base'][n])
            np.testing.assert_array_equal(pair[n], p['base'][n])
        else:
            lam = np.asarray(p['lambdas'][n])[p['buckets'].astype(int), None]
            core = (p['base'][n] - lam*p['legacy'][n]) / (1-lam)
            for new, ev in ((additive[n], ev_a[n]), (pair[n], ev_b[n])):
                max_error = max(max_error, float(np.max(np.abs(new - ((1-lam)*core+lam*ev)))))
                np.testing.assert_array_equal(new[lam[:, 0] == 0], p['base'][n][lam[:, 0] == 0])
    assert max_error <= 1e-12
    arms = {'R': p['base'], 'A_half': {n: p['base'][n]+.5*(additive[n]-p['base'][n]) for n in NAMES},
            'B_half': {n: p['base'][n]+.5*(pair[n]-p['base'][n]) for n in NAMES}}
    for arm in arms.values():
        valid(arm)
    arrays = {f'{a}/{n}': v for a, values in arms.items() for n, v in values.items()}
    arrays.update(roles=p['roles'], groups=p['groups'])
    with (LOCAL/'library.npz').open('xb') as stream:
        np.savez_compressed(stream, **arrays)
    changed = {c: sum(int(np.any(arms['B_half'][n] != arms[c][n], axis=1).sum()) for n in NAMES) for c in ('R', 'A_half')}
    take = p['roles'] == 'oracle'
    bounds = upper_bounds({a: {n: v[take] for n, v in x.items()} for a, x in arms.items()})
    gate = 'STOP_IDENTITY' if changed['A_half'] == 0 else 'STOP_OUTPUT_BOUND' if min(bounds) <= 1e-10 else 'ORACLE'
    result = {'gate': gate, 'library_sha256': sha(LOCAL/'library.npz'), 'prepared_sha256': pre['prepared_sha256'],
              'execution_hashes': pre['execution_hashes'], 'registration_sha256': pre['registration_sha256'],
              'beta': solution.x.tolist(), 'iterations': int(solution.nit), 'optimizer_success': bool(solution.success),
              'optimizer_status': int(solution.status), 'optimizer_message': str(solution.message),
              'beta_fits': 1, 'base_fits': 0, 'fit_seconds': monitor['fit_seconds'], 'beta0_exact': True,
              'reconstruction_max_abs': max_error, 'changed_B_vectors': changed, 'total_vectors': 41993,
              'oracle_label_free_bounds': bounds, 'new_evaluation_labels_read': False}
    save(OUT/'fit.json', result)
    print(json.dumps(result), flush=True)


def evaluate(stage, monitor):
    provenance()
    from scripts.screen_e058 import load_rows
    from scripts.screen_e055 import make_adapter
    manifest = read(OUT/'fit.json')
    assert sha(LOCAL/'library.npz') == manifest['library_sha256']
    keys = pd.read_parquet(ROOT/'external/a019/evaluation-keys.parquet')
    take = keys.role.eq(stage).to_numpy()
    selected = keys.loc[take]
    with np.load(LOCAL/'library.npz', allow_pickle=False) as library:
        np.testing.assert_array_equal(library['roles'], keys.role.to_numpy(dtype=str))
        np.testing.assert_array_equal(library['groups'], keys.SSUID.to_numpy(dtype=str))
        arms = {a: {n: library[f'{a}/{n}'][take] for n in NAMES} for a in ARMS}
    save(LOCAL/f'{stage}-opened.json', {'stage': stage, 'library_sha256': manifest['library_sha256']})
    frame, schema = make_adapter(load_rows(selected, responses=True))
    assert schema == read(OLD/'library.json')['schema']
    labels = {n: frame[n].map({v: i for i, v in enumerate(schema['items'][n]['values'] +
              ([schema['gated_value']] if schema['items'][n].get('gate') else []))}).to_numpy(dtype=int) for n in NAMES}
    logs = np.stack([np.column_stack([np.log(floor_mix(arms[a][n])[np.arange(len(selected)), labels[n]]) for n in NAMES]).mean(1) for a in ARMS])
    groups = selected.SSUID.to_numpy(dtype=str)
    u = float((np.log(2)+6*np.log(3))/7)
    d = contrasts(logs)
    if stage == 'oracle':
        gain = d.mean(1)/u
        result = {'delta_skill': gain.tolist(), 'gate': 'SELECT' if np.all(gain > 1e-10) else 'STOP_ORACLE'}
    elif stage == 'selection':
        result = selection_gate(d, groups)
    else:
        intervals = bootstrap(d/u, groups)
        result = {'delta_skill': (d.mean(1)/u).tolist(), 'central_97_5_intervals': intervals.tolist(),
                  'bootstrap_draws': 2000, 'bootstrap_seed': 5801,
                  'gate': 'FOLLOWUP_UNHCR_RESEARCH' if np.all(intervals[:, 0] > 0) else 'STOP_AUDIT'}
    with (LOCAL/f'{stage}-scores.npz').open('xb') as stream:
        np.savez_compressed(stream, logs=logs, groups=groups)
    result.update(role=stage, persons=len(selected), ssuids=len(np.unique(groups)),
                  comparison_order=['B_half-R', 'B_half-A_half'], arm_order=list(ARMS),
                  arm_skills=(1+logs.mean(1)/u).tolist(), uniform_reference=u,
                  library_sha256=manifest['library_sha256'], scores_sha256=sha(LOCAL/f'{stage}-scores.npz'))
    save(OUT/f'{stage}.json', result)
    print(json.dumps(result), flush=True)


def worker(stage):
    start = time.perf_counter()
    memory, done = MemoryTree(os.getpid()), threading.Event()
    peak = memory.sample()
    monitor = {'fit_seconds': 0., 'fit_start': None}
    def watch():
        while not done.wait(.2):
            try:
                for k, v in memory.sample().items():
                    peak[k] = max(peak[k], v)
                fit = monitor['fit_seconds'] + (time.perf_counter()-monitor['fit_start'] if monitor['fit_start'] else 0)
                reason = 'memory' if max(peak.values()) >= 8*1024**3 else 'beta_time' if fit >= 120 else 'wall' if time.time() >= DEADLINE else None
            except Exception as error:
                reason = type(error).__name__
            if reason:
                save(OUT/f'{stage}-abort.json', {'reason': reason, 'peak_bytes': peak})
                os._exit(3)
    threading.Thread(target=watch, daemon=True).start()
    try:
        numerical()
        prior = {n: read(OUT/f'{n}.json') for n in ('preflight', 'fit', 'oracle', 'selection') if (OUT/f'{n}.json').exists()}
        allow_stage(stage, prior)
        if stage == 'preflight':
            preflight(monitor)
        elif stage == 'fit':
            fit_library(monitor)
        else:
            evaluate(stage, monitor)
    except Exception as error:
        save(OUT/f'{stage}-error.json', {'gate': 'STOP_TECHNICAL', 'type': type(error).__name__, 'message': str(error)})
        raise
    finally:
        done.set()
        for k, v in memory.sample().items():
            peak[k] = max(peak[k], v)
        save(OUT/f'{stage}-resources.json', {'worker_seconds': time.perf_counter()-start,
                                           'fit_seconds': monitor['fit_seconds'], 'peak_bytes': peak})


def run(stage):
    if time.time() >= DEADLINE:
        raise TimeoutError('Session deadline')
    if list(OUT.glob('*-error.json')) or list(OUT.glob('*-abort.json')):
        raise ValueError('Earlier technical STOP; no retry')
    prior = {n: read(OUT/f'{n}.json') for n in ('preflight', 'fit', 'oracle', 'selection') if (OUT/f'{n}.json').exists()}
    allow_stage(stage, prior)
    if (OUT/f'{stage}.json').exists():
        raise FileExistsError('Completed stage')
    LOCAL.mkdir(exist_ok=True)
    save(LOCAL/f'{stage}-started.json', {'start_utc': datetime.now(timezone.utc).isoformat()})
    start, reason = time.perf_counter(), 'COMPLETE'
    peak = {'rss': 0, 'commitment': 0}
    with (OUT/f'{stage}-run.log').open('x', encoding='utf-8') as log:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), 'worker', stage], cwd=ROOT,
                                   stdout=log, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            memory = MemoryTree(os.getpid())
            while process.poll() is None:
                try:
                    for k, v in memory.sample().items():
                        peak[k] = max(peak[k], v)
                except OSError:
                    if process.poll() is None:
                        reason = 'MONITOR_FAILURE'
                if max(peak.values()) >= 8*1024**3:
                    reason = 'MEMORY_CAP'
                if time.time() >= DEADLINE:
                    reason = 'WALL_CAP'
                if reason != 'COMPLETE':
                    break
                time.sleep(.2)
        finally:
            if process.poll() is None:
                subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
            code = process.wait(timeout=10)
    save(OUT/f'{stage}-runtime.json', {'parent_inclusive_seconds': time.perf_counter()-start,
         'peak_tree_bytes': peak, 'reason': reason, 'exit_code': code})
    if code or reason != 'COMPLETE':
        raise SystemExit(1)
    print(read(OUT/f'{stage}.json')['gate'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('run', 'worker'))
    parser.add_argument('stage', choices=('preflight', 'fit', 'oracle', 'selection', 'audit'))
    args = parser.parse_args()
    (run if args.mode == 'run' else worker)(args.stage)
