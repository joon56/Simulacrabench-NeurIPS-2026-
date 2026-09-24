# E054 pre-run probe and package review

Reviewed 2026-09-24 at dispatched freeze 286ca28: new
src/models/e041_gated_probe.py, scripts/prepare_e054.py,
tests/test_e054_probe.py, and submissions/2026-09-24-E054/SCORES.md.
Read relevant cache verifier and fixed E041 snapshot. No fits or test reruns.

## Pre-run verdict

No blocking implementation defect found. Ready for sequential technical
verification; no claim that checks have passed before their outputs exist.

- The transform detects UNHCR by its established schema marker. Other
  instruments return the original vector collection unchanged.
- For UNHCR, PREDICT items follow schema order, rows follow frame order,
  and only blank targets advance the canonical vector index. Count mismatch
  raises before replacement. GIVEN and EXCLUDE items cannot be targeted.
- Only final gated vectors are replaced with full-width uniform vectors,
  including their sentinel slot. The output list is shallow-copied;
  unaffected arrays remain the same objects and changed arrays are newly
  allocated. Base probabilities are not mutated. Base predict runs once
  before the transform, so replacements cannot propagate to descendants.
- Packaging verifies the fixed E041 SHA-256, appends the inspected transform
  and wrapper to its exact bytes, and places main.py at ZIP root. The fixed
  E041 snapshot already supplies numpy. No incumbent rewrite is performed.
- Fresh source execution captures the unmodified base before transformation.
  It requires exact vector equality to matching-frame, matching-source E041
  caches and absolute skill difference <=.002 against E025. Cache hashes are
  archived. The deliberate probe loss is evaluated separately from base
  regression, including direct decomposition equality for UNHCR.
- Every instrument requires untouched-vector equality, exact source/official
  assembled vector parity and skill equality. ZIP checker, all three official
  phase-1 PASS results, and summed official runtime <900 seconds are required
  before final verification.json is written.
- Package/main/ZIP/run-directory preflight rejects an existing namespace;
  files use exclusive creation, including ZIP. A failed partial run cannot
  silently overwrite prior outputs on restart. Model endpoints are frozen
  before local scoring; scorecard and source hashes are archived pre-run.

## Scope and nonblocking limitations

Root reports four focused unit tests passed; this reviewer did not duplicate
them. Full technical success awaits actual outputs and their independent
review. Existing 51-file preservation is root's separate frozen-hash check,
not established merely by reading this script.

The source verifier hardcodes floor .001, matching the frozen official config;
schema/config provenance should remain fixed. A future config change needs
an explicit check or use of config['scoring']['floor']. Source cache frame
hash includes schema/config/frame/cells/truth and prevents an accidental
comparison across inputs. Cache metadata is trusted local provenance, not
an independent reconstruction of historical execution.

execute() has no external subprocess timeout; official score.py controls its
inference timeout. Summed local official seconds are measured conservatively
across three scorer launches but do not guarantee hosted shared-process
runtime, memory, numerical stability, or repeated true control predictions.

Scorecard explicitly preserves the preregistration interpretation ambiguity,
93-only implementation PASS, lack of any common-order six-draw passing arm,
low expected-information evidence, unresolved .39-.43 arms, and the distinction
between after-rounding outer feasibility and common-model conclusions at .44.
No point forecast, repair-mechanism inference, adoption, or upload is implied.
