"""Cooperative local-only test guard; not native egress isolation."""
import asyncio
from asyncio import selector_events, proactor_events
import os
from pathlib import Path
import socket
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
TEMP = ROOT / 'tmp/a040-local-preparation-repair2'
SITE = ROOT / 'tmp/a040-modal-full-path1/sdk-venv/Lib/site-packages'
STDLIB = Path(sys.base_prefix) / 'Lib'
state = threading.local()
events = []
pairs = []
unexpected = []
original_pair = socket.socketpair
pair_code = socket._fallback_socketpair.__code__
pipe_codes = {selector_events.BaseSelectorEventLoop._make_self_pipe.__code__,
              proactor_events.BaseProactorEventLoop._make_self_pipe.__code__}
blocked_codes = {}


class Blocked(PermissionError):
    pass


def deny(kind):
    expected = getattr(state, 'negative', None)
    events.append({'blocked': kind, 'expected': expected, 'thread': threading.get_ident()})
    if expected != kind:
        unexpected.append(kind)
    raise Blocked(kind)


def owned_pair(*args, **kwargs):
    caller = sys._getframe(1)
    if caller.f_code not in pipe_codes or getattr(state, 'pair', False):
        deny('unowned_socketpair')
    state.pair = True
    record = {'pid': os.getpid(), 'thread': threading.get_ident(),
              'loop': type(caller.f_locals['self']).__name__, 'started': time.monotonic()}
    try:
        result = original_pair(*args, **kwargs)
        assert result[0].getsockname() == result[1].getpeername()
        assert result[1].getsockname() == result[0].getpeername()
        record['endpoints'] = [list(s.getsockname()) for s in result]
        pairs.append((record, result))
        return result
    finally:
        state.pair = False


def own_ipc(event, args):
    if not getattr(state, 'pair', False):
        return False
    frame = sys._getframe(1)
    while frame and frame.f_code is not pair_code:
        frame = frame.f_back
    if frame is None:
        return False
    listener = frame.f_locals.get('lsock')
    if listener is None:
        return False
    sock, address = args
    if address[0] not in ('127.0.0.1', '::1'):
        return False
    if event == 'socket.bind':
        return sock is listener and address[1] == 0
    return sock is frame.f_locals.get('csock') and tuple(address[:2]) == listener.getsockname()[:2]


def audit(event, args):
    if event in ('socket.bind', 'socket.connect'):
        if own_ipc(event, args):
            events.append({'ipc': event, 'pid': os.getpid(), 'thread': threading.get_ident()})
        else:
            deny('external_connect' if event == 'socket.connect' else 'external_bind')
    elif event in ('socket.getaddrinfo', 'socket.gethostbyname', 'socket.gethostbyaddr'):
        deny('dns')
    elif event in ('subprocess.Popen', 'os.system', 'os.spawn', 'os.exec'):
        deny('subprocess')
    elif event == 'open' and isinstance(args[0], (str, bytes)):
        path = Path(os.fsdecode(args[0])).resolve()
        name = path.name.lower()
        if name in ('.modal.toml', 'token.json', 'credentials') or '.aws' in path.parts:
            deny('credentials')
        if path.suffix.lower() in ('.parquet', '.npz', '.pt', '.safetensors'):
            deny('protected_file')
        allowed = (HERE, TEMP, SITE, STDLIB, Path(sys.base_prefix) / 'DLLs')
        if not any(path == base or base in path.parents for base in allowed):
            deny('outside_allowed_files')
    elif event == 'import' and args[0].split('.')[0] in ('torch', 'tabicl', 'numpy', 'pandas'):
        deny('model_import')


def trace(frame, event, arg):
    if event != 'call':
        return None
    code = frame.f_code
    if code in blocked_codes:
        deny(blocked_codes[code])
    name = code.co_name
    filename = code.co_filename.replace('\\', '/')
    if name == 'install_pins' and filename.endswith('/controller_core.py'):
        deny('installer')
    if name in ('from_env', '__init__', '_open') and filename.endswith('/modal/client.py'):
        deny('client_auth')
    if name == '_load' and any(filename.endswith('/modal/' + f) for f in ('_image.py', '_functions.py', 'mount.py')):
        deny('remote_loader')
    return None


def arm_trace():
    sys.settrace(trace)
    threading.settrace(trace)


def install():
    for key in list(os.environ):
        if key.startswith(('MODAL_', 'AWS_', 'HF_TOKEN', 'HUGGING_FACE_HUB_TOKEN')):
            del os.environ[key]
    os.environ['MODAL_CONFIG_PATH'] = str(TEMP / 'empty-modal-config.toml')
    assert not Path(os.environ['MODAL_CONFIG_PATH']).exists()
    sys.dont_write_bytecode = True
    socket.socketpair = owned_pair
    sys.addaudithook(audit)
    arm_trace()


def block_code(function, kind):
    function = getattr(function, '__func__', function)
    while function is not None:
        code = getattr(function, '__code__', None)
        if code:
            blocked_codes[code] = kind
        function = getattr(function, '__wrapped__', None)


def negative(kind, operation):
    state.negative = kind
    try:
        operation()
    except Blocked as error:
        assert str(error) == kind
    else:
        raise AssertionError('Forbidden action not blocked: ' + kind)
    finally:
        state.negative = None
        arm_trace()


def evidence():
    records = []
    for record, sockets in pairs:
        item = dict(record)
        item['closed'] = all(sock.fileno() == -1 for sock in sockets)
        records.append(item)
    return {'events': events, 'pairs': records, 'unexpected': unexpected,
            'scope': 'Python guards only; no native/OS security certification'}
