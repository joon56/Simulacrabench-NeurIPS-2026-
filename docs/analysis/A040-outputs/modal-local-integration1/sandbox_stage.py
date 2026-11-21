"""Fixed all3 target phase ordering, time gates, export and named output checks."""
import json
import time
from contract import CAP_BYTES, GPU_PLAN, REMOTE_DIR, sha

BOUNDARY_COMMAND = ("python", "-I", "-B", "-u", REMOTE_DIR + "/linux_boundary.py")


async def command(sandbox, args, timeout, operation):
    process = await operation(sandbox.exec(*args, timeout=timeout, text=True), "exec_start")
    # Consume both pipes concurrently so a verbose command cannot deadlock.
    import asyncio
    stdout, stderr, code = await operation(asyncio.gather(process.stdout.read(), process.stderr.read(), process.wait()), "process", timeout+10)
    return {"stdout": stdout, "stderr": stderr, "exit_code": code}


def validate_boundary(value):
    required = ("source_payload_verified", "native_network_blocked", "swap_disabled", "gpu_h100_single",
                "python_pins_match", "duplicate_latch_guard", "two_logical_affinity")
    if value.get("outcome") != "BOUNDARY_PASS" or any(value.get(k) is not True for k in required):
        raise RuntimeError("Target boundary incomplete or failed")
    if value.get("memory_limit_bytes") != CAP_BYTES or value.get("physical_cpu_limit") != 1:
        raise RuntimeError("Target cgroup limits not the fixed contract")


async def execute(context):
    plan, endpoint, payload, state = context.plan, context.endpoint, context.payload, context.state
    plan.require_time(2400, "gpu")
    if plan.whole_deadline-time.time() < 2400+1200:
        raise TimeoutError("No whole GPU/closeout window")
    context.costs.gate(GPU_PLAN)
    state["payload"] = payload.verify()
    state["sandbox_intent"] = True
    context.persist()
    state["sandbox_id"] = await context.op(endpoint.sandbox_create(plan.app_name + "-gpu"), "sandbox_create", 120)
    if not state["sandbox_id"]:
        raise RuntimeError("Sandbox ID missing")
    context.gpu_deadline = min(plan.gpu_latest_end, time.time()+2400)
    context.costs.gpu_started = time.monotonic()
    context.persist()
    state["transfer"] = await payload.transfer(endpoint.sandbox.filesystem, context.op)
    # Immutable per-attempt target config; credentials never appear in it.
    config = {"files": payload.files, "gpu_deadline": context.gpu_deadline,
              "image_id": state["image_id"], "pins": context.pins,
              "scope": plan.scope, "scientific_seconds": 900, "expected_vectors": 189649,
              "expected_heads": 213, "memory_cap": CAP_BYTES}
    await context.op(endpoint.sandbox.filesystem.write_bytes(json.dumps(config).encode(), REMOTE_DIR + "/target-contract.json"), "transfer")
    state["boundary_intent"] = True
    context.persist()
    boundary = await command(endpoint.sandbox, BOUNDARY_COMMAND, 60, context.op)
    context.save("boundary-process.json", boundary)
    if boundary["exit_code"] != 0:
        raise RuntimeError("Target boundary process failed")
    boundary_data = json.loads(await context.op(endpoint.sandbox.filesystem.read_bytes(REMOTE_DIR + "/boundary-result.json"), "export"))
    context.save("boundary-result.json", boundary_data)
    validate_boundary(boundary_data)
    inventory = await context.op(endpoint.sandbox.filesystem.read_bytes(REMOTE_DIR + "/linux-requirements.json"), "export")
    context.save_bytes("linux-requirements.json", inventory)
    state["boundary"] = "PASS_WITHIN_EXECUTION_SCOPE"
    for mode in ("reference", "candidate"):
        remaining = context.gpu_deadline-time.time()
        needed = 1900 if mode == "reference" else 950
        if remaining < needed:
            raise TimeoutError("Insufficient complete scientific phase time")
        context.costs.observe(await context.op(endpoint.billing(), "billing"))
        context.costs.gate(0)
        context.latch(mode)
        state[mode + "_intent"] = True
        context.persist()
        args = ("python", "-I", "-B", "-u", REMOTE_DIR + "/linux_watchdog.py", mode)
        process = await command(endpoint.sandbox, args, 925, context.op)
        context.save(mode + "-process.json", process)
        # Export the fixed mode artifacts even when its process failed.
        result = await export_mode(context, mode)
        if process["exit_code"] != 0 or result["resources"].get("child_exit") != 0:
            raise RuntimeError(mode + " process failed")
        expected = "REFERENCE_PASS" if mode == "reference" else "LOCAL_FULL_PATH_PASS"
        if result["result"].get("outcome") != expected or result["resources"].get("outcome") != expected:
            raise RuntimeError(mode + " named contract not passed")
        if result["resources"].get("elapsed_seconds", 901) > 900 or not result["result"].get("full_path_completed"):
            raise RuntimeError(mode + " timing or completeness failed")
        if sum(result["result"].get("output_counts", {}).values()) != 189649:
            raise RuntimeError(mode + " canonical vector count failed")
        state[mode] = "PASS_WITHIN_EXECUTION_SCOPE"
        context.persist()


async def export_mode(context, mode):
    collected = {}
    for name in ("result.json", "resources.json", "events.jsonl", "resource-samples.jsonl", "stdout.txt", "stderr.txt"):
        path = REMOTE_DIR + "/" + mode + "/" + name
        try:
            raw = await context.op(context.endpoint.sandbox.filesystem.read_bytes(path), "export", 20)
            context.save_bytes(mode + "/" + name, raw)
            if name in ("result.json", "resources.json"):
                collected[name[:-5]] = json.loads(raw)
        except Exception as exc:
            context.event("partial_export", mode=mode, artifact=name, error=repr(exc))
    if "result" not in collected or "resources" not in collected:
        raise RuntimeError(mode + " result/resources export incomplete")
    # Export only fixed output names, verifying the runner's byte hashes.
    hashes = collected["result"].get("output_hashes", {})
    required = {"unicef", "wb", "unhcr"}
    if mode == "candidate":
        required |= {"unhcr-engineering-alpha025", "unhcr-final-e041"}
    if collected["result"].get("full_path_completed") and set(hashes) != required:
        raise RuntimeError("Output export manifest mismatch")
    if not set(hashes) <= required:
        raise RuntimeError("Unexpected output export path")
    for name, expected in hashes.items():
        raw = await context.op(context.endpoint.sandbox.filesystem.read_bytes(
            "/work/tmp/a040-modal-local-integration1/" + mode + "/" + name + ".json"), "export", 30)
        if sha(raw) != expected:
            raise ValueError("Exported output identity mismatch")
        context.save_bytes(mode + "/outputs/" + name + ".json", raw)
    return collected
