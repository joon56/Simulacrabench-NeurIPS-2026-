# 2026-09-10-E026 — E022 evidence layer ∘ full E017 capacity grid

Experiment: E026 (parent E025). Code: E025 assembly with the trunk
selected per instrument from E017's full grid {64×2, 128×2+do,
256×2+do, 128×3+do}. Zip: `submissions/2026-09-10-E026.zip`,
check_submission_zip OK.

## Local scores (2026-09-09, seed 0, phase 1)

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact (runner) | 0.4435 | 0.5006 | 0.4548 | 0.5629 | 0.5061 |
| E025 (LB 0.63 / unhcr 0.89) | 0.4436 | 0.5006 | 0.4548 | 0.5629 | 0.5061 |

Identical to E025 on the sandbox (it picks 128×2 again — the sandbox
is blind to capacity). Official score.py PASS ×3: 0.5000 / 0.4500 / 0.5600 (parity exact). Runtime
~420 s local on CPU (4 trainings per instrument); the hosted H100
absorbs training (E025 at ~300 s local-CPU ran without timeout).
Accepted risk: if the GPU path ever fails, this would time out —
fallback = E025.

## Leaderboard expectation (real data)

Reference: E025 LB = 0.63 (0.52 / 0.49 / 0.89). Pre-registered
2026-09-09 BEFORE submission:

- **unhcr 0.90** (Grand → 0.64) ⇒ a wider/deeper trunk won on real
  unhcr; keep the grid, try width 512 / depth 3 at 256 next.
- **unhcr 0.89** ⇒ 128×2 is the real optimum; capacity axis complete —
  stop spending on architecture, move to phase-2 preparation and
  remaining structural ideas.
- **unhcr ≤ 0.88** ⇒ selection instability on real data; pin E025's
  two configs.
- unicef/wb: flat expected (unicef control stays small; wb at ceiling).

## Actual leaderboard result (2026-09-10)

**Grand 0.63, no leaderboard update** — E026 ≤ E025 (unhcr ≤ 0.89).
The pre-registered **0.89 arm**: the wider/deeper configs did not beat
128×2 on real data; **capacity axis complete** (E015 local null →
E017 +0.01 → E025 +0.01 stacked → E026 flat). Ran without timeout with
four trainings per instrument — the hosted GPU path is robust.
E026 parked; E025 remains the best submission (0.63 / 0.52 / 0.49 /
0.89).

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
| 920060 | 2026-09-10-E026.zip | 2026-09-09 19:48:08.532143 +09:00 | Finished | 0.6300000000 | 0.5200000000 | 0.4900000000 | 0.8800000000 | false |

UNHCR 0.8800000000 is one released increment below E025 0.8900000000,
although both Grand values display as 0.63. The old Grand-only flat reading
does not establish instrument equality or a precise causal regression.

[Complete score ledger](../SCORES.md) and [sanitized source](../hosted-scores/2026-09-27.json).
All score precision fields are 2. Failed attempts have no scores; never substitute zero.
