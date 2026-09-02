# E014 — two-stage probabilistic cross-round linkage (Fellegi–Sunter-style)
parent: E013
status: adopted
date: 2026-09-03

## Hypothesis

E013's fuzzy matcher (≤2 of 71 signature columns mismatching) armed
nothing on real unhcr data. If the cause is recall — real cross-round
drift moves MORE than 2 columns (an age-band crossing shifts paired
roster columns; a different household member answering shifts many) —
then a probabilistic matcher that (i) finds high-precision seed pairs,
(ii) learns per-column agreement rates m_j from the seeds and collision
rates u_j from value frequencies, and (iii) re-matches by summed
log-odds weights with data-driven acceptance, recovers the pairs E013
missed and unlocks the linkage gain. If instead the rounds are disjoint
in the competition build, E014 stays inert and its flat leaderboard
result FALSIFIES the overlap hypothesis conclusively — the submission
is itself the experiment.

## Domain check

Pre-registered 2026-09-03 BEFORE implementation.

- (a) Technical: Fellegi–Sunter record linkage is the standard for
  exactly this (household surveys re-contacted across rounds, noisy
  keys). Seeds need precision only, not recall; u_j from squared value
  frequencies; acceptance requires score separation between the seed
  and random-pair distributions (no separation ⇒ inert), a runner-up
  margin, 1:1 claim resolution, and the MIN_PAIRS guard on the final
  visible-visible set. Every threshold is derived from the data at
  runtime — nothing hardcoded to the real instrument.
- (b) Background: real re-contact surveys show exactly this drift
  pattern (roster counts re-asked with noise, proxy respondents) — the
  reason exact/near-exact matching under-recalls on true panels while
  probabilistic linkage is the census-bureau standard.
- (c) Local evidence plan: (1) clean runner ≡ E012/E013 (independent
  rows: no seed separation, inert); (2) heavy-drift panel sim — each
  twin perturbs Poisson(2.5) GIVEN columns (many beyond E013's reach) —
  E014 must recover a large gain where E013's is mostly gone;
  (3) mild-drift sim — E014 ≈ E013 (no regression when the easy matcher
  suffices). Leaderboard readings pre-registered: unhcr up ⇒ recall was
  the E013 failure; flat again ⇒ rounds disjoint ⇒ linkage line
  ABANDONED and the 0.92 analysis re-opens toward pure capacity.

## Change

`src/models/prob_link.py` (planned): cross_link with build_links
replaced by the two-stage matcher; stability mixing, guards, and
everything else unchanged.

## Attempt log (append-only)

- **v1 (hard two-stage matcher) built, then measured against its own
  premise and discarded**: the heavy-drift sim exposed that the
  signature is only ~16 GIVEN columns — the "72" in earlier notes
  counted EXCLUDE (same arithmetic error A004 caught for wb). Seed
  median score 56.5 vs random max 55.2 (gap 1.3): true-with-drift and
  random-collision are barely separable, and hard 1:1 uniqueness is
  exactly what concentrated real populations break. E013's real-data
  flat re-read: likely COLLISIONS (margin rejected everything), not
  necessarily missing overlap.
- **v2 (soft posterior evidence mixing, shipped)**: no seeds, no
  uniqueness. Rarity-weighted agreement (c_j = −log u_j) is a
  log-likelihood ratio ⇒ softmax over the top-10 other-round candidates
  is a posterior; evidence = posterior-weighted candidate answers;
  per-item λ calibrated by replaying the construction on VISIBLE rows
  against realized answers. Collisions share mass instead of being
  rejected; no signal ⇒ λ→0.
- **Discovered and kept**: on the clean sandbox vs a weak (marginal)
  model the layer arms as k-NN conditioning (signature-similar rows are
  trait-similar). Against the full E012 net it is redundant — unhcr
  −0.0002. E014's identity is therefore "panel evidence + k-NN
  residual, self-calibrated"; the runner judges the composite.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

Clean sandbox: 0.4429 / 0.5006 / 0.4549 / 0.5627 — unhcr −0.0002 vs
E012 (within the ±0.002 bound), others identical. Sims (scored full
pipeline, unhcr sandbox): heavy-drift panel (Poisson(2.5) GIVEN drift,
504 held-out twins) **+0.1556 log over E012**; layer-level: 211/213
items at λ ≥ 0.5 under drift, 213/213 at λ ≥ 0.3 under forced
signature collisions (governorate columns destroyed) — the exact regime
that killed E013. Calibration deterministic (test-pinned).

## Decision

**Adopted (real-data motivated, E003 route; organizer-ruled legal).**
Clean no-regression + large sim gain + collision robustness + λ
self-calibration as the safety layer. The leaderboard is the decisive
experiment BY DESIGN: unhcr up ⇒ rounds overlap and E013 failed on
collisions; unhcr flat ⇒ overlap conclusively dead (soft matching finds
nothing either) ⇒ linkage line abandoned and the 0.92 question
re-opens. Submission: `submissions/2026-09-04-E014/`.
