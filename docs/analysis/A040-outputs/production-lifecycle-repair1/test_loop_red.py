"""Original independent-loop defect at actual SDK handle/stream hydration."""
import asyncio
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import local_guard
local_guard.install()
from modal.client import _Client
from modal.sandbox import _Sandbox
from modal_proto import api_pb2 as pb
local_guard.block_sdk_auth()

async def reproduce():
    client = _Client('http://localhost', pb.CLIENT_TYPE_CLIENT, None)
    client._cancellation_context_event_loop = asyncio.get_running_loop()
    try:
        _Sandbox._new_hydrated('sb-aaaaaaaaaaaaaaaaaaaaaa', client, pb.SandboxHandleMetadata(app_id='ap-local'))
    except AssertionError:
        return {'outcome':'ORIGINAL_HYDRATION_LOOP_FAIL_REPRODUCED','actual_sdk_hydration':True,'auth_rpc':0}
    raise AssertionError('Expected original stream-constructor loop rejection')

print(json.dumps(asyncio.run(reproduce())))
