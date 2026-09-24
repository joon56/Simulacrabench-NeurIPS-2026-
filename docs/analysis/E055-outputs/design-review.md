# E055 finite coupled-star preregistration review

Date: 2026-09-24. Design-only review before model fitting or scoring.
Reviewed `docs/experiments/E055-coupled-star-replay.md`, A014 plan,
A014 metadata review and aggregate audit, A009/A011 calibration analysis,
`link_sharp.predict`, `supervised_retrieval`, and E053 capture/optimizer.
No code changes, model fits, oracle scores, or channel-acceptance decision.

## Verdict

No mathematical or leakage blocker in the written finite preregistration.
Execution remains conditional on root's final A014 acceptance and implementation
verification. The recommendation is exclusively the existing twelve-point
`LAMBDA_GRID_X` family. The earlier scratch continuous alternative is not part
of this registration or review approval.

## Exact bound and implementation conditions

Each of seven items has two constant original concentration-bucket shares,
each chosen from `{0,.1,.2,.3,.4,.5,.6,.7,.8,.9,.95,.98}`. Freeze all base
products, donors, agreement tables, and original bucket assignments. There are
up to `12^14` assignments, but star topology permits exact factorization:

1. Enumerate at most 144 parent share pairs.
2. For each, render actual parent beliefs and all child pre-own-evidence bases
   using the cached original renderer with child shares zero.
3. For each child/bucket, select the best of twelve raw evidence mixtures under
   official final renormalization and floor. Count every row, including absent
   evidence at that parent's recomputed base and every NA_GATED truth.
4. Sum parent and all six child log-score sums; maximize over parent pairs and
   explicit unchanged E041 endpoint.

For a fixed parent pair, children have no mutual edges, and each child/bucket
parameter affects only its own cells. Therefore its separate maximum can be
summed, giving the exact finite-family maximum. Soft gate agreement and final
normalization do not invalidate this separability. Raw parent beliefs must
propagate unchanged: normalizing or flooring parent first defines another
renderer. Never optimize parent on its own score alone.

Use cell sums or means weighted by actual bucket counts. With n oracle rows,
N=7n and U=(log(2)+6log(3))/7, the comparison is
`delta_skill/3 = (S_oracle-S_identity)/(3*N*U)`. The registered 1e-10 skill/3
margin appropriately leaves threshold-adjacent results unresolved. This is a
finite maximum, not a continuous upper bound; interpolation is outside scope.

## Identity, dormancy and ties

- Assert every original E041 share lies on the frozen grid. Missing item shares
  mean zero. Preserve explicit original complete output, with exact raw capture
  replay parity and selected composed-star parity through the original renderer.
- Original empty evidence layer must remain exact identity. Dormant evidence
  can be materialized only from captured signatures, initial weights, learned
  section selection and fit-only donor labels, as E053 capture_layer does.
  Absent captured state is unavailable evidence, not permission for new fitting.
- Original concentration flag comes from initial nearest-donor posterior even
  where learned section metrics replace evidence. Reassigning buckets from
  learned donor posteriors changes the family. Report returned and materialized
  evidence, natural activity, and both bucket occupancies separately.
- When evidence is absent, changing parent can still change a child. Preserve
  that new child base; do not substitute original E041 final child vector.
- Registered preference for original share, then smaller grid value is sound.
  Implement deterministic complete-assignment ties in fixed schema/bucket
  order; give exact unchanged endpoint priority when total scores tie. Empty
  buckets retain original shares. These choices affect reproducibility and
  changed-vector diagnostics, not the oracle maximum.

## Channel, sample and leakage checks

Public metadata describes four ERACE categories; A014 aggregate audit records
only codes 1,2,3,4. EEDUC observed values are blank or 31..46; EMS values are
blank or 1..6. Their explicit feature MISSING categories preserve observations,
not target answers. Keep the preregistered category rejection checks. Eligibility
uses month-12 TAGE_EHC, whereas GIVEN TAGE is age at interview.

The 12,000-person SHA256 cap is fixed before model scores and independent of
labels. It changes the screened population size but does not select favorable
model outcomes. Use the identical sample in both views, retain string identity
representations, and preserve existing A014-person-v1/A014-household-v1 role
functions; do not repartition after truncation. Person sampling can retain only
part of a sample unit, but every retained member must share its SSUID-view role.
Keep IDs outside model inputs and respondent-level artifacts out of Git.

Each view must fit only its own fit labels, with the complete seven-target
block masked for calibration/oracle/selection/audit roles. All donor references,
agreement fitting and metric selection must obey that boundary. Different views
can assign the same person to different roles; this is permitted overlapping
robustness evaluation, not globally untouched respondents or independent
replications. Do not share fitted products or label-dependent choices across
views. Existing GIVEN-only transductive signature behavior should be disclosed.

Use generic supervised-layer E041 invocation, because its ordinary public
wrapper falls back on non-UNHCR schemas. Freeze captures and provenance before
oracle label access. No selection/audit score access in this stage. Aggregate
A014 counts were already inspected, so no untouched-population claim.

## Interpretation and later learner

The finite family differs from E050's common whole-component transformations
and E053's ungated oracle. It tests coupled existing share choices on an
observed natural star, optionally including dormant evidence. Earlier STOPs
remain scoped and unchanged.

Both registered structural views must pass before a learner. That learner
must use the same grid and constant item/bucket domain, select shares from
separate calibration labels against complete recursive score, and then pass
selection/audit. Any continuous shares, row-wise choices, changed confidence
buckets, donors, agreements or freely tuned base fall outside this bound.
Refits change the frozen library; later protocol must specify refitting and
measure its shift before claiming deployment evidence.

If neither gate routing nor available evidence changes predictions, report
mechanism unexercised. All-diffuse occupancy establishes no concentrated-donor
ceiling. Exact edited SIPP gates do not establish approximate UNHCR behavior.
Passing oracle establishes headroom in this finite observed family only,
not learnability, transfer, a hosted score forecast, or submission readiness.
