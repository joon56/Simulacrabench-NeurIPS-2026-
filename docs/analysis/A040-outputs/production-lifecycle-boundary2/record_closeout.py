"""Stdlib-only record/preservation of permitted sources and new protocol evidence."""
from datetime import datetime,timezone
import difflib
import hashlib
import json
from pathlib import Path
import shutil

D=Path(__file__).resolve().parent
ROOT=D.parents[3]
T=ROOT/'tmp/a040-production-lifecycle-boundary2'
BASE=ROOT/'docs/analysis/A040-outputs/production-lifecycle-repair1'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def save(name,obj):D.joinpath(name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def diff(a,b,an,bn):return ''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),an,bn))

entry=read(D/'entry.json'); baseline=read(D/'baseline-source-manifest.json'); current=read(D/'source-manifest.json')
assert sha((BASE/'source-manifest.json').read_bytes())==entry['source_manifest_sha256']
assert sha((ROOT/'docs/workflow.md').read_bytes())==entry['workflow_sha256']
preserved=[]; unchanged=[]; source_diff=''; placement_diff=''
for row in baseline['files']:
    name=row['path'];old=(BASE/name).read_bytes();new=(D/name).read_bytes()
    assert sha(old)==row['sha256'],name
    preserved.append({'path':name,'sha256':sha(old)})
    if old==new:unchanged.append(name)
    before=old.decode('utf-8-sig').replace('\r\n','\n')
    placed=before.replace('production-lifecycle-repair1','production-lifecycle-boundary2') if name in ('contract.py','live_launcher.py') else before
    after=new.decode('utf-8-sig').replace('\r\n','\n')
    placement_diff+=diff(before,placed,'repair1/'+name,'placed/'+name)
    source_diff+=diff(placed,after,'placed/'+name,'boundary2/'+name)
for row in current['files']:
    assert sha((D/row['path']).read_bytes())==row['sha256'],row['path']
assert len(unchanged)==10
D.joinpath('source.diff').write_text(source_diff,encoding='utf-8')
D.joinpath('placement.diff').write_text(placement_diff,encoding='utf-8')
save('preservation.json',{'repair1_source13':preserved,'unchanged_new_source10':unchanged,
    'production_change':'live_worker adds cleanup_enter and exact_terminal_saved event only',
    'placement_only':['contract.py','live_launcher.py'],'workflow_preserved':True,
    'installer_scientific_policy_preserved':True,'protected_inputs_not_read_or_hashed':True})

processes=[read(p) for p in sorted(D.glob('*-process.json'))]
used=sum(r['supervisor_wall_seconds'] for r in processes)
assert used<=420 and all(r['within_cap'] for r in processes)
stall=read(D/'real-stall1-process.json')
assert stall['remaining_owned_pid']==0 and stall['actual_python']['has_exited']
trace=[json.loads(line) for line in D.joinpath('attempts/real-stall1/trace.jsonl').read_text().splitlines()]
times={r['event']:r for r in trace}
stall_seconds=times['create_cancellation_observed']['elapsed_seconds']-times['sandbox_create_started']['elapsed_seconds']
assert 119.5<=stall_seconds<125
stall_dir=T/'a040-boundary2-real-stall1'
events=[json.loads(line) for line in (stall_dir/'events.jsonl').read_text().splitlines()]
stage={r['event']:r for r in events if r['event'] in ('cleanup_enter','exact_terminal_saved')}
term=read(stall_dir/'termination-receipt.json')
assert term['sandbox_terminal']['status']==3
proof=D/'protocol-evidence';proof.mkdir(exist_ok=False)
for directory in sorted(T.glob('a040-boundary2-*')):
    if not directory.is_dir():continue
    target=proof/directory.name;target.mkdir()
    for name in ('state.json','result.json','termination-receipt.json','sandbox-query-receipt.json',
                 'sandbox-terminal-evidence.json','cost-ledger.json','source-gate.json','events.jsonl'):
        path=directory/name
        if path.exists():shutil.copyfile(path,target/name)

scope={'outcome':'LOCAL_PRODUCTION_LIFECYCLE_HOLD','remote':'REMOTE_MEASUREMENT_NOT_AUTHORIZED',
    'phase_observations':{
        'actual_Image_build_resolver_function_mount_and_Sandbox_link_observed':True,
        'exact_project_source':'/root/controller_core.py',
        'exact_project_source_sha256':'fc561eee08f1eafbbeac2cbcc5fa31890ef719bf603c5c7dd1af7aea5e556bcb',
        'builder_failure_sandbox_create0_scientific_commands0_app_cleanup_observed':True,
        'real_create_stall_seconds':stall_seconds,'create_and_terminate_each1':True,
        'stall_boundary_reference_candidate_commands0':True,
        'stall_production_timeout_and_exact_terminal_observed':True},
    'unresolved':'Owned Python process exits with access violation c0000005 in python313.dll during final GC; transition assertions alone are not boundary PASS.',
    'root_cause_confirmed':False,'dependency_or_SDK_patched':False,
    'source_manifest_sha256':sha((D/'source-manifest.json').read_bytes()),
    'real_stall_process':stall,'checks_supervisor_wall_seconds':used,
    'all_processes_clean_exit':all(r['exit_code']==0 for r in processes),
    'cpu_caveat':'Wrapper affinity was assigned at launch. Early redirected Python child affinity was not independently captured. Final checks set actual Python affinity before SDK import; stall supervisor also captured that process.',
    'native_error_evidence':'owned-native-crash-evidence.json, supervisor receipts and faulthandler stderr',
    'actual_auth_rpc_model_new_resources':0,'packet_capture_claim':False,
    'old_suite_science_terminal_query_repeated':False}
save('verification.json',scope)
save('stall-timing.json',{'case':'real-stall1','create_start':times['sandbox_create_started'],
    'cancellation_observed':times['create_cancellation_observed'],'wait_seconds':stall_seconds,
    'cleanup_enter_epoch':stage['cleanup_enter']['time'],'terminal_saved_epoch':stage['exact_terminal_saved']['time'],
    'terminal_observed_utc':term['terminal_observed_utc'],'child_finally':times['child_finally'],
    'supervisor':stall,'qualification':'PHASE_ASSERTIONS_OBSERVED_PROCESS_EXIT_FAILED'})
now=datetime.now(timezone.utc)
active=(now-datetime.fromisoformat(entry['entry_utc'].replace('Z','+00:00'))).total_seconds()
assert active<2700
save('cost-time-ledger.json',{'entry_utc':entry['entry_utc'],'recorded_utc':now.isoformat(),
    'active_seconds':active,'prior_preparation_seconds':17197.7879076,'cumulative_preparation_seconds':17197.7879076+active,
    'science_processes_unchanged':4,'science_seconds_unchanged':1077.3504532,'checks_supervisor_wall_seconds':used,
    'aggregate_check_cap_seconds':420,'processes':processes,'child_time_not_double_counted':True,
    'new_remote_cost_actions':0,'cash_actions':0,'historical_workspace_metered_usd':.01009897,
    'historical_workspace_billed_usd':0,'final_attributed_A040_cost':None,'historical_gpu_seconds':None,
    'preparation_plan_usd':1,'total_plan_usd':5,'cash_authority_usd':0,'reservation_2400s_usd':2.965933453125})

status='''- **2026-10-06 A040 S1 boundary2: transitions observed; full lifecycle HOLD.**
  Actual SDK Image.build/function/mount/resolver reached Sandbox/output/terminal;
  builder failure produced Sandbox0/science0. Real120s create expiry reached metadata
  terminal with create1/terminate1 and no boundary/reference/candidate commands.
  Owned Python then failed at final GC with c0000005/python313.dll. Assertions are
  not clean-process PASS; root cause unresolved, no SDK/dependency change or remote retry.
  S0 review only. Prior repair1 HOLD/old terminal/science/STOP/HOLDs preserved.
  [Closeout](analysis/A040-outputs/production-lifecycle-boundary2/closeout.md),
  [S0 handoff](analysis/A040-outputs/production-lifecycle-boundary2/s0-handoff.ko.md).

'''
log='''## 2026-10-06 - A040 S1 observes actual Image.build and120s timeout boundaries; exit failure retains HOLD

- User supplied same-S1 continuation; current AGENTS/CLAUDE/status/log3/workflow r5
  reread, source13 identity matched9bed4451.45min/10min closeout,420s local checks,
  short60s/stall210s caps. No older successful11-case suite or live query repeated.
- Default Endpoint._build invoked actual SDK Image.build/resolver/function/mount.
  Only project source controller_core.py1760bytes/hashfc561eee entered fake transfer;
  exact completed image reached real SDK Sandbox/FS/streams and protocol terminal.
  Builder failure stopped before Sandbox/science and reached App cleanup.
- Real production120s stall, cancel_grace2 and cleanup60 preserved; cancellation,
  cleanup entry, exact terminal file and actual Python/launcher exit times recorded.
  Create1/terminate1, boundary/reference/candidate0. No fake clock or immediate exception.
- Transition assertions completed but native c0000005 during Python final GC recurred.
  Profile cleanup, narrower monitoring, explicit GC/loop close and plain protobuf
  evidence did not repair it; no-observer await-chain variant also failed. Owned Windows
  error records identify python313.dll, not a proven root cause. No dependency install,
  SDK patch, os._exit success masking or additional model/remote action.
- New production change only two lifecycle timestamps; two path placements, other10
  sources byte-identical. Old failure/HOLD/source/latches preserved. Current full verdict
  LOCAL_PRODUCTION_LIFECYCLE_HOLD / REMOTE_MEASUREMENT_NOT_AUTHORIZED; return S0.
- Prep17197.7879076s plus this active wall once; science4/1077.3504532s unchanged.
  See cost ledger for all retries; supervisor/actual child lifetimes kept separate.
  Historical meteredUSD0.01009897/billed0 is not final A040 cost or zero GPU use.
  No auth/RPC/build/model/protected data/ZIP/commit/push/tree/subagent/S2/S3.
  All existing research STOP/HOLD/exposure/E041/E025/parked/A018-unconfirmed retained.
- [Closeout](analysis/A040-outputs/production-lifecycle-boundary2/closeout.md),
  [Verification](analysis/A040-outputs/production-lifecycle-boundary2/verification.json),
  [S0 handoff](analysis/A040-outputs/production-lifecycle-boundary2/s0-handoff.ko.md).

'''
docrecords=[]
for name,addition in [('status',status),('log',log)]:
    path=ROOT/'docs'/f'{name}.md';before=T.joinpath(name+'-before.md').read_bytes()
    assert path.read_bytes()==before,'Concurrent doc edit: '+name
    added=addition.replace('\n','\r\n').encode('utf-8')
    marker=b'## Current position\r\n\r\n'
    at=before.index(marker)+len(marker) if name=='status' else before.index(b'## ')
    after=before[:at]+added+before[at:]
    path.write_bytes(after)
    assert after[:at]+after[at+len(added):]==before
    docrecords.append({'path':'docs/'+name+'.md','before_sha256':sha(before),'after_sha256':sha(after),
                       'addition_offset':at,'addition_bytes':len(added),'original_restored_by_removing_addition':True})
save('document-preservation.json',docrecords)
print(json.dumps({'outcome':scope['outcome'],'stall_seconds':stall_seconds,'check_seconds':used,
    'active_seconds':active,'source_sha256':scope['source_manifest_sha256']}))
