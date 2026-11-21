"""Focused whole-path protocol regression; no payload, models, credentials or RPC."""
import asyncio
import ast
from dataclasses import replace
import inspect
import json
import os
from pathlib import Path
import socket
import sys
import time
import traceback
from types import SimpleNamespace
from unittest.mock import patch

START = time.monotonic()
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUTPUT = Path(sys.argv[1]).resolve()
OUTPUT.mkdir(parents=True, exist_ok=False)
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
# Windows event-loop self-pipe is initialized before external call guards.
# No SDK is imported at this point. This is local IPC, not an egress proof.
LOOP = asyncio.new_event_loop()
asyncio.set_event_loop(LOOP)
os.environ["MODAL_CONFIG_PATH"] = str(OUTPUT / "nonexistent-no-credentials.toml")
for key in ("MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET", "MODAL_PROFILE"):
    os.environ.pop(key, None)
BLOCKED = []


def deny(*args, **kwargs):
    BLOCKED.append("forbidden_external_endpoint")
    raise PermissionError("Local integration: external endpoint forbidden")


def audit(name, args):
    if name in ("socket.connect", "socket.getaddrinfo", "socket.sendto", "subprocess.Popen", "os.system", "os.posix_spawn"):
        deny()
    if name == "import" and args[0].split(".")[0] in ("torch", "tabicl", "numpy", "pandas", "sklearn", "transformers"):
        deny()
    if name == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
        path = os.fsdecode(args[0]).replace("\\", "/").lower()
        if any(term in path for term in (".modal.toml", "/.aws/", "/.ssh/", "fake3", "/acquisition/", "/staging/", "/vaf/")) or path.endswith((".parquet", ".npz", ".ckpt")):
            deny()


sys.addaudithook(audit)
socket.create_connection = deny
socket.socket.connect = deny
socket.socket.connect_ex = deny
socket.getaddrinfo = deny
socket.socket.sendto = deny

from live_binding import SDK
from modal_proto import api_pb2 as pb
from modal_version import __version__
from google.protobuf.empty_pb2 import Empty
from modal.sandbox_fs import _SandboxFilesystem
from modal.container_process import _ContainerProcess, _StreamReader
from contract import Plan, MODULES, CAP_BYTES, REMOTE_DIR, sha, verify_sources
from payload import Payload, FileReader
from sdk_endpoint import Endpoint
from live_worker import Context, run

assert __version__ == "1.6.0"
AUTH_PATCH = patch.object(SDK.Client, "from_env", side_effect=deny)
AUTH_PATCH.start()
# Block native client construction/transport opening as well as from_env.
OPEN_PATCH = patch.object(SDK.Client, "_open", side_effect=deny)
OPEN_PATCH.start()
MANIFEST = json.loads((HERE / "source-manifest.json").read_text(encoding="utf-8"))
PINS = (ROOT / "docs/analysis/A040-outputs/full-path-resume1/requirements.lock.txt").read_text(encoding="utf-8-sig")
BASE = b"tiny-protocol-result"
FIXTURE_BYTES = b"meaningless-local-transfer"
CASES = []


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def bind(function, *args, **kwargs):
    inspect.signature(function).bind(*args, **kwargs)


class RemoteProcess:
    __slots__ = ("stdout", "stderr", "code")
    def __init__(self, code):
        self.stdout = Stream("protocol fixture only")
        self.stderr = Stream("")
        self.code = code
    async def wait(self):
        bind(_ContainerProcess.wait, self)
        return self.code


class Stream:
    __slots__ = ("value",)
    def __init__(self, value):
        self.value = value
    async def read(self):
        bind(_StreamReader.read, self)
        return self.value


class Filesystem:
    __slots__ = ("owner", "data")
    def __init__(self, owner):
        self.owner, self.data = owner, {}
    async def write_bytes(self, data, remote_path):
        bind(_SandboxFilesystem.write_bytes, self, data, remote_path)
        check(isinstance(data, bytes) and remote_path.startswith("/work/"), "File transport types")
        self.owner.calls.append("write:" + remote_path)
        if self.owner.fault == "transfer":
            raise IOError("injected transport failure")
        self.data[remote_path] = data
    async def read_bytes(self, remote_path):
        bind(_SandboxFilesystem.read_bytes, self, remote_path)
        self.owner.calls.append("read:" + remote_path)
        if self.owner.fault == "export" and remote_path.endswith("reference/result.json"):
            raise IOError("injected result loss")
        if self.owner.fault == "export_hash" and "/tmp/" in remote_path:
            return b"changed-output"
        return self.data[remote_path]


class Sandbox:
    __slots__ = ("owner", "object_id", "filesystem", "stopped")
    def __init__(self, owner):
        self.owner, self.object_id = owner, "sb-protocol"
        self.filesystem = Filesystem(owner)
        self.stopped = False
    async def exec(self, *args, **kwargs):
        bind(SDK.Sandbox.exec, self, *args, **kwargs)
        self.owner.commands.append({"args": args, "kwargs": kwargs})
        check(args[:4] == ("python", "-I", "-B", "-u"), "Explicit isolated Python command")
        if args[4].endswith("linux_boundary.py"):
            check(kwargs == {"timeout": 60, "text": True}, "Boundary60s cap")
            value = dict(outcome="BOUNDARY_PASS", source_payload_verified=True, native_network_blocked=True,
                swap_disabled=True, gpu_h100_single=True, python_pins_match=True, duplicate_latch_guard=True,
                two_logical_affinity=True, memory_limit_bytes=CAP_BYTES, physical_cpu_limit=1,
                evidence_scope="LOCAL_PROTOCOL_FIXTURE")
            if self.owner.fault == "boundary":
                value["native_network_blocked"] = False
            self.filesystem.data[REMOTE_DIR + "/boundary-result.json"] = json.dumps(value).encode()
            self.filesystem.data[REMOTE_DIR + "/linux-requirements.json"] = b'[["fixture","0"]]'
            return RemoteProcess(0)
        check(args[4] == REMOTE_DIR + "/linux_watchdog.py", "Only fixed remote programs")
        mode = args[5]
        check(mode in ("reference", "candidate"), "Named science mode")
        check(kwargs == {"timeout": 925, "text": True}, "Wrapper time cap")
        self.owner.science.append(mode)  # Recorder only. No command is executed.
        failed = self.owner.fault == mode
        outcome = "INJECTED_FAILURE" if failed else ("REFERENCE_PASS" if mode == "reference" else "LOCAL_FULL_PATH_PASS")
        names = ["unicef", "wb", "unhcr"]
        if mode == "candidate":
            names += ["unhcr-engineering-alpha025", "unhcr-final-e041"]
        result = {"outcome": outcome, "full_path_completed": not failed,
            "output_counts": {"unicef": 1, "wb": 1, "unhcr": 189647},
            "output_hashes": {name: sha(b"[]") for name in names}, "evidence_scope": "LOCAL_PROTOCOL_FIXTURE"}
        resources = {"outcome": outcome, "child_exit": 1 if failed else 0, "elapsed_seconds": .01,
                     "evidence_scope": "LOCAL_PROTOCOL_FIXTURE"}
        if self.owner.fault == "science_timeout" and mode == "reference":
            resources["elapsed_seconds"] = 901
        if self.owner.fault == "vectors" and mode == "reference":
            result["output_counts"]["unhcr"] = 0
        for name, raw in {"result.json": json.dumps(result).encode(), "resources.json": json.dumps(resources).encode(),
                          "events.jsonl": b"", "resource-samples.jsonl": b"", "stdout.txt": b"", "stderr.txt": b""}.items():
            self.filesystem.data[REMOTE_DIR + "/" + mode + "/" + name] = raw
        for name in names:
            self.filesystem.data["/work/tmp/a040-modal-local-integration1/" + mode + "/" + name + ".json"] = b"[]"
        return RemoteProcess(1 if failed else 0)
    async def terminate(self):
        bind(SDK.Sandbox.terminate, self)
        self.owner.calls.append("sandbox_terminate")
        if self.owner.fault == "cleanup_terminate":
            raise IOError("injected terminate failure")
        self.stopped = True
    async def poll(self):
        bind(SDK.Sandbox.poll, self)
        self.owner.calls.append("sandbox_poll")
        return 0 if self.stopped else None


class Rpc:
    __slots__ = ("owner", "ImageJoinStreaming")
    def __init__(self, owner):
        self.owner = owner
        self.ImageJoinStreaming = ImageStream(owner)
    async def WorkspaceNameLookup(self, request):
        check(isinstance(request, Empty), "Workspace actual Empty request")
        return pb.WorkspaceNameLookupResponse(username="wrong" if self.owner.fault == "workspace" else "joon56")
    async def WorkspaceBillingSummary(self, request):
        check(isinstance(request, pb.WorkspaceBillingSummaryRequest), "Billing actual request")
        self.owner.calls.append("billing")
        return pb.WorkspaceBillingSummaryResponse(metered_cost="4" if self.owner.fault == "cost" else "0",
            billed_cost="1" if self.owner.fault == "cash" else "0", metered_cost_breakdown={"apps": "0.00001152"})
    async def ImageFromId(self, request):
        check(isinstance(request, pb.ImageFromIdRequest), "Image actual request")
        return pb.ImageFromIdResponse(image_id="im-wrong" if self.owner.fault == "image_identity" else request.image_id)
    async def AppGetOrCreate(self, request):
        check(isinstance(request, pb.AppGetOrCreateRequest), "App actual request")
        check(request.app_name == self.owner.plan.app_name and request.environment_name == "main", "Owned name only")
        creating = request.object_creation_type == pb.OBJECT_CREATION_TYPE_CREATE_IF_MISSING
        self.owner.calls.append("app_create" if creating else "app_recover")
        if creating and self.owner.fault == "app_id_loss":
            raise IOError("injected lost create reply")
        return pb.AppGetOrCreateResponse(app_id="ap-protocol")
    async def AppStop(self, request):
        check(isinstance(request, pb.AppStopRequest) and request.app_id == "ap-protocol", "Owned AppStop")
        self.owner.calls.append("app_stop")
        if self.owner.fault == "cleanup_stop":
            raise IOError("injected AppStop failure")
        return Empty()
    async def AppGetInfo(self, request):
        check(isinstance(request, pb.AppGetInfoRequest) and request.app_id == "ap-protocol", "Owned AppInfo")
        if self.owner.fault == "cleanup_query":
            raise IOError("injected query failure")
        response = pb.AppGetInfoResponse()
        response.info.lifecycle.app_state = pb.APP_STATE_STOPPED if self.owner.fault != "cleanup_state" else pb.APP_STATE_DEPLOYED
        return response
    async def TaskList(self, request):
        check(isinstance(request, pb.TaskListRequest) and request.app_id == "ap-protocol", "Owned task list")
        response = pb.TaskListResponse()
        if self.owner.fault == "cleanup_tasks":
            response.tasks.add()
        return response
    async def SandboxGetFromName(self, request):
        check(isinstance(request, pb.SandboxGetFromNameRequest), "Sandbox recovery actual request")
        self.owner.calls.append("sandbox_recover")
        return pb.SandboxGetFromNameResponse(sandbox_id="sb-protocol")
    async def SandboxGetFromNameV2(self, request, *, metadata):
        check(metadata == [("x-modal-auth-token", "LOCAL_PROTOCOL_NOT_A_TOKEN")], "Only explicit token-endpoint fixture")
        return await self.SandboxGetFromName(request)
    async def SandboxTerminate(self, request):
        check(isinstance(request, pb.SandboxTerminateRequest), "Recovered sandbox terminate")
        self.owner.calls.append("sandbox_terminate")
        return Empty()
    async def SandboxWait(self, request):
        check(isinstance(request, pb.SandboxWaitRequest), "Recovered sandbox poll")
        return pb.SandboxWaitResponse(result=pb.GenericResult(status=pb.GenericResult.GENERIC_STATUS_SUCCESS, exitcode=0))


class ImageStream:
    __slots__ = ("owner",)
    def __init__(self, owner):
        self.owner = owner
    async def unary_stream(self, request):
        check(isinstance(request, pb.ImageJoinStreamingRequest), "Image stream actual request")
        check(request.timeout == 3, "Original image stream timeout")
        fault = self.owner.fault
        if fault == "empty":
            return
        if fault == "base_timeout":
            await asyncio.sleep(5)
        if fault == "wrong_type":
            yield Empty()
            return
        status = pb.GenericResult.GENERIC_STATUS_SUCCESS
        if fault == "status_failure":
            status = pb.GenericResult.GENERIC_STATUS_FAILURE
        if fault == "status_unspecified":
            status = 0
        yield pb.ImageJoinStreamingResponse(result=pb.GenericResult(status=status,
                data=b"wrong" if fault == "base_identity" else BASE))


class TokenEndpoint:
    __slots__ = ()
    async def get_token(self):
        # Explicit RPC-boundary fixture, never a lookup of user authentication.
        return "LOCAL_PROTOCOL_NOT_A_TOKEN"


class Scenario:
    def __init__(self, name, fault="", changes=None):
        self.name, self.fault = name, fault
        self.calls, self.commands, self.science = [], [], []
        now = time.time()
        self.plan = Plan("LOCAL_PROTOCOL_FIXTURE", "a040-local-" + name.replace("_", "-"), "im-base", sha(BASE),
            now+1500, now+5000, now+7000, operation_timeout=.08, build_timeout=.1,
            cleanup_timeout=.08, cancel_grace=.005, poll_seconds=.002)
        if changes:
            self.plan = replace(self.plan, **changes)
        self.client = SimpleNamespace(_stub=Rpc(self), _cancellation_context_event_loop=LOOP,
                                      _auth_token_manager=TokenEndpoint())
        self.endpoint = Endpoint(client_factory=self.connect, image_builder=self.image_build, sandbox_factory=self.sandbox_create)
        rows = [{"path": "tiny.txt", "bytes": len(FIXTURE_BYTES), "sha256": sha(FIXTURE_BYTES)}]
        payload = Payload(rows, [], self.read_payload, self.read_payload, "LOCAL_PROTOCOL_FIXTURE")
        self.context = Context(OUTPUT / name, self.plan, self.endpoint, payload, PINS)
    async def connect(self):
        self.calls.append("injected_client")
        return self.client
    def read_payload(self, path):
        check(path == "tiny.txt", "Only meaningless protocol bytes")
        return b"bad" if self.fault == "payload" else FIXTURE_BYTES
    async def image_build(self, image, app):
        check(isinstance(image, SDK.Image) and isinstance(app, SDK.App), "Actual SDK image/App handles")
        self.calls.append("image_build")
        if self.fault == "build":
            raise RuntimeError("injected image failure")
        if self.fault == "build_timeout":
            await asyncio.sleep(5)
        image._hydrate("im-complete-protocol", self.client, pb.ImageMetadata())
    async def sandbox_create(self, *args, **kwargs):
        bind(SDK.Sandbox.create, *args, **kwargs)
        self.calls.append("sandbox_create")
        check(args == ("sleep", "2400"), "Fixed Sandbox lifetime")
        check(kwargs["gpu"] == "H100!" and kwargs["cpu"] == (1, 1) and kwargs["memory"] == (15258, 15258), "Fixed resource request")
        check(kwargs["runtime"] == "gvisor" and kwargs["block_network"] is True, "Native network request")
        check(kwargs["secrets"] == [] and kwargs["include_oidc_identity_token"] is False, "No tokens in Sandbox")
        check(kwargs["env"]["OMP_NUM_THREADS"] == "2" and kwargs["env"]["HF_HUB_OFFLINE"] == "1", "Fixed thread/offline env")
        if self.fault == "sandbox_id_loss":
            raise IOError("injected lost Sandbox reply")
        return Sandbox(self)
    async def execute(self, manifest=None, source=HERE):
        result = await run(self.context, manifest or MANIFEST, source)
        check(not BLOCKED, "Forbidden access attempted")
        return result


async def integration_cases():
    # Original enum defect is reproduced against the actual installed module.
    try:
        getattr(pb, "GENERIC_STATUS_SUCCESS")
    except AttributeError:
        check(pb.GenericResult.GENERIC_STATUS_SUCCESS == 1, "Nested real enum")
    else:
        raise AssertionError("Original defect did not reproduce")
    CASES.append({"name": "original_enum_reproduced", "pass": True})
    normal = Scenario("normal")
    value = await normal.execute()
    check(value["outcome"] == "LOCAL_PROTOCOL_PATH_PASS", repr(value))
    check(normal.science == ["reference", "candidate"], "Single ordered modes")
    check(normal.calls.count("app_create") == normal.calls.count("image_build") == normal.calls.count("sandbox_create") == 1, "Single create/build/Sandbox")
    check(value["actual_remote_facts"] == "UNVERIFIED", "Mock cannot claim remote facts")
    CASES.append({"name": "normal_single_production_path", "pass": True, "commands": normal.commands,
                  "mock_calls": normal.calls, "result": value["outcome"]})
    before = len(normal.calls)
    try:
        await normal.execute()
    except FileExistsError:
        check(len(normal.calls) == before, "Duplicate contacted endpoint")
    else:
        raise AssertionError("Duplicate run accepted")
    try:
        normal.context.latch("reference")
    except FileExistsError:
        check(True, "Existing mode latch refused")
    else:
        raise AssertionError("Duplicate science latch accepted")
    CASES.append({"name": "duplicate_run_and_mode_latches", "pass": True})

    no_create = ("empty", "status_failure", "status_unspecified", "wrong_type", "base_identity", "image_identity", "workspace", "cash", "cost", "base_timeout")
    no_science = ("build", "build_timeout", "payload", "transfer", "boundary", "app_id_loss", "sandbox_id_loss")
    stop_reference = ("reference", "science_timeout", "vectors", "export", "export_hash")
    late = ("candidate", "cleanup_terminate", "cleanup_stop", "cleanup_query", "cleanup_state", "cleanup_tasks")
    for fault in (*no_create, *no_science, *stop_reference, *late):
        item = Scenario(fault, fault)
        result = await item.execute()
        check(result["outcome"] != "LOCAL_PROTOCOL_PATH_PASS", fault + " false PASS")
        if fault in no_create:
            check("app_create" not in item.calls, fault + " created app")
        if fault in no_create + no_science:
            check(item.science == [], fault + " invoked science")
        if fault in stop_reference:
            check(item.science == ["reference"], fault + " invoked candidate")
        if fault == "app_id_loss":
            check(item.calls.count("app_create") == 1 and item.calls.count("app_recover") == 1, "ID recovery must be read-only")
        if fault == "sandbox_id_loss":
            check(item.calls.count("sandbox_create") == 1 and item.calls.count("sandbox_recover") == 1, "Sandbox recovery must be read-only")
        CASES.append({"name": fault, "pass": True, "outcome": result["outcome"],
                      "recorded_science": item.science, "termination": result["termination"], "error": result.get("error")})

    for label, change in (("prepare_time", {"prepare_deadline": time.time()+500}),
                          ("gpu_time", {"gpu_latest_end": time.time()+2000}),
                          ("unauthorized_live", {"scope": "LIVE"})):
        item = Scenario(label, changes=change)
        try:
            result = await item.execute()
        except PermissionError:
            check(label == "unauthorized_live" and not item.calls, "Fresh authorization gate")
        else:
            check(result["outcome"] != "LOCAL_PROTOCOL_PATH_PASS" and not item.science, label)
        CASES.append({"name": label, "pass": True})

    for fault in ("missing", "hash", "placeholder"):
        item = Scenario("source_" + fault)
        manifest = json.loads(json.dumps(MANIFEST))
        source = HERE
        if fault == "missing":
            manifest["files"].pop()
        elif fault == "hash":
            manifest["files"][0]["sha256"] = "0"*64
        else:
            source = OUTPUT / "placeholder-source"
            source.mkdir()
            for row in manifest["files"]:
                raw = (HERE / row["path"]).read_bytes()
                if row["path"] == "sandbox_stage.py":
                    raw = b"async def execute(context):\n    raise NotImplementedError()\n"
                (source / row["path"]).write_bytes(raw)
                row["sha256"] = sha(raw)
        try:
            await item.execute(manifest, source)
        except ValueError:
            check(not item.calls, "Source gate must precede endpoint")
        else:
            raise AssertionError("Source defect accepted: " + fault)
        CASES.append({"name": "source_" + fault, "pass": True})
    try:
        FileReader(ROOT, [], normal.plan)
    except PermissionError:
        check(True, "Real payload cannot open in local fixture")
    else:
        raise AssertionError("Real payload allowed in fixture")
    CASES.append({"name": "real_payload_reader_refused", "pass": True})


def source_policy_checks():
    original = (ROOT / "docs/analysis/A040-outputs/full-path-resume1/runner.py").read_text(encoding="utf-8-sig")
    expected = original.replace("TEMP=ROOT/'tmp/a040-full-path-resume1'", "TEMP=ROOT/'tmp/a040-modal-local-integration1'\nPOLICY=ROOT/'docs/analysis/A040-outputs/full-path-resume1'")
    expected = expected.replace("sys.path[:0]=[str(HERE),str(SOURCE)]", "sys.path[:0]=[str(HERE),str(POLICY),str(SOURCE)]")
    expected = expected.replace("HERE/'frozen-inputs/manifest.json'", "HERE/'target-contract.json'")
    expected = expected.replace("HERE/'fixture-manifest.json'", "POLICY/'fixture-manifest.json'").replace("HERE/'roles.json'", "POLICY/'roles.json'")
    expected = expected.replace("if '3070' not in torch.cuda.get_device_name(0)", "if torch.cuda.device_count()!=1 or 'H100' not in torch.cuda.get_device_name(0)")
    check(expected == (HERE / "linux_runner.py").read_text(encoding="utf-8-sig"), "Scientific runner differs beyond mechanical port")
    old_core = ast.parse((ROOT / "docs/analysis/A040-outputs/modal-full-path1-resume3/controller_core.py").read_text(encoding="utf-8-sig"))
    new_core = ast.parse((HERE / "controller_core.py").read_text(encoding="utf-8-sig"))
    function = lambda tree: next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "install_pins")
    check(ast.dump(function(old_core)) == ast.dump(function(new_core)), "Installer policy changed")
    # Compile all future target modules but never import or execute their bodies.
    for name in MODULES:
        compile((HERE / name).read_bytes(), str(HERE / name), "exec")
    CASES.append({"name": "mechanical_runner_installer_preservation_and_compile", "pass": True})


result = {"scope": "LOCAL_PROTOCOL_FIXTURE", "sdk": __version__, "cases": CASES,
          "actual_rpc": 0, "actual_science": 0, "actual_native_boundary": 0,
          "actual_payload112_read": 0, "new_remote_chargeable_actions": 0,
          "native_egress_enforcement_proven": False, "runtime_image_account_payload_facts": "UNVERIFIED"}
code = 1
try:
    source_policy_checks()
    LOOP.run_until_complete(integration_cases())
    check(not BLOCKED, "Forbidden attempted access")
    check(not any(n.split(".")[0] in ("torch", "tabicl", "numpy", "pandas", "sklearn", "transformers") for n in sys.modules), "Model import")
    result["outcome"] = "LOCAL_INTEGRATION_REGRESSION_PASS"
    code = 0
except BaseException:
    result.update(outcome="LOCAL_INTEGRATION_REGRESSION_FAIL", traceback=traceback.format_exc())
finally:
    result.update(elapsed_seconds=time.monotonic()-START, blocked_attempts=BLOCKED, completed_cases=len(CASES))
    (OUTPUT / "regression-result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k != "cases"}, ensure_ascii=False), flush=True)
    # No unbounded shutdown gather, no live SDK client ever opened.
    os._exit(code)
