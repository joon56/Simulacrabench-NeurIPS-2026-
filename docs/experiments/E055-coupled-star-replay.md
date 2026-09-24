# E055 — Coupled star replay oracle on observed SIPP
parent: E041
status: rejected
date: 2026-09-24

## Hypothesis

Jointly selecting E041's existing evidence shares against complete recursive
predictions has recoverable held-out loss that independent full-head replay
misses on a naturally gated observed parent-child block.

## Domain check

Registered before model fitting or scoring; execution requires A014 final PASS.
Historical E025 UNHCR .79 base+.10 evidence demonstrates a useful information
source; .079 gated residual includes asked content. Neither is E041's loss map
or a quantified gain opportunity. A011 measured replay/deployment mismatch,
not causation of the plateau. E053's ungated Adult oracle STOP does not include
natural parent propagation. This experiment retains the E041 donor recipe and
changes only the parameter-family objective used for an oracle screen.

SIPP2023 hospital reasons are person-level, conditional on hospitalization;
public status flags independently identify not-in-universe blanks. A014 checks
show exact edited gates here, unlike approximate UNHCR gates. US health versus
refugee survey, editing/imputation, rare hospitalization and demographic-only
signatures limit transfer. The oracle cannot estimate the hidden survey ceiling.
Source: official Census2023 dictionary, hospital block, linked in A014 review.

## Frozen channel and roles

- A014 approved eligible month12 extract only, retained imputed responses.
  Pick the first12000 persons sorted by SHA256 of the UTF-8 NUL-separated
  namespace E055-sample-v1, SSUID, PNUM. Same sample for both robustness views.
  This resource cap and order are fixed before any model score; not selection
  on hospitalization, answers, model activity or gains.
- Preserve A014 role function and namespaces for respondent and SSUID-group
  views separately. Views overlap and are not independent replications.
  Only fit roles expose PREDICT labels to base/donor/metric/agreement fitting.
  Whole target blocks masked for calibration/oracle/selection/audit roles.
  Only oracle labels scored in this stage; all others remain unscored.
- GIVEN: TAGE strings0..90; ESEX1/2; ERACE1..4; EORIGIN1/2;
  EEDUC31..46 plus MISSING; EMS1..6 plus MISSING. Explicit blank categories
  retain age-related feature universes. No IDs, flags, hospital variables or
  target summaries are model inputs. Reject unexpected categories.
- PREDICT parent HOSPITALIZED is THOSPNIT0 versus>=1. Six original EHREAS_*
  children have values1/2 and NA_GATED only for observed blank with AHREASON0.
  Parent precedes children; every child gate is parent=1. No invented answers,
  no one-hot mutual exclusion across reason indicators. Exact duration discarded.

## Oracle family and proof scope

Use generic link_sharp.predict with supervised_retrieval.supervised_layer and
hh_cap.CONFIGS, not the public wrapper that falls back on non-UNHCR schemas.
Freeze all first-stage products, donor choices, agreement tables and original
concentration flags. Capture/materialize dormant evidence using E053's existing
capture_layer without refitting or adding donors; unavailable evidence stays
unavailable. Record natural activity and bucket counts, no forced concentration.

Each of7 items and2 original concentration buckets chooses from the unchanged
LAMBDA_GRID_X={0,.1,.2,.3,.4,.5,.6,.7,.8,.9,.95,.98}. Exact finite family, not
continuous or respondent-specific calibration. Explicit unchanged E041 endpoint
must be present; assert original shares lie on this grid.

Enumerate at most144 parent pairs. For each, run the cached original renderer
with zero child shares; parent raw beliefs propagate through the actual soft
gate mixture. Optimize each child/bucket independently across the same12 raw
mixtures with actual official normalization/floor .001, including rows lacking
evidence at their unchanged-for-that-parent base. Sum parent and all six child
log scores and choose the best entire star. Children have no edges between them,
so this factorization is the exact maximum over the finite Cartesian family.
Do not normalize parent beliefs before propagation or optimize parent alone.
Exact ties prefer the explicit original endpoint, then share assignments in
schema item/bucket order with original share first and remaining values ascending.

Predictions/capture/provenance must be saved before opening oracle labels.
Verify unchanged raw endpoint and selected composed star via original renderer;
all probability vectors finite/nonnegative with positive mass. Score-margin
tolerance1e-10 skill/3 makes threshold-adjacent results unresolved. No interpolated
renderer substitution without separate parity/proof review before execution.

## Fixed decision

Both views must have oracle delta_skill/3 > .005+1e-10. Either at or below
.005-1e-10 stops this finite observed-family study; boundary unresolved.
Report parent gain and child total, activity and both bucket occupancies.
All calibration/selection/audit score access prohibited until oracle gate passes.
This is not a Grand forecast or evidence the oracle choices are learnable.

If PASS, a learner must stay in this same finite constant-item/bucket family,
choose weights from separate calibration labels with the full recursive
objective, then pass selection and untouched model-score audit before packaging.
That later protocol must freeze refitting and runtime behavior before fitting.
If STOP, no estimator, source model or submission ZIP. No threshold/grid/sample
revision after scores. E041 remains incumbent; E054 stays parked and unsubmitted.

## Result

Protocol committed in 2a52f18; title delimiter corrected for tree rendering and
reviewed implementation committed in df10864 before either fit. Original run
registration bytes retained separately for each view. A014 accepted the source;
10 focused adapter/oracle/audit tests passed. No production model changed.

| View | Fit / oracle rows | E041 proxy skill | Oracle skill | Delta skill / 3 | Gate |
| --- | ---: | ---: | ---: | ---: | --- |
| Person | 5939 / 1850 | .674532609 | .674871988 | +.000113126178 | STOP |
| SSUID group | 5922 / 1872 | .668734959 | .669042129 | +.000102390016 | STOP |

Both gains fall far below the fixed +.005 threshold. Uniform reference
U=1.0406887018; complete seven-head pooled log score used. Parent log-sum gain
is .267721231 / .538372580; six-child total is 4.306055682 / 3.650562130.
Group EHREAS_BIR loses 1.880009362 while the joint star improves; selecting
parents independently would not represent this objective.

Oracle diffuse/concentrated counts are 1845/5 and 1355/517. Every oracle row
has evidence for all seven heads; both first-stage fits returned legacy evidence
without dormant materialization. Original and selected active counts are in
the JSON artifacts. Root endpoint changes alter every child's predictions,
so the natural recursive path was exercised. The group view also exercises
both concentration buckets substantially; this is not an all-diffuse fallback.

All 144 parent scenarios per view were saved before oracle labels were scored.
Original raw endpoint equality and selected composition/renderer parity are
exact. Library fit plus scenario generation took 138.754s / 141.474s locally;
these are diagnostic timings, not submission runtime. Frozen-artifact review
independently recomputes the finite optimum, verifies source/data/registration
hashes, whole-block masks, roles and fit-only donors without model refits.
Calibration, selection and audit scores remain unopened.

Domain verdict: small gains are compatible with weak additional retrieval
information from these demographic inputs and edited exact gates; that is an
interpretation, not a causal explanation or a claim about refugee responses.
SIPP domain, imputation, one-star topology and overlapping robustness views
limit transfer. This finite sample/family maximum does not bound continuous,
respondent-specific, refitted-donor or hidden-UNHCR policies.

## Decision

REJECT this registered finite observed-family study. Do not train its proposed
calibrator, expand the grid/sample, lower the threshold or package a ZIP after
the STOP. A011's descriptive mismatch still exists, but this oracle supplies
no adequate measured headroom for the proposed repair. No hosted score forecast.
E041 remains incumbent; E054 remains parked and unsubmitted. A new experiment
needs a distinct mechanism and a valid pre-implementation ceiling channel.
