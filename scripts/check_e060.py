"""Bounded E060 synthetic engineering and release checks; no hosted actions."""
import argparse
from datetime import datetime, timezone
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
from scripts.check_e057 import MemoryTree, cases, sha, read, save, blob
from scripts.assemble_e060 import build_source, package, SNAP, BASE, BASE_SHA

OUT = ROOT / 'docs/analysis/E060-outputs/technical-retry1'
LOCAL = ROOT / 'external/e060/technical-retry1'
KIT = ROOT / 'external/starter-kit'
REG = ROOT / 'docs/experiments/E060-content-target-retrieval.md'
DEADLINE = datetime(2026, 9, 27, 9, 10, tzinfo=timezone.utc)
NAMES = ('unicef', 'world_bank', 'unhcr')


def preflight():
    if OUT.exists() or LOCAL.exists():
        raise FileExistsError('Preserve occupied E060 output namespace')
    prior = read(ROOT / 'docs/analysis/E057-outputs/preflight.json')
    hashes = dict(prior['prior_source_files'])
    hashes[BASE.relative_to(ROOT).as_posix()] = BASE_SHA
    for name, entry in prior['inputs'].items():
        hashes[f'external/starter-kit/data/{name}.json'] = entry['schema_sha256']
        hashes[f'external/starter-kit/_sandbox/{name}/respondents.parquet'] = entry['data_sha256']
        for cache in entry['caches'].values():
            hashes[cache['path']] = cache['sha256']
    for path, expected in hashes.items():
        assert sha(ROOT / path) == expected, 'Changed prior input: ' + path
    datasets = cases()
    for name, case in datasets.items():
        assert case[-1] == prior['inputs'][name]['frame_sha256']
        for label, cache in prior['inputs'][name]['caches'].items():
            value = pickle.loads((ROOT / cache['path']).read_bytes())
            assert value['frame_sha256'] == case[-1]
            source = BASE if label == 'E041' else ROOT / 'submissions/2026-09-09-E025/main.py'
            assert value['source_sha256'] == sha(source)
    import numpy, pandas, sklearn, torch
    versions = dict(python=sys.version, numpy=numpy.__version__, pandas=pandas.__version__,
                    sklearn=sklearn.__version__, torch=torch.__version__)
    assert versions == prior['versions'], 'Environment changed'
    paths = [REG, Path(__file__), ROOT / 'scripts/assemble_e060.py',
             ROOT / 'src/models/content_target_retrieval.py',
             ROOT / 'tests/test_content_target_retrieval.py', ROOT / 'tests/test_e060_assembly.py']
    hashes.update({p.relative_to(ROOT).as_posix(): sha(p) for p in paths})
    OUT.mkdir()
    LOCAL.mkdir()
    (OUT / 'registration.md').write_bytes(REG.read_bytes())
    (LOCAL / 'main.py').write_bytes(build_source())
    hashes[(LOCAL / 'main.py').relative_to(ROOT).as_posix()] = sha(LOCAL / 'main.py')
    monitor = MemoryTree(os.getpid())
    sample = monitor.sample()
    save(OUT / 'preflight.json', dict(hashes=hashes, inputs=prior['inputs'], versions=versions,
         status='PASS', phase=1, deadline=DEADLINE.isoformat(), monitor_smoke=sample,
         scope='Existing exposed synthetic phase1 only; no observed proxy or synthetic TEST'))
    print('PREFLIGHT PASS', len(hashes), 'hashes', flush=True)


def verify():
    result = read(OUT / 'preflight.json')
    for path, expected in result['hashes'].items():
        assert sha(ROOT / path) == expected, 'Freeze changed: ' + path
    return result


def module_from(path):
    spec = importlib.util.spec_from_file_location('e060_assembly', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact(a, b):
    import numpy as np
    return len(a) == len(b) and all(np.array_equal(x, y) for x, y in zip(a, b))


def prediction_worker(mode):
    manifest = verify()
    datasets = cases()
    import numpy as np
    from score import floored, score as grade
    from src.models import content_target_retrieval as source, shared_trunk
    model = source if mode == 'source' else module_from(LOCAL / 'main.py')
    calls = {'neural_requests': 0, 'neural_attempts': 0, 'metric_optimizers': 0}
    def counted(owner, name, counter):
        original = getattr(owner, name)
        def call(*args, **kwargs):
            calls[counter] += 1
            return original(*args, **kwargs)
        setattr(owner, name, call)
    counted(shared_trunk if mode == 'source' else model, '_train', 'neural_requests')
    counted(shared_trunk if mode == 'source' else model, '_train_on', 'neural_attempts')
    counted(model, 'minimize', 'metric_optimizers')
    results = {}
    for name, (config, schema, frame, cells, truth, frame_hash) in datasets.items():
        assert frame_hash == manifest['inputs'][name]['frame_sha256']
        before_calls = dict(calls)
        before = time.perf_counter()
        vectors = model.predict(frame, schema)
        elapsed = time.perf_counter() - before
        assert len(vectors) == len(cells)
        for vector, (_, _, item) in zip(vectors, cells):
            size = len(schema['items'][item]['values']) + bool(schema['items'][item].get('gate'))
            a = np.asarray(vector)
            assert a.shape == (size,) and np.isfinite(a).all() and (a >= 0).all() and a.sum() > 0
        def skill(v):
            return grade(schema, config, floored(v, schema, cells, config['scoring']['floor']), truth, cells)['skill']
        refs = {label: pickle.loads((ROOT / cache['path']).read_bytes())['vectors']
                for label, cache in manifest['inputs'][name]['caches'].items()}
        scored = skill(vectors)
        scores = {label: skill(v) for label, v in refs.items()}
        changes = sum(not np.array_equal(a, b) for a, b in zip(vectors, refs['E041']))
        row = dict(seconds=elapsed, cells=len(cells), candidate_skill=scored,
                   baseline_skill=scores, delta_e025=scored-scores['E025'],
                   delta_e041=scored-scores['E041'], changed_vectors=changes,
                   max_probability_delta=max(float(np.max(np.abs(np.asarray(a)-b))) for a,b in zip(vectors, refs['E041'])),
                   call_counts={k:calls[k]-before_calls[k] for k in calls})
        row['release_pass'] = abs(row['delta_e025']) <= .002 and row['delta_e041'] >= -.002
        if name != 'unhcr':
            assert exact(vectors, refs['E041']) and exact(vectors, refs['E025'])
        if mode == 'assembly':
            assert exact(vectors, pickle.loads((LOCAL / f'source-{name}.pkl').read_bytes()))
            row['source_raw_exact'] = True
        row['vectors_sha256'] = blob(LOCAL / f'{mode}-{name}.pkl', vectors)
        results[name] = row
        save(OUT / f'{mode}-{name}.json', row)
        print(mode, name, json.dumps(row), flush=True)
    status = ('STOP_RELEASE' if not all(r['release_pass'] for r in results.values()) else
              'STOP_IDENTITY' if results['unhcr']['changed_vectors'] == 0 else 'PASS')
    save(OUT / f'{mode}.json', dict(status=status, instruments=results, call_counts=calls))
    if status != 'PASS':
        raise SystemExit(2)


def official_worker():
    verify()
    check = read(OUT / 'package.json')
    for name, expected in check['files'].items():
        path = SNAP.with_suffix('.zip') if name.endswith('.zip') else SNAP / name
        assert sha(path) == expected
    results = {}
    for name in NAMES:
        command = [sys.executable, str(KIT/'score.py'), '--submission', str(LOCAL/'extracted'),
                   '--data', str(KIT/'_sandbox'/name), '--schema', str(KIT/'data'/f'{name}.json'),
                   '--phase', '1', '--keep', '--log', str(OUT/f'official-{name}.json')]
        done = subprocess.run(command, cwd=KIT, capture_output=True, text=True, encoding='utf-8', errors='replace')
        output = done.stdout + done.stderr
        (OUT/f'official-{name}.log').write_text(output, encoding='utf-8')
        assert done.returncode == 0, output[-2000:]
        result = read(OUT/f'official-{name}.json')
        assert result['status'] == 'PASS' and result['phase'] == 1
        work = Path(re.search(r'^\[work\] (.+)$', output, re.MULTILINE).group(1).strip())
        vectors = json.loads((work/'predictions.json').read_text(encoding='utf-8'))
        assert exact(vectors, pickle.loads((LOCAL/f'assembly-{name}.pkl').read_bytes()))
        results[name] = dict(status='PASS', skill=result['skill'], seconds=result['seconds'], raw_exact=True)
        print('official', name, results[name], flush=True)
    save(OUT/'official.json', dict(status='PASS', instruments=results))


def run(mode):
    verify()
    if mode != 'source':
        prior = 'source' if mode == 'assembly' else 'assembly'
        assert read(OUT/f'{prior}.json')['status'] == 'PASS'
        assert read(OUT/f'{prior}-runtime.json')['status'] == 'PASS'
    if (OUT/f'{mode}-runtime.json').exists() or (OUT/f'{mode}.log').exists():
        raise FileExistsError('Refuse repeated suite')
    used = read(OUT.parent/'source-runtime.json')['seconds'] + sum(read(p)['seconds'] for p in OUT.glob('*-runtime.json'))
    assert used < 2700 and datetime.now(timezone.utc) < DEADLINE
    monitor = MemoryTree(os.getpid())
    monitor.sample()  # Fail before creating any child if monitoring unavailable.
    env = dict(os.environ, OMP_NUM_THREADS='2', MKL_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2',
               CUDA_VISIBLE_DEVICES='', PYTHONIOENCODING='utf-8')
    start = time.perf_counter()
    peak = {'rss':0, 'commitment':0}
    process = None
    reason = 'COMPLETE'
    try:
        with (OUT/f'{mode}.log').open('x', encoding='utf-8') as log:
            process = subprocess.Popen([sys.executable, '-B', __file__, 'worker', mode], cwd=ROOT,
                                       env=env, stdout=log, stderr=subprocess.STDOUT,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
            failures = 0
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
                elapsed = time.perf_counter()-start
                if elapsed >= 900 or used+elapsed >= 2700 or datetime.now(timezone.utc) >= DEADLINE:
                    reason = 'TIMEOUT'
                if max(peak.values()) >= 8*1024**3:
                    reason = 'MEMORY_CAP'
                if reason != 'COMPLETE':
                    break
                time.sleep(.2)
    finally:
        if process is not None and process.poll() is None:
            subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'], capture_output=True)
            process.wait(timeout=10)
    code = process.returncode if process else -1
    seconds = time.perf_counter()-start
    status = 'PASS' if code == 0 and reason == 'COMPLETE' and seconds < 900 else 'FAIL'
    result = dict(status=status, reason=reason, exit_code=code, seconds=seconds,
                  total_suite_seconds=used+seconds, peak_process_tree_bytes=peak)
    save(OUT/f'{mode}-runtime.json', result)
    print(json.dumps(result), flush=True)
    if status != 'PASS':
        raise SystemExit(1)


def make_package():
    verify()
    assert read(OUT/'source.json')['status'] == 'PASS'
    assert read(OUT/'assembly.json')['status'] == 'PASS'
    files = package()
    assert (SNAP/'main.py').read_bytes() == (LOCAL/'main.py').read_bytes()
    extracted = LOCAL/'extracted'
    extracted.mkdir()
    with zipfile.ZipFile(SNAP.with_suffix('.zip')) as archive:
        assert archive.namelist() == ['main.py', 'NOTICE.txt']
        for name in archive.namelist():
            raw = archive.read(name)
            assert raw == (SNAP/name).read_bytes()
            (extracted/name).write_bytes(raw)
    done = subprocess.run([sys.executable,str(KIT/'tools/check_submission_zip.py'),str(SNAP.with_suffix('.zip'))],
                          capture_output=True, text=True, timeout=60)
    assert done.returncode == 0 and 'OK:' in done.stdout, done.stdout+done.stderr
    save(OUT/'package.json', dict(files=files, checker=done.stdout.strip(), status='PENDING_OFFICIAL'))
    print(files, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['preflight','run','worker','package'])
    parser.add_argument('mode', nargs='?', choices=['source','assembly','official'])
    args = parser.parse_args()
    if args.action == 'preflight': preflight()
    elif args.action == 'package': make_package()
    elif args.action == 'run': run(args.mode)
    elif args.mode == 'official': official_worker()
    else: prediction_worker(args.mode)
