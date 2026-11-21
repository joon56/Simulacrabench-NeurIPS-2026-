"""In-memory E041 observation; delegates unchanged arguments and returns."""
from collections import defaultdict
from functools import wraps
import time

import numpy as np

from orchestration import fingerprint, layout, restore


class E041Observer:
    def __init__(self,module,log,reference=None):
        self.module,self.log,self.reference=module,log,reference
        self.instrument=None
        self.stage=None
        self.allowed=set()
        self.heads=[]
        self.counts=defaultdict(int)
        self.seconds=defaultdict(float)
        self.failures=defaultdict(int)
        self.stage_records=[]
        self.boundary_checks=0
        names=['select_ladder','tune_and_train','_train','_train_on','minimize',
               'fit_sections','build_ladder','_best_lambda','_complete_rows','_targets',
               '_given_matrix','conditional_agreement','supervised_layer',
               'hh_sharp_layer','_evidence','_topk_excl','_SHARP_PREDICT']
        for name in names:self._wrap(name)

    def check_frame(self,frame,fit_only=False):
        if fit_only:
            if not set(frame.index).issubset(self.allowed):
                raise PermissionError('Held-role rows reached E041 fitting helper')
        else:
            outside=[i for i in frame.index if i not in self.allowed]
            available=[h for h in self.heads if h in frame.columns]
            if outside and available and not frame.loc[outside,available].isna().all().all():
                raise PermissionError('Unmasked held-role labels reached E041 helper')
        self.boundary_checks+=1

    def _wrap(self,name):
        original=getattr(self.module,name)
        frame_functions={'select_ladder','tune_and_train','_complete_rows','_given_matrix',
                         'conditional_agreement','supervised_layer','hh_sharp_layer','_evidence','_SHARP_PREDICT'}
        verbose={'select_ladder','tune_and_train','_train','_train_on','minimize','fit_sections',
                 'conditional_agreement','supervised_layer','hh_sharp_layer'}
        @wraps(original)
        def observed(*args,**kwargs):
            key=self.instrument+'/'+self.stage+'/'+name
            self.counts[key]+=1
            if name in frame_functions:self.check_frame(args[0])
            if name in ('build_ladder','_targets'):self.check_frame(args[0],fit_only=True)
            if name=='fit_sections':
                labels=args[1]
                outside=sorted(set(range(len(labels)))-self.allowed)
                if outside and not np.all(labels[outside]==-1):raise PermissionError('Held truth reached metric fit')
                for positions in args[2:5]:
                    if not set(map(int,positions)).issubset(self.allowed):raise PermissionError('Metric role outside F')
                self.boundary_checks+=1
            if name=='_best_lambda' and len(args[0])<30:
                raise AssertionError('Legacy minimum30 changed')
            info={}
            if name=='_train_on':
                info['device']=str(args[0]);self.counts['neural_device_'+str(args[0])]+=1
            if name=='_train':info['fit_rows']=int(args[0].shape[0])
            if name in verbose:self.log.emit('e041_call_start',instrument=self.instrument,stage=self.stage,function=name,**info)
            start=time.perf_counter()
            try:
                value=original(*args,**kwargs)
                if name=='_complete_rows':self.check_frame(value,fit_only=True)
                if name in ('supervised_layer','hh_sharp_layer'):
                    self.counts[key+'/empty_evidence']+=int(not bool(value[0]))
                return value
            except BaseException as exc:
                self.failures[key]+=1
                self.log.emit('e041_call_error',instrument=self.instrument,stage=self.stage,function=name,error=repr(exc),**info)
                raise
            finally:
                elapsed=time.perf_counter()-start
                self.seconds[key]+=elapsed
                if name in verbose:self.log.emit('e041_call_end',instrument=self.instrument,stage=self.stage,function=name,seconds=elapsed,**info)
        setattr(self.module,name,observed)

    def __call__(self,frame,schema,stage,fit_rows):
        self.stage=stage
        self.allowed=set(map(int,fit_rows))
        _,self.heads,options=layout(schema)
        self.check_frame(frame)
        visible=set(frame.index[frame[self.heads].notna().all(axis=1)])
        if visible!=self.allowed:raise PermissionError('E041 complete-row role mismatch')
        if self.instrument=='unhcr' and len(visible)<500:raise AssertionError('Tiny supervised fallback forbidden')
        query=sorted(set(frame.index)-visible)
        before=fingerprint(frame)
        start=time.perf_counter()
        self.counts['pipeline']+=1
        self.log.emit('pipeline_start',instrument=self.instrument,stage=stage,fit_rows=len(visible),query_rows=len(query))
        output=self.module.predict(frame,schema)
        restore(output,self.heads,query,options)
        if fingerprint(frame)!=before:raise AssertionError('E041 input mutated')
        parity=None
        if self.reference is not None and stage!='unhcr_shadow':
            reference=self.reference[self.instrument]
            parity=len(reference)==len(output) and all(np.array_equal(np.asarray(a),np.asarray(b)) for a,b in zip(output,reference))
            if not parity:raise AssertionError('Exact E041 reference parity failed: '+self.instrument+'/'+stage)
        elapsed=time.perf_counter()-start
        record=dict(instrument=self.instrument,stage=stage,fit_rows=len(visible),query_rows=len(query),vectors=len(output),seconds=elapsed,reference_exact=parity)
        self.stage_records.append(record)
        self.log.emit('pipeline_end',**record)
        return output

    def summary(self):
        return dict(counts=dict(self.counts),inclusive_seconds=dict(self.seconds),failed_attempts=dict(self.failures),
                    stages=self.stage_records,boundary_checks=self.boundary_checks,
                    note='Nested timings overlap. Whole pipeline includes recursive rendering and all observer work.')
