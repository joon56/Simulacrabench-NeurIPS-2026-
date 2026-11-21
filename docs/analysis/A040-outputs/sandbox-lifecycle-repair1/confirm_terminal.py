"""Single authorized metadata/termination window; never create or hydrate a Sandbox."""
import asyncio
from datetime import datetime, timezone, timedelta
import json
import os
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
APP = "ap-XiMVzlJgrNrCiFpIN1kB4W"
APP_NAME = "a040-resume5-20261005-094405"
NAME = APP_NAME + "-gpu"
START = time.monotonic()
NOW = datetime.now(timezone.utc)
RECEIPT = {"workspace": "joon56", "environment": "main", "app_id": APP,
           "app_name": APP_NAME, "sandbox_name": NAME, "sandbox_id": None,
           "terminal": "UNCONFIRMED", "terminate_requests": 0,
           "calls": [], "new_resources": 0, "remote_commands": 0,
           "remote_file_operations": 0, "errors": []}


def save():
    RECEIPT["observed_utc"] = datetime.now(timezone.utc).isoformat()
    RECEIPT["observed_kst"] = datetime.now(timezone(timedelta(hours=9))).isoformat()
    RECEIPT["elapsed_seconds"] = time.monotonic() - START
    (HERE / "termination-billing-receipt.json").write_text(
        json.dumps(RECEIPT, indent=2), encoding="utf-8")


with (HERE / "remote-window.json").open("x", encoding="utf-8") as stream:
    json.dump({"started_utc": NOW.isoformat(), "deadline_utc": (NOW + timedelta(seconds=120)).isoformat(),
               "discovery_cutoff_utc": (NOW + timedelta(seconds=90)).isoformat(),
               "call_cap_seconds": 15, "final_evidence_reserve_seconds": 30,
               "allowed_calls": ["Client.from_env", "WorkspaceNameLookup", "AppLookup", "AppGetInfo",
                                 "TaskList", "SandboxList(include_finished=True)", "SandboxWait",
                                 "SandboxTerminate(max1)", "WorkspaceBillingSummary"],
               "forbidden": "create/build/exec/files/transfer", "app_id": APP, "sandbox_name": NAME}, stream, indent=2)
save()

from modal.client import _Client
from modal._utils.async_utils import synchronizer
from modal_proto import api_pb2 as pb
from google.protobuf.empty_pb2 import Empty


async def call(name, factory, evidence=False):
    remaining = (119 if evidence else 89) - (time.monotonic() - START)
    if remaining <= 0:
        raise TimeoutError("Remote window cutoff")
    cap = min(14.5, remaining)
    row = {"method": name, "started_utc": datetime.now(timezone.utc).isoformat(), "cap_seconds": cap}
    RECEIPT["calls"].append(row)
    save()
    task = asyncio.create_task(factory(cap))
    done, _ = await asyncio.wait({task}, timeout=cap)
    if not done:
        task.cancel()
        row["outcome"] = "TIMEOUT"
        save()
        raise TimeoutError(name)
    try:
        value = task.result()
    except BaseException as exc:
        row["outcome"] = type(exc).__name__
        save()
        raise
    row["outcome"] = "RETURNED"
    row["finished_utc"] = datetime.now(timezone.utc).isoformat()
    save()
    return value


def result_metadata(result):
    return {"status": int(result.status), "status_name": pb.GenericResult.GenericStatus.Name(result.status),
            "exitcode": int(result.exitcode)}


async def main():
    client = None
    try:
        client = await call("Client.from_env", lambda _: _Client.from_env())
        if client._cancellation_context_event_loop is not asyncio.get_running_loop():
            raise RuntimeError("Managed client loop mismatch")
        workspace = await call("WorkspaceNameLookup", lambda cap: client._stub.WorkspaceNameLookup(Empty(), timeout=cap))
        if workspace.username != "joon56":
            raise RuntimeError("Workspace mismatch")
        app_identity = await call("AppGetInfo", lambda cap: client._stub.AppGetInfo(
            pb.AppGetInfoRequest(app_id=APP), timeout=cap))
        info = app_identity.info
        if (info.app_id, info.description, info.environment_name) != (APP, APP_NAME, "main"):
            raise RuntimeError("App name/ID/environment mismatch")
        RECEIPT["identity"] = {"app_id": info.app_id, "description": info.description,
                               "environment": info.environment_name, "workspace": workspace.username}
        before = 0.0
        matches = []
        for _ in range(3):
            listing = await call("SandboxList", lambda cap: client._stub.SandboxList(
                pb.SandboxListRequest(app_id=APP, environment_name="main", include_finished=True,
                                      before_timestamp=before), timeout=cap))
            matches.extend(row for row in listing.sandboxes if row.app_id == APP and row.name == NAME)
            if matches or not listing.sandboxes:
                break
            before = min(row.created_at for row in listing.sandboxes)
        if len(matches) != 1 or not matches[0].id:
            raise RuntimeError("Unique exact-name finished-inclusive metadata unavailable")
        row = matches[0]
        RECEIPT["sandbox_id"] = row.id
        RECEIPT["sandbox_metadata"] = {"id": row.id, "name": row.name, "app_id": row.app_id,
            "created_at": row.created_at, "image_id": row.image_id,
            "list_include_finished": True, "task_result": result_metadata(row.task_info.result)}
        save()
        wait = await call("SandboxWait", lambda cap: client._stub.SandboxWait(
            pb.SandboxWaitRequest(sandbox_id=row.id, timeout=0), timeout=cap), evidence=True)
        RECEIPT["sandbox_result"] = result_metadata(wait.result)
        if wait.result.status == pb.GenericResult.GENERIC_STATUS_UNSPECIFIED:
            if time.monotonic() - START >= 89:
                raise TimeoutError("No new termination request after discovery cutoff")
            RECEIPT["terminate_requests"] = 1
            save()
            await call("SandboxTerminate", lambda cap: client._stub.SandboxTerminate(
                pb.SandboxTerminateRequest(sandbox_id=row.id), timeout=cap))
            wait = await call("SandboxWait", lambda cap: client._stub.SandboxWait(
                pb.SandboxWaitRequest(sandbox_id=row.id, timeout=min(10, cap)), timeout=cap), evidence=True)
            RECEIPT["sandbox_result"] = result_metadata(wait.result)
        if wait.result.status in range(1, 9):
            RECEIPT["terminal"] = "SANDBOX_TERMINAL_CONFIRMED"
        save()
        info = await call("AppGetInfo", lambda cap: client._stub.AppGetInfo(pb.AppGetInfoRequest(app_id=APP), timeout=cap), evidence=True)
        tasks = await call("TaskList", lambda cap: client._stub.TaskList(pb.TaskListRequest(app_id=APP), timeout=cap), evidence=True)
        RECEIPT["app"] = {"state": int(info.info.lifecycle.app_state), "tasks": len(tasks.tasks),
                          "stopped_task0": info.info.lifecycle.app_state == pb.APP_STATE_STOPPED and len(tasks.tasks) == 0}
        request = pb.WorkspaceBillingSummaryRequest()
        request.start_timestamp.FromDatetime(datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0))
        bill = await call("WorkspaceBillingSummary", lambda cap: client._stub.WorkspaceBillingSummary(request, timeout=cap), evidence=True)
        RECEIPT["billing"] = {"metered_cost": bill.metered_cost, "billed_cost": bill.billed_cost,
            "metered_breakdown": dict(bill.metered_cost_breakdown), "attribution": "WORKSPACE_AGGREGATE_NOT_TASK_INVOICE",
            "posting_delay_unknown": True}
    except BaseException as exc:
        RECEIPT["errors"].append({"type": type(exc).__name__, "stage": RECEIPT["calls"][-1]["method"] if RECEIPT["calls"] else "import"})
    finally:
        save()


if __name__ == "__main__":
    synchronizer.create_blocking(main)()
    print(json.dumps({k: RECEIPT.get(k) for k in ("terminal", "sandbox_id", "terminate_requests", "app", "billing", "errors", "elapsed_seconds")}))
