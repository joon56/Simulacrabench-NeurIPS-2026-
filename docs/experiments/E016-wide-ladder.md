# E016 — lift the ladder's cardinality cap (governorate into the cells)
parent: E012
status: rejected
date: 2026-09-05

## Hypothesis

Raising the greedy ladder's candidate cap MAX_CARD from 12 to 64 admits
`governorate_col` (K=46) and `s2_4a_origin_governorate_lbl` (K=16) —
and any analogous high-cardinality GIVEN elsewhere — into the count
ladder's selection, improving skill, because residence and origin
geography are among the strongest conditioners in displacement data
(assistance access, rent, services and intentions vary by governorate —
A001/eRPIS reports tabulate by governorate) and the ladder plus the
asked-only conditional tables have NEVER been allowed to see them. The
shared-trunk net encodes them one-hot, but the cell tables and their
κ-shrinkage are a different estimator family — the blend weight decides
row by row. Selection stays fully data-driven: high-card columns only
enter if they win the held-out gain contest, and per-level κ absorbs
cell fragmentation.

## Domain check

Pre-registered 2026-09-05 BEFORE implementation.

- (a) Technical: the risk of high-card cells is fragmentation
  (10k rows / 46 cells ≈ 200 rows), exactly what the E006 κ-backoff
  design absorbs (depth-3 κ already selects 30–100). Greedy selection
  can only add such a column when it beats the incumbent candidates on
  the internal holdout — the change widens the search space, it forces
  nothing.
- (b) Background: eRPIS publishes its tables BY GOVERNORATE — the
  instrument's own designers treat it as a primary stratifier; ditto
  origin governorate for return intentions (Aleppo vs Damascus corridors
  differ). Expectation: unhcr ladder likely swaps a roster column for
  governorate at some depth; unicef/wb unaffected (their GIVEN
  cardinalities were already under 12 except none).
- (c) Sandbox validity: the sandbox has the real column shapes, and the
  invented trait couples every GIVEN to every item, so a K=46 column
  carries signal locally too — the runner threshold (+0.005 vs E012)
  judges normally. Watch point: if the ladder selects governorate
  locally but the gain is < threshold, record the selected ladders
  anyway — the real-data geography claim in (b) would then be testable
  only by a leaderboard A/B, to be its own experiment.

## Change

`src/models/wide_ladder.py` (planned): thin wrapper that runs
shared_trunk.predict (E012) with hier_backoff.MAX_CARD temporarily set
to 64 (restored afterwards). No other knob moves (COND_MAX_CARD, net
config, gates untouched — one change per experiment).

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | sample | unicef | world_bank | unhcr | 3-inst mean | Δ vs E012 |
|---|---|---|---|---|---|---|
| E012 | 0.4429 | 0.5006 | 0.4549 | 0.5629 | 0.5061 | — |
| this | 0.4429 | 0.5006 | 0.4549 | 0.5631 | 0.5062 | +0.0002 |

Watch point recorded: the unhcr ladder DID change —
`governorate_col`(κ100) replaced `s1_2_country_asylum_lbl` at depth 3
(held-out −0.5868 vs −0.5873). The mechanism works; the sandbox gain is
just negligible, consistent with the generator coupling every column to
the trait uniformly (a K=46 column carries no more per-column signal
than a K=4 one locally).

## Decision

**Rejected** (Δ +0.0002 < +0.005). Domain check verdict: (c)'s
contingency fired — selection admits geography but the sandbox cannot
value it. The (b) real-data geography claim (governorate ⊃ country
nesting, eRPIS's own primary stratifier) moves to the leaderboard-A/B
candidate pool alongside E015/E017; do NOT fold it into E017 (one
change per A/B, attribution first).
