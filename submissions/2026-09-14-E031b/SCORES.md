# 2026-09-14-E031b — E025 + calibration replay cap lift only (no ensemble)

Contingency after E031 failed without an HSCC code. Code: the E025
assembly with `CAL_QUERIES` 6000 → all visible rows (one-line diff).
Zip: `submissions/2026-09-14-E031b.zip`, check_submission_zip OK.
Submitted the same day as the failed E031 — a failed submission does
not consume the daily slot.

## Local scores (seed 0, phase 1)

Identical to E025 on the clean sandbox (0.5006 / 0.4548 / 0.5629; the
cap is inert there). Household sims: +0.0000 (phase 1) / +0.0005
(phase 2). Runtime and memory = E025's (unhcr peak working set 1.82 GB).

## Leaderboard expectation (real data)

Pre-registered (E031 SCORES.md, cap-lift half): unhcr 0.90+ ⇒ λ
estimation noise on 6k rows was real; 0.89 ⇒ flat, 6k rows suffice.

## Actual leaderboard result (2026-09-13)

**Grand 0.63, no update (≤ E025; unhcr ≤ 0.89).** Flat arm: the replay
cap lift adds nothing on real data — 6,000 replay rows already
estimate λ per (item, bucket) to within the metric's resolution. Kept
at 6000 for phase 1 (runtime guard); lifting it in phase 2 is harmless
but pointless. The E029 ensemble remains UNREAD on real data (E031
failed before scoring).
