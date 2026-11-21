"""Normal SDK authentication; read-only, minimized account evidence. No resources."""
import asyncio
import dataclasses
import json
from datetime import datetime, timezone
from pathlib import Path
from modal._workspace import _Workspace
from modal._environments import _Environment
from modal_proto import api_pb2

async def main():
    out = {"recorded_utc": datetime.now(timezone.utc).isoformat(), "resource_requests": 0}
    ws = await _Workspace.from_context().hydrate()
    out["workspace"] = ws.name
    if ws.name != "joon56":
        raise RuntimeError("WORKSPACE_MISMATCH")
    out["settings"] = dataclasses.asdict(await ws.settings.list())
    summary = await ws.billing.summary()
    out["billing_summary"] = dataclasses.asdict(summary)
    env = await _Environment.from_context(client=ws.client).hydrate()
    try:
        budget = await ws.client._stub.EnvironmentGetBudget(
            api_pb2.EnvironmentGetBudgetRequest(environment_id=env.object_id))
        out["environment_budget"] = {f.name: getattr(budget, f.name) for f in budget.DESCRIPTOR.fields}
        out["environment_budget_caution"] = "Effective environment fields do not independently identify workspace gross/net settings or unused credits."
    except Exception as exc:
        out["environment_budget_error_type"] = type(exc).__name__
    out["credits_remaining_independently_verified"] = False
    target = Path(__file__).with_name("account-read.json")
    with target.open("x", encoding="utf-8") as stream:
        json.dump(out, stream, indent=2, default=str)
    print(json.dumps(out, default=str))

asyncio.run(asyncio.wait_for(main(), timeout=45))
