"""Three new boundaries only. Actual Image.build + real 120s timer; no model."""
import asyncio
from dataclasses import asdict
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import sys
import threading
import time
import ctypes
if not ctypes.windll.kernel32.SetProcessAffinityMask(ctypes.windll.kernel32.GetCurrentProcess(),3):
    raise OSError('CPU2 affinity could not be set')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import local_guard
local_guard.install()
local_guard.block_sdk_auth()
from modal._utils.async_utils import synchronizer
from modal._image import _Image
from modal.sandbox import _Sandbox
import fixture_transport as wire
wire.install_router_transport()
from boundary_transport import Backend,BUILT
from contract import Plan,sha
from payload import Payload
from sdk_endpoint import Endpoint
from live_worker import Context, cleanup
from controller_core import install_pins
import live_launcher

ROOT=HERE.parents[3]
WORK=ROOT/'tmp/a040-production-lifecycle-boundary2'
ATTEMPT,CASE=sys.argv[1:]
assert CASE in ('success','builder_fail','stall')
evidence=HERE/'attempts'/ATTEMPT
evidence.mkdir(parents=True,exist_ok=False)
name='a040-boundary2-'+ATTEMPT
directory=WORK/name
backend=Backend(CASE,name,directory,evidence/'trace.jsonl')
wire.ACTIVE=backend
started=time.perf_counter()
backend.record('child_entry',pid=os.getpid(),case=CASE)

now=time.time()
# Production120s create/2s cancellation/60s cleanup retained; child supervisor is separate.
plan=Plan('LOCAL_PROTOCOL_FIXTURE',name,'im-fixturebase',sha(b'base-protocol'),now+2400,now+4800,now+7200)
assert plan.cancel_grace==2 and plan.cleanup_timeout==60
manifest=json.loads((HERE/'source-manifest.json').read_text())
config={'plan':asdict(plan),'source_manifest_sha256':sha((HERE/'source-manifest.json').read_bytes()),
    'extra_files':[dict(r,path='docs/analysis/A040-outputs/production-lifecycle-boundary2/'+r['path'],reason='new local boundary source') for r in manifest['files']]}
config_path=evidence/'protocol-config.json'; config_path.write_text(json.dumps(config))
contexts=[]
def factory(config,plan):
    raw=b'bounded protocol bytes'
    row={'path':'protocol.txt','bytes':len(raw),'sha256':sha(raw)}
    endpoint=Endpoint(client_factory=backend.factory)
    assert endpoint.image_builder.__func__ is Endpoint._build
    assert endpoint.sandbox_factory is not None
    context=Context(directory,plan,endpoint,Payload([row],[],lambda _:raw,lambda _:b'',plan.scope),'PROTOCOL_PINS_NOT_INSTALLED')
    contexts.append(context)
    return context
try:
    code=live_launcher.main([str(config_path),'--child'],context_factory=factory)
    context=contexts[0]
    result=json.loads((directory/'result.json').read_text())
    term=json.loads((directory/'termination-receipt.json').read_text())
    backend.record('production_return',outcome=result['outcome'],termination=term['termination'])
    assert any(r['event']=='sdk_image_build_chain' for r in backend.timeline)
    assert backend.source_files and backend.function_definition is not None
    if CASE=='success':
        assert code==0 and result['outcome']=='LOCAL_PROTOCOL_PATH_PASS',result
        assert type(context.endpoint.image) is _Image and context.endpoint.image.object_id==BUILT
        assert type(context.endpoint.sandbox) is _Sandbox
        assert backend.created==backend.terminated==1
        assert backend.stream_reads>0 and backend.stream_writes>0
        assert term['sandbox_terminal']['status']==3
    elif CASE=='builder_fail':
        assert code==1 and result['outcome']=='STOP_FIRST_ERROR',result
        assert 'fixed protocol builder failure' in result['error'],result
        assert backend.created==backend.terminated==0 and backend.commands==[]
        assert backend.stopped and term['termination']=='TERMINAL_TASK0_CONFIRMED',term
    else:
        assert code==1 and result['outcome']=='STOP_FIRST_ERROR',result
        assert 'Operation deadline; cancellation completion not assumed' in result['error']
        assert backend.created==backend.terminated==1 and backend.commands==[]
        assert term['sandbox_terminal']['status']==3 and term['termination']=='TERMINAL_TASK0_CONFIRMED'
        events={r['event']:r for r in backend.timeline}
        elapsed=events['create_cancellation_observed']['elapsed_seconds']-events['sandbox_create_started']['elapsed_seconds']
        assert 119.5<=elapsed<125,elapsed
        stages=[json.loads(line) for line in (directory/'events.jsonl').read_text().splitlines()]
        cleanup_enter=next(r for r in stages if r['event']=='cleanup_enter')['time']
        terminal_saved=next(r for r in stages if r['event']=='exact_terminal_saved')['time']
        assert terminal_saved>=cleanup_enter>=datetime.fromisoformat(events['create_cancellation_observed']['utc']).timestamp()
    assert not local_guard.blocked,local_guard.blocked
    report={'outcome':'BOUNDARY_PASS','case':CASE,'protocol_only':True,'sdk_default_build':True,
        'image_id':BUILT,'creates':backend.created,'terminates':backend.terminated,'commands':backend.commands,
        'terminal':term,'source_files':backend.source_files,'child_work_seconds':time.perf_counter()-started,
        'actual_auth_rpc_model':0,'protected_access':0}
    (evidence/'check-result.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k not in ('commands','terminal')}))
finally:
    backend.record('child_finally',pid=os.getpid())
