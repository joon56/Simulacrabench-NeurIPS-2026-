# E053 — Uncensored donor evidence with absolute bucket calibration
parent: E041
status: rejected
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

Both registered splits completed, exit0, after A012 phase2 timing finished.
Registration commit a452465 and implementation commit 570738f preceded fits.
The identical preregistration bytes are archived beside each capture; SHA256
08c2f15d49a6934dcc9976834823479ea70c229dd52ffaa4435e567d24d74a5d.
Executed script SHA256
6fcf6a1511ca267616d146a79a193e8bb932f08dccc55e69b7c6e47c2aa194bf.

All values below are Adult oracle skill/3, an arithmetic mean-equivalent scale,
not predicted Grand gains. Each split scores800oracle rows/6400cells only.

| Seed | Legacy five-arm | Returned continuous buckets | Uncensored primary | Certified upper | Gate |
|---|---:|---:|---:|---:|---|
|54|+.000434552631|+.000523121587|+.000523121587|+.000523121587|STOP|
|55|+.000003739795|+.000172892178|+.000172892178|+.000172892178|STOP|

Baseline/oracle Adult skills are .333891613030/.335460977790 and
.346976208156/.347494884689. Fit-and-capture times7.956/7.760s. Both numerical
pooled log gaps are0 at recorded precision; upper/attained skill arithmetic
differs by less than7e-17 due to rounding, far from the .005 decision boundary.
Frozen endpoint raw parity and lambda reconstruction passed before scoring.
Captures, arrays, metadata and registration were persisted before oracle labels
were mapped. Selection/audit were not scored. Known prior-role overlaps are
archived explicitly; these are not untouched public populations.

Both fits naturally returned donor evidence: dormant materialization was NOT
activated. Returned and uncensored results are therefore identical. This run
does not isolate the benefit of recovering suppressed evidence. The sole
learned section was active in each fit; all2400queries had evidence on all
eight heads and were in concentration bucket0 (800oracle rows likewise).
Thus second-bucket freedom was not naturally exercised either. Raw endpoint
and reconstruction maximum errors were0. Changed-vector counts5600/6400 can
include normalization-only changes; they are not counts of substantive gains.
The five-arm
comparison includes lambda1 while the primary stops at.98, so these families
are not strictly nested despite the primary's greater bucket freedom.
Complete bucket optima, diagnostics, evidence availability, donor records and
exposure inventory are in docs/analysis/E053-outputs/. Pre-fit validation:
13focused tests PASS; independent reviewer-authored scalar probe80checks PASS,
max difference1.78e-15 versus independent numerical optimization.

Domain verdict: a small allocation gain on an ungated public proxy is compatible
with A011's optimism diagnostic, but neither proves a deployable repair nor
transfers to household evidence and approximate survey gates. No new simulated
structure or positive subset was used to rescue a failed threshold.

## Decision

Rejected for further estimator work under the registered gate: both certified
proxy bounds are below.005. No learned calibrator, production module or ZIP.
Do not lower the threshold, search more seeds or relabel this family to reopen
it. This is a resource-allocation stop on these ungated proxy channels, not a
bound on nonlinear UNHCR recursion or proof that honest calibration cannot help.
Any future recursive family needs a distinct specification and a valid oracle;
the scalar bound here cannot be reused for coupled parent/descendant changes.
The standing adoption bar remains actual mean skill improvement>.005, with
required no-regression/parity/official/runtime checks. No threshold relaxation.
