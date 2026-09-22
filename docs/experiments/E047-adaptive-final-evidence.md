# E047 — Query-adaptive final evidence with honest selection
parent: E041
status: parked
date: 2026-09-22

## Hypothesis

An out-of-sample confidence model can identify respondents for whom extra
E041 donor evidence improves the final distribution, without changing donor
metrics, and a separate selector/audit can reject unhelpful corrections.

## Domain check

Registered before the oracle or estimator. E046 failed its tree-mixture gate
and remains parked. This is a different mechanism. E042 bounded an item-wise
constant extra-evidence blend on one injected household simulation, not an
adaptive per-respondent policy on observed data. Survey sections describe
distinct intentions, needs and circumstances (public UNHCR schema descriptions,
docs/domain.md); GIVEN-neighbor relevance can vary across respondents. No
new household-copy assumption is introduced. Final model/evidence agreement
and confidence are observable without the query's answers.

Historical E025 .79 base + .10 evidence motivates improving the allocation of
existing evidence, not claiming a new decomposition of E041's .92. Keep
E041 unchanged as the first-stage prediction and donor-evidence generator.
Only UNHCR changes. The correction is AFTER the whole gate/evidence pipeline;
there is no new gate propagation after this explicitly final mixture.

Ceiling channel: observed Adult protocol, fixed new seeds47/48, 6000 distinct
modeled profiles: bank2000 / metric fit1000 / metric selection800 / correction
fit1000 / correction selection600 / audit600. E041 fit_sections uses only the
first three partitions; logistic base fits those same 3800 visible rows.
E041 learned metrics/activation determine donor evidence from bank2000.
Choose the initial section-shared base/evidence mixture on metric selection
only using the existing ALPHAS=(0,.1,.25,.5,.75,1). This is an E041-like proxy,
not the full HSCC gate pipeline. Audit the family (1-a)*initial + a*evidence,
one a per query and section, a in [0,.5]. Evaluate feasible choices {0,.25,.5}
using audit labels. This permissive oracle allows query-adaptive decisions;
it is not a bound for constant coefficients and does not establish learnability.
Proceed only if its feasible oracle skill/3 gain >.005 on seed47 and >0 on
seed48. A positive feasible gain certifies at least that much family headroom.
If it fails, stop this estimator; do not relax settings after seeing results.

After a passing oracle, correction share a=.5*sigmoid(beta dot features), one
model per schema section. Features: intercept; section means of normalized
entropy of final E041 and donor probabilities, each maximum probability,
their probability overlap (dot product), and argmax agreement. Standardize
nonconstant features on correction-fit rows only (std floor .001). Optimize
the official final-mixture log loss plus .01*mean(beta[1:]**2), L-BFGS-B50,
coefficients bounded [-6,6], initial intercept -2 and other coefficients0.
Use correction-fit labels only. Select each section against unmodified E041
on correction-selection: mean paired respondent log gain >max(.001,2SE).
The untouched audit accepts the complete selected policy only if overall
gain >max(0,1SE), otherwise exact E041. No audit retuning. Guarded audit is
acceptance, not a second unbiased estimate; report pre-guard audit too.

Production outer shuffle seed4701, correction fit1000 / selection600 / audit400
(each capped at visible_count/10 on smaller inputs); remove their PREDICT
answers before all first-stage fits. Final E041 refit uses all visible rows;
freeze the selected correction model/scaling. Small inputs below4000 visible
rows retain E041. No correction without evidence. Controls stay bit-identical.
Selection-to-refit distribution shift remains a limitation, checked locally.

## Change

Added src/models/adaptive_final_evidence.py, its objective/isolation/integration
tests, active assembly tests, deterministic scripts/assemble_e047.py, and
scripts/evaluate_e047_observed.py. Preserved every historical source module
and snapshot. ZIP contains main.py only; no external records or fitted assets.

## Result

Observed oracle PASS before estimator implementation: seed47 feasible gain
+.039922327789 log, +.026376005841 skill, +.008792001947 skill/3; seed48
+.038283081171 log, +.025292983363 skill, +.008430994454 skill/3. Each query
uses one share per section, with no per-cell choice. Independent review found
no important blocker; partition/masking assertions and declared hashes passed.
Report: docs/analysis/A008-outputs/e047-final-evidence-oracle.json.

Learned observed correction: seed47 selected finances only, pre-guard audit
gain +.000414123061 log (respondent SE .000336607537), accepted by the fixed
1SE guard. Skill +.000273604093; descriptive interval [-.000162282068,
+.000709490254] includes zero. Seed48 selected no section, exact fallback0.
No settings revised after audit. The same audit labels previously screened
the family oracle, so this is not a wholly untouched research holdout; the
guard also uses audit for acceptance. These are exploratory readings, not a
validated HSCC gain. Production's internal audit remains isolated from fit
and selection labels.

Sixteen objective/leakage/fallback/active-assembly tests passed (4.64s).
Clean skill .500648423071/.454717307363/.562462728858, all probability vectors
exactly E041. UNHCR delta vs E025 -.000486144847, within .002 tolerance.
All eight clean section corrections rejected; this is no-regression evidence,
not improvement. Source time491.1342037s, with a concurrent household run.

Existing household seed13: UNHCR .554337041587 vs E041 .552012531240,
delta+.002324510347 (mean equivalent+.000774836782). Sections7b/7c selected;
internal audit +.000697325768 log, SE .000517350491, accepted. This channel
injects household structure and is directional only; it does not establish
real-data gain or pass the +.005 mean adoption threshold. Source529.7275s.
Raw results are in docs/analysis/E047-outputs/.

ZIP checker and official phase1 all3 PASS, with every source/archive vector
exactly equal. Official seconds36.547247410/92.483175039/386.149091244,
total515.179513693 <900; verification wall526.7669924s. Windows11,
torch2.13.0+cpu, CUDA unavailable,2 threads. A concurrent diagnostic ran during
part of verification; these local timings do not guarantee hosted runtime.
Verification manifest binds archive/source/input hashes and raw parity.

Actual active-household assembly PASS too: .554337041587, max probability
difference0 across180411 cells,529.2693297s. This complements the two active
unit/assembly fixtures and official clean fallback path. Dedicated report:
docs/analysis/E047-outputs/active-assembly-parity.json.

## Decision

**Hosted result, user-reported 2026-09-22: Grand .64, no best update.** Individual
instrument scores unavailable; no submission ID, upload timestamp or hosted
runtime supplied. Apply the preregistered .64-without-update arm.

PARKED after submission #28 at submissions/2026-09-22-E047.zip: no demonstrated
best improvement, not locally or hosted adopted. Clean mean delta0 vs
E041, directional sim mean equivalent+.000774837 below+.005. All mandatory
technical gates and active-path parity pass. Observed learned benefit remains
small/inconclusive; do not turn oracle headroom into a forecast. E041 stays
DEV incumbent, E025 stays the validated phase2 fallback. Rounded/noised equality
does not establish zero effect, hidden UNHCR .92 or inactive hosted selection.
Clean fallback and sim activation do not reveal hosted behavior. The positive
sim direction did not establish a best improvement; this is not a universal
calibration ceiling. No blind coefficient/threshold grid; require a separately
screened mechanism for further work. Preserve the archive and all local readings.
