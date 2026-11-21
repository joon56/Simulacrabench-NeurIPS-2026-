"""Actual SDK wrappers/auth manager and protobufs; replace external transport only."""
import asyncio
import base64
import json
from pathlib import Path
from types import SimpleNamespace
import time
import local_guard
local_guard.install()
from modal._grpc_client import UnaryUnaryWrapper
from modal._utils.auth_token_manager import _AuthTokenManager
from modal._utils.async_utils import synchronizer
from modal.client import _Client
from modal.exception import ServiceError
from modal_proto import api_pb2 as pb
local_guard.block_sdk_auth()
from confirm_terminal import Query, APP, APP_NAME, NAME

V1 = 'sb-' + 'a'*22
V2 = 'sb-' + 'b'*26
ENC = base64.urlsafe_b64encode(json.dumps({'exp': time.time()+3600}).encode()).decode().rstrip('=')
FAKE_TOKEN = 'fixture.' + ENC + '.signature'
RPCS = ('WorkspaceNameLookup', 'AppGetInfo', 'SandboxListV2', 'SandboxWait', 'SandboxWaitV2',
        'SandboxTerminate', 'SandboxTerminateV2', 'TaskList', 'WorkspaceBillingSummary')


class Transport:
    _snapshotted = False
    def __init__(self, case, v2=False, clock=None):
        self.case, self.id, self.clock = case, V2 if v2 else V1, clock
        self._cancellation_context_event_loop = asyncio.get_running_loop()
        self.calls, self.terminates, self.token_fetches = [], 0, 0
        self._stub = SimpleNamespace(**{name: UnaryUnaryWrapper(SimpleNamespace(name=name), self, 'fixture://local') for name in RPCS})
        async def fetch(retry):
            self.token_fetches += 1
            return FAKE_TOKEN
        self._auth_token_manager = _AuthTokenManager(self._stub, fetch=fetch)

    async def _get_channel(self, server_url):
        assert server_url == 'fixture://local'
        return None

    async def _call_unary(self, method, request, *, timeout, metadata):
        name = method.name
        assert 0 < timeout <= 14.5
        assert name in RPCS
        self.calls.append(name)
        if name.endswith('V2'):
            assert metadata == [('x-modal-auth-token', FAKE_TOKEN)]
        else:
            assert metadata is None
        if name == 'WorkspaceNameLookup':
            if self.case == 'timeout':
                await asyncio.sleep(1)
            if self.case == 'cancel':
                raise asyncio.CancelledError('fixture cancel')
            if self.case == 'budget':
                self.clock[0] += 100
            return pb.WorkspaceNameLookupResponse(username='wrong' if self.case == 'workspace' else 'joon56')
        if name == 'AppGetInfo':
            assert request.app_id == APP
            return pb.AppGetInfoResponse(info=pb.AppHandleMetadata(app_id=APP,
                description=APP_NAME, environment_name='wrong' if self.case == 'environment' else 'main',
                lifecycle=pb.AppLifecycle(app_state=pb.APP_STATE_STOPPED)))
        if name == 'SandboxListV2':
            assert request.app_id == APP and request.environment_name == ''
            assert isinstance(request, pb.SandboxListRequest)
            if request.before_timestamp or self.case == 'empty':
                return pb.SandboxListResponse()
            status = pb.GenericResult.GENERIC_STATUS_TERMINATED
            if self.case in ('running', 'terminate_timeout', 'unspecified'):
                status = pb.GenericResult.GENERIC_STATUS_UNSPECIFIED
            if self.case == 'unknown_list':
                status = 99
            row = pb.SandboxInfo(id=self.id, app_id='wrong' if self.case == 'app_mismatch' else APP,
                name='wrong' if self.case == 'name' else NAME, created_at=100,
                task_info=pb.TaskInfo(sandbox_id=self.id,
                    started_at=0 if self.case == 'unspecified' else 101,
                    finished_at=0 if self.case in ('running', 'terminate_timeout', 'unspecified') else 102,
                    result=pb.GenericResult(status=status)))
            if self.case == 'unknown_id':
                row.id = 'alien-resource'
            return pb.SandboxListResponse(sandboxes=[row, row] if self.case == 'duplicate' else [row])
        if name.startswith('SandboxWait'):
            assert request.sandbox_id == self.id
            assert name == ('SandboxWaitV2' if self.id == V2 else 'SandboxWait')
            status = pb.GenericResult.GENERIC_STATUS_TERMINATED
            if self.case in ('running', 'terminate_timeout', 'unspecified') and not self.terminates:
                status = pb.GenericResult.GENERIC_STATUS_UNSPECIFIED
            if self.case == 'unknown_wait':
                status = 99
            return pb.SandboxWaitResponse(result=pb.GenericResult(status=status),
                metadata=pb.SandboxHandleMetadata(app_id='wrong' if self.case == 'wait_mismatch' else APP))
        if name.startswith('SandboxTerminate'):
            assert request.sandbox_id == self.id
            assert name == ('SandboxTerminateV2' if self.id == V2 else 'SandboxTerminate')
            self.terminates += 1
            assert self.terminates == 1
            if self.case == 'terminate_timeout':
                await asyncio.sleep(1)
            return pb.SandboxTerminateResponse()
        if name == 'TaskList':
            assert request.app_id == APP
            return pb.TaskListResponse()
        if name == 'WorkspaceBillingSummary':
            if self.case == 'billing_fail':
                raise ServiceError('token=' + FAKE_TOKEN)
            return pb.WorkspaceBillingSummaryResponse(metered_cost=.01, billed_cost=0)
        raise AssertionError('Unexpected transport method')


async def suite():
    started = time.monotonic()
    records = []
    cases = [('terminal', False), ('terminal', True), ('running', False), ('running', True),
        ('empty', False), ('duplicate', False), ('workspace', False), ('environment', False),
        ('app_mismatch', False), ('name', False), ('unknown_id', False), ('unspecified', False),
        ('unknown_list', False), ('unknown_wait', False), ('wait_mismatch', False),
        ('timeout', False), ('cancel', False), ('budget', False), ('terminate_timeout', True),
        ('billing_fail', True)]
    for case, v2 in cases:
        clock = [0.0]
        endpoint = Transport(case, v2, clock)
        snapshots = []
        query = Query(lambda value: snapshots.append(json.loads(json.dumps(value))),
                      clock=(lambda: clock[0]) if case == 'budget' else time.monotonic,
                      call_cap=.01 if case in ('timeout', 'terminate_timeout') else 14.5)
        async def factory():
            return endpoint
        result = await query.run(factory)
        expected_terminal = case in ('terminal', 'running', 'billing_fail')
        assert (result['terminal'] == 'TERMINAL_CONFIRMED') == expected_terminal, (case, result)
        assert result['terminate_requests'] == int(case in ('running', 'terminate_timeout')), (case, result)
        assert endpoint.terminates == result['terminate_requests']
        assert snapshots and result['new_resources'] == result['remote_commands'] == 0
        assert FAKE_TOKEN not in json.dumps(result)
        if expected_terminal:
            assert any(row['terminal'] == 'TERMINAL_CONFIRMED' for row in snapshots)
        if case == 'billing_fail':
            assert result['errors'] and '[REDACTED]' in result['errors'][0]['message']
        if case in ('timeout', 'cancel', 'budget', 'terminate_timeout'):
            before = len(endpoint.calls)
            try:
                await query.rpc('TaskList', pb.TaskListRequest(app_id=APP))
            except TimeoutError:
                pass
            else:
                raise AssertionError('Calls continued after closed budget/cancellation')
            assert len(endpoint.calls) == before
        records.append({'case': case, 'version': 'V2' if v2 else 'V1', 'pass': True,
                        'fake_transport_calls': len(endpoint.calls), 'terminate': endpoint.terminates,
                        'token_fetches': endpoint.token_fetches})
    assert not local_guard.blocked, local_guard.blocked
    # Independent barriers: actual normal client auth and network stay denied.
    try:
        await _Client.from_env()
    except PermissionError:
        pass
    else:
        raise AssertionError('Real auth guard missing')
    import socket
    try:
        socket.getaddrinfo('example.invalid', 443)
    except PermissionError:
        pass
    else:
        raise AssertionError('External network guard missing')
    return {'outcome': 'LOCAL_QUERY_CONTRACT_PASS', 'cases': records,
            'elapsed_seconds': time.monotonic()-started, 'actual_rpc': 0,
            'actual_auth': 0, 'guard_negatives': local_guard.blocked,
            'wrapper': 'Installed UnaryUnaryWrapper.__call__/direct unmodified',
            'auth_manager': 'Installed _AuthTokenManager; fake external token fetch only'}


if __name__ == '__main__':
    result = synchronizer.create_blocking(suite)()
    print(json.dumps(result))
