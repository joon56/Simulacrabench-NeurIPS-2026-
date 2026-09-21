# E045 preserve-and-expand retrieval implementation plan

Goal: prepare today's technically validated UNHCR-only score-seeking archive.
Architecture: preserve E041, screen a distinct candidate union before fitting
a guarded section metric. Reuse existing evidence and lambda flow by replacing
only fit_sections and _replace_evidence bindings in a new layer module.
Tools: Python, NumPy/SciPy, pytest, existing official scorer and sandbox.

Constraints: user-authorized daily submission preparation; no hosted upload.
English code/comments; previous modules and archives immutable. Existing
unrelated working-tree changes excluded. Final archive lives in submissions/.
Use subagent-driven-development for isolated oracle work and independent review;
controller handles integration and archive verification in this session.

- [x] Read CLAUDE, status, latest three log entries; inspect E041/E043/E044.
- [x] Register hypothesis, domain check, alternatives and stopping thresholds.
- [x] Oracle task: scripts/oracle_e045.py imports the E043 protocol helpers,
  uses seeds 43/44 and distinct union vs old32 with inactive sections identical.
  Record independent source hashes and audit-label masking checks to
  docs/analysis/E045-outputs/. Do not implement production code before PASS.
- [x] Model task after PASS: test duplicate-free masked union posteriors,
  self-exclusion, retention of every original donor, gradient by finite
  differences, unchanged inactive sections, audit/selector-label separation,
  and exact non-UNHCR fallback. Then implement src/models/union_retrieval.py.
- [x] Observed audit: fixed seeds 43/44, separate audit, existing honest logistic
  comparison; report actual selected sections, delta and paired uncertainty.
  Do not change settings after audit outcomes. Local training is not evidence
  about unseen HSCC score.
- [x] Measure existing household sim for direction only.
- [x] Clean source validation: frozen E041/E025 against current frame/source
  hashes; all three schemas, exact controls and <=.002 UNHCR no-regression.
- [x] Assemble E041 bytes plus explicit overrides, deterministic ZIP. Run
  checker and isolated score.py all three; compare every output probability
  with source and check total runtime. Register SCORES.md before any upload.
- [x] Independent review of scope, leakage, estimator/oracle mismatch,
  self-exclusion, assembly and verification. Resolve important findings.
- [x] Update experiment Decision, top log, status, submission row #27, A008,
  tree. Verify old snapshots and user changes untouched.

Delivery: commit scoped E045 files and push work/e045-submission to private origin.

Progress updates are recorded here so unfinished work can resume after compaction.

Oracle task complete: seed43 +.007834131668 and seed44 +.009196163696, certified
marginal skill/3. Gate PASS; independent oracle review PASS, no blockers.
Model/test task delegated with locked API fit_union_sections/union_evidence,
candidate_union/union_objective, union_layer and isolated LAST_DIAGNOSTICS.
Root prepared observed audit and assembly scripts, plus date/output overrides
on the existing verifier. Frozen E041/E025 baseline caches revalidated against
current frame and snapshot hashes, copied to today's analysis outputs without
rerunning training. Cached timings are historical, not new measurements.

Model completed and frozen: root final test run 23 passed in 5.99s. Observed
audit deltas +.000426 / +.000495 skill; both paired intervals include zero.
No settings revised after the audit. Independent code review found no important
blocker; renamed an output field to retrieval_shares (no numerical change).
Assembler's first overly broad parent-name check falsely matched E025 local
variables; scoped it to the appended E045 tree. Build and checker then PASS.
New source clean run and existing household simulation run are in progress.

Clean source now complete: .500648423/.454717307/.562397862, exact controls,
UNHCR delta -.000064867 vs E041 / -.000551012 vs E025, both pass. Selected
unions in sections 3/4/5/6; mean delta -.000021622. Source time 401.921 s.
Official extracted-ZIP verification running; household simulation still running.

Household sim complete: .551945260 vs E041 .552012531, delta -.000067271.
First official verification stopped at writing a relative --log path after
switching subprocess cwd to the kit. Resolved output directory before subprocess
launch; rerunning all three official schemas. Submission code/ZIP unchanged.

Official rerun completed: PASS x3, all-vector source/archive parity zero,
395.852123499 s combined / 406.7298399 s wall. User-facing archive ready for
one exploratory slot; no hosted result or upload. E041 remains incumbent.
Final independent records review PASS, no blockers. Integrity check PASS:
current source dependency hash, ZIP/main parity, old snapshot hashes, all
official scores/parity/no-regression/runtime, historical rows1-26, unchanged
preregistered reading arms, and no edits to prior model files. This completed
validation record accompanies the scoped delivery commit; no hosted upload.
