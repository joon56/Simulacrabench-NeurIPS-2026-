# E008 — full-GIVEN logistic conditionals blended with the E006 ladder
parent: E006
status: adopted
date: 2026-08-30

## Hypothesis

Per-PREDICT-item multinomial logistic regression on the one-hot-encoded
FULL GIVEN block, mixed with the E006 ladder in probability space
(p = w·logit + (1−w)·ladder, one w per instrument tuned on the internal
holdout), beats E006, because the ladder conditions on at most 3 GIVEN
columns while the instruments carry 7 (unicef) / 30 (world_bank) /
72 (unhcr) GIVEN items — and the 2026-08-28/29 leaderboards showed real
GIVEN-answer coupling is stronger than the sandbox trait. Additive
main-effects structure generalizes where deeper count cells would empty
out (the reason E006 stopped at depth 3).

## Domain check

Pre-registered 2026-08-30 BEFORE implementation.

- (a) Technical: the kit tutorial's own naive-Bayes warning (2026-08-11
  log) says answers are conditionally dependent through a shared
  respondent trait; a discriminative logistic on the whole GIVEN block is
  the cheap proxy for that trait without double-counting evidence. MRP
  literature (domain guide §7.1): cell-based pooling dies by empty cells;
  regression main effects are the standard escape.
- (b) Real-data expectations (leaderboard tests these, not the sandbox):
  world_bank should move for the first time since E002 (flat 0.48→0.48
  across E005/E006) — its GIVEN block holds banded psychometric scores,
  and cross-task cognitive correlation (g-factor; Laajaj & Macours per
  A001) is exactly a many-weak-predictors situation the 3-column ladder
  cannot see. unhcr largest absolute gain again (72 GIVEN columns, only
  3 used so far; 155 PREDICT gate parents multiply any parent-belief
  improvement through the cascade; cheapest U = 1.2618). unicef smallest
  gain (7 GIVEN, ladder already uses 3; gating nearly deterministic
  already).
- (c) Sandbox validity: trait_scale = 2.0 induces genuine respondent-level
  dependence, so the mechanism (logit > 3-col ladder, blend weight lands
  strictly inside (0,1)) IS locally measurable; magnitudes still won't
  transfer.

## Change

`src/models/logit_blend.py` (planned): E006 machinery unchanged (ladder
selection, gate recursion, E003 agreement softening). New: per PREDICT
item, `LogisticRegression` (C=1.0, lbfgs) on one-hot GIVEN features fit
on complete visible rows — a full-distribution model (incl. NA_GATED)
and, for gated items, an asked-only conditional model. Blend with the
corresponding ladder distribution at the belief level before gate math;
w per instrument from grid {0, 0.1, …, 1.0} on the same 20% internal
holdout (fit on 80%, log score of blended full-table dists). Items whose
training target is single-class fall back to ladder only. Guard rails:
runtime profiled on the unhcr sandbox (budget 900 s total, hosted 8 CPU);
if sequential fits exceed ~400 s locally, parallelize with joblib.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | sample | unicef | world_bank | unhcr | mean | Δ vs E006 (3-inst) |
|---|---|---|---|---|---|---|
| E006 (parent) | 0.4385 | 0.4772 | 0.4196 | 0.5382 | 0.4684 | — |
| this | 0.4418 | 0.4994 | 0.4447 | 0.5532 | 0.4848 | **+0.0208** |

3-inst mean (sample excluded): 0.4783 → 0.4991. Largest local gain since
E004. Wall-clock: 1.1 / 6.8 / 36 / 138 s ≈ 182 s total (≪ 900 s budget;
tune adds 1–25 s per instrument on top of ladder selection).

Tuned blend weights (sandbox): sample w=0.6, unicef 0.9, world_bank 0.8,
unhcr 0.6 — **all strictly interior with smooth concave holdout curves**
(pre-registered watch point (c) hit: both components contribute; w=1.0 is
worse than w* everywhere, so the ladder still pays even with the full
logistic in the mix). Ladder selections unchanged from E006.

Convergence probe: lbfgs at max_iter=200 emits STOP warnings on a few
items, but max_iter=1000 reproduces every skill to 4 decimals at
identical wall-clock, and max_iter=5 only drops sample 0.4418 → 0.4415 —
the cap is immaterial; kept at 200.

Edge guard added before packaging: gated items with zero asked rows in
the visible data (possible under real approximate gates) fall back to
the ladder-only conditional instead of fitting on an empty design matrix
— unreachable on the sandbox (exact gates), cheap insurance on unhcr.

Tests 27/27 (4 new: vector validity, w=0 ≡ E006 bit-exact, tuned w range
+ no-worse-than-ladder on holdout, single-class fallback).

Reproduce: `PYTHONPATH=. .venv/Scripts/python src/eval/runner.py src/models/logit_blend.py`

## Decision

**Adopted.** Δ(3-inst mean, sample excluded) = 0.4991 − 0.4783 = +0.0208
≫ +0.005, within budget. Domain check verdict: consistent — (a) the
discriminative full-GIVEN model beats cell-based pooling exactly where
the MRP empty-cell thesis says count tables must stop, and (c) interior
blend weights confirm complementarity rather than replacement. The
real-data placement claims in (b) — world_bank finally moving, unhcr
largest absolute — are tested by the 2026-08-30 leaderboard submission;
sandbox cannot arbitrate them. Submission: `submissions/2026-08-30-E008/`.
