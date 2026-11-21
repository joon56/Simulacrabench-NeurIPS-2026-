# A040 S0 — resume3 protocol failure review

2026-10-04 KST. **ACCEPT_SCOPED_FAILURE / LOCAL_INTEGRATION_FIRST.**
Recommend one bounded, RPC-blocked S1 implementation/validation task. No remote
retry in this scope. [Next S1 prompt](s1-local-integration.ko.md).

## Receipt

S0 technical-result review. Read AGENTS, CLAUDE, status, latest three log entries,
workflow2026-09-27-r4, then named resume3 artifacts. Workflow SHA256
`a83c6f4102f50d0b8919f0f2010acfd19954901e8e2a08e7771ef87831741642`.
HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`; existing dirty work retained.
Read/hash evidence in [verification](verification.json). CIM process enumeration
was denied; fallback Get-Process found no named python/pythonw/uv processes.
This does not certify every host job or remote workload absent.

## Findings

1. [Result](../modal-full-path1-resume3/result.json) records AttributeError at
   live_worker.py:95. Source reads the nonexistent module-level
   `SDK.pb.GENERIC_STATUS_SUCCESS`; installed SDK _image.py:806 and protobuf
   type declaration use `api_pb2.GenericResult.GENERIC_STATUS_SUCCESS`.
   This is a located client implementation defect. S0 did not reproduce it.
2. The preflight imports real SDK classes, checks signatures and image-handle
   translation. It never exercises `base_identity` with a real protobuf response.
   Its scoped PASS is consistent with missing this error; no broad protocol PASS.
3. `source.diff` removes the old injected run_controller path; live_worker now
   contains new preparation, base checking, billing and cleanup orchestration.
   The prior15-case PASS cannot automatically qualify that new implementation.
4. live_worker waits for `continue-sandbox.json` after image construction and then
   imports `sandbox_stage`. No sandbox_stage source appears in the named attempt
   docs/tmp inventory, consistent with closeout. Linux orchestration is unfinished.
   Fixing the enum alone would not make the complete path ready.
5. Fourteen selected artifacts match the artifact manifest; all seven live-freeze
   entries match. Freeze purpose explicitly excludes scientific freeze. No payload
   or checkpoint hash checked here. Historical failure code/latches remain intact.

Reported live invocation1,3.7834749s, exit1. Authentication/workspace/single-loop
were reached; App/build/transfer/Sandbox/H100/reference/candidate0. NO_CREATE_ATTEMPT
is appropriate; no owned-resource termination claim is needed. Base verification
did not finish. Account metadata RPC occurred; remote resource creation did not.
S0 independently read records/source only, not account or server state.

## Decision and responsibility

Repeated local plumbing failures are not adverse model evidence. They do consume
research time without answering H100 feasibility. The next task should reduce
this specific integration risk before another remote request.

The previous S0 handoff permitted image work before all downstream source was
complete. It required a later science freeze but did not force complete local
orchestration before the first live request. That staging was weak. Prospectively
require the complete called module set, response handling, local integration
evidence and frozen source before remote preparation. Preserve the old handoff as
history; do not reuse it as a fresh attempt grant.

Main: finish only the named controller/Sandbox-stage/Linux orchestration, exercise
that same production orchestration with actual SDK/protobuf types and fake RPC,
fake process and payload endpoints. No parallel replacement controller whose
PASS says nothing about live code. Existing scientific code/policy stays fixed.
Backup: bounded incomplete/failure closeout and exact unresolved interface.

Rejected next actions: one-line fix followed immediately by a remote request;
another class-signature-only PASS; re-running all old fixtures; changing resource
budgets, account settings or models to address this local error. No external user
input, new provider inquiry or authentication is presently needed for local work.

Proposed cap90min active work; focused model-free regressions180s cumulative,
at most3 complete regression cycles with all failures preserved. No new cloud
credits consumed by authorized operations. If integration is incomplete at cap,
return specific gaps and revisit the route's priority; no automatic next tiny
repair or remote attempt. This is a prospective S1 scope, activated by the user
delivering its prompt. This S0 has not implemented or executed it.

Passing resolves local orchestration readiness only. Actual Linux enforcement,
image/driver behavior, H100900s, target outputs and hosted effectiveness still need
separate measurement. Future remote execution must use the newly reviewed source,
fresh deadlines and applicable authority; original pair allowance is not a latch
that launches itself. No forecast of Grand or TEST winning probability follows.

## Ledger and preservation

Carry resume3 cumulative preparation/controller active5504.7268216s; scientific
history4process/1077.3504532s unchanged. These are distinct ledgers, not summed
blindly. Last recorded billing0/component0.00001152USD is not final attributed
cost. Management0.65001152 includes an allowance, not a charge. USD1/5 monitored
planning/cash0 unchanged, no budget proof or account-limit increase introduced.

E041 incumbent/E025 fallback; E057/E060/E061 parked; E058 STOP/E059 STOP_SELECTION,
A039 and all other HOLDs preserved. Exposure17999/12339SSUID and aggregate history,
A022 roles, consumed oracle1918/1124 and selection2007/1130, protected audit2074/1177
and calibration1866 preserved. A_half not promoted; A018 unconfirmed; S3 stopped;
no S2 candidate. New review documents/status/log only; no code, tree, install,
SDK import/RPC, fit/predict/score, tests, ZIP, upload, commit/push or subagents.
