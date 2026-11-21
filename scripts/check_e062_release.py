"""Bounded E062 S2 qualification; only named synthetic inputs/references."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import inspect
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
S1 = ROOT / 'docs/analysis/E062-outputs'
OUT = S1 / 's2'
KIT = ROOT / 'external/starter-kit'
SNAP = ROOT / 'submissions/2026-10-08-E062'
NAMES = ('unicef', 'world_bank', 'unhcr')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify():
    entry = read(OUT / 'entry.json')
    for path, expected in entry['hashes'].items():
        if path in ('docs/status.md', 'docs/log.md'):
            continue
        if sha(ROOT / path) != expected:
            raise RuntimeError('Frozen input changed: ' + path)
    frozen = OUT / 'release-freeze.json'
    if frozen.exists():
        for path, expected in read(frozen)['hashes'].items():
            if sha(ROOT / path) != expected:
                raise RuntimeError('S2 freeze changed: ' + path)


def counts():
    totals = dict(full_stack=0, neural=0, metric=0)
    for path in OUT.glob('calls-*.jsonl'):
        for line in path.read_text(encoding='utf-8').splitlines():
            event = json.loads(line)
            kind = event.get('kind')
            if event.get('event') == 'enter' and kind in totals:
                totals[kind] += 1
    return totals


def caps():
    if (OUT / 'technical-retry.json').exists():
        return dict(full_stack=9, neural=27, metric=24)
    return dict(full_stack=6, neural=18, metric=16)


class Audit:
    """Standalone observational profiler, also copied outside the ZIP for CLI."""
    def __init__(self, main_path, log_path, previous, limits, ntrain, instrument):
        self.main_path = os.path.normcase(os.path.abspath(main_path))
        self.stream = open(log_path, 'x', encoding='utf-8')
        self.totals = dict(previous)
        self.limits = limits
        self.ntrain = ntrain
        self.instrument = instrument
        self.started = {}
        self.environment_recorded = False
        self.roles = json.loads(os.environ.get('E062_ROLES', '{}'))

    def emit(self, row):
        row.update(instrument=self.instrument, pid=os.getpid())
        self.stream.write(json.dumps(row, allow_nan=False) + '\n')
        self.stream.flush()

    def profile(self, frame, event, arg):
        if event not in ('call', 'return'):
            return
        name = frame.f_code.co_name
        filename = os.path.normcase(os.path.abspath(frame.f_code.co_filename))
        is_model = filename == self.main_path
        if is_model and name == '<module>' and event == 'return':
            torch = sys.modules['torch']
            torch.set_num_threads(2)
            torch.set_num_interop_threads(2)
            if torch.cuda.is_available():
                raise RuntimeError('GPU not allowed')
            self.environment_recorded = True
            self.emit(dict(event='environment', torch_threads=torch.get_num_threads(),
                           torch_interop_threads=torch.get_num_interop_threads(), cuda=False))
        if is_model and name == '_targets' and event == 'call':
            rows, predicted = frame.f_locals['rows'], frame.f_locals['predict_items']
            if len(rows) and (min(rows.index) < 0 or max(rows.index) >= self.ntrain
                             or rows[predicted].isna().any().any()):
                raise RuntimeError('DEV PREDICT reached training targets')
            self.emit(dict(event='target_boundary', rows=len(rows)))
            digest = hashlib.sha256(__import__('numpy').asarray(rows.index, dtype='<i8').tobytes()).hexdigest()
            roles = [key for key, value in self.roles.items() if value['index_sha256'] == digest]
            if not roles:
                raise RuntimeError('Frozen neural target role mismatch')
            self.emit(dict(event='target_role', rows=len(rows), roles=roles, index_sha256=digest))
        kind = ('full_stack' if is_model and name == '_e062_predict' else
                'neural' if is_model and name in ('_train_on', '_e062_train_on') else
                'metric' if name == 'minimize' and filename.replace('\\', '/').endswith('/scipy/optimize/_minimize.py') else None)
        if kind is None:
            return
        if event == 'call':
            self.totals[kind] += 1
            self.emit(dict(event='enter', kind=kind, function=name, totals=dict(self.totals)))
            if self.totals[kind] > self.limits[kind]:
                raise RuntimeError('Call cap: ' + kind)
            self.started[id(frame)] = time.perf_counter()
        else:
            row = dict(event='return', kind=kind, function=name,
                       seconds=time.perf_counter() - self.started.pop(id(frame), time.perf_counter()),
                       returned=arg is not None)
            if kind == 'neural':
                row.update(epochs=int(frame.f_locals.get('epoch', 0)),
                           best_epoch=int(frame.f_locals.get('best_epoch', 0)),
                           device=str(frame.f_locals.get('dev')))
            if kind == 'metric' and arg is not None:
                row.update(iterations=int(arg.nit), success=bool(arg.success))
            self.emit(row)


def environment():
    import numpy as np
    import pandas as pd
    import torch
    import scipy
    import sklearn
    import pyarrow
    from threadpoolctl import threadpool_info
    torch.set_num_threads(2)
    torch.set_num_interop_threads(2)
    old = read(S1 / 'environment-candidate-01.json')
    actual = dict(python=sys.version, numpy=np.__version__, pandas=pd.__version__,
                  torch=torch.__version__, torch_threads=torch.get_num_threads(),
                  interop_threads=torch.get_num_interop_threads(),
                  cuda_available=torch.cuda.is_available(), threadpools=threadpool_info(),
                  scipy=scipy.__version__, sklearn=sklearn.__version__, pyarrow=pyarrow.__version__)
    for model in ('candidate', 'E025', 'E041'):
        old = read(S1 / f'environment-{model}-01.json')
        for key in ('python', 'numpy', 'pandas', 'torch', 'torch_threads', 'interop_threads', 'cuda_available'):
            if actual[key] != old[key]:
                raise RuntimeError('S1 environment mismatch: ' + model + '/' + key)
    if any(p['num_threads'] > 2 for p in actual['threadpools']):
        raise RuntimeError('Numerical thread cap')
    return actual


def official_module():
    sys.path.insert(0, str(KIT))
    return load_module('e062_s2_official', KIT / 'score.py')


def phase1_case(official, name, with_truth=False):
    import pandas as pd
    config = official.load_config(str(KIT / 'config.yml'))
    schema = official.load_schema(str(KIT / f'data/{name}.json'), config)
    items = official.generated_items(schema)
    path = KIT / f'_sandbox/{name}/respondents.parquet'
    train = pd.read_parquet(path, columns=['respondent_id', 'role'] + items,
                            filters=[('role', '==', 'TRAIN')]).astype(object)
    given = [n for n in items if schema['items'][n]['class'] == 'GIVEN']
    dev = pd.read_parquet(path, columns=['respondent_id', 'role'] + (items if with_truth else given),
                          filters=[('role', '==', 'DEV')]).astype(object)
    if not with_truth:
        dev = dev.reindex(columns=['respondent_id', 'role'] + items)
    respondents = pd.concat((train, dev), ignore_index=True).astype(object)
    counts_by_role = respondents.role.value_counts().to_dict()
    if counts_by_role != {'TRAIN': schema['split']['n_train'], 'DEV': schema['split']['n_dev']}:
        raise RuntimeError('Phase1 role mismatch')
    if respondents.respondent_id.duplicated().any():
        raise RuntimeError('Duplicate synthetic ID')
    for item in items:
        if not set(respondents[item].dropna()).issubset(set(official.options_for(schema, item))):
            raise RuntimeError('Synthetic option mismatch')
    frame, cells, truth = official.sample_rows(schema, respondents, 1)
    ntrain = schema['split']['n_train']
    if not frame.loc[ntrain:, official.scored_items(schema)].isna().all().all():
        raise RuntimeError('DEV PREDICT masking')
    actual = dict(rows=len(frame), train=ntrain, dev=schema['split']['n_dev'],
                  cells=len(cells), role_hash=hashlib.sha256(pd.util.hash_pandas_object(
                      respondents[['respondent_id', 'role']], index=True).values.tobytes()).hexdigest(),
                  masked_frame_hash=hashlib.sha256(pd.util.hash_pandas_object(frame, index=True).values.tobytes()).hexdigest())
    previous = read(S1 / 'frozen-inputs.json')['phase1'][name]
    actual['schema_runtime_sha256'] = hashlib.sha256(json.dumps(schema, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    if any(actual[k] != previous[k] for k in actual):
        raise RuntimeError('S1 split/frame identity mismatch: ' + name)
    return config, schema, respondents, frame, cells, truth, actual


def reference(model, name):
    import numpy as np
    filename = f'vectors-{model}-{name}.npz'
    path = S1 / filename
    expected = read(S1 / 'frozen-predictions.json')['outputs'][f'{model}-{name}']['sha256']
    if sha(path) != expected:
        raise RuntimeError('Reference changed: ' + filename)
    with np.load(path, allow_pickle=False) as arrays:
        if set(arrays.files) != {'flat', 'offsets'}:
            raise RuntimeError('Unexpected reference arrays')
        flat, offsets = arrays['flat'].copy(), arrays['offsets'].copy()
    if flat.dtype != np.float64 or offsets.dtype.kind not in 'iu' or offsets[0] != 0 or offsets[-1] != len(flat):
        raise RuntimeError('Invalid numeric reference')
    if not np.all(np.diff(offsets) > 0):
        raise RuntimeError('Reference offsets')
    return flat, offsets


def compare_vectors(official, name, vectors, schema, cells):
    import numpy as np
    official.check(schema, vectors, cells)
    offsets = np.r_[0, np.cumsum([len(v) for v in vectors])]
    flat = np.concatenate(vectors).astype(np.float64)
    maxsum = max(abs(float(np.asarray(v).sum()) - 1.) for v in vectors)
    if maxsum > 1e-6:
        raise RuntimeError('Raw sum contract')
    differences = {}
    for model in ('candidate', 'E041', 'E025'):
        frozen, frozen_offsets = reference(model, name)
        if not np.array_equal(offsets, frozen_offsets):
            raise RuntimeError('Reference shape mismatch')
        delta = np.abs(flat - frozen)
        per_vector = np.maximum.reduceat(delta, offsets[:-1])
        differences[model] = dict(max_abs=float(delta.max()), changed_vectors=int((per_vector != 0).sum()))
    if differences['candidate']['max_abs'] != 0:
        raise RuntimeError('Frozen source parity failed')
    if name != 'world_bank' and differences['E041']['max_abs'] != 0:
        raise RuntimeError('Control drift')
    if name == 'world_bank' and differences['E041']['changed_vectors'] == 0:
        raise RuntimeError('STOP_IDENTITY')
    return dict(vectors=len(vectors), max_raw_sum_error=maxsum, comparisons=differences,
                flat_sha256=hashlib.sha256(flat.tobytes()).hexdigest(), status='PASS')


def score_gates(name, skill):
    previous = read(S1 / 'comparison.json')['scores']
    delta025 = skill - previous[f'E025-{name}']['skill']
    delta041 = skill - previous[f'E041-{name}']['skill']
    if delta025 < -.002 or delta041 < -.002:
        raise RuntimeError('STOP_RELEASE')
    if abs(skill - previous[f'candidate-{name}']['skill']) > 1e-12:
        raise RuntimeError('Frozen score mismatch')
    return dict(skill=skill, delta_E025=delta025, delta_E041=delta041, release_pass=True)


def preflight():
    verify()
    env = environment()
    official = official_module()
    inputs = {}
    staging_hashes = {}
    for name in NAMES:
        config, schema, respondents, frame, cells, truth, identity = phase1_case(official, name, with_truth=True)
        for model in ('candidate', 'E041', 'E025'):
            flat, offsets = reference(model, name)
            vectors = [flat[a:b] for a, b in zip(offsets[:-1], offsets[1:])]
            official.check(schema, vectors, cells)
        directory = OUT / 'phase1' / name
        directory.mkdir(parents=True, exist_ok=False)
        path = directory / 'respondents.parquet'
        respondents.to_parquet(path, index=False)
        # Verify the official CLI's delivery path without predicting/scoring.
        restored = official.load_frames(str(directory), schema)
        restored_frame, restored_cells, _ = official.sample_rows(schema, restored, 1)
        if not restored.equals(respondents) or not restored_frame.equals(frame) or restored_cells != cells:
            raise RuntimeError('Official phase1 staging mismatch')
        inputs[name] = identity
        staging_hashes[str(path.relative_to(ROOT)).replace('\\', '/')] = sha(path)
    sys.path.insert(0, str(ROOT))
    from scripts.assemble_e062 import build_source
    raw = build_source()
    with (OUT / 'main.py').open('xb') as stream:
        stream.write(raw)
    observer = OUT / 'observer'
    observer.mkdir()
    text = ('import hashlib, json, os, sys, time\n' + inspect.getsource(Audit) + '\n'
            "if os.environ.get('E062_AUDIT_MAIN'):\n"
            "    _audit = Audit(os.environ['E062_AUDIT_MAIN'], os.environ['E062_AUDIT_LOG'] + '-' + str(os.getpid()) + '.jsonl', json.loads(os.environ['E062_PRIOR']), json.loads(os.environ['E062_CAPS']), int(os.environ['E062_NTRAIN']), os.environ['E062_INSTRUMENT'])\n"
            "    sys.setprofile(_audit.profile)\n")
    (observer / 'sitecustomize.py').write_text(text, encoding='utf-8')
    save(OUT / 'preflight.json', dict(status='PASS', environment=env, inputs=inputs,
                                     references=9, reference_policy='allow_pickle=False, numeric flat/offsets only',
                                     staging_hashes=staging_hashes, main_sha256=sha(OUT / 'main.py')))
    paths = ['scripts/assemble_e062.py', 'scripts/check_e062_release.py',
             'tests/test_e062_assembly.py', str((OUT / 'main.py').relative_to(ROOT)),
             str((OUT / 'observer/sitecustomize.py').relative_to(ROOT)),
             str((OUT / 'release-contract.md').relative_to(ROOT)),
             str((OUT / 'entry.json').relative_to(ROOT)),
             str((SNAP / 'SCORES.md').relative_to(ROOT)),
             'external/starter-kit/tools/check_submission_zip.py',
             'external/starter-kit/LICENSE']
    hashes = {p.replace('\\', '/'): sha(ROOT / p) for p in paths}
    hashes.update(staging_hashes)
    save(OUT / 'release-freeze.json', dict(frozen_utc=datetime.now(timezone.utc).isoformat(),
                                          hashes=hashes, model_calls=0, source='entry.json/S1 manifests'))
    print('PREFLIGHT PASS; source/scorecard/input freeze before S2 model calls', flush=True)


def assembly():
    verify()
    env = environment()
    official = official_module()
    module = load_module('e062_assembled', OUT / 'main.py')
    results = {}
    for name in NAMES:
        config, schema, _, frame, cells, truth, identity = phase1_case(official, name)
        audit = Audit(str(OUT / 'main.py'), str(OUT / f'calls-assembly-{name}.jsonl'),
                      counts(), caps(), identity['train'], name)
        audit.roles = read(S1 / 'frozen-inputs.json')['phase1'][name]['neural_roles']
        print('START assembly', name, flush=True)
        sys.setprofile(audit.profile)
        started = time.perf_counter()
        try:
            vectors = module.predict(frame.copy(deep=True), schema)
        finally:
            sys.setprofile(None)
            audit.stream.close()
        row = compare_vectors(official, name, vectors, schema, cells)
        # Evaluator-only answer projection occurs after predict has returned.
        _, _, _, _, _, truth, _ = phase1_case(official, name, with_truth=True)
        measured = official.score(schema, config, official.floored(vectors, schema, cells,
                                  config['scoring']['floor']), truth, cells, seed=0)
        row.update(score_gates(name, measured['skill']))
        row['prediction_and_check_seconds'] = time.perf_counter() - started
        save(OUT / f'assembly-{name}.json', row)
        results[name] = row
        print('DONE assembly', name, row, flush=True)
    save(OUT / 'assembly.json', dict(status='PASS', instruments=results, environment=env, cumulative_calls=counts()))


def package():
    verify()
    if read(OUT / 'assembly-resources.json')['status'] != 'PASS':
        raise RuntimeError('Assembly resource qualification required')
    if read(OUT / 'assembly.json')['status'] != 'PASS':
        raise RuntimeError('Assembly required')
    sys.path.insert(0, str(ROOT))
    from scripts.assemble_e062 import package as build_package
    files = build_package(SNAP, OUT / 'main.py')
    extracted = OUT / 'extracted'
    extracted.mkdir()
    with zipfile.ZipFile(SNAP.with_suffix('.zip')) as archive:
        if archive.namelist() != ['main.py', 'NOTICE.txt']:
            raise RuntimeError('Unexpected ZIP content')
        for name in archive.namelist():
            value = archive.read(name)
            if value != (SNAP / name).read_bytes():
                raise RuntimeError('Archive byte mismatch')
            with (extracted / name).open('xb') as stream:
                stream.write(value)
    if (extracted / 'main.py').read_bytes() != (OUT / 'main.py').read_bytes():
        raise RuntimeError('Extracted assembly bytes differ')
    command = [sys.executable, '-X', 'utf8', '-B', str(KIT / 'tools/check_submission_zip.py'), str(SNAP.with_suffix('.zip'))]
    done = subprocess.run(command, cwd=extracted, capture_output=True, text=True, encoding='utf-8', timeout=90)
    output = done.stdout + done.stderr
    (OUT / 'zip-check.log').write_text(output, encoding='utf-8')
    if done.returncode != 0 or 'OK:' not in output:
        raise RuntimeError('ZIP checker: ' + output[-1500:])
    save(OUT / 'package.json', dict(status='PASS_CHECKER_PENDING_OFFICIAL', files=files,
                                   extracted_main_sha256=sha(extracted / 'main.py'),
                                   zip_bytes=SNAP.with_suffix('.zip').stat().st_size,
                                   checker=output.strip(), checker_smoke='one tiny generated-frame predict; no neural or metric fit'))
    print('PACKAGE/CHECKER PASS', files, flush=True)


def official_run():
    verify()
    package_report = read(OUT / 'package.json')
    for name, expected in package_report['files'].items():
        path = SNAP.with_suffix('.zip') if name.endswith('.zip') else SNAP / name
        if sha(path) != expected:
            raise RuntimeError('Package changed')
    extracted = OUT / 'extracted'
    if sha(extracted / 'main.py') != package_report['extracted_main_sha256']:
        raise RuntimeError('Extracted main changed')
    environment()
    official = official_module()
    results = {}
    workroot = OUT / 'official-work'
    workroot.mkdir()
    for name in NAMES:
        config, schema, _, frame, cells, truth, identity = phase1_case(official, name)
        logfile = OUT / f'official-{name}.json'
        if logfile.exists():
            raise FileExistsError(logfile)
        env = dict(os.environ, PYTHONPATH=str(OUT / 'observer'),
                   TEMP=str(workroot), TMP=str(workroot),
                   E062_AUDIT_MAIN=str(extracted / 'main.py'),
                   E062_AUDIT_LOG=str(OUT / f'calls-official-{name}'),
                   E062_PRIOR=json.dumps(counts()), E062_CAPS=json.dumps(caps()),
                   E062_NTRAIN=str(identity['train']), E062_INSTRUMENT=name,
                   E062_ROLES=json.dumps(read(S1 / 'frozen-inputs.json')['phase1'][name]['neural_roles']))
        command = [sys.executable, '-X', 'utf8', '-B', str(KIT / 'score.py'),
                   '--submission', str(extracted), '--data', str(OUT / 'phase1' / name),
                   '--schema', str(KIT / f'data/{name}.json'), '--config', str(KIT / 'config.yml'),
                   '--phase', '1', '--seed', '0', '--keep', '--log', str(logfile)]
        print('START official', name, flush=True)
        started = time.perf_counter()
        done = subprocess.run(command, cwd=extracted, env=env, capture_output=True,
                              text=True, encoding='utf-8', errors='replace')
        cli_seconds = time.perf_counter() - started
        output = done.stdout + done.stderr
        (OUT / f'official-{name}.log').write_text(output, encoding='utf-8')
        if done.returncode != 0:
            raise RuntimeError('Official CLI failed: ' + output[-2000:])
        report = read(logfile)
        if report['status'] != 'PASS' or report['phase'] != 1:
            raise RuntimeError('Official status/phase')
        match = re.search(r'^\[work\] (.+)$', output, re.MULTILINE)
        if match is None:
            raise RuntimeError('Official prediction location missing')
        work = Path(match.group(1).strip()).resolve()
        if not work.is_relative_to(workroot.resolve()):
            raise RuntimeError('Unexpected official work directory')
        vectors = read(work / 'predictions.json')
        row = compare_vectors(official, name, vectors, schema, cells)
        row.update(score_gates(name, report['skill']))
        row.update(cli_startup_to_exit_seconds=cli_seconds, scorer_seconds=report['seconds'],
                   official_log=str(logfile.relative_to(ROOT)), predictions_sha256=sha(work / 'predictions.json'))
        # Observer must actually have run in the model process, not only CLI parent.
        events = [json.loads(line) for p in OUT.glob(f'calls-official-{name}-*.jsonl')
                  for line in p.read_text(encoding='utf-8').splitlines()]
        if sum(e.get('event') == 'environment' for e in events) != 1:
            raise RuntimeError('Official model observer missing')
        entered = [e for e in events if e.get('event') == 'enter']
        if sum(e.get('kind') == 'full_stack' for e in entered) != 1:
            raise RuntimeError('Official call count missing')
        results[name] = row
        save(OUT / f'official-parity-{name}.json', row)
        print('DONE official', name, row, flush=True)
    save(OUT / 'official.json', dict(status='PASS', instruments=results,
                                    cli_seconds_sum=sum(r['cli_startup_to_exit_seconds'] for r in results.values()),
                                    cumulative_calls=counts()))


def monitor(mode):
    sys.path.insert(0, str(ROOT))
    from scripts.check_e057 import MemoryTree
    entry = read(OUT / 'entry.json')
    deadline = datetime.fromisoformat(entry['computation_cutoff_utc'].replace('Z', '+00:00')).timestamp()
    prior = sum(read(p)['wall_seconds'] for p in OUT.glob('*-resources.json'))
    report_path, log_path = OUT / f'{mode}-resources.json', OUT / f'{mode}.log'
    if report_path.exists() or log_path.exists():
        raise FileExistsError('Never overwrite an attempt')
    verify()
    if mode == 'assembly' and read(OUT / 'preflight-resources.json')['status'] != 'PASS':
        raise RuntimeError('Preflight resources required')
    if mode == 'official' and read(OUT / 'package-resources.json')['status'] != 'PASS':
        raise RuntimeError('Package resources required')
    if mode in ('assembly', 'official'):
        current = counts()
        if any(current[k] + v > caps()[k] for k, v in dict(full_stack=3, neural=9, metric=8).items()):
            raise RuntimeError('Insufficient remaining call budget')
    env = dict(os.environ, OMP_NUM_THREADS='2', MKL_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2',
               NUMEXPR_NUM_THREADS='2', CUDA_VISIBLE_DEVICES='', PYTHONDONTWRITEBYTECODE='1',
               PYTHONIOENCODING='utf-8', PYTHONPATH=str(ROOT), PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    command = ([sys.executable, '-X', 'utf8', '-B', '-m', 'unittest',
                'tests.test_e062_assembly.AssemblyBoundaryTests.test_frozen_prefix_and_standalone_import' if mode == 'tests-red' else 'tests.test_e062_assembly', '-v']
               if mode.startswith('tests') else [sys.executable, '-X', 'utf8', '-B', __file__, 'worker', mode])
    memory = MemoryTree(os.getpid())
    peak = memory.sample()
    if max(peak.values()) >= 8 * 1024**3 or prior >= 2400 or time.time() >= deadline:
        raise RuntimeError('Prelaunch cap')
    start = time.perf_counter()
    process = None
    reason, error = 'COMPLETE', None
    limit = 900 if mode in ('assembly', 'official') else 120
    with log_path.open('x', encoding='utf-8') as log:
        try:
            process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
            while process.poll() is None:
                sample = memory.sample()
                peak = {k: max(peak[k], sample[k]) for k in peak}
                elapsed = time.perf_counter() - start
                if max(peak.values()) >= 8 * 1024**3:
                    reason = 'MEMORY_CAP'; break
                if elapsed >= limit or prior + elapsed >= 2400 or time.time() >= deadline:
                    reason = 'TIME_CAP'; break
                time.sleep(.1)
        except Exception as exc:
            reason, error = 'MONITOR_OR_LAUNCH_FAILURE', repr(exc)
        finally:
            if process is not None:
                if process.poll() is None:
                    subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
                process.wait(timeout=10)
    elapsed = time.perf_counter() - start
    code = None if process is None else process.returncode
    okay = code == 0 and reason == 'COMPLETE' and elapsed <= limit and prior + elapsed <= 2400
    report = dict(mode=mode, status='PASS' if okay else 'FAIL', command=command,
                  wall_seconds=elapsed, cumulative_worker_seconds=prior + elapsed,
                  historical_S1_worker_seconds=entry['historical_s1']['seconds'],
                  combined_worker_seconds=prior + elapsed + entry['historical_s1']['seconds'],
                  reason=reason, error=error, exit_code=code, peak_owned_tree_bytes=peak,
                  sample_interval_seconds=.1, numerical_threads=2, gpu=False,
                  memory_semantics='Owned controller+descendants; sum of per-process peak RSS/private commitment',
                  cumulative_calls=counts())
    save(report_path, report)
    print(json.dumps(report, indent=2), flush=True)
    return 0 if okay else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['run', 'worker'])
    parser.add_argument('mode', choices=['tests-red', 'tests', 'preflight', 'assembly', 'package', 'official'])
    args = parser.parse_args()
    if args.action == 'run':
        raise SystemExit(monitor(args.mode))
    {'preflight': preflight, 'assembly': assembly, 'package': package, 'official': official_run}[args.mode]()
