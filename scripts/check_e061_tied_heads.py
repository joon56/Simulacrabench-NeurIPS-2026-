"""E061 synthetic source checks only. No assembly, ZIP, cache or hosted work."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/analysis/E061-outputs'
KIT = ROOT / 'external/starter-kit'
NAMES = ('unicef', 'world_bank', 'unhcr')
CODE = ('src/models/tied_content_heads.py', 'tests/test_tied_content_heads.py',
        'scripts/check_e061_tied_heads.py')
sys.path.insert(0, str(ROOT))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_inputs(include_frozen=False):
    entry = read(OUT / 'entry.json')
    current = {}
    for path, expected in {**entry['source_hashes'], **entry['synthetic_hashes']}.items():
        if path in ('docs/status.md', 'docs/log.md'):
            continue
        actual = sha(ROOT / path)
        if actual != expected:
            raise RuntimeError('Input changed: ' + path)
        current[path] = actual
    if sha(OUT / 'registration.md') != entry['registration_sha256']:
        raise RuntimeError('Registration changed')
    if include_frozen:
        for path, expected in read(OUT / 'frozen-inputs.json')['code_hashes'].items():
            if sha(ROOT / path) != expected:
                raise RuntimeError('Frozen implementation changed: ' + path)
    return current


def prior_worker_seconds():
    total = 0.
    for path in OUT.glob('*-resources.json'):
        report = read(path)
        total += report.get('wall_seconds', 0.)
    return total


def monitor(mode, attempt):
    # This import defines only stdlib helpers; no E057 operation is invoked.
    from scripts.check_e057 import MemoryTree
    for name in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS'):
        os.environ[name] = '2'
    os.environ.update(CUDA_VISIBLE_DEVICES='', PYTHONDONTWRITEBYTECODE='1',
                      PYTHONPATH=str(ROOT), PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    report_path = OUT / f'{mode}-{attempt:02d}-resources.json'
    log_path = OUT / f'{mode}-{attempt:02d}.log'
    if report_path.exists() or log_path.exists():
        raise FileExistsError('Preserve prior attempt')
    entry = read(OUT / 'entry.json')
    deadline = datetime.fromisoformat(entry['deadline_utc'].replace('Z', '+00:00')).timestamp()
    prior = prior_worker_seconds()
    if mode == 'run':
        verify_inputs(include_frozen=True)
        if (OUT / 'comparison.json').exists():
            raise RuntimeError('Successful scientific run must not be repeated')
    command = ([sys.executable, '-X', 'utf8', '-B', '-m', 'unittest',
                'tests.test_tied_content_heads', '-v'] if mode == 'tests' else
               [sys.executable, '-X', 'utf8', '-B', __file__, '_worker', '--attempt', str(attempt)])
    memory = MemoryTree(os.getpid())
    peak = memory.sample()  # fail before launching if counters unavailable
    if max(peak.values()) > 8 * 1024**3 or time.time() >= deadline or prior >= 1800:
        raise RuntimeError('Prelaunch resource limit')
    started = time.perf_counter()
    process = None
    reason, error = 'COMPLETE', None
    candidate_observed_seconds = None
    candidate_path = OUT / f'candidate-{attempt:02d}-timing.json'
    with log_path.open('x', encoding='utf-8') as log:
        try:
            process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
            while process.poll() is None:
                sample = memory.sample()
                peak = {key: max(peak[key], sample[key]) for key in peak}
                elapsed = time.perf_counter() - started
                if mode == 'run' and candidate_path.exists() and candidate_observed_seconds is None:
                    candidate_observed_seconds = elapsed
                    if candidate_observed_seconds > 900:
                        reason = 'CANDIDATE_TIME_CAP'; break
                if max(peak.values()) > 8 * 1024**3:
                    reason = 'MEMORY_CAP'; break
                if time.time() >= deadline or elapsed + prior >= 1800:
                    reason = 'TIME_CAP'; break
                if mode == 'tests' and elapsed > 120:
                    reason = 'TEST_TIMEOUT'; break
                if mode == 'run' and not candidate_path.exists() and elapsed > 900:
                    reason = 'CANDIDATE_TIME_CAP'; break
                time.sleep(.1)
        except Exception as exc:
            reason, error = 'MONITOR_OR_LAUNCH_FAILURE', repr(exc)
        finally:
            if process is not None:
                if process.poll() is None:
                    subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
                process.wait(timeout=10)
    elapsed = time.perf_counter() - started
    code = None if process is None else process.returncode
    report = {'mode': mode, 'attempt': attempt, 'command': command,
              'started_utc': datetime.fromtimestamp(time.time() - elapsed, timezone.utc).isoformat(),
              'wall_seconds': elapsed, 'prior_worker_seconds': prior,
              'cumulative_worker_seconds': prior + elapsed,
              'candidate_stage_seconds_including_interpreter_startup': candidate_observed_seconds,
              'resource_stop': reason, 'error': error, 'exit_code': code,
              'peak_owned_tree_bytes': peak, 'sample_interval_seconds': .1,
              'counter_semantics': 'Sum of per-process RSS/private/page peaks, conservative; controller plus descendants',
              'memory_limit_bytes_each': 8 * 1024**3, 'numerical_threads': 2,
              'status': 'PASS' if code == 0 and reason == 'COMPLETE' else 'TECHNICAL_FAILURE'}
    save(report_path, report)
    print(json.dumps(report, indent=2))
    return 0 if report['status'] == 'PASS' else 1


class CallAudit:
    """Observe function entry/return without replacing model functions."""
    def __init__(self, path):
        self.stream = Path(path).open('x', encoding='utf-8')
        self.events = []
        self.model = self.instrument = None
        self.n_train = 0
        self.neural_calls = 0
        self.target_calls = 0
        self.full_stack_calls = 0
        for previous in OUT.glob('calls-*.jsonl'):
            if previous.resolve() == Path(path).resolve():
                continue
            for line in previous.read_text(encoding='utf-8').splitlines():
                event = json.loads(line)
                self.neural_calls += event.get('event') == 'enter' and event.get('function') == '_train_on'
                self.full_stack_calls += event.get('event') == 'full_stack_enter'

    def emit(self, record):
        record.update(model=self.model, instrument=self.instrument)
        self.events.append(record)
        self.stream.write(json.dumps(record, allow_nan=False) + '\n')
        self.stream.flush()

    def trace(self, frame, event, arg):
        if event != 'call':
            return None
        name = frame.f_code.co_name
        filename = frame.f_code.co_filename.replace('\\', '/')
        model_source = ('/src/models/' in filename or '/submissions/2026-09-' in filename)
        if model_source and name == '_targets':
            rows = frame.f_locals['rows']
            predicted = frame.f_locals['predict_items']
            if len(rows) and (min(rows.index) < 0 or max(rows.index) >= self.n_train
                              or rows[predicted].isna().any().any()):
                raise RuntimeError('Held-out PREDICT reached training targets')
            self.target_calls += 1
            return None
        neural = model_source and name == '_train_on'
        metric = name == 'minimize' and filename.endswith('/scipy/optimize/_minimize.py')
        other = model_source and name in ('select_ladder', 'tune_and_train', 'supervised_layer')
        if not (neural or metric or other):
            return None
        if neural:
            self.neural_calls += 1
            if self.neural_calls > 27:
                raise RuntimeError('Neural call cap')
        started = time.perf_counter()
        self.emit({'event': 'enter', 'function': name, 'neural_call_count': self.neural_calls})
        frame.f_trace_lines = False

        def finished(current, kind, value):
            if kind == 'return':
                loc = current.f_locals
                result = {'event': 'return', 'function': name,
                          'wall_seconds': time.perf_counter() - started}
                if neural:
                    result.update(epochs_executed=int(loc.get('epoch', 0)),
                                  best_epoch=int(loc.get('best_epoch', 0)),
                                  fit_rows=len(loc['X_fit']),
                                  validation_rows=0 if loc['X_val'] is None else len(loc['X_val']),
                                  config=list(loc['config']), device=str(loc['dev']),
                                  returned=value is not None)
                elif metric and value is not None:
                    result.update(iterations=int(value.nit), success=bool(value.success))
                elif name == 'tune_and_train' and value is not None:
                    result.update(blend_weight=float(value[0]))
                elif name == 'supervised_layer':
                    result.update(active_sections=[int(x) for x in loc.get('active', [])],
                                  nonzero_lambda_items=len(loc.get('lam', {})))
                self.emit(result)
            return finished
        return finished


def worker(attempt):
    started = time.perf_counter()
    verify_inputs(include_frozen=True)
    import numpy as np
    import pandas as pd
    import torch
    from threadpoolctl import threadpool_limits, threadpool_info
    torch.set_num_threads(2)
    torch.set_num_interop_threads(2)
    if torch.cuda.is_available():
        raise RuntimeError('GPU must be unavailable for this run')
    sys.path.insert(0, str(KIT))
    official = load_module('e061_official_score', KIT / 'score.py')
    from src.models import tied_content_heads
    predictors = {'candidate': tied_content_heads.predict,
                  'E041': load_module('e061_reference_e041', ROOT / 'submissions/2026-09-19-E041/main.py').predict,
                  'E025': load_module('e061_reference_e025', ROOT / 'submissions/2026-09-09-E025/main.py').predict}
    config = official.load_config(str(KIT / 'config.yml'))
    imported = time.perf_counter()
    inputs, input_manifest = {}, {}
    for name in NAMES:
        schema = official.load_schema(str(KIT / f'data/{name}.json'), config)
        # Phase1 only; TEST row groups/values are not requested from the reader.
        respondents = pd.read_parquet(KIT / f'_sandbox/{name}/respondents.parquet',
                                      filters=[('role', 'in', ['TRAIN', 'DEV'])]).astype(object)
        items = official.generated_items(schema)
        respondents = respondents[['respondent_id', 'role'] + items].reset_index(drop=True)
        counts = respondents.role.value_counts().to_dict()
        if counts != {'TRAIN': schema['split']['n_train'], 'DEV': schema['split']['n_dev']}:
            raise RuntimeError('Synthetic phase1 role count mismatch')
        if respondents.respondent_id.duplicated().any():
            raise RuntimeError('Duplicate synthetic ID')
        for item in items:
            if not set(respondents[item].dropna()).issubset(set(official.options_for(schema, item))):
                raise RuntimeError('Synthetic option mismatch')
        frame, cells, truth = official.sample_rows(schema, respondents, 1)
        predicted = official.scored_items(schema)
        ntrain = int(counts['TRAIN'])
        if not frame.loc[ntrain:, predicted].isna().all().all():
            raise RuntimeError('DEV PREDICT not fully masked')
        inputs[name] = (schema, frame, cells, truth, ntrain)
        input_manifest[name] = {
            'rows': len(frame), 'train': ntrain, 'dev': int(counts['DEV']),
            'predict_items': len(predicted), 'cells': len(cells),
            'gated_predict_items': sum(bool(schema['items'][x].get('gate')) for x in predicted),
            'split_hash': hashlib.sha256(pd.util.hash_pandas_object(
                respondents[['respondent_id', 'role']], index=True).values.tobytes()).hexdigest(),
            'masked_frame_hash': hashlib.sha256(pd.util.hash_pandas_object(frame, index=True).values.tobytes()).hexdigest(),
            'truth_scope': 'Exposed synthetic DEV; harness-only, unscored until all nine vectors frozen'}
    save(OUT / f'phase1-inputs-{attempt:02d}.json', input_manifest)
    audit = CallAudit(OUT / f'calls-{attempt:02d}.jsonl')
    outputs, prediction_files, timings, contracts = {}, {}, {}, {}
    try:
        with threadpool_limits(limits=2):
            save(OUT / f'environment-{attempt:02d}.json', {
                'python': sys.version, 'numpy': np.__version__, 'pandas': pd.__version__,
                'torch': torch.__version__, 'torch_threads': torch.get_num_threads(),
                'torch_interop_threads': torch.get_num_interop_threads(),
                'cuda_available': torch.cuda.is_available(), 'threadpools': threadpool_info(),
                'imports_and_preflight_seconds': imported - started})
            for model, predictor in predictors.items():
                for name in NAMES:
                    schema, frame, cells, truth, ntrain = inputs[name]
                    audit.model, audit.instrument, audit.n_train = model, name, ntrain
                    if audit.full_stack_calls >= 9:
                        raise RuntimeError('Cumulative full-stack call cap')
                    audit.full_stack_calls += 1
                    audit.emit({'event': 'full_stack_enter', 'function': 'predict',
                                'full_stack_call_count': audit.full_stack_calls})
                    print(f'START {model} {name}', flush=True)
                    call_start = time.perf_counter()
                    sys.settrace(audit.trace)
                    try:
                        vectors = predictor(frame.copy(deep=True), schema)
                    finally:
                        sys.settrace(None)
                    wall = time.perf_counter() - call_start
                    official.check(schema, vectors, cells)
                    norm = max(abs(float(np.asarray(v).sum()) - 1.) for v in vectors)
                    if norm > 1e-6:
                        raise RuntimeError('Normalization contract')
                    key = f'{model}-{name}'
                    offsets = np.r_[0, np.cumsum([len(v) for v in vectors])]
                    flat = np.concatenate(vectors).astype(np.float64)
                    path = OUT / f'vectors-{attempt:02d}-{key}.npz'
                    if path.exists():
                        raise FileExistsError(path)
                    np.savez_compressed(path, flat=flat, offsets=offsets)
                    prediction_files[path.name] = sha(path)
                    outputs[key] = vectors
                    timings[key] = wall
                    contracts[key] = {'vectors': len(vectors), 'max_sum_error': norm,
                                      'official_check': 'PASS'}
                    print(f'DONE {key} wall={wall:.3f}s neural_calls={audit.neural_calls}', flush=True)
                if model == 'candidate':
                    candidate_wall = time.perf_counter() - started
                    save(OUT / f'candidate-{attempt:02d}-timing.json', {
                        'wall_seconds_including_imports_and_input_preparation': candidate_wall,
                        'predict_seconds': sum(timings.values()), 'limit_seconds': 900})
                    if candidate_wall > 900:
                        raise RuntimeError('Candidate all3 time cap')
            # This file is written before any truth is mapped to a score.
            save(OUT / f'frozen-predictions-{attempt:02d}.json', {
                'files': prediction_files, 'contracts': contracts,
                'all_nine_calls_complete': True, 'score_access_so_far': 0,
                'source_manifest_sha256': sha(OUT / 'frozen-inputs.json')})
            comparison, scores = {}, {}
            for name in NAMES:
                schema, frame, cells, truth, ntrain = inputs[name]
                for model in predictors:
                    key = f'{model}-{name}'
                    floored = official.floored(outputs[key], schema, cells, config['scoring']['floor'])
                    measured = official.score(schema, config, floored, truth, cells, seed=0)
                    scores[key] = {k: measured[k] for k in ('skill', 'log_score', 'n_cells', 'uniform_reference')}
                differences = [float(np.max(np.abs(np.asarray(a) - np.asarray(b))))
                               for a, b in zip(outputs[f'candidate-{name}'], outputs[f'E041-{name}'])]
                delta041 = scores[f'candidate-{name}']['skill'] - scores[f'E041-{name}']['skill']
                delta025 = scores[f'candidate-{name}']['skill'] - scores[f'E025-{name}']['skill']
                comparison[name] = {'delta_E041': delta041, 'delta_E025': delta025,
                                    'max_absolute_vector_difference_E041': max(differences),
                                    'changed_vectors_over_1e_10': sum(d > 1e-10 for d in differences),
                                    'regression_pass': delta041 >= -.002 and delta025 >= -.002}
            controls = all(comparison[n]['max_absolute_vector_difference_E041'] <= 1e-10
                           for n in ('unicef', 'world_bank'))
            changed = comparison['unhcr']['changed_vectors_over_1e_10'] > 0
            regression = all(v['regression_pass'] for v in comparison.values())
            verdict = ('TECHNICAL_FAILURE' if not controls else 'NO_OP' if not changed else
                       'STOP_REGRESSION' if not regression else 'EXPLORATORY_SOURCE_QUALIFIED_PENDING_RESOURCE_REVIEW')
            save(OUT / 'comparison.json', {
                'verdict': verdict, 'scores': scores, 'comparison': comparison,
                'control_parity': controls, 'nonidentity': changed, 'regression_pass': regression,
                'timings': timings, 'full_stack_calls': audit.full_stack_calls,
                'neural_train_calls': audit.neural_calls, 'target_access_checks': audit.target_calls,
                'metric_optimizer_calls': sum(e['event'] == 'enter' and e['function'] == 'minimize' for e in audit.events),
                'contracts': contracts, 'worker_seconds_to_results': time.perf_counter() - started,
                'scope': 'Reused synthetic phase1 engineering; no ERPIS efficacy inference'})
            print(json.dumps({'verdict': verdict, 'comparison': comparison}, indent=2), flush=True)
    finally:
        sys.settrace(None)
        audit.stream.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('tests', 'freeze', 'run', '_worker'))
    parser.add_argument('--attempt', type=int, default=1)
    args = parser.parse_args()
    if args.mode == 'freeze':
        inputs = verify_inputs()
        tests = read(OUT / f'tests-{args.attempt:02d}-resources.json')
        if tests['status'] != 'PASS':
            raise RuntimeError('Focused tests not qualified')
        save(OUT / 'frozen-inputs.json', {
            'frozen_utc': datetime.now(timezone.utc).isoformat(), 'input_hashes': inputs,
            'code_hashes': {p: sha(ROOT / p) for p in CODE},
            'registration_sha256': sha(OUT / 'registration.md'),
            'test_report_sha256': sha(OUT / f'tests-{args.attempt:02d}-resources.json'),
            'scores_accessed': False})
        print('FROZEN before synthetic predict/score')
        return 0
    if args.mode == '_worker':
        worker(args.attempt)
        return 0
    return monitor(args.mode, args.attempt)


if __name__ == '__main__':
    raise SystemExit(main())
