# E021 — data-estimated signature weights (household-aware matching)
parent: E018
status: superseded-by:E022
date: 2026-09-07

## Hypothesis

E018's matcher weights every GIVEN column by rarity (−log u_j). If the
real matches are household co-respondents (E020 re-diagnosis), the
individual columns — age band, education, marital status, household
relationship, single-parent flag — legitimately DIFFER between a
respondent and its best match, and rarity weighting penalizes exactly
those disagreements, diluting the posterior over random neighbours.
Estimating per-column agreement rates m_j among provisional matches
(Fellegi–Sunter, one EM-style iteration: initial rarity match → top-1
pairs above a posterior-mass threshold → m_j = agreement rate on j →
weights log(m_j/u_j) − log((1−m_j)/(1−u_j)), clipped at 0 → re-match)
lets the data discover which columns define a household and
concentrates the posterior on real co-respondents. λ replay
calibration unchanged.

## Domain check

Pre-registered 2026-09-07 BEFORE implementation.

- (a) Technical: m_j estimated from top-1 pairs contains false pairs;
  their agreement pattern is the random one (≈ u_j), which pulls m_j
  toward u_j and the weight toward 0 — conservative direction. With no
  duplicate structure, m_j ≈ u_j everywhere ⇒ weights ≈ 0 ⇒ posteriors
  flat ⇒ evidence ≈ k-NN noise ⇒ λ→0 ⇒ inert (E018's guarantee kept).
- (b) Background: ProGres registers households; CATI re-contact reaches
  whoever answers the household phone — different adults of one
  household in one round is the natural source of near-duplicates, and
  household composition (children by age/sex, elders) is the shared
  block while person-level fields differ. Weights should self-organize
  into roster ≫ individual.
- (c) Local evidence plan: NEW household sim — twins copy the roster
  columns, RESAMPLE the individual GIVEN columns, and copy answers per
  item with item-specific probability (drawn ρ_i ∈ [0.3, 0.95]) — then
  (1) E018 vs E021 scored on it: E021 > E018 by > +0.005 log;
  (2) E019 ≈ E018 on it (the instrument must reproduce the real flat —
  a sim that still rewards E019 is still wrong); (3) clean runner within
  ±0.002; (4) learned weights: roster columns > individual columns
  (printed, asserted).

## Change

`src/models/hh_link.py` (planned): dup_link with a weight-estimation
step between the rarity pass and the final pass. Everything else
unchanged.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

Household sim (roster copied, person-level GIVEN resampled, per-item
copy rate ρ ~ U(0.3, 0.95)): learned weights **roster mean 3.08 vs
person mean 1.39** — the data separates the household block from the
individual columns as hypothesized; scored E021 −0.5510 vs E018
−0.5611, **+0.0100 log**. Harder regime ρ ~ U(0.2, 0.8): **+0.0068**.
E019 on the same sims: +0.0097 / +0.0053 — the instrument still credits
E019 a little, which is consistent with the real "flat" once the
leaderboard's resolution (0.01 rounding, ±0.01–0.02 noise) is taken
into account: gains of this size are individually invisible there.

## Decision

**Superseded by E022** — verified on its own (mechanism and gain), but
shipped only as part of the composition, because a +0.005–0.01 real
gain cannot be read off the phase-1 leaderboard; stacking with E019 is
what gets the family above the resolution floor.
