"""Producer-derived output-envelope regression; no models or real output arrays."""
import ast
import asyncio
import json
import os
from pathlib import Path
import socket
import sys
import time
import traceback
from types import SimpleNamespace

START = time.monotonic()
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = ROOT / 'docs/analysis/A040-outputs/modal-local-integration1'
MODE, OUT = sys.argv[1], Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=False)
sys.path.insert(0, str(HERE))
sys.dont_write_bytecode = True
LOOP = asyncio.new_event_loop()  # Windows local self-pipe before network guards.
asyncio.set_event_loop(LOOP)
BLOCKED = []


def deny(*args, **kwargs):
    BLOCKED.append('forbidden_endpoint')
    raise PermissionError('Local output contract only')


def audit(name, args):
    if name in ('socket.connect', 'socket.getaddrinfo', 'socket.sendto', 'subprocess.Popen', 'os.system', 'os.posix_spawn'):
        deny()
    if name == 'import' and args[0].split('.')[0] in ('torch', 'tabicl', 'numpy', 'pandas', 'sklearn', 'modal'):
        deny()
    if name == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
        path = os.fsdecode(args[0]).replace('\\', '/').lower()
        if any(s in path for s in ('.modal.toml', '/.aws/', '/.ssh/', '/staging/', '/acquisition/', '/vaf/', '/tmp/a040-full-path-', '/tmp/a040-local-technical/', '/docs/analysis/a040-outputs/full-path-resume1/')) or path.endswith(('.parquet', '.npz', '.ckpt')):
            deny()


sys.addaudithook(audit)
socket.create_connection = socket.socket.connect = socket.socket.connect_ex = deny
socket.getaddrinfo = socket.socket.sendto = deny

from contract import Plan, REMOTE_DIR, CAP_BYTES, sha
from payload import Payload
from live_worker import Context
from modal_proto import api_pb2 as pb
import sandbox_stage as stage

METADATA_PATH = HERE / 'producer-metadata.json'
assert sha(METADATA_PATH.read_bytes()) == '0f77640aa495ac6ec66b98ce2a7c933bcb302dfa7345b5b107fe62a2a9b5ec12'
metadata = json.loads(METADATA_PATH.read_text(encoding='utf-8-sig'))
# Expectations originate in the producer, never stage constants.
COUNTS = {row['instrument']: row['vectors'] for row in metadata['fixture_instrument_vectors']}
assert COUNTS == metadata['reference_counts'] == {'unicef': 17856, 'world_bank': 39520, 'unhcr': 132273}
assert set(metadata['reference_hash_keys']) == set(COUNTS)
producer_raw = (OLD / 'linux_runner.py').read_bytes()
assert producer_raw == (HERE / 'linux_runner.py').read_bytes()
tree = ast.parse(producer_raw.decode('utf-8-sig'))
extra_loops = [n for n in ast.walk(tree) if isinstance(n, ast.For) and isinstance(n.target, ast.Tuple)
               and [x.id for x in n.target.elts if isinstance(x, ast.Name)] == ['label', 'vectors']]
assert len(extra_loops) == 1
EXTRAS = [ast.literal_eval(pair.elts[0]) for pair in extra_loops[0].iter.elts]
assert EXTRAS == ['unhcr-engineering-alpha025', 'unhcr-final-e041']
assert "for name in ('unicef','world_bank','unhcr')" in producer_raw.decode('utf-8-sig')
CASES = []


class Filesystem:
    def __init__(self):
        self.data, self.reads = {}, []
    async def read_bytes(self, path):
        self.reads.append(path)
        return self.data[path]
    async def write_bytes(self, data, path):
        self.data[path] = data


class Stream:
    async def read(self):
        return 'PROTOCOL_FIXTURE_ONLY'


class Process:
    stdout, stderr = Stream(), Stream()
    async def wait(self):
        return 0


def populate(filesystem, mode, fault=''):
    counts = dict(COUNTS)
    names = list(COUNTS) + (EXTRAS if mode == 'candidate' else [])
    hashes = {name: sha(b'[]') for name in names}
    if fault == 'wb_hash':
        hashes['wb'] = hashes.pop('world_bank')
    elif fault == 'wb_count':
        counts['wb'] = counts.pop('world_bank')
    elif fault == 'missing_hash':
        hashes.pop('world_bank')
    elif fault == 'extra_hash':
        hashes['unexpected'] = sha(b'[]')
    elif fault == 'missing_count':
        counts.pop('world_bank')
    elif fault == 'extra_count':
        counts['unexpected'] = 0
    elif fault == 'same_total_wrong_counts':
        counts['unicef'] += 1
        counts['world_bank'] -= 1
        assert sum(counts.values()) == sum(COUNTS.values())
    elif fault == 'extra_candidate_counts':
        counts[EXTRAS[0]] = 0
        counts[EXTRAS[1]] = 0
    elif fault == 'noninteger_count':
        counts['unicef'] = float(counts['unicef'])
    elif fault == 'bad_hash':
        hashes['world_bank'] = '0'*64
    outcome = 'REFERENCE_PASS' if mode == 'reference' else 'LOCAL_FULL_PATH_PASS'
    result = dict(outcome=outcome, mode=mode, full_path_completed=True,
                  output_counts=counts, output_hashes=hashes, actual_effect_evidence=False,
                  evidence_scope='SMALL_PROTOCOL_FIXTURE_NOT_PREDICTIONS')
    resources = dict(outcome=outcome, child_exit=0, elapsed_seconds=.01,
                     evidence_scope='SMALL_PROTOCOL_FIXTURE_NOT_RESOURCE_MEASUREMENT')
    for name, value in {'result.json': json.dumps(result).encode(), 'resources.json': json.dumps(resources).encode(),
                        'events.jsonl': b'', 'resource-samples.jsonl': b'', 'stdout.txt': b'', 'stderr.txt': b''}.items():
        filesystem.data[REMOTE_DIR + '/' + mode + '/' + name] = value
    for name in hashes:
        if fault == 'missing_file' and name == 'world_bank':
            continue
        if fault == 'missing_extra_file' and name == EXTRAS[0]:
            continue
        filesystem.data['/work/tmp/a040-modal-local-integration1/' + mode + '/' + name + '.json'] = b'[]'
    return result


class Endpoint:
    def __init__(self, fault='', failed_mode='reference'):
        self.fault, self.failed_mode = fault, failed_mode
        self.calls = []
        self.sandbox = SimpleNamespace(filesystem=Filesystem(), exec=self.exec)
    async def sandbox_create(self, name):
        self.calls.append('sandbox_recorded')
        return 'sb-PROTOCOL-ONLY'
    async def billing(self):
        return pb.WorkspaceBillingSummaryResponse(metered_cost='0', billed_cost='0')
    async def exec(self, *args, **kwargs):
        assert args[:4] == ('python', '-I', '-B', '-u')
        if args[4].endswith('/linux_boundary.py'):
            self.calls.append('boundary_recorded')
            value = dict(outcome='BOUNDARY_PASS', source_payload_verified=True, native_network_blocked=True,
                swap_disabled=True, gpu_h100_single=True, python_pins_match=True, duplicate_latch_guard=True,
                two_logical_affinity=True, memory_limit_bytes=CAP_BYTES, physical_cpu_limit=1,
                evidence_scope='PROTOCOL_FIXTURE_ONLY')
            self.sandbox.filesystem.data[REMOTE_DIR + '/boundary-result.json'] = json.dumps(value).encode()
            self.sandbox.filesystem.data[REMOTE_DIR + '/linux-requirements.json'] = b'[]'
        else:
            assert args[4] == REMOTE_DIR + '/linux_watchdog.py'
            mode = args[5]
            self.calls.append(mode)
            populate(self.sandbox.filesystem, mode, self.fault if mode == self.failed_mode else '')
        return Process()


def context(name, fault='', failed_mode='reference'):
    now = time.time()
    plan = Plan('LOCAL_PROTOCOL_FIXTURE', 'a040-output-protocol', 'im-PROTOCOL', '0'*64,
                now+1500, now+5000, now+7000)
    endpoint = Endpoint(fault, failed_mode)
    row = {'path': 'tiny.txt', 'bytes': 1, 'sha256': sha(b'_')}
    payload = Payload([row], [], lambda path: b'_', lambda path: b'_', plan.scope)
    ctx = Context(OUT / name, plan, endpoint, payload, '')
    ctx.directory.mkdir()
    ctx.state['image_id'] = 'im-PROTOCOL-ONLY'
    return ctx


async def run_cases():
    if MODE == 'reproduce':
        assert sha((HERE / 'sandbox_stage.py').read_bytes()) == '8e0cfd474416aa586af9f7ec936c20c7d4fbf0c1888d2d770cc10c4d038027d0'
        ctx = context('old_producer_mismatch')
        envelope = populate(ctx.endpoint.sandbox.filesystem, 'reference')
        try:
            await stage.export_mode(ctx, 'reference')
        except RuntimeError as exc:
            assert str(exc) == 'Output export manifest mismatch'
            CASES.append(dict(name='old_exporter_rejects_canonical_producer', expected_failure=str(exc),
                              envelope=envelope, pass_expected_reproduction=True))
        else:
            raise AssertionError('Old mismatch was not reproduced')
        return
    assert MODE == 'verify'
    ctx = context('normal_pair')
    await stage.execute(ctx)
    assert [x for x in ctx.endpoint.calls if x in ('reference', 'candidate')] == ['reference', 'candidate']
    for mode in ('reference', 'candidate'):
        files = {p.stem for p in (ctx.directory / mode / 'outputs').iterdir()}
        assert files == set(COUNTS) | (set(EXTRAS) if mode == 'candidate' else set())
        assert (ctx.directory / mode / 'outputs/world_bank.json').read_bytes() == b'[]'
        assert not (ctx.directory / mode / 'outputs/wb.json').exists()
        result = json.loads((ctx.directory / mode / 'result.json').read_text())
        assert result['output_counts'] == COUNTS and sum(result['output_counts'].values()) == 189649
    CASES.append(dict(name='normal_pair_canonical_keys_paths_counts', passed=True, calls=ctx.endpoint.calls))
    faults = ('wb_hash', 'wb_count', 'missing_hash', 'extra_hash', 'missing_count', 'extra_count',
              'same_total_wrong_counts', 'noninteger_count', 'bad_hash', 'missing_file')
    for fault, mode in [(f, 'reference') for f in faults] + [('extra_candidate_counts', 'candidate'),
                ('missing_extra_file', 'candidate'), ('missing_hash', 'candidate')]:
        ctx = context(fault + '_' + mode, fault, mode)
        try:
            await stage.execute(ctx)
        except (RuntimeError, ValueError, KeyError) as exc:
            expected_calls = ['reference'] if mode == 'reference' else ['reference', 'candidate']
            assert [x for x in ctx.endpoint.calls if x in ('reference', 'candidate')] == expected_calls
            assert mode not in ctx.state
            CASES.append(dict(name=fault + '_' + mode, passed=True, rejection=str(exc), calls=ctx.endpoint.calls))
        else:
            raise AssertionError('Invalid output accepted: ' + fault)


record = dict(mode=MODE, scope='LOCAL_OUTPUT_PROTOCOL_FIXTURE', cases=CASES,
              producer_counts=COUNTS, candidate_extra_hashes=EXTRAS,
              producer_metadata_extract_sha256=sha(METADATA_PATH.read_bytes()),
              producer_runner_sha256=sha(producer_raw), actual_arrays_opened=0,
              actual_rpc=0, actual_science=0, actual_linux_boundary=0, model_imports=0)
code = 1
try:
    LOOP.run_until_complete(run_cases())
    assert not BLOCKED
    record['outcome'] = 'EXPECTED_MISMATCH_REPRODUCED' if MODE == 'reproduce' else 'FOCUSED_OUTPUT_REGRESSION_PASS'
    code = 0
except BaseException:
    record.update(outcome='FOCUSED_OUTPUT_REGRESSION_FAIL', traceback=traceback.format_exc())
finally:
    record.update(elapsed_seconds=time.monotonic()-START, blocked_attempts=BLOCKED, cases_completed=len(CASES))
    (OUT / 'result.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    print(json.dumps({k:v for k,v in record.items() if k != 'cases'}), flush=True)
    os._exit(code)
