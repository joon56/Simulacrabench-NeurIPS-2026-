"""Bounded documentation/preservation audit. Stdlib only; no runtime imports."""
import ast
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import shutil

D=Path(__file__).resolve().parent
ROOT=D.parents[3]
T=ROOT/'tmp/a040-production-lifecycle-repair1'
BASE=ROOT/'docs/analysis/A040-outputs/local-preparation-repair2'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def save(name,obj): D.joinpath(name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def diff(a,b,an,bn): return ''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),an,bn))

entry=read(D/'entry.json')
original=read(D/'original/source-manifest.json')
current=read(D/'source-manifest.json')
preserved=[]; changed=[]; unchanged=[]; source_diff=''; placement_diff=''
for row in original['files']:
    name=row['path']; old=(BASE/name).read_bytes(); copied=(D/'original'/name).read_bytes()
    assert sha(old)==sha(copied)==row['sha256'],name
    preserved.append({'path':str((BASE/name).relative_to(ROOT)).replace('\\','/'),'sha256':sha(old)})
    new=D.joinpath(name).read_bytes()
    (unchanged if new==old else changed).append(name)
    before=old.decode('utf-8-sig').replace('\r\n','\n')
    after=new.decode('utf-8-sig').replace('\r\n','\n')
    placed=before.replace('docs/analysis/A040-outputs/local-preparation-repair2',
                          'docs/analysis/A040-outputs/production-lifecycle-repair1')
    placement_diff+=diff(before,placed,'original/'+name,'placed/'+name)
    source_diff+=diff(placed,after,'placed/'+name,'new/'+name)
for row in current['files']:
    raw=D.joinpath(row['path']).read_bytes()
    assert sha(raw)==row['sha256'] and len(raw)==row['bytes'],row['path']
    ast.parse(raw.decode('utf-8-sig'))
helper=ROOT/'docs/analysis/A040-outputs/termination-query-repair1/confirm_terminal.py'
assert sha(helper.read_bytes())==entry['helper_sha256']
assert sha((BASE/'source-manifest.json').read_bytes())==entry['source_manifest_sha256']
assert sha((ROOT/'docs/workflow.md').read_bytes())==entry['workflow_sha256']
D.joinpath('source.diff').write_text(source_diff,encoding='utf-8')
D.joinpath('placement.diff').write_text(placement_diff,encoding='utf-8')
D.joinpath('cleanup-query-reuse.diff').write_text(diff(helper.read_text(encoding='utf-8-sig'),D.joinpath('cleanup_query.py').read_text(encoding='utf-8-sig'),'accepted/confirm_terminal.py','new/cleanup_query.py'),encoding='utf-8')
assert set(unchanged)=={'protocol.py','controller_core.py','live_binding.py','payload.py','linux_boundary.py','linux_watchdog.py','linux_runner.py'}
save('preservation.json',{'original_production12':preserved,'unchanged_new_copies':unchanged,
    'changed_new_copies':changed,'new_production_module':'cleanup_query.py',
    'original_helper_sha256':sha(helper.read_bytes()),'workflow_sha256':entry['workflow_sha256'],
    'installer_and_scientific_runner_bytes_unchanged':True,'protected_inputs_not_hashed':True})

process_names=['loop-red','cycle1','cycle2','cycle3','cycle4','cli','parent-cli','parent-cli2']
processes=[dict(name=name,**read(D/(name+'-process.json'))) for name in process_names]
check_seconds=sum(r['wall_seconds'] for r in processes)
cases=sum((read(D/(name+'-case-results.json')) for name in ['cycle2','cycle3','cycle4']),[])
assert len(cases)==11 and all(r['pass'] for r in cases)
assert check_seconds<180
proof=D/'protocol-evidence'; proof.mkdir(exist_ok=False)
for run in sorted(T.glob('a040-local-cycle*')):
    if not run.is_dir(): continue
    target=proof/run.name; target.mkdir()
    # Metadata/events only, all newly generated in this session. No old arrays.
    for name in ('state.json','result.json','termination-receipt.json','sandbox-query-receipt.json',
                 'sandbox-terminal-evidence.json','cost-ledger.json','source-gate.json','events.jsonl'):
        path=run/name
        if path.exists(): shutil.copyfile(path,target/name)
    config=T/(run.name+'.json')
    if config.exists(): shutil.copyfile(config,target/'protocol-config.json')
for name in ('child-guard.json','contract.json'):
    shutil.copyfile(T/'cli-parent-retry2'/name,proof/('parent-'+name))
for name in ('exit.json','stdout.txt','stderr.txt'):
    shutil.copyfile(T/'cli-parent-retry2/launcher'/name,proof/('parent-'+name))

now=datetime.now(timezone.utc)
active=(now-datetime.fromisoformat(entry['entry_utc'].replace('Z','+00:00'))).total_seconds()
assert active<3000
ledger={'entry_utc':entry['entry_utc'],'recorded_utc':now.isoformat(),'active_seconds':active,
    'whole_limit_seconds':3600,'work_cutoff_utc':entry['work_cutoff_utc'],'closeout_reserved_seconds':600,
    'preparation_prior_seconds':14777.0797748,'preparation_cumulative_seconds':14777.0797748+active,
    'science_processes_unchanged':4,'science_seconds_unchanged':1077.3504532,
    'checks_supervisor_wall_sum_seconds':check_seconds,'checks_limit_seconds':180,
    'check_processes':processes,'overlap_policy':'CLI child included in parent wall once; no double charge',
    'per_check_cap_caveat':'cycle3 killed at WaitForExit(30000); supervisor/reap wall 30.0874074. Strict <=30s child lifetime not independently established. Subsequent checks used 29s termination.',
    'real_auth_rpc_build_science':0,'this_task_remote_cost_actions':0,'this_task_cash_actions':0,
    'prior_workspace_metered_usd':.01009897,'prior_workspace_billed_usd':0,
    'historical_gpu_seconds':None,'final_a040_attributed_cost':None,
    'prior_component_usd':.00001152,'prior_management_value_not_invoice':.6550409048674121,
    'reservation_2400s_usd':2.965933453125,'preparation_plan_usd':1,'total_plan_usd':5,'cash_authority_usd':0}
save('cost-time-ledger.json',ledger)
save('verification.json',{'outcome':'LOCAL_PRODUCTION_LIFECYCLE_HOLD',
    'implementation':'LOCAL_REPAIR_IMPLEMENTED','remote':'REMOTE_MEASUREMENT_NOT_AUTHORIZED',
    'named_lifecycle_cases_pass':cases,'expected_original_loop_rejection':True,
    'actual_script_entry_negative_cases':2,'actual_parent_child_cli_gate_pass':True,
    'positive_input_injected_main_child_dispatch_pass':True,
    'original_pass_suites_or_science_or_terminal_query_rerun':False,
    'unresolved':[
        'Extra actual 120-second create-stall validation could not complete inside 30-second check cap; supervisor/reap wall30.0874074, strict per-child compliance unproved.',
        'Positive orchestration uses input Context factory and image_builder completed-image provider. Actual Sandbox/FS/process/streams are retained, but SDK Image.build itself is not executed in this suite; external-RPC-only replacement for the entire build-to-CLI chain is therefore not claimed.',
        'Actual Linux/native offline/memory/watchdog, H100900s, full pinned input path and model/release remain unmeasured.'
    ],'original_source_and_workflow_preserved':True,'source_manifest_sha256':sha((D/'source-manifest.json').read_bytes()),
    'checks_supervisor_wall_seconds':check_seconds,'current_test_suite_all_passed':False,
    'real_auth_rpc_model_gpu':0,'evidence_basis':'local source, audit guards and fixture traces; not packet capture'})

status_add='''- **2026-10-05 A040 S1: local production lifecycle repaired; full validation HOLD.**
  Actual SDK loop/Sandbox hydration/FS/streams, pre-create reservation and metadata
  cleanup integrated;11 named lifecycle cases passed. Actual parent/child CLI gate passed.
  Extra120s stall check was killed at30s (supervisor30.0874s); native timer validation incomplete.
  Completed-image provider remains in positive fixture; entire build chain is not RPC-only validated.
  No real auth/RPC/build/model/GPU/old-resource lookup; original terminal remains closed.
  S0 review only; no remote/H100/S2 authority. Original sources and all STOP/HOLDs preserved.
  [Closeout](analysis/A040-outputs/production-lifecycle-repair1/closeout.md),
  [S0 handoff](analysis/A040-outputs/production-lifecycle-repair1/s0-handoff.ko.md).

'''
log_add='''## 2026-10-05 - A040 S1 repairs production lifecycle locally; returns bounded validation HOLD

- Current same-chat S1 authority; actual r5 read/receipt and source identity recorded.
  Original production12, accepted cleanup helper and workflow preserved. No old suites repeated.
- New copies use SDK-managed dispatch, durable pre-create resource/reservation intent,
  single-mutation journal and metadata-only exact-ID cleanup; terminal saved before billing.
  Installer/scientific runner/selection/900s policy unchanged; seven production copies byte-identical.
- Eleven named actual-SDK lifecycle cases passed, plus expected original loop rejection,
  actual __main__ gates and real parent/child CLI gate using new invalid protocol pins.
  Fixture AppStop protobuf and Windows audit executable=None mistakes fixed in this session.
- Preserve failed extra120s create-stall check: killed at30s, supervisor/reap30.0874074s.
  Real timer validation and strict per-child <=30s evidence incomplete. Positive fixture also
  supplies completed image rather than running SDK Image.build; no full external-RPC-only claim.
- LOCAL_PRODUCTION_LIFECYCLE_HOLD / REMOTE_MEASUREMENT_NOT_AUTHORIZED; S0 review.
  No auth/RPC/billing lookup/build/H100/model/data/ZIP/commit/push/tree/subagents/S2/S3.
  Prior preparation14777.0797748s plus this task once; science4/1077.3504532s unchanged.
  Detailed wall/cap caveat in cost ledger. Existing terminal closed; all research STOP/HOLD,
  exposure17999/12339, roles, E041/E025/parked and A018-unconfirmed/S3-stop preserved.
- [Closeout](analysis/A040-outputs/production-lifecycle-repair1/closeout.md),
  [Verification](analysis/A040-outputs/production-lifecycle-repair1/verification.json),
  [S0 handoff](analysis/A040-outputs/production-lifecycle-repair1/s0-handoff.ko.md).

'''
documents=[]
for name,addition in [('status',status_add),('log',log_add)]:
    path=ROOT/'docs'/f'{name}.md'; before=T.joinpath(name+'-before.md').read_bytes()
    assert path.read_bytes()==before,'Concurrent document edit: '+name
    raw=addition.replace('\n','\r\n').encode('utf-8')
    if name=='status':
        marker=b'## Current position\r\n\r\n'; at=before.index(marker)+len(marker)
    else: at=before.index(b'## ')
    after=before[:at]+raw+before[at:]
    assert after[:at]+after[at+len(raw):]==before
    path.write_bytes(after)
    documents.append({'path':'docs/'+name+'.md','prior_sha256':sha(before),'new_sha256':sha(after),
        'addition_offset':at,'addition_bytes':len(raw),'removing_only_addition_restores_original':True})
save('document-preservation.json',documents)
save('artifact-manifest.json',{'files':[{'path':p.relative_to(D).as_posix(),'bytes':p.stat().st_size,
    'sha256':sha(p.read_bytes())} for p in sorted(D.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json' and '__pycache__' not in p.parts]})
print(json.dumps({'outcome':'BOUNDED_RECORDS_WRITTEN','active_seconds':active,'cumulative_preparation_seconds':14777.0797748+active,
    'checks_wall_seconds':check_seconds,'lifecycle_case_passes':len(cases),'changed':changed,'unchanged':unchanged}))
