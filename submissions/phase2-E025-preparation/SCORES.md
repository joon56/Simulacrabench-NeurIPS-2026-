# E025 phase-2 preparation - pre-registered reading plan

Status: local preparation only; Test submission not made.
Model: unchanged `submissions/2026-09-09-E025/main.py`.
Method attachment: `output/pdf/method-4p.pdf` (four rendered pages).
Procedure and rules: `docs/phase2-preparation.md`.

## Fixed settings

E006 backoff + E010 agreement + E012 shared trunk, architecture selected
from {64x2, 128x2 with dropout 0.1}, plus E022 full-pool evidence.
Top ten candidates; 6,000 calibration queries; two concentration buckets;
lambda grid {0, 0.1, ..., 0.9, 0.95, 0.98}. TRAIN+DEV visible; TEST scored.
No E027/E028/E031b/E036/E038/E040 additions, external weights, or external
training data. The original E025 assembly is the release source.

## Test result interpretation, registered before upload

The historical DEV reference is Grand 0.63, UNICEF 0.52, World Bank 0.49,
UNHCR 0.89. TEST roles differ from DEV, and DEV readings are noised and
rounded. No numeric TEST band is justified by the synthetic scores.

| Arm | Interpretation | Next action |
|---|---|---|
| Valid TEST score, any value | Exact held-out performance of the fixed E025 method; a TEST-minus-DEV difference is not a controlled model A/B. | Record all returned instrument scores, Grand, submission identifier and runtime if available; report uncertainty and role differences. No score-driven resubmission. |
| Valid TEST score lower than the DEV reference | Possible role/generalization variation or different utility of evidence; aggregate scores do not identify the cause. | Describe the discrepancy and limitations; do not infer hidden labels or claim that one mechanism failed. |
| Participant-side contract or runtime failure | Final artifact did not satisfy the execution contract; the single-Test quota may be consumed. | Preserve the sanitized failure and local reproduction; do not assume permission for a second submission. |
| Organizer infrastructure failure documented by the platform | Clause 12's infrastructure exception may apply. | Use the organizer-authorized retry process, with the same fixed artifact unless organizers instruct otherwise. |
| Schema, harness, or rules change before upload | This preparation no longer certifies the final environment. | Inspect the change, repeat local no-regression/parity/official checks, and update this record before spending the one Test submission. |

The UNHCR-only relation delta_UNHCR = 3 * delta_Grand is for same-phase
controlled A/Bs only; do not apply it to TEST-versus-DEV.

## Validation record

Historical hardening: official phase-2 scores 0.4902 / 0.4620 / 0.5652;
291-second local CPU runner total. These historical values are retained in
the method. Fresh continuation checks and artifact hashes are recorded in
`verification.json` after completion. All inputs are synthetic sandboxes.

No model code changed, so file identity is the baseline no-regression
guarantee; fresh phase-2 scores are also compared with the historical values.
Source/assembly scores must agree within 0.002, with actual differences
reported rather than described as bit-identical if they are nonzero.

## Actual TEST outcome

Not submitted. No TEST leaderboard result or final submission identifier exists.
Copy this reading plan into the dated final snapshot and fill this section
only after the official Test result arrives.
