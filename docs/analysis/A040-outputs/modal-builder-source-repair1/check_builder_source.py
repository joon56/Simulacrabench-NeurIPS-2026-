"""Bounded local SDK discovery, never remote resolution or installer execution."""
import ast
import asyncio
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
TEMP = ROOT / "tmp/a040-modal-builder-source-repair1"
EXPECTED = "fc561eee08f1eafbbeac2cbcc5fa31890ef719bf603c5c7dd1af7aea5e556bcb"
MODE = sys.argv[1]
assert MODE in ("baseline", "fixed")
START = time.monotonic()
RESULT = {"mode": MODE, "rpc": 0, "installer_calls": 0, "checks": []}

# Do not inherit account settings or read the real user configuration.
for key in list(os.environ):
    if key.startswith("MODAL_"):
        del os.environ[key]
os.environ["MODAL_CONFIG_PATH"] = str(TEMP / "absent-config.toml")
assert not Path(os.environ["MODAL_CONFIG_PATH"]).exists()
sys.dont_write_bytecode = True


def audit(event, args):
    if event in ("socket.connect", "socket.getaddrinfo", "os.system"):
        raise PermissionError("Network/command disabled")
    if event == "open" and isinstance(args[0], (str, bytes)):
        path = os.fsdecode(args[0]).lower().replace("\\", "/")
        if path.endswith((".parquet", ".npz", ".safetensors", ".pt", ".modal.toml")):
            raise PermissionError("Protected input/config disabled")
    if event == "import" and args[0].split(".")[0] in ("torch", "tabicl", "numpy", "pandas"):
        raise PermissionError("Model/data imports disabled")


sys.addaudithook(audit)
sys.path.insert(0, str(HERE))


def check(name, condition):
    RESULT["checks"].append({"name": name, "pass": bool(condition)})
    if not condition:
        raise AssertionError(name)


class DiscoveryComplete(Exception):
    """Interrupt at the external build endpoint, before resolution or RPC."""


async def stop_before_build(image, app):
    raise DiscoveryComplete()


def prohibited(*args, **kwargs):
    raise PermissionError("Client/RPC/build disabled")


def guard_installer(frame, event, arg):
    if event == "call" and frame.f_code.co_name == "install_pins":
        raise PermissionError("Installer execution disabled")


ISOLATED = r'''
import sys, os, json, hashlib, importlib
from pathlib import Path
root = Path(sys.argv[1]).resolve()
before = set(sys.modules)
sys.path.insert(0, str(root))
def audit(event, args):
    if event in ('subprocess.Popen', 'os.system', 'socket.connect', 'socket.getaddrinfo'):
        raise PermissionError('No commands or network in isolated import')
sys.addaudithook(audit)
def trace(frame, event, arg):
    if event == 'call' and frame.f_code.co_name == 'install_pins':
        raise PermissionError('Installer body forbidden')
sys.setprofile(trace)
try:
    module = importlib.import_module('controller_core')
except ModuleNotFoundError as exc:
    print(json.dumps({'imported': False, 'missing': exc.name}))
    sys.exit(0)
new = []
for name in sorted(set(sys.modules) - before):
    mod = sys.modules[name]
    origin = getattr(mod, '__file__', None)
    if origin:
        resolved = Path(origin).resolve()
        assert root in resolved.parents or Path(sys.base_prefix).resolve() in resolved.parents, (name, origin)
    assert name.split('.')[0] not in ('modal', 'torch', 'tabicl', 'numpy', 'pandas')
    new.append(name)
assert Path(module.__file__).resolve() == root / 'controller_core.py'
assert module.install_pins.__module__ == 'controller_core'
assert module.install_pins.__qualname__ == 'install_pins'
print(json.dumps({'imported': True, 'module': module.install_pins.__module__,
 'function': module.install_pins.__qualname__, 'file': module.__file__,
 'sha256': hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest(),
 'transitive_imports': new, 'sys_path': sys.path, 'cwd': os.getcwd(), 'installer_calls': 0}))
'''


def isolated(directory):
    result = subprocess.run(
        [sys.executable, "-I", "-S", "-B", "-c", ISOLATED, str(directory)],
        cwd=directory, capture_output=True, text=True, encoding="utf-8", timeout=10,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
    )
    if result.returncode:
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)


def validate_bytes(raw):
    if hashlib.sha256(raw).hexdigest() != EXPECTED:
        raise ValueError("Wrong source hash")
    return raw


def validate_inventory(rows):
    expected_file = (HERE / "controller_core.py").resolve()
    if len(rows) != 1:
        raise ValueError("Exactly one project source required")
    local, remote = rows[0]
    if Path(local).resolve() != expected_file or str(remote) != "/root/controller_core.py":
        raise ValueError("Wrong source or destination")
    return validate_bytes(Path(local).read_bytes())


async def main():
    import modal
    from modal.client import _Client
    from modal._image import _Image
    from modal._functions import _Function
    from modal.mount import _Mount, _MountFile, _select_files
    from modal._utils.function_utils import FunctionSourceInfoType
    from grpclib.client import Channel
    # Source discovery remains real. Only external access is blocked.
    _Client.from_env = prohibited
    _Client.__init__ = prohibited
    Channel.request = prohibited
    _Image.build = prohibited
    from sdk_endpoint import Endpoint
    sys.setprofile(guard_installer)
    check("SDK1.6.0", modal.__version__ == "1.6.0")
    endpoint = Endpoint(client_factory=prohibited, image_builder=stop_before_build,
                        sandbox_factory=prohibited)
    try:
        # Protocol placeholders are never installed. Real pins remain untouched.
        await endpoint.build("im-local-source-check", "LOCAL_PROTOCOL_ONLY", 0)
    except DiscoveryComplete:
        pass
    else:
        raise AssertionError("External build boundary not intercepted")
    dependencies = endpoint.image._deps_()
    functions = [obj for obj in dependencies if isinstance(obj, _Function)]
    check("one_actual_builder_function", len(functions) == 1)
    builder = functions[0]
    info = builder._source_info
    check("FILE_not_PACKAGE", info._type is FunctionSourceInfoType.FILE)
    check("module_function_identity", (info.module_name, info.function_name, info.implementation_name)
          == ("controller_core", "install_pins", "install_pins"))
    mounts = builder._spec.mounts
    deps_mounts = [obj for obj in builder._deps_() if isinstance(obj, _Mount)]
    check("spec_dependency_mounts_identical", mounts == deps_mounts)
    check("default_client_mount_separate", len(mounts) >= 1 and not mounts[0].is_local())
    rows = []
    for mount in mounts[1:]:
        check("single_FILE_entry_only", len(mount.entries) == 1 and isinstance(mount.entries[0], _MountFile))
        rows.extend(_select_files(mount.entries))
    RESULT["builder"] = {"classification": info._type.value, "module": info.module_name,
        "function": info.function_name, "implementation": info.implementation_name,
        "defining_file": info._file, "client_mount": repr(mounts[0]),
        "all_mount_count": len(mounts), "project_files": [[str(a), str(b)] for a, b in rows]}
    stage = TEMP / MODE
    stage.mkdir(exist_ok=False)
    if MODE == "baseline":
        check("original_source_mount_omitted", rows == [])
        RESULT["isolated"] = isolated(stage)
        check("missing_module_negative", RESULT["isolated"] == {"imported": False, "missing": "controller_core"})
        RESULT["outcome"] = "EXPECTED_SOURCE_CONTRACT_FAILURE_REPRODUCED"
    else:
        raw = validate_inventory(rows)
        check("exact_source_hash", hashlib.sha256(raw).hexdigest() == EXPECTED)
        rejected = []
        for name, invalid in (
            ("missing", []), ("extra", rows + rows),
            ("wrong_path", [(HERE / "sdk_endpoint.py", rows[0][1])]),
            ("wrong_remote", [(rows[0][0], "/root/wrong.py")]),
        ):
            try:
                validate_inventory(invalid)
            except ValueError:
                rejected.append(name)
        check("invalid_inventory_rejected", len(rejected) == 4)
        # Hash rejection uses different bytes, without changing source on disk.
        try:
            validate_bytes(raw + b"\n")
        except ValueError:
            check("wrong_hash_rejected", True)
        else:
            check("wrong_hash_rejected", False)
        (stage / "controller_core.py").write_bytes(raw)
        RESULT["isolated"] = isolated(stage)
        check("isolated_exact_import", RESULT["isolated"]["imported"] and RESULT["isolated"]["sha256"] == EXPECTED)
        RESULT["outcome"] = "LOCAL_BUILDER_SOURCE_CONTRACT_PASS"
    RESULT["installer_top_level_imports"] = [node.names[0].name for node in ast.parse((HERE / "controller_core.py").read_bytes()).body if isinstance(node, ast.Import)]
    check("stdlib_top_level_only", RESULT["installer_top_level_imports"] == ["asyncio"])


try:
    asyncio.run(main())
except BaseException:
    RESULT["outcome"] = "LOCAL_CHECK_FAIL"
    RESULT["error"] = traceback.format_exc()
finally:
    RESULT["elapsed_seconds"] = time.monotonic() - START
    (HERE / (MODE + "-result.json")).write_text(json.dumps(RESULT, indent=2), encoding="utf-8")
    print(json.dumps(RESULT, indent=2))
sys.exit(1 if RESULT["outcome"] == "LOCAL_CHECK_FAIL" else 0)
