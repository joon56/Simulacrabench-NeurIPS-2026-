"""Preregistered E053 ungated oracle; no learned policy or production changes."""
import argparse
from copy import deepcopy
import gzip
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import pickle
import sys
import time
from types import FunctionType

for variable in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ[variable] = '2'
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
import torch
from src.eval.logloss import floor_mix
from src.eval.recursive_candidates import cached_renderer, mask_query, component_oracle
from src.models import hh_cap, supervised_retrieval as retrieval
from src.models.hier_backoff import _layout
from scripts.screen_e050_e051 import ADULT_SOURCE, adapt_adult
from tests.e041_external import load_observed

OUTPUT = ROOT / 'docs/analysis/E053-outputs'
PROTOCOL = 'E053-uncensored-buckets-2600-800-800-800-v1'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def normalized(probability):
    p = np.asarray(probability, dtype=float)
    if not np.isfinite(p).all() or (p < 0).any() or not np.allclose(p.sum(1), 1, atol=2e-6, rtol=0):
        raise ValueError('Endpoint is not a finite nonnegative unit distribution')
    return p / p.sum(1, keepdims=True)


def split_frame(frame, schema):
    if len(frame) != 5000:
        raise ValueError('Registered sample has exactly 5000 rows')
    parts = {name: np.arange(lo, hi) for name, lo, hi in
             [('fit',0,2600),('oracle',2600,3400),('selection',3400,4200),('audit',4200,5000)]}
    return mask_query(frame, schema, np.arange(2600,5000)), parts


def capture_layer(frame, schema, model_dists):
    """Run original layer once; retain its fitted state for dormant query work."""
    records, items, options = _layout(frame, schema)
    predicted = [n for n in items if records[n]['class'] == 'PREDICT']
    hidden = frame[predicted].isna().any(axis=1).to_numpy()
    visible, query = np.flatnonzero(~hidden), np.flatnonzero(hidden)
    if len(visible) < 500 or not len(query) or not frame.iloc[query][predicted].isna().all().all():
        raise ValueError('Require at least 500 fit rows and whole masked query blocks')
    state = {'query_donor_checks': 0, 'query_donor_records': []}
    namespace = retrieval.supervised_layer.__globals__.copy()
    namespace['LAST_DIAGNOSTICS'] = {}

    def saved(name, function):
        def call(*args, **kwargs):
            if name in state:
                raise AssertionError(f'Unexpected repeated fit: {name}')
            value = function(*args, **kwargs)
            state[name] = deepcopy(value)
            return value
        return call

    def donor_call(function, *args, **kwargs):
        requested, bank = np.asarray(args[2]), np.asarray(args[3])
        outer = np.isin(requested, query)
        if outer.any():
            if not outer.all() or not np.isin(bank, visible).all():
                raise AssertionError('Outer query donor pool contains hidden labels')
            state['query_donor_checks'] += 1
        result = function(*args, **kwargs)
        if outer.any():
            donors = result if isinstance(result, np.ndarray) else np.concatenate([p for p, _ in result])
            if not np.isin(donors, visible).all():
                raise AssertionError('Returned donor is not a fit row')
            state['query_donor_records'].append({'function':function.__name__,
                'query':requested.copy(),'bank':bank.copy(),'result':deepcopy(result)})
        return result

    namespace['_sig_data_all'] = saved('signature', namespace['_sig_data_all'])
    namespace['estimate_weights'] = saved('weights', namespace['estimate_weights'])
    namespace['fit_sections'] = saved('sections', namespace['fit_sections'])
    topk = namespace['_topk_excl']
    namespace['_topk_excl'] = lambda *a, **kw: donor_call(topk, *a, **kw)
    replace_namespace = retrieval._replace_evidence.__globals__.copy()
    candidates = replace_namespace['candidate_indices']
    replace_namespace['candidate_indices'] = lambda *a, **kw: donor_call(candidates, *a, **kw)
    replace = FunctionType(retrieval._replace_evidence.__code__, replace_namespace,
                           argdefs=retrieval._replace_evidence.__defaults__)
    namespace['_replace_evidence'] = replace
    layer = FunctionType(retrieval.supervised_layer.__code__, namespace,
                         argdefs=retrieval.supervised_layer.__defaults__)
    legacy, lambdas = layer(frame, schema, model_dists)
    evidence = legacy
    dormant = False
    if not legacy and not lambdas and 'sections' in state:
        codes, _ = state['signature']
        initial, _ = state['weights']
        learned, active, _ = state['sections']
        post = namespace['_topk_excl'](codes, initial, query, visible)
        values = namespace['_evidence'](frame, items, records, options, post, query)
        values = replace(values, frame, records, items, options, codes, query,
                         visible, initial, predicted, retrieval._groups(predicted), learned, active)
        concentration = namespace['_max_q'](post) >= namespace['CONC_SPLIT']
        evidence = {int(row): ({n: values[n][i] for n in values}, bool(concentration[i]))
                    for i, row in enumerate(query)}
        dormant = True
    return {'legacy_evidence': legacy, 'evidence': evidence, 'lambdas': lambdas,
            'materialized_dormant': dormant, 'query_donor_checks': state['query_donor_checks'],
            'fitted_state': state, 'diagnostics': deepcopy(namespace['LAST_DIAGNOSTICS'])}


def build_library(frame, schema):
    records, items, options = _layout(frame, schema)
    predicted = [n for n in items if records[n]['class'] == 'PREDICT']
    if any(records[n].get('gate') for n in predicted):
        raise ValueError('E053 separable oracle is restricted to ungated schemas')
    query = np.flatnonzero(frame[predicted].isna().any(axis=1))
    captured = {}
    def layer(f, s, model):
        if captured:
            raise AssertionError('A second layer fit is forbidden')
        captured.update(capture_layer(f, s, model))
        captured['base'] = {n: np.array(model[n][query], copy=True) for n in predicted}
        return captured['legacy_evidence'], captured['lambdas']
    render = cached_renderer()
    raw = render(frame, schema, layer_fn=layer, configs=hh_cap.CONFIGS)
    parity = render(frame, schema, layer_fn=lambda *args:(captured['legacy_evidence'],captured['lambdas']),
                    configs=hh_cap.CONFIGS)
    if len(raw) != len(query)*len(predicted) or any(not np.array_equal(a,b) for a,b in zip(raw,parity)):
        raise AssertionError('Frozen original renderer endpoint mismatch')
    identity = {n: np.stack(raw[j::len(predicted)]) for j,n in enumerate(predicted)}
    evidence = {n: np.zeros_like(identity[n]) for n in predicted}
    available = {n: np.zeros(len(query), dtype=bool) for n in predicted}
    concentration = np.zeros(len(query), dtype=bool)
    for i,row in enumerate(query):
        entry = captured['evidence'].get(int(row))
        if entry is None:
            continue
        values, concentration[i] = entry
        for n,p in values.items():
            if n in evidence and np.asarray(p).sum() > 0:
                evidence[n][i] = p
                available[n][i] = True
    reconstruction = 0.
    for n in predicted:
        normalized(captured['base'][n]); normalized(identity[n])
        mask = available[n]
        if mask.any():
            normalized(evidence[n][mask])
        old = np.array(captured['base'][n],copy=True)
        if captured['legacy_evidence']:
            shares = np.asarray(captured['lambdas'].get(n,(0.,0.)))[concentration.astype(int)]
            if np.any((shares<0)|(shares>.98)):
                raise AssertionError('Legacy lambda outside registered interval')
            old[mask] = (1-shares[mask,None])*old[mask] + shares[mask,None]*evidence[n][mask]
        reconstruction = max(reconstruction,float(np.max(np.abs(old-identity[n]))))
    if reconstruction > 1e-12:
        raise AssertionError('Original lambda reconstruction mismatch')
    return {'base':captured.pop('base'),'identity':identity,'evidence':evidence,'available':available,
            'concentration':concentration,'query':query,'predicted':predicted,'options':options,
            'legacy_returned':bool(captured['legacy_evidence']),'capture':captured,
            'raw_parity_max_abs':0.,'reconstruction_max_abs':reconstruction}


def optimize_bucket(base_truth, evidence_truth, classes):
    a = .001+(1-classes*.001)*np.asarray(base_truth,dtype=float)
    d = (1-classes*.001)*(np.asarray(evidence_truth,dtype=float)-base_truth)
    if not len(a) or np.any(a<=0) or np.any(a+.98*d<=0):
        raise ValueError('Invalid nonempty scalar objective')
    def derivative(x): return float(np.mean(d/(a+x*d)))
    if derivative(0.) <= 0:
        weight = 0.
    elif derivative(.98) >= 0:
        weight = .98
    else:
        lo,hi = 0.,.98
        for _ in range(80):
            mid=(lo+hi)/2
            if derivative(mid)>0: lo=mid
            else: hi=mid
        weight=(lo+hi)/2
    score=float(np.log(a+weight*d).mean())
    slope=derivative(weight)
    gap=max(0.,slope*(0.-weight),slope*(.98-weight))
    return {'lambda':weight,'log_score':score,'log_upper':score+gap,'tangent_gap':gap}


def score_family(library, labels, selected, returned_only):
    names=list(library['identity'])
    total_log,total_upper,base_log,cells,changed=0.,0.,0.,0,0
    details=[]
    for n in names:
        baseline=library['identity'][n][selected]
        truth=labels[n]
        old_logs=np.log(floor_mix(baseline)[np.arange(len(truth)),truth])
        gains,upper=old_logs.copy(),old_logs.copy()
        valid=library['available'][n][selected].copy()
        if returned_only and not library['legacy_returned']: valid[:]=False
        for bucket in (0,1):
            mask=valid & (library['concentration'][selected]==bucket)
            if not mask.any(): continue
            b=normalized(library['base'][n][selected][mask])
            e=normalized(library['evidence'][n][selected][mask])
            y=truth[mask]; rows=np.arange(len(y))
            fit=optimize_bucket(b[rows,y],e[rows,y],b.shape[1])
            candidate=(1-fit['lambda'])*b+fit['lambda']*e
            candidate_logs=np.log(floor_mix(candidate)[rows,y])
            identity_log=float(old_logs[mask].mean())
            use=fit['log_score'] > identity_log
            if use:
                gains[mask]=candidate_logs
                changed+=int(np.any(candidate!=baseline[mask],axis=1).sum())
            upper[mask]=max(identity_log,fit['log_upper'])
            details.append({'item':n,'bucket':bucket,'rows':int(mask.sum()),'identity_log':identity_log,
                            'selected':'optimized' if use else 'identity',**fit})
        total_log+=float(gains.sum()); total_upper+=float(upper.sum())
        base_log+=float(old_logs.sum()); cells+=len(truth)
    u=float(np.mean([np.log(library['identity'][n].shape[1]) for n in names]))
    delta=(total_log-base_log)/cells/u
    bound=(total_upper-base_log)/cells/u
    gap=(total_upper-total_log)/cells
    if gap < -1e-12 or gap>1e-9:
        raise AssertionError(f'Oracle certificate gap {gap}')
    return {'delta_skill':delta,'delta_skill_over_3':delta/3,'upper_skill_over_3':bound/3,
            'log_optimality_gap':max(0.,gap),'baseline_skill':1+base_log/cells/u,
            'oracle_skill':1+total_log/cells/u,'cells':cells,'changed_vectors':changed,'buckets':details}


def old_five_arms(library, labels, selected):
    arms={'identity':{n:p[selected] for n,p in library['identity'].items()}}
    for name in ('zero','half','toward_one','one'):
        heads={}
        for n,p in library['base'].items():
            output=np.array(library['identity'][n],copy=True)
            if library['legacy_returned']:
                pair=np.asarray(library['capture']['lambdas'].get(n,(0.,0.)))
                values={'zero':pair*0,'half':pair*.5,'toward_one':pair+.5*(1-pair),'one':np.ones(2)}[name]
                weight=values[library['concentration'].astype(int)]
                mask=library['available'][n]
                output[mask]=(1-weight[mask,None])*p[mask]+weight[mask,None]*library['evidence'][n][mask]
            heads[n]=output[selected]
        arms[name]=heads
    return component_oracle(arms,labels,[[n] for n in library['predicted']])


def prepare(seed):
    frame,source_ids,counts=load_observed(ADULT_SOURCE,seed,rows=5000)
    frame,schema=adapt_adult(frame)
    masked,partitions=split_frame(frame,schema)
    prior={}
    prior_hashes={}
    source_hash=digest(ADULT_SOURCE.read_bytes())
    if len(np.unique(source_ids)) != len(source_ids):
        raise AssertionError('Source identities must be unique within a split')
    for prior_seed in (51,52):
        path=ROOT/f'docs/analysis/E050-outputs/adult-seed{prior_seed}-manifest.json'
        data=json.loads(path.read_text(encoding='utf-8'))
        if data['source_file_sha256'] != source_hash:
            raise AssertionError('Prior source provenance differs')
        prior_hashes[path.relative_to(ROOT).as_posix()]=digest(path.read_bytes())
        ids=np.asarray(data['source_ids'])
        prior[f'E050-seed{prior_seed}']={n:ids[lo:hi] for n,(lo,hi) in data['partitions'].items()}
    path=ROOT/'docs/analysis/A011-outputs/adult-manifest.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    if data['source_file_sha256'] != source_hash:
        raise AssertionError('A011 source provenance differs')
    prior_hashes[path.relative_to(ROOT).as_posix()]=digest(path.read_bytes())
    ids=np.asarray(data['source_ids'])
    prior['A011-seed53']={n:ids[positions] for n,positions in data['partition_rows'].items()}
    _,other_ids,_=load_observed(ADULT_SOURCE,55 if seed==54 else 54,rows=5000)
    prior['other_E053_seed']={n:other_ids[rows] for n,rows in partitions.items()}
    overlaps={n:{old:{role:np.intersect1d(source_ids[rows],ids).tolist() for role,ids in groups.items()}
                  for old,groups in prior.items()} for n,rows in partitions.items()}
    return frame,schema,masked,partitions,{'source_ids':source_ids.tolist(),'counts':counts,
            'known_role_intersections':overlaps,'prior_manifest_sha256':prior_hashes,
            'exposure_inventory_is_exhaustive':False}


def run(seed, output_dir=OUTPUT):
    if seed not in (54,55): raise ValueError('Registered seeds are 54 and 55')
    out=Path(output_dir); stem=f'adult-seed{seed}'
    if any(out.glob(stem+'-*')):
        raise FileExistsError('Refuse existing E053 artifacts before loading/fitting')
    torch.set_num_threads(2)
    frame,schema,masked,partitions,metadata=prepare(seed)
    paths=sorted((ROOT/'src').rglob('*.py'))+[Path(__file__),ROOT/'scripts/screen_e050_e051.py',
        ROOT/'tests/e041_external.py', ROOT/'tests/test_e053_oracle.py']
    registration=(ROOT/'docs/experiments/E053-uncensored-bucket-replay.md').read_bytes()
    hashes={p.relative_to(ROOT).as_posix():digest(p.read_bytes()) for p in paths}
    manifest={'protocol':PROTOCOL,'seed':seed,'source_hashes':hashes,
              'registration_sha256':digest(registration),'registration_archive':f'{stem}-registration.md',
              'source_file_sha256':digest(ADULT_SOURCE.read_bytes()),
              'frame_sha256':digest(pickle.dumps((schema,frame),protocol=5)),
              'masked_frame_sha256':digest(pickle.dumps((schema,masked),protocol=5)),
              'partition_rows':{n:p.tolist() for n,p in partitions.items()},
              'versions':{n:version(n) for n in ('numpy','pandas','torch','scipy','scikit-learn')},**metadata}
    print(f'{stem}: fitting frozen generic E041 library',flush=True)
    start=time.perf_counter(); library=build_library(masked,schema)
    manifest['fit_and_capture_seconds']=time.perf_counter()-start
    raw=pickle.dumps(library,protocol=5); packed=gzip.compress(raw,mtime=0)
    out.mkdir(parents=True,exist_ok=True)
    with (out/f'{stem}-registration.md').open('xb') as f: f.write(registration)
    with (out/f'{stem}-capture.pkl.gz').open('xb') as f: f.write(packed)
    dense={f'{group}/{n}':v for group in ('base','identity','evidence','available')
           for n,v in library[group].items()}
    dense.update(query=library['query'],concentration=library['concentration'])
    with (out/f'{stem}-arrays.npz').open('xb') as f: np.savez_compressed(f,**dense)
    manifest.update(capture_sha256=digest(packed),raw_capture_sha256=digest(raw),
                    arrays_sha256=digest((out/f'{stem}-arrays.npz').read_bytes()),
                    legacy_returned=library['legacy_returned'],
                    materialized_dormant=library['capture']['materialized_dormant'])
    with (out/f'{stem}-manifest.json').open('x',encoding='utf-8') as f: json.dump(manifest,f,indent=2)
    # Oracle labels are mapped only after immutable captures and provenance exist.
    rows=partitions['oracle']; selected=np.arange(800)
    labels={n:frame.iloc[rows][n].map({v:i for i,v in enumerate(library['options'][n])}).to_numpy(dtype=int)
            for n in library['predicted']}
    result={'protocol':PROTOCOL,'seed':seed,'scored_partition':'oracle','selection_or_audit_evaluated':False,
            'capture_sha256':manifest['capture_sha256'],
            'original_five_arm':old_five_arms(library,labels,selected),
            'returned_bucket':score_family(library,labels,selected,True),
            'uncensored_bucket':score_family(library,labels,selected,False)}
    primary=result['uncensored_bucket']
    result['gate']='PASS' if primary['delta_skill_over_3']>.005 else (
                   'STOP' if primary['upper_skill_over_3']<=.005 else 'NUMERICALLY_UNRESOLVED')
    with (out/f'{stem}-oracle.json').open('x',encoding='utf-8') as f:
        json.dump(result,f,indent=2,allow_nan=False)
    print(json.dumps({'seed':seed,'gate':result['gate'],'primary':primary,
                      'legacy_returned':library['legacy_returned']}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed',type=int,choices=(54,55),required=True)
    parser.add_argument('--output-dir',type=Path,default=OUTPUT)
    args=parser.parse_args()
    run(args.seed,args.output_dir)
