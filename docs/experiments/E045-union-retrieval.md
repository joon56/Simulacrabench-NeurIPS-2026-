# E045 — Preserve-and-expand supervised retrieval candidates
parent: E041
status: parked
date: 2026-09-21

## Hypothesis

Preserving E041's original 32 donors while adding up to 32 learned-metric
donors can recover useful evidence that replacement search discarded, and a
separate selector can reject unhelpful expansions on UNHCR.

## Domain check

Registered before oracle execution and production implementation. Technical:
E043 replacement search failed its marginal oracle gate; its larger union
family had diagnostic headroom. This is a new, explicitly broader family,
not a retrospective relabeling of E043. E044's adverse hosted reading supports
retaining learned weight use. E041 uses the original common metric to shortlist
all sections. Expanding rather than replacing avoids losing its candidate set.

Background: the different UNHCR survey sections cover different needs and
intentions (public schema descriptions; docs/domain.md), so GIVEN attributes
need not rank respondents equally for every target section. This does not
assume household duplicates, recurring panels or exact skip logic. Historical
E025 loss map .79 base + .10 evidence motivates improving evidence coverage;
it neither decomposes E041's .92 nor quantifies E045's opportunity.

Ceiling channel: unchanged observed Adult encoding/deduplication protocol,
new prespecified random splits 43 and 44, 5000 distinct profiles each, donor
bank 2000 / metric fit 1000 / selection 1000 / audit 1000. These reuse the
same source dataset, not independent new data. Audit labels may enter only
oracle scoring. In active E041 sections compare original 32 against the
distinct original 32 + learned 32 union. The oracle has one convex mixture per
query and section over donor one-hots and an honest logistic base, official
floor .001. Inactive sections are identical. Use 2000 iterations and report
certified gaps. Proceed only if (union feasible - original upper)/U/3 > .005
on seed43 and >0 on seed44. This permissive headroom is not learnability.
If this gate fails, park E045 without an estimator and choose a separately
registered fallback; do not silently loosen the gate.

After the gate: retain E041 metric training, activation, partitions and base.
For active sections, fit a second diagonal metric on fixed distinct union
candidates generated with the original and frozen E041 learned metrics.
Use fit labels only, initialize/regularize at the E041 learned weights, retain
its 0..12 bounds, 50 iterations and .001 penalty. Jointly fit the proxy base
share using the existing marginal prior. Compare against E041's K32 learned
metric and fitted share on selection rows: activate the union only for mean
log gain > max(.003, 2 paired respondent standard errors). This selector is
still a marginal proxy, not full-stack validation. No audit-driven tuning.
Inference and replay must use the identical selected candidate construction;
keep the original replay labels and lambda algorithm. Downstream recalibration
is part of the intervention. UNICEF/WB outputs must remain exact E041/E025.

## Change

Planned new model src/models/union_retrieval.py, oracle and observed evaluation
scripts, focused invariant tests, E041-based immutable main.py and ZIP under
submissions/2026-09-21-E045*. Never alter previous models or snapshots.

## Result

Oracle completed before estimator implementation. Certified marginal skill
divided by three: seed43 **+.007834131668**, seed44 **+.009196163696**. Both
preregistered gates pass. Original sections active: family/employment (43),
family/employment/finances (44). All audit-mask invariance checks pass and
inactive sections are exactly identical between oracle arms. Independent
oracle review found no important blocker. These are empirical upper-family
headroom readings on observed Adult, not learned gains or HSCC predictions.
Raw artifacts: ../analysis/E045-outputs/oracle-summary.json and per-seed files.

Actual observed estimator, fixed settings, seed43/44: UNHCR-scale proxy skill
delta **+.000425999541 / +.000495116206**, mean-equivalent +.000142000 /
+.000165039. Paired approximate 95% skill intervals [-.000229188, +.001081187]
and [-.000468785, +.001459017] both include zero. Family and employment unions
were selected on both splits; finance retained E041. Audit-label masking
preserved fitting, selection, base and evidence. The permissive oracle gains
were not realized by this constrained estimator. No post-audit tuning.
Raw files: ../analysis/E045-outputs/observed-summary.json and per-seed files.
Review corrected only the output key name from base_shares to retrieval_shares;
the recorded alphas and all numerical results are unchanged.

Twenty-three tests passed, including union padding/normalization, original
donor preservation, analytic gradient, untouched fallback, selection/audit
label isolation and inherited replay splitting. ZIP checker passes.

| Clean phase 1 | E025 | E041 | E045 | E045 minus E041 |
|---|---:|---:|---:|---:|
| UNICEF | .500648423 | .500648423 | .500648423 | 0 |
| World Bank | .454717307 | .454717307 | .454717307 | 0 |
| UNHCR | .562948874 | .562462729 | .562397862 | -.000064867 |

Every control probability is identical. UNHCR delta versus E025 -.000551012;
mean delta versus E041 -.000021622. Both <=.002 no-regression checks pass.
Union selected on sections 3, 4, 5 and 6 of the clean schema; candidate is not
identical to E041 (UNHCR maximum raw probability difference .264736391).
Source total time 401.921 s with partially concurrent simulation work, not
a hosted guarantee. Frozen reference caches were validated by frame and pinned
snapshot hashes; their timing fields are inherited historical measurements.
Existing household sim seed13: E041 .552012531, E045 .551945260, delta
-.000067271 skill / -.000084879 log, mean equivalent -.000022424. Union
selected sections 2/5; unchanged simulator, no newly injected assumptions and
no tuning after this reading. This direction is not a real-DEV forecast.
Simulation time 364.004 s with concurrent clean/official work. Official archive
phase-1 PASS x3, every raw source/ZIP probability identical. Total local time
395.852 s (rounded components 37.671/93.269/264.913), two numerical threads;
verification wall 406.730 s. Below shared 900 s budget, not a hosted guarantee.
First official run stopped at a relative log-path error in the verifier;
resolved the path before the subprocess and reran all three. Submission unchanged.
Independent oracle and implementation reviews found no important blocker.

## Decision

Parked pending hosted reading; **technically ready as submission #27** under
the user's daily exploration policy. Clean mean delta -.000021622, household
mean equivalent -.000022424 and observed audit mean equivalents +.000142000 /
+.000165039 do not clear the +.005 adoption bar. Neither oracle headroom nor
these small estimator readings warrant adopting E045 or forecasting .65.

All exploratory eligibility requirements passed: <=.002 clean no-regression
against both baselines, exact controls, leakage/scope tests, exact assembly
parity, checker and official x3 schemas within 900 s. Keep E041 incumbent and
E025's validated phase-2 fallback. This is a new evidence-coverage intervention
with measurable candidate headroom, not a daily parameter grid or an E043
replacement-search revival. The positive but inconclusive observed direction
is compatible with the domain hypothesis; the tiny local losses do not verify
transfer. Domain mechanism and magnitude remain unresolved until the slot.

SCORES.md registered >=.65 favourable; .64 with best update inspect/preserve;
.64 without update unresolved; .63 adverse; <=.62 larger adverse; FAILED no
statistical reading. Only UNHCR changes, so Grand deltas translate approximately
x3; never fabricate hidden scores. No upload performed by this preparation.
