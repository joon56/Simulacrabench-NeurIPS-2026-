"""New actual-SDK production lifecycle integration; no real endpoints/models."""
import asyncio
from dataclasses import asdict
import json
from pathlib import Path
import runpy
import sys
import time
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import local_guard
local_guard.install()
from modal._utils.async_utils import synchronizer
from modal.sandbox import _Sandbox
from modal.sandbox_fs import _SandboxFilesystem
from modal.io_streams import _StreamReader, _StreamWriter
local_guard.block_sdk_auth()
import fixture_transport as wire
wire.install_router_transport()
from contract import Plan, MODULES, GPU_PLAN, sha
from payload import Payload
from sdk_endpoint import Endpoint
from live_worker import Context, cleanup
import live_launcher

ROOT=HERE.parents[3]
WORK=ROOT/'tmp/a040-production-lifecycle-repair1'
CYCLE=sys.argv[1]
CASES=sys.argv[2:] or ['normal','hydrate','id_lost','timeout','cancel','reference_fail','unknown_terminal','billing_fail']
manifest=json.loads((HERE/'source-manifest.json').read_text())
records=[]
for case in CASES:
    name='a040-local-'+CYCLE+'-'+case.replace('_','-')
    directory=WORK/name
    backend=wire.Backend(case,name,directory)
    wire.ACTIVE=backend
    now=time.time()
    plan=Plan('LOCAL_PROTOCOL_FIXTURE',name,'im-fixturebase',sha(b'base-protocol'),now+2400,now+4800,now+7200,
              operation_timeout=1,build_timeout=3,cleanup_timeout=2,cancel_grace=.01,poll_seconds=.001)
    config={'plan':asdict(plan),'source_manifest_sha256':sha((HERE/'source-manifest.json').read_bytes()),
            'extra_files':[dict(r,path='docs/analysis/A040-outputs/production-lifecycle-repair1/'+r['path'],reason='protocol source closure') for r in manifest['files']]}
    config_path=WORK/(name+'.json'); config_path.write_text(json.dumps(config))
    contexts=[]
    def factory(config,plan):
        raw=b'bounded protocol bytes'
        row={'path':'protocol.txt','bytes':len(raw),'sha256':sha(raw)}
        payload=Payload([row],[],lambda _:raw,lambda _:b'',plan.scope)
        endpoint=Endpoint(client_factory=backend.factory,image_builder=backend.image_build_response)
        context=Context(directory,plan,endpoint,payload,'PROTOCOL_PINS_NOT_INSTALLED')
        contexts.append(context); return context
    # Same argument parser, child branch, source gates and dispatch as production.
    code=live_launcher.main([str(config_path),'--child'],context_factory=factory)
    context=contexts[0]
    result=json.loads((directory/'result.json').read_text())
    term=json.loads((directory/'termination-receipt.json').read_text())
    if case=='normal':
        assert code==0 and result['outcome']=='LOCAL_PROTOCOL_PATH_PASS',result
        assert type(context.endpoint.sandbox) is _Sandbox
        assert type(context.endpoint.sandbox.filesystem) is _SandboxFilesystem
        async def verify_objects():
            recovered=await _Sandbox.from_id(wire.SID,client=backend.client)
            assert type(recovered) is _Sandbox
            assert isinstance(synchronizer._translate_in(recovered.stdout),_StreamReader)
            assert isinstance(synchronizer._translate_in(recovered.stdin),_StreamWriter)
            await recovered.detach()
            # Instance guard intercepts before a second actual create/terminate RPC.
            try: await context.endpoint.sandbox_create(name+'-gpu')
            except RuntimeError as error: assert 'Duplicate Sandbox mutation' in str(error)
            else: raise AssertionError('Duplicate create allowed')
            from modal_proto import api_pb2 as pb
            try: await backend.client._stub.SandboxTerminate(pb.SandboxTerminateRequest(sandbox_id=wire.SID))
            except RuntimeError as error: assert 'Duplicate Sandbox mutation' in str(error)
            else: raise AssertionError('Duplicate termination allowed')
            await context.endpoint.sandbox.detach()
        synchronizer.create_blocking(verify_objects)()
        assert backend.created==backend.terminated==1
        assert backend.stream_reads>0 and backend.stream_writes>0
        try: live_launcher.main([str(config_path),'--child'],context_factory=factory)
        except FileExistsError: pass
        else: raise AssertionError('Attempt ownership latch reused')
    else:
        assert code==1 and result['outcome']!='LOCAL_PROTOCOL_PATH_PASS',result
        if case in ('hydrate','timeout','cancel'):
            assert context.endpoint.sandbox is None and term['termination']=='TERMINAL_TASK0_CONFIRMED',term
            assert backend.created==backend.terminated==1
            assert result['sandbox_resource_possible'] and context.costs.gpu_reservation==GPU_PLAN
        if case in ('id_lost','unknown_terminal'):
            assert term['termination']=='UNCONFIRMED' and 'sandbox_terminal' not in term,term
        if case=='reference_fail':
            assert not any(args[-1]=='candidate' for args in backend.commands)
        if case=='billing_fail':
            assert (directory/'sandbox-terminal-evidence.json').exists()
            assert term['sandbox_terminal']['status']==3 and term['errors']
    records.append({'case':case,'pass':True,'fake_creates':backend.created,'fake_terminates':backend.terminated,
        'outcome':result['outcome'],'termination':term['termination'],'stream_reads':backend.stream_reads,'stream_writes':backend.stream_writes})
    (HERE/(CYCLE+'-case-results.json')).write_text(json.dumps(records,indent=2))
assert not local_guard.blocked,local_guard.blocked
print(json.dumps({'outcome':'LOCAL_PRODUCTION_LIFECYCLE_CASES_PASS','cases':records,
    'actual_auth_rpc_model':0,'scope':'Protocol bytes/count metadata only; no real predictions'}))
