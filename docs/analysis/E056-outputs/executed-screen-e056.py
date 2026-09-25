"""E056 fixed conditional-content diagnostic; no production model or upload."""

from __future__ import annotations

import argparse
import ctypes
import gzip
import hashlib
import json
import os
from pathlib import Path
import pickle
import sys
import threading
from time import perf_counter

for variable in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ[variable] = '2'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import HistGradientBoostingClassifier
from threadpoolctl import threadpool_limits

from scripts.screen_e055 import (SOURCE, TARGETS, REASONS, PARENT, GIVEN,
                                 prepare, sample_digest)
from src.eval.logloss import floor_mix
from src.eval.recursive_candidates import TREE_PARAMETERS

LOCAL = ROOT / 'external/e056'
OUT = ROOT / 'docs/analysis/E056-outputs'
REGISTRATION = ROOT / 'docs/experiments/E056-conditional-leaf-content.md'
SHARES = (0., .25, .5)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)


def intervene(p, q, alpha):
    if alpha == 0 or q is None:
        return p
    mass = p[:, :-1].sum(1)
    result = p.copy()
    rows = mass > 0
    result[rows, :-1] = (1 - alpha) * p[rows, :-1] + alpha * mass[rows, None] * q[rows]
    return result


def smooth_tree(probability, classes, counts):
    counts = np.asarray(counts)
    aligned = np.zeros((len(probability), len(counts)))
    aligned[:, np.asarray(classes, dtype=int)] = probability
    return .99 * aligned + .01 * (counts + 1) / (counts.sum() + len(counts))


def fit_trees(masked, schema, query, leaves, monitor=None):
    records = schema['items']
    predicted = [n for n, r in records.items() if r['class'] == 'PREDICT']
    missing = masked[predicted].isna().to_numpy()
    if not np.array_equal(np.flatnonzero(missing.any(1)), query) or not missing[query].all():
        raise ValueError('Whole query block masking required')
    visible = np.flatnonzero(~missing.any(1))
    given = [n for n, r in records.items() if r['class'] == 'GIVEN']
    features = np.column_stack([masked[n].map({v: i for i, v in enumerate(records[n]['values'])})
                                .to_numpy(dtype=float) for n in given])
    if not np.isfinite(features).all() or any(len(records[n]['values']) > 255 for n in given):
        raise ValueError('Unexpected GIVEN vocabulary')
    tree, details = {}, {'given': given, 'heads': {}, 'fit_count': 0, 'fit_seconds': 0.}
    parents = {r['gate']['parent'] for r in records.values() if r.get('gate')}
    with threadpool_limits(limits=2):
        for name in leaves:
            if name in parents or not records[name].get('gate'):
                raise ValueError('Only gated leaves allowed')
            options = records[name]['values']
            asked = visible[masked.iloc[visible][name].ne(schema['gated_value']).to_numpy()]
            labels = masked.iloc[asked][name].map({v: i for i, v in enumerate(options)}).to_numpy(dtype=int)
            counts = np.bincount(labels, minlength=len(options))
            details['heads'][name] = {'asked_fit_rows': len(asked), 'class_counts': counts.tolist()}
            if len(asked) < 100 or np.count_nonzero(counts) < 2:
                tree[name] = None
                continue
            model = HistGradientBoostingClassifier(**dict(TREE_PARAMETERS), categorical_features=[True] * len(given))
            start = perf_counter()
            if monitor:
                monitor.fit_started = start
            model.fit(features[asked], labels)
            elapsed = perf_counter() - start
            if monitor:
                monitor.fit_seconds += elapsed
                monitor.fit_started = None
            details['fit_seconds'] += elapsed
            details['fit_count'] += 1
            tree[name] = smooth_tree(model.predict_proba(features[query]), model.classes_, counts)
    return tree, details


def make_arms(base, trees):
    return {n: [intervene(p, trees.get(n), a) for a in SHARES] for n, p in base.items()}


def score_arms(arms, labels):
    return {n: np.stack([np.log(floor_mix(p)[np.arange(len(labels[n])), labels[n]]) for p in rows])
            for n, rows in arms.items()}


def oracle(scores, names, base):
    chosen = {n: int(scores[n].sum(1).argmax()) for n in names}
    old = sum(scores[n][0].sum() for n in names)
    best = sum(scores[n][chosen[n]].sum() for n in names)
    u = float(np.mean([np.log(base[n].shape[1]) for n in names]))
    cells = len(scores[names[0]][0]) * len(names)
    delta = float((best - old) / (cells * u))
    return {'shares': chosen, 'identity_log_sum': float(old), 'best_log_sum': float(best),
            'uniform_reference': u, 'baseline_skill': float(1 + old / (cells * u)),
            'oracle_skill': float(1 + best / (cells * u)), 'delta_skill': delta,
            'delta_skill_over_3': delta / 3, 'gate': 'PASS' if delta > 1e-10 else 'STOP',
            'per_head_gain_log_sum': {n: float(scores[n][chosen[n]].sum() - scores[n][0].sum()) for n in names}}


def group_sums(values, groups):
    _, inverse = np.unique(groups, return_inverse=True)
    return np.bincount(inverse, weights=values), np.bincount(inverse)


def cluster_mean_se(values, groups):
    sums, counts = group_sums(values, groups)
    mean = float(np.mean(values))
    g = len(counts)
    if g < 2:
        return mean, float('inf')
    return mean, float(np.sqrt(g / (g - 1) * np.sum((sums - counts * mean)**2) / len(values)**2))


def select(scores, leaves, groups):
    shares, details = {}, {}
    for n in leaves:
        choice = int(scores[n].sum(1).argmax())
        mean, se = cluster_mean_se(scores[n][choice] - scores[n][0], groups)
        shares[n] = choice if mean > 0 and mean > se else 0
        details[n] = {'proposed_index': choice, 'paired_mean_log': mean,
                      'cluster_se': se if np.isfinite(se) else None}
    return shares, details


def cluster_bootstrap(values, groups):
    sums, counts = group_sums(values, groups)
    rng = np.random.default_rng(5601)
    draws = []
    for _ in range(2000):
        draw = rng.integers(0, len(counts), len(counts))
        draws.append(sums[draw].sum() / counts[draw].sum())
    return np.quantile(draws, [.025, .975])


def allow_stage(stage, prior):
    if stage == 'oracle':
        return
    if stage not in ('selection', 'audit') or prior.get('oracle', {}).get('gate') != 'PASS':
        raise ValueError('Oracle PASS required; calibration scores forbidden')
    if stage == 'audit' and not any(prior.get('selection', {}).get('shares', {}).values()):
        raise ValueError('Frozen nonzero selection required before audit')


def load_channel():
    """Reconstruct unchanged roles; never compute a model score here."""
    frame, masked, schema, roles, manifest = prepare('group')
    keys = pd.read_parquet(SOURCE)
    eligible = keys['THHLDSTATUS'].isin(['1', '2']) & pd.to_numeric(keys['TAGE_EHC'], errors='coerce').ge(1)
    keys = keys.loc[eligible].copy()
    keys['sample_digest'] = keys.apply(sample_digest, axis=1)
    keys = keys.sort_values(['sample_digest', 'SSUID', 'PNUM']).head(12000).reset_index(drop=True)
    if digest(b''.join(keys['sample_digest'])) != manifest['sample_hash']:
        raise AssertionError('Group key alignment failed')
    groups = keys['SSUID'].to_numpy()
    if pd.DataFrame({'group': groups, 'role': roles}).groupby('group')['role'].nunique().max() != 1:
        raise AssertionError('SSUID role overlap')
    return frame, masked, schema, roles, groups, manifest


def load_cache(masked, schema, roles, manifest):
    cache = ROOT / 'external/e055'
    old = json.loads((cache / 'sipp-group-manifest.json').read_text(encoding='utf-8'))
    for key in ('view', 'rows', 'role_counts', 'sample_hash', 'sample_namespace', 'role_namespace'):
        if old[key] != manifest[key]:
            raise AssertionError(f'Cache mismatch: {key}')
    if old['source_sha256'] != digest(SOURCE.read_bytes()):
        raise AssertionError('Source data changed')
    for name, expected in old['source_code_sha256'].items():
        if digest((ROOT / name).read_bytes()) != expected:
            raise AssertionError(f'Source changed: {name}')
    for role, positions in old['role_positions'].items():
        if positions != np.flatnonzero(roles.eq(role)).tolist():
            raise AssertionError('Role positions changed')
    if digest(pickle.dumps((schema, masked), protocol=5)) != old['masked_frame_sha256']:
        raise AssertionError('Masked frame changed')
    payload = (cache / 'sipp-group-capture.pkl.gz').read_bytes()
    if digest(payload) != old['capture_sha256']:
        raise AssertionError('Capture changed')
    frozen = pickle.loads(gzip.decompress(payload))
    query = np.flatnonzero(roles.ne('fit'))
    if not np.array_equal(query, frozen['query']) or frozen['original_parity_max_abs'] != 0:
        raise AssertionError('Cache coverage or original parity failed')
    base = frozen['identity']
    if list(base) != TARGETS or any(len(v) != len(query) for v in base.values()):
        raise AssertionError('Incomplete original endpoint')
    return base, query, old


def validate_arms(arms):
    summary = {'raw_sentinel_max_abs': 0., 'postfloor_sentinel_max_abs': 0., 'total_mass_max_abs': 0.}
    for name, rows in arms.items():
        p = rows[0]
        for a in rows:
            if not np.isfinite(a).all() or (a < 0).any() or (a.sum(1) <= 0).any():
                raise AssertionError('Invalid probability')
            error = float(np.max(np.abs(a.sum(1) - p.sum(1))))
            summary['total_mass_max_abs'] = max(summary['total_mass_max_abs'], error)
            if name == PARENT:
                np.testing.assert_array_equal(a, p)
            else:
                np.testing.assert_array_equal(a[:, -1], p[:, -1])
                delta = float(np.max(np.abs(floor_mix(a)[:, -1] - floor_mix(p)[:, -1])))
                summary['postfloor_sentinel_max_abs'] = max(summary['postfloor_sentinel_max_abs'], delta)
    if summary['total_mass_max_abs'] > 1e-12:
        raise AssertionError('Total mass changed')
    return summary


def freeze_library(monitor):
    if (LOCAL / 'library.npz').exists() or (OUT / 'manifest.json').exists():
        raise FileExistsError('Refusing existing library before any fit')
    _, masked, schema, roles, groups, manifest = load_channel()
    base, query, cache_manifest = load_cache(masked, schema, roles, manifest)
    trees, details = fit_trees(masked, schema, query, REASONS, monitor)
    arms = make_arms(base, trees)
    checks = validate_arms(arms)
    for filename, expected in [('submissions/2026-09-19-E041/main.py',
         '22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073'),
         ('submissions/2026-09-19-E041.zip', '1502ebad20e85ae57db617fa6d202b9e199594c1c043acd6d0d1d52102362a50')]:
        if digest((ROOT / filename).read_bytes()) != expected:
            raise AssertionError('Comparator snapshot changed')
    arrays = {f'{n}/{i}': a for n, rows in arms.items() for i, a in enumerate(rows)}
    arrays.update({'query': query, 'groups': groups[query].astype(str), 'roles': roles.iloc[query].to_numpy(dtype=str)})
    with (LOCAL / 'library.npz').open('xb') as stream:
        np.savez_compressed(stream, **arrays)
    (OUT / 'registration.md').write_bytes(REGISTRATION.read_bytes())
    script = Path(__file__)
    (OUT / 'executed-screen-e056.py').write_bytes(script.read_bytes())
    manifest.update({'library_sha256': digest((LOCAL / 'library.npz').read_bytes()),
        'registration_sha256': digest(REGISTRATION.read_bytes()), 'script_sha256': digest(script.read_bytes()),
        'source_sha256': cache_manifest['source_sha256'], 'masked_frame_sha256': cache_manifest['masked_frame_sha256'],
        'roles_sha256': digest(json.dumps(cache_manifest['role_positions'], sort_keys=True).encode()),
        'cache_manifest_sha256': digest((ROOT / 'external/e055/sipp-group-manifest.json').read_bytes()),
        'cache_capture_sha256': cache_manifest['capture_sha256'], 'source_code_sha256': cache_manifest['source_code_sha256'],
        'tree_parameters': dict(TREE_PARAMETERS), 'trees': details, 'checks': checks,
        'e041_new_fits': 0, 'query_rows': len(query), 'groups': int(len(np.unique(groups))),
        'versions': {'python': sys.version, 'numpy': np.__version__, 'pandas': pd.__version__, 'sklearn': sklearn.__version__},
        'scored_roles': [], 'label_exposure': 'Prior E055 oracle is development evidence; calibration unscored.'})
    write_json(OUT / 'manifest.json', manifest)
    print(json.dumps({'stage': 'library', 'trees': details, 'checks': checks}), flush=True)


def evaluate_stage(stage):
    destination = OUT / f'{stage}.json'
    if destination.exists() or (LOCAL / f'{stage}-opened.json').exists():
        raise FileExistsError('Refusing repeated role access')
    prior = {name: json.loads((OUT / f'{name}.json').read_text())
             for name in ('oracle', 'selection') if (OUT / f'{name}.json').exists()}
    allow_stage(stage, prior)
    manifest = json.loads((OUT / 'manifest.json').read_text())
    if digest((LOCAL / 'library.npz').read_bytes()) != manifest['library_sha256']:
        raise AssertionError('Frozen library changed')
    if digest(Path(__file__).read_bytes()) != manifest['script_sha256']:
        raise AssertionError('Executed code changed')
    frame, masked, schema, roles, groups, fresh = load_channel()
    if fresh['sample_hash'] != manifest['sample_hash'] or digest(pickle.dumps((schema, masked), protocol=5)) != manifest['masked_frame_sha256']:
        raise AssertionError('Evaluation channel changed')
    if digest(SOURCE.read_bytes()) != manifest['source_sha256']:
        raise AssertionError('Evaluation source changed')
    with np.load(LOCAL / 'library.npz', allow_pickle=False) as data:
        query = data['query']
        if not np.array_equal(data['roles'], roles.iloc[query].to_numpy(dtype=str)):
            raise AssertionError('Evaluation role alignment changed')
        take = np.flatnonzero(roles.iloc[query].eq(stage))
        arms = {n: [data[f'{n}/{i}'][take] for i in range(3)] for n in TARGETS}
    selected_groups = groups[query[take]]
    # This persistent marker is written before the only score access to a role.
    write_json(LOCAL / f'{stage}-opened.json', {'role': stage, 'library_sha256': manifest['library_sha256']})
    labels = {n: frame.iloc[query[take]][n].map({v: i for i, v in enumerate(
        schema['items'][n]['values'] + ([] if n == PARENT else [schema['gated_value']]))}).to_numpy(dtype=int) for n in TARGETS}
    if stage == 'audit':
        # Only score the frozen policy and comparator, not unused audit arms.
        fixed = {PARENT: 0, **prior['selection']['shares']}
        scored = score_arms({n: [rows[0], rows[fixed[n]]] for n, rows in arms.items()}, labels)
        scores = {n: np.stack([scored[n][0] if i != fixed[n] else scored[n][1]
                               for i in range(3)]) for n in TARGETS}
    else:
        scores = score_arms(arms, labels)
    # Restricted score arrays permit independent arithmetic verification without
    # reopening response labels or evaluating another policy on the audit.
    with (LOCAL / f'{stage}-scores.npz').open('xb') as stream:
        saved = ({f'base/{n}': scored[n][0] for n in TARGETS} |
                 {f'selected/{n}': scored[n][1] for n in TARGETS}) if stage == 'audit' else scores
        np.savez_compressed(stream, **saved, groups=selected_groups.astype(str))
    base = {n: rows[0] for n, rows in arms.items()}
    if stage == 'oracle':
        result = oracle(scores, TARGETS, base)
    elif stage == 'selection':
        shares, detail = select(scores, REASONS, selected_groups)
        result = {'shares': shares, 'detail': detail,
                  'gate': 'AUDIT' if any(shares.values()) else 'STOP_NO_INTERVENTION'}
    else:
        choices = {PARENT: 0, **prior['selection']['shares']}
        u = float(np.mean([np.log(base[n].shape[1]) for n in TARGETS]))
        delta = np.column_stack([scores[n][choices[n]] - scores[n][0] for n in TARGETS]).mean(1) / u
        interval = cluster_bootstrap(delta, selected_groups)
        selected = {n: arms[n][choices[n]] for n in TARGETS}
        changes = {n: int(np.any(selected[n] != base[n], axis=1).sum()) for n in TARGETS}
        conditional = {}
        for n in REASONS:
            asked = labels[n] != 2
            row = np.arange(asked.sum())
            losses = []
            for vector in (base[n], selected[n]):
                p = floor_mix(vector)[asked, :-1]
                p /= p.sum(1, keepdims=True)
                losses.append(float(-np.log(p[row, labels[n][asked]]).mean()) if asked.any() else None)
            conditional[n] = {'asked_rows': int(asked.sum()), 'baseline_loss': losses[0], 'selected_loss': losses[1]}
        result = {'shares': choices, 'delta_skill': float(delta.mean()), 'delta_skill_over_3': float(delta.mean() / 3),
            'bootstrap_95': interval.tolist(), 'bootstrap_seed': 5601, 'bootstrap_draws': 2000,
            'baseline_skill': float(1 + np.column_stack([scores[n][0] for n in TARGETS]).mean() / u),
            'selected_skill': float(1 + np.column_stack([scores[n][choices[n]] for n in TARGETS]).mean() / u),
            'changed_vectors': changes, 'changed_fraction': sum(changes.values()) / (len(take) * 7),
            'conditional_asked_loss': conditional, 'checks': validate_arms({n: [base[n], selected[n]] for n in TARGETS}),
            'gate': 'FOLLOWUP_RESEARCH' if delta.mean() > 0 and interval[0] > 0 else 'STOP_INCONCLUSIVE_OR_NONPOSITIVE'}
    result.update({'role': stage, 'rows': len(take), 'ssuid_groups': len(np.unique(selected_groups)),
                   'library_sha256': manifest['library_sha256'], 'share_values': list(SHARES),
                   'scores_sha256': digest((LOCAL / f'{stage}-scores.npz').read_bytes())})
    write_json(destination, result)
    print(json.dumps(result, allow_nan=False), flush=True)


class ResourceMonitor:
    """Native Windows worker and descendant RSS sampler; no extra dependency."""
    def __init__(self, stage):
        self.stage, self.start = stage, perf_counter()
        self.fit_started, self.fit_seconds, self.peak = None, 0., 0
        self.done = threading.Event()
        class Counters(ctypes.Structure):
            _fields_ = [('cb', ctypes.c_ulong), ('PageFaultCount', ctypes.c_ulong)] + [
                (n, ctypes.c_size_t) for n in ('PeakWorkingSetSize', 'WorkingSetSize', 'QuotaPeakPagedPoolUsage',
                 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage', 'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage')]
        self.counters = Counters()
        self.counters.cb = ctypes.sizeof(Counters)
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        self.kernel = kernel
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        self.handle = kernel.GetCurrentProcess()
        class ProcessEntry(ctypes.Structure):
            _fields_ = [('dwSize', ctypes.c_ulong), ('cntUsage', ctypes.c_ulong),
                ('th32ProcessID', ctypes.c_ulong), ('th32DefaultHeapID', ctypes.c_size_t),
                ('th32ModuleID', ctypes.c_ulong), ('cntThreads', ctypes.c_ulong),
                ('th32ParentProcessID', ctypes.c_ulong), ('pcPriClassBase', ctypes.c_long),
                ('dwFlags', ctypes.c_ulong), ('szExeFile', ctypes.c_wchar * 260)]
        self.entry_type = ProcessEntry
        kernel.CreateToolhelp32Snapshot.argtypes = [ctypes.c_ulong, ctypes.c_ulong]
        kernel.CreateToolhelp32Snapshot.restype = ctypes.c_void_p
        for name in ('Process32FirstW', 'Process32NextW'):
            getattr(kernel, name).argtypes = [ctypes.c_void_p, ctypes.POINTER(ProcessEntry)]
        kernel.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
        kernel.OpenProcess.restype = ctypes.c_void_p
        kernel.CloseHandle.argtypes = [ctypes.c_void_p]
        self.get_memory = ctypes.WinDLL('psapi', use_last_error=True).GetProcessMemoryInfo
        self.get_memory.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
        self.thread = threading.Thread(target=self.sample, daemon=True)

    def record(self, reason):
        return {'stage': self.stage, 'worker_wall_seconds': perf_counter() - self.start,
                'fit_seconds': self.fit_seconds, 'peak_rss_bytes': self.peak, 'reason': reason,
                'scope': 'Worker plus descendants; .25s summed RSS samples, including worker OS lifetime peak.'}

    def memory(self):
        if not self.get_memory(self.handle, ctypes.byref(self.counters), self.counters.cb):
            raise OSError('Worker memory unavailable')
        total = max(int(self.counters.WorkingSetSize), int(self.counters.PeakWorkingSetSize))
        snapshot = self.kernel.CreateToolhelp32Snapshot(2, 0)
        if snapshot == ctypes.c_void_p(-1).value:
            raise OSError('Process snapshot unavailable')
        entry = self.entry_type()
        entry.dwSize = ctypes.sizeof(entry)
        parents = {}
        try:
            more = self.kernel.Process32FirstW(snapshot, ctypes.byref(entry))
            if not more:
                raise OSError('Process enumeration unavailable')
            while more:
                parents[int(entry.th32ProcessID)] = int(entry.th32ParentProcessID)
                more = self.kernel.Process32NextW(snapshot, ctypes.byref(entry))
        finally:
            self.kernel.CloseHandle(snapshot)
        descendants = {os.getpid()}
        while True:
            expanded = descendants | {pid for pid, parent in parents.items() if parent in descendants}
            if expanded == descendants:
                break
            descendants = expanded
        for pid in descendants - {os.getpid()}:
            handle = self.kernel.OpenProcess(0x410, False, pid)
            if not handle:
                raise OSError('Descendant memory unavailable')
            try:
                if not self.get_memory(handle, ctypes.byref(self.counters), self.counters.cb):
                    raise OSError('Descendant memory unavailable')
                total += int(self.counters.WorkingSetSize)
            finally:
                self.kernel.CloseHandle(handle)
        return total

    def sample(self):
        while not self.done.is_set():
            try:
                measured = self.memory()
            except OSError:
                reason = 'MEMORY_MONITOR_FAILED'
            else:
                self.peak = max(self.peak, measured)
                active = 0. if self.fit_started is None else perf_counter() - self.fit_started
                reason = ('MEMORY_CAP' if self.peak >= 8 * 1024**3 else
                          'FIT_CAP' if self.fit_seconds + active >= 1200 else
                          'WALL_CAP' if perf_counter() - self.start >= 4800 else None)
            if reason:
                write_json(OUT / f'{self.stage}-resources.json', self.record(reason))
                os._exit(3)
            self.done.wait(.25)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['library', 'oracle', 'selection', 'audit'])
    args = parser.parse_args()
    LOCAL.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / f'{args.stage}-resources.json').exists():
        raise FileExistsError('Refusing repeated stage execution')
    monitor = ResourceMonitor(args.stage)
    monitor.thread.start()
    reason = 'ERROR'
    try:
        if args.stage == 'library':
            freeze_library(monitor)
        else:
            evaluate_stage(args.stage)
        reason = 'COMPLETE'
    finally:
        monitor.done.set()
        monitor.thread.join()
        write_json(OUT / f'{args.stage}-resources.json', monitor.record(reason))


if __name__ == '__main__':
    main()
