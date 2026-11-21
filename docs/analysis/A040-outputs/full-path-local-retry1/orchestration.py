"""Research composition; models injected, no model imports or hidden-data access."""
from dataclasses import dataclass
import hashlib
import json

import numpy as np
import pandas as pd


def layout(schema):
    given = [n for n,r in schema['items'].items() if r['class']=='GIVEN']
    heads = [n for n,r in schema['items'].items() if r['class']=='PREDICT']
    options = {n:list(r['values'])+([schema['gated_value']] if r.get('gate') else [])
               for n,r in schema['items'].items() if r['class'] in ('GIVEN','PREDICT')}
    return given,heads,options


def fingerprint(frame):
    h=hashlib.sha256(json.dumps(list(frame.columns)).encode())
    h.update(pd.util.hash_pandas_object(frame,index=True).to_numpy().tobytes())
    return h.hexdigest()


@dataclass(frozen=True)
class RolePlan:
    fit: tuple
    selection: tuple
    evaluation: tuple
    external: tuple


class FitView:
    """Only a masked frame and entitled fit/query rows reach the expert."""
    def __init__(self, frame, schema, fit_rows, query_rows):
        self.shadow=frame
        self.fit_rows=sorted(fit_rows)
        self.query_rows=sorted(query_rows)
        self.given,self.heads,self.options=layout(schema)
        if set(self.fit_rows)&set(self.query_rows):
            raise PermissionError('Fit/query overlap')
        outside=sorted(set(frame.index)-set(self.fit_rows))
        if not frame.loc[outside,self.heads].isna().all().all():
            raise PermissionError('Non-fit target reached expert view')
        if not frame.loc[self.fit_rows,self.given+self.heads].notna().all().all():
            raise ValueError('Incomplete fit role')

    def fit_input(self, head):
        X=self.shadow.loc[self.fit_rows,self.given].copy().astype(object)
        y=self.shadow.loc[self.fit_rows,head].map({v:i for i,v in enumerate(self.options[head])})
        if y.isna().any():
            raise ValueError('Invalid fit label')
        if len(X) and not any(X[n].nunique(dropna=False)>1 for n in self.given):
            raise ValueError('Zero usable features')
        return X,y.to_numpy(dtype=int)


class SealedRoles:
    def __init__(self, frame, schema, plan):
        given,self.heads,self.options=layout(schema)
        all_rows=plan.fit+plan.selection+plan.evaluation+plan.external
        if len(all_rows)!=len(set(all_rows)) or set(all_rows)!=set(frame.index):
            raise ValueError('Roles must partition original row positions')
        self.plan=plan
        self._selection=self._encode(frame,sorted(plan.selection))
        self._evaluation=self._encode(frame,sorted(plan.evaluation))
        self.shadow=frame.copy(deep=True)
        self.shadow.loc[sorted(plan.selection+plan.evaluation+plan.external),self.heads]=np.nan
        self._phase='fitting'

    def _encode(self,frame,rows):
        result={}
        for h in self.heads:
            y=frame.loc[rows,h].map({v:i for i,v in enumerate(self.options[h])})
            if y.isna().any():raise ValueError('Invalid sealed fake label')
            result[h]=y.to_numpy(dtype=int);result[h].setflags(write=False)
        return result

    def shadow_complete(self):
        if self._phase!='fitting':raise PermissionError('Shadow phase reused')
        self._phase='ready'

    def selection(self):
        if self._phase!='ready':raise PermissionError('Selection before shadow complete')
        self._phase='selection';return self._selection

    def freeze(self,alpha):
        if self._phase!='selection' or alpha not in (0,.25,.5):raise PermissionError('Invalid freeze')
        self._phase='frozen'

    def evaluation(self):
        if self._phase!='frozen':raise PermissionError('Evaluation before freeze')
        self._phase='evaluated';return self._evaluation


def restore(vectors,heads,rows,options):
    if len(vectors)!=len(heads)*len(rows):raise ValueError('Wrong canonical vector count')
    result={}
    for j,h in enumerate(heads):
        p=np.asarray(vectors[j::len(heads)],dtype=np.float64)
        if p.shape!=(len(rows),len(options[h])) or not np.isfinite(p).all() or (p<0).any() or (p.sum(axis=1)<=0).any():
            raise ValueError('Invalid canonical probabilities for '+h)
        result[h]=p
    return result


def subset(maps,all_rows,rows):
    index={r:i for i,r in enumerate(all_rows)}
    ix=[index[r] for r in sorted(rows)]
    return {h:p[ix] for h,p in maps.items()}


def flatten(maps,heads):
    n=len(maps[heads[0]])
    return [maps[h][i].tolist() for i in range(n) for h in heads]


class FullPathPredictor:
    def __init__(self,base_call,expert_call,math,log):
        self.base_call,self.expert_call,self.math,self.log=base_call,expert_call,math,log
        self.last=None

    def predict(self,frame,schema,plan=None):
        given,heads,options=layout(schema)
        if 's3_11_intent_return_12m_lbl' not in schema['items']:
            visible=tuple(frame.index[frame[heads].notna().all(axis=1)])
            return self.base_call(frame,schema,'control',visible)
        if plan is None:raise ValueError('UNHCR requires frozen role mapping')
        before=fingerprint(frame)
        sealed=SealedRoles(frame,schema,plan)
        shadow_query=sorted(plan.selection+plan.evaluation+plan.external)
        score_query=sorted(plan.selection+plan.evaluation)
        shadow_raw=self.base_call(sealed.shadow,schema,'unhcr_shadow',plan.fit)
        p_all=restore(shadow_raw,heads,shadow_query,options)
        p_score=subset(p_all,shadow_query,score_query)
        view=FitView(sealed.shadow,schema,plan.fit,score_query)
        q_score=self.expert_call(view,'expert_shadow')
        sealed.shadow_complete()
        alpha=self.math.select_alpha(subset(p_score,score_query,plan.selection),
                                     subset(q_score,score_query,plan.selection),sealed.selection())
        sealed.freeze(alpha)
        self.log.emit('alpha_frozen',alpha=alpha)
        accepted,lower=self.math.independent_check(subset(p_score,score_query,plan.evaluation),
                            subset(q_score,score_query,plan.evaluation),sealed.evaluation(),alpha)
        self.log.emit('natural_decision',alpha=alpha,accepted=bool(accepted),lower=lower,efficacy_evidence=False)
        del p_all,p_score,q_score,shadow_raw,view,sealed
        visible=tuple(sorted(plan.fit+plan.selection+plan.evaluation))
        final_raw=self.base_call(frame,schema,'unhcr_final',visible)
        final_maps=restore(final_raw,heads,sorted(plan.external),options)
        final_view=FitView(frame,schema,visible,plan.external)
        self.last=dict(raw=final_raw,maps=final_maps,q=None,view=final_view,
                       heads=heads,alpha=alpha,accepted=bool(accepted),lower=lower)
        if accepted:
            self.last['q']=self.expert_call(final_view,'expert_final')
            output=self.render_final(alpha)
        else:
            output=final_raw
            self.log.emit('natural_final_expert_skipped',alpha=alpha)
        if fingerprint(frame)!=before:raise AssertionError('Input frame mutated')
        return output

    def render_final(self,alpha,empty=False):
        if alpha==0 or empty:return self.last['raw']
        if self.last['q'] is None:raise ValueError('Active rendering needs final expert')
        maps={h:self.math.mix(self.last['maps'][h],self.last['q'][h],alpha) for h in self.last['heads']}
        return flatten(maps,self.last['heads'])

    def engineering_active(self):
        if self.last is None:raise ValueError('No final baseline')
        if self.last['q'] is None:
            self.log.emit('engineering_forced_final_expert',natural_accepted=self.last['accepted'])
            self.last['q']=self.expert_call(self.last['view'],'expert_final')
        self.log.emit('engineering_render',alpha=.25,natural_alpha=self.last['alpha'],natural_accepted=self.last['accepted'])
        return self.render_final(.25)
