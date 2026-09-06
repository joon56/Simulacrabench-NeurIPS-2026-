# E019 — sharpen the evidence layer (λ ceiling + concentration buckets)
parent: E018
status: parked
date: 2026-09-06

## Hypothesis

Two calibration refinements close part of the 0.87→0.92 gap E018
opened: (1) extending the λ grid past 0.9 to {0.95, 0.98} — a
near-exact twin's evidence puts ~1.0 on the truth, and the current 0.9
ceiling forces every matched cell to keep 10% model mass it does not
want; (2) calibrating λ per (item × posterior-concentration bucket) —
one λ per item currently averages over exact-twin rows (max posterior
weight high, want λ≈0.98) and diffuse-kNN rows (want λ low), so both
regimes get a compromise. Split at max-q ≥ 0.5, two λs per item, same
replay estimator on both buckets.

## Domain check

Pre-registered 2026-09-06 BEFORE implementation.

- (a) Technical: both changes stay inside the replay-calibration
  contract — the data picks every λ, ceilings and buckets only widen
  the hypothesis space; degenerate data still tunes everything to 0.
  Risks: λ=0.98 amplifies a FALSE match's damage (wrong twin answer at
  0.98 ⇒ log(0.02+…) per cell) — the concentration bucket is itself the
  guard (false matches are diffuse, they land in the low-λ bucket);
  bucket splitting halves the replay sample per estimate (≥ ~1–3k rows
  per bucket per item on unhcr — still ample for a 12-point grid).
- (b) Background: E018's leaderboard result implies a large exact-twin
  subpopulation (roughly a third to half of DEV rows) — precisely the
  regime where the 0.9 ceiling binds. The leaders' 0.92 is consistent
  with mixing weights near 1 on matched rows.
- (c) Local evidence plan: the within-round dup sim is now a VALIDATED
  instrument (its ≥+0.02 arm fired at +0.09 on the real leaderboard).
  (1) dup-sim scored: E019 > E018 by > +0.005 log; (2) clean runner
  within ±0.002 of E018 (no duplicates ⇒ buckets inert); (3) unit test
  on bucket split + λ structure. E003-route adoption.

## Change

`src/models/link_sharp.py` (planned): dup_link with (i) LAMBDA_GRID
extended {0 … 0.9, 0.95, 0.98}; (ii) per-item λ becomes a pair
(diffuse, concentrated) split at max posterior weight ≥ 0.5, both
replay-calibrated; evidence rows carry their concentration flag so
predict applies the matching λ. Everything else (pool, scoring,
self-exclusion, caps, E012 stack) unchanged.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

Clean sandbox: 0.4429 / 0.5006 / 0.4549 / 0.5626 — identical to E018
(no duplicates ⇒ buckets inert), 239 s local.

Within-round dup sim (the leaderboard-validated instrument; same frame
as E018's test): **E018 −0.4849 → E019 −0.4537, Δ +0.0312 log** —
6× the +0.005 bar. λ structure verified: the concentrated bucket's λ
exceeds the old 0.9 ceiling on real twins, and concentrated λ ≥ diffuse
λ on average (the two regimes separate as hypothesized). Tests 2/2 new.

Reproduce: `.venv/Scripts/python -m pytest tests/test_link_sharp.py -q -s`

## Decision

**Adopted (E003 route on a validated sim).** Both refinements pay on
the instrument that predicted E018's +0.09; clean no-regression exact.
Leaderboard readings pre-registered in SCORES.md. Submission:
`submissions/2026-09-07-E019/`.
