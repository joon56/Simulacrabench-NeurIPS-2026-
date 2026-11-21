"""E064 bounded synthetic technical controller; no TEST or old cache access."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/analysis/E064-outputs'
KIT = ROOT / 'external/starter-kit'
NAMES = ('unicef', 'world_bank', 'unhcr')
COUNTS = {'unicef': 17856, 'world_bank': 39520, 'unhcr': 132273}
CODE = ('src/models/conditional_gradient.py', 'tests/test_conditional_gradient.py',
        'scripts/check_e064_conditional_gradient.py', 'docs/analysis/E064-outputs/memory_tree.py')
REG_HASH = 'f1113c07ac9127938fc8b02486830e0a23aa1add32ead4e1ce2269811986a8c7'
sys.path.insert(0, str(ROOT))


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_module(name, path):
    if Path(path).parent == KIT and str(KIT) not in sys.path:
        sys.path.insert(0, str(KIT))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_sources(freeze=None):
    entry = read(OUT / 'entry.json')
    checked = {}
    for path, expected in entry['source_hashes'].items():
        if path in ('docs/status.md', 'docs/log.md'):
            continue
        actual = sha(ROOT / path)
        if actual != expected:
            raise RuntimeError('Source identity mismatch: ' + path)
        checked[path] = actual
    if sha(OUT / 'registration.md') != REG_HASH:
        raise RuntimeError('Immutable registration changed')
    if freeze is not None:
        for path, expected in freeze['code_hashes'].items():
            if sha(ROOT / path) != expected:
                raise RuntimeError('Frozen code changed: ' + path)
    return checked


def verify_synthetic():
    checked = {}
    for path, expected in read(OUT / 'entry.json')['synthetic_hashes'].items():
        actual = sha(ROOT / path)
        if actual != expected:
            raise RuntimeError('Authorized synthetic identity mismatch: ' + path)
        checked[path] = actual
    return checked


def stage_limit(mode, prior, remaining_session):
    value = min(900. if mode in ('R', 'H') else 60., 1800. - prior, remaining_session)
    if value <= 0:
        raise RuntimeError('Computational allowance exhausted')
    return value


def usage():
    reports = [read(OUT / 'precontroller-resources.json')]
    for path in sorted((OUT / 'attempts').glob('*')):
        if not path.is_dir():
            continue
        if not (path / 'resources.json').exists():
            raise RuntimeError('Unaccounted attempt: ' + path.name)
        reports.append(read(path / 'resources.json'))
    return sum(x['wall_seconds'] for x in reports), sum(x['wall_seconds'] for x in reports if x['mode'] == 'tests')


def resolve_arm(arm):
    candidates = list((OUT / 'attempts').glob(arm + '-*/complete.json'))
    if len(candidates) != 1:
        raise RuntimeError('Exactly one completed ' + arm + ' required')
    path = candidates[0]
    report = read(path.parent / 'resources.json')
    if report['status'] != 'PASS':
        raise RuntimeError('Arm has no resource PASS: ' + arm)
    return path.parent, read(path)


def require_all_outputs():
    paths = {}
    sources = []
    for arm in ('R', 'H'):
        folder, complete = resolve_arm(arm)
        sources.append(complete['freeze_sha256'])
        for name in NAMES:
            record = complete['outputs'][name]
            if sha(OUT / record['file']) != record['sha256']:
                raise RuntimeError('New raw output identity mismatch')
            paths[arm + '-' + name] = record
    if len(paths) != 6 or len(set(sources)) != 1:
        raise RuntimeError('Six outputs under one code freeze required')
    return paths


def monitor(mode, attempt, only=None, freeze_name='freeze-01.json'):
    begin = time.perf_counter()
    MemoryTree = load_module('e064_memory', OUT / 'memory_tree.py').MemoryTree
    for var in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[var] = '2'
    os.environ.update(CUDA_VISIBLE_DEVICES='', PYTHONDONTWRITEBYTECODE='1',
                      PYTHONPATH=str(ROOT), PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    prior, focused = usage()
    entry = read(OUT / 'entry.json')
    cutoff = datetime.fromisoformat(entry['computation_cutoff_utc'].replace('Z', '+00:00')).timestamp()
    limit = stage_limit(mode, prior, cutoff - time.time())
    if mode == 'tests':
        limit = min(limit, 300. - focused)
    if limit <= 2:
        raise RuntimeError('No launch with insufficient cleanup allowance')
    if mode in ('R', 'H'):
        attempts = [p for p in (OUT / 'attempts').glob('*') if p.name.startswith(('R-', 'H-'))]
        if len(attempts) >= 3:
            raise RuntimeError('Scientific process allowance exhausted')
        if list((OUT / 'attempts').glob(mode + '-*/complete.json')):
            raise RuntimeError('Completed unchanged arm must not be repeated')
        previous = list((OUT / 'attempts').glob(mode + '-*'))
        if previous and not (OUT / 'repair-authorization.json').exists():
            raise RuntimeError('Preserved invalid-arm cause/check/new-freeze record required')
        if mode == 'H':
            resolve_arm('R')
    folder = OUT / 'attempts' / f'{mode}-{attempt:02d}'
    folder.mkdir(parents=True, exist_ok=False)
    save(folder / 'start.json', {'utc': datetime.now(timezone.utc).isoformat(), 'mode': mode,
                                'attempt': attempt, 'only': only, 'freeze': freeze_name,
                                'prior_seconds': prior, 'limit_seconds': limit,
                                'registration_sha256': REG_HASH})
    snapshots = folder / 'source'
    snapshots.mkdir()
    code_hashes = {}
    for path in CODE:
        if (ROOT / path).exists():
            shutil.copyfile(ROOT / path, snapshots / Path(path).name)
            code_hashes[path] = sha(ROOT / path)
    save(folder / 'source.json', code_hashes)
    process = None
    reason = 'COMPLETE'; error = None; peak = {'rss': 0, 'commitment': 0}
    samples = 0; code = None; child_seconds = 0.; max_gap = 0.; previous_sample = None
    try:
        verify_sources(read(OUT / freeze_name) if mode in ('R', 'H', 'score') else None)
        memory = MemoryTree(os.getpid())
        peak = memory.sample()
        if max(peak.values()) > 8 * 1024**3:
            raise RuntimeError('Prelaunch memory cap')
        command = ([sys.executable, '-X', 'utf8', '-B', '-m', 'unittest',
                    only or 'tests.test_conditional_gradient', '-v'] if mode == 'tests' else
                   [sys.executable, '-X', 'utf8', '-B', __file__, '_worker',
                    '--operation', mode, '--attempt', str(attempt), '--freeze', freeze_name])
        with (folder / 'stdout.log').open('x', encoding='utf-8') as log:
            child_start = time.perf_counter()
            process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
            previous_sample = time.perf_counter()
            while process.poll() is None:
                sample = memory.sample(); samples += 1
                sampled_at = time.perf_counter()
                max_gap = max(max_gap, sampled_at - previous_sample)
                previous_sample = sampled_at
                peak = {key: max(peak[key], sample[key]) for key in peak}
                elapsed = time.perf_counter() - begin
                if max_gap > 1.:
                    reason = 'MONITOR_GAP'; break
                if max(peak.values()) > 8 * 1024**3:
                    reason = 'MEMORY_CAP'; break
                if time.time() >= cutoff - 2 or elapsed >= limit - 2:
                    reason = 'TIME_CAP'; break
                time.sleep(.1)
    except Exception:
        reason = 'MONITOR_OR_PRELAUNCH_FAILURE'; error = traceback.format_exc()
    finally:
        if process is not None:
            if process.poll() is None:
                subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                               capture_output=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
            process.wait(timeout=10)
            child_seconds = time.perf_counter() - child_start
            code = process.returncode
        wall = time.perf_counter() - begin
        if wall + prior > 1800 or wall > limit:
            reason = 'TIME_CAP'
        report = {'mode': mode, 'attempt': attempt, 'only': only,
                  'wall_seconds': wall, 'child_seconds': child_seconds,
                  'prior_seconds': prior, 'cumulative_seconds': prior + wall,
                  'focused_cumulative_seconds': focused + (wall if mode == 'tests' else 0),
                  'exit_code': code, 'resource_stop': reason, 'error': error,
                  'peak_owned_tree_bytes': peak, 'sample_count': samples,
                  'max_observed_sample_gap_seconds': max_gap,
                  'sample_interval_seconds': .1, 'threads': 2, 'gpu': 0,
                  'semantics': 'Conservative sum of per-process peak RSS/private, controller and descendants; stage wall includes parent source verification and cleanup',
                  'status': 'PASS' if code == 0 and reason == 'COMPLETE' else 'FAIL'}
        save(folder / 'resources.json', report)
    print(json.dumps(report, indent=2), flush=True)
    return 0 if report['status'] == 'PASS' else 1

def masked_phase1(official,schema,train,dev):
    import pandas as pd
    items=official.generated_items(schema)
    predicted=official.scored_items(schema)
    visible=train[['respondent_id','role']+items].copy()
    given=[n for n in items if schema['items'][n]['class']=='GIVEN']
    hidden=dev[['respondent_id','role']+given].copy()
    hidden[predicted]=float('nan')
    rows=pd.concat((visible,hidden[['respondent_id','role']+items]),ignore_index=True)
    frame,cells,unused_truth=official.sample_rows(schema,rows,1)
    if not frame.loc[len(train):,predicted].isna().all().all():
        raise RuntimeError('Complete DEV PREDICT block must be masked')
    if any(schema['items'].get(c,{}).get('class')=='EXCLUDE' for c in frame):
        raise RuntimeError('EXCLUDE reached predictor')
    return frame,cells


def phase_frames(pd,official,schema,name,with_truth=False):
    """Project DEV to GIVEN columns in model workers; labels only in evaluator."""
    path=KIT/f'_sandbox/{name}/respondents.parquet'
    items=official.generated_items(schema)
    given=[n for n in items if schema['items'][n]['class']=='GIVEN']
    train=pd.read_parquet(path,columns=['respondent_id','role']+items,
                          filters=[('role','==','TRAIN')]).astype(object)
    dev=pd.read_parquet(path,columns=['respondent_id','role']+(items if with_truth else given),
                        filters=[('role','==','DEV')]).astype(object)
    return train,dev


def index_hash(indices):
    import numpy as np
    return hashlib.sha256(np.asarray(indices,dtype='<i8').tobytes()).hexdigest()


def phase_inputs(official,config,with_truth=False):
    import numpy as np
    import pandas as pd
    inputs={}; metadata={}
    for name in NAMES:
        schema=official.load_schema(str(KIT/f'data/{name}.json'),config)
        train,dev=phase_frames(pd,official,schema,name,with_truth)
        ntrain,ndev=len(train),len(dev)
        if (ntrain,ndev)!=(schema['split']['n_train'],schema['split']['n_dev']):
            raise RuntimeError('TRAIN/DEV count mismatch: '+name)
        if set(train.role)!={'TRAIN'} or set(dev.role)!={'DEV'}:
            raise RuntimeError('Unauthorized row role')
        roles=pd.concat((train[['respondent_id','role']],dev[['respondent_id','role']]),ignore_index=True)
        if roles.respondent_id.duplicated().any(): raise RuntimeError('Duplicate synthetic ID')
        for rows in (train,dev):
            for item in official.generated_items(schema):
                if item in rows and not set(rows[item].dropna()).issubset(set(official.options_for(schema,item))):
                    raise RuntimeError('Undeclared synthetic category')
        frame,cells=masked_phase1(official,schema,train,dev)
        if len(cells)!=COUNTS[name]: raise RuntimeError('Canonical cell count mismatch')
        items=official.generated_items(schema)
        if not frame.iloc[:ntrain][items].notna().all().all():
            raise RuntimeError('Synthetic TRAIN completeness changed')
        predicted=official.scored_items(schema)
        positions=np.arange(ntrain)
        outer=np.random.default_rng(0).random(ntrain)<.2
        fit=positions[~outer]
        inner=np.random.default_rng(1).random(len(fit))<.2
        neural_roles={'inner_train':fit[~inner],'inner_stop':fit[inner],
                      'outer_selection':positions[outer],'final_refit':positions}
        cal=positions if ntrain<=6000 else np.sort(np.random.default_rng(0).choice(positions,6000,replace=False))
        meta={'rows':len(frame),'train':ntrain,'dev':ndev,'cells':len(cells),
              'predict_items':len(predicted),'options_widths':[len(official.options_for(schema,n)) for n in predicted],
              'schema_runtime_sha256':hashlib.sha256(json.dumps(schema,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),
              'role_hash':hashlib.sha256(pd.util.hash_pandas_object(roles,index=True).values.tobytes()).hexdigest(),
              'masked_frame_hash':hashlib.sha256(pd.util.hash_pandas_object(frame,index=True).values.tobytes()).hexdigest(),
              'neural_roles':{key:{'rows':len(ix),'index_sha256':index_hash(ix)} for key,ix in neural_roles.items()},
              'lambda_replay':{'rows':len(cal),'index_sha256':index_hash(cal),'independent':False},
              'DEV_predict_columns_read_by_model_worker':False,'TEST_rows_requested':False}
        if name=='unhcr':
            order=np.random.default_rng(4101).permutation(positions)
            nf=min(1200,max(1,ntrain//5)); ns=min(800,max(1,ntrain//10)); nr=min(800,max(1,ntrain//10))
            meta['metric_roles']={key:{'rows':len(ix),'index_sha256':index_hash(ix)} for key,ix in
                                  {'fit':order[:nf],'select':order[nf:nf+ns],'replay':order[nf+ns:nf+ns+nr],'bank':order[nf+ns+nr:]}.items()}
        truth=None
        if with_truth:
            combined=pd.concat((train,dev),ignore_index=True)
            truth_frame,truth_cells,truth=official.sample_rows(schema,combined,1)
            if truth_cells!=cells or not truth_frame.equals(frame):
                raise RuntimeError('Evaluator/model canonical frame mismatch')
        metadata[name]=meta
        inputs[name]=(schema,frame,cells,truth,ntrain)
    return inputs,metadata


def prediction_contract(np,official,schema,vectors,cells):
    official.check(schema,vectors,cells)
    error=max(abs(float(np.asarray(v).sum())-1.) for v in vectors)
    if error>1e-6: raise RuntimeError('Output normalization contract')
    return {'vectors':len(vectors),'max_sum_error':error,'official_check':'PASS',
            'zero_entries':sum(int((np.asarray(v)==0).sum()) for v in vectors)}




class CallAudit:
    WATCH = {'select_ladder', 'tune_and_train', '_train', '_train_on',
             'conditional_agreement', 'hh_sharp_layer', 'supervised_layer', 'round_layer',
             'fit_sections', '_replace_evidence', '_topk_excl', '_evidence', '_max_q',
             'candidate_indices', 'estimate_weights', 'predict'}

    def __init__(self, folder, arm, metadata):
        self.arm = arm; self.instrument = None; self.metadata = metadata
        self.counts = {'pipeline': 0, 'neural': 0, 'metric': 0}
        self.local = dict.fromkeys(self.counts, 0)
        self.retrieval = {}; self.invariants = {}; self.training = {}; self.target_checks = 0
        for path in (OUT / 'attempts').glob('*/calls.jsonl'):
            for line in path.read_text(encoding='utf-8').splitlines():
                record = json.loads(line)
                if record['event'] == 'attempt':
                    self.counts[record['kind']] += 1
        self.stream = (folder / 'calls.jsonl').open('x', encoding='utf-8')

    def emit(self, value):
        value.update(arm=self.arm, instrument=self.instrument, monotonic=time.perf_counter())
        self.stream.write(json.dumps(value, allow_nan=False) + '\n'); self.stream.flush()

    def attempt(self, kind):
        cap = {'pipeline': 9, 'neural': 27, 'metric': 24}[kind]
        if self.counts[kind] >= cap:
            raise RuntimeError(kind + ' attempt cap')
        self.counts[kind] += 1; self.local[kind] += 1
        self.emit({'event': 'attempt', 'kind': kind, 'cumulative': self.counts[kind]})

    def enter_pipeline(self, name):
        self.instrument = name
        self.retrieval[name] = {}
        self.invariants[name] = {}; self.training[name] = []
        self.attempt('pipeline')

    def invariant(self, key, value, phase='always'):
        records = self.invariants[self.instrument].setdefault(key, {'phase': phase, 'hashes': []})
        records['hashes'].append(structured_digest(value))

    def trace(self, frame, event, arg):
        if event != 'call':
            return None
        name = frame.f_code.co_name
        filename = frame.f_code.co_filename.replace('\\', '/')
        source = '/src/models/' in filename or filename.endswith('/src/eval/retrieval_oracle.py')
        loc = frame.f_locals
        meta = self.metadata[self.instrument]
        if source and name == '_targets':
            rows = loc['rows']; predicted = loc['predict_items']
            digest = index_hash(rows.index)
            roles = [k for k, v in meta['neural_roles'].items() if v['index_sha256'] == digest]
            if not roles or (len(rows) and (min(rows.index) < 0 or max(rows.index) >= meta['train'])) or rows[predicted].isna().any().any():
                raise RuntimeError('Neural target role/mask violation')
            self.target_checks += 1
            self.emit({'event': 'targets', 'rows': len(rows), 'roles': roles, 'index_sha256': digest})
            return None
        metric = name == 'minimize' and filename.endswith('/scipy/optimize/_minimize.py')
        if not ((source and name in self.WATCH) or metric):
            return None
        if name == 'predict' and not filename.endswith('/link_sharp.py'):
            return None
        if name == '_train_on':
            self.attempt('neural')
            if str(loc['dev']) != 'cpu':
                raise RuntimeError('Non-CPU training device')
        if metric:
            self.attempt('metric')
            args = loc['args']; nf = meta['metric_roles']['fit']['rows']
            if args[0].shape[0] != nf or args[1].shape[0] != nf or args[2].shape[0] != nf:
                raise RuntimeError('S/Q rows entered metric optimizer')
            self.emit({'event': 'optimizer_slice', 'fit_rows': nf, 'coordinates': len(loc['x0'])})
        if source and name == 'fit_sections':
            for role in ('fit', 'select', 'bank'):
                if index_hash(loc[role]) != meta['metric_roles'][role]['index_sha256']:
                    raise RuntimeError('Metric role identity changed')
        begin = time.perf_counter()
        outer = frame.f_back.f_locals if frame.f_back is not None else {}
        concentration_phase = 'held' if name == '_max_q' and loc.get('posteriors') is outer.get('post') else 'visible'
        self.emit({'event': 'enter', 'function': name})
        frame.f_trace_lines = False
        def returned(current, kind, value):
            if kind == 'return':
                local = current.f_locals
                record = {'event': 'return', 'function': name, 'wall_seconds': time.perf_counter() - begin}
                if name == '_train_on':
                    record.update(epochs_executed=int(local.get('epoch', 0)), best_epoch=int(local.get('best_epoch', 0)),
                                  config=list(local['config']), fit_rows=len(local['X_fit']),
                                  validation_rows=0 if local['X_val'] is None else len(local['X_val']),
                                  device=str(local['dev']), completed=value is not None)
                    if value is not None:
                        expected = 'ConditionalGradientNet' if self.arm == 'H' and self.instrument == 'unhcr' else '_Net'
                        if type(value[0]).__name__ != expected:
                            raise RuntimeError('Local neural factory disconnected')
                        record['network_class'] = type(value[0]).__name__
                        self.training[self.instrument].append(record.copy())
                if name == 'tune_and_train' and value is not None:
                    record.update(w=float(value[0]), selected_config=list(local.get('config', ())),
                                  selected_epoch=int(local.get('best_epoch', 0)))
                    self.retrieval[self.instrument]['neural_selection'] = {
                        'w': record['w'], 'config': record['selected_config'], 'epoch': record['selected_epoch']}
                if name == 'fit_sections' and value is not None:
                    weights, active, diagnostics = value
                    self.retrieval[self.instrument].update(weights=[x.tolist() for x in weights],
                                                           active=list(active), sections=diagnostics)
                    self.invariant('metric_result', value)
                if name == 'estimate_weights' and value is not None:
                    self.invariant('initial_weights', value)
                if name in ('candidate_indices', '_topk_excl', '_evidence', '_replace_evidence') and value is not None:
                    query = local.get('query', local.get('query_pos'))
                    if query is not None:
                        phase = 'held' if len(query) and min(query) >= meta['train'] else 'visible'
                        self.invariant(name + ':' + index_hash(query), value, phase)
                        if name in ('candidate_indices', '_topk_excl'):
                            donors = value if name == 'candidate_indices' else [p[0] for p in value]
                            if any(int(q) in d for q, d in zip(query, donors)):
                                raise RuntimeError('Donor self exclusion broken')
                if name == '_max_q' and value is not None:
                    self.invariant('concentration:' + structured_digest(local['posteriors']), value >= .5, concentration_phase)
                if name in ('supervised_layer', 'round_layer', 'hh_sharp_layer'):
                    self.retrieval[self.instrument]['lambda'] = {k: list(v) for k, v in local.get('lam', {}).items()}
                if name == 'supervised_layer' and value is not None and 'active_items' in local:
                    self.invariant('replay_eligibility', {k: local[k] for k in
                        ('cal', 'original_cal', 'replay', 'active_items', 'conc_cal')})
                if name == 'predict' and value is not None:
                    self.invariant('ladder_and_agreement', {k: local[k] for k in
                        ('cols', 'kappas', 'full_tables', 'cond_tables', 'agreement')})
                if metric and value is not None:
                    record.update(iterations=int(value.nit), evaluations=int(value.nfev), success=bool(value.success))
                self.emit(record)
            return returned
        return returned


def structured_digest(value):
    """Hash only this fresh run's internal engineering state; never deserialize caches."""
    import numpy as np
    digest = hashlib.sha256()
    def visit(v):
        if isinstance(v, np.ndarray):
            digest.update(str((v.dtype.str, v.shape)).encode())
            if v.dtype.hasobject:
                for x in v.flat: visit(x)
            else: digest.update(np.ascontiguousarray(v).tobytes())
        elif isinstance(v, dict):
            digest.update(b'dict')
            for key in sorted(v, key=repr): visit(key); visit(v[key])
        elif isinstance(v, (list, tuple)):
            digest.update(str((type(v).__name__, len(v))).encode())
            for x in v: visit(x)
        elif isinstance(v, set):
            visit(sorted(v, key=repr))
        else:
            digest.update((type(v).__name__ + ':' + repr(v) + ';').encode())
    visit(value)
    return digest.hexdigest()


def compare_invariants(rr, hr):
    results = {}; missing = []
    for name in NAMES:
        a, b = rr['invariants'][name], hr['invariants'][name]
        compared = 0
        for key in sorted(set(a) | set(b)):
            if key in a and key in b:
                if a[key] != b[key]:
                    raise RuntimeError('Expected invariant changed: ' + name + '/' + key)
                compared += 1
            else:
                present, absent = (a, hr) if key in a else (b, rr)
                # Production `if not lam` legitimately omits the held evidence path.
                if present[key]['phase'] != 'held' or absent['retrieval'][name].get('lambda'):
                    raise RuntimeError('Unexpected missing invariant path: ' + name + '/' + key)
                missing.append({'instrument': name, 'key': key, 'reason': 'zero-lambda held path skipped'})
        results[name] = {'matched_keys': compared, 'status': 'PASS'}
    return {'instruments': results, 'permitted_unobserved_paths': missing}


def environment(np, pd, torch):
    import importlib.metadata as metadata
    from threadpoolctl import threadpool_info
    return {'python': sys.version, 'executable_sha256': sha(Path(sys.executable)),
            'packages': {p: metadata.version(p) for p in ('numpy', 'pandas', 'scipy', 'torch', 'pyarrow', 'scikit-learn', 'threadpoolctl', 'PyYAML')},
            'torch_threads': torch.get_num_threads(), 'interop_threads': torch.get_num_interop_threads(),
            'cuda_available': bool(torch.cuda.is_available()), 'threadpools': threadpool_info()}


def evaluate(np, official, config, inputs, paths):
    scores = {}; comparison = {}
    _, hr = resolve_arm('H'); _, rr = resolve_arm('R')
    invariants = compare_invariants(rr, hr)
    for name in NAMES:
        schema, frame, cells, truth, ntrain = inputs[name]
        outputs = {}; floored = {}
        for arm in ('R', 'H'):
            with np.load(OUT / paths[arm + '-' + name]['file'], allow_pickle=False) as stored:
                flat, offsets = stored['flat'], stored['offsets']
                outputs[arm] = [flat[offsets[i]:offsets[i+1]] for i in range(len(offsets)-1)]
            prediction_contract(np, official, schema, outputs[arm], cells)
            floored[arm] = official.floored(outputs[arm], schema, cells, config['scoring']['floor'])
            measured = official.score(schema, config, floored[arm], truth, cells, seed=0)
            scores[arm + '-' + name] = {k: measured[k] for k in ('skill', 'log_score', 'n_cells', 'uniform_reference')}
        differences = np.array([np.max(np.abs(a - b)) for a, b in zip(outputs['H'], outputs['R'])])
        delta = scores['H-' + name]['skill'] - scores['R-' + name]['skill']
        comparison[name] = {'delta_skill_H_R': delta,
                            'delta_log_H_R': scores['H-' + name]['log_score'] - scores['R-' + name]['log_score'],
                            'max_raw_difference': float(differences.max()), 'changed_vectors': int((differences > 0).sum()),
                            'regression_pass': delta >= -.002}
    controls = all(comparison[n]['max_raw_difference'] == 0 for n in ('unicef', 'world_bank'))
    changed = comparison['unhcr']['changed_vectors'] > 0
    regression = all(x['regression_pass'] for x in comparison.values())
    verdicts = []
    if not controls: verdicts.append('TECHNICAL_FAIL')
    if not any(x['changed_vectors'] for x in comparison.values()): verdicts.append('STOP_NO_OP')
    if not regression: verdicts.append('REGRESSION_HOLD')
    if not verdicts and changed: verdicts.append('LOCAL_TECHNICAL_PASS_FOR_S0_PENDING_RESOURCE_RECEIPT')
    rlam = rr['retrieval']['unhcr'].get('lambda', {}); hlam = hr['retrieval']['unhcr'].get('lambda', {})
    lambda_changed = sum(rlam.get(k, [0., 0.]) != hlam.get(k, [0., 0.]) for k in set(rlam) | set(hlam))
    return {'verdicts': verdicts, 'scores': scores, 'comparison': comparison,
            'expected_invariants': invariants,
            'H_active': hr['retrieval']['unhcr'].get('active', []),
            'R_active': rr['retrieval']['unhcr'].get('active', []), 'lambda_items_changed': lambda_changed,
            'neural_selection': {arm: report['retrieval']['unhcr']['neural_selection'] for arm, report in (('R', rr), ('H', hr))},
            'control_parity': controls, 'regression_pass': regression,
            'channel': 'Already exposed synthetic TRAIN/DEV; no new oracle, independent audit or actual UNHCR efficacy'}


def worker(operation, attempt, freeze_name):
    begin = time.perf_counter()
    folder = OUT / 'attempts' / f'{operation}-{attempt:02d}'
    freeze = read(OUT / freeze_name) if operation != 'prepare' else None
    verified = verify_sources(freeze)
    synthetic = verify_synthetic()
    paths = None
    if operation == 'score':
        paths = require_all_outputs()
        save(folder / 'frozen-predictions.json', {'outputs': paths, 'six_complete': True,
                                                'DEV_truth_access_before_freeze': False, 'freeze_sha256': sha(OUT / freeze_name)})
    import numpy as np
    import pandas as pd
    import torch
    from threadpoolctl import threadpool_limits
    torch.set_num_threads(2); torch.set_num_interop_threads(2)
    if torch.cuda.is_available(): raise RuntimeError('GPU must be unavailable')
    env = environment(np, pd, torch)
    save(folder / 'environment.json', env)
    official = load_module('e064_official', KIT / 'score.py')
    config = official.load_config(str(KIT / 'config.yml'))
    if config['scoring']['floor'] != .001: raise RuntimeError('Official floor changed')
    if freeze is not None and env != freeze['environment']:
        raise RuntimeError('Environment changed after freeze')
    original_read = pd.read_parquet
    def projected_read(path, columns, filters, **kwargs):
        allowed = [KIT / f'_sandbox/{n}/respondents.parquet' for n in NAMES]
        if Path(path) not in allowed or filters not in ([('role', '==', 'TRAIN')], [('role', '==', 'DEV')]):
            raise RuntimeError('Unauthorized source/role request')
        if filters == [('role', '==', 'DEV')] and operation != 'score':
            name = Path(path).parent.name
            schema = official.load_schema(str(KIT / f'data/{name}.json'), config)
            expected = ['respondent_id', 'role'] + [n for n in official.generated_items(schema) if schema['items'][n]['class'] == 'GIVEN']
            if columns != expected: raise RuntimeError('DEV PREDICT projection reached model worker')
        with (folder / 'projection.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps({'source': str(Path(path).relative_to(ROOT)), 'role_filter': filters,
                                     'columns': columns, 'operation': operation}) + '\n')
        return original_read(path, columns=columns, filters=filters, **kwargs)
    pd.read_parquet = projected_read
    with threadpool_limits(limits=2):
        inputs, metadata = phase_inputs(official, config, operation == 'score')
        if operation == 'prepare':
            qualification = read(OUT / 'unit-qualification.json')
            if qualification['status'] != 'PASS': raise RuntimeError('Unit qualification missing')
            for path, digest in qualification['code_hashes'].items():
                if sha(ROOT / path) != digest: raise RuntimeError('Unit/source freeze mismatch')
            save(OUT / freeze_name, {'frozen_utc': datetime.now(timezone.utc).isoformat(),
                 'source_hashes': verified, 'synthetic_hashes': synthetic,
                 'code_hashes': {p: sha(ROOT / p) for p in CODE}, 'environment': env,
                 'registration_sha256': REG_HASH, 'unit_qualification_sha256': sha(OUT / 'unit-qualification.json'),
                 'phase1': metadata, 'deadline': read(OUT / 'entry.json')['deadline_utc'],
                 'DEV_truth_accessed': False})
            print('FROZEN before full-stack fitting/scoring', flush=True)
            return 0
        if metadata != freeze['phase1']: raise RuntimeError('Frame/schema/role identity changed')
        if operation == 'score':
            result = evaluate(np, official, config, inputs, paths)
            save(folder / 'comparison.json', result)
            print(json.dumps({'verdicts': result['verdicts'], 'comparison': result['comparison']}, indent=2), flush=True)
            return 0
        from src.models import supervised_retrieval as original
        if operation == 'H':
            from src.models import conditional_gradient as candidate
            predictor = candidate.predict
        else:
            predictor = original.predict
        audit = CallAudit(folder, operation, metadata)
        outputs = {}; timings = {}
        try:
            for name in NAMES:
                schema, frame, cells, truth, ntrain = inputs[name]
                if truth is not None: raise RuntimeError('DEV truth retained by model worker')
                audit.enter_pipeline(name)
                print('START', operation, name, flush=True)
                started = time.perf_counter(); sys.settrace(audit.trace)
                try: vectors = predictor(frame.copy(deep=True), schema)
                finally: sys.settrace(None)
                timing = time.perf_counter() - started
                contract = prediction_contract(np, official, schema, vectors, cells)
                path = folder / ('vectors-' + name + '.npz')
                with path.open('xb') as stream:
                    np.savez_compressed(stream, flat=np.concatenate(vectors).astype(np.float64),
                                        offsets=np.r_[0, np.cumsum([len(v) for v in vectors])])
                outputs[name] = {'file': path.relative_to(OUT).as_posix(), 'sha256': sha(path), 'contract': contract}
                timings[name] = timing
                audit.emit({'event': 'pipeline_complete', 'vectors': len(vectors), 'predict_seconds': timing})
                print('DONE', operation, name, round(timing, 3), 's', flush=True)
            if audit.local != {'pipeline': 3, 'neural': 9, 'metric': 8}:
                raise RuntimeError('Unexpected full-stack call totals: ' + str(audit.local))
            save(folder / 'complete.json', {'outputs': outputs, 'timings': timings,
                 'worker_seconds': time.perf_counter() - begin, 'calls_this_worker': audit.local,
                 'calls_cumulative': audit.counts, 'target_checks': audit.target_checks,
                 'retrieval': audit.retrieval, 'invariants': audit.invariants,
                 'training': audit.training, 'DEV_truth_accessed': False,
                 'freeze_sha256': sha(OUT / freeze_name)})
        finally:
            sys.settrace(None); audit.stream.close()
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('tests', 'prepare', 'R', 'H', 'score', '_worker'))
    parser.add_argument('--attempt', type=int, default=1)
    parser.add_argument('--only')
    parser.add_argument('--operation')
    parser.add_argument('--freeze', default='freeze-01.json')
    args = parser.parse_args()
    if args.mode == '_worker':
        try:
            return worker(args.operation, args.attempt, args.freeze)
        except Exception:
            folder = OUT / 'attempts' / f'{args.operation}-{args.attempt:02d}'
            save(folder / 'error.json', {'utc': datetime.now(timezone.utc).isoformat(), 'traceback': traceback.format_exc()})
            raise
    return monitor(args.mode, args.attempt, args.only, args.freeze)


if __name__ == '__main__':
    raise SystemExit(main())

