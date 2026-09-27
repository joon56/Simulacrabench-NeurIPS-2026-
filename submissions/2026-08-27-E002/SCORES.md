# 2026-08-27-E002 — gated marginal (first leaderboard submission)

Experiment: E002 (adopted). Code: exact copy of `src/models/gated_marginal.py`.
Zip: `submissions/2026-08-27-E002.zip` (main.py at root, no requirements.txt —
numpy/pandas pre-installed). `check_submission_zip.py`: OK.

## Local scores (2026-08-27, seed 0, phase 1)

Exact skill via `src/eval/runner.py`:

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact | 0.3210 | 0.3232 | 0.2909 | 0.4297 | 0.3479 |

Official `score.py` (noised, PASS all three): unicef 0.3200 (2.1 s) ·
world_bank 0.2900 (3.4 s) · unhcr 0.4300 (9.1 s). Total predict wall-clock
~15 s ≪ 900 s budget. Matches the 2026-08-19 measurement exactly — no drift.

## Purpose and expectation

Purpose: validate the hosted submission pipeline end-to-end and establish the
first REAL-data score baseline. Sandbox skills above do NOT predict the
leaderboard numbers (invented marginals); expectations are qualitative only:

- unicef: gate gain should transfer (5/7 gates on GIVEN parents,
  deterministic NA_GATED) — expect the largest skill of the three... unknown
  magnitude.
- world_bank: small gate gain (6/40 gates on GIVEN parents).
- unhcr: expect ≈ real-data marginal (all gates on PREDICT parents → E002
  algebraically equals marginal). Hard coupling is safe here for exactly that
  reason; it becomes unsafe only once parents are predicted respondent-
  specifically (E004) — soft gating (E003) must land first.

The reported LB triple becomes the reference point every later submission's
local-vs-LB gap is measured against.

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
| 904087 | 2026-08-27-E002.zip | 2026-08-27 18:08:47.038956 +09:00 | Finished | 0.4300000000 | 0.4500000000 | 0.4300000000 | 0.4100000000 | false |

[Complete score ledger](../SCORES.md) and [sanitized source](../hosted-scores/2026-09-27.json).
All score precision fields are 2. Failed attempts have no scores; never substitute zero.
