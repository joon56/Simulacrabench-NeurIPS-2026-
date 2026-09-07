# E023 — evidence layer stack 2: replay-selected K + second weight iteration
parent: E022
status: rejected
date: 2026-09-08

## Hypothesis

Two further sim-measurable refinements of the household evidence layer
stack on E022: (1) the posterior's candidate count K is chosen by the
replay from {3, 5, 10} — households have 1–3 co-respondents, so K=10
dilutes the evidence with random neighbours whenever the posterior is
not sharply concentrated; (2) a second Fellegi–Sunter iteration
re-estimates the column weights from the purer provisional pairs the
first iteration produces. Same-wave candidate weighting (queued) is
already subsumed: `wave` is a signature column and the EM weight for
it is learned from the data.

## Domain check

Pre-registered 2026-09-08 BEFORE implementation.

- (a) Technical: K is selected on the same replay that calibrates λ
  (pooled replay log score at each K's best per-(item, bucket) λ) —
  three candidates, thousands of rows: negligible selection pressure.
  Smaller-K posteriors are exact restrictions of the K=10 softmax
  (renormalize the kept masses), so no extra matching cost. Iteration 2
  can only move weights toward the agreement pattern of the pairs the
  learned weights select; with no duplicate structure both iterations
  return ≈ rarity-neutral weights and λ→0 (inertness kept).
- (b) Background: household size distribution among Syrian refugee
  households in the region (eRPIS: median 4–5 members, 1–2 adults
  reachable by CATI) says the true co-respondent count per row is
  small — K=3–5 is the natural regime.
- (c) Local evidence plan: hard household sim (ρ ∈ [0.2, 0.8]), each
  refinement alone and composed vs E022; compose what passes
  (> +0.003 log each, composition > E022 + 0.005); clean runner within
  ±0.002; runtime ≤ ~160 s local. The instrument is now quantitatively
  validated (E018/E019/E022 readings), so the sim delta is the expected
  real delta: target composition ≥ +0.015 log (≈ +0.012 skill → unhcr
  0.89–0.90, Grand rounding to 0.64).

## Change

`src/models/hh_stack.py` (planned): E022's layer with (i) the weight
estimation looped `em_iters` times and (ii) the calibration replay run
per K in `k_grid` on restricted posteriors, K chosen by pooled replay
score; held-out evidence built at the chosen K. Everything else E022.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

Hard household sim (ρ ∈ [0.2, 0.8]), vs E022 (−0.5634 log):
K-select alone **+0.0000**, second EM iteration alone **−0.0001**,
both **−0.0001**. The replay picks K=10 (restricting to 3/5 changes
nothing — under the learned weights the softmax already puts
negligible mass on random neighbours), and iteration 2 leaves the
weights where iteration 1 put them.

## Decision

**Rejected — both refinements null.** Reading: the household-matching
layer is SATURATED at E022 on this sim family (weights converged, K
irrelevant, λ ceiling/buckets already applied). The remaining
0.88 → 0.92 gap is therefore not in matching precision or mixing
weights; it must come from structure this sim does not model —
cross-item household structure (a co-respondent's answer to A informing
B; household-level items identical across members) or a better base on
unmatched rows. Next: E024 = evidence-as-input net (E020's idea) used
as the BASE inside E022's mixture, sim-checked for no-harm, spent as a
pre-registered A/B because the sim cannot see cross-item structure.
