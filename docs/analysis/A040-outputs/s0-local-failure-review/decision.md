# A040 S0 — bounded instrumentation repair recommended

2026-10-02 KST. **RECOMMEND_SEPARATE_S1_REPAIR_ONCE**.
Original LOCAL_CONTRACT_FAIL remains the first-attempt verdict. No S0 repair,
scientific execution or S2 candidate.

## Diagnosis and decision

Reviewed original [closeout](../local-technical/closeout.md),
[result/traceback](../local-technical/result.json),
[resources](../local-technical/resources.json),
[verification](../local-technical/verification.json) and
[frozen manifest](../local-technical/frozen-inputs/run-manifest.json).
runner.py:22 takes `event(name, **values)`; tests_local.py:124 supplies both the
positional event identifier and `name=name`. The TypeError occurs during argument
binding, before the logger body. Earlier calls without that keyword are consistent
with the successful recorded events. This is source diagnosis, not a new reproduction.

Smallest recommended fix: rename that call's head metadata keyword to `head_name`
in a retry copy, preserving the event identifier and numerical assertions. Check
consumers and other event calls; do not redesign the logger/model or suppress errors.
First use a model-free regression against the actual logger function: reproduce the
original binding error, then verify corrected event/head/classes JSON output.

One retry has decision value: the explicit measurement-code defect prevented the
registered test from answering its question. Partial K15 exact parity, A/B/A state
and masking/arithmetic checks support keeping the same procedure. They do not prove
the unfinished full local contract. Repair/completion is preferable now to another
model search, paid H100 or release assembly; no numerical efficacy forecast follows.

## Scope and outcomes

[Separate S1 handoff](s1-repair-handoff.ko.md). Existing install/acquisition approval
and organizer-policy resolution stand. No repeated permission or policy inquiry.
The prepared handoff defines a new run only when the user instructs a separate S1;
it does not execute in S0 or reset the failed invocation's latch.

Main: model-free logging regression, then at most one unchanged complete local
suite in a fresh attempt directory. Preserve original code/manifest/latch/events/
resources/verdict. Only logging metadata and mechanical new-attempt paths/deadline/
manifest/latch wiring may change. Prototype/settings/assertions stay fixed.

The unfinished tests depend on fresh shared weights, counters, roles and before/after
state hashes. Replaying the original suite once is necessary fresh-state regression,
not independent scientific replication. Do not splice old partial arrays or run
successful components again as separate experiments.

Task wall60min; model-free regression60s total; one scientific child120s maximum,
RTX3070/CPU2/one heavy job, host cap16,000,000,000 bytes and original1s watchdog.
First failure/limit stops the run; no second invocation or threshold/seed/head/context
rescue. Original11.89s child/13.26s parent and memory peaks describe an interrupted
tiny suite, not a completion or full-path cost forecast.

Require all213 heads/four K>10 heads/1917 canonical vectors, fixed fake-model S/E
decision, final parameter/buffer equality and216-fit/217-predict/2-load assertions.
Only complete named checks earn LOCAL_CONTRACT_PASS. Logging success alone is not
PASS. Local resource failure is not H100/model infeasibility. Backup is failure or
incomplete closeout, returned to S0 without further repair.

Actual E041/control parity, full-shape context/selection/E/refit/all3 costs,
OS/native network isolation, release assembly/checker/official scorer and hosted
benefit remain unverified. This recommendation permits none of those tasks.

## Receipt and preservation

C:\Users\USER\Desktop\SimulacraBench; S0 result review/handoff;
workflow2026-09-27-r4. Ordered AGENTS/CLAUDE/status/newest3logs/workflow reads,
then artifacts/source. Evidence ed7fec, f0eb4e,297eb8,8b6528; digest in verification.
Systematic-debugging and karpathy-guidelines applied to source diagnosis/minimal scope.
HEADa43f4379ec78dbc2de260463eef67bb1d567d7e1; visible Python/uv jobs none, not an
exhaustive host audit. Existing dirty work preserved.

49 allowed document/source comparisons plus7 selected frozen code/registration/schema
comparisons match. Other154 downloaded-source/checkpoint manifest entries were not
rehashed; S1's original161 checks are historical, not reverified by S0. No fixture,
response, key, Parquet/NPZ/cache/model read or hash. Only new S0 review records and
scoped status/log additions; no source edits, tests, model calls, agents/contact,
ZIP/upload/commit/push.

Inherited17999 people/12339SSUID, A022 original roles/aggregate history and E059
consumed oracle/selection/protected audit/calibration remain per the original
[ledger](../local-technical/exposure-ledger.md). E041 incumbent/E025 fallback,
E057/E060/E061 parked; E058 STOP/E059 STOP_SELECTION/A039 and all other HOLDs
preserved; no A_half promotion. A018 unconfirmed/S3 stopped.
