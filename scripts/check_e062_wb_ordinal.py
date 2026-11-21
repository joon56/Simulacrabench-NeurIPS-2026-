"""E062 bounded synthetic engineering. Never access TEST or old output caches."""
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

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/analysis/E062-outputs'
KIT=ROOT/'external/starter-kit'
NAMES=('unicef','world_bank','unhcr')
COUNTS={'unicef':17856,'world_bank':39520,'unhcr':132273}
CODE=('src/models/wb_ordinal_heads.py','tests/test_wb_ordinal_heads.py','scripts/check_e062_wb_ordinal.py')
sys.path.insert(0,str(ROOT))


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path,value):
    with Path(path).open('x',encoding='utf-8') as f:
        json.dump(value,f,indent=2,allow_nan=False)
        f.write('\n')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_module(name,path):
    if Path(path).parent==KIT and str(KIT) not in sys.path:
        sys.path.insert(0,str(KIT))
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def verify_inputs(frozen=False):
    entry=read(OUT/'entry.json')
    supplement=read(OUT/'source-supplement.json')['source_hashes']
    checked={}
    for path,expected in {**entry['source_hashes'],**supplement,**entry['synthetic_hashes']}.items():
        if path in ('docs/status.md','docs/log.md'): continue
        actual=sha(ROOT/path)
        if actual!=expected: raise RuntimeError('Input identity mismatch: '+path)
        checked[path]=actual
    if sha(OUT/'registration.md')!=entry['registration_sha256']:
        raise RuntimeError('Registration changed')
    if frozen:
        freeze=read(OUT/'frozen-inputs.json')
        if checked!=freeze['input_hashes']:
            raise RuntimeError('Frozen input manifest changed')
        for path,expected in freeze['code_hashes'].items():
            if sha(ROOT/path)!=expected: raise RuntimeError('Frozen code changed: '+path)
    return checked


def prior_seconds():
    return sum(read(p)['wall_seconds'] for p in OUT.glob('*-resources.json'))


def monitor(mode,attempt,only=None):
    from scripts.check_e057 import MemoryTree
    for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        os.environ[name]='2'
    os.environ.update(CUDA_VISIBLE_DEVICES='',PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(ROOT),PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    report_path=OUT/f'{mode}-{attempt:02d}-resources.json'
    log_path=OUT/f'{mode}-{attempt:02d}.log'
    if report_path.exists() or log_path.exists(): raise FileExistsError('Preserve prior attempt')
    entry=read(OUT/'entry.json')
    deadline=datetime.fromisoformat(entry['computation_cutoff_utc'].replace('Z','+00:00')).timestamp()
    prior=prior_seconds()
    if mode in ('E025','E041','candidate','score'): verify_inputs(True)
    command=([sys.executable,'-X','utf8','-B','-m','unittest',only or 'tests.test_wb_ordinal_heads','-v'] if mode=='tests' else [sys.executable,'-X','utf8','-B',__file__,'_worker','--operation',mode,'--attempt',str(attempt)])
    memory=MemoryTree(os.getpid())
    peak=memory.sample()
    if max(peak.values())>8*1024**3 or time.time()>=deadline or prior>=1800:
        raise RuntimeError('Prelaunch resource limit')
    start=time.perf_counter(); started_utc=datetime.now(timezone.utc).isoformat()
    remaining_session=deadline-time.time()
    process=None; reason='COMPLETE'; error=None; samples=0
    with log_path.open('x',encoding='utf-8') as log:
        try:
            process=subprocess.Popen(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
            while process.poll() is None:
                sample=memory.sample(); samples+=1
                peak={k:max(peak[k],sample[k]) for k in peak}
                elapsed=time.perf_counter()-start
                if max(peak.values())>8*1024**3: reason='MEMORY_CAP'; break
                if elapsed>=remaining_session or elapsed+prior>=1800: reason='TIME_CAP'; break
                if mode=='candidate' and elapsed>900: reason='CANDIDATE_TIME_CAP'; break
                if mode in ('tests','prepare') and elapsed>120: reason='FOCUSED_TIMEOUT'; break
                time.sleep(.1)
        except Exception as exc:
            reason='MONITOR_OR_LAUNCH_FAILURE'; error=repr(exc)
        finally:
            if process is not None:
                if process.poll() is None:
                    subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True,timeout=10)
                process.wait(timeout=10)
    wall=time.perf_counter()-start
    code=None if process is None else process.returncode
    report={'mode':mode,'attempt':attempt,'started_utc':started_utc,'wall_seconds':wall,
            'prior_worker_seconds':prior,'cumulative_worker_seconds':prior+wall,'exit_code':code,
            'resource_stop':reason,'error':error,'peak_owned_tree_bytes':peak,'sample_count':samples,
            'sample_interval_seconds':.1,'counter_semantics':'Conservative sum of per-process peak RSS/private commitment, owned controller and descendants',
            'numerical_threads':2,'gpu':0,'status':'PASS' if code==0 and reason=='COMPLETE' else 'FAIL'}
    save(report_path,report)
    print(json.dumps(report,indent=2))
    return 0 if report['status']=='PASS' else 1


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


class CallAudit:
    """Observe real source entries without substituting learner/selection code."""
    WATCH={'select_ladder','tune_and_train','_train_on','conditional_agreement',
           'hh_sharp_layer','supervised_layer','_topk_excl','_evidence','_best_lambda'}
    def __init__(self,path,model,metadata):
        self.model=model; self.instrument=None; self.metadata=metadata; self.events=[]
        self.neural_calls=0; self.pipeline_calls=0; self.target_checks=0
        for previous in OUT.glob('calls-*.jsonl'):
            for line in previous.read_text(encoding='utf-8').splitlines():
                record=json.loads(line)
                self.neural_calls+=record.get('event')=='enter' and record.get('function')=='_train_on'
                self.pipeline_calls+=record.get('event')=='pipeline_enter'
        self.stream=Path(path).open('x',encoding='utf-8')

    def emit(self,value):
        value.update(model=self.model,instrument=self.instrument,monotonic=time.perf_counter())
        self.events.append(value)
        self.stream.write(json.dumps(value,allow_nan=False)+'\n'); self.stream.flush()

    def enter_pipeline(self,name):
        if self.pipeline_calls>=9: raise RuntimeError('Pipeline allowance exhausted')
        self.instrument=name; self.pipeline_calls+=1
        self.emit({'event':'pipeline_enter','pipeline_attempts':self.pipeline_calls})

    def trace(self,frame,event,arg):
        if event!='call': return None
        name=frame.f_code.co_name
        filename=frame.f_code.co_filename.replace('\\','/')
        source='/src/models/' in filename or '/submissions/2026-09-' in filename
        if source and name=='_targets':
            rows=frame.f_locals['rows']; predicted=frame.f_locals['predict_items']
            meta=self.metadata[self.instrument]
            digest=index_hash(rows.index)
            roles=[role for role,record in meta['neural_roles'].items() if record['index_sha256']==digest]
            if not roles or (len(rows) and (min(rows.index)<0 or max(rows.index)>=meta['train'])) or rows[predicted].isna().any().any():
                raise RuntimeError('Training target role/mask violation')
            self.target_checks+=1
            self.emit({'event':'targets','rows':len(rows),'roles':roles,'index_sha256':digest})
            return None
        metric=name=='minimize' and filename.endswith('/scipy/optimize/_minimize.py')
        if not ((source and name in self.WATCH) or metric): return None
        if name=='_train_on':
            if self.neural_calls>=27: raise RuntimeError('Neural allowance exhausted')
            self.neural_calls+=1
        start=time.perf_counter()
        self.emit({'event':'enter','function':name,'neural_attempts':self.neural_calls})
        frame.f_trace_lines=False
        def returned(current,kind,value):
            if kind=='return':
                loc=current.f_locals
                result={'event':'return','function':name,'wall_seconds':time.perf_counter()-start}
                if name=='_train_on':
                    result.update(epochs_executed=int(loc.get('epoch',0)),best_epoch=int(loc.get('best_epoch',0)),
                                  fit_rows=len(loc['X_fit']),validation_rows=0 if loc['X_val'] is None else len(loc['X_val']),
                                  config=list(loc['config']),device=str(loc['dev']),returned=value is not None)
                elif name=='tune_and_train' and value is not None:
                    result.update(w=float(value[0]),config=list(loc.get('config',())),best_epoch=int(loc.get('best_epoch',0)),
                                  final_refit=value[1] is not None)
                elif name in ('hh_sharp_layer','supervised_layer'):
                    result.update(nonzero_lambda_items=len(loc.get('lam',{})),active_sections=[int(x) for x in loc.get('active',[])])
                elif metric and value is not None:
                    result.update(iterations=int(value.nit),success=bool(value.success),evaluations=int(value.nfev))
                self.emit(result)
            return returned
        return returned


def prediction_contract(np,official,schema,vectors,cells):
    official.check(schema,vectors,cells)
    error=max(abs(float(np.asarray(v).sum())-1.) for v in vectors)
    if error>1e-6: raise RuntimeError('Output normalization contract')
    return {'vectors':len(vectors),'max_sum_error':error,'official_check':'PASS',
            'zero_entries':sum(int((np.asarray(v)==0).sum()) for v in vectors)}


def require_all_outputs():
    paths={}
    for model in ('E025','E041','candidate'):
        complete=read(OUT/f'{model}-complete.json')
        report=read(OUT/f'{model}-01-resources.json')
        if report['status']!='PASS': raise RuntimeError('Model worker not resource-qualified')
        for name in NAMES:
            key=f'{model}-{name}'
            record=complete['outputs'][name]
            path=OUT/record['file']
            if sha(path)!=record['sha256']: raise RuntimeError('Raw output changed')
            paths[key]=record
    if len(paths)!=9: raise RuntimeError('All nine outputs required before score')
    return paths


def evaluate(np,official,config,inputs,paths):
    from src.models.wb_ordinal_heads import TARGETS
    scores={}; comparison={}; breakdown={}
    for name in NAMES:
        schema,frame,cells,truth,ntrain=inputs[name]
        outputs={}; floored={}
        for model in ('E025','E041','candidate'):
            record=paths[f'{model}-{name}']
            with np.load(OUT/record['file'],allow_pickle=False) as stored:
                flat,offsets=stored['flat'],stored['offsets']
                outputs[model]=[flat[offsets[i]:offsets[i+1]] for i in range(len(offsets)-1)]
            prediction_contract(np,official,schema,outputs[model],cells)
            floored[model]=official.floored(outputs[model],schema,cells,config['scoring']['floor'])
            measured=official.score(schema,config,floored[model],truth,cells,seed=0)
            scores[f'{model}-{name}']={k:measured[k] for k in ('skill','log_score','n_cells','uniform_reference')}
        delta041=scores[f'candidate-{name}']['skill']-scores[f'E041-{name}']['skill']
        delta025=scores[f'candidate-{name}']['skill']-scores[f'E025-{name}']['skill']
        diffs=np.array([np.max(np.abs(np.asarray(a)-np.asarray(b))) for a,b in zip(outputs['candidate'],outputs['E041'])])
        comparison[name]={'delta_E041':delta041,'delta_E025':delta025,
                          'max_raw_difference_E041':float(diffs.max()),'changed_vectors_exact':int((diffs>0).sum()),
                          'regression_pass':delta041>=-.002 and delta025>=-.002}
        if name=='world_bank':
            logdiff=[]; target=[]; missing=[]
            for i,((_,_,item),answer) in enumerate(zip(cells,truth)):
                k=official.options_for(schema,item).index(answer)
                logdiff.append(float(np.log(floored['candidate'][i][k])-np.log(floored['E041'][i][k])))
                target.append(item in TARGETS); missing.append(item in TARGETS and answer=='Not answered')
            a=np.array(logdiff); target=np.array(target); missing=np.array(missing)
            for label,mask in {'target16':target,'other60':~target,'target16_Not_answered':missing,'target16_substantive':target&~missing}.items():
                breakdown[label]={'cells':int(mask.sum()),'mean_log_score_difference_E041':float(a[mask].mean()) if mask.any() else None,
                                  'changed_vectors_exact':int((diffs[mask]>0).sum())}
    controls=all(comparison[n]['max_raw_difference_E041']==0 for n in ('unicef','unhcr'))
    changed=comparison['world_bank']['changed_vectors_exact']>0
    regression=all(v['regression_pass'] for v in comparison.values())
    verdict='TECHNICAL_FAIL' if not controls else 'NO_OP' if not changed else 'REGRESSION_HOLD' if not regression else 'EXPLORATORY_SOURCE_QUALIFIED_PENDING_FINAL_RESOURCE_RECEIPT'
    return {'verdict':verdict,'scores':scores,'comparison':comparison,'WB_descriptive_breakdown':breakdown,
            'control_parity':controls,'WB_changed':changed,'regression_pass':regression,
            'channel':'Previously exposed synthetic TRAIN/DEV engineering, not independent WB efficacy'}


def worker(operation,attempt):
    started=time.perf_counter()
    verify_inputs(operation!='prepare')
    if operation in ('E025','E041','candidate'):
        save(OUT/f'{operation}-started.json',{'utc':datetime.now(timezone.utc).isoformat(),'attempt':attempt})
    paths=None
    if operation=='score':
        paths=require_all_outputs()
        save(OUT/'frozen-predictions.json',{'outputs':paths,'all_nine_complete':True,'engineering_scores_accessed':0,
                                         'frozen_source_manifest_sha256':sha(OUT/'frozen-inputs.json')})
    import numpy as np
    import pandas as pd
    import torch
    from threadpoolctl import threadpool_limits,threadpool_info
    torch.set_num_threads(2); torch.set_num_interop_threads(2)
    if torch.cuda.is_available(): raise RuntimeError('GPU must be unavailable')
    official=load_module('e062_official',KIT/'score.py')
    config=official.load_config(str(KIT/'config.yml'))
    if config['scoring']['floor']!=.001: raise RuntimeError('Official floor changed')
    predictor=None
    if operation=='candidate':
        from src.models import wb_ordinal_heads
        predictor=wb_ordinal_heads.predict
    elif operation in ('E025','E041'):
        snapshot='2026-09-09-E025' if operation=='E025' else '2026-09-19-E041'
        predictor=load_module('e062_'+operation,ROOT/f'submissions/{snapshot}/main.py').predict
    with threadpool_limits(limits=2):
        inputs,metadata=phase_inputs(official,config,operation=='score')
        if operation=='prepare':
            from src.models import wb_ordinal_heads as candidate
            schema,frame,*_=inputs['world_bank']
            records,items,options=candidate._layout(frame,schema)
            indices=candidate.ordinal_indices(official.scored_items(schema),records,options)
            if len(indices)!=16: raise RuntimeError('WB target count')
            reports=[read(OUT/'tests-02-resources.json'),read(OUT/'tests-03-resources.json')]
            if any(r['status']!='PASS' for r in reports): raise RuntimeError('Affected tests incomplete')
            save(OUT/'frozen-inputs.json',{'frozen_utc':datetime.now(timezone.utc).isoformat(),
                 'input_hashes':verify_inputs(False),'code_hashes':{p:sha(ROOT/p) for p in CODE},
                 'registration_sha256':sha(OUT/'registration.md'),'phase1':metadata,'target_indices':list(indices),
                 'test_reports':{f'tests-{i:02d}-resources.json':sha(OUT/f'tests-{i:02d}-resources.json') for i in (2,3)},
                 'engineering_scores_accessed':False,'deadline':read(OUT/'entry.json')['deadline_utc']})
            print('FROZEN source/input/runtime schema/splits before any pipeline',flush=True)
            return 0
        if metadata!=read(OUT/'frozen-inputs.json')['phase1']:
            raise RuntimeError('Runtime frame/schema/split identity changed')
        save(OUT/f'environment-{operation}-{attempt:02d}.json',{'python':sys.version,'numpy':np.__version__,
             'pandas':pd.__version__,'torch':torch.__version__,'torch_threads':torch.get_num_threads(),
             'interop_threads':torch.get_num_interop_threads(),'cuda_available':False,'threadpools':threadpool_info(),
             'imports_input_seconds':time.perf_counter()-started})
        if operation=='score':
            result=evaluate(np,official,config,inputs,paths)
            result['scoring_worker_seconds']=time.perf_counter()-started
            save(OUT/'comparison.json',result)
            print(json.dumps({'verdict':result['verdict'],'comparison':result['comparison']},indent=2),flush=True)
            return 0
        audit=CallAudit(OUT/f'calls-{operation}-{attempt:02d}.jsonl',operation,metadata)
        outputs={}; timings={}
        try:
            for name in NAMES:
                schema,frame,cells,truth,ntrain=inputs[name]
                if truth is not None: raise RuntimeError('DEV truth retained by model worker')
                audit.enter_pipeline(name)
                print(f'START {operation} {name}',flush=True)
                begin=time.perf_counter(); sys.settrace(audit.trace)
                try: vectors=predictor(frame.copy(deep=True),schema)
                finally: sys.settrace(None)
                predict_seconds=time.perf_counter()-begin
                validation_started=time.perf_counter()
                contract=prediction_contract(np,official,schema,vectors,cells)
                path=OUT/f'vectors-{operation}-{name}.npz'
                if path.exists(): raise FileExistsError(path)
                np.savez_compressed(path,flat=np.concatenate(vectors).astype(np.float64),offsets=np.r_[0,np.cumsum([len(v) for v in vectors])])
                outputs[name]={'file':path.name,'sha256':sha(path),'contract':contract}
                timings[name]={'predict_seconds':predict_seconds,'validate_save_seconds':time.perf_counter()-validation_started}
                audit.emit({'event':'pipeline_return','predict_seconds':predict_seconds,'vectors':len(vectors)})
                print(f'DONE {operation} {name} {predict_seconds:.3f}s neural={audit.neural_calls}',flush=True)
            save(OUT/f'{operation}-complete.json',{'outputs':outputs,'timings':timings,
                 'worker_seconds':time.perf_counter()-started,'pipeline_attempts_cumulative':audit.pipeline_calls,
                 'neural_attempts_cumulative':audit.neural_calls,'target_checks':audit.target_checks,
                 'metric_calls_this_worker':sum(e['event']=='enter' and e.get('function')=='minimize' for e in audit.events),
                 'scores_accessed':0})
        finally:
            sys.settrace(None); audit.stream.close()
    return 0


def main():
    p=argparse.ArgumentParser()
    p.add_argument('mode',choices=('tests','prepare','E025','E041','candidate','score','_worker'))
    p.add_argument('--attempt',type=int,default=1)
    p.add_argument('--only')
    p.add_argument('--operation')
    args=p.parse_args()
    if args.mode=='_worker': return worker(args.operation,args.attempt)
    return monitor(args.mode,args.attempt,args.only)


if __name__=='__main__':
    raise SystemExit(main())
