"""Actual SDK construction with guarded effects; no loader or build execution."""
import sys
import time
from pathlib import Path
MODE, GATE, NUMBER = sys.argv[1:]
end = time.monotonic() + 5
while not Path(GATE).exists():
    if time.monotonic() >= end:
        raise TimeoutError('CPU gate missing')
    time.sleep(.01)
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import local_guard as guard
guard.install()
import asyncio
import hashlib
import json
import os
import socket
import subprocess
import threading
import traceback

START = time.monotonic()
RESULT = {'mode': MODE, 'checks': []}
EXPECTED = 'fc561eee08f1eafbbeac2cbcc5fa31890ef719bf603c5c7dd1af7aea5e556bcb'


def check(name, condition):
    RESULT['checks'].append({'name': name, 'pass': bool(condition)})
    if not condition:
        raise AssertionError(name)


async def loop_probe():
    await asyncio.sleep(0)
    return {'thread': threading.get_ident(), 'loop': type(asyncio.get_running_loop()).__name__}


def drive(coroutine):
    try:
        coroutine.send(None)
    finally:
        coroutine.close()


def validate_bytes(raw):
    if hashlib.sha256(raw).hexdigest() != EXPECTED:
        raise ValueError('Source hash mismatch')
    return raw


def validate_inventory(rows):
    if len(rows) != 1:
        raise ValueError('Expected one project file')
    local, remote = rows[0]
    if Path(local).resolve() != (HERE / 'controller_core.py').resolve() or str(remote) != '/root/controller_core.py':
        raise ValueError('Source path mismatch')
    return validate_bytes(Path(local).read_bytes())


class Captured(Exception):
    pass


async def capture(image, app):
    # Called only after real SDK image/function/mount construction.
    raise Captured()


async def inventory():
    from sdk_endpoint import Endpoint
    from modal._functions import _Function
    from modal.mount import _Mount, _MountFile, _select_files
    from modal._utils.function_utils import FunctionSourceInfoType
    endpoint = Endpoint(image_builder=capture)
    try:
        await endpoint.build('im-local-source-check', 'LOCAL_PROTOCOL_ONLY', 0)
    except Captured:
        pass
    else:
        raise AssertionError('Build boundary not captured')
    builders = [obj for obj in endpoint.image._deps_() if isinstance(obj, _Function)]
    check('one_real_builder', len(builders) == 1)
    builder = builders[0]
    info = builder._source_info
    check('FILE_only', info._type is FunctionSourceInfoType.FILE)
    check('module_function', (info.module_name, info.function_name, info.implementation_name) ==
          ('controller_core', 'install_pins', 'install_pins'))
    check('defining_file', Path(info._file).resolve() == (HERE / 'controller_core.py').resolve())
    mounts = builder._spec.mounts
    check('spec_deps_equal', mounts == [obj for obj in builder._deps_() if isinstance(obj, _Mount)])
    check('default_client_separate', not mounts[0].is_local())
    rows = []
    for mount in mounts[1:]:
        check('one_file_entry', len(mount.entries) == 1 and isinstance(mount.entries[0], _MountFile))
        rows.extend(_select_files(mount.entries))
    RESULT['builder'] = {'type': info._type.value, 'module': info.module_name,
        'function': info.function_name, 'implementation': info.implementation_name,
        'defining_file': info._file, 'mount_count': len(mounts), 'client_mount': repr(mounts[0]),
        'project_files': [[str(a), str(b)] for a, b in rows],
        'image_dependencies': [type(obj).__name__ for obj in endpoint.image._deps_()],
        'builder_dependencies': [type(obj).__name__ for obj in builder._deps_()]}
    stage = guard.TEMP / ('empty' if MODE == 'baseline' else 'selected')
    stage.mkdir(exist_ok=False)
    if MODE == 'baseline':
        check('original_project_source_omitted', rows == [])
    else:
        raw = validate_inventory(rows)
        for label, invalid in [('missing', []), ('extra', rows + rows),
                               ('wrong_local', [(HERE / 'contract.py', rows[0][1])]),
                               ('wrong_remote', [(rows[0][0], '/root/other.py')])]:
            try:
                validate_inventory(invalid)
            except ValueError:
                check('reject_' + label, True)
            else:
                check('reject_' + label, False)
        try:
            validate_bytes(raw + b'\n')
        except ValueError:
            check('reject_hash', True)
        else:
            check('reject_hash', False)
        (stage / 'controller_core.py').write_bytes(raw)
        RESULT['selected_sha256'] = hashlib.sha256(raw).hexdigest()
        RESULT['stage'] = str(stage)


sync = None
try:
    if MODE == 'boundary':
        RESULT['pre_sdk_loop'] = asyncio.run(loop_probe())
    # -S avoids user .pth/site startup. Add only the existing SDK environment.
    sys.path.append(str(guard.SITE))
    import modal
    from modal.client import _Client
    from modal._image import _Image
    from modal._resolver import Resolver
    from grpclib.client import Channel
    from modal._utils.async_utils import synchronizer
    sync = synchronizer
    guard.block_code(Channel.request, 'rpc')
    guard.block_code(_Image.build, 'image_build')
    guard.block_code(Resolver.load, 'remote_resolution')
    check('SDK1.6.0', modal.__version__ == '1.6.0')
    if MODE == 'boundary':
        RESULT['post_sdk_loop'] = asyncio.run(loop_probe())
        async def worker_probe():
            result = await loop_probe()
            guard.negative('client_auth', lambda: drive(_Client.from_env()))
            return result
        RESULT['sync_worker'] = synchronizer.create_blocking(worker_probe)()
        check('worker_thread_distinct', RESULT['sync_worker']['thread'] != threading.get_ident())
        from synchronicity.async_utils import Runner
        with Runner() as runner:
            RESULT['synchronicity_runner'] = runner.run(loop_probe())
        guard.negative('client_auth', lambda: drive(_Client.from_env()))
        guard.negative('rpc', lambda: Channel.request(None, 'dummy', None, None, None))
        guard.negative('image_build', lambda: drive(_Image.build(None, None)))
        guard.negative('remote_resolution', lambda: drive(Resolver.load(None, None, None)))
        with socket.socket() as sock:
            guard.negative('external_connect', lambda: sock.connect(('203.0.113.1', 9)))
            guard.negative('external_connect', lambda: sock.connect(('127.0.0.1', 9)))
        guard.negative('dns', lambda: socket.getaddrinfo('a040.invalid', 9))
        guard.negative('subprocess', lambda: subprocess.Popen(['A040_NONEXISTENT_DUMMY']))
        guard.negative('credentials', lambda: (guard.TEMP / '.modal.toml').read_bytes())
        from controller_core import install_pins
        guard.negative('installer', lambda: install_pins('DUMMY', 0))
        check('negative_guards', not guard.unexpected)
    else:
        asyncio.run(inventory())
    sync._close_loop()
    check('all_owned_ipc_closed', all(p['closed'] for p in guard.evidence()['pairs']))
    check('no_unexpected_forbidden_attempts', not guard.unexpected)
    RESULT['outcome'] = 'PASS'
except BaseException:
    RESULT['outcome'] = 'FAIL'
    RESULT['error'] = traceback.format_exc()
finally:
    if sync is not None:
        sync._close_loop()
    RESULT['guard'] = guard.evidence()
    RESULT['elapsed_seconds'] = time.monotonic() - START
    (HERE / ('result-' + NUMBER + '.json')).write_text(json.dumps(RESULT, indent=2), encoding='utf-8')
    print(json.dumps(RESULT, indent=2))
sys.exit(0 if RESULT['outcome'] == 'PASS' else 1)
