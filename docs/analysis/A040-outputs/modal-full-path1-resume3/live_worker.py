"""One real Modal preparation and conditional fixed target workflow; no retry."""
import asyncio
import base64
import dataclasses
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import traceback

from controller_core import bounded, install_pins
from live_binding import SDK, image_from_id

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ENTRY = json.loads((HERE / "entry.json").read_text(encoding="utf-8-sig"))
PREP_END = datetime.fromisoformat(ENTRY["preparation_deadline_utc"].replace("Z", "+00:00")).timestamp()
WHOLE_END = datetime.fromisoformat(ENTRY["whole_deadline_utc"].replace("Z", "+00:00")).timestamp()
APP_NAME = "a040-resume3-20261004-123330"
BASE = "im-eWgRNij0VH6mzozlOzEyxy"
STATE = {"execution": "REAL_MODAL_RESUME3", "outcome": "PREPARING", "app_id": None,
         "app_name": APP_NAME, "sandbox_id": None, "create_attempts": 0, "build_attempts": 0,
         "scientific_reference": 0, "scientific_candidate": 0, "termination": "UNCONFIRMED"}


def save(name, value):
    target = HERE / name
    temp = target.with_name(target.name + ".writing")
    with temp.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, default=str)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, target)


def event(kind, **values):
    with (HERE / "events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"utc": datetime.now(timezone.utc).isoformat(), "event": kind,
                                 **values}, default=str, ensure_ascii=False) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def persist():
    save("live-state.json", STATE)


class Context:
    client = workspace = app = image = sandbox = None
    build_started = None
    cumulative_posted = 0.00001152
    gpu_started = None

    async def bill(self):
        summary = await bounded(self.workspace.billing.summary(), 10, 2)
        data = dataclasses.asdict(summary)
        if float(summary.billed_cost) != 0:
            raise RuntimeError("Observed cash billing contradiction")
        components = sum(max(0, float(value)) for value in summary.metered_cost_breakdown.values())
        self.cumulative_posted = max(self.cumulative_posted, float(summary.metered_cost), components)
        event("billing", summary=data, cumulative_account_evidence=self.cumulative_posted,
              attribution="Account observation, not task-attributed final invoice")
        save("billing-latest.json", data)
        return data

    def management(self):
        elapsed = time.monotonic()-self.build_started if self.build_started else 0
        # Build estimate includes subsequent preparation wait conservatively.
        estimate = 0.00001152 + .65 + elapsed*(.0000131 + 8*.00000222)
        if self.gpu_started is not None:
            estimate += (time.monotonic()-self.gpu_started)*.00123580560546875
        return max(estimate, self.cumulative_posted)

    def gate(self, next_plan):
        value = self.management()
        event("cost_gate", management=value, next_plan=next_plan, sum=value+next_plan,
              threshold=4, unknown_prior_posting=True, exact_invoice_bound=False)
        if value+next_plan >= 4:
            raise RuntimeError("Cumulative planning gate reached; cleanup only")


async def base_identity(ctx):
    expected = json.loads((HERE.parent / "modal-full-path1-resume2/termination-receipt.json").read_text(encoding="utf-8-sig"))
    observed = None
    async def read_status():
        nonlocal observed
        request = SDK.pb.ImageJoinStreamingRequest(image_id=BASE, timeout=3)
        async for row in ctx.client._stub.ImageJoinStreaming.unary_stream(request):
            if row.result.status:
                observed = row.result
    await bounded(read_status(), 15, 2)
    if observed is None or observed.status != SDK.pb.GENERIC_STATUS_SUCCESS:
        raise RuntimeError("Saved base is not currently SUCCESS")
    if bytes(observed.data) != base64.b64decode(expected["image_result"]["data"]):
        raise RuntimeError("Saved base result identity mismatch")
    response = await bounded(ctx.client._stub.ImageFromId(SDK.pb.ImageFromIdRequest(image_id=BASE)), 10, 2)
    if response.image_id != BASE:
        raise RuntimeError("Base image ID mismatch")
    save("base-identity.json", {"image_id": BASE, "status": "GENERIC_STATUS_SUCCESS",
        "saved_result_bytes_equal": True, "result_sha256": hashlib.sha256(bytes(observed.data)).hexdigest(),
        "metadata_sha256": hashlib.sha256(response.metadata.SerializeToString()).hexdigest(),
        "complete_dependency_image": False})


async def cleanup(ctx):
    start = time.monotonic()
    # Reserve10s inside the60s cleanup budget for the final normal billing read.
    deadline = min(start+50, time.monotonic()+max(0, WHOLE_END-time.time()-25))
    receipt = {"app_id": STATE["app_id"], "sandbox_id": STATE["sandbox_id"], "errors": [],
               "app_stop_ack": False, "termination": "UNCONFIRMED", "observations": []}
    async def call(coro):
        remaining = max(0, deadline-time.monotonic())
        return await bounded(coro, min(10, remaining), 0)
    try:
        if ctx.client is None:
            receipt["termination"] = "NO_CLIENT_NO_RESOURCE"
            return
        if STATE["app_id"] is None and STATE["create_attempts"]:
            # Read-only lookup of this unique intent; never creates or builds.
            try:
                app = await call(SDK.App.lookup(APP_NAME, client=ctx.client, create_if_missing=False,
                                                environment_name="main"))
                STATE["app_id"] = app.app_id
                receipt["app_id"] = app.app_id
                event("lost_create_id_recovered_read_only", app_id=app.app_id)
                persist()
            except BaseException as exc:
                receipt["errors"].append({"stage": "lookup_own_intent", "error": repr(exc)})
        if ctx.sandbox is not None:
            try:
                await call(ctx.sandbox.terminate())
                receipt["sandbox_terminate_ack"] = True
            except BaseException as exc:
                receipt["errors"].append({"stage": "sandbox_terminate", "error": repr(exc)})
        app_id = STATE["app_id"]
        if not app_id:
            receipt["termination"] = "ID_UNKNOWN" if STATE["create_attempts"] else "NO_CREATE_ATTEMPT"
            return
        try:
            await call(ctx.client._stub.AppStop(SDK.pb.AppStopRequest(app_id=app_id, source=SDK.pb.APP_STOP_SOURCE_CLI)))
            receipt["app_stop_ack"] = True
        except BaseException as exc:
            receipt["errors"].append({"stage": "app_stop", "error": repr(exc)})
        while time.monotonic() < deadline-1:
            try:
                info = await call(ctx.client._stub.AppGetInfo(SDK.pb.AppGetInfoRequest(app_id=app_id)))
                tasks = await call(ctx.client._stub.TaskList(SDK.pb.TaskListRequest(app_id=app_id)))
                row = {"app_state": int(info.info.lifecycle.app_state), "task_count": len(tasks.tasks)}
                if ctx.sandbox is not None:
                    row["sandbox_returncode"] = await call(ctx.sandbox.poll())
                receipt["observations"].append(row)
                save("termination-receipt.json", receipt)
                if info.info.lifecycle.app_state == SDK.pb.APP_STATE_STOPPED and len(tasks.tasks) == 0 and (
                        ctx.sandbox is None or row["sandbox_returncode"] is not None):
                    receipt["termination"] = "TERMINAL_TASK0_CONFIRMED"
                    break
            except BaseException as exc:
                receipt["errors"].append({"stage": "query", "error": repr(exc)})
            await asyncio.sleep(min(2, max(0, deadline-time.monotonic())))
    finally:
        receipt["elapsed_seconds"] = time.monotonic()-start
        STATE["termination"] = receipt["termination"]
        save("termination-receipt.json", receipt)
        persist()


async def main():
    ctx = Context()
    try:
        # Exclusive attempt latch before any credentials or RPC.
        with (HERE / "live-started.json").open("x", encoding="utf-8") as stream:
            json.dump({"utc": datetime.now(timezone.utc).isoformat(), "pid": os.getpid(), "app_name": APP_NAME}, stream)
            stream.flush(); os.fsync(stream.fileno())
        preflight = json.loads((HERE / "preflight-result.json").read_text(encoding="utf-8"))
        if preflight["outcome"] != "LIVE_BINDING_PREFLIGHT_PASS":
            raise RuntimeError("New binding preflight missing")
        async def prepare():
            ctx.client = await SDK.Client.from_env()
            if ctx.client._cancellation_context_event_loop is not asyncio.get_running_loop():
                raise RuntimeError("Raw client event-loop mismatch")
            ctx.workspace = SDK.Workspace.from_context(client=ctx.client)
            await ctx.workspace.hydrate()
            if ctx.workspace.name != "joon56":
                raise RuntimeError("Workspace mismatch")
            baseline = await ctx.bill()
            save("billing-baseline.json", baseline)
            event("live_binding_confirmed", sdk="1.6.0", raw_client_same_loop=True, workspace="joon56")
        await bounded(prepare(), 60, 2)
        await bounded(base_identity(ctx), 30, 2)
        ctx.gate(.20)
        if PREP_END-time.time() < 1000:
            raise TimeoutError("Insufficient full image and cleanup time")
        STATE["create_attempts"] = 1
        persist()
        ctx.app = await bounded(SDK.App.lookup(APP_NAME, client=ctx.client, create_if_missing=True,
                                               environment_name="main"), 30, 2)
        STATE["app_id"] = ctx.app.app_id
        persist(); event("owned_app_id", app_id=ctx.app.app_id)
        pins_path = ROOT / "docs/analysis/A040-outputs/full-path-resume1/requirements.lock.txt"
        pin_bytes = pins_path.read_bytes()
        if hashlib.sha256(pin_bytes).hexdigest() != "6c6f0d0fc5db943eb1cb95ff4610ddea5df724bc50031b883a0dd67656771b70":
            raise RuntimeError("Pinned lock identity mismatch")
        ctx.image = image_from_id(BASE, ctx.client).run_function(install_pins,
            args=(pin_bytes.decode("utf-8-sig"), min(PREP_END-75, time.time()+900)),
            cpu=(1, 1), memory=(8192, 8192), timeout=600, include_source=False)
        if not isinstance(ctx.image, SDK.Image):
            raise TypeError("Image binding is not raw async")
        # Capture image IDs at the actual SDK join, without extra create/build.
        import modal._image as image_module
        original_join = image_module._image_await_build_result
        async def observed_join(image_id, client):
            event("image_join", image_id=image_id)
            return await original_join(image_id, client)
        image_module._image_await_build_result = observed_join
        STATE["build_attempts"] = 1
        persist()
        ctx.build_started = time.monotonic()
        with SDK.enable_output():
            task = asyncio.create_task(ctx.image.build(ctx.app))
            last_bill = 0
            try:
                while not task.done():
                    now = time.monotonic()
                    if now-last_bill >= 45:
                        await ctx.bill()
                        last_bill = now
                    ctx.gate(0)
                    if now-ctx.build_started >= 900 or time.time() >= PREP_END-75:
                        raise TimeoutError("Image preparation deadline")
                    await asyncio.wait({task}, timeout=5)
                await task
            finally:
                if not task.done():
                    task.cancel()
                    await asyncio.wait({task}, timeout=2)
        STATE.update(outcome="IMAGE_READY", image_id=ctx.image.object_id)
        persist(); save("image-result.json", {**STATE, "seconds": time.monotonic()-ctx.build_started})
        # Port work may finish during build; only explicit frozen gate continues.
        while not (HERE / "continue-sandbox.json").exists():
            if time.time() >= PREP_END-75:
                raise TimeoutError("Port/freeze not ready within preparation deadline")
            ctx.gate(0)
            await asyncio.sleep(5)
        from sandbox_stage import execute
        await execute(ctx, STATE, save, event, persist)
        STATE["outcome"] = "H100_FULL_PATH_PASS"
    except BaseException as exc:
        STATE.update(outcome="STOP_FIRST_ERROR", error=repr(exc), traceback=traceback.format_exc())
        persist(); event("first_error", error=repr(exc), stage_state=dict(STATE))
        print(traceback.format_exc(), file=sys.stderr, flush=True)
    finally:
        try:
            await cleanup(ctx)
        except BaseException as exc:
            STATE["cleanup_error"] = repr(exc)
            persist()
        if ctx.workspace is not None:
            try:
                await bounded(ctx.bill(), 10, 0)
            except BaseException as exc:
                event("final_billing_unavailable", error=repr(exc))
        save("cost-ledger.json", {"prior_ledger": "../modal-full-path1-resume2/cost-ledger.json",
             "planning_preparation": 1, "planning_total": 5, "cash_authority": 0,
             "cumulative_account_evidence": ctx.cumulative_posted, "management_estimate": ctx.management(),
             "final_task_attributed_cost": None, "unposted_retry_transfer_storage_unknown": True,
             "historical_apps_component": .00001152, "active_prior_seconds": 4477.3871369})
        save("result.json", STATE)
    return 0 if STATE["outcome"] == "H100_FULL_PATH_PASS" and STATE["termination"] == "TERMINAL_TASK0_CONFIRMED" else 1


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="strict", line_buffering=True)
    # No local helpers are needed by this pinned raw SDK workflow. Fail closed.
    def deny_helpers(name, args):
        if name in ("subprocess.Popen", "os.system", "os.posix_spawn"):
            raise PermissionError("Live worker may not spawn unowned local helpers")
    sys.addaudithook(deny_helpers)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    code = loop.run_until_complete(main())
    sys.stdout.flush(); sys.stderr.flush()
    os._exit(code)  # Parent owns lifetime; no unbounded SDK/asyncio shutdown gather.
