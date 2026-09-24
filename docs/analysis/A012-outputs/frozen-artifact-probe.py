"""Frozen A012 qualification checks. No model imports, fits or new scoring."""
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'submissions/phase2-E041-preparation'
def read(path): return json.loads(path.read_text())
manifest=read(folder/'verification.json')
supplement=read(folder/'supplemental-verification.json')
for relative,expected in supplement['artifacts_sha256'].items():
 assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()==expected,relative
names=('unicef','world_bank','unhcr')
assert set(manifest['instruments'])==set(names)==set(supplement['instruments'])
reports=[];seconds=0.; oldskills=[];newskills=[]
for name in names:
 prefix=ROOT/'docs/analysis/A012-outputs'
 old=read(prefix/f'E025-{name}-source.json'); new=read(prefix/f'E041-{name}-source.json')
 official=read(prefix/f'E041-{name}-official.json'); vectors=read(prefix/f'E041-{name}-official-predictions.json')
 assert vectors==new['vectors']
 assert old['phase']==new['phase']==official['phase']==2 and official['status']=='PASS'
 assert old['visible_roles']==new['visible_roles']==['TRAIN','DEV']
 assert old['hidden_role']==new['hidden_role']=='TEST'
 assert old['n_cells']==new['n_cells']==official['n_cells']==len(vectors)
 assert len(old['vectors'])==len(vectors)
 for key in ('frame_sha256','schema_sha256','data_sha256'): assert old[key]==new[key]
 assert new['skill']==official['skill'] and new['log_score']==official['log_score']
 row=manifest['instruments'][name]; extra=supplement['instruments'][name]
 delta=new['skill']-old['skill']
 assert delta==row['e041_minus_e025']==extra['delta_skill']
 assert abs(delta)<=.002 and extra['registered_abs_0p002_gate']
 maximum=max(abs(a-b) for before,after in zip(old['vectors'],vectors) for a,b in zip(before,after))
 assert all(len(a)==len(b) for a,b in zip(old['vectors'],vectors))
 assert maximum==extra['e025_e041_raw_max_abs']
 assert official['seconds']==row['e041_official_seconds']
 seconds+=official['seconds'];oldskills.append(old['skill']);newskills.append(new['skill'])
 reports.append({'instrument':name,'cells':len(vectors),'delta_skill':delta,'baseline_raw_max_abs':maximum,'source_official_exact':True})
assert seconds==manifest['official_seconds_sum']==supplement['official_seconds_sum_recomputed']
assert seconds<3600 and supplement['registered_absolute_gate_all3']
with zipfile.ZipFile(ROOT/'submissions/2026-09-19-E041.zip') as archive:
 assert archive.namelist()==['main.py']
 assert archive.read('main.py')==(ROOT/'submissions/2026-09-19-E041/main.py').read_bytes()
print(json.dumps({'frozen_artifact_checks':'PASS','artifact_hash_count':len(supplement['artifacts_sha256']),
 'reports':reports,'cells_total':sum(x['cells'] for x in reports),'official_inclusive_seconds':seconds,
 'mean_e025_skill':sum(oldskills)/3,'mean_e041_skill':sum(newskills)/3,
 'mean_delta':(sum(newskills)-sum(oldskills))/3,'model_fits':0,'new_scores':0},indent=2))
