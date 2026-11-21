"""One reference or candidate process; launched only by watchdog.py."""
import argparse
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import time
import traceback

START=time.perf_counter()
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
TEMP=ROOT/'tmp/a040-full-path-resume1'
SOURCE=ROOT/'tmp/a040-local-technical/source/tabicl-0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3/src'
CHECKPOINT=ROOT/'tmp/a040-local-technical/acquisition/tabicl-classifier-v2-20260212.ckpt'
sys.path[:0]=[str(HERE),str(SOURCE)]
from telemetry import EventLog
PARSER=argparse.ArgumentParser();PARSER.add_argument('mode',choices=['reference','candidate'])
MODE=PARSER.parse_args().mode
OUT=HERE/MODE
LOG=EventLog((OUT/'events.jsonl').open('x',encoding='utf-8'))
COUNTS=dict(checkpoint_loads=0,expert_fit=0,expert_predict=0,expert_empty=0,expert_singleton=0)
NETWORK=dict(deliberate_blocks=0,package_attempts=0,subprocess_attempts=0)
EXPERT_STAGES=[]


def save(name,value):
    (OUT/name).write_text(json.dumps(value,indent=2),encoding='utf-8')


def state_hash(model):
    digest=hashlib.sha256()
    for name,value in model.state_dict().items():
        digest.update(name.encode());digest.update(value.detach().cpu().contiguous().numpy().tobytes())
    return digest.hexdigest()


def main():
    import psutil
    current=psutil.Process();current.cpu_affinity(current.cpu_affinity()[:2])
    for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[name]='2'
    os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HOME=str(TEMP/'hf-offline'),A040_CHECKPOINT=str(CHECKPOINT))
    deliberate=[True]
    def audit(name,args):
        if name in ('socket.connect','socket.getaddrinfo','socket.sendto'):
            NETWORK['deliberate_blocks' if deliberate[0] else 'package_attempts']+=1
            raise PermissionError('A040 runtime network denied')
        if name in ('subprocess.Popen','os.system','os.posix_spawn'):
            NETWORK['subprocess_attempts']+=1
            raise PermissionError('A040 runtime subprocess denied')
    sys.addaudithook(audit)
    import socket
    with socket.socket() as probe:
        try:probe.connect(('127.0.0.1',9))
        except PermissionError:pass
        else:raise AssertionError('Network guard failed')
    deliberate[0]=False
    manifest=json.loads((HERE/'frozen-inputs/manifest.json').read_text(encoding='utf-8-sig'))
    for row in manifest['files']:
        if hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()!=row['sha256']:raise AssertionError('Frozen input changed: '+row['path'])
    LOG.emit('manifest_verified',files=len(manifest['files']),mode=MODE)
    import numpy as np
    import pandas as pd
    import torch
    global TORCH
    TORCH=torch
    torch.set_num_threads(2);torch.set_num_interop_threads(2)
    if not torch.cuda.is_available():raise RuntimeError('Required local CUDA unavailable')
    if '3070' not in torch.cuda.get_device_name(0):raise RuntimeError('Unexpected GPU')
    torch.cuda.reset_peak_memory_stats()
    LOG.emit('runtime',torch=torch.__version__,cuda=torch.version.cuda,device=torch.cuda.get_device_name(0),affinity=current.cpu_affinity())
    from orchestration import FullPathPredictor,RolePlan,layout,restore,fingerprint
    from observer import E041Observer
    from schema_entry import runtime_entry
    source=ROOT/'submissions/2026-09-19-E041/main.py'
    spec=importlib.util.spec_from_file_location('e041',source)
    e041=importlib.util.module_from_spec(spec);sys.modules['e041']=e041;spec.loader.exec_module(e041)
    adapter=None;before_state=None
    if MODE=='candidate':
        original_load=torch.load
        def observed_load(path,*args,**kwargs):
            if Path(path).resolve()!=CHECKPOINT.resolve():raise PermissionError('Unexpected model file')
            if hashlib.sha256(CHECKPOINT.read_bytes()).hexdigest()!='bdc7dbd5e4ff21f8f0456fcf90c6b7cdf72dbea960f2d05b19bec19f9b3d4ed0':raise AssertionError('Checkpoint bytes changed')
            COUNTS['checkpoint_loads']+=1
            start=time.perf_counter();value=original_load(path,*args,**kwargs)
            LOG.emit('checkpoint_load',count=COUNTS['checkpoint_loads'],seconds=time.perf_counter()-start)
            return value
        torch.load=observed_load
        import adapter
        before_state=state_hash(adapter.SHARED_MODEL)
        if COUNTS['checkpoint_loads']!=1:raise AssertionError('Import-time load contract')
        LOG.emit('candidate_import_complete',checkpoint_loads=1,state_sha256=before_state,
                 gpu_allocated_peak=torch.cuda.max_memory_allocated(),gpu_reserved_peak=torch.cuda.max_memory_reserved())
    reference=None
    if MODE=='candidate':
        ref_result=json.loads((HERE/'reference/result.json').read_text())
        if ref_result['outcome']!='REFERENCE_PASS':raise PermissionError('Reference did not pass')
        reference={}
        for name in ('unicef','world_bank','unhcr'):
            path=TEMP/'reference'/(name+'.json')
            if hashlib.sha256(path.read_bytes()).hexdigest()!=ref_result['output_hashes'][name]:raise AssertionError('Reference output changed')
            reference[name]=json.loads(path.read_text())
        LOG.emit('new_reference_read',instruments=3,old_predictions_read=False)
    observer=E041Observer(e041,LOG,reference)
    global OBSERVER
    OBSERVER=observer
    expert_scope={}
    if MODE=='candidate':
        original_fit=adapter.SharedClassifier.fit
        original_predict=adapter.SharedClassifier.predict_proba
        def observed_fit(self,X,y,*args,**kwargs):
            view=expert_scope['view']
            if list(X.index)!=view.fit_rows or list(X.columns)!=view.given:raise PermissionError('Expert fit role/feature mismatch')
            expected=view.shadow.loc[view.fit_rows,expert_scope['head']].map({v:i for i,v in enumerate(view.options[expert_scope['head']])}).to_numpy(dtype=int)
            if not np.array_equal(y,expected):raise PermissionError('Expert target isolation failed')
            COUNTS['expert_fit']+=1
            start=time.perf_counter();value=original_fit(self,X,y,*args,**kwargs);torch.cuda.synchronize()
            LOG.emit('expert_fit_end',stage=expert_scope['stage'],head_name=expert_scope['head'],seconds=time.perf_counter()-start,fit_rows=len(X),
                     gpu_allocated_peak=torch.cuda.max_memory_allocated(),gpu_reserved_peak=torch.cuda.max_memory_reserved())
            return value
        def observed_predict(self,X,*args,**kwargs):
            view=expert_scope['view']
            if list(X.index)!=view.query_rows or list(X.columns)!=view.given:raise PermissionError('Expert query boundary')
            COUNTS['expert_predict']+=1
            start=time.perf_counter();value=original_predict(self,X,*args,**kwargs);torch.cuda.synchronize()
            LOG.emit('expert_predict_end',stage=expert_scope['stage'],head_name=expert_scope['head'],seconds=time.perf_counter()-start,query_rows=len(X),
                     gpu_allocated_peak=torch.cuda.max_memory_allocated(),gpu_reserved_peak=torch.cuda.max_memory_reserved())
            return value
        adapter.SharedClassifier.fit=observed_fit
        adapter.SharedClassifier.predict_proba=observed_predict

    def expert(view,stage):
        start=time.perf_counter();values={};previous=None
        expected=(6279,2000) if stage=='expert_shadow' else (8279,621)
        if (len(view.fit_rows),len(view.query_rows))!=expected:raise AssertionError('Expert context shape changed')
        LOG.emit('expert_stage_start',stage=stage,fit_rows=expected[0],query_rows=expected[1],heads=len(view.heads))
        for head in view.heads:
            expert_scope.update(view=view,stage=stage,head=head)
            X,y=view.fit_input(head)
            if len(np.unique(y))!=len(view.options[head]):raise AssertionError('Fixture class coverage changed')
            del X,y
            LOG.emit('expert_head_start',stage=stage,head_name=head,classes=len(view.options[head]))
            estimator,p=adapter.predict_head(view,head)
            if estimator is None:raise AssertionError('Unexpected singleton/empty fixture head')
            if estimator.model_ is not adapter.SHARED_MODEL or estimator.model_kv_cache_ is not None:raise AssertionError('Shared weight/cache contract')
            if previous is not None and (previous.X_encoder_ is estimator.X_encoder_ or previous.ensemble_generator_ is estimator.ensemble_generator_):raise AssertionError('Head context objects shared')
            if p.shape!=(len(view.query_rows),len(view.options[head])) or not np.isfinite(p).all() or (p<0).any() or not np.allclose(p.sum(axis=1),1,rtol=0,atol=1e-6):raise AssertionError('Invalid expert probabilities')
            values[head]=p;previous=estimator
        del previous
        expert_scope.clear()
        stage_record=dict(stage=stage,heads=len(values),fit_rows=expected[0],query_rows=expected[1],seconds=time.perf_counter()-start)
        EXPERT_STAGES.append(stage_record);LOG.emit('expert_stage_end',**stage_record)
        return values

    predictor=FullPathPredictor(observer,expert,adapter,LOG) if MODE=='candidate' else None
    fixture=json.loads((HERE/'fixture-manifest.json').read_text())
    role_json=json.loads((HERE/'roles.json').read_text())
    plan=RolePlan(*(tuple(role_json[k]) for k in ('fit','selection','evaluation','external')))
    output_hashes={};output_counts={};decision=None
    for row in fixture['inputs']:
        name=row['instrument'];observer.instrument=name
        payload=json.loads((ROOT/row['path']).read_text(encoding='utf-8'))
        frame=pd.DataFrame(payload['data'],columns=payload['columns'],index=payload['index'],dtype=object)
        frame=frame.where(frame.notna(),np.nan)
        del payload
        schema,runtime_metadata=runtime_entry(ROOT/row['schema_path'])
        if runtime_metadata!=row['runtime_schema']:raise AssertionError('Generator/runtime normalized schema mismatch')
        LOG.emit('runtime_schema_verified',instrument=name,runtime_sha256=runtime_metadata['runtime_sha256'])
        given,heads,options=layout(schema)
        if list(frame.index)!=list(range(row['visible']+row['query'])):raise AssertionError('Original row positions lost')
        if not frame.iloc[row['visible']:][heads].isna().all().all():raise PermissionError('External query truth present')
        before=fingerprint(frame)
        LOG.emit('instrument_start',instrument=name,visible=row['visible'],query=row['query'])
        if MODE=='reference':
            output=observer(frame,schema,'reference',range(row['visible']))
        else:
            output=predictor.predict(frame,schema,plan if name=='unhcr' else None)
        restore(output,heads,range(row['visible'],len(frame)),options)
        if len(output)!=row['vectors']:raise AssertionError('Full canonical vector count')
        path=TEMP/MODE/(name+'.json')
        with path.open('x',encoding='utf-8') as stream:json.dump([list(map(float,v)) for v in output],stream,separators=(',',':'))
        output_hashes[name]=hashlib.sha256(path.read_bytes()).hexdigest();output_counts[name]=len(output)
        if MODE=='candidate' and name=='unhcr':
            engineering=predictor.engineering_active()
            restore(engineering,heads,range(row['visible'],len(frame)),options)
            inactive=predictor.render_final(0);fallback=predictor.render_final(.25,empty=True)
            if inactive is not predictor.last['raw'] or fallback is not predictor.last['raw']:raise AssertionError('Inactive/fallback identity changed')
            if not all(np.array_equal(np.asarray(a),np.asarray(b)) for a,b in zip(inactive,reference[name])):raise AssertionError('Inactive exact parity')
            for label,vectors in [('unhcr-engineering-alpha025',engineering),('unhcr-final-e041',inactive)]:
                path=TEMP/MODE/(label+'.json')
                with path.open('x',encoding='utf-8') as stream:json.dump([list(map(float,v)) for v in vectors],stream,separators=(',',':'))
                output_hashes[label]=hashlib.sha256(path.read_bytes()).hexdigest()
            decision={k:predictor.last[k] for k in ('alpha','accepted','lower')}
            LOG.emit('branch_parity',inactive_exact=True,empty_fallback_exact=True,engineering_alpha=.25,natural_decision=decision)
        if fingerprint(frame)!=before:raise AssertionError('Caller input mutated')
        LOG.emit('instrument_end',instrument=name,vectors=len(output))
    if sum(output_counts.values())!=189649:raise AssertionError('Wrong all3 count')
    if NETWORK!=dict(deliberate_blocks=1,package_attempts=0,subprocess_attempts=0):raise AssertionError('Runtime network attempt')
    if MODE=='candidate':
        if state_hash(adapter.SHARED_MODEL)!=before_state:raise AssertionError('Frozen model state changed')
        if COUNTS['checkpoint_loads']!=1 or COUNTS['expert_fit']!=426 or COUNTS['expert_predict']!=426:raise AssertionError('Full expert call counts')
        if adapter.COUNTS!=dict(adapter_injections=426,singleton=0,empty=0):raise AssertionError('Unexpected expert fallback/injection counts')
        if observer.counts['pipeline']!=4:raise AssertionError('Candidate pipeline count')
    elif observer.counts['pipeline']!=3:raise AssertionError('Reference pipeline count')
    return dict(output_hashes=output_hashes,output_counts=output_counts,natural_decision=decision,
                frozen_state_sha256=before_state,full_path_completed=True,actual_effect_evidence=False)


if __name__=='__main__':
    result=dict(outcome='LOCAL_FULL_PATH_FAIL',mode=MODE)
    code=1
    try:
        result.update(main());result['outcome']='REFERENCE_PASS' if MODE=='reference' else 'LOCAL_FULL_PATH_PASS';code=0
    except BaseException as exc:
        result.update(error=repr(exc),traceback=traceback.format_exc())
        if 'out of memory' in str(exc).lower():result['outcome']='LOCAL_RESOURCE_LIMIT'
        if isinstance(exc,ModuleNotFoundError) or 'CUDA unavailable' in str(exc):result['outcome']='BLOCKED_RESOURCE'
        LOG.emit('failure',error=repr(exc),outcome=result['outcome'])
    finally:
        result.update(elapsed_seconds=time.perf_counter()-START,counts=COUNTS,network=NETWORK,expert_stages=EXPERT_STAGES)
        if 'OBSERVER' in globals():result['e041']=OBSERVER.summary()
        if 'TORCH' in globals() and TORCH.cuda.is_initialized():
            result['gpu']=dict(allocated_peak=TORCH.cuda.max_memory_allocated(),reserved_peak=TORCH.cuda.max_memory_reserved(),device_capacity=TORCH.cuda.get_device_properties(0).total_memory)
        save('result.json',result);LOG.sink.close()
    sys.exit(code)
