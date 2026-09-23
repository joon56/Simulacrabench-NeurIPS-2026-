# A009 - Why the post-E041 submissions have not improved DEV
date-started: 2026-09-24
status: done
relates-to: A006 / A008 / E041 / E044 / E045 / E047 / E049

## Scope and current decision

User reported E049 Grand .64 without a best update. Individual instrument
scores, hosted activation, submission ID, upload time and runtime are unknown.
Apply its preregistered unresolved arm: park this configuration, keep E041
.64/.52/.49/.92 and E025 as the separately validated phase2 fallback.
This is a completed scored submission, not a failed attempt. No new model,
oracle run, submission archive or competition upload in this review.

## Evidence ledger

| Experiment | Actual learned observed-data gain (skill) | Local behavior | Hosted reading |
| --- | --- | --- | --- |
| E045 | +.000426 / +.000495; intervals include zero | Clean UNHCR -.000065 vs E041; household -.000067 | .64, no update |
| E047 | +.000273604 / 0; inconclusive | Clean exact E041; household +.002325, injected structure | .64, no update |
| E049 | +.001739413 / 0; inconclusive | Clean and household exact E041; all four policies reject | .64, no update |

Observed-data numbers are exploratory Adult surrogate readings, not HSCC
instrument gains or calibrated forecasts. They cannot be ranked across
different splits and target scopes as if measured on a common test set.
Equal displayed Grand does not identify a zero underlying effect or inactive
hosted selection. E044's .63 adverse reading supports preserving learned
weight use, conditional on that intervention, not every E041 design choice.

## Likely bottlenecks and what is actually known

1. The oracle-to-learner gap is observed. E049's continuous oracle skill/3
   was +.008301/+.007549; actual learned equivalents were +.000580/0. A
   respondent-wise truth oracle can choose when a weak model happens to be
   right. Available GIVEN/confidence features may not predict those choices.
   Passing that bound supports a possibility; it is weak evidence of a
   learnable gain. The recent packaging effort exceeded the strength of the
   efficacy evidence. Earlier exploratory authorization did not change that.
2. The validation channel does not establish humanitarian-survey transfer.
   Adult is observed data, but its fields, targets and missingness mechanism
   differ from HSCC. The sandbox's exact gates and synthetic marginals differ
   too. E041 won despite unfavorable local evidence. These channels are
   useful for correctness and screening; they do not rank hosted candidates
   reliably. A failed Adult bound cannot establish a universal HSCC ceiling.
3. The recent policies can produce little or no change. This is confirmed
   locally for E047/E049, not on hosted data. Selection protects against weak
   candidates; automatically lowering the guard would not create signal.
   E049 is specifically original V2,512 reference rows,four parent heads and
   a bounded guarded blend, not a broad test of tabular foundation models.
   Its descendant reach is wider than four output cells, but new content
   heads for all descendants were not trained.
4. A006's inner replay concern remains in source. supervised_retrieval.py
   evaluates model_dists on replay rows included in the base refit, and
   chooses lambda against full-head distributions. link_sharp.py deploys
   evidence inside the gate recursion after mixing conditional and soft
   full-head distributions. Objective/floor differences also remain.
   E047/E049 honestly mask their OUTER rows but preserve this INNER replay.
   This is not DEV-label leakage, and its effect on hosted skill is unknown.
   Conservative bias may be protective. No claim that repairing it must win.
5. Three equal rounded/noised scores have poor diagnostic resolution. They
   provide no demonstrated best improvement; they cannot distinguish weak
   transfer, inactive guards or small positive/negative effects. A new model
   name does not guarantee a sufficiently large prediction intervention.

## Recommended next research order (proposed, not an executed experiment)

### First: evaluate the original evidence calibration inside the renderer

Mechanism: the useful E041 learned donor evidence may be misallocated because
its inner calibration compares in-sample base predictions and a different
distribution from the one scored. Preserve its donor metric, candidate set
and base architecture; change the calibration evidence/objective only in a
separately registered experiment. This is the known A006 hypothesis, not a
newly discovered signal or a continuation of E047's final-output correction.

Loss-map fit: historical E025 .79 base + .10 evidence demonstrates a useful
information source whose allocation matters. Its .079 gated residual includes
asked-answer errors, so parent propagation must be scored. These numbers do
not decompose E041's .92 and do not quantify recoverable headroom.

Before building a new estimator, preregister a small, explicit family of
complete recursive predictions with equally held-out base and donor labels.
Use the actual final scoring floor. Compute an oracle for THAT family on
frozen predictions; include the unchanged E041 endpoint. A finite-arm maximum
bounds only those arms, not arbitrary per-row policies or recursive weights.
Do not use E042's fixed-parent postblend bound to close this distinct family.
Require the existing >.005 three-instrument-equivalent oracle gate on the
declared screening channel; if it fails, stop that scoped estimator. The real
HSCC ceiling cannot be measured externally before submission.

If the family passes, learn calibration from out-of-fold predictions, assess
it on untouched outer respondents, and render the exact deployment recursion.
Keep every hidden respondent's whole PREDICT block out of all fits and donor
labels. Freeze weights before refitting and measure the resulting distribution
shift. Start with a profiled split, not an unbudgeted multi-fold ensemble.
Hosted visible TRAIN supports this ordinary internal validation, but detailed
diagnostics stay inside the evaluation environment. Local diagnostics must
show policy acceptance, fraction of changed vectors, effect size by section,
and held-out gain separately. Do not export statistics through coded scores.

Expected benefit is unmeasured. Added validation consumes the same900s budget;
the repair can increase variance or reduce useful conservative shrinkage.

### Second: strengthen the independent-model evidence before packaging again

Use a fixed, documented observed survey benchmark with GIVEN-only inputs,
whole-target-block masking, and untouched evaluation rows where available.
Check provenance, access permissions, schema compatibility and license before
using any new data. Do not acquire the competition's restricted raw surveys.
Survey resemblance is still not proof of transfer. Keep Adult as a secondary
engineering channel, and do not switch benchmarks after seeing failed audits.

Compare a bounded independent content predictor with E041 under identical
out-of-fold evaluation; require actual reproducible learned gain, not merely
a permissive oracle. Specify the changed family before choosing architecture,
reference size or model version. E049 does not justify blind PFN upgrades,
larger reference grids, unconditional replacement or relaxed guards.
Loss-map fit: this targets the historical .79 base and asked-answer part of
the gated residual, rather than only donor reweighting or parent routing.
Before an ensemble selector is built, freeze equal-training, out-of-fold
candidate outputs and measure a preregistered finite whole-output mixture
oracle against E041, followed by a separately held-out learned selector.
Its ceiling is conditional on that observed benchmark and candidate library;
it does not establish the hidden survey's ceiling. Existing conditional/full
heads already exist in E041, so merely naming that factorization is not a new
mechanism. A new predictor must supply measured complementary errors.
WB local screening can proceed independently because .49 is not a known
ceiling. Hosted experiments retain the standing UNHCR-only control rule until
a separately authorized, single-instrument WB test is planned.

### Submission discipline

Keep technically validated exploratory submissions possible under the user's
daily-slot preference, but state a score-seeking versus diagnostic purpose.
A diagnostic intervention must distinguish stated hypotheses at the available
resolution; no artificial telemetry encoding or routine repeats to chase noise.
For a score-seeking candidate, reserve the bulk of effort for demonstrating
learnable held-out improvement and meaningful prediction changes before full
packaging. All current no-regression/parity/checker/runtime rules still apply.
No E050 registration or executable plan is claimed by this strategy review.

## Score scenarios, not forecasts

Treating displayed components as exact only for arithmetic:
(.52+.49+.92)/3=.6433; replacing H with .93 gives .6467, approximately .65.
With WB .50 and H .95 the mean is .6567, approximately .66. Real displayed
scores are rounded/noised, and winning rank depends on future competitors.
Neither .65 nor a particular method guarantees victory. No calibrated success
probability or expected improvement can be assigned from the current evidence.

## Sources checked in this review

- A006/A007/A008, E042/E045/E047/E049 experiments and frozen scorecards.
- Current supervised_retrieval.py, link_sharp.py, adaptive_final_evidence.py,
  adaptive_tabpfn_parents.py; no source edits.
- scikit-learn stacking documentation, accessed2026-09-24: out-of-fold base
  predictions are used for meta-estimation; reused training predictions can
  overfit. This supports the validation principle, not a score-gain claim.
  https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.StackingClassifier.html
- Original TabPFN paper, checked2026-09-24; generic benchmark performance does
  not establish this restricted E049 configuration's humanitarian transfer.
  https://www.nature.com/articles/s41586-024-08328-6
