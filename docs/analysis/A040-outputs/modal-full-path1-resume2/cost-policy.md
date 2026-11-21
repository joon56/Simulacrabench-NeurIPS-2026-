# Prospective monitored cost plan — 2026-10-03 KST

User amendment replaces the strict USD1/5 invoice-proof prerequisite only.
Cash authorization0; user-reported credits30/spend0/usage30 inherited unchanged.
Normal current baseline metered0/billed0; no budget RPC or login repeated.

One recipe: python:3.13.14-slim registry base, one CPU-only run_function installer,
all original34 pins (torch cu126 index additionally), no scientific import. CPU
request/limit1, memory request/limit8192MiB; installer timeout600s and absolute
preparation deadline. include_source=False, no secrets/volumes/region preference.
No client rebuild/force_build/repeated install. Provider retries observed in logs.

Published rates rechecked https://modal.com/pricing on2026-10-03KST:
Function core0.0000131/GiB0.00000222 per second; Sandbox core0.00003942/
GiB0.00000667; H1000.001097. No premium region or nonpreemptible option.

| Component | Planning estimate USD |
|---|---:|
| CPU preparation allocation, including startup time allowance |0.20|
| Unmeasured pull/layer/snapshot/transfer/retry overhead allowance |0.65|
| H1001 + original CPU1/RAM15258MiB, full2400s resource time |2.965933453125|
| Recovery/termination/other reserve |1.00|
| Planned total |4.815933453125|

Overhead0.65 is a planning allowance, not measured charge or guaranteed ceiling.
Target preparation1/total5 retained; initiation gate management value+next stage
estimate must remain below4. During preparation use the larger of measured account
baseline delta and estimated preparation resource time plus overhead allowance.
Account delta is conservative unattributed usage, not a claim of task attribution.
Poll billing at most60s apart when accessible; persist estimates despite delayed
posting. USD4 triggers cleanup, no new stage. Any later posted>5 reported openly.
Stop own exact IDs at first error/deadline; client timeout alone is not termination.

Prep deadline2026-10-02T16:04:10Z; whole deadline17:04:10Z. Old2295.2633125s
carried. Historical build-cost HOLD remains valid under its old contract.
