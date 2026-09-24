# E050 - Held-out selection of recursive evidence strength
parent: E041
status: parked
date: 2026-09-24

## Hypothesis

Selecting evidence strength on genuinely held-out full recursive predictions
improves allocation of E041's useful donor information compared with its
retained in-sample, full-head replay.

## Domain check

Registered before today's screening runs and estimator implementation.
Historical E025 base .79 + evidence .10 establishes a useful source, and the
.079 gated residual includes content errors; these are not E041's decomposition.
UNHCR ERPIS gates are approximate (CLAUDE.md; docs/domain.md section9), so both
overuse and underuse of donor beliefs may affect descendant answers. Preserve
the existing soft gates and learned donor metric; do not assume new households.

Finite family, fixed now: identity lambda; zero; half legacy lambda;
legacy lambda + .5*(1-legacy lambda); one. Transform both concentration buckets
for each item with captured evidence. Missing lambda defaults to zero. Do not
extract dormant evidence if E041 returned no evidence rows. Identity returns
the exact original vectors. Fully render each arm through unchanged recursive
gates, sharing every fitted product/evidence vector within a frame.

Policy scope: one fixed arm per connected component of PREDICT-to-PREDICT gate
edges; GIVEN parents form fixed boundaries. No query-specific or bucket-specific
arm selection. All predicted heads belong to exactly one component. This makes
component composition of global arm outputs exact, including every descendant.
The exact finite-family oracle chooses each component's best pooled log score;
it is not a bound on arbitrary continuous/query-wise calibration.

Channels: official clean UNHCR and unchanged household seed13 are regression
and directional diagnostics. Observed deduplicated Adult seeds51/52,5000 rows
each, using the ACTUAL E041 stack on a flat schema: first2600 fit, next800
oracle, next800 selection, final800 audit. No invented gates. All2400 query PREDICT blocks
masked before fitting. Existing fixed binning/vocabulary protocol is retained
and disclosed. Full-sample vocabulary emulates public schema; source IDs never
predictors. These overlapping source populations are split replications, not
independent external datasets or untouched research confirmation.

Before an estimator: freeze/hash all candidate vectors and compute the oracle-slice
finite-component oracle skill/3. Require >.005 on both observed splits; if it
fails, stop this estimator. A failed bound closes only this observed family,
not real UNHCR headroom. Also report whole-arm and clean/household bounds.
After gate only: choose arms on selection rows; evaluate once on audit without
retuning. Require gain >max(.001,2 respondent SE) per component, unchanged E041
on rejection. Report the selected policy on audit regardless of its direction;
do not use audit labels to alter arms or thresholds. Oracle rows are separate
from selection and audit. Comparing multiple candidates still makes winner
selection exploratory; no post-selection confirmatory confidence claim.

Production details will be registered before production fitting if qualified.
All controls exact E041, 900s combined runtime, official all3, parity and clean
regression <=.002 against E041/E025 mandatory. No hosted upload by agent.

## Change

Pre-estimator candidate-library tooling only until the oracle gate is read.

## Result

Observed oracle seed51 skill/3 =0; seed52=.0000139017224502304, both below
.005. Both runs completed natively with exit0. Seed51's retained E041 layer
exposed no evidence, making every arm identical. The bound is therefore
uninformative about a survey with useful donor evidence; it still fails the
registered gate for this observed channel. Selection/audit remain unscored.
Frozen libraries, manifests and oracle readings: docs/analysis/E050-outputs/.
Eleven library tests PASS; independent spec/quality review found no blocker.

Pre-execution clarification: the initial3000/1000/1000 outline was changed to
2600/800/800/800 before any library fit or result, explicitly separating oracle
screening from the later learned-policy audit. No outputs existed at this change.

## Decision

Parked at the registered oracle gate. No E050 selector, production model or
ZIP. Do not relax the gate or claim a UNHCR recursive-calibration ceiling.
The distinct E052 fixed structural control is separately registered after
this stop; it does not retroactively make E050 pass.
