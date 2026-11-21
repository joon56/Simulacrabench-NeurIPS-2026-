"""Append verified B01 result; preserve previous shared bytes and release writer."""
from pathlib import Path
import hashlib,json,os
from datetime import datetime,timezone,timedelta
ROOT=Path(__file__).resolve().parents[4]; OUT=Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):
    with p.open('x',encoding='utf-8',newline='\n') as f: json.dump(obj,f,indent=2,ensure_ascii=False);f.write('\n')
entry=read(OUT/'batch-entry.json'); pre=read(OUT/'completion-precheck.json')
assert pre['status']=='PASS'
jobs=read(OUT/'exit-job-census.json'); assert jobs['named_jobs']==[]
ledger=read(OUT/'cost-time-ledger.json'); package=read(OUT/'package.json')
snapshot=ROOT/read(OUT/'package-path.json')['snapshot']
before=(OUT/'status-before.md').read_bytes()
startnote="\r\n- **2026-10-23 EXEC-B01-E064 owns writes: remaining S2 in progress.** S3 and S0 releases accepted; named jobs0 at intake. Completed E064 S1 reused. Original B01 caps/gates retained; no upload/TEST/commit/push. [Entry](analysis/E064-outputs/s2/batch-entry.json).\r\n"
expected=before.decode('utf-8-sig').replace('## Current position','## Current position\r\n'+startnote).encode('utf-8')
assert (ROOT/'docs/status.md').read_bytes()==expected,'Concurrent status edit; do not overwrite'
logbefore=(OUT/'log-before.md').read_bytes()
assert (ROOT/'docs/log.md').read_bytes()==logbefore,'Concurrent log edit; do not overwrite'
notice=f'''\r\n\r\n- **2026-10-23 B01 E064 S2 complete: RELEASE_QUALIFIED_FOR_USER_REVIEW.**
  S1 reused; source/assembly/extracted189649 raw exact, controls exact. Checker and
  official all3 PASS ({ledger['stage_receipts']['official']['wall_seconds']:.3f}s/900s).
  UNHCR delta E025-.000570498449/E041-.000084353602; fixed release gates pass,
  small synthetic decline retained, no efficacy/TEST adoption. E064 parked.
  ZIP2026-10-23-E064.zip prepared locally, not uploaded. Two ordinary controller
  repairs retained; no scientific restart. B01 charged{ledger['charged_total_seconds']:.3f}/3600s,
 6pipeline/18neural/16metric, CPU2/GPU0/cash0. [Closeout](analysis/E064-outputs/s2/closeout.md),
  [S0 handoff](analysis/E064-outputs/s2/s0-handoff.ko.md), [verification](analysis/E064-outputs/s2/verification.json).
  **Writer none after B01 release; next S0 review.** Named local jobs0 observed,
  no remote census. All parked/STOP/HOLD/protected roles/A_half/A018 preserved.
'''.replace('\n','\r\n').replace('\r\r\n','\r\n')
status=before.replace(b'## Current position',b'## Current position'+notice.encode('utf-8'),1)
lognote=f'''## 2026-10-23 - B01 E064 S2 release qualified; writer returned to S0

- Explicit user B01/resume authority; current workflow r6 reread, S3/S0 releases
  accepted. Completed E064 S1 not repeated. Original source/input/criteria/caps retained.
- New assembly checks3 PASS; exact189649 source/assembly/extracted raw, controls exact;
  metric/donor/replay/ladder invariants5/8/16 and lambda match S1 H. Stock checker and
  official phase1 all3 PASS. E025 absolute.002 and E041 signed-.002 per-instrument PASS.
- UNHCR deltaE025-.000570498449168, deltaE041-.000084353601793; synthetic decline
  retained, no actual efficacy/oracle/audit/TEST claim. E064 parked/E041 incumbent.
- Assembly{ledger['stage_receipts']['assembly']['wall_seconds']:.6f}s;
  official whole{ledger['stage_receipts']['official']['wall_seconds']:.6f}s/900s.
  Measured monitored stages{ledger['measured_controller_seconds']:.6f}s plus conservative
  administration420s = {ledger['charged_total_seconds']:.6f}/3600; historical S1 separate.
 2all3 starts/6pipeline/18neural/16metric, fresh baseline0, scientific restart0.
- Manifest reader failed before numerical work, repaired with preserved attempt.
  Independent read-only review found final memory predicate gap; recorded peaks below
  cap, corrected and1 new stdlib boundary test PASS before later stages. No S1 repeat.
- E062 baseline missing environment fields disclosed; common recorded fields and
  input/source/receipt/raw identity match. No complete historical/hosted image equality.
- ZIP2026-10-23-E064.zip,{package['zip_bytes']}bytes, SHA256{pre['local_zip_sha256']}.
  Prepared only; account/slot/remote bytes/ID/upload unknown. Original SCORES arms kept.
- Named jobs0 at exit; writer released to none/S0 review. No upload/TEST choice,
  source/tree/old snapshot edit, commit/push/remote/install/protected-input access.
  All parked/STOP/HOLD/exposure/A022/E059/A_half/A018 boundaries preserved.
- [Closeout](analysis/E064-outputs/s2/closeout.md),
  [S0 handoff](analysis/E064-outputs/s2/s0-handoff.ko.md),
  [Verification](analysis/E064-outputs/s2/verification.json).

'''.replace('\n','\r\n')
idx=logbefore.index(b'## ')
log=logbefore[:idx]+lognote.encode('utf-8')+logbefore[idx:]
(ROOT/'docs/status.md').write_bytes(status);(ROOT/'docs/log.md').write_bytes(log)
assert status.replace(notice.encode('utf-8'),b'',1)==before
assert log[:idx]+log[idx+len(lognote.encode('utf-8')):]==logbefore
scores_before=(snapshot/'SCORES.md').read_bytes()
append=f'''\n## Local B01 qualification — 2026-10-23

RELEASE_QUALIFIED_FOR_USER_REVIEW. ZIP checker/official all3 and189649 raw parity
PASS; E025 absolute.002 and E041 signed-.002 per instrument PASS. UNHCR deltas
-.000570498449168/-.000084353601793 respectively; exposed synthetic decline retained.
E064 parked, actual hosted result NOT OBSERVED. No upload/slot/account/ID claim.
ZIP SHA256 {pre['local_zip_sha256']}; {package['zip_bytes']}bytes.
Details: ../../docs/analysis/E064-outputs/s2/closeout.md.
Original prospective arms above unchanged. No automatic adoption or repeat.
'''.encode('utf-8')
(snapshot/'SCORES.md').write_bytes(scores_before+append)
save(OUT/'shared-document-additions.json',dict(status_original_sha256=hashlib.sha256(before).hexdigest(),
    status_final_sha256=sha(ROOT/'docs/status.md'),status_insertion=notice,
    log_original_sha256=hashlib.sha256(logbefore).hexdigest(),log_final_sha256=sha(ROOT/'docs/log.md'),
    log_insert_offset=idx,log_insertion=lognote,original_bytes_reconstructed=True,
    snapshot_scorecard_original_sha256=hashlib.sha256(scores_before).hexdigest(),
    snapshot_scorecard_final_sha256=sha(snapshot/'SCORES.md'),scorecard_original_prefix_preserved=True))
now=datetime.now(timezone(timedelta(hours=9))).isoformat()
artifacts={}
for directory,dirs,files in os.walk(OUT):
    dirs[:]=[name for name in dirs if name not in ('official-work','__pycache__')]
    for name in files:
        if name in ('artifact-manifest.json','verification.json'): continue
        p=Path(directory)/name
        artifacts[p.relative_to(ROOT).as_posix()]=sha(p)
for p in (snapshot/'main.py',snapshot/'NOTICE.txt',snapshot/'SCORES.md',snapshot.with_suffix('.zip'),
          ROOT/'docs/status.md',ROOT/'docs/log.md'):
    artifacts[p.relative_to(ROOT).as_posix()]=sha(p)
save(OUT/'artifact-manifest.json',dict(created_at=now,hashes=artifacts,
    scope='Owned B01 artifacts and explicit snapshot/shared documents only. Self/final verification excluded. Official temporary compiler/cache tree not traversed; prediction hashes are in official parity receipts.'))
save(OUT/'verification.json',dict(record='B01-E064-S2',verdict='RELEASE_QUALIFIED_FOR_USER_REVIEW',
    observed_at=now,authority=entry['authority'],role='EXEC-B01-E064 / S2',workflow_revision=entry['workflow_revision'],
    workflow_sha256=entry['workflow_sha256'],read_receipt='batch-entry.json',
    head=jobs['head'],branch=jobs['branch'],dirty_inventory=jobs['dirty'],dirty_inventory_limit=jobs['inventory_limit'],
    input_reuse='baseline-reuse.json; reuse-receipt-identities.json; numeric-identity.json',
    code_freeze='release-freeze.json plus controller-repair-freeze.json; predecessor preserved',
    technical=pre,release_regression=read(OUT/'regression.json'),cost_time='cost-time-ledger.json',
    preservation='preservation.json; shared-document-additions.json',exposure='exposure-ledger.md',
    artifact_manifest_sha256=sha(OUT/'artifact-manifest.json'),
    original_s1_repeated=False,original_assembly_checks_repeated=False,
    repairs='repair-history.md',independent_review='independent-review.md; static only',
    package=package,zip_path=snapshot.with_suffix('.zip').relative_to(ROOT).as_posix(),
    upload=False,hosted_result=False,commit_push=False,final_test_choice=False,
    limitations=['Small negative exposed-synthetic result is not actual effect evidence.',
      'Historical baseline lacks some package/executable identities; common recorded fields only.',
      'Administrative420s charge is conservative, not measured execution time.',
      'Sampled process high-water peaks, not continuous/allocator peak; no hidden/H100 runtime guarantee.',
      'Private deployed scorer/version, account/slot and remote bytes unknown.'],
    named_jobs=jobs['named_jobs'],job_scope='Local python/pythonw/uv process metadata, not remote/all-session census',
    outgoing_owner='EXEC-B01-E064 /root',incoming_owner='none; S0 result review next',
    exclusive_writer_released=True,release_at=now,owned_running_commands=[],
    release_condition='Effective after this finite document process completes; no scientific process remains.',
    preserved_states='E041 incumbent/E025 fallback; E057/E060/E061/E062/E063/E064 parked; all STOP/HOLD,17999/12339SSUID/A022/E059 consumed/protected roles,A_half not promoted,A018 unconfirmed.'))
print('Shared additions preserve original bytes; writer release receipt saved.')
