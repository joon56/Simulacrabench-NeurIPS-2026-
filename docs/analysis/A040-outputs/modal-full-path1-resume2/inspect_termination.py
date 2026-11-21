"""Read-only exact owned IDs after first build error. Never creates resources."""
import asyncio
import dataclasses
from datetime import datetime, timezone
import json
from pathlib import Path
from modal.client import _Client
from modal._workspace import _Workspace
from modal_proto import api_pb2
from google.protobuf.json_format import MessageToDict

HERE = Path(__file__).resolve().parent
APP = 'ap-CJkQ7byYW3D872nirY6KRM'
IMAGE = 'im-eWgRNij0VH6mzozlOzEyxy'

async def main():
    client = await _Client.from_env()
    receipt = dict(utc=datetime.now(timezone.utc).isoformat(), app_id=APP, image_id=IMAGE,
                   new_resource_requests=0, scientific_requests=0)
    info = await client._stub.AppGetInfo(api_pb2.AppGetInfoRequest(app_id=APP))
    receipt['app_lifecycle'] = MessageToDict(info.info.lifecycle, preserving_proto_field_name=True)
    tasks = await client._stub.TaskList(api_pb2.TaskListRequest(app_id=APP))
    receipt['owned_tasks'] = [MessageToDict(t, preserving_proto_field_name=True) for t in tasks.tasks]
    entries = []
    async def image_status():
        request = api_pb2.ImageJoinStreamingRequest(image_id=IMAGE, timeout=3)
        async for row in client._stub.ImageJoinStreaming.unary_stream(request):
            if row.result.status:
                receipt['image_result'] = MessageToDict(row.result, preserving_proto_field_name=True)
            for entry in row.task_logs:
                if entry.data:
                    entries.append(entry.data)
    try:
        await asyncio.wait_for(image_status(), 8)
    except Exception as exc:
        receipt['image_status_read_error_type'] = type(exc).__name__
    receipt['image_logs'] = entries
    workspace = _Workspace.from_context(client=client)
    await workspace.hydrate()
    if workspace.name != 'joon56':
        raise RuntimeError('Workspace mismatch during cleanup')
    receipt['billing_summary'] = dataclasses.asdict(await workspace.billing.summary())
    with (HERE/'termination-receipt.json').open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, indent=2, default=str)
    print(json.dumps({'app_lifecycle': receipt['app_lifecycle'], 'owned_task_count':len(receipt['owned_tasks']),
                      'image_result':receipt.get('image_result'), 'billing':receipt['billing_summary']},default=str))

asyncio.run(asyncio.wait_for(main(), 35))
