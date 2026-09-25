"""E057 phase-1 engineering rehearsal; never package, upload or read proxies."""

import argparse
import ctypes
from ctypes import wintypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import pickle
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/analysis/E057-outputs'
LOCAL = ROOT / 'external/e057'
KIT = ROOT / 'external/starter-kit'
REGISTRATION = ROOT / 'docs/experiments/E057-unhcr-conditional-content.md'
NAMES = ('unicef', 'world_bank', 'unhcr')
BASE = ROOT / 'submissions/2026-09-19-E041/main.py'
BASE_HASH = '22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073'
FALLBACK_HASH = '00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)


def blob(path, value):
    with path.open('xb') as stream:
        pickle.dump(value, stream, protocol=5)
    return sha(path)


class MemoryTree:
    """Read only an owned Windows process tree; fail if counters unavailable."""
    class Entry(ctypes.Structure):
        _fields_ = [('dwSize', wintypes.DWORD), ('cntUsage', wintypes.DWORD),
                    ('pid', wintypes.DWORD), ('heap', ctypes.c_size_t),
                    ('module', wintypes.DWORD), ('threads', wintypes.DWORD),
                    ('parent', wintypes.DWORD), ('priority', ctypes.c_long),
                    ('flags', wintypes.DWORD), ('exe', ctypes.c_wchar * 260)]

    class Counters(ctypes.Structure):
        _fields_ = [('cb', wintypes.DWORD), ('faults', wintypes.DWORD)] + [
            (n, ctypes.c_size_t) for n in ('peak_rss', 'rss', 'qpp', 'qp', 'qnp',
                                          'qn', 'page', 'peak_page', 'private')]

    def __init__(self, pid):
        self.pid = pid
        self.kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        self.kernel.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        self.kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        for name in ('Process32FirstW', 'Process32NextW'):
            getattr(self.kernel, name).argtypes = [wintypes.HANDLE, ctypes.POINTER(self.Entry)]
        self.kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        self.kernel.OpenProcess.restype = wintypes.HANDLE
        self.kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        self.api = ctypes.WinDLL('psapi', use_last_error=True).GetProcessMemoryInfo
        self.api.argtypes = [wintypes.HANDLE, ctypes.POINTER(self.Counters), wintypes.DWORD]

    def sample(self):
        snapshot = self.kernel.CreateToolhelp32Snapshot(2, 0)
        if snapshot == ctypes.c_void_p(-1).value:
            raise OSError('Cannot enumerate processes')
        parents = {}
        entry = self.Entry()
        entry.dwSize = ctypes.sizeof(entry)
        try:
            more = self.kernel.Process32FirstW(snapshot, ctypes.byref(entry))
            if not more:
                raise OSError('Empty process snapshot')
            while more:
                parents[int(entry.pid)] = int(entry.parent)
                more = self.kernel.Process32NextW(snapshot, ctypes.byref(entry))
        finally:
            self.kernel.CloseHandle(snapshot)
        owned = {self.pid}
        while True:
            expanded = owned | {pid for pid, parent in parents.items() if parent in owned}
            if expanded == owned:
                break
            owned = expanded
        totals = {'rss': 0, 'commitment': 0}
        for pid in owned:
            handle = self.kernel.OpenProcess(0x410, False, pid)
            if not handle:
                raise OSError('Owned process counters unavailable')
            counters = self.Counters()
            counters.cb = ctypes.sizeof(counters)
            try:
                if not self.api(handle, ctypes.byref(counters), counters.cb):
                    raise OSError('Memory query failed')
                totals['rss'] += max(int(counters.rss), int(counters.peak_rss))
                totals['commitment'] += max(int(counters.private), int(counters.peak_page))
            finally:
                self.kernel.CloseHandle(handle)
        return totals


def imports():
    for variable in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
        os.environ[variable] = '2'
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(KIT))
    import torch
    torch.set_num_threads(2)
    from make_sandbox import load_config, load_schema
    from score import load_frames, sample_rows
    return load_config, load_schema, load_frames, sample_rows


def cases():
    load_config, load_schema, load_frames, sample_rows = imports()
    config = load_config(str(KIT / 'config.yml'))
    result = {}
    for name in NAMES:
        schema = load_schema(str(KIT / 'data' / f'{name}.json'), config)
        data = load_frames(str(KIT / '_sandbox' / name), schema)
        frame, cells, truth = sample_rows(schema, data, 1)
        frame_hash = hashlib.sha256(pickle.dumps((schema, config, frame, cells, truth), protocol=5)).hexdigest()
        result[name] = (config, schema, frame, cells, truth, frame_hash)
    return result


def preflight():
    if (OUT / 'preflight.json').exists():
        raise FileExistsError('Existing E057 preflight; do not overwrite')
    from_source = read(ROOT / 'submissions/2026-09-24-E054/verification.json')
    if sha(BASE) != BASE_HASH:
        raise AssertionError('Original E041 snapshot changed')
    # E054 previously demonstrated exact source-E041/cache vectors on these frames.
    checked = {}
    for path, expected in from_source['source_hashes'].items():
        if sha(ROOT / path) != expected:
            raise AssertionError(f'Prior source changed: {path}')
        checked[path] = expected
    datasets = cases()
    inputs = {}
    for name, (_, _, _, _, _, frame_hash) in datasets.items():
        old = from_source['instruments'][name]
        if frame_hash != old['frame_sha256']:
            raise AssertionError(f'Frame/cells/truth/split mismatch: {name}')
        schema_path = KIT / 'data' / f'{name}.json'
        data_path = KIT / '_sandbox' / name / 'respondents.parquet'
        if sha(schema_path) != old['schema_sha256'] or sha(data_path) != old['data_sha256']:
            raise AssertionError('Public input changed')
        caches = {}
        for label, source_hash in (('E041', BASE_HASH), ('E025', FALLBACK_HASH)):
            path = ROOT / f'tmp/e043-eval/clean-{name}-{label}.pkl'
            expected = old['baseline_cache_hashes'][path.relative_to(ROOT).as_posix()]
            if sha(path) != expected:
                raise AssertionError('Baseline cache file changed')
            value = pickle.loads(path.read_bytes())
            if value['source_sha256'] != source_hash or value['frame_sha256'] != frame_hash:
                raise AssertionError('Cache predictor/frame provenance mismatch')
            caches[label] = {'path': path.relative_to(ROOT).as_posix(), 'sha256': expected}
        inputs[name] = {'frame_sha256': frame_hash, 'schema_sha256': sha(schema_path),
                        'data_sha256': sha(data_path), 'caches': caches}
    files = ['src/models/conditional_leaf_content.py', 'scripts/check_e057.py',
             'tests/test_e057_conditional_content.py', 'docs/analysis/E057-outputs/schema-audit.json']
    import numpy, pandas, sklearn, torch
    manifest = {'input_head': '9284bf4d277e339a9ae4a334d6cf7ee7bde2c6ba',
        'registration_sha256': sha(REGISTRATION), 'base_sha256': BASE_HASH,
        'source_files': {p: sha(ROOT / p) for p in files}, 'prior_source_files': checked,
        'inputs': inputs, 'phase': 1, 'label_exposure': 'Existing synthetic engineering data only; no proxy access.',
        'versions': {'python': sys.version, 'numpy': numpy.__version__, 'pandas': pandas.__version__,
                     'sklearn': sklearn.__version__, 'torch': torch.__version__}}
    save(OUT / 'preflight.json', manifest)
    with (OUT / 'registration.md').open('xb') as stream:
        stream.write(REGISTRATION.read_bytes())
    print(json.dumps({'preflight': 'PASS', 'prior_hashes': len(checked), 'cache_files': 6}))


def invariants(base, candidate, predicted, query, leaves, records):
    import numpy as np
    from src.models.conditional_leaf_content import validate_vectors, floor_mix
    validate_vectors(candidate, predicted, query, records)
    changed, sentinel, mass, floored_sentinel = {}, 0., 0., 0.
    for j, name in enumerate(predicted):
        p = np.stack(base[j::len(predicted)])
        q = np.stack(candidate[j::len(predicted)])
        changed[name] = int(np.any(p != q, axis=1).sum())
        if name not in leaves:
            np.testing.assert_array_equal(p, q)
        else:
            np.testing.assert_array_equal(p[:, -1], q[:, -1])
            sentinel = max(sentinel, float(np.max(np.abs(p[:, -1] - q[:, -1]))))
            floored_sentinel = max(floored_sentinel, float(np.max(np.abs(floor_mix(p)[:, -1] - floor_mix(q)[:, -1]))))
        mass = max(mass, float(np.max(np.abs(p.sum(1) - q.sum(1)))))
    if max(mass, floored_sentinel) > 1e-12:
        raise AssertionError('Mass/sentinel invariant failed')
    return {'changed_vectors': sum(changed.values()), 'total_vectors': len(candidate),
            'changed_heads': {n: v for n, v in changed.items() if v}, 'raw_sentinel_max_abs': sentinel,
            'postfloor_sentinel_max_abs': floored_sentinel, 'mass_max_abs': mass}


def worker():
    started = time.perf_counter()
    monitor = MemoryTree(os.getpid())
    peak = monitor.sample()  # Before numerical imports.
    state = {'fit_seconds': 0., 'fit_start': None, 'stage': 'import'}
    done = threading.Event()

    def watchdog():
        while not done.wait(.2):
            try:
                counters = monitor.sample()
                for key in peak:
                    peak[key] = max(peak[key], counters[key])
                current_fit = 0. if state['fit_start'] is None else time.perf_counter() - state['fit_start']
                reason = ('memory' if max(peak.values()) >= 8 * 1024**3 else
                          'fit' if state['fit_seconds'] + current_fit >= 1200 else
                          'runtime' if time.perf_counter() - started >= 900 else None)
            except Exception as error:
                reason = 'monitor_' + type(error).__name__
            if reason:
                save(OUT / 'abort.json', {'reason': reason, 'stage': state['stage'], 'seconds': time.perf_counter()-started,
                                          'fit_seconds': state['fit_seconds'], 'memory': peak})
                os._exit(3)
    threading.Thread(target=watchdog, daemon=True).start()
    imports()
    import numpy as np
    from src.models import conditional_leaf_content as candidate
    from score import floored, uniform_reference
    manifest = read(OUT / 'preflight.json')
    for path, expected in {**manifest['source_files'], **manifest['prior_source_files']}.items():
        if sha(ROOT / path) != expected:
            raise AssertionError(f'Code changed before run: {path}')
    if sha(BASE) != BASE_HASH:
        raise AssertionError('Snapshot changed')
    spec = importlib.util.spec_from_file_location('e057_frozen_e041', BASE)
    base_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base_module)
    import_seconds = time.perf_counter() - started
    datasets = cases()
    outputs, run_records = {}, {}
    for name, (config, schema, frame, cells, truth, frame_hash) in datasets.items():
        if frame_hash != manifest['inputs'][name]['frame_sha256']:
            raise AssertionError('Worker frame/split differs from preflight')
        predicted, leaves, _ = candidate.layout(schema)
        hidden = np.flatnonzero(frame[predicted].isna().any(axis=1))
        record = {'events': [], 'phase_seconds': {}, 'frame_sha256': frame_hash}
        captured = {}

        def observe(event, payload):
            state['stage'] = name + ':' + event
            record['events'].append({'event': event, 'seconds_since_import_start': time.perf_counter() - started})
            if event == 'fit_start':
                state['fit_start'] = time.perf_counter()
                print(name + ' ' + payload['stage'] + ' start', flush=True)
            elif event == 'fit_end':
                state['fit_seconds'] += payload['seconds']
                state['fit_start'] = None
                record['phase_seconds'][payload['stage']] = payload['seconds']
            elif event == 'split':
                roles = {n: payload[n].tolist() for n in ('fit', 'selection', 'validation', 'query', 'shadow_query')}
                save(LOCAL / 'split.json', roles)
                record['split_sha256'] = sha(LOCAL / 'split.json')
                record['role_counts'] = {n: len(v) for n, v in roles.items()}
                record['masked_shadow_sha256'] = blob(LOCAL / 'masked-shadow.pkl', (schema, payload['masked_frame']))
            elif event == 'shadow_frozen':
                captured['shadow'] = payload
                record['shadow_library_sha256'] = blob(LOCAL / 'shadow-library.pkl', payload)
                record['shadow_head_details'] = payload['details']
            elif event == 'selection_frozen':
                save(OUT / 'selection.json', payload)
                record['selection_sha256'] = sha(OUT / 'selection.json')
            elif event == 'validation_scored':
                details = {k: v for k, v in payload.items() if k != 'paired_difference'}
                details['differences_sha256'] = blob(LOCAL / 'validation-differences.pkl', payload['paired_difference'])
                save(OUT / 'validation.json', details)
            elif event == 'policy_frozen':
                save(OUT / 'policy.json', payload)
                record['policy_sha256'] = sha(OUT / 'policy.json')
            elif event == 'refit_frozen':
                record['refit_library_sha256'] = blob(LOCAL / 'refit-library.pkl', payload)
                record['refit_head_details'] = payload['details']
                forced = candidate.apply_policy(payload['base'], predicted, payload['query'], payload['trees'],
                                                 dict.fromkeys(leaves, .5))
                record['forced_fixture'] = invariants(payload['base'], forced, predicted, payload['query'], leaves, schema['items'])
                record['forced_fixture']['score_access'] = False
                record['forced_predictions_sha256'] = blob(LOCAL / 'forced-vectors.pkl', forced)
                shifts, tree_shifts = [], []
                for j, item in enumerate(predicted):
                    before = captured['shadow']['base'][item][payload['shadow_query_index']]
                    after = np.stack(payload['base'][j::len(predicted)])
                    shifts.append(.5 * np.abs(before / before.sum(1, keepdims=True) - after / after.sum(1, keepdims=True)).sum(1))
                    q0 = captured['shadow']['trees'].get(item)
                    q1 = payload['trees'].get(item)
                    if q0 is not None and q1 is not None:
                        tree_shifts.append(.5 * np.abs(q0[payload['shadow_query_index']] - q1).sum(1))
                record['shadow_refit_shift'] = {'base_mean_tv': float(np.mean(shifts)), 'base_max_tv': float(np.max(shifts)),
                    'tree_mean_tv': float(np.mean(tree_shifts)) if tree_shifts else 0., 'tree_heads': len(tree_shifts),
                    'scope': 'Common original hidden GIVEN rows; no target labels.'}
            elif event == 'final':
                captured['base'] = payload['base']
                record['invariants'] = invariants(payload['base'], payload['output'], predicted, hidden, leaves, schema['items'])
            elif event == 'fallback':
                record['fallback'] = payload['reason']
            save(LOCAL / f'{name}-event-{len(record["events"]):02d}.json', record['events'][-1])

        before = time.perf_counter()
        vectors = candidate.predict(frame, schema, base_predict=base_module.predict, observer=observe)
        record['predict_seconds'] = time.perf_counter() - before
        base_vectors = captured.get('base', vectors)
        record['predictions_sha256'] = blob(LOCAL / f'{name}-vectors.pkl', {'candidate': vectors, 'base': base_vectors})
        outputs[name] = (vectors, base_vectors)
        run_records[name] = record
        save(OUT / f'{name}-execution.json', record)
        print(name + ' predictions frozen', flush=True)
    prediction_seconds = time.perf_counter() - started
    # All three instruments' returned predictions are frozen before DEV scoring.
    results = {}
    for name, (config, schema, frame, cells, truth, frame_hash) in datasets.items():
        vectors, base_vectors = outputs[name]
        ref = {}
        for label, entry in manifest['inputs'][name]['caches'].items():
            path = ROOT / entry['path']
            if sha(path) != entry['sha256']:
                raise AssertionError('Cache changed during run')
            ref[label] = pickle.loads(path.read_bytes())
        if not all(np.array_equal(a, b) for a, b in zip(base_vectors, ref['E041']['vectors'])):
            raise AssertionError(f'Full E041 snapshot/cache parity defect: {name}')
        if len(base_vectors) != len(ref['E041']['vectors']):
            raise AssertionError('Base vector count differs')
        def measured(raw):
            p = floored(raw, schema, cells, config['scoring']['floor'])
            logs = [np.log(v[(schema['items'][n]['values'] + ([schema['gated_value']] if schema['items'][n].get('gate') else [])).index(y)])
                    for v, y, (_, _, n) in zip(p, truth, cells)]
            return float(1 + np.mean(logs) / uniform_reference(schema))
        actual, e41, e25 = measured(vectors), measured(base_vectors), measured(ref['E025']['vectors'])
        results[name] = {'skill': actual, 'e041_skill': e41, 'e025_skill': e25,
            'delta_e041': actual - e41, 'delta_e025': actual - e25,
            'e025_absolute_002_pass': abs(actual-e25) <= .002, 'base_cache_raw_exact': True,
            'cells': len(cells), 'predict_seconds': run_records[name]['predict_seconds']}
    done.set()
    final_memory = monitor.sample()
    for key in peak:
        peak[key] = max(peak[key], final_memory[key])
    result = {'instruments': results, 'import_seconds': import_seconds,
        'prediction_complete_seconds': prediction_seconds, 'worker_total_seconds': time.perf_counter()-started,
        'conservative_fit_seconds': state['fit_seconds'], 'peak_memory_bytes': peak,
        'runtime_pass': prediction_seconds < 900, 'memory_pass': max(peak.values()) < 8*1024**3,
        'no_regression_pass': all(v['e025_absolute_002_pass'] for v in results.values()),
        'phase': 1, 'scope': 'Synthetic engineering only; official CLI and new assembly not run.'}
    save(OUT / 'result.json', result)
    print(json.dumps(result), flush=True)


def run():
    if (OUT / 'runtime.json').exists() or (LOCAL / 'run-start.json').exists():
        raise FileExistsError('Refusing existing run before fitting')
    LOCAL.mkdir(parents=True, exist_ok=True)
    save(LOCAL / 'run-start.json', {'registration_sha256': sha(OUT / 'registration.md')})
    start = time.perf_counter()
    with (OUT / 'run.log').open('x', encoding='utf-8') as log:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), 'worker'], cwd=ROOT,
                                   stdout=log, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
        monitor = MemoryTree(process.pid)
        peak = {'rss': 0, 'commitment': 0}
        reason = 'COMPLETE'
        while process.poll() is None:
            try:
                sample = monitor.sample()
                for key in peak:
                    peak[key] = max(peak[key], sample[key])
            except OSError:
                if process.poll() is None:
                    reason = 'MONITOR_FAILURE'
            if time.perf_counter() - start >= 900:
                reason = 'TIMEOUT'
            if max(peak.values()) >= 8 * 1024**3:
                reason = 'MEMORY_CAP'
            if reason != 'COMPLETE':
                subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True, check=False)
                process.wait(timeout=10)
                break
            time.sleep(.2)
        exit_code = process.wait()
    save(OUT / 'runtime.json', {'parent_inclusive_seconds': time.perf_counter()-start,
        'peak_tree_memory_bytes': peak, 'exit_code': exit_code, 'reason': reason,
        'limits': {'seconds': 900, 'fit_seconds': 1200, 'memory_bytes': 8*1024**3}})
    print(json.dumps(read(OUT / 'runtime.json')), flush=True)
    if exit_code or reason != 'COMPLETE':
        raise SystemExit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('preflight', 'run', 'worker'))
    args = parser.parse_args()
    {'preflight': preflight, 'run': run, 'worker': worker}[args.mode]()
