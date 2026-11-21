"""Local checks only: isolated config, blocked auth/model/network, owned stdlib IPC."""
import os
from pathlib import Path
import socket
import sys
import threading

blocked = []
ipc = threading.local()
original_pair = socket.socketpair
socket_source = str(Path(socket.__file__).resolve()).lower()


def install(allowed_child=None):
    os.environ['MODAL_CONFIG_PATH'] = str(Path(__file__).parent / 'NO_CREDENTIAL_CONFIG')
    for name in ('MODAL_TOKEN_ID', 'MODAL_TOKEN_SECRET', 'MODAL_OAUTH_REFRESH_TOKEN',
                 'MODAL_OAUTH_CLIENT_ID', 'MODAL_OAUTH_CLIENT_SECRET'):
        os.environ[name] = ''

    def pair(*args, **kwargs):
        ipc.active = True
        try:
            return original_pair(*args, **kwargs)
        finally:
            ipc.active = False

    socket.socketpair = pair

    def audit(event, args):
        deny = False
        if event == 'socket.connect':
            address = args[1]
            frame = sys._getframe(1)
            trusted = False
            while frame:
                if str(Path(frame.f_code.co_filename).resolve()).lower() == socket_source:
                    trusted = frame.f_code.co_name in ('socketpair', '_fallback_socketpair')
                    if trusted:
                        break
                frame = frame.f_back
            deny = not (getattr(ipc, 'active', False) and trusted and
                        isinstance(address, tuple) and address[0] in ('127.0.0.1', '::1'))
        elif event == 'subprocess.Popen':
            # One exact owned CLI child for the parent/child entry regression.
            import subprocess
            expected = subprocess.list2cmdline(allowed_child) if allowed_child else None
            deny = not (expected and args[1] == expected and args[0] in (None, allowed_child[0]))
        elif event in ('socket.getaddrinfo', 'socket.sendto', 'os.system'):
            deny = True
        elif event == 'import':
            deny = args[0].split('.')[0] in ('torch', 'tabicl', 'numpy', 'pandas', 'sklearn')
        elif event == 'open' and isinstance(args[0], (str, bytes)):
            name = os.fsdecode(args[0]).lower()
            deny = name.endswith(('.parquet', '.npz', '.pt', '.safetensors', '.modal.toml'))
        if deny:
            blocked.append(event)
            raise PermissionError('Local guard: ' + event)
    sys.addaudithook(audit)


def block_sdk_auth():
    from modal.client import _Client
    async def denied(*args, **kwargs):
        blocked.append('real_client_auth_or_transport')
        raise PermissionError('Real SDK client forbidden in local checks')
    _Client.from_env = classmethod(denied)
    _Client._call_unary = denied
    _Client._call_stream = denied
