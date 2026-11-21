"""Only external service/auth/transfer responses; actual SDK build/resolver kept."""
import asyncio
from datetime import datetime,timezone
import json
from pathlib import Path
import time
import fixture_transport as wire
from modal_proto import api_pb2 as pb
from contract import sha

HERE=Path(__file__).resolve().parent
BUILT='im-'+'d'*22
FUNCTION='fu-'+'f'*22
SOURCE_MOUNT='mo-'+'g'*22
CLIENT_MOUNT='mo-'+'h'*22

class Backend(wire.Backend):
    def __init__(self,case,name,directory,evidence):
        super().__init__('normal',name,directory)
        self.boundary_case=case
        self.evidence=Path(evidence)
        self.started=time.perf_counter()
        self.timeline=[]; self.source_files=[]; self.function_definition=None
        self.mount_source=(HERE/'controller_core.py').read_bytes()

    def record(self,event,**values):
        row={'event':event,'utc':datetime.now(timezone.utc).isoformat(),
             'elapsed_seconds':time.perf_counter()-self.started,**values}
        self.timeline.append(row)
        with self.evidence.open('a',encoding='utf-8') as stream:
            stream.write(json.dumps(row)+'\n')

    async def unary(self,name,request,metadata=None):
        self.record('rpc_response_boundary',method=name)
        if name=='EnvironmentGetOrCreate':
            return pb.EnvironmentGetOrCreateResponse(environment_id='en-'+'e'*22,
                metadata=pb.EnvironmentMetadata(name='main',settings=pb.EnvironmentSettings(image_builder_version='2025.06')))
        if name=='MountBatchedCheckExistence':
            assert list(request.sha256_hex_hashes)==[sha(self.mount_source)],'Unexpected source mount bytes'
            return pb.MountBatchedCheckExistenceResponse(missing_sha256_hex_hashes=request.sha256_hex_hashes)
        if name=='MountPutFile':
            assert request.data==self.mount_source and request.sha256_hex==sha(self.mount_source)
            assert not request.data_blob_id
            self.record('exact_builder_source_bytes',sha256=request.sha256_hex,bytes=len(request.data))
            return pb.MountPutFileResponse(exists=True)
        if name=='MountGetOrCreate':
            if request.files:
                rows=[{'filename':r.filename,'sha256':r.sha256_hex} for r in request.files]
                assert len(rows)==1 and rows[0]['filename']=='/root/controller_core.py',rows
                assert rows[0]['sha256']==sha(self.mount_source)
                self.source_files=rows
                self.record('project_mount',files=rows)
                return pb.MountGetOrCreateResponse(mount_id=SOURCE_MOUNT)
            assert request.deployment_name.startswith('modal-client-'),request.deployment_name
            self.record('sdk_client_mount_reference',name=request.deployment_name)
            return pb.MountGetOrCreateResponse(mount_id=CLIENT_MOUNT)
        if name=='FunctionPrecreate':
            assert request.function_name=='install_pins'
            return pb.FunctionPrecreateResponse(function_id=FUNCTION)
        if name=='FunctionCreate':
            function=request.function
            assert function.module_name=='controller_core' and function.function_name=='install_pins'
            assert function.is_builder_function and SOURCE_MOUNT in function.mount_ids
            assert set(function.mount_ids)<={SOURCE_MOUNT,CLIENT_MOUNT}
            assert not function.function_serialized
            # Keep evidence as plain metadata, not a borrowed protobuf submessage
            # owned by a transient request arena across async RPC lifetimes.
            self.function_definition={'module':function.module_name,'function':function.function_name,
                                      'mount_ids':list(function.mount_ids)}
            self.record('builder_function',module=function.module_name,function=function.function_name,
                mount_ids=list(function.mount_ids),image_id=function.image_id,timeout=function.timeout_secs)
            data=pb.FunctionData(module_name=function.module_name,function_name=function.function_name,
                ranked_functions=[pb.FunctionData.RankedFunction(rank=0,function=function)])
            return pb.FunctionCreateResponse(function_id=FUNCTION,function=function,function_data=data)
        if name=='ImageGetOrCreate':
            assert request.build_function_id==FUNCTION and self.function_definition is not None
            assert self.source_files
            chains=[]
            for task in asyncio.all_tasks():
                current=task.get_coro(); names=[]
                while current is not None:
                    code=getattr(current,'cr_code',getattr(current,'gi_code',None))
                    if code is not None: names.append({'file':code.co_filename.replace('\\','/'),'function':code.co_name})
                    current=getattr(current,'cr_await',getattr(current,'gi_yieldfrom',None))
                if any(r['file'].endswith('/modal/_image.py') and r['function']=='build' for r in names): chains.append(names)
            assert chains,'Actual Image.build missing from live SDK await chain'
            assert any(any(r['file'].endswith('/sdk_endpoint.py') and r['function']=='_build' for r in c) for c in chains)
            self.record('sdk_image_build_chain',chains=chains)
            self.record('image_build_requested',image_id=BUILT,base_images=[r.image_id for r in request.image.base_images])
            return pb.ImageGetOrCreateResponse(image_id=BUILT)
        if name=='SandboxCreate':
            assert request.definition.image_id==BUILT
            self.record('sandbox_create_started',image_id=request.definition.image_id)
            response=await super().unary(name,request,metadata)
            if self.boundary_case=='stall':
                try:
                    await asyncio.Future()
                except asyncio.CancelledError:
                    self.record('create_cancellation_observed')
                    raise
            return response
        return await super().unary(name,request,metadata)

    async def control_stream(self,name,request):
        if name=='ImageJoinStreaming' and request.image_id==BUILT:
            self.record('builder_result',image_id=BUILT,status='FAILURE' if self.boundary_case=='builder_fail' else 'SUCCESS')
            yield pb.ImageJoinStreamingResponse(result=pb.GenericResult(
                status=2 if self.boundary_case=='builder_fail' else 1,
                exception='fixed protocol builder failure' if self.boundary_case=='builder_fail' else ''),
                metadata=pb.ImageMetadata(image_builder_version='2025.06'))
        else:
            async for response in super().control_stream(name,request):
                yield response
