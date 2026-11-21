"""Reuse exact query body; route output and enforce global mutation intent."""
import asyncio
import ctypes
import hashlib
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
here = Path(__file__).resolve().parent
output = Path(sys.argv[1]).resolve()
assert output.parent == here and output.name.startswith('attempt-')
config = json.loads((output / 'config.json').read_text())
sys.path.insert(0, str(here))
from runtime import save, claim_termination, EXPECTED
source = here / 'original/confirm_terminal.py'
assert hashlib.sha256(source.read_bytes()).hexdigest() == EXPECTED
kernel = ctypes.WinDLL('kernel32', use_last_error=True)
kernel.GetCurrentProcess.restype = ctypes.c_void_p
kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
assert kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 3)
sys.path.insert(0, str(source.parent))
from confirm_terminal import Query, execute_on_sdk_loop, _Client, _get_sandbox_version, SandboxVersion
from confirm_terminal import APP, APP_NAME, NAME, Empty, pb, TERMINAL, result_metadata

claimed = False
def receipt(value):
    global claimed
    if value['terminate_requests'] and not claimed:
        if config['read_only']:
            raise RuntimeError('Read-only continuation attempted mutation')
        claim_termination(here / 'termination-intent.json', {
            'attempt': output.name, 'sandbox_id': value['sandbox_id'],
            'identity': value.get('identity'), 'utc': value['observed_utc'],
            'meaning': 'Intent persisted before possible request; never repeat'})
        claimed = True
    save(output / 'receipt.json', value)
    if value['terminal'] == 'TERMINAL_CONFIRMED' and not (output / 'terminal-evidence.json').exists():
        with (output / 'terminal-evidence.json').open('x', encoding='utf-8') as stream:
            json.dump(value, stream, indent=2)

class ReadOnlyQuery(Query):
    async def execute(self, client_factory=None):
        prior = config['prior']
        assert prior['identity'] == {'workspace': 'joon56', 'environment': 'main', 'app_id': APP, 'app_name': APP_NAME}
        assert prior['listed']['app_id'] == APP and prior['listed']['name'] == NAME
        sid = prior['sandbox_id']
        assert sid == prior['listed']['id']
        self.receipt.update(sandbox_id=sid, identity=prior['identity'], listed=prior['listed'])
        self.client = await self.call('Client.from_env', lambda _: _Client.from_env(), evidence=True)
        assert self.client._cancellation_context_event_loop is asyncio.get_running_loop()
        workspace = await self.rpc('WorkspaceNameLookup', Empty(), evidence=True)
        if workspace.username != 'joon56':
            raise ValueError('Workspace mismatch')
        v2 = _get_sandbox_version(sid) == SandboxVersion.V2
        suffix = 'V2' if v2 else ''
        result = await self.rpc('SandboxWait' + suffix, pb.SandboxWaitRequest(sandbox_id=sid, timeout=0), v2=v2, evidence=True)
        if result.metadata.app_id and result.metadata.app_id != APP:
            raise ValueError('Wait metadata app mismatch')
        self.receipt['sandbox_result'] = result_metadata(result.result)
        if result.result.status not in TERMINAL:
            raise ValueError('No named terminal result')
        self.receipt.update(terminal='TERMINAL_CONFIRMED', terminal_source='Exact-ID SandboxWait' + suffix)
        self.save()

left = config['deadline_monotonic'] - time.monotonic()
if left <= (1 if config['read_only'] else 30):
    raise TimeoutError('Insufficient child allowance after import')
query = (ReadOnlyQuery if config['read_only'] else Query)(receipt, total=left)
result = execute_on_sdk_loop(query)
print(json.dumps({'terminal': result['terminal'], 'sandbox_id': result['sandbox_id'],
    'terminate_requests': result['terminate_requests'], 'errors': result['errors']}))
raise SystemExit(0 if result['terminal'] == 'TERMINAL_CONFIRMED' else 1)
