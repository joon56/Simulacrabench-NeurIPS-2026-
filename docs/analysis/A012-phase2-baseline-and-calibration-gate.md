# A012 - Phase-2 reference and calibration decision gates
date-started: 2026-09-24
status: complete
relates-to: E025 / E041 / E052 / A011 / E053

## Authorization and fixed scope

User approved three deliverables: E041 phase-2 comparison table, the next
calibration preregistration, and its oracle pass/stop decision. No hosted
submission, final-model promotion, new production estimator or model tuning
is included. Preserve all existing src and submission main/ZIP bytes.

## Phase-2 protocol registered before execution

Use the current official clean sandbox and phase=2 explicitly: TRAIN+DEV
visible, whole TEST PREDICT blocks hidden. Compare unchanged frozen E025 and
E041 snapshots on UNICEF, World Bank and UNHCR. Scores are engineering/local
direction only, never predictions of confidential TEST performance.

Run the E041 source implementation and original assembled snapshot with the
official grader for all3 schemas; compare every raw probability vector.
Run unchanged E025 snapshot once under the same frames for an exact local
reference; reuse its previous official qualification, not its old timing.
Check original E041 ZIP with the official checker; do not create a new ZIP.
Record schema/frame/source/snapshot/archive hashes, package versions, scored
cell counts, paired score deltas, raw-vector parity and per-instrument timing.
Profile official E041 runs sequentially with2threads and no competing fits.
Combined official import+prediction time must be below3600s locally; no claim
about hosted CPU/GPU speed. Leave room for overhead and method completion.

Reading arms: parity/schema/runtime failure blocks technical qualification.
Absolute local E041-minus-E025 delta <=.002 per instrument qualifies the local
no-regression check, but not final adoption. Larger adverse delta triggers
investigation and preservation of E025 fallback; larger positive delta remains
local evidence. Any unanticipated exception is logged, not silently rerun with
changed scoring/model settings. Never equate successful packaging with gain.

## Calibration design and oracle

Root will finish a distinct E053 family specification after reviewing E050's
failed scope and A011's measured mismatch, and commit it before any new
candidate fitting/scoring. No unseen rows are claimed merely by changing a
seed on previously used public source data. Oracle outcomes authorize only
further research when their scope and threshold permit it, not deployment.

## Results and decision

All three deliverables completed on2026-09-24. Protocol146eb7f preceded fits;
E053 registrationa452465 and diagnostic implementation570738f preceded its runs.

### 1. E041 phase2 reference

| Instrument | Fresh E025 | E041 source and official | Delta |
|---|---:|---:|---:|
|UNICEF|.490197770701|.490197770701|0|
|World Bank|.462029504790|.462029504790|0|
|UNHCR|.565173813942|.564665364947|-.000508448996|

Official phase2 PASSx3; every E041 source/assembled raw vector exactly equal.
Original ZIP checker PASS. Fresh E025 controls also raw-exact E041. Registered
absolute per-instrument delta<=.002 passed. Inclusive local official time
367.176995s<3600; sequential2thread runs with no competing model fits. This is
an engineering qualification, not evidence of confidential TEST gain or a
measured hosted16GB peak/speed guarantee. No final-model promotion.

Scores, raw vectors and provenance: submissions/phase2-E041-preparation/SCORES.md,
verification.json, supplemental-verification.json; docs/analysis/A012-outputs/.
Two disclosed execution deviations: baseline source workers scored before
saving vectors; full supplementary provenance was collected after fitting.
The original executed verifier is archived. Its one-sided delta flag was
corrected in a separate derived report using the registered absolute threshold,
without refitting or overwriting the original results. The reusable script
now checks that threshold and refuses an existing run before expensive work.
Fresh E025 differs slightly from its historical rehearsal on UNICEF/WB; cause
unassigned, current comparison uses fresh paired outputs. Five focused tests PASS.

### 2. Calibration preregistration

E053 specified unchanged donor evidence with independent absolute item/bucket
weights in[0,.98], including dormant query evidence from the same fitted state.
Actual generic E041 fit once per seed on observed Adult54/55,2600fit/800oracle/
800selection/800audit; every outer query PREDICT block hidden before all fits.
No assumed household/gate structure added. Registration, arrays and captures
were persisted before oracle scoring. Prior-role population overlaps disclosed;
selection/audit not scored. The concave oracle is valid only without recursive
gates, explicitly not an upper bound on coupled UNHCR parent/descendant changes.

### 3. Oracle pass/stop

E053 upper mean-equivalent skill gains: seed54+.000523121587,
seed55+.000172892178, both below the fixed+.005 gate. STOP; no calibrator,
production module or new ZIP. Existing E041 section retrieval was active in
both runs, but both already returned evidence and all queries were in the low
concentration bucket. Dormant recovery and second-bucket freedom therefore
were not naturally exercised. Returned/uncensored bounds are identical.
Do not interpret these proxy results as a universal survey calibration ceiling.
Thirteen focused tests and80 independent scalar probes PASS; frozen-artifact
recomputation checks exact captures, donor membership and oracle arithmetic.

E041 remains DEV incumbent and is now locally qualified on phase2. E025 stays
fallback; E052 remains parked. Final method coverage of E041 is still pending.
Next scientific work must address the limits exposed here: specify a genuinely
distinct recursive family and a valid coupled oracle/validation channel before
building a repair. Do not rescue E053 with more seeds, threshold reductions or
a renamed weight grid. E041's real-data loss map is still unmeasured; an E041
component probe may separately guide DEV work, with its one-instrument scope
and expected readings preregistered before any packaging. No such probe was
built or uploaded in this task.
