# 2026-09-20-E040 — tree blend on unhcr content items over E025

Experiment: E040 (real-data A/B; parent E039/E025). Code: the E025
assembly + one HistGradientBoosting classifier per ungated PREDICT item
on the largest instrument (≥ 150 PREDICT items ⇒ unhcr only), fitted on
the fit split, mixed into the full-head distribution at a weight v
chosen on the outer holdout (v = 0 ⇒ E025). unicef / wb = E025.
Zip: `submissions/2026-09-20-E040.zip`, check_submission_zip OK.

## Local scores (2026-09-20, seed 0, phase 1)

| | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|
| exact (runner) | 0.5006 (= E025) | 0.4548 (= E025) | 0.5629 | 0.5061 |
| E025 (LB 0.63 / unhcr 0.89) | 0.5006 | 0.4548 | 0.5629 | 0.5061 |

Sandbox holdout picks v = 0 (log score by v: 0 → −0.72983, 0.1 →
−0.73015 … 0.5 → −0.73680, monotone worse) — exactly what A005 predicts
(the net is at the sandbox's GIVEN-only ceiling). Runtime +≈ 50 s local
CPU-side on unhcr (57 fits + probabilities). Parity assembled vs src exact
(unhcr 0.562949 both). Official score.py PASS ×3: 0.5000 / 0.4500 /
0.5600 (= E025 within grader noise).

## Leaderboard expectation (real data)

Reference: E025 LB = 0.63 (0.52 / 0.49 / 0.89). Pre-registered
2026-09-20 BEFORE submission. On real data the ladder still earns
w ≈ 0.6–0.9 against the net (1.0 on the sandbox), i.e. real GIVEN
interactions are not fully captured; trees are the cheapest strong
nonparametric conditional. Content items hold 0.031 of unhcr's
remaining loss.

- **Grand 0.64 (unhcr ≥ 0.90)** ⇒ the real-data base model is under-fit;
  the phase-2 file (3,600 s) carries the full E039 tree blend (all 213
  items) — validated by this reading; consider trees on unicef/wb too.
- **Grand 0.63, no update** ⇒ base model at its real ceiling as well;
  E025 stays for phase 2. Together with E027–E038 this closes every
  axis we can name: base, evidence recall, λ calibration, gates.
- **Grand ≤ 0.62** ⇒ holdout-tuned v > 0 but over-confident trees on
  held-out cells — revert; tighten MAX_ITER / add early stopping.
- Timeout ⇒ the +50 s CPU-side crossed the budget on a slow worker;
  revert (no diagnostic value).

## Actual leaderboard result (2026-09-20)

**Grand 0.63, no update (≤ E025; unhcr ≤ 0.89).** Pre-registered
"base model at its real ceiling" arm: gradient-boosted trees on the
GIVEN block add nothing to the net+ladder base on real unhcr content
items either. Sixth flat real-data A/B. E040 parked; E025 stays the
model of record and the phase-2 file; the full E039 blend is NOT
carried into phase 2 (no reading justifies its runtime).
