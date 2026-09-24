# E053 — Uncensored donor evidence with absolute bucket calibration
parent: E041
status: parked
date: 2026-09-24

## Hypothesis

Exposing the unchanged donor recipe when legacy replay suppresses every weight,
then calibrating independent absolute item/bucket weights on honest deployment
predictions, has useful capacity beyond E041's retained in-sample replay.

## Domain check

Registered before implementation, fits or oracle labels are scored. Historical
E025 base .79 + evidence .10 motivates studying their allocation; the .079
gated residual includes asked-answer errors. These numbers do not decompose
E041. A011 measured membership-associated optimism, not recoverable gain.
ERPIS households and approximate gates can make nearby respondents useful or
misleading (CLAUDE.md; docs/domain.md section9). Neither more evidence nor new
household assumptions are prescribed. Preserve original learned metrics,
donor pool, tie-breaking, gate agreement and concentration flags.

Distinction from E050: that experiment used five transformations shared across
both buckets and each gate component, and explicitly prohibited materializing
query evidence if legacy replay returned none. E053 executes the SAME fitted
query-donor recipe in that dormant case and allows independent absolute
item/bucket weights. This is a broader allocation family, not a new donor
model. Continuous optimization alone would not justify reopening E050.
E050/E051 remain stopped. E052 changed routing, not this replay mechanism.

## Fixed channel, partitions and disclosure

Cached public UCI Adult, existing adapter/binning/deduplication/public vocabulary,
5000rows per seed54 and55.2600fit/800oracle/800selection/800audit in sample order.
Whole2400 outer query PREDICT blocks hidden before every first-stage fit,
retrieval metric selection, replay and donor construction. Source IDs are
provenance only. Assert no gates: this exact oracle is an UNGATED proxy only.

Samples overlap prior Adult work and one another; new seeds are not untouched
populations. Archive role intersections against E050 seeds51/52 and A011 seed53,
and between54/55. This is a known-manifest exposure inventory, not an exhaustive
claim about all earlier work. Selection/audit remain unscored in this study;
they are not called globally untouched confirmation. Do not alter samples or
roles based on overlap/results. No new data download or fabricated gates.

## Fixed candidate family and oracle

Fit the actual generic E041 renderer once per split, with query blocks masked.
Capture full-head base B, original final F, original lambdas, section selection,
initial/learned metrics and original returned evidence. When all lambdas are
zero, execute the original query recipe with its already fitted state; do not
refit, force positive replay weights, change donors or fabricate distributions.
If code/signatures cannot produce evidence, retain unchanged output.
Concentration uses the original initial-metric posterior even where a learned
section replaces donor evidence. Every query donor belongs to2600fit.

For each item and original concentration bucket, one absolute weight in[0,.98]:
P(lambda)=(1-lambda)*B+lambda*E. Validate finite nonnegative unit-sum endpoints
to2e-6; normalize endpoints exactly for the declared optimization. Check that
original lambda reconstructs original raw F to1e-12 before scoring. Include
the original output as an explicit option in each bucket, covering floating
point normalization differences. Missing/zero evidence retains original F.
All nonempty oracle buckets may be optimized; no learned policy is fit here.

For normalized endpoints and official floor f=.001, realized probability is
q(lambda)=f+(1-K*f)*(B_y+lambda*(E_y-B_y)). Mean log q is concave; its derivative
is mean(d/q). Endpoint checks plus bisection locate the optimum. A supporting
tangent gives the numerical upper bound: g(x)+max(g'(x)*(0-x),g'(x)*(.98-x)).
Require pooled log optimality gap<=1e-9. Compare this certified bound with
frozen original F using official normalization/flooring and schema U.

Save full captures, arrays, frame/source/partition hashes BEFORE oracle scoring.
Score800oracle only. Sole primary gate: uncensored continuous-bucket oracle
delta_skill/3 >.005 on BOTH seeds, using certified upper bound for stopping
and attained bound for passing. If a numerical interval straddles threshold,
resolve numerical precision without changing family; do not build an estimator.
Always execute both registered splits even if the first fails.

Fixed same-fit descriptive ablations, never alternative gates: (a) original
E050 five-arm component oracle on only returned evidence, (b) continuous
item/bucket oracle on only returned evidence, (c) primary uncensored family.
Report evidence availability, changed vectors, selected-section diagnostics,
all bucket optima and all three bounds regardless of direction.

The separable proof applies only to ungated Adult. On UNHCR, changing a parent
weight changes descendant bases; this oracle is not a recursive upper bound.
An Adult failure is the registered resource-allocation stop, not proof that
honest survey calibration cannot help. No favorable new simulator is added.

## Change and verification

New scripts/screen_e053.py and tests/test_e053_oracle.py only; no src changes.
Test dormant/nonempty capture and no refits, donor membership, full-block
masking, exact baseline endpoint, buckets/option order, analytic optimum and
tangent certificate versus dense numerical reference, absence behavior,
pre-score freeze and existing-output refusal. Freeze script hash before runs.
Use2threads; wait for A012 phase2 timing to finish before any full fits.

## Result

Not run at registration. No expected score or positive-transfer claim.

## Decision

Parked pending primary oracle. A failed split stops this candidate before a
learned calibrator, production module or ZIP. Passing both authorizes only a
separately specified learned calibration/selection/audit study and a valid
gated-family assessment; it does not authorize adoption or final submission.
The standing adoption bar remains actual mean skill improvement>.005, with
required no-regression/parity/official/runtime checks. No threshold relaxation.
