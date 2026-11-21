# A040 exact-resource check — STOP_TERMINATION_UNCONFIRMED

2026-10-05. S1 technical. The current attachment activated only existing-resource
status/necessary termination and conditional local repair. Resume5 remains consumed.

**STOP_TERMINATION_UNCONFIRMED / QUERY_ARGUMENT_CONTRACT_FAIL**.
The new query helper failed before obtaining fresh workspace/App/Sandbox/billing
evidence. The conditional production repair and local regression did not start.

Observed execution: one hidden existing-SDK process, CPU affinity3/two logical
CPUs. SDK-managed loop, normal `_Client.from_env()` returned. The next
WorkspaceNameLookup wrapper raised InvalidError. Receipt wall1.2158657s, at
2026-10-05T11:09:18.491885Z /20:09:18.491892KST. New remote window was registered
11:09:17.276031Z to11:11:17.276031Z, calls<=15s, final30s reserved. No fresh
window, second process or additional remote call followed the failure.

Cause found by reading installed SDK source after failure: the new helper passes
`timeout=cap` without `retry=None`. SDK1.6.0 modal/_grpc_client.py:125-126 rejects
this combination before `direct()` transport with the literal error
`Retry must be None when timeout is set`. The recorded exception type and call
arguments match this deterministic local guard. No rerun was used to confirm it.
This is an agent-written query-helper defect, not evidence of denied account
access, absent Sandbox, unavailable service or the earlier StreamReader failure.
The receipt intentionally retains only exception type/stage; the literal text
above is source evidence, not a retrospectively fabricated runtime message.

No Sandbox identity query, termination, billing, new resource, build, remote command,
file operation or science occurred after client initialization. SDK initialization
may perform its normal authentication/ClientHello; its internal wire call count
was not separately instrumented. WorkspaceNameLookup was invoked locally but
rejected before transport. Process exit0 means the helper wrote its failure
receipt; **it does not mean terminal PASS**.

Required remaining evidence is unchanged:

- workspace joon56 / main, App `ap-XiMVzlJgrNrCiFpIN1kB4W`;
- App name `a040-resume5-20261005-094405`;
- Sandbox name `a040-resume5-20261005-094405-gpu`, ID still unknown;
- exact Sandbox finished result, or official resource detail showing its ID/name/
  owning App and explicit terminal state with observation time. Running-list
  absence, NotFound, elapsed2400s, App STOPPED/task0 or an ACK is insufficient.

The user can inspect that exact Sandbox in the official Modal interface and
terminate only it if still running. This session did not inspect the interface.
Alternatively S0 may scope a corrected, independently checked metadata request
path with a fresh bounded authorization; this closeout does not activate it.
Do not require new login, credentials, account limits or model inputs to fix this
local call-contract defect. Local production repair remains conditional on actual
terminal evidence, not merely on repairing the helper.

Old App STOPPED/task0 observation remains historical. Sandbox terminal and final
billing remain UNCONFIRMED. Prior metered0.00178978USD is workspace aggregate,
not final task cost;2400s reservation2.965933453125USD remains planning. Historical
reserve-inclusive3.620974357992412USD/cash0/USD1/5 plans are not reset or recast
as actual bills. No new paid resource was requested; unresolved prior usage is
not assigned zero. See cost-time-ledger.json for non-overlapping time accounting.

Original source12/manifest and resume5 records remain unchanged. No payload112,
pins-original, response/key/checkpoint/cache/VAF read/hash, model import/fit/
predict/score, old suite, subagent, ZIP, commit/push, S2/S3/TEST operation.
All existing scientific STOP/HOLD/exposure/incumbent/parked states remain.

Artifacts: entry.json, remote-window.json, termination-billing-receipt.json,
source-manifest.json, local-regression.json, verification.json, exposure-ledger.md,
cost-time-ledger.json, s0-handoff.ko.md. Empty source.diff/placement.diff explicitly
mean **production repair NOT_STARTED**, not a validated zero-change repair.
