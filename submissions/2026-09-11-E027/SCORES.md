# 2026-09-11-E027 — concentrated-row evidence as net input, over E025

Experiment: E027 (adopted as A/B; parent E025). Code: E025 assembly +
`concentrated_evidence_block` fed as extra net input (rows with max
posterior ≥ 0.5 only; zeros elsewhere). Zip:
`submissions/2026-09-11-E027.zip`, check_submission_zip OK.

## Local scores (2026-09-10, seed 0, phase 1)

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact (runner) | 0.4436 | 0.5008 | 0.4534 | 0.5623 | 0.5055 |
| E025 (LB 0.63 / unhcr 0.89) | 0.4436 | 0.5006 | 0.4548 | 0.5629 | 0.5061 |

Household sim: +0.0011 log vs E025 (no-harm). Official score.py PASS
×3: 0.5000 / 0.4500 / 0.5600 (parity exact). Runtime ~330 s local CPU; hosted GPU absorbs training.

## Leaderboard expectation (real data)

Reference: E025 LB = 0.63 (0.52 / 0.49 / 0.89). Pre-registered
2026-09-10 BEFORE submission:

- **unhcr 0.90** (Grand → 0.64) ⇒ cross-item household structure is
  real and learnable — extend (lower CONC_SPLIT, add co-respondent
  GIVEN columns as inputs).
- **unhcr 0.89** ⇒ nothing beyond per-item copying is exploitable; close
  the evidence-input idea for good.
- **unhcr ≤ 0.88** ⇒ the block hurt on real data; pin E025.
- unicef/wb: flat expected (block ~zero there).

## Actual leaderboard result (2026-09-11)

**Grand 0.63, no update (≤ E025; unhcr ≤ 0.89).** Pre-registered 0.89
arm: nothing beyond per-item copying is exploitable from concentrated
matches — the evidence-input idea (E020/E024/E027) is closed. Parked.
