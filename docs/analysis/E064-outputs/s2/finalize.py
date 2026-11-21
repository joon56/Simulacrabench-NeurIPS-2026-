"""B01 document closeout from completed receipts only; stdlib, no numeric loads."""
from datetime import datetime, timezone, timedelta
from pathlib import Path
import hashlib
import json
import subprocess
import os

ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(name,value):
    with (OUT/name).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(value,f,indent=2,ensure_ascii=False,allow_nan=False); f.write('\n')
def write(name,text):
    with (OUT/name).open('x',encoding='utf-8',newline='\n') as f: f.write(text)

entry=read(OUT/'batch-entry.json')
stages={p.name.removesuffix('-resources.json'):read(p) for p in OUT.glob('*-resources.json')}
required=('tests','tests-resources','preflight2','assembly','evaluate','package','official')
for s in required:
    r=stages[s]
    assert r['status']=='PASS' and r['exit_code']==0 and r['reason']=='COMPLETE',s
    assert max(r['peak_owned_tree_bytes'].values())<8*1024**3,s
assert stages['preflight']['status']=='FAIL' and stages['preflight']['cumulative_calls']['full_stack']==0
for s in ('assembly','official'): assert stages[s]['wall_seconds']<=900
measured=sum(r['wall_seconds'] for r in stages.values())
charged=measured+entry['administrative_compute_reserve_seconds']
assert charged<=3600
assert len(list(OUT.glob('all3-start-*.json'))) == 2
official=read(OUT/'official.json'); assembly=read(OUT/'assembly.json')
regression=read(OUT/'regression.json'); package=read(OUT/'package.json')
assert official['status']==assembly['status']==regression['status']=='PASS'
calls=official['cumulative_calls']
assert calls=={'full_stack':6,'neural':18,'metric':16}
for n,count in (('unicef',17856),('world_bank',39520),('unhcr',132273)):
    for report in (assembly,official):
        r=report['instruments'][n]
        assert r['vectors']==count and r['comparisons']['H']['max_abs']==0
        assert r['natural_policy']['status']=='PASS'
        if n!='unhcr': assert r['comparisons']['E041']['max_abs']==0
    r=regression['instruments'][n]
    assert abs(r['delta_E025'])<=.002 and r['delta_E041']>=-.002

# Verify only explicit allowed inputs/outputs and immutable source/receipt maps.
preserved={}
for p,h in entry['hashes'].items():
    if p in ('docs/status.md','docs/log.md'): continue
    assert sha(ROOT/p)==h,p
    preserved[p]=h
frozen=read(OUT/'release-freeze.json')['hashes']
repair=read(OUT/'controller-repair-freeze.json')
for p,h in repair['replaces'].items(): assert frozen[p]==h
assert sha(OUT/'controller-repair1/release-before.py')==repair['old_controller_sha256']
frozen.update(repair['hashes'])
for p,h in frozen.items(): assert sha(ROOT/p)==h,p
snapshot=ROOT/read(OUT/'package-path.json')['snapshot']
for n,h in package['files'].items():
    path=snapshot.with_suffix('.zip') if n.endswith('.zip') else snapshot/n
    assert sha(path)==h
assert (snapshot/'main.py').read_bytes()==(OUT/'extracted/main.py').read_bytes()==(OUT/'main.py').read_bytes()
assert (snapshot/'SCORES.md').read_bytes()==(OUT/'SCORES.md').read_bytes()

events=[json.loads(line) for p in OUT.glob('calls-*.jsonl') for line in p.read_text(encoding='utf-8').splitlines()]
nested={k:sum(e.get('seconds',0) for e in events if e.get('event')=='return' and e.get('kind')==k) for k in ('full_stack','neural','metric')}
projection=[json.loads(x) for x in (OUT/'projection.jsonl').read_text(encoding='utf-8').splitlines()]
assert all(x['role'] in ('TRAIN','DEV') for x in projection)
peaks={k:max(r['peak_owned_tree_bytes'][k] for r in stages.values()) for k in ('rss','commitment')}
gap=max(r['maximum_monotonic_sample_gap_seconds'] for r in stages.values())
now=datetime.now(timezone(timedelta(hours=9)))
assert now.timestamp()<datetime.fromisoformat(entry['closeout_deadline_utc'].replace('Z','+00:00')).timestamp()
gross=(now-datetime.fromisoformat(entry['resumed_entry_kst'])).total_seconds()+600
assert gross<=10800
ledger=dict(stage_receipts=stages,measured_controller_seconds=measured,
    administrative_conservative_charge_seconds=420,charged_total_seconds=charged,limit_seconds=3600,
    measured_plus_historical_s1_seconds=measured+877.3776708,
    charged_plus_historical_s1_seconds=charged+877.3776708,historical_s1_seconds=877.3776708,
    administrative_limit='420s is a charged conservative administrative allowance, not measured model/CPU wall; reads/writes/hash helper commands only, no unmonitored fit/test. No time reset.',
    nested_seconds_not_added=nested,calls=calls,all3_starts=2,all3_restart=0,conditional_fresh_E025=0,
    focused_test_processes=2,focused_and_repair_cycles=3,
    focused_cycle_semantics='Initial assembly checks; one manifest-reader preflight repair cycle; one final-memory-predicate check. No further focused cycle available.',
    focused_and_repair_seconds=sum(stages[k]['wall_seconds'] for k in ('tests','preflight','preflight2','tests-resources')),
    checker_predict_no_fit=1,cash=0,gpu=0,numerical_threads=2,
    official_affinity=read(OUT/'official-affinity.json'),assembly_affinity='not fixed; numerical pools2',
    peak_owned_tree_bytes=peaks,maximum_sample_gap_seconds=gap,
    memory_semantics='Sampled sum of per-process peak RSS/private; not continuous or simultaneous allocator peak.',
    gross_conservative_elapsed_seconds=gross,prior_hold_gross_charge_seconds=600,inter_session_wait_excluded=True)
save('cost-time-ledger.json',ledger)
ziphash=package['files'][snapshot.with_suffix('.zip').name]
row=regression['instruments']['unhcr']
table='\n'.join(f"| {n} | {r['skill']:.15f} | {r['delta_E025']:+.15f} | {r['delta_E041']:+.15f} |" for n,r in regression['instruments'].items())
text=f'''# E064 B01 S2 closeout

{now.isoformat()}. **RELEASE_QUALIFIED_FOR_USER_REVIEW**; E064 stays parked.
Remaining S2 completed under the user's B01 approval. Return S0; no upload,
TEST choice, actual hosted result or commit/push. Completed S1 was not repeated.

Package: `{snapshot.relative_to(ROOT).as_posix()}.zip`,{package['zip_bytes']}bytes.
SHA256 `{ziphash}`. Actual preparation time is in package-path.json; upload time,
remote bytes/ID/account/slot and deployed scorer version remain unknown.
Root main.py/NOTICE.txt only; no bundled data/weights/new dependencies. Exact E041
prefix and isolated E064 functions. Original source/experiments/snapshots retained.

Three new assembly checks plus one new monitor test (7 boundary assertions) PASS.
Preflight manifest-reader failure preserved and repaired before model/array reads.
Read-only reviewer found final-sample memory predicate gap; original controller
preserved, actual recorded assembly peak below cap, pure boundary repaired/tested
before later stages with supplemental freeze. No scientific restart or policy change.

Source H/assembly/extracted all189649 vectors exact, controls exact E041;
UNHCR132225 changed versus E041. All213 UNHCR heads checked. Metric/donor/replay/
ladder invariant keys5/8/16 and lambda exact against completed S1 H.
Stock ZIP checker PASS; extracted stock official phase1 all3 PASS.
Assembly {stages['assembly']['wall_seconds']:.6f}s; whole official {stages['official']['wall_seconds']:.6f}s,
each<=900s including imports/all instruments/output/driver. No extra parity fit.

| Instrument | Skill | H-E025 | H-E041 |
|---|---:|---:|---:|
{table}

E025 absolute difference<=.002 and H-E041>=-.002 per instrument PASS. UNHCR small
synthetic decline remains counterevidence, not actual efficacy/independent audit.
R and clean E041 all189649 raw exact; clean E025/E041 outputs reused, fresh0.
Historical baseline environment records omit some package/executable fields;
only recorded common fields matched, while current full E064 environment matches
S1. Do not call this complete historical environment or hosted image equality.

Measured monitored stages {measured:.6f}s; plus conservative administrative charge420s
= {charged:.6f}/3600s. Historical S1 {877.3776708:.7f}s separate, not renewed.
Normal6pipeline/18neural/16metric;2all3 starts, restart0. Nested timings not added.
CPU numerical2/GPU0/heavy1; official affinity logicalCPU0/2. Conservative observed
RSS/private {peaks['rss']/1024**3:.6f}/{peaks['commitment']/1024**3:.6f}GiB<8 each,
max sampler gap {gap:.6f}s. No H100/hidden-data900s guarantee; no cash/remote spend.

Only named12 old raw files and3 existing synthetic files; TRAIN/DEV projections,
whole DEV PREDICT masked before model, truth only after fresh assembly output freeze.
No TEST row request, protected raw/key/cache/Adult/SIPP/VAF access. Existing base/
selection/refit/in-sample replay reuse unchanged. Exact whitelist and requests in
batch-entry/numeric-identity/projection; baseline reuse and limitations separate.

Original B01 hosted favorable/adverse/tie/mixed/technical/HOLD arms remain frozen
in SCORES. No public result yet; no automatic promotion or identical resubmission.
E041 incumbent/E025 fallback; E057/E060/E061/E062/E063/E064 parked; all STOP/HOLD,
E058/E059/A023/A024/A039/A040,17999/12339SSUID/aggregates/A022 roles/E059 consumed
and protected audit2074/1177/calibration1866,A_half unpromoted,A018 unconfirmed kept.

Next: S0 reviews fixed package and disclosed limits. Separate user decision for
any upload/TEST action. Final job census/ownership release in verification.json.
'''
write('closeout.md',text)
write('s0-handoff.ko.md',f'''# EXEC-B01-E064 → S0

**RELEASE_QUALIFIED_FOR_USER_REVIEW. E064 parked 유지.**

- 완료 S1 재실행0. 새 조립검사3+감시기 영향검사1 PASS.
- Assembly/source/extracted189649 raw exact; U/WB controls exact; 불변량5/8/16·lambda 일치.
- ZIP checker·stock official all3 PASS. Assembly{stages['assembly']['wall_seconds']:.3f}s,
  official 전체{stages['official']['wall_seconds']:.3f}s/900s.
- UNHCR ΔE025{row['delta_E025']:+.12f}, ΔE041{row['delta_E041']:+.12f}.
  E025 절대.002/기관 및 E041 하한-.002 통과. 합성 하락·실제 효과 미확정 유지.
- 감시 stage 실측{measured:.3f}s + 준비/기록 보수적 차감420s = {charged:.3f}/3600s.
 6pipeline/18neural/16metric, all3시작2, 과학재시도0, cash0. 과거 S1 별도.
- manifest reader·최종 메모리 판정 경계 수리 기록 보존. 성공 학습 반복 없음.
- 과거 baseline의 일부 환경 식별값은 미기록; complete environment equality 주장 없음.

ZIP: `{snapshot.relative_to(ROOT).as_posix()}.zip` ({package['zip_bytes']}bytes)
SHA256 `{ziphash}`.
공식 제작 시각/바이트는 package-path/package.json, 비교·비용·한계는 closeout/verification.
업로드/계정/slot/ID/remote bytes 미확인. 자동 업로드·TEST 선택·commit/push 없음.
S0는 고정 산출물·한계와 원래 SCORES 판독표를 검토한다. 새 연구/추가학습 자동 시작 없음.
쓰기 해제와 jobs는 최종 verification의 명시적 receipt를 따른다.
''')
save('preservation.json',dict(status='PASS',original_hashes=preserved,
    current_frozen_hashes=frozen,source_input_policy_unchanged=True,
    limit='Explicit allowed files only; no whole dirty tree/protected cache scan or rollback.'))
save('completion-precheck.json',dict(status='PASS',verdict='RELEASE_QUALIFIED_FOR_USER_REVIEW',
    observed_at=now.isoformat(),calls=calls,projection_requests=len(projection),
    scientific_starts=2,source_assembly_extracted_raw_vectors=189649,
    local_zip_sha256=ziphash,remaining='Final named-job census, shared result addition, writer release receipt.'))
print(json.dumps({'status':'PASS','measured_seconds':measured,'charged_seconds':charged,'zip_sha256':ziphash}))
