# 2026-09-17-E036 — λ per twin relation (same-round vs cross-round) over E025

Experiment: E036 (adopted, E003 route; parent E025). Code: the E025
assembly with the evidence weight λ calibrated per (item, concentration
bucket, same-round vs cross-round top candidate); < 30-row buckets fall
back to the pooled λ; unicef / wb (no round column) = E025 exactly.
Zip: `submissions/2026-09-17-E036.zip`, check_submission_zip OK.

## Local scores (2026-09-17, seed 0, phase 1)

| | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|
| exact (runner) | 0.5006 | 0.4548 | 0.5629 | 0.5061 |
| E025 (LB 0.63 / unhcr 0.89) | 0.5006 | 0.4548 | 0.5629 | 0.5061 |

Identical on the clean sandbox (no twins). Household sims (unhcr log
score): same-round twins only **+0.0010** (cross buckets engage on
random k-NN candidates, harmless); **panel sim** (half the twins in the
other round with copy rates 0.7–0.95 vs 0.2–0.5 same-round) **+0.0105**
over E025. Parity of the assembled file vs src exact (unhcr 0.562877 both).
Official score.py PASS ×3: 0.5000 / 0.4500 / 0.5700 (grader noise around
E025's 0.50 / 0.45 / 0.56). Runtime = E025's (38 / 88 / 198 s local, CPU
training).

## Leaderboard expectation (real data)

Reference: E025 LB = 0.63 (0.52 / 0.49 / 0.89). Pre-registered
2026-09-17 BEFORE submission. Real unhcr evidence is worth +0.10
(E034); if a meaningful share of it comes from cross-round recurrences
whose per-item agreement differs from same-round co-respondents, the
relation split recalibrates λ where it is currently averaged.

- **Grand 0.64 (unhcr ≥ 0.90, best updates, per-instrument visible)** ⇒
  relation-specific agreement is real and ≥ +0.01; next: relation ×
  wave direction (round-1 twin for a round-2 query vs the reverse), and
  the E029 ensemble as a ride-along.
- **Grand 0.63, no update** ⇒ pooled λ already adequate on real data
  (relations agree similarly, or one relation dominates the matches);
  park; the remaining +0.03 is not in λ calibration.
- **Grand ≤ 0.62** ⇒ refined buckets too thin somewhere (raise
  MIN_BUCKET) — revert to E025.
- unicef / wb: identical to E025 by construction.

## Actual leaderboard result

(pending)
