# A012 Task1 phase-2 review

Static review dated 2026-09-24. Reviewed the A012 protocol, Task1 plan,
scripts/verify_e041_phase2.py, tests/test_e041_phase2.py, supplied executed-code
diff, and official grader phase/masking/timing/scoring implementation. Only
partial artifacts existed at this review: UNICEF/World Bank official logs and
source comparisons; UNHCR sequence remained in progress. No new fits or test
suite rerun performed by reviewer.

## Verdict

No additional scientific blocker found beyond the disclosed archival and
absolute-threshold discrepancies. Final qualification remains pending all three
completed instruments, complete provenance, and the corrected derived assessment.
Do not claim final-model adoption or completed phase2 qualification from the
partial output reviewed here.

## Correct aspects

- Source workers explicitly use official sample_rows(...,2) and assert phase2
  means TRAIN+DEV visible and TEST hidden. Official sample_rows masks every
  scored PREDICT item for all TEST respondents and produces canonical cells.
- E025 and E041 source compare the same schema/data/frame hashes and cell counts.
  Their frozen baseline snapshot hashes are checked before the sequence.
- E041 official command explicitly uses --phase 2 and the original assembled
  snapshot. The ZIP is checked and its sole main.py member compared byte-for-
  byte with the snapshot, so snapshot parity also binds the existing ZIP.
- Full raw JSON-vector equality is checked against source, not merely aggregate
  skill equality; official skill/log score must match too. Official PASS already
  validates all vector widths, nonnegativity, finiteness and positive sums.
- Completeness requires all three instruments before the final manifest.
- Calls are sequential in this driver. Absence of other training jobs is an
  operational condition root manages; source inspection alone cannot prove it.
- E025 is freshly run on the same phase2 frame; previous timing is not substituted.
  It is not freshly run through the isolated official driver, consistent with
  the preregistered reuse of its previous official qualification.

## Already identified discrepancies: resolution requirements

1. Source workers score before saving vectors, contrary to the plan's generic
   persist-before-score instruction. These are fixed baseline comparisons, not
   fitted correction/oracle selection; this does not create label leakage into
   the frozen predictions. Preserve the executed script and disclose the actual
   order. Do not claim a pre-score freeze for A012. E053's stricter freeze order
   remains separate.
2. The script's local_no_regression is one-sided (delta >= -.002), while the
   registration says abs(delta) <= .002. Derive a new assessment from the frozen
   per-instrument deltas using the registered absolute test. Retain the original
   manifest and clearly distinguish its legacy flag from the corrected result.
   A >+.002 result would be positive local evidence but would not satisfy that
   explicitly registered absolute-distance check. No refit is needed.
3. Full dependency/package/artifact provenance was not recorded before fitting.
   Bind the executed verifier bytes; source and test bytes; config.yml;
   make_sandbox.py; score.py/checker; all src dependencies; package versions;
   schema/data/snapshot/ZIP; and every result/prediction/log artifact afterward.
   Label the collection post-run, not contemporaneous pre-run proof. Matching
   archived prior src hashes supplies additional evidence for unchanged source.

## Additional nonblocking details for final reporting

The official JSON `seconds` is not pure import+predict time. score.py starts its
clock before loading config/schema/data, and stops after prediction, validation,
scoring and baseline calculation. It includes staging/environment preparation
and repeated process/model imports for each instrument. Therefore the summed
value is an inclusive local rehearsal measurement and safely includes the
required import+prediction work; label it accordingly. It is not a measurement
of one hosted shared-process execution. Source `predict_seconds` excludes module
import and should not be presented as the official combined budget metric.

The driver invokes the official subprocess with no Docker memory cap. Passing
shows local official contract/runtime behavior, not a measured 16GB hosted peak
or a GPU/CPU hosted speed guarantee. This limitation does not require additional
fits for this bounded comparison deliverable.

write_new refuses replacement but does not refuse an entire existing run before
starting expensive work: a repeat invocation may execute the checker or a fit
before its existing output file raises. Do not rerun this same output namespace
to complete review. Finish the existing sequence; compute missing derived facts
from frozen artifacts. This is an operational guard weakness, not corruption of
the first run's already exclusive-write artifacts.

The original per-source frame digest omits the truth vector directly, but the
underlying respondent parquet and schema hashes bind truth through deterministic
sample_rows. Hash config.yml and the loader/scorer implementation in supplementary
provenance to complete that reconstruction chain.

## Verification status and attribution

This A012 review is static plus inspection of partial JSON/log artifacts. No
independent full vector recount or final all-three arithmetic verification is
claimed yet. The root executed the focused tests and is executing the official
runs; numerical pass claims belong to those recorded executions.

Separately, for E053, reviewer-authored independent probe was executed by root:
80 synthetic scalar comparisons passed, maximum score difference
1.7763568394002505e-15; metadata checks and 51 source hashes passed; no model fits
or observed labels were scored in that probe. That numerical evidence must not
be mislabeled as an A012 fit or a reviewer-local runtime execution.

## Final artifact review checklist

Read final verification and supplementary corrected assessment; recompute all
three deltas, absolute thresholds, cell counts, official seconds sum and mean
skills from archived JSON. Verify source/official vector equality from frozen
predictions without fitting, artifact hashes, unchanged baseline/source bytes,
and agreement between the comparison table, A012 result, status and final report.
Confirm no production promotion, hosted upload, package replacement or method
completion claim is introduced by this engineering qualification.

## Final A012 record review after all three runs

Inspected completed verification.json, supplemental-verification.json, SCORES.md
and updated A012 result. All three official runs are complete. Fresh E025 and
E041 scores agree on UNICEF/World Bank; UNHCR delta is
-.0005084489956005411. All pass the registered absolute .002 criterion. The
supplementary derived assessment corrects the original one-sided flag without
replacing the historical run output. Original executed verifier bytes remain
archived separately from the corrected reusable script.

Reviewer independently verified all89 supplemental artifact SHA-256 entries
using PowerShell: zero mismatches. Coverage includes current/executed verifier,
tests, official config/load/scorer/checker, source tree, schemas, data, original
snapshots/ZIP, predictions and logs. This is post-run provenance, explicitly so
labeled. Registration and result documents correctly disclose score-before-save
and provenance timing rather than retroactively claiming a pre-score freeze.

Final table uses the correct fresh paired comparison, mean E025 .505800363144,
mean E041 .505630880146 and mean delta -.000169483000. Inclusive official time
367.1769950389862s is below3600s. The table correctly distinguishes E025/E041 raw
maximum difference (.5364180261586164 on UNHCR) from exact E041 source/official
parity. No positive humanitarian-transfer or final promotion claim appears.

The small fresh E025 drift from its prior rehearsal is disclosed with cause
unassigned; it does not invalidate the current paired same-frame comparison.
E025 fallback remains intact. E041 method coverage remains pending.

A reviewer-authored stdlib-only probe at tmp/a012-frozen-artifact-probe.py was
provided to root for independent full-vector and arithmetic confirmation. It
performs no model imports/fits or new scoring. Root execution result is to be
appended below; until then these conclusions distinguish completed hash/static
review from that additional dynamic artifact check.

### Root-executed frozen-artifact probe: PASS

Root executed the reviewer-authored probe successfully (exit0); reviewer read
tmp/a012-frozen-artifact-probe.log. All89 artifact hashes passed. Every one of
442425 E041 source/official raw vectors matched exactly:41676 UNICEF,92112
World Bank,308637 UNHCR. Frame/schema/data alignment, phase roles, all3 PASS,
score/delta arithmetic, baseline vector differences, corrected absolute gates,
original ZIP/main equality and inclusive seconds sum all passed.

Recomputed means: E025 .5058003631442556, E041 .505630880145722,
mean delta approximately -.0001694829985335; inclusive time
367.1769950389862s. No model fits or new scoring in this probe. Root also reports
corrected reusable-script focused5tests PASS0.016s; reviewer did not duplicate.

Final verdict: E041 satisfies this registered local phase2 engineering
qualification. No unresolved blocker for the requested comparison deliverable.
This is not final-model promotion, method completion, hosted runtime/memory
qualification, or evidence of confidential TEST improvement. E025 fallback and
E041 DEV incumbent roles remain correctly separated.
