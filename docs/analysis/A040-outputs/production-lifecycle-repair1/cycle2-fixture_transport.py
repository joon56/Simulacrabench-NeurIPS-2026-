"""Small protocol endpoints; real SDK wrappers, Sandbox/FS/process/streams retained."""
import asyncio
import base64
import json
from pathlib import Path
import time
import grpclib.client
from grpclib import GRPCError, Status
from google.protobuf.empty_pb2 import Empty
from modal.client import _Client
from modal._utils.auth_token_manager import _AuthTokenManager
from modal._utils import task_command_router_client as router
from modal_proto import api_pb2 as pb, task_command_router_pb2 as sr
from contract import REMOTE_DIR, CAP_BYTES, GPU_PLAN, sha

SID='sb-'+'a'*22
APP='ap-'+'b'*22
TASK='ta-'+'c'*22
TOKEN='fixture.'+base64.urlsafe_b64encode(json.dumps({'exp':time.time()+3600}).encode()).decode().rstrip('=')+'.signature'
ACTIVE=None

class Backend:
    def __init__(self, case, name, directory):
        self.case,self.name,self.directory=case,name,Path(directory)
        self.calls=[]; self.commands=[]; self.processes={}; self.files={}
        self.created=0; self.terminated=0; self.stopped=False; self.client=None
        self.stream_reads=0; self.stream_writes=0
        boundary={'outcome':'BOUNDARY_PASS','memory_limit_bytes':CAP_BYTES,'physical_cpu_limit':1}
        for key in ('source_payload_verified','native_network_blocked','swap_disabled','gpu_h100_single','python_pins_match','duplicate_latch_guard','two_logical_affinity'):
            boundary[key]=True
        self.files[REMOTE_DIR+'/boundary-result.json']=json.dumps(boundary).encode()
        self.files[REMOTE_DIR+'/linux-requirements.json']=b'{"protocol_fixture":true}'
        for mode, outcome in [('reference','REFERENCE_PASS'),('candidate','LOCAL_FULL_PATH_PASS')]:
            hashes={}
            names=['unicef','world_bank','unhcr']+(['unhcr-engineering-alpha025','unhcr-final-e041'] if mode=='candidate' else [])
            for name in names:
                raw=json.dumps({'protocol_fixture':True,'mode':mode,'name':name}).encode()
                self.files['/work/tmp/a040-modal-local-integration1/'+mode+'/'+name+'.json']=raw
                hashes[name]=sha(raw)
            result={'outcome':outcome,'full_path_completed':True,'output_counts':{'unicef':17856,'world_bank':39520,'unhcr':132273},'output_hashes':hashes,'protocol_fixture':True}
            resources={'outcome':outcome,'child_exit':0,'elapsed_seconds':.01,'protocol_fixture':True}
            for name,data in [('result.json',json.dumps(result).encode()),('resources.json',json.dumps(resources).encode()),('events.jsonl',b'{}\n'),('resource-samples.jsonl',b'{}\n'),('stdout.txt',b'fixture stdout'),('stderr.txt',b'')]:
                self.files[REMOTE_DIR+'/'+mode+'/'+name]=data

    async def factory(self):
        self.client=Client(self)
        await self.client.initialize()
        return self.client

    async def image_build_response(self, image, app):
        # Existing independent builder-source verification is reused. Only its
        # external completed-image response is supplied; no installer/body runs.
        image._hydrate('im-'+'d'*22, self.client, None)

    async def unary(self, name, req, metadata=None):
        self.calls.append(name)
        if name=='WorkspaceNameLookup': return pb.WorkspaceNameLookupResponse(username='joon56')
        if name=='WorkspaceBillingSummary':
            if self.case=='billing_fail' and self.terminated:
                assert (self.directory/'sandbox-terminal-evidence.json').exists()
                raise GRPCError(Status.INVALID_ARGUMENT,'fixed billing failure')
            return pb.WorkspaceBillingSummaryResponse(metered_cost='0.01009897',billed_cost='0')
        if name=='ImageFromId': return pb.ImageFromIdResponse(image_id=req.image_id)
        if name=='AppGetOrCreate': return pb.AppGetOrCreateResponse(app_id=APP)
        if name=='SecretGetOrCreate': return pb.SecretGetOrCreateResponse(secret_id='st-'+'e'*22)
        if name=='SandboxCreate':
            self.created+=1
            assert self.created==1
            state=json.loads((self.directory/'state.json').read_text())
            assert state['sandbox_resource_possible'] and state['sandbox_reservation_usd']==GPU_PLAN
            assert state['sandbox_create_rpc_intent'] and state['sandbox_name']==self.name+'-gpu'
            if self.case=='timeout': raise TimeoutError('Protocol create response lost')
            if self.case=='cancel': raise asyncio.CancelledError('Protocol cancellation after create')
            return pb.SandboxCreateResponse(sandbox_id='bad-prefix' if self.case=='hydrate' else SID,metadata=pb.SandboxHandleMetadata(app_id=APP))
        if name in ('SandboxGetTaskId','SandboxGetTaskIdV2'): return pb.SandboxGetTaskIdResponse(task_id=TASK)
        if name=='TaskGetCommandRouterAccess':
            return pb.TaskGetCommandRouterAccessResponse(url='http://localhost:1',jwt=TOKEN)
        if name=='AppGetInfo':
            return pb.AppGetInfoResponse(info=pb.AppHandleMetadata(app_id=APP,description=self.name,environment_name='main',lifecycle=pb.AppLifecycle(app_state=pb.APP_STATE_STOPPED if self.stopped else pb.APP_STATE_EPHEMERAL)))
        if name=='SandboxListV2':
            assert metadata==[('x-modal-auth-token',TOKEN)]
            if req.before_timestamp or self.case=='id_lost': return pb.SandboxListResponse()
            return pb.SandboxListResponse(sandboxes=[pb.SandboxInfo(id=SID,app_id=APP,name=self.name+'-gpu',created_at=100,image_id='im-fixture',task_info=pb.TaskInfo(sandbox_id=SID,started_at=101,finished_at=102 if self.terminated else 0,result=pb.GenericResult(status=3 if self.terminated else 0)))])
        if name in ('SandboxWait','SandboxWaitV2'):
            assert req.sandbox_id==SID
            return pb.SandboxWaitResponse(result=pb.GenericResult(status=99 if self.case=='unknown_terminal' else (3 if self.terminated else 0)),metadata=pb.SandboxHandleMetadata(app_id=APP))
        if name in ('SandboxTerminate','SandboxTerminateV2'):
            assert req.sandbox_id==SID
            self.terminated+=1; assert self.terminated==1
            return pb.SandboxTerminateResponse()
        if name=='AppStop': self.stopped=True; return Empty()
        if name=='TaskList': return pb.TaskListResponse()
        if name=='SandboxStdinWrite': return pb.SandboxStdinWriteResponse()
        raise AssertionError('Unregistered fake control-plane RPC: '+name)

    async def control_stream(self,name,request):
        self.calls.append(name)
        if name=='ImageJoinStreaming':
            yield pb.ImageJoinStreamingResponse(result=pb.GenericResult(status=1,data=b'base-protocol'))
        elif name=='SandboxGetLogs':
            yield pb.SandboxGetLogsResponse(eof=True)
        else: raise AssertionError('Unexpected control stream '+name)

    async def router_unary(self,name,request):
        self.calls.append(name)
        if name=='TaskExecStart':
            args=list(request.command_args); self.commands.append(args)
            self.processes[request.exec_id]={'args':args,'stdin':b''}
            return sr.TaskExecStartResponse()
        if name in ('TaskExecWait','TaskExecPoll'):
            args=self.processes[request.exec_id]['args']
            code=9 if self.case=='reference_fail' and args[-1]=='reference' else 0
            return (sr.TaskExecWaitResponse if name=='TaskExecWait' else sr.TaskExecPollResponse)(code=code)
        if name=='TaskExecStdinWrite':
            self.stream_writes+=1
            return sr.TaskExecStdinWriteResponse()
        raise AssertionError('Unregistered router RPC '+name)

class Client(_Client):
    def __init__(self,backend):
        super().__init__('http://localhost',pb.CLIENT_TYPE_CLIENT,None)
        self.backend=backend
    async def initialize(self):
        self._cancellation_context_event_loop=asyncio.get_running_loop()
        self._control_plane_stub=await self._get_stub(self.server_url)
        async def fetch(retry): return TOKEN
        self._auth_token_manager=_AuthTokenManager(self._stub,fetch=fetch)
    async def _get_channel(self,server_url): return None
    async def _call_unary(self,method,request,*,timeout=None,metadata=None):
        return await self.backend.unary(method.name.rsplit('/',1)[-1],request,metadata)
    async def _call_stream(self,method,request,*,metadata=None):
        async for item in self.backend.control_stream(method.name.rsplit('/',1)[-1],request): yield item

class WireStream:
    def __init__(self,name): self.name=name; self.request=None; self.exec_id=None; self.data=b''
    async def __aenter__(self): return self
    async def __aexit__(self,*args): return False
    async def send_message(self,request,end=False):
        if self.name=='TaskExecStdinWriteStream':
            kind=request.WhichOneof('data_or_control') if 'data_or_control' in request.DESCRIPTOR.oneofs_by_name else request.WhichOneof(request.DESCRIPTOR.oneofs[0].name)
            if kind=='start': self.exec_id=request.start.exec_id
            elif kind=='data': self.data+=request.data
            elif kind=='end':
                args=ACTIVE.processes[self.exec_id]['args']; command=json.loads(args[1])
                ACTIVE.files[command['WriteFile']['path']]=self.data; ACTIVE.stream_writes+=1
        else: self.request=request
    async def recv_message(self): return sr.TaskExecStdinWriteStreamResponse()
    def __aiter__(self): return self.items()
    async def items(self):
        assert self.name=='TaskExecStdioRead'
        ACTIVE.stream_reads+=1
        args=ACTIVE.processes[self.request.exec_id]['args']
        if self.request.file_descriptor==sr.TASK_EXEC_STDIO_FILE_DESCRIPTOR_STDERR: data=b''
        elif args[0].endswith('modal-sandbox-fs-tools'):
            command=json.loads(args[1]); data=ACTIVE.files[command['ReadFile']['path']] if 'ReadFile' in command else b''
        else: data=b'protocol stdout\n'
        for start in range(0,len(data),13): yield sr.TaskExecStdioReadResponse(data=data[start:start+13])

def install_router_transport():
    async def no_connection(channel): return None
    router._connect_channel=no_connection
    async def unary(method,request,**kwargs):
        name=method.name.rsplit('/',1)[-1]
        assert name.startswith('TaskExec'), name
        return await ACTIVE.router_unary(name,request)
    def stream(method,**kwargs):
        name=method.name.rsplit('/',1)[-1]
        assert name in ('TaskExecStdioRead','TaskExecStdinWriteStream'),name
        return WireStream(name)
    grpclib.client.UnaryUnaryMethod.__call__=unary
    grpclib.client.UnaryStreamMethod.open=stream
    grpclib.client.StreamUnaryMethod.open=stream
