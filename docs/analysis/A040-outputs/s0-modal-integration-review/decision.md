# A040 S0 — local integration review, 2026-10-04 KST

**RECORDED_LOCAL_PASS / REMOTE_HOLD_OUTPUT_CONTRACT.**
The39 recorded regression cases passed within their fixture scope. Source review
finds a deterministic producer/exporter mismatch that those fixtures missed.
Do not execute the current frozen path remotely. Recommend one focused local
[S1 correction](s1-output-contract-repair.ko.md), not another full integration task.

## Receipt and preservation

Role S0; document/source review and handoff only. AGENTS, CLAUDE entry section,
status, latest3log, workflow routing were reread in order; unchanged remaining
instructions were read in the preceding review. Workflow2026-09-27-r4 SHA256
`a83c6f4102f50d0b8919f0f2010acfd19954901e8e2a08e7771ef87831741642`.
HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`; dirty work preserved. Named local
python/pythonw/uv check returned no processes; not a whole-host/account audit.
Twelve source-manifest entries and24 selected artifact-manifest entries match.
Read/hash evidence and preservation checks: [verification](verification.json).

The source closure, corrected nested enum and implemented Sandbox/Linux/export
modules are real progress. S1's39/39 pass,2cycles/8.5363744s, failed test-endpoint
cycle preservation and zero actual RPC/science remain historical results. The
old resume3 failure is not a new execution or H100 result. Do not rewrite either
prior verdict. This new review limits advancement based on a newly identified gap.

## Blocking finding: canonical output names do not agree

- Existing [fixture manifest](../full-path-resume1/fixture-manifest.json) uses
  `unicef`, `world_bank`, `unhcr`, counts17856/39520/132273.
- [linux_runner.py](../modal-local-integration1/linux_runner.py):164-186 takes
  `row['instrument']` for filename, output_hashes and output_counts. Candidate
  also explicitly reads `world_bank` at103-105. The earlier reference/result.json
  confirms these same metadata keys and counts; no prediction arrays were opened.
- [sandbox_stage.py](../modal-local-integration1/sandbox_stage.py):103 instead
  requires `{'unicef','wb','unhcr'}`. After a complete real reference, its exact-set
  check would raise `Output export manifest mismatch`, before candidate dispatch.
  This is a source-derived conclusion, not a newly executed failure.
- [tests_integration.py](../modal-local-integration1/tests_integration.py):158-163
  creates `wb` and counts1/1/189647. The fake agrees with the exporter rather than
  the producer. Thus its normal-path PASS does not test their compatibility.

Related limited validation gap: the current outer gate checks only the sum of
output_counts. An incorrect per-instrument distribution can have the correct
total189649, as the fixture itself demonstrates. The scientific runner separately
checks each actual output; preserve that check. The integration contract should
also verify canonical names and per-instrument metadata, without pretending the
small protocol fixture contains189649 predictions.

## Next action and value

Main: canonical producer/consumer metadata and filename repair, with fixtures
derived from the frozen fixture manifest/runner and existing result metadata.
Keep model and scientific runner unchanged. Reproduce the current mismatch with
model-free inputs, repair only the new consumer/test boundary, then cover normal
reference/candidate and wrong-key/equal-total-wrong-count rejection. This avoids
spending remote preparation/reference time on an already predictable export error.

Proposed45min local task; focused regression120s cumulative/max3cycles. No remote
request or model work. Backup is exact failure/incomplete closeout. A new defect
outside this boundary returns to S0; no broad rewrite or automated repair chain.
Repeated generic mocks or immediate cloud retry add no information here. No user
account input, new credits, provider inquiry or policy change is needed.

If corrected, S0 can reconsider the original bounded remote measurement. Actual
Linux cgroup/native egress/OS kill, image/dependencies/current payload identity,
H100900s, cleanup/billing and release remain unverified. This correction grants
none of those PASSes and makes no score-improvement claim.

## Boundaries

Carry preparation/controller active7553.1022106s separately from scientific
4process/1077.3504532s. USD1/5 monitored plans/cash0 unchanged. Billing summary0,
component0.00001152USD and unposted/attribution uncertainty are inherited, not
queried anew. No new chargeable operation in this review or proposed local scope.

E041 incumbent/E025 fallback; E057/E060/E061 parked; all STOP/HOLD including E058,
E059 STOP_SELECTION/A039. Exposure17999/12339SSUID, aggregates/A022 roles, E059
consumed oracle1918/1124 and selection2007/1130; protect audit2074/1177/calibration1866.
A_half not promoted; A018 unconfirmed; S3 stopped; S2 none. Only new S0 records
and status/log written. No source edit/import/test/model/payload/RPC/build/ZIP/
commit/push/tree/subagent operation. Prompt preparation is not S1 execution.
