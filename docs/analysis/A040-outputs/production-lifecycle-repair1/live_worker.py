"""One production orchestration; only external endpoints are injected in tests."""
import asyncio
from dataclasses import asdict
import json
import os
from pathlib import Path
import time
import traceback

from contract import Costs, verify_sources
from controller_core import bounded
from protocol import validate_base, validate_image_id, termination_observation
from sandbox_stage import execute


class Context:
    def __init__(self, directory, plan, endpoint, payload, pins):
        self.directory = Path(directory)
        self.plan, self.endpoint, self.payload, self.pins = plan, endpoint, payload, pins
        self.costs = Costs()
        self.endpoint.journal = self.mutation_intent
        self.gpu_deadline = None
        self.state = {"scope": plan.scope, "outcome": "NOT_STARTED", "app_name": plan.app_name,
                      "create_intent": False, "build_intent": False, "sandbox_intent": False,
                      "app_id": None, "sandbox_id": None, "image_id": None,
                      "actual_remote_facts": "UNVERIFIED" if plan.scope != "LIVE" else "PENDING"}

    def mutation_intent(self, kind, request):
        self.latch("sandbox-" + kind + "-rpc")
        self.state["sandbox_" + kind + "_rpc_intent"] = True
        if kind == "terminate":
            self.state["terminate_sandbox_id"] = request.sandbox_id
        self.persist()

    def save_bytes(self, name, raw):
        from contract import safe_relative
        safe_relative(name)
        path = self.directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".tmp")
        with temporary.open("wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)

    def save(self, name, value):
        self.save_bytes(name, json.dumps(value, indent=2, ensure_ascii=False).encode("utf-8"))

    def persist(self):
        self.save("state.json", self.state)

    def event(self, name, **values):
        with (self.directory / "events.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"event": name, "time": time.time(), **values}, ensure_ascii=False) + "\n")
            stream.flush()

    def latch(self, name):
        with (self.directory / (name + "-started.json")).open("x", encoding="utf-8") as stream:
            json.dump({"scope": self.plan.scope, "app_name": self.plan.app_name, "time": time.time()}, stream)
            stream.flush()
            os.fsync(stream.fileno())

    async def op(self, awaitable, stage, seconds=None):
        end = (self.gpu_deadline - 60) if self.gpu_deadline else (self.plan.prepare_deadline - 60)
        remaining = min(end, self.plan.whole_deadline - 60) - time.time()
        timeout = min(self.plan.operation_timeout if seconds is None else seconds, remaining)
        if timeout <= 0:
            if hasattr(awaitable, "close"):
                awaitable.close()
            elif isinstance(awaitable, asyncio.Future):
                awaitable.cancel()
            raise TimeoutError("Operation deadline: " + stage)
        self.event("operation", stage=stage, timeout=timeout)
        return await bounded(awaitable, timeout, self.plan.cancel_grace)


async def build(context):
    context.plan.require_time(1000)
    context.costs.gate(.20)
    context.state["create_intent"] = True
    context.persist()
    context.state["app_id"] = await context.op(context.endpoint.app_lookup(context.plan.app_name, True), "app_create")
    if not context.state["app_id"]:
        raise RuntimeError("App ID missing")
    context.persist()
    context.state["build_intent"] = True
    context.costs.prepare_started = time.monotonic()
    context.persist()
    task = asyncio.create_task(context.endpoint.build(context.plan.base_id, context.pins,
                                min(context.plan.prepare_deadline - 75, time.time() + 900)))
    start, last_bill = time.monotonic(), float("-inf")
    try:
        while not task.done():
            if time.monotonic() - last_bill >= 45:
                context.costs.observe(await context.op(context.endpoint.billing(), "build_billing"))
                last_bill = time.monotonic()
            context.costs.gate(0)
            if time.monotonic() - start >= context.plan.build_timeout or time.time() >= context.plan.prepare_deadline - 75:
                raise TimeoutError("Image preparation cap")
            await asyncio.wait({task}, timeout=context.plan.poll_seconds)
        context.state["image_id"] = await task
        if not context.state["image_id"]:
            raise RuntimeError("Completed image ID missing")
        context.persist()
    finally:
        if not task.done():
            task.cancel()
            done, _ = await asyncio.wait({task}, timeout=context.plan.cancel_grace)
            if not done:
                context.state["unsettled_build_task"] = True
        if task.done() and not task.cancelled():
            task.exception()


async def cleanup(context):
    from cleanup_query import CleanupQuery
    started = time.monotonic()
    total = min(context.plan.cleanup_timeout, max(0, context.plan.whole_deadline-time.time()))
    deadline = started + total
    endpoint, state = context.endpoint, context.state
    receipt = {"scope": context.plan.scope, "termination": "UNCONFIRMED", "errors": [], "observations": []}

    async def attempt(name, awaitable):
        try:
            left = deadline-time.monotonic()
            if left <= 0:
                if hasattr(awaitable, "close"):
                    awaitable.close()
                raise TimeoutError("Entire cleanup cap")
            return await bounded(awaitable, min(14.5, left), min(.1, left))
        except BaseException as exc:
            receipt["errors"].append({"stage": name, "error": repr(exc)})
            return None

    def save_query(value):
        if value.get("sandbox_id"):
            state["sandbox_id"] = value["sandbox_id"]
        context.save("sandbox-query-receipt.json", value)
        if value["terminal"] == "TERMINAL_CONFIRMED" and "sandbox_terminal" not in receipt:
            receipt["sandbox_terminal"] = value["sandbox_result"]
            receipt["sandbox_id"] = value["sandbox_id"]
            receipt["terminal_source"] = value["terminal_source"]
            receipt["terminal_observed_utc"] = value["observed_utc"]
            context.save("sandbox-terminal-evidence.json", receipt)
        context.persist()

    try:
        if state["create_intent"] and not state["app_id"]:
            state["app_id"] = await attempt("app_id_recovery", endpoint.app_lookup(context.plan.app_name, False))
            context.persist()
        if state["sandbox_intent"] and state["app_id"] and endpoint.client is not None:
            query = CleanupQuery(save_query, state["app_id"], context.plan.app_name,
                total=max(0, deadline-time.monotonic()), reserve=min(15, total/3), call_cap=14.5)
            # SDK create may itself attempt termination on scheduling failure.
            # The mutation-boundary journal covers both that path and this query.
            query.receipt["terminate_requests"] = int(bool(state.get("sandbox_terminate_rpc_intent")))
            async def existing_client():
                return endpoint.client
            result = await query.run(existing_client)
            receipt["errors"].extend(result["errors"])
            if result.get("billing") is not None:
                receipt["billing_final"] = result["billing"]
                context.costs.posted = max(context.costs.posted, float(result["billing"]["metered_cost"]))
                if float(result["billing"]["billed_cost"]) != 0:
                    receipt["errors"].append({"stage": "final_billing", "error": "Cash billing contradiction"})
        if not state["create_intent"]:
            receipt["termination"] = "NO_CREATE_ATTEMPT"
        elif state["app_id"]:
            await attempt("app_stop", endpoint.stop_app(state["app_id"]))
            info = await attempt("app_info", endpoint.app_info(state["app_id"]))
            tasks = await attempt("tasks", endpoint.tasks(state["app_id"]))
            if info is not None and tasks is not None:
                observation = termination_observation(info, tasks)
                receipt["observations"].append(observation)
                sandbox_proved = not state["sandbox_intent"] or "sandbox_terminal" in receipt
                if observation["confirmed"] and sandbox_proved and not state.get("unsettled_build_task"):
                    receipt["termination"] = "TERMINAL_TASK0_CONFIRMED"
        if endpoint.client is not None and "billing_final" not in receipt:
            summary = await attempt("final_billing", endpoint.billing())
            if summary is not None:
                context.costs.observe(summary)
                receipt["billing_final"] = {"metered": summary.metered_cost, "billed": summary.billed_cost}
    finally:
        receipt["elapsed_seconds"] = time.monotonic()-started
        state["termination"] = receipt["termination"]
        context.save("termination-receipt.json", receipt)
        context.persist()
    return receipt


async def run(context, source_manifest, source_directory):
    started = time.monotonic()
    # No endpoint, source data, or overwrite before unique local run ownership.
    context.plan.check()
    source_gate = verify_sources(source_directory, source_manifest)
    context.directory.mkdir(parents=True, exist_ok=False)
    context.latch("attempt")
    context.save("source-gate.json", source_gate)
    context.save("plan.json", asdict(context.plan))
    complete = False
    try:
        context.state["workspace"] = await context.op(context.endpoint.connect(), "connect", 60)
        context.costs.observe(await context.op(context.endpoint.billing(), "billing"))
        context.state["base"] = await context.op(validate_base(context.endpoint.base_stream(context.plan.base_id), context.plan.base_result_sha256), "base_stream")
        context.state["base_metadata_sha256"] = validate_image_id(await context.op(context.endpoint.image_info(context.plan.base_id), "base_identity"), context.plan.base_id)
        await build(context)
        await execute(context)
        complete = True
    except BaseException as exc:
        context.state.update(outcome="STOP_FIRST_ERROR", error=repr(exc), traceback=traceback.format_exc())
        context.event("first_error", error=repr(exc))
    finally:
        try:
            receipt = await cleanup(context)
            if receipt["errors"]:
                context.state["cleanup_error"] = "Cleanup stage errors retained in termination receipt"
        except BaseException as exc:
            context.state["cleanup_error"] = repr(exc)
            context.state["termination"] = "UNCONFIRMED"
        confirmed = context.state.get("termination") == "TERMINAL_TASK0_CONFIRMED"
        if complete and confirmed and not context.state.get("cleanup_error"):
            context.state["outcome"] = "LOCAL_PROTOCOL_PATH_PASS" if context.plan.scope == "LOCAL_PROTOCOL_FIXTURE" else "H100_FULL_PATH_PASS"
        elif complete:
            context.state["outcome"] = "STOP_CLEANUP_UNCONFIRMED"
        context.state["elapsed_seconds"] = time.monotonic() - started
        context.save("cost-ledger.json", {"scope": context.plan.scope, "management_estimate": context.costs.value(),
            "posted_evidence": context.costs.posted, "actual_cost_this_local_fixture": 0 if context.plan.scope != "LIVE" else None,
            "prior_component": .00001152, "cash_authority": 0, "total_plan": 5,
            "invoice_attribution": "UNVERIFIED", "historical_active_seconds": 14777.0797748,
            "gpu_request_reservation": context.costs.gpu_reservation, "gpu_actual_seconds": None,
            "reservation_is_invoice": False, "historical_workspace_metered": .01009897,
            "historical_2400s_reservation": 2.965933453125})
        context.persist()
        context.save("result.json", context.state)
    return context.state
