"""Execute only AST-extracted SDK task-context method against local mocks.

No modal import, authentication, connection or RPC. SDK source is permitted input.
"""
import ast
import asyncio
import __future__
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace as NS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
path = ROOT / "tmp/a040-modal-full-path1/sdk-venv/Lib/site-packages/modal/client.py"
source = path.read_text(encoding="utf-8")
cls = next(n for n in ast.parse(source).body if isinstance(n, ast.ClassDef) and n.name == "_Client")
node = next(n for n in cls.body if isinstance(n, ast.AsyncFunctionDef) and n.name == "_call_safely")
warnings = []
namespace = {"asyncio": asyncio, "logger": NS(warning=warnings.append), "ClientClosed": RuntimeError}
exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), "exec",
             flags=__future__.annotations.compiler_flag), namespace)

async def check():
    loop = asyncio.get_running_loop()
    created = []
    def create_task(coro):
        task = asyncio.create_task(coro)
        created.append(task)
        return task
    client = NS(is_closed=lambda: False, _cancellation_context_event_loop=loop,
                _cancellation_context=NS(create_task=create_task))
    async def rpc_mock():
        assert asyncio.get_running_loop() is loop
        return "fake-response"
    method = namespace["_call_safely"]
    assert await method(client, rpc_mock(), "fake.AppStop") == "fake-response"
    assert len(created) == 1 and warnings == []
    client._cancellation_context_event_loop = object()  # No actual cross-thread/network call.
    assert await method(client, rpc_mock(), "fake.AppStop") == "fake-response"
    assert len(created) == 1 and len(warnings) == 1 and "outside of task context" in warnings[0]
    client.is_closed = lambda: True
    coro = rpc_mock()
    try:
        await method(client, coro, "fake.AppStop")
    except RuntimeError:
        assert coro.cr_frame is None
    else:
        raise AssertionError("Closed client was accepted")

asyncio.run(check())
print(json.dumps({"passed": True, "actual_sdk_ast_method": "_Client._call_safely",
    "source_sha256": hashlib.sha256(source.encode()).hexdigest(), "same_loop_task_context": True,
    "different_loop_warning_reproduced": True, "closed_client_rejected": True,
    "sdk_imports": 0, "real_rpc_calls": 0,
    "limit": "Mock method contract; observed historical hang root cause remains unproven"}))
