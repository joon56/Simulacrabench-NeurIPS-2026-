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

## API score reconciliation - 2026-09-27

Source: user-supplied My Submissions JSON, recorded 2026-09-27.
This supplement supersedes missing-score/ID/time statements above for the IDs
listed here; the earlier registration, interpretation and local checks remain
historical. Values below are released API scores, not unnoised raw scores.
Created time is platform submission metadata, not the snapshot directory date.
Current leaderboard membership is not a historical best-update event log.
The uploaded ZIP bytes/hash and hosted runtime are not verified by this response.

| Submission ID | Filename | Created (KST) | Status | Grand API | UNICEF API | World Bank API | UNHCR API | On leaderboard at snapshot |
|---|---|---|---|---:|---:|---:|---:|---|
| 922271 | 2026-09-14-E031b.zip | 2026-09-11 16:52:37.077152 +09:00 | Finished | 0.6333333333 | 0.5200000000 | 0.4900000000 | 0.8900000000 | false |

[Complete score ledger](../SCORES.md) and [sanitized source](../hosted-scores/2026-09-27.json).
All score precision fields are 2. Failed attempts have no scores; never substitute zero.
