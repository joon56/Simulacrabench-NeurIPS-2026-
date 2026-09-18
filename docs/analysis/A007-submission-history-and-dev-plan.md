# A007 - Complete submission review and conditional DEV plan
date-started: 2026-09-18
status: done
relates-to: E002-E040 / A005 / A006

## Scope and provenance

Read the complete docs/log.md and all 24 dated submission SCORES.md files;
cross-checked the connected experiment records, current pipeline, E040
snapshot, and public UNHCR schema. Some older scorecards omit the actual
result, which is recorded in log.md instead. This is a review, not a new
training run or submission. Historical results through September 21 come
from the supplied repository; the execution clock says September 18.
Use D+1 for the next working/submission day, not an invented calendar date.

## Submission ledger

H denotes UNHCR. Scores below are reported DEV readings, rounded/noised.
An unavailable H score must not be replaced with the incumbent's H score.
Directories identify snapshots, not necessarily the actual upload date.

| Snapshot | Change | Recorded hosted result | What survives review |
|---|---|---|---|
| E002 | Gate-aware marginal | Grand .43; H .41 | Valid initial pipeline |
| E005 | Soft gates + strata | .53; H .63 | Largest structural gain |
| E006 | Hierarchical backoff | .55; H .66 | Richer GIVEN conditioning helped |
| E008 | Full-GIVEN logistic blend | .58; H .74 | Another substantial base gain |
| E010 | Conditional gate agreement | .59; H .77 | Gate robustness helped |
| E012 | Shared-trunk network | .60; H .78 | Modest additional base gain |
| E013 | Hard cross-round linkage | .60, no gain reported | This matching design did not improve DEV |
| E014 | Soft cross-round linkage | .60, no update | A broader pool remained untested then |
| E017 | Capacity selection | v1 failed; v3 .60, H .79 | Small reading; later composed, not decisive alone |
| E018 | All-visible-row evidence | .63; H .87 | Evidence contributes; relationship type unidentified |
| E019 | Higher lambda + concentration buckets | Initial timeout; later .63, no update | Large duplicate-sim prediction did not transfer visibly |
| E022 | Learned matching weights + E019 | .63; H .88 | Incumbent improved within the same displayed Grand |
| E025 | E022 + E017 capacity | .63; H .89 | Current best; strongest retained composition |
| E026 | Four capacity candidates | .63, no update | No detected improvement from this grid |
| E027 | Concentrated evidence as network input | .63, no update | No detected gain; not a clean UNHCR-only intervention |
| E028 | Parent-value-conditional gate decoder | .63, no update | Injected overlap gain did not transfer visibly |
| E031 | Uncapped replay + three seeds | FAILED, no usable diagnostic | No score; ensemble remains unmeasured on DEV |
| E031b | Uncapped replay alone | .63, no update | Does not test out-of-sample replay |
| E032 | Gated predictions made uniform | Grand .16; H .23 reported | Loss-map probe, not a candidate improvement |
| E033 | Preserve sentinel, uniform asked answers | Grand .55 | H approximately .64-.65; substantial content contribution |
| E034 | Disable evidence on UNHCR | Grand .60 | Base approximately .79, evidence contribution approximately .10 |
| E036 | Same/cross-round lambda buckets | .63, no update | Assumed panel heterogeneity did not transfer visibly |
| E038 | Identifier-derived signature | .63, no update | No detected gain from this extra signature |
| E040 | Trees for 57 ungated heads | .63, no update | Selection defects prevent a general tree-ceiling conclusion |

E032 also has a second-account reading in its historical scorecard. That
account is retired and is not a replication channel for this plan.

## What went wrong after the successful structural steps

1. **A successful component was mistaken for a validated population model.**
   E018's gain does not identify duplicate prevalence, household relationships,
   or per-item copying rates. E019 called its injected duplicate simulation
   validated, predicted H around .89-.91, and then read flat. E028/E036/E038
   repeat the broader lesson: a plausible simulation is not measured DEV gain.
   The schema describes one adult respondent per household per round; gains
   from neighbours alone cannot establish several adults from one household.
2. **Validation and deployment differ.** E040 compares held-out trees against
   a refitted, in-sample network and deploys a different blend formula. E025
   compares self-excluded evidence with an in-sample, pre-gate base. E018
   explicitly acknowledged this bias; its claim that lambda can only err low
   was stronger than established. Confident false matches can exist: a peaked
   matching posterior is not a correctness guarantee.
3. **Null readings were interpreted too broadly.** A005 bounds the synthetic
   generator, not the real survey. E037 rejects its cross-fitted isotonic
   procedure, not all calibration. E031 failed; E031b only tests the cap.
   A displayed .63 does not establish exact equality or a universal ceiling.
   E018/E022/E025 themselves improved H .87/.88/.89 with Grand always .63.
4. **Units and throughput matter.** Simulation log-score deltas are not Grand
   skill deltas: for a UNHCR-only change, delta_Grand = delta_log/(3*U_H).
   Use U_H from the schema, approximately 1.2618. E019's +.0312 log would
   translate to only +.0082 Grand even if it transferred exactly, which it did
   not. More training is not free merely because a GPU exists; E017/E019
   timeouts and E031's failure require measured shared-budget headroom.

## Correction to A006 and implications for trees

E040 directly trains 57 ungated heads. Their parent beliefs can propagate to
155 gated descendants; the public schema gives s3_11_intent_return_12m_lbl
73 direct children. Thus A006 v1's statement that the 156 gated items are
untested was too strong. The +.000892 Grand arithmetic for a +.01 improvement
on 57/213 cells describes a direct-only effect, not the full pipeline.
Selection must score all 213 final item distributions, including descendants.
No claim is made that any reachable descendant actually changed on DEV.

## First candidate: honest evidence calibration over E025

Provisional ID E041; no experiment file or adopted implementation yet.

**Mechanism / loss-map fit:** E034 attributes approximately .10 of H skill to
evidence on top of a .79 base. If the replay overstates the base's performance
or evaluates the wrong gated distribution, its chosen evidence weight can be
wrong. This concerns an observed useful component, not a newly assumed type
of household. It may improve or worsen performance; conservative replay can
currently be protecting against variance and false matches.

**Design:** keep the E025 matcher, candidates, capacity choices, K, lambda
grid, and concentration buckets. Change UNHCR only. Obtain calibration
predictions from models not trained on those rows; remove held-out PREDICT
answers from fitting and candidate pools. Match the deployed gate recursion,
evidence order, and official uniform-mixture floor. Separate fit, weight
selection, and final audit rows; architecture selection belongs inside fit.
Start with one deterministic split, not an unprofiled five-fold ensemble.
Keep near neighbours eligible across splits: deleting all similar households
would evaluate a different task. Exclude the query itself and every withheld
answer. Quantify the smaller calibration pool and refit-to-full-data effects.

The calibration/evaluation distinction follows the standard use of held-out
base predictions for stacking, documented by scikit-learn:
https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.StackingClassifier.html

**Before building the estimator:** freeze equally out-of-sample candidate
distributions on existing held-out data; compute a truth-optimized bound for
the explicitly specified fixed-distribution mixture family. Report its scope
and both log and instrument/Grand skill units. Gate-dependent families need
their own complete-pipeline evaluation; a fixed-parent bound does not bound
every recursive decoder. If the relevant local oracle cannot exceed +.005
three-instrument mean, stop that local estimator branch. Existing household
simulations can check directional behaviour, but cannot establish real gain.
Static row-membership and objective checks are independent correctness
evidence, not a substitute for the adoption threshold.

## Second candidate: a fair tree comparison

Provisional ID E042; develop independently against E025 before composition.

**Mechanism / loss-map fit:** improve the .79 base by allowing a genuinely
held-out competitor to be selected. E040's flat score cannot tell us whether
the unfair comparison rejected a useful tree. No new claim about why leading
teams score .93 is needed.

Use identical training rows for net, ladder and trees; preserve validation
predictions before final refit. Use one blend formula for selection and
deployment, with zero tree weight recovering E025. Retain the 57-head scope
initially to isolate the repair and control CPU cost, but choose weights by
all 213 final predictions, including gate descendants and evidence. Separate
weight-selection rows from evaluation rows. Begin with row-membership,
probability-algebra and fixed-candidate oracle checks, then profile end-to-end.
Do not expand to all 213 tree heads merely because the earlier selector was
wrong. Direct conditional-answer heads would be a separate later experiment.

## D+1 onward: conditional work and submission schedule

| Order | Work | Submission condition |
|---|---|---|
| D+1 | Register E041 Domain check; reproduce mismatches; run scoped oracle; implement only if it clears the bar | Submit E041 only after measured qualification and all packaging checks; otherwise retain the slot |
| Next eligible day | Evaluate E042 independently, with the same oracle-first order | One UNHCR-only A/B if qualified; do not submit merely because the calendar advanced |
| After results | Compare actual arms and interaction checks | Compose only measured useful components; not an automatic third upload |

Every qualifying candidate needs the fixed local adoption rule (or the
already authorized E003 directional-sim route, explicitly labelled), clean
sandbox no-regression within .002 per instrument, source/snapshot parity,
ZIP checker, official score.py for all three schemas, and measured shared
900-second runtime headroom. The E003 route is not permission to report a
simulation gain as evidence of transfer. CPU-side work around 150 local
seconds is a historical warning level, not a hosted timing guarantee.
Register exact arms in SCORES.md before uploading. Unicef and World Bank
retain E025 byte-identical behaviour. No additional public ablation probe is
needed before these correctness questions are resolved.

## Expected score: planning anchor, not a fitted forecast

No new candidate has been trained or scored. Six recent flat A/Bs make
**Grand .63 the conservative planning anchor for either candidate**. There
is no defensible narrow confidence interval or measured success probability.
H .90-.91 / Grand approximately .64 is a success scenario. H around .93 /
Grand approximately .65 is a stretch target, not tomorrow's forecast.

Assuming the displayed control scores .52/.49 were exact and unchanged,
pure arithmetic gives:

| H | Mean before rounding | Approximate displayed Grand |
|---|---|---|
| .89 | .6333 | .63 |
| .90 | .6367 | .64 |
| .91 | .6400 | .64 |
| .92 | .6433 | .64 |
| .93 | .6467 | .65 |

Actual displayed components are rounded/noised, so these are scenario
calculations, not leaderboard predictions. Moving H .89 to .93 requires
recovering .04 of .11 remaining loss, roughly 36%; that is a substantial gain.

Pre-registration arms: .65 is a large positive reading requiring updated
instrument confirmation; .64 is a positive candidate reading, not proof of
the entire mechanism; .63 is unresolved at this resolution, not exact zero;
.62 or below is a negative reading that keeps E025 incumbent. Same-Grand
best updates must be inspected, because E022/E025 demonstrate they can matter.
Do not repeatedly spend slots to chase rounded/noised readings.

## Delivered by this review

Complete ledger, correction to A006, conditional experiment order and honest
score scenarios. No model, submission archive, or historical score changed;
no slot consumed. Phase-2 materials remain the prepared fallback.
