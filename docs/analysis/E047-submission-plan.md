# E047 submission work plan

2026-09-22, branch work/e046-submission (contains the stopped E046 screen).
E047 is a separately preregistered fallback; parent E041.

1. Screen the registered query-adaptive final-evidence family on observed
   Adult seeds47/48. No production estimator until both oracle gates pass.
2. Add src/models/adaptive_final_evidence.py and meaningful tests first:
   analytic gradient, masking/split isolation, constant-feature stability,
   section selection independent of audit, audit rejection identity,
   normalized mixture/floor, exact control fallback, frozen assembly parity.
3. Fit the correction only on outer correction-fit rows. Selection/audit
   remain separate. Reuse immutable E041 through link_sharp's layer_fn hook
   to capture raw evidence. Final correction acts after every gate/evidence
   step; it is not fed back into gate propagation. No old source edits.
4. Apply the same correction code to saved observed proxy predictions, report
   selection and pre-guard audit effects and uncertainty without retuning.
5. Run clean all3 source evaluation against E025/E041 and household diagnostic.
   Assemble pinned E041 plus new code to submissions/2026-09-22-E047/main.py,
   ZIP at submissions/2026-09-22-E047.zip. Preregister hosted readings.
6. Verify checker, official all3, raw-vector parity and total <900s, including
   separate tests that exercise an active correction even if sandbox rejects.
7. Independent review, resolve important findings; record A008/top log/status/
   experiment/submission #28/tree. Commit scoped files and push private origin.
   Preserve unrelated user changes; no hosted upload or main-branch merge.

E046 was stopped at .00014514 proxy skill/3, below .005. Its script/results
remain recorded. Do not replace E046's failed family with E047 retroactively.
E047's more permissive query-wise oracle measures possible adaptive headroom,
not estimated improvement or proof that the seven features can learn it.

Progress: both oracle gates passed (+.008792002 / +.008430994 skill/3) and
independent review found no important blocker. New model/tests delegated;
root ran RED: two collection errors for the intentionally missing module.
Root added deterministic assembly, active-path assembly tests, observed
estimator evaluator, and preregistered submission #28 scorecard. Source and
official evaluations remain pending. Frozen baseline caches revalidated by
current frame+snapshot hashes; their recorded times are historical.

Branch renamed work/e047-submission. Source model frozen; sixteen tests passed
in4.64s, independent review found no important blocker. Clarified reuse of
the observed audit after oracle screening; no parameter change. Observed
learned skill +.000273604/0 is inconclusive. Clean all3 exactly matches E041,
UNHCR delta -.000486145 vs E025. Source total491.134s; all clean sections reject.
Household source skill .554337042 vs E041 .552012531, delta+.002324510; groups
3/4 (sections7b/7c) selected and internal audit passed. This is assumed-structure
directional evidence only, below the .005 mean adoption bar. Official x3 and
an additional actual active-household assembly parity check are running.

Completed: checker + official phase1 all3 PASS, source/archive every-vector
parity0, total515.179513693s <900 (CPU-only,2 threads; verification wall526.767s).
Actual active-household snapshot run .554337041587 exactly matches source;
dedicated hash-bound parity record PASS across180411 cells. Independent review
found no important blocker; audit-reuse wording corrected. All technical work
complete. Model remains parked/exploratory, no hosted result or local adoption.
Final records/tree updated; commit and private origin push complete the handoff.
