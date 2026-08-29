# E006 — hierarchical backoff ladder (MRP-lite) + soft gating
parent: E005
status: adopted
date: 2026-08-29

## Hypothesis

Replacing E004's flat 1–2-column stratum with a backoff ladder — cell →
parent cell → single column → marginal, each level's distribution using the
level above as its prior pseudo-counts, p_L = (count_L + κ_L·p_{L-1}) /
(n_L + κ_L) — approximates MRP partial pooling and beats E005, because the
2026-08-28 leaderboard showed real GIVEN-answer coupling is STRONGER than
the sandbox trait (unhcr +0.22 vs sandbox +0.105): deeper conditioning
should pay where cells stay populated, and κ_L absorbs the rest.

## Domain check

Pre-registered 2026-08-29 BEFORE implementation. (a) MRP literature (domain
guide §7.1): gains from deeper cells shrink as cells empty — if the greedy
ladder stops at depth 2 or the depth-3 gain is ~0, that is the empty-cell
thesis measured, not a failure. (b) Real-data expectations: unhcr should
sustain depth 3 (10.3k rows over country×wave cells of ~1.3k rows each —
room for one more split, e.g. household composition); wb sparse-answer
GIVEN columns ('Not answered' heavy) should be absorbed by κ rather than
selected deep; unicef depth beyond Country+religion likely thin (1.5–2k
per country). Local caveat as always: sandbox content is random — local
run validates the ladder mechanism and the stop rule, not these real-data
placements; the leaderboard triple tests them.

## Change

`src/models/hier_backoff.py` (planned): greedy forward selection of up to
3 GIVEN columns (card ≤ 12) on the E004 internal holdout; per-level κ from
{1,3,10,30,100}; stop when held-out gain ≤ 0. Gate coupling and E003
agreement-weighted softening unchanged from E005 (asked-only conditionals
get the same ladder). Submission build inlined as
`submissions/2026-08-29-E006/main.py` if adopted.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | sample | unicef | world_bank | unhcr | mean | Δ vs E005 (3-inst) |
|---|---|---|---|---|---|---|
| E005 (parent) | 0.4333 | 0.4593 | 0.4105 | 0.5347 | 0.4595 | — |
| this | 0.4385 | 0.4772 | 0.4196 | 0.5382 | 0.4684 | **+0.0101** |

Ladders selected (sandbox; greedy, held-out log score per depth):

- sample: urban_rural(κ30) → age_band(κ1) → region(κ100); −0.8888 →
  −0.7697 → −0.7473 → −0.7383
- unicef: Q13(κ1) → Q05(κ10) → Country(κ30); −1.3153 → −1.0449 → −0.8496
  → −0.8266
- world_bank: wageOfSimilarEmployees(κ30) → group(κ30) →
  employmentStatus(κ30); −1.5315 → −1.2814 → −1.2138 → −1.1984
- unhcr: girls_0_5(κ30) → hh_relationship(κ30) → country_asylum(κ100);
  −0.7172 → −0.6082 → −0.5899 → −0.5873

**MRP watch point measured**: depth-3 marginal gains shrink everywhere
(unicef 0.195→0.023, wb 0.068→0.015, unhcr 0.018→0.003 log/cell) and the
selected depth-3 κ rises (30/100) — partial pooling kicks in exactly as
the empty-cell thesis predicts. Selection cost: 0.4/2.4/12/75 s; total
runner wall-clock ~95 s (≪ 900 s). Tests 4/4 (validity, empty-ladder ≈
E002, fallback chain, large-κ collapse to parent). Official score.py:
PASS 0.4800 / 0.4200 / 0.5400.

Reproduce: `PYTHONPATH=. .venv/Scripts/python src/eval/runner.py src/models/hier_backoff.py`

## Decision

**Adopted.** Δ(3-inst mean, sample excluded) = 0.4783 − 0.4682 = +0.0101 >
+0.005 within budget. Domain check verdict: consistent — depth-gain decay
and κ growth at depth 3 match the MRP prediction; real-data ladder
composition is tested by the leaderboard (expect country_asylum/wave to
enter for unhcr on real data). 2026-08-29 submission.
