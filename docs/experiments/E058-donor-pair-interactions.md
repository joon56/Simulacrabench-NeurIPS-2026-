# E058 — Fixed-donor GIVEN pair interactions
parent: E041
status: rejected
date: 2026-09-26

## Contract and novelty

User's supplied S1 protocol is the scope. Input HEAD eaed6a5; A019 entry audit
registered24803a1 and PASS before this E number was allocated. No E058 collision.
Research clock10:06UTC..11:36UTC,90minutes after entry audit; fit wall1200s,
CPU2threads, process-tree aggregate8GiB, one heavy fit, no GPU/paid/install.
No backup. E041 DEV incumbent/E025 fallback; E057 parked after Grand.64/no update.
E056/E057 rerun, relaxed guard, resubmission, S3 and final TEST selection forbidden.

Hypothesis: simultaneous GIVEN matches contain useful donor-ranking information
beyond additive E041 weights within its existing32 candidates. E043/E045 changed
candidate coverage, E055 varied fixed-evidence shares, E057 added content trees.
This changes only second-order matching terms. E041's whole hosted improvement
is not attributed causally to a weight. Its in-sample base replay and marginal
metric objective remain unchanged, not repaired by this experiment.

Background: demographic conjunctions may distinguish useful donor evidence,
but fixed pools can lack complementary labels and15 extra terms can overfit.
SIPP US hospital reasons, editing/imputation, six demographics and exact gates
lack UNHCR geography and approximate routing. No numerical transfer forecast.
Oracle failure, alpha0 selection or nonpositive/inconclusive audit refutes this
registered research continuation on this sample/library, not all private TEST.

## Data and exposure, fixed before response access

A019 key-only reconstruction matches E055 person/group and E056 source/sample
hashes. Historical12000 persons span8908SSUIDs; excluding their entire units
removes24432/39131 eligible persons. Remaining14699persons/8406SSUIDs. Fixed
whole-group hash prefix selects5999persons/3431SSUIDs, no boundary splitting:
oracle1918/1124, selection2007/1130, audit2074/1177. All meet1000/500 minimum.
Exact selection/role namespaces and key hashes: A019 record/entry-audit.json.
No alternate sample/seed. Same source previously loaded/preprocessed and
aggregately audited; new model-score roles are not a new independent dataset.

Fit only original E055 SSUID-group fit5922 in original sample order. All other
E055/E056 labels, including calibration1866 and consumed oracle/selection/audit,
remain closed. New evaluation roles are SSUID-disjoint from all historical
model-use units. Read fit labels via exact SSUID/PNUM-filtered Arrow scan; query
construction reads GIVEN only. Read evaluation responses only for its permitted
stage after prediction freeze; never deserialize old model/score/response caches.
Keys/flags are never model features. Every new query PREDICT block is NaN before
any fitting. Frame order: old fit order, then A019 evaluation SSUID/PNUM order.

## Fixed first stage and candidate

Comparator is actual generic link_sharp.predict + supervised_layer +
hh_cap.CONFIGS. Public small-schema wrapper would fall back and is forbidden.
Original E041 snapshot SHA256
22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073.
At most one fresh first-stage fit: old caches have different frames and are
invalid here. Private function namespaces capture original outputs/arguments
without editing source or changing arithmetic. Cached original gate renderer
reuses first-stage products for beta0 and candidate; no second base fit.

Keep candidate32 identities/order, section groups, original learned first-order
weights and active sections fixed. Keep base, conditional agreement/gates,
deployed evidence-share pairs and original concentration buckets fixed. No
activation of inactive sections or dormant evidence. SIPP schema is original
HOSPITALIZED plus six EHREAS children and six GIVEN; public grouping gives one
section. Capture original metric-fit/reference/selection roles, rather than
introducing a fresh split or using new evaluation labels.

For each originally active section fit all15 pairs j<k, in GIVEN/schema order.
score(q,d)=sum_j w_j e_j + sum_{j<k} beta_jk e_j e_k; e_j is exact GIVEN match.
beta starts allzero, bounds[-2,2], L-BFGS-B maxiter50/ftol1e-7, one start.
Freeze original section retrieval share r and bank+.5 marginal prior m.
Loss=-mean_{metric-fit query,section item} log[.001+(1-K*.001)*
((1-r)*m_truth+r*sum_d softmax(score)_d*1[y_d=y_query])]+.01*sum(beta^2).
Analytic gradient; no share/weight/penalty/iteration grid. Nonfinite optimizer
output is technical STOP; finite maxiter termination retained and disclosed.
No section-specific gain filtering after this fit. Inactive sections unchanged.

Replace only query evidence in active sections. Same existing visible5922 donor
pool and original32 order; labels of all5999 queries absent from metric fitting,
donor pools and every first-stage selector. Recursive rendering propagates any
parent change through the unchanged gate mechanism. beta0 must reproduce raw
E041 endpoint exactly; do not bypass this check by returning baseline directly.

## Frozen evaluation and decisions

Persist full baseline, beta0 and candidate outputs, masked frame, role/source/
code/registration hashes BEFORE reading any new evaluation response. For each
alpha in{0,.25,.5} use (1-alpha)*baseline_raw+alpha*candidate_raw, constant for
all seven items/respondents. alpha0 returns original. Official normalization
then .001 linear uniform floor; pooled seven-head skill with U=mean(logK).
No per-head mixture or oracle optimization beyond these three whole outputs.

Oracle: score three frozen arms once; exact maximum includesalpha0. Delta skill
<=1e-10 stops this library. >1e-10 permits selection as numerical feasibility
only, not improvement/adoption. This does not reopen E055's failed criteria.

Selection: maximize pooled mean log score; ties smaller alpha. For paired
per-person seven-head mean log difference d_i, N persons, G SSUIDs, n_g size,
S_g=sum d_i, m=sum d_i/N:
SE=sqrt((G/(G-1))*sum_g(S_g-n_g*m)^2/N^2). Require G>=2, m>0 and m>2SE for
nonzero; otherwisealpha0, STOP and do not open audit. Freeze policy before audit.

Audit: score baseline and selected policy only, exactly once. Paired row skill
difference=mean7(log p_selected-log p_base)/U. SSUID bootstrap2000 draws,
numpy.default_rng(5801), sample G groups with replacement; use sum of group
differences / sum of group sizes. Linear2.5/97.5 percentiles. Report delta,
interval, changed-vector ratio, frozen section activity and cost. No unused
audit arms or secondary item/asked subgroup search. CI conditions on trained
library/selection; excludes training/selection variability, survey weights and
domain shift. Delta>0 AND lower95%>0 warrants follow-up UNHCR research only;
otherwise stop nonpositive/inconclusive. No S2-ready/TEST claim even if positive.

## Implementation plan and stop controls

Applying writing-plans and test-driven-development; execute sequentially.
- [ ] New scripts/screen_e058.py for interaction objective, private E041 capture,
  exact filtered row loader, staged freeze/oracle/selection/audit and monitors.
- [ ] First write tests/test_e058_interactions.py: analytic/finite-difference
  gradient, beta0 posterior/loss, fixed donors/weights/share, query label isolation,
  inactive identity, mask contract, score/floor, cluster SE and stage ordering.
  Hand-built fixtures only; no real model fits in tests.
- [ ] Commit registration, then tested implementation before first-stage fit.
- [ ] One monitored first stage plus active-section beta fits. Worker timer starts
  before numerical imports; owned process-tree RSS and commitment sampled.2s;
  fit1200s and per-worker remaining wall capped3600s. Watchdog exits owned worker
  on cap/error; parent kills owned tree on wall/memory/monitor failure. At most
  one heavy worker. One-frame first-stage products retained only in this run.
- [ ] Freeze entire prediction library; then each allowed score stage once.
  Persistent opened-role markers prevent repeats. Preserve partial artifacts on
  masking/parity/probability/data/resource failure and stop without repair-fit.
- [ ] Verify frozen arithmetic/hashes without new labels/fits; record scoped
  result/exposure/limits, update status/log/tree, commit only owned work and push
  within existing authorization. No production module, ZIP, method or upload.

All row arrays/keys remain ignored external/e058. Tracked aggregate/source
records under docs/analysis/E058-outputs. Audit scalar/stage markers do not
authorize future relabeling as untouched. No automatic third branch.

## Result

Registration completed before response access (f537a79); immutable original:
[registration.md](../analysis/E058-outputs/registration.md). Tested execution
code8bcdf51. Implementation and one monitored library run completed; evaluation
stages deliberately not run, for the exact identity reason below. No thresholds,
donor pools, activation rules, sample or seeds changed after observation.

A019 PASS:5999 new query persons/3431SSUIDs, disjoint from historical8908SSUIDs.
One generic E041 first stage fit on original5922 fit persons. Its original
learned section selector activated **zero sections**. Inner roles were
metric-fit1184/selection592/reference3554/replay592. The original selector's
gain_log=-.0015416657769860144, SE=.004426562883715935; these are internal fit
diagnostics, NOT new outer selection results. Existing legacy evidence remained
in use; zero learned active sections does not mean zero retrieval evidence.

No beta fit was permitted. Baseline, recomputed beta0 and candidate are exact
across41993 vectors. All three registered global mixtures on the oracle role
are exact after official normalization/floor as well. Label-free certificate: exact arithmetic
oracle delta0; conservative floating gain upper1e-12 < registered1e-10 STOP.
No new oracle, selection or audit response was read; no efficacy score or CI.

**Disclosed label-saving deviation:** instead of opening oracle labels to score
three identical predictions, verify exact identity plus a worst-class bound
using frozen predictions only. Every possible label assignment gives the same
STOP. This replaces the planned oracle scoring operation, not its criterion.
The verification script was added after library observation, uses no new labels
and cannot create a continuation arm. Selection and audit remain unopened.

Focused tests12 PASS (4.30s); frozen verifier checked59 source hashes, data/key/
registration/artifact hashes, full query masking, donor/fit-role isolation,
official floor, identity and resource caps. Real beta0 exercise was inactive;
active interaction objective/evidence path was tested only with small fixtures.
No empirical learned-interaction gain or active-path real-data validation.

Whole library parent/worker run20.267330s, worker19.527362s; conservative fit
12.978182s. Peak aggregate process-tree RSS634986496bytes (.591GiB), commitment
708263936bytes (.660GiB), sampled.2s including monitor harness. One heavy fit,
CPU2, no GPU/install/paid resource. Key audit6.8364s, identity verification.9851s
are separate. These are this local SIPP diagnostic costs, not hosted all3 cost.
All jobs completed within caps. No old model cache reused.

Details, artifact hashes and commands: [closeout](../analysis/E058-outputs/closeout.md),
[exposure ledger](../analysis/E058-outputs/exposure-ledger.md),
[identity certificate](../analysis/E058-outputs/oracle-identity-certificate.json).

## Decision

STOP this registered fixed-active-section family. Technical diagnostic and
inactive identity checks PASS; proxy efficacy unmeasured. No positive UNHCR
research handoff, S2 candidate, release qualification or TEST adoption. E041
incumbent/E025 fallback unchanged; E057 parked, earlier STOPs retained, S3 stopped
and A018 still unconfirmed. No alternate activation policy, split or seed search.
This does not reject pair interactions generally or bound hidden UNHCR/TEST gain.
Resume only under a separately authorized, preregistered design addressing the
inactive-section limitation and preserving this exposure history. No automatic
backup or further experiment. Planned checklist above remains historical;
scored stages were intentionally superseded by the label-free STOP certificate.
