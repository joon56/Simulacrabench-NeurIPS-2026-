# E015 — trunk capacity selection for the shared multi-head net
parent: E012
status: parked
date: 2026-09-03

## Hypothesis

Selecting the trunk architecture per instrument from a small grid
(width {64, 128, 256} × depth {2, 3}, dropout at the wider settings) on
the internal holdout beats E012's fixed 64×2, because (i) the E013-flat
result weakens the linkage explanation of the 0.92 unhcr leaders,
leaving "much stronger conditional models" as the leading alternative,
and (ii) the campaign's most reproduced pattern is that real
GIVEN-answer coupling is 3–5× the sandbox trait — a capacity increase
that is merely neutral-to-slightly-positive locally is likely
under-measured relative to its real-data value.

## Domain check

Pre-registered 2026-09-03 BEFORE implementation.

- (a) Technical: architecture selection over 4 configs on the pooled
  holdout CE is mild selection pressure (not E009's 33-point per-item
  grid); the runner's untouched DEV cells remain the arbiter. Dropout +
  early stopping guard the wider settings against memorizing 8k rows.
- (b) Background: unhcr's sectioned multi-factor structure (household /
  return intentions / work / income) is the case for width — more
  factors than a 64-dim single trunk comfortably carries alongside 213
  heads. unicef (12 heads, 7 GIVEN) should select the small config —
  watch point: if the selector picks 256 for unicef, suspect holdout
  overfitting rather than signal.
- (c) Sandbox validity: the generator is 1-factor, so the LOCAL gain
  ceiling for capacity is low by construction (E009/E011 lesson). The
  runner threshold (+0.005) still governs adoption; if the result lands
  in (0, +0.005), the pre-registered fallback is to PARK with the
  real>sandbox amplification argument explicitly NOT invoked as an
  adoption loophole — a leaderboard A/B on a later slot may test it,
  but only as its own pre-registered experiment.

## Change

`src/models/shared_trunk.py` parameterized (width, depth, dropout as
arguments; defaults unchanged = E012 exactly); new
`src/models/trunk_select.py`: per instrument, train each grid config on
the inner split, pick by outer-holdout pooled CE of the net alone, then
tune w and final-retrain at the chosen config. Runtime profiled
(4 configs × ~10–40 s per instrument locally; hosted H100 trivial).

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | sample | unicef | world_bank | unhcr | 3-inst mean | Δ vs E012 |
|---|---|---|---|---|---|---|
| E012 | 0.4429 | 0.5006 | 0.4447→0.4549 | 0.5629 | 0.5061 | — |
| this | 0.4436 | 0.5006 | 0.4548 | 0.5633 | 0.5062 | +0.0001 |

(shared_trunk parameterization itself verified bit-identical to E012 at
the default config before the selection run.) unicef unchanged — the
selector did NOT chase a big config there (watch point (b) clean).
Runtime grows ~2× (4 configs trained per instrument).

## Decision

**Parked** per the pre-registered (c) fallback: Δ = +0.0001 lands in
(0, +0.005). The 1-factor sandbox caps capacity gains by construction
(third confirmation after E009/E011), and the real>sandbox
amplification argument is explicitly NOT invoked as an adoption
loophole. Revive path: a dedicated pre-registered leaderboard A/B on a
spare slot, or any future local evidence channel that can see
multi-factor structure.
