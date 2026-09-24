# A012 - Phase-2 reference and calibration decision gates
date-started: 2026-09-24
status: in-progress
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

Execution pending. E041 remains DEV incumbent, E025 phase2 fallback, E052
parked after Grand .64 without update. Final model choice remains open.
