"""Bounded exact-resource metadata cleanup; no creation, handles, streams or model code."""
import asyncio
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import re
import time

from google.protobuf.empty_pb2 import Empty
from modal.client import _Client
from modal._utils.async_utils import synchronizer
from modal.sandbox import _get_sandbox_version, SandboxVersion
from modal_proto import api_pb2 as pb

APP = 'ap-XiMVzlJgrNrCiFpIN1kB4W'
APP_NAME = 'a040-resume5-20261005-094405'
NAME = APP_NAME + '-gpu'
TERMINAL = frozenset(getattr(pb.GenericResult, name) for name in (
    'GENERIC_STATUS_SUCCESS', 'GENERIC_STATUS_FAILURE', 'GENERIC_STATUS_TERMINATED',
    'GENERIC_STATUS_TIMEOUT', 'GENERIC_STATUS_INIT_FAILURE', 'GENERIC_STATUS_INTERNAL_FAILURE',
    'GENERIC_STATUS_IDLE_TIMEOUT', 'GENERIC_STATUS_MEMORY_MANAGER_EVICTION'))


def result_metadata(result):
    try:
        name = pb.GenericResult.GenericStatus.Name(result.status)
    except ValueError:
        name = 'UNKNOWN'
    return {'status': int(result.status), 'status_name': name, 'exitcode': int(result.exitcode)}


class Query:
    def __init__(self, save, *, clock=time.monotonic, total=120, reserve=30, call_cap=14.5):
        self.clock, self.started = clock, clock()
        self.deadline, self.discovery_end = self.started + total - .5, self.started + total - reserve
        self.call_cap, self.save_callback = call_cap, save
        self.stopped = False
        self.secrets = []
        self.client = None
        self.receipt = {'app_id': APP, 'app_name': APP_NAME, 'sandbox_name': NAME,
            'sandbox_id': None, 'terminal': 'UNCONFIRMED', 'calls': [], 'errors': [],
            'terminate_requests': 0, 'new_resources': 0, 'remote_commands': 0,
            'remote_file_operations': 0}

    def save(self):
        self.receipt.update(observed_utc=datetime.now(timezone.utc).isoformat(),
            observed_kst=datetime.now(timezone(timedelta(hours=9))).isoformat(),
            elapsed_seconds=self.clock()-self.started)
        self.save_callback(self.receipt)

    def safe_message(self, error):
        message = str(error)
        for secret in self.secrets:
            message = message.replace(secret, '[REDACTED]')
        message = re.sub(r'eyJ[\w-]+\.[\w-]+\.[\w-]+', '[REDACTED_JWT]', message)
        message = re.sub(r'(?i)(token|secret|password|authorization)(\s*[:=]\s*)\S+',
                         r'\1\2[REDACTED]', message)
        return message[:300]

    async def call(self, stage, factory, *, evidence=False):
        remaining = (self.deadline if evidence else self.discovery_end) - self.clock()
        if self.stopped or remaining <= 0:
            self.stopped = True
            raise TimeoutError('Aggregate remote window exhausted')
        cap = min(self.call_cap, remaining)
        row = {'method': stage, 'started_utc': datetime.now(timezone.utc).isoformat(), 'cap_seconds': cap}
        self.receipt['calls'].append(row)
        self.save()
        task = asyncio.create_task(factory(cap))
        try:
            done, _ = await asyncio.wait({task}, timeout=cap)
            if not done:
                task.cancel()
                self.stopped = True
                raise TimeoutError('Call deadline: ' + stage)
            value = task.result()
            row['outcome'] = 'RETURNED'
            return value
        except BaseException as exc:
            task.cancel()
            row['outcome'] = type(exc).__name__
            row['message'] = self.safe_message(exc)
            self.stopped = True
            raise
        finally:
            self.save()

    async def rpc(self, name, request, *, v2=False, evidence=False):
        metadata = None
        if v2:
            token = await self.call('AuthTokenManager.get_token',
                lambda _: self.client._auth_token_manager.get_token(), evidence=evidence)
            self.secrets.append(token)
            metadata = [('x-modal-auth-token', token)]
        return await self.call(name, lambda cap: getattr(self.client._stub, name)(
            request, retry=None, timeout=cap, metadata=metadata), evidence=evidence)

    async def rows(self, *, finished):
        # Installed SDK _experimental_list supports both versions and uses this auth path.
        before, found = 0.0, []
        for _ in range(3):
            response = await self.rpc('SandboxListV2', pb.SandboxListRequest(
                app_id=APP, environment_name='', include_finished=finished, before_timestamp=before), v2=True)
            if not response.sandboxes:
                return found
            for row in response.sandboxes:
                if row.app_id != APP:
                    raise ValueError('App-scoped listing identity mismatch')
                if row.name == NAME:
                    found.append(row)
            next_before = response.sandboxes[-1].created_at
            if next_before <= 0 or (before and next_before >= before):
                raise ValueError('Invalid pagination cursor')
            before = next_before
        raise ValueError('Listing incomplete within fixed three-page cap')

    async def execute(self, client_factory=None):
        self.client = await self.call('Client.from_env', lambda _: (client_factory or _Client.from_env)())
        if self.client._cancellation_context_event_loop is not asyncio.get_running_loop():
            raise RuntimeError('SDK managed client loop mismatch')
        workspace = await self.rpc('WorkspaceNameLookup', Empty())
        if workspace.username != 'joon56':
            raise ValueError('Workspace mismatch')
        app = (await self.rpc('AppGetInfo', pb.AppGetInfoRequest(app_id=APP))).info
        if (app.app_id, app.description, app.environment_name) != (APP, APP_NAME, 'main'):
            raise ValueError('App ID/name/environment mismatch')
        self.receipt['identity'] = {'workspace': workspace.username, 'environment': app.environment_name,
                                  'app_id': app.app_id, 'app_name': app.description}
        matches = await self.rows(finished=True)
        if len(matches) != 1:
            raise ValueError('Exact-name listing is empty or ambiguous')
        row = matches[0]
        if not row.id.startswith('sb-') or not row.id[3:].isalnum() or len(row.id[3:]) < 22:
            raise ValueError('Unrecognized Sandbox ID shape')
        version = _get_sandbox_version(row.id)
        v2 = version == SandboxVersion.V2
        suffix = 'V2' if v2 else ''
        self.receipt['sandbox_id'] = row.id
        self.receipt['version'] = version.name
        self.receipt['listed'] = {'id': row.id, 'name': row.name, 'app_id': row.app_id,
            'image_id': row.image_id, 'created_at': row.created_at,
            'started_at': row.task_info.started_at, 'finished_at': row.task_info.finished_at,
            'include_finished': True, 'result': result_metadata(row.task_info.result)}
        self.save()
        status = row.task_info.result.status
        if status not in TERMINAL and status != pb.GenericResult.GENERIC_STATUS_UNSPECIFIED:
            raise ValueError('Unknown listed result status')
        wait = await self.rpc('SandboxWait' + suffix, pb.SandboxWaitRequest(sandbox_id=row.id, timeout=0),
                              v2=v2, evidence=True)
        if wait.metadata.app_id and wait.metadata.app_id != APP:
            raise ValueError('Wait metadata app mismatch')
        self.receipt['sandbox_result'] = result_metadata(wait.result)
        if wait.result.status == pb.GenericResult.GENERIC_STATUS_UNSPECIFIED:
            if status != pb.GenericResult.GENERIC_STATUS_UNSPECIFIED or not (
                    row.task_info.started_at > 0 and row.task_info.finished_at == 0 and
                    row.task_info.sandbox_id == row.id):
                raise ValueError('Unspecified result lacks independent running metadata')
            active = await self.rows(finished=False)
            if len(active) != 1 or active[0].id != row.id:
                raise ValueError('Exact running Sandbox not confirmed')
            if self.receipt['terminate_requests'] or self.clock() >= self.discovery_end:
                raise RuntimeError('Termination allowance unavailable')
            # Persist possible side effect before request; never automatically repeat it.
            self.receipt['terminate_requests'] = 1
            self.save()
            await self.rpc('SandboxTerminate' + suffix, pb.SandboxTerminateRequest(sandbox_id=row.id), v2=v2)
            wait = await self.rpc('SandboxWait' + suffix, pb.SandboxWaitRequest(sandbox_id=row.id, timeout=10),
                                  v2=v2, evidence=True)
            if wait.metadata.app_id and wait.metadata.app_id != APP:
                raise ValueError('Final wait metadata app mismatch')
            self.receipt['sandbox_result'] = result_metadata(wait.result)
        if wait.result.status not in TERMINAL:
            raise ValueError('No named terminal result')
        self.receipt['terminal'] = 'TERMINAL_CONFIRMED'
        self.receipt['terminal_source'] = 'Exact-ID SandboxWait' + suffix
        self.save()  # Billing or App checks cannot erase terminal proof.
        current_app = (await self.rpc('AppGetInfo', pb.AppGetInfoRequest(app_id=APP), evidence=True)).info
        tasks = await self.rpc('TaskList', pb.TaskListRequest(app_id=APP), evidence=True)
        self.receipt['app'] = {'state': int(current_app.lifecycle.app_state), 'tasks': len(tasks.tasks),
            'stopped_task0': current_app.lifecycle.app_state == pb.APP_STATE_STOPPED and not tasks.tasks}
        request = pb.WorkspaceBillingSummaryRequest()
        request.start_timestamp.FromDatetime(datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0))
        bill = await self.rpc('WorkspaceBillingSummary', request, evidence=True)
        self.receipt['billing'] = {'metered_cost': bill.metered_cost, 'billed_cost': bill.billed_cost,
            'metered_breakdown': dict(bill.metered_cost_breakdown),
            'attribution': 'WORKSPACE_AGGREGATE_NOT_TASK_INVOICE', 'posting_delay_unknown': True}

    async def run(self, client_factory=None):
        try:
            await self.execute(client_factory)
        except BaseException as exc:
            self.stopped = True
            self.receipt['errors'].append({'type': type(exc).__name__, 'message': self.safe_message(exc),
                'stage': self.receipt['calls'][-1]['method'] if self.receipt['calls'] else 'entry'})
        finally:
            self.save()
        return self.receipt


def main():
    here = Path(__file__).resolve().parent
    now = datetime.now(timezone.utc)
    with (here / 'remote-window.json').open('x', encoding='utf-8') as stream:
        json.dump({'started_utc': now.isoformat(), 'deadline_utc': (now+timedelta(seconds=120)).isoformat(),
            'discovery_cutoff_utc': (now+timedelta(seconds=90)).isoformat(), 'call_cap_seconds': 15,
            'final_reserve_seconds': 30, 'terminate_max': 1, 'new_resources': 0}, stream, indent=2)
    def save(value):
        (here / 'termination-billing-receipt.json').write_text(json.dumps(value, indent=2), encoding='utf-8')
    query = Query(save)
    result = synchronizer.create_blocking(query.run)()
    print(json.dumps({k: result.get(k) for k in ('terminal', 'sandbox_id', 'version', 'terminate_requests', 'app', 'billing', 'errors', 'elapsed_seconds')}))
    return 0 if result['terminal'] == 'TERMINAL_CONFIRMED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
