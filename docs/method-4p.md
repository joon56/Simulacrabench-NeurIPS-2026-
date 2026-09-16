# Method description (4-page draft) — HSCC phase-2 submission

> Draft 2026-09-12 from the experiment tree (docs/tree.md, E001–E029).
> Required with the phase-2 submission. Sections marked [P2] are filled
> from the phase-2 runner and the final packaged model; every number
> here must match docs/log.md and the snapshot in submissions/.

## 1. Problem framing

Each held-out respondent shows only its GIVEN block; every PREDICT cell
is blank and scored by log probability of the realized answer, pooled
over cells, expressed as skill = 1 + log_score / U (U = mean log K over
scored items, gate sentinel included). Three things follow and shaped
every decision below. (i) The gate sentinel ("never asked") is an
ordinary scored answer, so predicting *who is skipped* is worth as much
as predicting *what they say*; on UNHCR ERPIS 156 of 213 scored items
are gated, so the gate structure alone carries a large share of the
score. (ii) The grader floors every probability at 1e-3: a confident
wrong cell costs ≈ 6.9 nats against ≈ 1.4 for an honest hedge, so
calibration dominates sharpness. (iii) The leaderboard is a plain mean
of the three instruments' skills, so UNHCR (largest item count, lowest
U, deepest gate cascades) is where the headroom is.

We optimized exact held-out skill on locally built sandboxes (the kit's
`make_sandbox`, real schema, invented marginals) and on simulations
layered on top of them, and used the noised phase-1 leaderboard only as
a pre-registered A/B channel. Every model change is one experiment file
with a parent, a pre-registered domain check, a measured Δ and a verdict
(adoption threshold Δ mean skill > +0.005 on the three instruments).

## 2. Preprocessing and skip logic

**Option vectors.** Every item's option list comes from the schema
(`values` plus the `gated_value` slot for gated items); data order is
never used. EXCLUDE items are dropped by class, not by position. NaN
means "held out" and nothing else; refusals and "don't know" are
ordinary levels.

**Gate recursion (E002).** Items are decoded in schema order so a gated
child sees its parent's belief. With b_parent the parent's vector
(one-hot if visible, a predicted distribution if not),

    P(asked) = Σ_{v ∈ observed_if} b_parent[v]
    hard_i   = [ P(asked) · cond_i ,  1 − P(asked) ]

where cond_i is the child's distribution *given asked* (its own model,
trained on asked rows only). Chains close automatically because each
parent's sentinel mass propagates to its children.

**Softened coupling (E003/E005).** Gates are approximate on the real
UNHCR data (schema: agreement median 0.83, range 0.29–0.98). Hard
coupling is therefore mixed with the child's unconditional model:

    belief_i = a_i · hard_i + (1 − a_i) · soft_i

with a_i the child's gate-agreement rate on visible rows, beta-binomial
shrunk toward 1 (α = 20). On exact gates a_i → 1 and the mixture is the
hard gate.

**Conditional agreement (E010).** Because agreement is heterogeneous
across rows (e.g. five multi-select families mark the sentinel in one
CATI round only), a_i becomes a function of at most one GIVEN column
(cardinality ≤ 12), chosen per gated item by held-out Bernoulli
log-likelihood of the agree indicator on a 20% split; the per-value
rates are shrunk toward the item's scalar. If no column beats the
scalar, the scalar stays.

Two structural extensions were built and measured null on the
leaderboard — parent-value-conditional decoding of the overlapping
return-intention branches (E028) — or rejected locally, and are kept in
the tree for the record.

## 3. Model

The stack has three stages, each adopted on a measured gain and each
inert when its signal is absent.

**3.1 Hierarchical backoff ladder (E004–E006).** Partial pooling over
GIVEN cells approximated by count smoothing: with an ordered list of
GIVEN columns c_1..c_D, level L conditions on (c_1..c_L) and uses level
L−1 as its prior,

    p_L(v | cell) = (n_L(v) + κ_L · p_{L−1}(v | parent cell)) / (n_L + κ_L).

Column order, depth (≤ 3) and κ_L ∈ {1, 3, 10, 30, 100} are selected
greedily at run time by held-out log score on a 20% split of the
complete visible rows; nothing is hard-coded to any instrument. Gated
children ride the same ladder for their asked-only conditionals.
Leaderboard: 0.43 (marginal) → 0.53 (gated marginal + softening) → 0.55
(ladder).

**3.2 Shared-trunk multi-head network (E008 → E012, E017/E025).** The
ladder sees at most three columns. The full one-hot GIVEN block feeds
one network per instrument: Linear–ReLU trunk → a softmax head per
PREDICT item (full distribution, sentinel included) plus a masked
asked-only conditional head per gated item; pooled cross-entropy, Adam,
full batch, early stopping on an inner split, final retrain on all
complete rows for the selected epoch count. The trunk architecture is
chosen per instrument from {64×2, 128×2 + dropout 0.1} on the outer
holdout. The net replaced 76–213 independent multinomial logistics
(E008) because marginalizing a latent respondent factor makes
P(item | GIVEN) nonlinear and shared across items; the gain ordering
across instruments followed the number of heads exactly as
pre-registered. The net and the ladder are mixed in probability space,

    model_i = w · net_i + (1 − w) · ladder_i,

with one w per instrument from a 0.1 grid on the outer holdout — the
calibration guard that keeps an over-sharp net from paying the floor
penalty. Leaderboard: 0.55 → 0.58 (logistics) → 0.60 (shared trunk).
(A 3-seed ensemble and an output temperature tuned jointly with w
were measured at +0.0004 and exactly zero, E029: the early-stopped net
is already calibrated.)

**3.3 Visible-row evidence layer (E014 → E018 → E022).** The organizers
confirmed that matching rows within a dataset is permitted. Household
co-respondents, re-dials and double entries share most of their GIVEN
signature and much of their answers, and the datasets contain them.
For every held-out row, every visible row is a candidate (self excluded
in the calibration replay). A Fellegi–Sunter score sums per-column
agreement weights log(m_j/u_j) − log((1−m_j)/(1−u_j)) (clipped at 0);
u_j is the random-agreement probability from value frequencies, m_j the
agreement rate among provisional top-1 pairs with concentrated posterior
— one iteration, so household-defining columns keep their weight while
person-level columns (age, education, relationship) lose it. A softmax
over the top-10 candidates gives a posterior q(c); the evidence vector
for item i is Σ_c q(c) · onehot(answer_c,i). It enters the belief before
gated children consume parent beliefs:

    belief_i = (1 − λ_{i,b}) · model_i + λ_{i,b} · ev_i,

with λ chosen per (item, concentration bucket b ∈ {diffuse,
concentrated: max q ≥ 0.5}) from a grid up to 0.98 by replaying the
identical construction on visible rows against their realized answers.
Data without duplicate structure drives m_j → u_j, the posteriors flat,
and every λ to 0: the layer is bit-inert on the clean sandbox and was
validated on a household simulation (co-respondent twins injected with
per-item copy rates ρ ∈ [0.2, 0.8]) whose predicted gains matched the
leaderboard readings quantitatively. Leaderboard: 0.60 → 0.63
(unhcr 0.78 → 0.87 → 0.88 → 0.89).

## 4. Calibration

All calibration is decided on visible rows only, at run time, per
instrument: the ladder's κ and depth, the net's early-stop epoch and
architecture, the net/ladder weight w, the gate-agreement rates a_i and
their conditioning column, and the evidence weights λ_{i,b}. No
parameter is set from the sandbox or from the leaderboard. Where the
holdout has too little data (the kit's smoke frame) every knob falls
back to its inert value (w = 0, λ = 0, scalar a_i), which the zip
checker exercises before each submission. Sharpness beyond what the
holdout supports was rejected repeatedly: per-item blend weights and
regularization grids (E009), ordinal option smoothing (E011), published
marginal priors (E007), and further matching refinements (E023) all
measured ≈ 0.

## 5. Training and compute budget

Nothing is fitted offline: `predict()` receives the frame, fits every
stage on its visible rows, and returns the vectors. No bundled
artifacts, no `models.txt`, no external data; dependencies are the
hosted image's numpy/pandas/torch/scikit-learn. Training runs on the
hosted GPU with an automatic CPU fallback. Wall-clock on the sandbox
(8-core CPU, no GPU):

| phase | unicef | world_bank | unhcr | total | budget |
|---|---|---|---|---|---|
| 1 (TRAIN visible, DEV scored) | 26 s | 60 s | 151 s | 241 s | 900 s |
| 2 (TRAIN+DEV visible, TEST scored) | 30 s | 64 s | 149 s | 254 s | 3600 s |

Phase-2 settings: the phase-1 model of record unchanged. Three
phase-2-motivated additions were measured and left out — a lifted
calibration-replay cap (6,000 → all visible rows: +0.0000 / +0.0005 on
the phase-1 / phase-2 household sims, flat on the leaderboard), a
3-seed net ensemble (+0.0004 locally) and a relation-split evidence
weight (flat on the leaderboard) — because a single no-retry
submission is not the place for components whose measured value is
zero. Worst case (no GPU): ≈ 250 s local CPU × the observed hosted
slowdown (≤ 4×) ≈ 1,000 s, inside 3,600 s.

## 6. Results

Local exact skill (kit sandbox, seed 0, phase 1) and the phase-1
leaderboard (Laplace-noised, rounded to 0.01) for the adopted chain:

| stage | local unicef / wb / unhcr | LB Grand | LB unicef / wb / unhcr |
|---|---|---|---|
| E002 gated marginal | 0.323 / 0.291 / 0.430 | 0.43 | 0.45 / 0.43 / 0.41 |
| E005 + softened gates + strata | 0.459 / 0.411 / 0.535 | 0.53 | 0.49 / 0.48 / 0.63 |
| E006 backoff ladder | 0.477 / 0.420 / 0.538 | 0.55 | 0.50 / 0.48 / 0.66 |
| E008 + full-GIVEN logistics | 0.499 / 0.445 / 0.553 | 0.58 | 0.51 / 0.49 / 0.74 |
| E010 + conditional agreement | 0.499 / 0.445 / 0.553 | 0.59 | 0.51 / 0.49 / 0.77 |
| E012 shared-trunk net | 0.501 / 0.455 / 0.563 | 0.60 | 0.52 / 0.49 / 0.78 |
| E018 full-pool evidence | 0.501 / 0.455 / 0.563 | 0.63 | 0.52 / 0.49 / 0.87 |
| E022 household weights ∘ sharp λ | 0.501 / 0.455 / 0.563 | 0.63 | 0.52 / 0.49 / 0.88 |
| E025 + trunk capacity selection | 0.501 / 0.455 / 0.563 | 0.63 | 0.52 / 0.49 / 0.89 |
| phase-2 submission = E025 | 0.490 / 0.462 / 0.565 (phase-2 cells) | — | — |

**Where the remaining loss sits (probe submissions, unhcr).** Four
phase-1 slots were spent on measurement rather than rank: replacing a
defined cell subset with the uniform vector removes exactly its
contribution (share and the uniform vector's own skill are exact from
the schema), and switching a component off reads its contribution.
Results: gated items 0.892 per cell vs content items 0.885 (on the
exact-gate instruments gated cells are twice as easy — on UNHCR the
approximate gates make them no easier); with the model's sentinel mass
kept and content flattened, gated cells fall to 0.56, so most gated
skill is content prediction on asked cells; with the evidence layer
off, UNHCR falls to 0.79 — the layer is worth +0.10. A Bayes-optimal
oracle for the sandbox generator (replaying its random stream) puts
the base model within 0.004 skill of the GIVEN-only ceiling on every
sandbox, which is why base-model changes could not be validated
locally and only the evidence layer had local headroom.

The sandbox is blind to two of the adopted gains by construction
(random marginals carry no household structure and no capacity
signal), which is why the household simulation and pre-registered
leaderboard A/Bs exist. Local-vs-leaderboard agreement: every
pre-registered direction held; magnitudes on real data exceeded the
sandbox by 3–5× because real GIVEN coupling is stronger than the
sandbox trait.

## 7. Reproducibility

Repository: `src/models/` (one module per experiment, rejected code
kept), `src/eval/runner.py` (in-process scorer using the kit's own
`score()`), `tests/` (simulations), `docs/experiments/E0XX-*.md`
(hypothesis → domain check → result → verdict), `docs/tree.md`. All
seeds fixed (holdout 0, torch 0); one command reproduces every local
number: `python src/eval/runner.py <main.py>`. The submission is a
single self-contained `main.py` assembled from the verified modules and
checked for parity against them before packaging. License and
disclosure obligations: [verify against the Codabench terms accepted at
registration; no external models or data were used].
