"""Injected async controller. No SDK import, credentials, input reads or live CLI.

Use raw internal async objects consistently (SDK1.6.0 contract), never public .aio
wrappers with a raw stub. Only the fake binding is executable in this scope.
"""
import asyncio
import dataclasses
import json
import time
import traceback
from pathlib import Path


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


class AsyncSDKTransport:
    def __init__(self, sdk, requirements, deadline, app_name, record):
        self.sdk, self.requirements, self.deadline = sdk, requirements, deadline
        self.app_name, self.record = app_name, record
        self.client = self.app = self.image = None

    async def prepare(self):
        self.client = await self.sdk.Client.from_env()
        self.workspace = self.sdk.Workspace.from_context(client=self.client)
        await self.workspace.hydrate()
        if self.workspace.name != "joon56":
            raise RuntimeError("Workspace mismatch")
        self.baseline = await self.workspace.billing.summary()
        if float(self.baseline.billed_cost) != 0:
            raise RuntimeError("Cash billing contradiction")

    async def create(self):
        self.app = await self.sdk.App.lookup(self.app_name, client=self.client,
                            create_if_missing=True, environment_name="main")
        return self.app.app_id

    def construct(self):
        self.image = self.sdk.Image.from_registry('python:3.13.14-slim').run_function(
            install_pins, args=(self.requirements, self.deadline), cpu=(1,1), memory=(8192,8192),
            timeout=600, include_source=False)

    async def build(self):
        # Same recipe and monitored budget formula as original. No retry/rebuild.
        started, last_bill, delta = time.monotonic(), 0.0, 0.0
        task = None
        try:
            with self.sdk.enable_output():
                task = asyncio.create_task(self.image.build(self.app))
                while not task.done():
                    elapsed = time.monotonic() - started
                    if elapsed-last_bill >= 45 or last_bill == 0:
                        try:
                            summary = await bounded(self.workspace.billing.summary(), 10, 0.1)
                            delta = max(0, float(summary.metered_cost)-float(self.baseline.metered_cost))
                            self.record("billing", dataclasses.asdict(summary))
                        except Exception as exc:
                            self.record("billing_error", {"error": repr(exc)})
                        last_bill = max(elapsed, 0.001)
                    estimate = .65 + elapsed*(.0000131+8*.00000222)
                    self.record("cost", {"estimate": estimate, "management_value": max(estimate, delta)})
                    if max(estimate, delta) >= 4 or time.time() >= self.deadline-45:
                        raise TimeoutError("Preparation time/cost stop")
                    await asyncio.wait({task}, timeout=10)
                await task
            return self.image.object_id
        finally:
            if task is not None and not task.done():
                task.cancel()  # Parent controller/launcher bounds remaining tasks.

    async def stop(self, app_id):
        pb = self.sdk.pb
        await self.client._stub.AppStop(pb.AppStopRequest(app_id=app_id, source=pb.APP_STOP_SOURCE_CLI))

    async def query(self, app_id):
        pb = self.sdk.pb
        info = await self.client._stub.AppGetInfo(pb.AppGetInfoRequest(app_id=app_id))
        tasks = await self.client._stub.TaskList(pb.TaskListRequest(app_id=app_id))
        # Fail closed: only explicit STOPPED and complete empty task query suffice.
        return {"stopped": info.info.lifecycle.app_state == pb.APP_STATE_STOPPED,
                "task_count": len(tasks.tasks)}


async def bounded(awaitable, seconds, cancel_grace=0.03):
    """wait_for/gather can wait indefinitely when cancellation is suppressed."""
    task = asyncio.create_task(awaitable)
    done, _ = await asyncio.wait({task}, timeout=max(0, seconds))
    if done:
        return task.result()
    task.cancel()
    done, _ = await asyncio.wait({task}, timeout=max(0, cancel_grace))
    if done:
        # Retrieve cancellation/error without replacing the primary timeout.
        try:
            task.result()
        except BaseException:
            pass
    raise TimeoutError("Operation deadline; cancellation completion not assumed")


async def run_controller(transport, output, phase=0.12, cleanup_total=0.35):
    output = Path(output)
    result = {"outcome": "NOT_STARTED", "owned_app_id": None, "stop_ack": False,
              "termination": "UNCONFIRMED", "create_attempts": 0, "build_attempts": 0,
              "stop_attempts": 0, "cleanup_errors": [], "execution": "INJECTED_LOCAL_ONLY"}
    def persist():
        write_json(output / "result.json", result)
    started = time.monotonic()
    try:
        # Entire preparation/creation/construction lies inside cleanup boundary.
        await bounded(transport.prepare(), phase)
        result["create_attempts"] = 1
        persist()  # Intent persisted BEFORE request, including unknown-ID case.
        app_id = await bounded(transport.create(), phase)
        if not isinstance(app_id, str) or not app_id:
            raise RuntimeError("Missing owned App ID")
        result["owned_app_id"] = app_id
        persist()
        transport.construct()
        result["build_attempts"] = 1
        persist()
        result["image_id"] = await bounded(transport.build(), phase)
        result["outcome"] = "BUILD_COMPLETED"
    except BaseException as exc:
        result.update(outcome="BUILD_FAILED", error=repr(exc), traceback=traceback.format_exc())
        # Persist original exception BEFORE cancellation/stop/query work.
        persist()
    finally:
        cleanup_start = time.monotonic()
        deadline = cleanup_start + cleanup_total
        app_id = result["owned_app_id"]
        if app_id is None:
            result["termination"] = ("ID_UNKNOWN" if result["create_attempts"] else "NO_CREATE_ATTEMPT")
        else:
            result["stop_attempts"] = 1
            persist()
            try:
                remaining = max(0, deadline-time.monotonic())
                await bounded(transport.stop(app_id), min(phase, remaining), 0)
                result["stop_ack"] = True
            except BaseException as exc:
                result["cleanup_errors"].append({"stage": "stop", "error": repr(exc)})
            # One exact-ID status pair, no stop reissue or create/discovery retry.
            remaining = max(0, deadline-time.monotonic())
            if remaining > 0:
                try:
                    observed = await bounded(transport.query(app_id), min(phase, remaining), 0)
                    result["termination_observation"] = observed
                    if observed["stopped"] is True and observed["task_count"] == 0:
                        result["termination"] = "TERMINAL_TASK0_CONFIRMED"
                except BaseException as exc:
                    result["cleanup_errors"].append({"stage": "query", "error": repr(exc)})
        result["cleanup_seconds"] = time.monotonic()-cleanup_start
        result["elapsed_seconds"] = time.monotonic()-started
        persist()
    return result

def install_pins(requirements, absolute_deadline):
    import json
    from pathlib import Path
    import subprocess
    import sys
    import time
    if sys.version_info[:3] != (3, 13, 14):
        raise RuntimeError('Pinned Python unavailable')
    pins = Path('/a040-requirements.txt')
    pins.write_text(requirements)
    seconds = min(600, int(absolute_deadline-time.time())-30)
    if seconds <= 0:
        raise TimeoutError('Preparation deadline before installer')
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-cache-dir',
                    '--only-binary=:all:', '--extra-index-url',
                    'https://download.pytorch.org/whl/cu126', '-r', str(pins),
                    '--report', '/a040-install-report.json'], check=True, timeout=seconds)
    inventory = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze', '--all'], text=True)
    Path('/a040-linux-requirements.lock.txt').write_text(inventory)
    print('A040_LINUX_PINS='+json.dumps(inventory), flush=True)

