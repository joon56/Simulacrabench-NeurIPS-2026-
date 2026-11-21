# A040 S0 — local controller review, 2026-10-04 KST

**ACCEPT_LOCAL_CONTROLLER_CONTRACT / RECOMMEND_BOUNDED_S1_CONTINUATION.**
S0 reviewed documents and source only. No remote execution authorized by this
record's creation. Deliver the [proposed scope](s1-remote-resume.ko.md) to the
existing S1 as a user instruction to activate it.

## Receipt and evidence

Role S0; technical-result review and next-scope decision. Read AGENTS, CLAUDE,
status, newest three log entries, workflow then the named repair handoff/artifacts.
Workflow 2026-09-27-r4; SHA256
`a83c6f4102f50d0b8919f0f2010acfd19954901e8e2a08e7771ef87831741642`.
HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`; dirty work preserved.
Entry read commands and source/document hashes are in [verification](verification.json).
No Python/pythonw/uv processes appeared in the named local process check; this is
not an exhaustive host or Modal-account workload audit.

Reviewed [closeout](../modal-controller-repair1/closeout.md), verification,
diagnosis, entry, controller/launcher, diff, source hashes, cleanup state table,
suite2 regression result, SDK AST result, prior-artifact check and manifest.
Twelve selected artifacts match their artifact-manifest entries. The manifest's
own current hash is recorded separately, not self-authenticated. No fixture run.

## What passed and what did not

- Reported local regression: 15/15 corrected cases; all regression subprocess
  time 6.5996745s. Original cp949 failure and first fake-suite logging failure
  remain preserved. Installer-source equality is recorded.
- Actual controller with injected fake transport checks Unicode, bounded waits,
  exception preservation and honest termination states. Only explicit STOPPED
  plus task0 qualifies termination in that mock contract.
- SDK AST checks support the single-loop design. They do not verify actual SDK
  binding, remote cleanup, or the complete cause of the historical hang.
- `run_controller` still defaults to phase0.12s/cleanup0.35s;
  `launcher.launch` defaults to3s and invokes `fake_worker.py`. These are local
  test settings, not a ready production launcher. A new live worker and explicit
  stage deadlines are required. PID-only termination assumes no grandchildren
  in the fake; live SDK helper ownership must be handled separately.
- Image completion, Linux boundary, H100 runtime and complete candidate outputs
  remain unverified. Nothing here measures ERPIS benefit or release eligibility.

## Decision value and alternatives

The unresolved useful question is whether the unchanged full-context policy can
complete the named all3 contract on the selected H100 resource. RTX3070's900s
timeout leaves that question open. This newly verified controller removes one
concrete local prerequisite; a bounded continuation can now produce either a
complete technical result or a located platform/resource failure. No expected
Grand gain or H100 speedup is inferred.

Main recommendation: one S1 scope covering real binding preflight, one image
recipe attempt, and conditional original reference/candidate pair. Passing an
intermediate gate need not return to S0. This avoids another planning-only loop
while retaining the first actual error STOP and original scientific policy.
Backup: failure/blocked closeout with owned-resource termination and exact missing
input. No substitute model, optimizer changes, context reduction or new research
branch. Repeating the15-case suite or unresolved budget-proof investigation adds
no decision value. Direct S2 packaging remains premature.

## Prospective bounds and authority

The proposed S1 task gets a new explicit120min active-work window, including at
most60min preparation,40min single H100 resource lifetime and20min cleanup/export/
closeout. This is a proposal activated by the user delivering the prompt, not a
claim that old deadlines or unused time authorize a retry. Record new deadlines
at S1 entry. Carry prior preparation/controller active4477.3871369s separately;
scientific history remains4 processes/1077.3504532 parent seconds.

USD1 preparation/USD5 total remain monitored **planning targets**, cash authority
USD0. Existing user-reported credits30/spend0/usage30 are not a new live account
verification. Carry cumulative costs and unknown posted costs, do not reset the
ledger. Do not restore the superseded exact-invoice-proof gate or request an
account-limit increase. Prior summary0/component0.00001152USD is not final cost0.

No current source/launcher modification, installation, SDK import, account RPC,
test/model/build/ZIP execution or remote cleanup occurred in this S0 review.
Only this decision, proposed handoff, verification and status/log were written.

## Preserved decisions

E041 incumbent/E025 fallback; E057/E060/E061 parked. All STOP/HOLD including
E058 STOP, E059 STOP_SELECTION and separate A039 HOLD remain. Exposure17999
persons/12339SSUID, aggregate exposure/A022 original roles, E059 consumed
oracle1918/1124 and selection2007/1130, protected audit2074/1177 and calibration1866
remain. A_half not promoted; A018 unconfirmed; S3 stopped; no S2 candidate.
