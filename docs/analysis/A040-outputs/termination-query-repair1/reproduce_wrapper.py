"""Replay the original helper AST call through the installed real wrapper."""
import ast
import json
from pathlib import Path
from types import SimpleNamespace
import time
import local_guard
local_guard.install()
from modal._grpc_client import UnaryUnaryWrapper
from modal._utils.async_utils import synchronizer
from modal.exception import InvalidError
from google.protobuf.empty_pb2 import Empty
local_guard.block_sdk_auth()

OLD = Path(__file__).parent.parent / 'sandbox-lifecycle-repair1/confirm_terminal.py'
tree = ast.parse(OLD.read_text(encoding='utf-8'))
node = next(n for n in ast.walk(tree) if isinstance(n, ast.Call) and
            isinstance(n.func, ast.Attribute) and n.func.attr == 'WorkspaceNameLookup')
calls = []
class Transport:
    _snapshotted = False
    async def _get_channel(self, *args):
        return None
    async def _call_unary(self, *args, **kwargs):
        calls.append('transport')
        return Empty()

async def check():
    start = time.monotonic()
    method = SimpleNamespace(name='/fixture/WorkspaceNameLookup')
    wrapper = UnaryUnaryWrapper(method, Transport(), 'fixture://local')
    client = SimpleNamespace(_stub=SimpleNamespace(WorkspaceNameLookup=wrapper))
    try:
        await eval(compile(ast.Expression(node), str(OLD), 'eval'), {'client': client, 'cap': 1, 'Empty': Empty})
    except InvalidError as exc:
        assert str(exc) == 'Retry must be None when timeout is set'
        assert calls == []
        return {'outcome': 'ORIGINAL_FAILURE_REPRODUCED', 'message': str(exc),
                'transport_calls': 0, 'elapsed_seconds': time.monotonic()-start,
                'unexpected_forbidden_actions': local_guard.blocked}
    raise AssertionError('Original call unexpectedly passed')

if __name__ == '__main__':
    result = synchronizer.create_blocking(check)()
    print(json.dumps(result))
