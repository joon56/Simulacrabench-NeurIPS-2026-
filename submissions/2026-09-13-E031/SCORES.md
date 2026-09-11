# 2026-09-13-E031 — phase-2 ingredients read on real data (E025 + replay cap lift + E029 ensemble)

Experiment: E031 (pre-registered real-data A/B; parent E025). Code: the
E025 assembly with (1) `CAL_QUERIES` 6000 → all visible rows (the λ
replay per (item, concentration bucket) uses every visible row) and
(2) E029's 3-seed net ensemble with output temperature tuned jointly
with w on the outer holdout. Zip: `submissions/2026-09-13-E031.zip`,
check_submission_zip OK (smoke frame exercises the ensemble guards).

## Local scores (2026-09-13, seed 0, phase 1)

| | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|
| exact (runner) | 0.5009 | 0.4551 | 0.5634 | 0.5065 |
| E025 (LB 0.63 / unhcr 0.89) | 0.5006 | 0.4548 | 0.5629 | 0.5061 |

Δ +0.0004 = E029's ensemble; the cap lift is inert on the clean sandbox.
Household sim (unhcr log score): cap lift +0.0000 (phase 1, 9,271
visible) / +0.0005 (phase 2, 9,965 visible). Parity of the assembled
file vs the src composition exact (unicef 0.500934 both). Official
score.py PASS ×3: 0.5000 / 0.4500 / 0.5600 (63 / 176 / 361 s local CPU,
training on CPU — 600 s total, hosted GPU absorbs the 7 trainings). Runtime 711 s local CPU under 3-way contention
(E029 alone 528 s; 7 trainings per instrument — hosted H100 absorbs
training; CPU-side ≈ E025 + 38% more replay queries on unhcr).

## Leaderboard expectation (real data)

Reference: E025 LB = 0.63 (0.52 / 0.49 / 0.89). Both ingredients
measured ≈ 0 locally; this slot buys the real-data reading of two
things the sims cannot show — real between-seed net variance (real
GIVEN coupling is 3–5× the sandbox's) and real λ estimation noise on
6k vs 8.3k replay rows. Pre-registered 2026-09-13 BEFORE submission:

- **unhcr 0.90+** ⇒ real net variance / λ noise is larger than the
  sim's; both ingredients go into the phase-2 stack as measured gains,
  and seed count becomes a phase-2 knob (5–10 members, GPU free).
- **unhcr 0.89, Grand 0.63** ⇒ flat, as the sims say; ingredients stay
  in the phase-2 model as no-risk defaults (self-tuning), nothing more
  is expected from them.
- **≤ 0.88 or timeout** ⇒ the replay on all rows or the 7 trainings
  broke the 900 s budget on a slow worker day — restore CAL_QUERIES
  6000 / N_SEEDS 1 for phase 1 and keep both only under the 3600 s
  phase-2 budget.
- unicef / wb: flat (0.52 / 0.49) — ensemble Δ is +0.0003 there.

## Actual leaderboard result

(pending)
