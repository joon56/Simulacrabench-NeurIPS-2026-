# E010 — conditional gate-agreement softening (data-selected, per item)
parent: E008
status: adopted
date: 2026-09-01

## Hypothesis

Replacing E003/E008's scalar per-item gate-agreement weight ã_i with a
conditionally estimated ã_i(v) — agreement computed per value v of ONE
data-selected GIVEN column, beta-binomial-shrunk toward the item's
scalar ã_i — improves real unhcr skill, because the schema itself states
gate-vs-data agreement is heterogeneous across rows: five multi-select
families (59 items, ~28% of unhcr scored cells) mark the sentinel in
round 2 ONLY, and `wave` is GIVEN. A scalar ã pools a near-1 agreement
regime with a near-0 one; the conditional version separates them and the
selection is done on visible data at runtime (no hardcoded column — if
wave truly drives it, the data picks wave).

## Domain check

Pre-registered 2026-09-01 BEFORE implementation.

- (a) Technical: this is E003's empirical-Bayes design one level deeper
  (agreement as a per-cell Bernoulli with partial pooling item → column
  value). Column choice per item by held-out Bernoulli log-likelihood of
  the agree indicator on a 20% split of visible rows, against the scalar
  baseline — only adopted per item when it wins, so the model can only
  degenerate back to E008.
- (b) Background: CATI practice (A001/A002, E003 domain check) says
  round 1 uses the skip marker and round 2 leaves cells empty for the
  multi-select families — agreement should split BY ROUND, i.e. the
  selected column on real data should be the wave/round item for those
  59 items. That prediction is unobservable locally and untestable even
  on the leaderboard at item level (no per-item detail) — the evidence
  is the unhcr aggregate.
- (c) Local evidence plan (E003 precedent — sandbox gates are exact, so
  the clean runner CANNOT show a gain): (1) clean sandbox must equal
  E008 within ±0.002 (ã ≈ 1 everywhere, conditioning never selected or
  irrelevant); (2) violation sim with GROUP-DEPENDENT flip rates (one
  GIVEN column's values get 35% vs 2% flips) must show conditional-ã
  clearly beating scalar-ã; (3) violation sim with UNIFORM flips must
  show conditional-ã ≈ scalar-ã (shrinkage prevents a loss when there is
  no heterogeneity to find). All three pre-registered as the adoption
  evidence; threshold rule applies to (1) as a no-regression bound, and
  adoption is real-data motivated as in E003.

## Change

`src/models/cond_agree.py` (planned): E008 predict with
`agreement_weights` replaced by a conditional estimator. Per gated item:
candidates = GIVEN columns with cardinality ≤ 12; 80/20 split of rows
where parent and child are both visible; per candidate, per-value
agreement shrunk (α = 20) toward the item's fit-split scalar ã; pick the
candidate whose eval-split Bernoulli LL beats the scalar baseline, else
keep scalar. Final estimates recomputed on all visible rows. At predict
time ã depends on the row's value of the selected column (unseen value →
scalar). Everything else (ladder, logistic blend, per-instrument w,
guards) unchanged from E008.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

Clean sandbox — identical to E008 to 4 decimals on every schema
(0.4418 / 0.4994 / 0.4447 / 0.5532, 3-inst mean 0.4991): evidence (1)
no-regression met exactly as pre-registered (exact gates → ã ≈ 1,
conditioning never engages).

Violation sims (unhcr, full E008-vs-E010 pipeline, shared ladder/w from
the clean frame so only the agreement layer differs; seed 1, log score):

| sim | scalar ã (E008) | conditional ã (this) | Δ log |
|---|---|---|---|
| group-dependent flips (35% vs 2% by column value) | −0.8517 | −0.8164 | **+0.0352** (≈ +0.028 skill at U 1.2618) |
| uniform 17% flips | −0.8354 | −0.8353 | +0.0000 |

The sim's group column (first GIVEN with card ≤ 6) happened to be the
sandbox `wave` item — the exact column the domain check predicts real
data will select. Shrinkage no-loss confirmed under uniform violations.
Runtime: agreement selection adds ~10–20 s on unhcr (candidates ×
gated items, vectorized enough); total ≪ 900 s. Tests 4/4 new
(validity, clean ≈ E008, group-sim gain, uniform-sim no-loss).

Reproduce: `PYTHONPATH=. .venv/Scripts/python src/eval/runner.py src/models/cond_agree.py`
and `.venv/Scripts/python -m pytest tests/test_cond_agree.py -s`

## Decision

**Adopted (real-data motivated, E003 precedent).** All three
pre-registered evidence points hit: (1) clean-sandbox Δ = 0.0000
(bound was ±0.002); (2) group-dependent sim +0.0352 log — larger than
E003's own +0.0289, consistent with the heterogeneous-agreement thesis;
(3) uniform sim +0.0000 — the shrinkage guarantees the model can only
degenerate to E008 when there is no heterogeneity. Domain check verdict:
consistent; the real-data claim (the 59 round-2-only multi-select items
select the wave column and unhcr gains) is tested by the 2026-09-01
leaderboard submission. Submission: `submissions/2026-09-01-E010/`.
