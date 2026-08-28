# E004 — GIVEN-stratum backoff with interpolated smoothing
parent: E002
status: adopted
date: 2026-08-28

## Hypothesis

Conditioning each item's distribution on a low-cardinality GIVEN stratum
(country; country×wave on unhcr), interpolated with the crowd marginal via
a count-dependent weight λ = n/(n+κ) (Jelinek–Mercer / Witten–Bell, κ tuned
on a held-out split of visible rows), improves skill directly and — because
gate parents become respondent-specific — unlocks the unhcr gate cascade
that E002 could not use (155/156 gates on PREDICT parents).

## Domain check

Pre-registered 2026-08-28, before implementation. Background domain
(A001/A002) predicts: (a) unhcr — published eRPIS tables show strong
country-of-asylum variation on the cascade root s3_11 (12-month "Yes":
Egypt 29 / Iraq 4 / Jordan 22 / Lebanon 14) and the round-2-only sentinel
families make `wave` the dominant sentinel predictor → country×wave is the
domain-correct stratum; (b) unicef — country-level attitude/screener
asymmetry (WGM: heard-of-vaccine 44–98% by region) → Country is the
domain-correct stratum; (c) wb — country is recorded for only 38.8% of
rows, so a data-driven selection rule should NOT pick country; expect
employmentStatus / RCT arm / hadJob instead. Caveat honored: sandbox
content is random, so the local run validates the mechanism and the
selection rule's behavior, not these real-data expectations — those are
checked on the leaderboard. Verdict after run: see Decision.

## Change

`src/models/stratum_backoff.py` + `src/eval/split.py` +
`tests/test_stratum_backoff.py` (4 pass). Spec followed:
`trip/tasks/T3-E004-stratum-backoff.md`, with one deviation — stratum
selection is DATA-DRIVEN instead of smallest-cardinality: candidates =
GIVEN items with card ≤ 12; best single by held-out log score (20% of
complete visible rows, seed 0), then best pair containing that single;
κ ∈ {1,3,10,30,100} chosen jointly. Reason: A002 finding 5 (wb country
recorded for only 38.8% of rows) shows the cardinality heuristic picks
wrong on at least one real instrument; held-out selection adapts to the
real data at grading time. Selection runs inside predict().

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | sample | unicef | world_bank | unhcr | mean | Δ vs parent (3-inst) |
|---|---|---|---|---|---|---|
| E002 (parent) | 0.3210 | 0.3232 | 0.2909 | 0.4297 | 0.3412 | — |
| this (auto strat+κ) | 0.4333 | 0.4593 | 0.4105 | 0.5347 | 0.4595 | **+0.1202** |

Sandbox-selected strata (auto, per instrument): sample [urban_rural,
age_band] κ=1 · unicef [Q13, Q05] κ=1 · world_bank
[user.wageOfSimilarEmployees, group] κ=3 · unhcr [s2_3_girls_0_5,
s2_1_hh_relationship_lbl] κ=10. Wall-clock: 0.7/3.9/13.4/82.1 s
(sum ~100 s ≪ 900 s; unhcr dominated by the 17-candidate selection loop).

**unhcr moved for the first time** (+0.105 vs E002/marginal): stratum-
conditioned parent beliefs opened the 155 PREDICT-parent gates — the gate
cascade multiplier is real, as the 08-12 structural conclusion predicted.

Reproduce: `.venv/Scripts/python src/eval/runner.py src/models/stratum_backoff.py`

## Decision

**Adopted.** Δ(3-inst mean, sample excluded) = 0.4682 − 0.3479 = +0.1202 >
+0.005. Domain check verdict: mechanism-level pass — the selection rule
behaves as designed; the specific sandbox strata are artifacts of invented
content (expected, not surprising) and carry no real-data meaning. The
pre-registered real-data expectations (country×wave on unhcr, Country on
unicef, non-country on wb) are checked on the leaderboard, not locally.
NOT submitted alone: hard gate coupling + respondent-specific parents is
unsafe on real unhcr (approximate gates) — ships only together with E003
soft gating (E005).
