"""Only executable binding: stdlib fake SDK; no live transport option."""
import asyncio
from contextlib import nullcontext
from dataclasses import dataclass
import json
import os
from pathlib import Path
import sys
import time
from types import SimpleNamespace as NS

from controller import AsyncSDKTransport, run_controller, write_json

TEXT = "• 한글 로그"
SCENARIOS = {"success", "unicode_error", "cancel_resistant", "stop_timeout", "stop_failure",
             "ack_running", "terminal_tasks", "terminal_zero", "create_lost", "construct_error",
             "prepare_error", "query_timeout", "blocked_loop"}


async def resist_cancel():
    while True:
        try:
            await asyncio.sleep(0.02)
        except asyncio.CancelledError:
            continue


def fake_sdk(scenario, calls, loop):
    def note(name, **values):
        assert asyncio.get_running_loop() is loop
        calls.append({"call": name, **values})

    @dataclass
    class Bill:
        billed_cost: float = 0
        metered_cost: float = 0

    class Stub:
        async def AppStop(self, request):
            note("AppStop", app_id=request.app_id)
            assert request.app_id == "ap-FAKE-OWNED"
            if scenario == "stop_timeout":
                await resist_cancel()
            if scenario == "stop_failure":
                raise RuntimeError("stop failed • 한글")

        async def AppGetInfo(self, request):
            note("AppGetInfo", app_id=request.app_id)
            assert request.app_id == "ap-FAKE-OWNED"
            if scenario == "query_timeout":
                await resist_cancel()
            stopped = scenario not in {"ack_running", "stop_timeout", "stop_failure"}
            return NS(info=NS(lifecycle=NS(app_state="STOPPED" if stopped else "RUNNING")))

        async def TaskList(self, request):
            note("TaskList", app_id=request.app_id)
            assert request.app_id == "ap-FAKE-OWNED"
            return NS(tasks=["fake-task"] if scenario in {"terminal_tasks", "ack_running"} else [])

    client = NS(_stub=Stub())

    class Client:
        @staticmethod
        async def from_env():
            note("FAKE_Client.from_env")
            if scenario == "prepare_error":
                raise RuntimeError("before create • 한글")
            return client

    class Workspace:
        name = "joon56"
        @staticmethod
        def from_context(*, client):
            note("FAKE_Workspace.from_context")
            return Workspace()
        async def hydrate(self):
            note("hydrate")
        async def summary(self):
            note("billing.summary")
            return Bill()
        @property
        def billing(self):
            return self

    class App:
        @staticmethod
        async def lookup(name, *, client, create_if_missing, environment_name):
            note("App.lookup", app_name=name, create_if_missing=create_if_missing, environment=environment_name)
            assert create_if_missing and environment_name == "main"
            if scenario == "create_lost":
                # Simulated server creation with lost response: ID remains unknown.
                raise TimeoutError("create response lost • 한글")
            return NS(app_id="ap-FAKE-OWNED")

    class Image:
        object_id = "im-FAKE"
        @staticmethod
        def from_registry(tag):
            note("Image.from_registry", tag=tag)
            assert tag == "python:3.13.14-slim"
            if scenario == "construct_error":
                raise RuntimeError("construction before old try • 한글")
            return Image()
        def run_function(self, fn, *, args, cpu, memory, timeout, include_source):
            note("run_function_recipe", cpu=cpu, memory=memory, timeout=timeout, include_source=include_source)
            assert fn.__name__ == "install_pins" and args[0] == "FAKE_PINS_NOT_REAL_INPUT"
            assert cpu == (1, 1) and memory == (8192, 8192) and timeout == 600 and include_source is False
            return self  # NEVER call installer.
        async def build(self, app):
            note("Image.build", app_id=app.app_id)
            print(TEXT + " stdout", flush=True)
            print(TEXT + " stderr", file=sys.stderr, flush=True)
            if scenario == "unicode_error":
                raise RuntimeError("retained exception • 한글")
            if scenario == "cancel_resistant":
                await resist_cancel()
            if scenario == "blocked_loop":
                time.sleep(60)  # Parent must kill own worker at1s, never wait60s.
            return self

    return NS(Client=Client, Workspace=Workspace, App=App, Image=Image,
              enable_output=nullcontext, pb=NS(AppStopRequest=NS, AppGetInfoRequest=NS,
                  TaskListRequest=NS, APP_STOP_SOURCE_CLI="CLI", APP_STATE_STOPPED="STOPPED"))


def main():
    scenario, destination = sys.argv[1:]
    assert scenario in SCENARIOS
    output = Path(destination)
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="strict", line_buffering=True)
    loop = asyncio.new_event_loop()  # stdlib event-loop IPC initialized, no SDK.
    asyncio.set_event_loop(loop)
    blocked = []
    def guard(event, args):
        if event in {"socket.connect", "socket.getaddrinfo", "socket.gethostbyname", "socket.sendto",
                     "subprocess.Popen", "os.system", "os.exec", "os.posix_spawn"}:
            blocked.append(event)
            raise PermissionError("Local regression forbids network/process operation: " + event)
        if event == "import" and args[0].split(".")[0] in {"modal", "modal_proto", "torch", "tabicl", "numpy"}:
            raise PermissionError("SDK/model import forbidden in fake worker")
        if event == "open" and isinstance(args[0], str):
            path = args[0].replace("\\", "/").lower()
            if any(part in path for part in (".modal", "/staging/", ".parquet", ".npz", ".safetensors", ".pt")):
                raise PermissionError("Protected file forbidden")
    sys.addaudithook(guard)
    # Synthetic audit event: proves fail-closed guard without opening a socket.
    try:
        sys.audit("socket.connect", None, ("not-a-real-target", 0))
    except PermissionError:
        assert blocked == ["socket.connect"]
    else:
        raise AssertionError("Network guard inactive")
    blocked.clear()
    calls = []
    def record(kind, value):
        with (output / "events.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"kind": kind, **value}, ensure_ascii=False) + "\n")
    transport = AsyncSDKTransport(fake_sdk(scenario, calls, loop), "FAKE_PINS_NOT_REAL_INPUT",
                                  time.time()+3600, "a040-LOCAL-FAKE", record)
    result = loop.run_until_complete(run_controller(transport, output))
    pending = list(asyncio.all_tasks(loop))
    write_json(output / "worker-audit.json", {"fake_calls": calls, "blocked_operations": blocked,
        "sdk_imported": "modal" in sys.modules, "model_imported": any(x in sys.modules for x in ("torch", "tabicl", "numpy")),
        "pending_tasks_at_exit": len(pending), "stdout_encoding": sys.stdout.encoding,
        "stderr_encoding": sys.stderr.encoding, "network_transport": "FAKE_ONLY",
        "live_rpc_calls": 0, "grandchildren_allowed": False, "synthetic_network_guard_probe_blocked": 1})
    if result.get("traceback"):
        print(result["traceback"], file=sys.stderr, flush=True)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    # Avoid asyncio.run's unbounded shutdown gather. Parent owns hard deadline.
    # Flush explicit journals/streams before isolated worker process exit.
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0 if result["outcome"] == "BUILD_COMPLETED" else 2)


if __name__ == "__main__":
    main()
