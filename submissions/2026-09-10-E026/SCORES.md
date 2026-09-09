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
