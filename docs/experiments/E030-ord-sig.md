# E030 — ordinal near-agreement in the matching signature
parent: E025
status: parked
date: 2026-09-13

## Hypothesis

The E021/E022 signature scores exact agreement only. Ordinal signature
columns (unhcr: age band + 8 household roster counts; wb: age and two
pay bands; unicef: age) drift by one level between a respondent and its
near-duplicate (a birth, a departure, a birthday crossing a band, a pay
re-estimate), and a one-level miss on a roster column costs the full
2.5–3 nat exact weight — the true match sinks in the ranking or into the
diffuse λ bucket. Adding a data-estimated adjacency weight v_j =
max(0, log P(adjacent | pair differs on j) − log P(adjacent | random
pair differs on j)) recovers those matches; where near-duplicates
agree exactly or don't exist, v_j → 0 and E030 is E025.

## Domain check

Pre-registered 2026-09-13 BEFORE the scored runs. (a) background: ERPIS
is a panel of the same refugee households re-called in two CATI rounds
(schema treats the rounds as independent cross-sections, but the
households recur); the E018 matches are those recurrences plus
co-respondents. Between rounds household composition changes on the
order of a few percent per age/sex cell (births, departures, ageing
across the 5/17/59 boundaries), and a respondent's own age band moves
for roughly 1 in 10 per year of gap. So real drift exists but is
light. (b) technical ceiling, computed before running: roster counts
concentrate on 0/1/2, so a RANDOM disagreement is already adjacent
~65% of the time — the adjacency weight is bounded by log(1/0.65) ≈
0.4–0.6 nats even when every true-pair disagreement is adjacent. The
lever is real but small by construction: a recovered match gains
~0.5 nats of score, not the 2.5 it lost. (c) local channels: clean
sandbox within ±0.001 of E025; no-drift household sim within ±0.002
(v_j residual from smoothing must not hurt); drift household sim
(roster ±1 with p = 0.15 per column, age +1 with p = 0.10) — the
pre-registered stack bar is > +0.005 log over E025; +0.002–0.005 ⇒
ride-along candidate only; ≤ +0.002 ⇒ park, matching recall is not
where the missing unhcr +0.03 lives.

## Change

`src/models/ord_sig.py`: `ordinal_ranks` (schema-order leading-number
parse, ≥ 3 increasing levels, 'N. label' prefixes excluded),
`estimate_weights_ord` (E021 exact weights + adjacency channel from the
same provisional pairs), `_topk_excl_ord` (adjacency term in the score;
falls back to the exact kernel when all v_j = 0), `ord_sharp_layer`
(E022 layer with those), `predict` = E025 with `layer_fn=ord_sharp_layer`.
`tests/test_ord_sig.py`: parser test, weight-arming tests, no-drift
parity, drift gain; `drift_ordinal` sim helper.

## Result

Attempt log.
- v1: adjacency contrast conditional on non-exact (v = log P(adj |
  differs, pair) − log P(adj | differs, random)). Bounded ≈ 0.4 by
  construction (random disagreements on 0/1/2-concentrated counts are
  adjacent ~65% of the time). Drift sim **+0.0011**, no-drift −0.0000.
- v2 (kept in the module): third Fellegi–Sunter outcome, adjacency
  weighted relative to "other" disagreement, capped at the exact
  weight, ≥ 5 adjacent pairs required. Weights (marginal stand-in
  model): no-drift residual ≤ 0.48 (exact max 4.84); drift roster mean
  0.52, age 0 (the sim resamples person columns uniformly). Drift sim
  **+0.0013**, no-drift **−0.0002**. The provisional pairs (rarity top-1
  with mass ≥ 0.5) are mostly false pairs, so m_oth is diluted and the
  estimated v stays near 0.5 nats.
- Ceiling probe (sim-only, adjacency credit forced to φ·w on every
  ordinal column): φ = 0.5 **+0.0025**, φ = 1.0 **−0.0021** (adjacent ≡
  exact promotes false matches). The drift itself costs E025 0.0091 log
  on this sim; the best any adjacency credit recovers is ~+0.0025.

Scored sims (log score, unhcr, phase 1):

| sim | E025 | E030 v2 Δ | ceiling (φ=0.5) |
|---|---|---|---|
| no-drift household (ρ ∈ [0.2, 0.8]) | −0.5627 | −0.0002 | — |
| drift household (roster ±1 p=0.15, age +1 p=0.10) | −0.5718 | +0.0013 | +0.0025 |

Clean sandbox (runner, phase 1): 0.5006 / 0.4548 / 0.5629 — identical
to E025 (v1 run; v2 differs only where adjacency arms, which the clean
sandbox does not).

## Decision

**Parked; matching-recall axis closed.** Drift sim +0.0013 (v2) against
a measured ceiling of +0.0025 at the oracle credit fraction — both
below the +0.002/+0.005 bars pre-registered above. Domain check
verdict: consistent — the technical ceiling computed beforehand
(adjacency on concentrated count columns is weak evidence) is what the
sim measured, and the estimator gets half of it. The missing unhcr
+0.03 does not live in signature recall. Not a ride-along either: the
no-drift residual weights are harmless (−0.0002) but the gain is not
worth the extra kernel. `tests/test_ord_sig.py::test_drift_e030_beats_e025`
is kept as a strict xfail — the recorded null.
