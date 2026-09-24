"""Verify frozen E053 arrays and oracle arithmetic; no fitting or audit scoring."""
import gzip, hashlib, json, pickle, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import numpy as np
from scripts import screen_e053 as s
out=ROOT/'docs/analysis/E053-outputs'
reports=[]
registrations=[]
for seed in (54,55):
 stem=f'adult-seed{seed}'
 manifest=json.loads((out/f'{stem}-manifest.json').read_text())
 saved=json.loads((out/f'{stem}-oracle.json').read_text())
 packed=(out/f'{stem}-capture.pkl.gz').read_bytes()
 raw=gzip.decompress(packed)
 assert s.digest(packed)==manifest['capture_sha256']
 assert s.digest(raw)==manifest['raw_capture_sha256']
 lib=pickle.loads(raw)
 arrays=np.load(out/f'{stem}-arrays.npz')
 for group in ('base','identity','evidence','available'):
  for name,value in lib[group].items():
   assert np.array_equal(value,arrays[f'{group}/{name}'])
 assert np.array_equal(lib['query'],np.arange(2600,5000))
 assert np.array_equal(lib['concentration'],arrays['concentration'])
 frame,schema,masked,parts,meta=s.prepare(seed)
 assert s.digest(pickle.dumps((schema,frame),protocol=5))==manifest['frame_sha256']
 assert s.digest(pickle.dumps((schema,masked),protocol=5))==manifest['masked_frame_sha256']
 assert meta['known_role_intersections']==manifest['known_role_intersections']
 labels={n:frame.iloc[parts['oracle']][n].map({v:i for i,v in enumerate(lib['options'][n])}).to_numpy(dtype=int) for n in lib['predicted']}
 selected=np.arange(800)
 recomputed={'original_five_arm':s.old_five_arms(lib,labels,selected),
  'returned_bucket':s.score_family(lib,labels,selected,True),
  'uncensored_bucket':s.score_family(lib,labels,selected,False)}
 assert recomputed['returned_bucket']==recomputed['uncensored_bucket']
 for family,value in recomputed.items():
  assert value==saved[family],family
 # Independently pool frozen official probabilities at archived chosen lambdas.
 old_logs=[]; new_logs=[]
 for name in lib['predicted']:
  y=labels[name]; rows=np.arange(800)
  baseline=lib['identity'][name][:800]
  candidate=baseline.copy()
  for item in saved['uncensored_bucket']['buckets']:
   if item['item']!=name or item['selected']!='optimized': continue
   mask=lib['available'][name][:800] & (lib['concentration'][:800]==item['bucket'])
   b=lib['base'][name][:800][mask].astype(float); b/=b.sum(1,keepdims=True)
   e=lib['evidence'][name][:800][mask].astype(float); e/=e.sum(1,keepdims=True)
   candidate[mask]=(1-item['lambda'])*b+item['lambda']*e
  def logs(p):
   p=p/p.sum(1,keepdims=True)
   return np.log(.001+(1-p.shape[1]*.001)*p[rows,y])
  old_logs.append(logs(baseline));new_logs.append(logs(candidate))
 u=np.mean([np.log(len(lib['options'][n])) for n in lib['predicted']])
 independent_delta=(np.stack(new_logs).mean()-np.stack(old_logs).mean())/u/3
 assert abs(independent_delta-saved['uncensored_bucket']['delta_skill_over_3'])<1e-12
 for record in lib['capture']['fitted_state']['query_donor_records']:
  result=record['result']
  donors=result if isinstance(result,np.ndarray) else np.concatenate([v[0] for v in result])
  assert np.isin(donors,np.arange(2600)).all()
  assert np.isin(record['bank'],np.arange(2600)).all()
 assert saved['scored_partition']=='oracle' and not saved['selection_or_audit_evaluated']
 registrations.append(manifest['registration_sha256'])
 reports.append({'seed':seed,'gate':saved['gate'],
  'active_sections':lib['capture']['diagnostics'].get('active'),
  'section_diagnostics':lib['capture']['diagnostics'].get('sections'),
  'legacy_returned':lib['legacy_returned'],'dormant_materialized':lib['capture']['materialized_dormant'],
  'evidence_available_all_queries':{n:int(v.sum()) for n,v in lib['available'].items()},
  'query_bucket_counts':np.bincount(lib['concentration'].astype(int),minlength=2).tolist(),
  'oracle_bucket_counts':np.bincount(lib['concentration'][:800].astype(int),minlength=2).tolist(),
  'reconstruction_max_abs':lib['reconstruction_max_abs'],
  'independent_delta_skill_over_3':independent_delta,
  'returned_equals_uncensored':True,'donor_record_count':len(lib['capture']['fitted_state']['query_donor_records'])})
assert registrations[0]==registrations[1]
print(json.dumps({'frozen_artifact_checks':'PASS','reports':reports,'model_fits':0,
 'scored_partition':'oracle only, existing frozen outputs','selection_audit_scored':False},indent=2))
