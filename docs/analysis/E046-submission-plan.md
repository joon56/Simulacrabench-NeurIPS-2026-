# E046 submission work plan

Registered 2026-09-22. Parent E041; branch work/e046-submission.

1. Run the observed-data tree oracle specified in the experiment. Stop the
   estimator if its gate fails; retain the failed screen in the experiment tree.
2. After a pass, add a new model with honest common training rows, section
   selection and a separate audit. Keep the original 57 ungated tree heads,
   E041 evidence, and the same mixture before gate propagation in all stages.
3. Test masking/split isolation, scorer flooring, descendant propagation,
   fallback identity and source/snapshot behavior on both active and inactive
   policies. Do not modify old model files.
4. Run clean sandbox source comparison with E025 and E041, plus the existing
   household diagnostic. Preserve controls exactly; no-regression <=.002.
5. Assemble from pinned E041, create the dated ZIP in submissions, preregister
   SCORES.md, and run official ZIP checker plus all three official phase-1
   scores with raw-vector parity and shared runtime under 900 seconds.
6. Independent code review, resolve material findings, update experiment,
   A008, status, top log, submission index and rendered tree. Commit only this
   experiment's files and push the private origin branch. No competition upload.

Implementation design after gate: precompute E041 component distributions once
per fit, then evaluate a vectorized renderer with section-shared neural/tree
weights {0,.25,.5}. Compare that renderer against the original link_sharp
composition on test fixtures before relying on it. All 213 final items enter
the selector, including descendants of the 57 roots. One fixed section-order
coordinate pass on selection; no audit optimization. Selection gain threshold
max(.001,2 respondent SE), independent overall audit threshold max(0,1SE).
Outer shuffle seed4601; selection800/audit400 (capped at visible_count/10
each on small inputs); all PREDICT cells blank in both before any fit. A final
full-data refit uses selected weights; rejected policies return exact E041.
Small inputs below4000 complete rows retain E041. No learned artifacts or
external records enter the ZIP. Existing observed Adult data only screens the
method offline, with its existing attribution retained.

Runtime risk: two E041 fits plus two sets of 57 short tree fits. Measure total,
not just model training. Do not claim the local CPU number guarantees hosted
runtime or use the oracle to predict hosted score.

Outcome: step1 failed (+.000145139/.000017564 skill/3). Stopped before model
implementation; no E046 archive. Remaining E046 estimator/package steps were
not executed. Today's separate fallback E047 has its own preregistration,
plan, oracle and submission #28; retained work branch work/e047-submission.
