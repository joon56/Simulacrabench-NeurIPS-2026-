# E012 — shared-trunk multi-head network replacing the per-item logistic
parent: E010
status: adopted
date: 2026-09-02

## Hypothesis

Replacing E008/E010's 76–213 independent per-item logistics with ONE
network per instrument — one-hot GIVEN block → small shared trunk →
per-item softmax heads (plus asked-only conditional heads), trained
jointly on complete visible rows with holdout early stopping — beats
E010, because (i) the target quantity P(item | GIVEN) =
∫ P(item | θ) p(θ | GIVEN) dθ is nonlinear in the GIVEN one-hots even
under the sandbox's own single-trait generator (marginalizing a latent
factor creates effective interactions a main-effects logistic cannot
represent), and (ii) sharing the trunk across all items is cross-item
partial pooling — the supervised form of the latent-trait structure the
kit's own tutorial warns makes answers conditionally dependent.

## Domain check

Pre-registered 2026-09-02 BEFORE implementation.

- (a) Technical: multi-task heads with a shared representation =
  standard cross-task regularization; joint CE over items. The blend
  weight w (per instrument, holdout-tuned, same grid) stays as the
  calibration guard, so an overconfident net gets down-weighted the way
  the logistic did. Early stopping on the same internal 20% split.
- (b) Background: real instruments are SECTIONED (unhcr s2 household /
  s3 return / s4 work / s6 income; wb self-report vs timed cognitive) —
  a multi-factor answer process. A shared trunk (width > 1) can carry
  several factors; the per-item logistic carries none. unhcr and wb
  should benefit most (many heads to share across); unicef least
  (12 heads, 7 GIVEN).
- (c) Sandbox validity: the generator IS a 1-factor nominal model with
  trait_scale 2.0 — the mechanism (latent marginalization ⇒ nonlinear
  P(y|x)) is present locally, so THIS experiment is judged by the
  normal +0.005 runner threshold, no sim channel needed. Watch point:
  if the net only ties the logistic locally, that is evidence the
  logistic already saturates a 1-factor world — reject here, and any
  real-data multi-factor bet would need its own evidence channel.

## Change

`src/models/shared_trunk.py` (planned): E010 with the logistic component
swapped for a torch MLP — one-hot GIVEN (D) → Linear(D, 64) → ReLU →
Linear(64, 64) → ReLU → per-item heads Linear(64, K_i) for full
distributions and Linear(64, K_values_i) for asked-only conditionals
(masked CE on asked rows). Adam, full-batch or large-batch, early stop
on holdout CE (patience-based), fixed torch seed. Blend with the ladder
by per-instrument holdout-tuned w exactly as before; ladder, gate
recursion, conditional agreement (E010) unchanged. CPU is enough
locally (~seconds per instrument at this width); the hosted H100 makes
it trivial. Budget profiled before packaging.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | sample | unicef | world_bank | unhcr | mean | Δ vs E010 (3-inst) |
|---|---|---|---|---|---|---|
| E010 (parent) | 0.4418 | 0.4994 | 0.4447 | 0.5532 | 0.4848 | — |
| this | 0.4429 | 0.5006 | 0.4549 | 0.5629 | 0.4904 | **+0.0070** |

3-inst mean (sample excluded): 0.4991 → 0.5061 — the first model-class
change to clear the threshold since E008. Placement matches the
pre-registered (b) expectation exactly: wb largest (+0.0102 — first
real wb movement in any experiment, 76 heads sharing one trunk), unhcr
next (+0.0097, 213 heads), unicef smallest (+0.0012, 12 heads). Sample
+0.0011.

Wall-clock ~200 s local CPU total (torch full-batch; hosted H100 makes
this trivial). Deterministic (fixed torch seed; repeat runs bit-close,
test-verified). Tests 3 new (validity, determinism, conditional-head
mask correctness); suite green.

Context from the same day (recorded in E011/log): per-item capacity
(E009), option-axis pooling (E011), holdout-seed bagging (probe: 3-inst
spread 0.0003 across seeds 0/1/2), and pseudo-count priors (E007) all
measured ≈ 0 — the gain here is specifically the model-CLASS change
(nonlinearity + cross-item sharing), not more knobs on the old class.

Reproduce: `PYTHONPATH=. .venv/Scripts/python src/eval/runner.py src/models/shared_trunk.py`

## Decision

**Adopted.** Δ = +0.0070 > +0.005, within budget. Domain check verdict:
consistent — (a) the latent-marginalization nonlinearity is measurable
exactly where the generator puts it, (c)'s watch point resolved in favor
of the net (the logistic did NOT saturate the 1-factor sandbox). The
real-data multi-factor claim in (b) — wb/unhcr gaining MORE than the
sandbox Δ because real instruments are sectioned — is tested by the
2026-09-02 leaderboard submission. Submission:
`submissions/2026-09-02-E012/`.
