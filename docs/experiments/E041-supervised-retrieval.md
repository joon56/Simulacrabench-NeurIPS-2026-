# E041 — Supervised section-specific retrieval
parent: E025
status: rejected
date: 2026-09-18

## Hypothesis

Learning separate GIVEN-agreement metrics for question sections from held-out
answer loss improves neighbour evidence over E025's single unsupervised metric.

## Domain check

Pre-registered before oracle, fitting or scoring in this execution session.

- Technical: the retrieval metric uses query/reference GIVEN only. Query
  answers supply a training loss, never inference features. Query labels and
  every outer validation row are excluded from reference banks and model fits.
  One metric per schema section shares strength across items. A disjoint
  selection split determines whether the candidate is used; an untouched
  audit split estimates the complete selection procedure. Final scoring uses
  the official uniform-mixture floor, including the NA_GATED class.
- Background: the public UNHCR schema describes different response domains
  (housing, employment, protection and return intentions), one adult respondent
  per household/round, and approximate routing. Different relevance of GIVEN
  columns across these domains is plausible but unmeasured. No duplicate,
  co-respondent, panel-recurrence or exact-routing assumption is imposed.
- Loss-map fit: E034 estimates base .79 plus evidence .10. This experiment
  tests whether the observed useful evidence is retrieved with an inadequate
  global metric, not whether a new latent population must exist.
- Oracle first: fixed, query-excluded reference distributions on existing
  observations. Optimize a shared section-level donor mixture or a finite
  section-level donor-policy library, not independent correct donors per cell.
  Report the bound's scope and skill units. Build the estimator only if the
  relevant oracle exceeds +.005 in a three-instrument-equivalent mean.
- Channels: clean official sandbox for correctness/no-regression, existing
  household sim for directional comparison only, and an accessible public
  observed survey/census benchmark for a non-injected external check. The
  latter is not an HSCC score forecast. Record source and access conditions;
  no external rows or fitted labels enter the submission.
- Reading arms: Grand .65+ is a large positive reading, .64 positive candidate
  evidence, .63 unresolved at leaderboard resolution, <=.62 adverse. Inspect
  any best update even at .63. No claim of winning or exact equality from one
  rounded/noised observation. Only UNHCR may change in the submission.

## Change

Planned new files: src/models/supervised_retrieval.py,
tests/test_supervised_retrieval.py, scripts/check_e041.py and a deterministic
E025-based assembly script. Existing models and snapshots remain unchanged.
Implementation is conditional on the pre-estimator oracle result.

## Result

Registration above preceded all measurements. The bounded diagonal metric
was implemented; this is not the larger neural retrieval family in A008.

- Clean UNHCR section-mixture oracle: feasible skill gain +.234499, mean
  equivalent +.078166. Its query-specific optimal mixtures are an optimistic
  information screen, not learnable weights or a forecast.
- Observed UCI Adult census screen: finite donor-policy oracle mean equivalents
  +.030381 / +.029367 on seeds 41 / 42. Actual learned-metric audit gains were
  only +.000594835 / +.000427069 skill over the fixed retrieval comparator;
  both paired 95% intervals include zero. The source, distinct-profile sampling
  limitation, CC BY 4.0 attribution and exact external wrapper are documented
  in `../analysis/A008-outputs/e041-external-source-method.md` and
  `../analysis/A008-outputs/e041-external-learned.md`. This is not HSCC data.
- Clean UNHCR: E025 .562948874, E041 .562462729, delta -.000486145 skill;
  clean UNICEF/WB unchanged at .500648423 / .454717307, every vector equal.
  Three-instrument mean delta -.000162048. Clean no-regression passes.
- Existing household sim, seed 13: E025 .554038343, E041 .552012531,
  delta -.002025811 skill (-.002556072 log score). Directional adoption fails.
- ZIP checker OK; isolated archive official phase-1 scorer PASS x3, source
  probability parity exactly zero x3. Sum of official CPU times 320.605 s
  with two numerical threads. Local timing does not guarantee hosted timing.
- Eleven invariant tests pass. Review corrected metric-fit/replay target
  reuse by adding a fourth partition, the selector's incumbent top10 count,
  and bank-order tie handling. Earlier v1 measurements remain archived.

The section selector still uses a marginal/evidence proxy rather than the
full E025 stack. Its base replay remains in-sample. Separate new-metric replay
does not fix that older limitation. This mismatch is a plausible failure
source, not an experimentally isolated explanation of the loss.

Domain verdict: different section relevance is plausible, but this observed
external screen gives no reliable large gain and the existing household
channel worsens. Do not infer new household structure or a universal matching
ceiling. No external dataset or fitted external weights enter the archive.

## Decision

Rejected for adoption: neither the +.005 mean bar nor the directional-sim
route passes. Preserve code and `output/dev/E041.zip` as a technically checked
research artifact; do not submit it as a qualified improvement. E025 remains
incumbent. No hosted score or daily slot used. Snapshot, preregistered reading
arms and machine-readable verification are in `submissions/2026-09-19-E041/`.
