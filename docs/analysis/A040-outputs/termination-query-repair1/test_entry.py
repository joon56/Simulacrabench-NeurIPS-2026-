"""Affected CLI loop-dispatch boundary; real SDK synchronizer, no real endpoints."""
import json
import local_guard
local_guard.install()
from modal._utils.async_utils import synchronizer
local_guard.block_sdk_auth()
from confirm_terminal import Query, execute_on_sdk_loop
from tests_query import Transport

q = Query(lambda _: None)
try:
    synchronizer.create_blocking(q.run)
except Exception as exc:
    assert 'not a class or a callable' in str(exc)
else:
    raise AssertionError('Original bound-method error absent')

async def factory():
    return Transport('terminal', True)

result = execute_on_sdk_loop(q, factory)
assert result['terminal'] == 'TERMINAL_CONFIRMED', result
assert result['terminate_requests'] == 0
assert not local_guard.blocked
print(json.dumps({'outcome': 'ENTRY_DISPATCH_PASS', 'original_reproduced': True, 'actual_auth_rpc': 0}))
