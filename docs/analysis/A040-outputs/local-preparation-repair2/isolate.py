"""Import only the SDK-selected file in a fresh -I/-S process."""
import sys
import time
from pathlib import Path
MODE, GATE, NUMBER = sys.argv[1:]
end = time.monotonic() + 5
while not Path(GATE).exists():
    if time.monotonic() >= end:
        raise TimeoutError('CPU gate missing')
    time.sleep(.01)
import hashlib
import importlib
import json
import os
import traceback
HERE = Path(__file__).resolve().parent
TEMP = HERE.parents[3] / 'tmp/a040-local-preparation-repair2'
STAGE = TEMP / ('empty' if MODE == 'isolate-empty' else 'selected')
EXPECTED = 'fc561eee08f1eafbbeac2cbcc5fa31890ef719bf603c5c7dd1af7aea5e556bcb'
for key in list(os.environ):
    if key.startswith(('MODAL_', 'AWS_', 'HF_TOKEN', 'HUGGING_FACE_HUB_TOKEN')):
        del os.environ[key]
os.environ['MODAL_CONFIG_PATH'] = str(TEMP / 'empty-modal-config.toml')
os.chdir(STAGE)
sys.path.insert(0, str(STAGE))
assert not any(str(HERE).lower() == str(p).lower() for p in sys.path)
START = time.monotonic()
RESULT = {'mode': MODE, 'cwd': os.getcwd(), 'sys_path': list(sys.path), 'installer_calls': 0}


def audit(event, args):
    if event in ('subprocess.Popen', 'os.system', 'socket.connect', 'socket.bind', 'socket.getaddrinfo'):
        raise PermissionError('Isolation forbids network and commands')
    if event == 'import' and args[0].split('.')[0] in ('modal', 'torch', 'tabicl', 'numpy', 'pandas'):
        raise PermissionError('Isolation forbids SDK/model imports')
    if event == 'open' and isinstance(args[0], (str, bytes)):
        path = Path(os.fsdecode(args[0])).resolve()
        if path.name == '.modal.toml' or path.suffix.lower() in ('.parquet', '.npz', '.safetensors', '.pt'):
            raise PermissionError('Protected input/config')
        allowed = (STAGE, Path(sys.base_prefix) / 'Lib', Path(sys.base_prefix) / 'DLLs')
        report = HERE / ('result-' + NUMBER + '.json')
        if path != report and not any(path == base or base in path.parents for base in allowed):
            raise PermissionError('Outside isolated input')


def trace(frame, event, arg):
    if event == 'call' and frame.f_code.co_name == 'install_pins':
        raise PermissionError('Installer body forbidden')
    return None


sys.addaudithook(audit)
sys.settrace(trace)
before = set(sys.modules)
try:
    try:
        module = importlib.import_module('controller_core')
    except ModuleNotFoundError as error:
        assert MODE == 'isolate-empty' and error.name == 'controller_core'
        RESULT['imported'] = False
        RESULT['missing'] = error.name
    else:
        assert MODE == 'isolate-fixed'
        assert Path(module.__file__).resolve() == STAGE / 'controller_core.py'
        assert module.install_pins.__module__ == 'controller_core'
        assert module.install_pins.__qualname__ == 'install_pins'
        digest = hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
        assert digest == EXPECTED
        origins = {}
        for name in sorted(set(sys.modules) - before):
            imported = sys.modules[name]
            source = getattr(imported, '__file__', None)
            if source:
                source = Path(source).resolve()
                assert STAGE in source.parents or Path(sys.base_prefix).resolve() in source.parents
                origins[name] = str(source)
            else:
                origins[name] = 'builtin/no-file'
        RESULT.update(imported=True, module='controller_core', function='install_pins',
                      sha256=digest, transitive_imports=origins, source=str(module.__file__))
    RESULT['outcome'] = 'PASS'
except BaseException:
    RESULT['outcome'] = 'FAIL'
    RESULT['error'] = traceback.format_exc()
finally:
    RESULT['elapsed_seconds'] = time.monotonic() - START
    (HERE / ('result-' + NUMBER + '.json')).write_text(json.dumps(RESULT, indent=2), encoding='utf-8')
    print(json.dumps(RESULT, indent=2))
sys.exit(0 if RESULT['outcome'] == 'PASS' else 1)
