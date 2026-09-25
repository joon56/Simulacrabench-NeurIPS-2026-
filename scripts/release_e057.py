"""Bounded E057 release verification; fixed inputs, no tuning or upload."""
import argparse
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import pickle
import re
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.check_e057 import MemoryTree, cases, sha, read, save, blob, invariants

KIT = ROOT / 'external/starter-kit'
S1 = ROOT / 'docs/analysis/E057-outputs'
OUT = S1 / 's2'
LOCAL = ROOT / 'external/e057-s2'
SNAP = ROOT / 'submissions/2026-09-25-E057'
NAMES = ('unicef', 'world_bank', 'unhcr')


def identical(actual, expected, label):
    import numpy as np
    if isinstance(expected, dict):
        assert actual.keys() == expected.keys(), label
        for key in expected:
            identical(actual[key], expected[key], label + '/' + str(key))
    elif isinstance(expected, (list, tuple)):
        assert len(actual) == len(expected), label
        for i, (a, b) in enumerate(zip(actual, expected)):
            identical(a, b, label + '/' + str(i))
    elif isinstance(expected, np.ndarray):
        np.testing.assert_array_equal(actual, expected, err_msg=label)
    else:
        assert actual == expected, label


def load_blob(path):
    return pickle.loads(Path(path).read_bytes())


def validate_inputs():
    prior = read(S1 / 'preflight.json')
    frozen = read(S1 / 'frozen-verification.json')
    hashes = {**prior['source_files'], **prior['prior_source_files'], **frozen['local_hashes']}
    for name, entry in prior['inputs'].items():
        hashes[f'external/starter-kit/data/{name}.json'] = entry['schema_sha256']
        hashes[f'external/starter-kit/_sandbox/{name}/respondents.parquet'] = entry['data_sha256']
        for cache in entry['caches'].values():
            hashes[cache['path']] = cache['sha256']
    for path, expected in hashes.items():
        assert sha(ROOT / path) == expected, 'Provenance changed: ' + path
    return prior, hashes


def verify_freeze():
    manifest = read(OUT / 'preflight.json')
    for path, expected in manifest['hashes'].items():
        assert sha(ROOT / path) == expected, 'Release freeze changed: ' + path
    return manifest


def preflight():
    if OUT.exists() or LOCAL.exists():
        raise FileExistsError('Refuse occupied E057 S2 output namespace')
    prior, hashes = validate_inputs()
    from scripts.assemble_e057 import build_source
    assert build_source() == (SNAP / 'main.py').read_bytes()
    datasets = cases()
    for name, case in datasets.items():
        assert case[-1] == prior['inputs'][name]['frame_sha256']
    OUT.mkdir()
    LOCAL.mkdir()
    extracted = LOCAL / 'extracted'
    extracted.mkdir()
    with zipfile.ZipFile(SNAP.with_suffix('.zip')) as archive:
        assert archive.namelist() == ['main.py', 'NOTICE.txt']
        for name in archive.namelist():
            raw = archive.read(name)
            assert raw == (SNAP / name).read_bytes()
            (extracted / name).write_bytes(raw)
    command = [sys.executable, str(KIT / 'tools/check_submission_zip.py'), str(SNAP.with_suffix('.zip'))]
    check = subprocess.run(command, capture_output=True, text=True, timeout=60)
    (OUT / 'zip-check.log').write_text(check.stdout + check.stderr, encoding='utf-8')
    assert check.returncode == 0 and 'OK:' in check.stdout
    paths = [Path(__file__), ROOT / 'scripts/assemble_e057.py', ROOT / 'tests/test_e057_release.py',
             S1 / 's2-plan.md', SNAP / 'SCORES.md', SNAP / 'main.py', SNAP / 'NOTICE.txt',
             SNAP.with_suffix('.zip'), extracted / 'main.py', extracted / 'NOTICE.txt',
             KIT / 'tools/check_submission_zip.py', S1 / 'frozen-verification.json']
    for p in paths:
        hashes[p.relative_to(ROOT).as_posix()] = sha(p)
    for p in (S1 / 'result.json', S1 / 'policy.json', S1 / 'selection.json', S1 / 'validation.json'):
        hashes[p.relative_to(ROOT).as_posix()] = sha(p)
    # Original S1 versions must remain the local runtime versions.
    import numpy, pandas, sklearn, torch
    versions = dict(python=sys.version, numpy=numpy.__version__, pandas=pandas.__version__,
                    sklearn=sklearn.__version__, torch=torch.__version__)
    assert versions == prior['versions']
    (OUT / 'scorecard-prerun.md').write_bytes((SNAP / 'SCORES.md').read_bytes())
    (OUT / 'plan-prerun.md').write_bytes((S1 / 's2-plan.md').read_bytes())
    save(OUT / 'preflight.json', {'hashes': hashes, 'versions': versions,
         'phase': 1, 'zip_checker': check.stdout.strip(), 'limits': {'suite_seconds': 900,
         'total_suite_seconds': 2700, 'process_tree_memory_bytes': 8 * 1024**3, 'threads': 2},
         'inputs': prior['inputs'], 'no_new_proxy_or_test_access': True})
    print('PREFLIGHT PASS', len(hashes), 'hashes', flush=True)


def module_from(path):
    spec = importlib.util.spec_from_file_location('e057_release_assembly', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prediction_worker(mode):
    started = time.perf_counter()
    manifest = verify_freeze()
    datasets = cases()
    import numpy as np
    from src.models import conditional_leaf_content as source
    model = source if mode == 'default' else module_from(LOCAL / 'extracted/main.py')
    import_seconds = time.perf_counter() - started
    results = {}
    for name, (_, schema, frame, cells, _, frame_hash) in datasets.items():
        assert frame_hash == manifest['inputs'][name]['frame_sha256']
        events, stages, checks = [], {}, {}
        predicted, leaves, _ = source.layout(schema)

        def observe(event, payload):
            events.append(event)
            if event == 'fit_start':
                print(mode, name, payload['stage'], 'start', flush=True)
            elif event == 'fit_end':
                stages[payload['stage']] = payload['seconds']
            elif event == 'split':
                old = read(ROOT / 'external/e057/split.json')
                for role in ('fit', 'selection', 'validation', 'query', 'shadow_query'):
                    np.testing.assert_array_equal(payload[role], old[role])
                raw = pickle.dumps((schema, payload['masked_frame']), protocol=5)
                assert hashlib.sha256(raw).hexdigest() == sha(ROOT / 'external/e057/masked-shadow.pkl')
                checks['split_and_mask_exact'] = True
            elif event in ('shadow_frozen', 'refit_frozen'):
                stage = 'shadow' if event == 'shadow_frozen' else 'refit'
                old = load_blob(ROOT / f'external/e057/{stage}-library.pkl')
                identical(payload, old, stage)
                blob(LOCAL / f'{mode}-{stage}.pkl', payload)
                checks[stage + '_exact_s1'] = True
                if mode == 'assembly':
                    identical(payload, load_blob(LOCAL / f'default-{stage}.pkl'), stage + '_default')
                    checks[stage + '_exact_default'] = True
                if stage == 'refit':
                    shares = dict.fromkeys(leaves, .5)
                    forced = source.apply_policy(payload['base'], predicted, payload['query'], payload['trees'], shares)
                    expected = load_blob(ROOT / 'external/e057/forced-vectors.pkl')
                    identical(forced, expected, 'forced_s1')
                    if mode == 'assembly':
                        actual = model._e057_apply_policy(payload['base'], predicted, payload['query'], payload['trees'], shares)
                        identical(actual, forced, 'forced_assembly')
                    checks['forced_active'] = invariants(payload['base'], forced, predicted, payload['query'], leaves, schema['items'])
                    checks['forced_active']['score_access'] = False
            elif event == 'selection_frozen':
                identical(payload, read(S1 / 'selection.json'), 'selection')
            elif event == 'validation_scored':
                old = read(S1 / 'validation.json')
                identical({k: v for k, v in payload.items() if k != 'paired_difference'},
                          {k: v for k, v in old.items() if k != 'differences_sha256'}, 'validation')
                identical(payload['paired_difference'], load_blob(ROOT / 'external/e057/validation-differences.pkl'), 'paired')
            elif event == 'policy_frozen':
                identical(payload, read(S1 / 'policy.json'), 'policy')
                checks['shares'] = payload['shares']

        before = time.perf_counter()
        # Exercise the actual source/assembly default; never inject base_predict.
        vectors = model.predict(frame, schema, observer=observe)
        elapsed = time.perf_counter() - before
        query = np.flatnonzero(frame[predicted].isna().any(axis=1))
        source.validate_vectors(vectors, predicted, query, schema['items'])
        original = load_blob(ROOT / f'external/e057/{name}-vectors.pkl')['candidate']
        identical(vectors, original, name + '_s1')
        if mode == 'assembly':
            identical(vectors, load_blob(LOCAL / f'default-{name}.pkl'), name + '_default')
        digest = blob(LOCAL / f'{mode}-{name}.pkl', vectors)
        results[name] = {'cells': len(cells), 'frame_sha256': frame_hash,
                         'vectors_sha256': digest, 'seconds': elapsed, 'events': events,
                         'fit_stages_seconds': stages, 'checks': checks, 'raw_exact_s1': True}
        print(mode, name, 'PASS', elapsed, flush=True)
    save(OUT / f'{mode}.json', {'status': 'PASS', 'instruments': results,
         'import_and_preflight_seconds': import_seconds,
         'worker_seconds': time.perf_counter() - started, 'injected_baseline': False})


def official_worker():
    verify_freeze()
    results = {}
    for name in NAMES:
        print('official', name, 'start', flush=True)
        log = OUT / f'{name}-official.json'
        command = [sys.executable, str(KIT / 'score.py'), '--submission', str(LOCAL / 'extracted'),
                   '--data', str(KIT / '_sandbox' / name), '--schema', str(KIT / 'data' / f'{name}.json'),
                   '--phase', '1', '--keep', '--log', str(log)]
        done = subprocess.run(command, cwd=KIT, capture_output=True, text=True, encoding='utf-8', errors='replace')
        stdout = done.stdout + done.stderr
        (OUT / f'{name}-official.log').write_text(stdout, encoding='utf-8')
        assert done.returncode == 0, stdout[-2000:]
        result = read(log)
        assert result['status'] == 'PASS' and result['phase'] == 1
        work = Path(re.search(r'^\[work\] (.+)$', stdout, re.MULTILINE).group(1).strip())
        raw = (work / 'predictions.json').read_bytes()
        vectors = json.loads(raw)
        identical(vectors, load_blob(LOCAL / f'assembly-{name}.pkl'), name + '_official')
        with (LOCAL / f'{name}-official-predictions.json.gz').open('xb') as stream:
            stream.write(gzip.compress(raw, mtime=0))
        results[name] = {'status': 'PASS', 'skill': result['skill'], 'seconds': result['seconds'],
                         'cells': result['n_cells'], 'assembly_raw_exact': True}
        print('official', name, 'PASS', result['seconds'], flush=True)
    assert sum(v['seconds'] for v in results.values()) < 900
    save(OUT / 'official.json', {'status': 'PASS', 'instruments': results})


def run(mode):
    verify_freeze()
    if mode != 'default':
        prerequisite = 'default' if mode == 'assembly' else 'assembly'
        assert read(OUT / f'{prerequisite}-runtime.json')['status'] == 'PASS'
    if (OUT / f'{mode}-runtime.json').exists() or (OUT / f'{mode}.log').exists():
        raise FileExistsError('Refuse repeated expensive suite')
    used = sum(read(p)['parent_inclusive_seconds'] for p in OUT.glob('*-runtime.json'))
    assert used < 1800 if mode == 'official' else used < 900 if mode == 'assembly' else used == 0
    env = dict(os.environ, OMP_NUM_THREADS='2', MKL_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2',
               CUDA_VISIBLE_DEVICES='', PYTHONIOENCODING='utf-8')
    env.pop('PYTHONPATH', None)
    started = time.perf_counter()
    peak = {'rss': 0, 'commitment': 0}
    reason, failures = 'COMPLETE', 0
    with (OUT / f'{mode}.log').open('x', encoding='utf-8') as log:
        process = subprocess.Popen([sys.executable, str(Path(__file__)), 'worker', '--suite', mode],
                                   cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        monitor = MemoryTree(os.getpid())  # Include launcher/harness and worker descendants.
        while process.poll() is None:
            try:
                sample = monitor.sample()
                for key in peak:
                    peak[key] = max(peak[key], sample[key])
                failures = 0
            except OSError:
                failures += 1
                if failures >= 3 and process.poll() is None:
                    reason = 'MONITOR_FAILURE'
            if time.perf_counter() - started >= 900:
                reason = 'TIMEOUT'
            if max(peak.values()) >= 8 * 1024**3:
                reason = 'MEMORY_CAP'
            if reason != 'COMPLETE':
                subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
                process.wait(timeout=10)
                break
            time.sleep(.2)
        code = process.wait()
    total = time.perf_counter() - started
    status = 'PASS' if code == 0 and reason == 'COMPLETE' and total < 900 else 'FAIL'
    save(OUT / f'{mode}-runtime.json', {'status': status, 'reason': reason, 'exit_code': code,
         'parent_inclusive_seconds': total, 'peak_process_tree_bytes': peak,
         'memory_scope': 'sum of live owned processes lifetime peak counters; includes launcher/harness',
         'total_suite_seconds_so_far': used + total})
    print(read(OUT / f'{mode}-runtime.json'), flush=True)
    if status != 'PASS':
        raise SystemExit(1)


def finalize():
    manifest = verify_freeze()
    datasets = cases()
    import numpy as np
    from score import floored, uniform_reference
    timings = {mode: read(OUT / f'{mode}-runtime.json') for mode in ('default', 'assembly', 'official')}
    assert all(v['status'] == 'PASS' for v in timings.values())
    assert sum(v['parent_inclusive_seconds'] for v in timings.values()) < 2700
    official = read(OUT / 'official.json')
    result = {}
    for name, (config, schema, _, cells, truth, frame_hash) in datasets.items():
        assert frame_hash == manifest['inputs'][name]['frame_sha256']
        vectors = load_blob(LOCAL / f'assembly-{name}.pkl')
        identical(vectors, load_blob(LOCAL / f'default-{name}.pkl'), name)
        saved = json.loads(gzip.decompress((LOCAL / f'{name}-official-predictions.json.gz').read_bytes()))
        identical(saved, vectors, name + '_official_final')
        def skill(raw):
            p = floored(raw, schema, cells, config['scoring']['floor'])
            logs = [np.log(v[(schema['items'][n]['values'] + ([schema['gated_value']] if schema['items'][n].get('gate') else [])).index(y)])
                    for v, y, (_, _, n) in zip(p, truth, cells)]
            return float(1 + np.mean(logs) / uniform_reference(schema))
        baseline = {}
        for label, entry in manifest['inputs'][name]['caches'].items():
            assert sha(ROOT / entry['path']) == entry['sha256']
            cache = load_blob(ROOT / entry['path'])
            assert cache['frame_sha256'] == frame_hash
            baseline[label] = skill(cache['vectors'])
            if label == 'E041':
                identical(vectors, cache['vectors'], name + '_E041')
        measured = skill(vectors)
        assert abs(measured - official['instruments'][name]['skill']) < 1e-12
        assert abs(measured - baseline['E025']) <= .002
        result[name] = {**official['instruments'][name], 'skill': measured,
                       'delta_e025': measured - baseline['E025'], 'delta_e041': measured - baseline['E041'],
                       'e025_absolute_002_pass': True, 'exact_e041': True}
    artifacts = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(OUT.glob('*')) if p.is_file()}
    artifacts.update({p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(LOCAL.glob('*')) if p.is_file()})
    summary = {'status': 'PASS', 'phase': 1, 'technical_qualification': True,
        'zip_sha256': sha(SNAP.with_suffix('.zip')), 'main_sha256': sha(SNAP / 'main.py'),
        'scorecard_prerun_sha256': sha(OUT / 'scorecard-prerun.md'), 'instruments': result,
        'runtime': timings, 'official_seconds_sum': sum(v['seconds'] for v in result.values()),
        'artifact_hashes': artifacts, 'source_and_input_hashes': manifest['hashes'],
        'hosted_result': None, 'adopted': False, 'test_selected': False,
        'scope': 'Previously exposed synthetic phase1, Windows CPU; active fixtures unscored.'}
    save(SNAP / 'verification.json', summary)
    print(json.dumps({k: v for k, v in summary.items() if k not in ('artifact_hashes', 'source_and_input_hashes')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('preflight', 'run', 'worker', 'finalize'))
    parser.add_argument('--suite', choices=('default', 'assembly', 'official'))
    args = parser.parse_args()
    if args.mode == 'preflight':
        preflight()
    elif args.mode == 'run':
        run(args.suite)
    elif args.mode == 'worker':
        official_worker() if args.suite == 'official' else prediction_worker(args.suite)
    else:
        finalize()
