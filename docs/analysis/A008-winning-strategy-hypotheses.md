# A008 - Winning objective: new model hypotheses
date-started: 2026-09-18
status: done
relates-to: A007 / E018 / E023 / E025 / E027 / E030 / E035

## Objective and status

The user prioritizes winning, permits replacing the incumbent method, and
asks how to reach beyond Grand .65. This is a researched proposal, not an
implemented design or a measured forecast. A007's validation findings remain
useful infrastructure; repairing the incumbent is no longer the main research
objective. No E-series ID is assigned to these hypotheses yet.

With controls held at their displayed .52/.49, H=.94 gives mean .6500;
H=.95 gives .6533; H=.96 gives .6567. Rounded Grand .65 alone does not ensure
first place. These are arithmetic targets, not predictions; the displayed
scores have noise and the leaderboard can move. H=.89 to .94 requires .05
skill, about 45% of the remaining .11 loss. For U_H about 1.2618 this is
.0631 mean log probability per cell. Component gains cannot be added without
measuring their interaction.

## Main hypothesis: learn which reference respondents help each question

### Evidence and loss-map fit

E034 puts the E025 base near .79 and the incremental evidence contribution
near .10. Source inspection confirms one learned GIVEN-agreement weight
vector and one candidate posterior are reused across all PREDICT items;
only the final lambda varies by item and concentration bucket. Matching
weights are estimated from provisional feature matches, not optimized for
held-out answer prediction.

Hypothesis: useful neighbours depend on the response domain, and GIVEN
interactions carry information that the global exact-agreement kernel misses.
Age/education may matter differently from household composition or geography
for different questions. These are motivations to test, not established facts
about this file. No household recurrence or duplicate prevalence is assumed.
The method targets conditional prediction using the same available data.

### Proposed method

A compact, supervised retrieval model learns query/reference embeddings from
GIVEN only. Small section-specific projections share statistical strength
across related items while allowing different neighbour weights. Reference
answers are probability values; the query's answers are training targets only.
Optimize the pooled final log score, including NA_GATED as an ordinary output
category. A base-prediction option lets the model abstain from borrowing a
reference answer when none is useful; a peaked relative neighbour score alone
does not establish reliability. Gates can inform the base but cannot impose
exact routing constraints on the approximate real UNHCR gates.

This is a new predictor family. E023 changed K and repeated unsupervised
weight estimation. E030 changed ordinal adjacency credit. E027 fed an
already fixed retrieval aggregate to a network. None trained section-specific
retrieval by the answer-prediction objective. E035's transition oracle on an
injected structure does not bound a different learned neighbour distribution.

TabR supplies primary-source precedent for learning tabular prediction with
retrieved training features and labels, not proof of an HSCC gain:
https://proceedings.iclr.cc/paper_files/paper/2024/hash/4ef594af0d9a519db8fb292452c461fa-Abstract-Conference.html
https://github.com/yandex-research/tabular-dl-tabr

### Ceiling channel before an estimator

On observed, non-injected survey rows, mask the complete PREDICT block on
query respondents and freeze the candidate bank and base predictions. An
optimistic oracle optimizes reference-mixture weights shared across a whole
question section, not an independent correct donor for every cell. Define
the admissible candidate family first; report the oracle only as a bound for
that family and those rows. A large oracle gain is necessary, not evidence
that GIVEN can learn it. Then require gains on separate evaluation rows with
the query labels absent from all fitting, reference banks and early stopping.
Split by respondent, not by individual cells; training/reference inclusion
must also be controlled while learning the supervised retrieval embeddings.

The local sandbox remains a correctness/no-regression channel. It cannot
establish the real-data ceiling. A public real survey is a possible independent
screening channel: UNHCR's Jordan VAF catalog describes household demographics
and multiple vulnerability domains. It is a different survey, so even success
there is external validation, not an HSCC estimate. Catalog located, but the
microdata access endpoint returned an error/403 in this review; no data was
downloaded and access conditions have not been verified:
https://microdata.unhcr.org/index.php/catalog/1030/study-description

Inside the competition container, visible TRAIN supports real, fully masked
respondent validation and ordinary model selection. Those diagnostics cannot
be read outside the enclave; a submission is still needed for the external
DEV transfer reading. Do not describe this as a pre-submission observation.
If no non-injected screening channel can be made operational, the proposed
method remains unqualified under the standing submission rules.

### Practical limits

Use shared embeddings and bounded candidate batches, not 213 independent
retrieval networks. Profile actual fit, calibration and prediction against
the shared 900-second budget before packaging. No runtime or gain is measured
yet. Exact query exclusion is insufficient if validation labels enter other
training queries' reference banks: validation must exclude all such paths.

## Independent challenger: a tabular foundation model for the base

Hypothesis: E025's small shared network misses GIVEN interactions which a
pretrained tabular predictor can model. UNHCR has 8,279 visible TRAIN rows and
17 GIVEN columns. TabPFNv2's published evaluation regime includes datasets
up to 10,000 rows and 500 features, making it a concrete candidate, not proof
of performance here:
https://www.nature.com/articles/s41586-024-08328-6

Begin with schema-selected gate parents and a bounded set of content heads;
score all final descendants rather than the parent head alone. The return-
intention parent has 73 direct children. This targets the .79 base and can
affect the .079 gated residual, which also contains asked-answer errors.
Do not claim that the gated residual is all recoverable by better parents.
Compare fully out-of-sample probabilities, then measure overlap/complementarity
with the incumbent and the retrieval candidate before any composition.

The oracle for a frozen candidate library bounds only its mixture-selection
headroom. It cannot predict how good an unrun foundation model will be;
the pretrained forward pass must first be measured. This differs from building
a new fitted estimator before testing its oracle ceiling.

Official documentation supports offline weights and distinguishes code and
weight licenses. Newer default releases have separate non-commercial weight
terms and access flows; v2 has a different attribution-based license. Pin the
chosen version and verify its exact weights, terms, compatibility and runtime.
Do not assume a default pip install is reproducible. Competition data stays
inside the runner; no hosted inference API is part of this proposal:
https://github.com/PriorLabs/TabPFN

## Work order and decisions

1. Prioritize the supervised retrieval hypothesis; define the constrained
   oracle, secure a lawful non-injected screening dataset, and test whether
   meaningful headroom exists before building its estimator.
2. Screen the independent pretrained base on a small, schema-defined head set
   for feasibility and held-out complementarity. Neither target head choice
   nor reported gain may use hidden DEV labels.
3. Compare learned models on separate respondent splits with final-output
   scoring. Preserve the adoption bar and all A007 packaging checks. Keep
   initial hosted interventions UNHCR-only for attribution.
4. Spend one eligible slot on a qualified candidate; compose only after
   measured evidence. Maintain E025 as a fallback, not a mandatory architecture.

No honest per-method score forecast is available today. .94-.96 UNHCR is a
research target needed to move beyond the recorded leading .93, not a claim
that either proposal will achieve it. Flat or worse remains plausible.
The next deliverable is a go/no-go measurement, not another synthetic story
chosen to make a preferred architecture look successful.

## v2 - User-provided leaderboard screenshot

The subsequent screenshot shows three rows at Grand .65 with
UNICEF/WB/UNHCR .52/.50/.93, three at .52/.49/.93, and two at .52/.49/.92.
Team identities and capture date are not shown. Treat this as a user-supplied
snapshot, not an independently refreshed leaderboard or a controlled A/B.

Relative to our displayed .52/.49/.89, the leading displayed component gap
is .01 WB plus .04 UNHCR. Their Grand contributions are .00333 and .01333;
80% of this arithmetic gap is UNHCR and 20% WB. Rounding/noise means these
are approximate planning figures, not exact causal gains.

Retain supervised retrieval on UNHCR as the main hypothesis. Add WB to local
screening of the independent pretrained tabular base; agreement among earlier
leaders was not a WB Bayes bound. No method or mechanism can be identified
from these displayed scores. Initial hosted tests stay UNHCR-only under the
standing rule; this update does not schedule a mixed-instrument submission.

With UNICEF .52 and WB .50, H .93/.94/.95 gives Grand arithmetic
.6500/.6533/.6567. Thus H .95 with WB .50 is a .66 display scenario, whereas
WB .49 requires H .96 for the same mean. Neither target is a forecast;
even achieving it would not guarantee winning a moving leaderboard.

## v3 - Actual E041 implementation and next-day artifact decision

The user's request to build the next-day artifact authorized implementation.
E041 is the bounded section-specific diagonal agreement metric, not neural
TabR. Its initial donor bank is frozen to 32 candidates per query. Pre-estimator
clean and observed-data oracle screens cleared their scope-specific gates,
but these permissive headroom checks did not establish learnable improvement.

Actual production comparison: clean UNHCR -.000486145 skill, UNICEF and WB
exactly unchanged; existing household sim UNHCR -.002025811. On observed UCI
Adult census profiles, the metric in an honest logistic-base wrapper improved
only +.000594835 / +.000427069 skill over fixed retrieval on seeds 41 / 42,
with both paired 95% intervals including zero. Adult is an accessible external
channel, not humanitarian microdata or an HSCC score estimator. Its protocol
deduplicates coarsened profiles and lacks approximate UNHCR gates. Full
source attribution, split definitions, source hashes and versioned results
are retained in `A008-outputs/e041-external-*`.

Review found and corrected target reuse between metric fitting and lambda
replay, top10 incumbent proxy construction and bank-order ties. The final
implementation retains in-sample incumbent base replay and a marginal-base
section selector; it does not claim to implement the broader honest
final-pipeline calibration design. These limits need materially different
experiments, not a post-hoc assertion that fixing them would yield .65.

E041's self-contained E025-based archive passes ZIP checking, official phase-1
score.py on all three schemas, and exact every-vector source parity. CPU
score time sums to 320.605 seconds. Eleven invariant tests pass. Nevertheless
the experiment is rejected and the archive marked DO NOT SUBMIT because
performance qualification failed. E025 remains incumbent; no slot was spent.

E042 then screened a narrower final-output evidence-blend family with an
oracle before any estimator: one fixed extra share per item over unchanged
E025 donor evidence, no descendant propagation. Existing sim finite-grid
optimum +.004569680 log (+.003621694 UNHCR skill) missed its registered .005
log gate. Parked without fitting or packaging an estimator. This does not
close all out-of-sample calibrators.

The independent pretrained tabular-base proposal remains unimplemented and
unmeasured. It is a separate next research branch, conditional on offline
availability, licensing, runtime and honest validation, not a ready next-day
submission. No measured evidence from this continuation supports a .65
forecast. Actual E041/E042 experiment assignments supersede A007's earlier
provisional names; historical proposals remain unchanged for traceability.

## v4 - User prioritizes using expiring slots for exploratory validation

The subsequent user direction corrects v3's slot decision, not its measurements.
E041 failed local adoption but passed clean no-regression and technical checks.
Its real-data supervised-retrieval transfer remains unmeasured. The unchanged
archive is therefore selected for one exploratory UNHCR-only DEV reading;
E025 remains incumbent until an actual result warrants replacement.

The older broad evidence-off probe is already read, and the independent base
is not ready. E041 offers a new pipeline-level comparison at no additional
implementation risk. It does not promise a detectable effect or isolate the
retrieval metric from its bank/selector/replay changes. An unchanged Grand can
remain inconclusive. Updated preregistered arms in its scorecard determine
the next research action; no repeated fine weight tuning after a flat result.
Archive bytes and performance_qualified=false remain unchanged. No upload
has been performed. A forecast of .65 is still unsupported.

## v5 - E041 hosted result reported: new DEV incumbent

On 2026-09-19 the user reported E041 Grand .64 / UNICEF .52 / World Bank .49 /
UNHCR .92, compared with E025 .63/.52/.49/.89. Displayed Grand gain +.01 and
UNHCR gain +.03, unchanged controls, select the preregistered .64 positive arm.
E041 is retained as the new leaderboard-backed DEV incumbent. This is a
user-reported reading, not a fetched platform record; submission ID, exact
upload time and runtime were not provided. The frozen archive is unchanged.

The original local failure and exploratory decision remain above. The negative
household sim and inconclusive Adult screen did not predict hosted transfer.
This result supports continuing research on the complete retrieval pipeline;
it does not identify a causal gain from learned weights separately from the
bank, selector and replay changes, or establish the exact unnoised effect.
The historical E025 .79+.10 loss map cannot be reused as an E041 decomposition.

Use E041 as the next DEV comparison baseline, preserve E025 as the separately
validated phase-2 fallback, and require scoped oracle/validation for new changes.
E041 phase-2 packaging and matching method documentation are not completed by
this result-recording task. No additional experiment, model edit or upload.

## v6 - E043 screen and E044 conditional weight-use control, 2026-09-20

E043 tested the named bottleneck in E041: common-metric top32 candidates are
only reranked with section metrics. The preregistered observed-data oracle
measured NEW versus OLD pool headroom under identical section-shared simplex
constraints, rather than reusing E041's large total oracle. Certified marginal
skill /3 +.000962822 / -.000392472 failed its primary/replication gates. Parked
without production code. The union of old/new pools is a larger diagnostic
family, not an approved post-hoc switch to a winning oracle family.

The agreed fallback E044 removes learned weight use from evidence conditional
on unchanged E041 activation. Fitting, candidate K32/search, splits and replay
algorithm remain; recalibrated lambda and descendant changes are downstream
effects. This measures one pipeline intervention, not all supervision. Clean
UNHCR -.000168016 vs E041, controls identical; existing household sim +.003090025.
The local adoption bar still fails. E041's earlier sim/DEV direction disagreement
is why this technically validated control is an informational hosted test.

E044 checker and official phase-1 x3 PASS, exact source/archive probability
parity, 371.022 s combined local scoring, 15 invariant tests. Ready as prepared
submission #26 under the user's slot-use preference, no upload performed.
Read its preregistered scorecard before choosing the next intervention. E041
remains DEV incumbent; E025 remains the verified phase-2 fallback.

## v7 - E044 adverse hosted reading; retain learned weight use

The user subsequently reported E044 Grand .63, no best update. All individual
instrument scores are unavailable. Apply the preregistered .63 adverse arm:
reject this configuration for adoption and retain E041 .64/.52/.49/.92.
Displayed Grand delta -.01 gives an approximate UNHCR effect translation of
-.03 because only UNHCR changes, not an observed instrument delta or a hidden
UNHCR score. One rounded/noised reading is near the recorded resolution.

The control supports useful learned weight use conditional on unchanged E041
activation, including downstream lambda and parent effects. It does not prove
that weights alone explain the entire E041 gain or identify a domain mechanism.
The positive household-sim direction did not transfer to displayed DEV.
Retain learned weights for subsequent metric/selector validation; no blind
daily weight-removal grid. E043 remains parked at its scoped oracle gate.
This result supplies no new .65 forecast and no phase-2 validation: E025 stays
the verified phase-2 fallback until E041's checks and method are completed.

## v8 - E045 preserve-and-expand retrieval, 2026-09-21

Today's score-seeking candidate preserves E041 learned weight use after E044's
adverse reading. E043 replaced an original32 candidate pool; E045 explicitly
tests the distinct original32 + learned32 union. Its earlier union observation
was exploratory motivation, not retroactive success for E043. New preregistered
random splits43/44 of the same observed Adult source yield certified marginal
oracle skill/3 +.007834132 / +.009196164, passing the >.005 / >0 gates before
any production estimator. These are candidate headroom, not learnable gains.

E045 fits an expanded diagonal metric only on fit rows, then compares with
the E041 K32 learned metric on separate selection rows. Require section gain
>max(.003, 2 paired respondent standard errors); otherwise preserve E041.
The search metric remains frozen at E041 even after expanded weights are
fitted. Original donors are retained, padding has zero mass, self excluded.
The activation proxy and inherited in-sample base replay remain limitations.
No external records or fitted parameters enter the archive.

Actual observed audit gains +.000426 / +.000495 skill have paired intervals
including zero. Clean UNHCR delta -.000064867 versus E041 / -.000551012 versus
E025, controls exact. Existing household sim delta -.000067271. Neither local
channel qualifies for model adoption. E045 is a named, screened exploration
targeting the established evidence contribution, not a proven .65 model.
No audit-driven parameter tuning; preserve E041 as incumbent pending its slot.
Technical assembly/official verification results are recorded in the E045
experiment and scorecard. E025's phase-2 fallback remains unchanged.

## v9 - E045 reported .64 without update, 2026-09-21

User reported Grand .64 and no best update; individual instrument scores are
unavailable. The preregistered unresolved arm applies: park this configuration,
retain E041 .64/.52/.49/.92. No exact hidden UNHCR value or underlying zero
effect follows from equal rounded/noised Grand. Hosted selector inactivity is
one possibility, not an observed fact; local activation cannot identify it.

E045 did not demonstrate a new best. Observed candidate-union oracle headroom
and weak learned Adult gains were insufficient to establish HSCC improvement.
This is not a universal retrieval ceiling or a reason to remove E041 learned
weights. Avoid a blind daily K/weight grid; prioritize final-output selector
auditing or a separately screened mechanism. No new method or forecast is
validated by this result. E025 remains the separately validated phase-2 fallback.

## v10 - E046 screen stopped; E047 adaptive final correction, 2026-09-22

The next direction was honest final-output selection, keeping E041 learned
retrieval after E044's adverse and E045's unresolved readings. First registered
E046's repaired tree comparison, motivated by A006's contaminated selection
and inconsistent formula. Observed Adult seeds45/46 constant-headwise mixture
oracles gave skill/3 +.000145139 / +.000017564. Seed45 failed the registered
.005 gate. No production tree estimator or E046 submission was built. This
does not validate the old broad real-data ceiling claim.

Registered E047 separately: keep E041 first-stage predictions and donor
evidence, then predict an extra evidence share <=.5 from section-average
confidence/agreement features for each respondent. Apply after final gate
propagation. This differs from E042's constant-per-item family; its permissive
query/section oracle allows variation across respondents. Observed seeds47/48
feasible oracle skill/3 +.008792002 / +.008430994 passed before implementation.
This headroom is not learnability or a forecast. E025's .79 base + .10 evidence
motivates allocation of existing evidence; it does not decompose E041's .92.

Production masks separate correction-fit/selection/audit respondents before
all first-stage fits. Fit one regularized seven-feature logistic share model
per section; select against unchanged E041 at >max(.001,2 respondent SE), then
accept the complete policy only if independent internal audit gain >1SE.
Rejected correction returns exact E041. Final full-data E041 refit can shift
the confidence features; this remains a transfer risk. First-stage E041's
legacy in-sample replay is retained, not silently relabeled as repaired.

Actual observed estimator: seed47 finances selected, audit +.000273604 skill,
descriptive interval [-.000162282,.000709490]; seed48 no section selected,
exact fallback0. The observed audit was also used for oracle family screening,
and the estimator's audit guard selects acceptance. These are exploratory
measurements, not an untouched overall research holdout or a demonstrated
HSCC gain. No settings retuned from these readings. Sixteen functional,
isolation and active-assembly tests passed; technical submission checks are
recorded in E047's experiment and scorecard as they finish. E041 stays DEV
incumbent and E025 stays the validated phase2 fallback. No hosted upload.

Final technical outcome: clean all3 exactly E041, household UNHCR+.002324510
with sections7b/7c active; no adoption threshold met. Checker/official all3/
raw source parity PASS, combined CPU515.180s <900. Actual active-household
assembly parity also0 across180411 cells. E047 is technically ready as #28,
still parked pending the preregistered hosted reading. No automatic phase2
promotion. Historical code and incumbent snapshots remain unchanged.

## v11 - E047 reported .64 without update, 2026-09-22

User reported Grand .64, no best update; individual instrument scores are
unavailable. The preregistered unresolved arm applies: park this configuration,
retain E041 .64/.52/.49/.92. No exact underlying delta, hidden UNHCR value or
hosted correction activation can be recovered from equal rounded/noised Grand.
Clean selection rejected every section and the household diagnostic activated
7b/7c; neither identifies selection on the real hosted TRAIN data.

E047 did not demonstrate a new best. Its positive assumed-structure sim and
permissive query-wise oracle were insufficient to establish transfer; learned
observed gains had already been small/inconclusive. Together with E045's
unresolved reading, this supports avoiding blind continuation of these specific
configurations, not a universal retrieval/calibration ceiling. Preserve E041
learned weights after E044's adverse reading. Require a separately screened
mechanism before another submission, not an audit-driven threshold relaxation.
E025 remains the independently validated phase2 fallback. No new code or upload.
