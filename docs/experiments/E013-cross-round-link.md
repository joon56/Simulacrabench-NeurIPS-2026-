# E013 — cross-round respondent linkage (runtime-detected, stability-calibrated)
parent: E012
status: adopted
date: 2026-09-02

## Hypothesis

On unhcr, matching a held-out respondent's row to the SAME PERSON's
visible row in the other CATI round (exact GIVEN-signature match,
required unique 1:1) and mixing the twin's observed answer into the
prediction, with a per-item mixing weight equal to the shrunk
cross-round answer-stability rate measured on visible-visible twin
pairs, raises unhcr skill far beyond conditional modelling — because
the real design is a panel (A001), both rounds sit inside one fieldwork
window (A002: answers nearly unchanged), and the 2026-09-02 organizer
ruling explicitly permits within-dataset row matching. Leaderboard
arithmetic says this is the mechanism behind the 0.92 unhcr scores
above us (avg 90% probability on truth is respondent-identity-level
knowledge, not conditioning).

## Domain check

Pre-registered 2026-09-02 BEFORE implementation.

- (a) Technical: record linkage by exact match on a high-cardinality
  stable signature + 1:1 uniqueness requirement keeps the false-match
  rate near zero (a single collision among thousands of signature cells
  is filtered by the uniqueness test). The mixing weight is NOT tuned on
  the leaderboard: visible rows contain BOTH rounds, so visible-visible
  twin pairs give a per-item stability estimate s_i (beta-shrunk to the
  instrument median, α = 20, the E003/E010 estimator family);
  prediction = s_i·(twin one-hot, lightly smoothed) + (1−s_i)·E012.
  Items whose answers genuinely drift between rounds get low s_i
  automatically — calibration by construction.
- (b) Background: eRPIS is a published panel (round 2 = re-contact of
  round-1 respondents within the same May–June 2025 window). Household
  roster variables (children counts by age/sex bands, relationship,
  country) are stable over weeks and jointly high-cardinality — a
  fingerprint. Expected match fraction: round-2 rows nearly all have
  round-1 twins (4,033 of 6,316 re-contacted); overall DEV match
  fraction plausibly 0.6–0.8 ⇒ expected unhcr skill 0.85–0.92 —
  consistent with the observed leader scores.
- (c) Local evidence plan (sandbox rows are INDEPENDENT by
  construction — no twins exist): (1) clean runner must equal E012
  within ±0.002 (the 1:1-unique exact-match detector finds ~nothing on
  independent rows; watch point: report the sandbox match count);
  (2) panel sim — rebuild a sandbox frame where a fraction of round-2
  rows are copies of round-1 rows with a small answer-perturbation
  rate, roles reassigned so twins straddle the visible/held-out
  boundary — must show a large E013-over-E012 gain that grows as the
  perturbation rate falls; (3) the same sim with ZERO copied rows must
  show E013 ≡ E012 (detector fires nothing). Adoption is real-data
  motivated on (1)+(2)+(3), the E003/E010 route, now with an explicit
  organizer ruling on legality (2026-09-02 email, quoted in log.md).
- Risk watch, pre-registered: the announced "<5 gating changes" kit
  update may alter unhcr gate structure — re-run the full harness on
  arrival before the next submission after it lands.

## Change

`src/models/cross_link.py` (planned): E012 + a linkage layer. Signature
= the GIVEN columns minus the wave/round item (identified from the
schema as the GIVEN item whose description/name marks the CATI round;
fallback: the GIVEN column with exactly 2 values covering all rows).
Match visible↔held-out rows across rounds on the exact signature tuple;
accept only 1:1 unique pairs. Stability s_i from visible-visible pairs
per PREDICT item (shrunk, α=20). Prediction for a matched held-out row:
mix the twin's one-hot (floored ε=0.02 toward the model dist) with the
E012 belief at weight s_i; unmatched rows fall through to E012
unchanged. Gate math runs after mixing (parent beliefs sharpen the
cascade too).

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

Clean sandbox — bit-identical to E012 on all four schemas
(0.4429 / 0.5006 / 0.4549 / 0.5629; verified in an isolated sequential
run — a first contended run showed unhcr 0.5623, traced to torch CPU
reduction nondeterminism under CPU contention, not to the layer;
isolated reruns reproduce 0.5629 exactly). Evidence (1) met: on
independent rows the matcher finds 1 spurious twin and 1 visible pair,
and the MIN_PAIRS=30 guard keeps the layer off (evidence (3) folded in).

Implementation evolved during verification (append-only):
- v1 exact-signature matching; clean sandbox showed 1 spurious
  collision → MIN_PAIRS guard added.
- v2 FUZZY matching (accept best cross-round candidate at ≥ n−2
  agreeing signature columns with a 90% relative floor — low-dim
  signatures stay exact — runner-up margin ≥ 2, 1:1 claim resolution):
  real panels drift (a new child moves an age-band column), exact
  matching would silently lose recall. Chunked int-code matcher, ~s.

Panel sims (unhcr sandbox, twins straddling the visible/held-out
boundary, shared ladder; log score):

| sim | E012 | E013 | Δ log |
|---|---|---|---|
| v1: exact copies, 10% answer perturbation (457 twins) | −0.5017 | −0.2724 | **+0.2293** |
| v2: + 30% of twins get one GIVEN column changed (372 twins) | −0.5041 | −0.3038 | **+0.2003** |

≈ +0.16–0.18 skill on matched regimes at U 1.2618. Tests: 4 fast
(matcher unit incl. collision rejection, stability shrinkage, clean
inertness, no-round-col inertness) + panel sim; suite green.

Reproduce: `PYTHONPATH=. .venv/Scripts/python src/eval/runner.py src/models/cross_link.py`
and `.venv/Scripts/python -m pytest tests/test_cross_link.py -q -s`

## Decision

**Adopted (real-data motivated; organizer-ruled legal 2026-09-02).**
Evidence triple met: clean no-regression exact, panel-sim gain large and
robust to GIVEN drift, null behavior guarded twice (MIN_PAIRS +
uniqueness margin). The real-data claims — match fraction 0.6–0.8,
expected unhcr LB ≈ 0.85–0.92 — are tested by the next submission.
Disclosure per FAQ: linkage motivated by public eRPIS panel
documentation; organizer email quoted in log.md. Submission:
`submissions/2026-09-03-E013/`.
