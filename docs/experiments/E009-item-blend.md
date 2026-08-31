# E009 — per-item blend weight + regularization grid on the E008 logistic
parent: E008
status: rejected
date: 2026-09-01

## Hypothesis

Replacing E008's single per-instrument blend weight (and fixed C=1.0)
with a per-PREDICT-item (C, w) pair chosen jointly on the internal
holdout beats E008, because items differ systematically in (i) how much
GIVEN signal exists (roster/demographic-driven items vs attitude items)
and (ii) effective sample size (asked-only conditionals shrink n), so
one instrument-level w necessarily underfits the strong items and
overfits the weak ones. C grid {0.3, 1.0, 3.0} adds a capacity axis in
both directions around E008's C=1.0.

## Domain check

Pre-registered 2026-09-01 BEFORE implementation.

- (a) Technical: per-target model selection is standard; the risk is
  winner's curse on the holdout (unicef ~2.9k / wb ~1.3k / unhcr ~1.6k
  eval cells per item, 33-point grid). Mitigation: the runner's DEV
  cells are untouched by tuning — a holdout-overfit selection shows up
  there as a non-gain, and the adoption threshold (+0.005) decides. If
  E009 gains on the tuning holdout but NOT on the runner, that IS the
  winner's curse measured — record and fall back to coarser sharing
  (e.g. per-item w, global C).
- (b) Background: expected heterogeneity is real, not noise — unhcr
  household-roster/demographic items should take high w (GIVEN block
  contains the roster), intention/attitude items lower w; wb psychometric
  band items should prefer w high with C ≥ 1 if the many-weak-predictors
  story from E008's open claim is real. **This experiment doubles as the
  wb probe**: wb rising on the runner AND its chosen w clustering high
  supports the story; wb flat again with per-item capacity leaves the
  claim dead on real data regardless of sandbox behavior.
- (c) Sandbox validity: trait_scale=2.0 gives real per-item signal
  differences (gate children vs plain items), so the mechanism and the
  selection code are locally measurable; real-data placements are
  leaderboard-tested. Watch point: chosen w should SPREAD (not collapse
  onto the E008 global value) if the hypothesis is right.

## Change

`src/models/item_blend.py` (planned): E008 machinery unchanged (ladder,
gate recursion, E003 softening, guards). tune step now returns
{item: (C, w)}: per item, fit logistic per C on the 80% split, score the
33-point (C, w) grid on the 20% split against the item's ladder
distribution, take the argmax; single-class items keep w=0. Final fit
per item uses its chosen C on all complete rows; the item's w applies to
both its full and asked-only conditional distributions (as in E008).
Runtime: tuning fits ×3 vs E008 (~+50 s local estimate) — profile.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | sample | unicef | world_bank | unhcr | mean | Δ vs E008 (3-inst) |
|---|---|---|---|---|---|---|
| E008 (parent) | 0.4418 | 0.4994 | 0.4447 | 0.5532 | 0.4848 | — |
| this | 0.4414 | 0.4994 | 0.4463 | 0.5554 | 0.4856 | +0.0013 |

Direction positive everywhere that matters (wb +0.0016, unhcr +0.0022,
unicef flat) but far under threshold. Wall-clock grew 182 → 306 s (C-grid
tuning ×3). Tests 4/4 (validity, all-w=0 ≡ E006, deterministic tuning +
heterogeneous w chosen, param shapes).

Reproduce: `PYTHONPATH=. .venv/Scripts/python src/eval/runner.py src/models/item_blend.py`

## Decision

**Rejected.** Δ(3-inst mean, sample excluded) = +0.0013 < +0.005. Domain
check verdict: the pre-registered winner's-curse arm fired — per-item
holdout selection did not transfer to DEV. Deeper reading (recorded for
the tree): the sandbox generator is single-trait with roughly uniform
item coupling, so per-item heterogeneity barely exists locally BY
CONSTRUCTION — this experiment cannot distinguish "no heterogeneity"
from "sandbox can't show it". Real data likely has the heterogeneity
(claim (b)), but the fixed threshold rules here and E009 has no E003-style
alternative evidence channel. Code kept for revival if a later diagnostic
shows real per-item spread. Capacity-axis lesson: on a single-trait
sandbox the main-effects logistic is near-optimal, so further capacity
(per-item tuning, boosted interactions) is locally capped — the next
locally-measurable lever must be STRUCTURAL, not capacity.
