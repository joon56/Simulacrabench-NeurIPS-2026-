# E057 S2 release verification plan

Date: 2026-09-25. Input HEAD949884b; owner: this S2 session.
User authorizes remaining release verification, not upload, S3 or TEST choice.
Existing user changes and all previous submissions/research records preserved.

Goal: bind unchanged E057 default source and its standalone archive to complete
phase-1 outputs, active-path invariants, official all3 and shared resource use.
No candidate tuning, new seed, alternate arm scoring, proxy access or baseline
refit. Existing S1 source/data/roles/caches must hash-match before reuse.

Implementation follows the supplied S2 design. New files only:
scripts/assemble_e057.py, scripts/release_e057.py,
tests/test_e057_release.py, this record, E057 s2 aggregate records, and
submissions/2026-09-25-E057/{main.py,SCORES.md,verification.json,NOTICE.txt}
with its matching ZIP. Row vectors remain ignored in external/e057-s2/.
Date is preparation date; intended/actual upload timestamps remain unknown.

## Frozen checks and execution budget

- [ ] Namespace-isolated deterministic E057 assembly on immutable E041 main
  SHA25622c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073.
  Copy the exact floor helper; preserve baseline globals and starter-kit notice.
  Test active/rejected/sparse/alpha0/schema-order fixtures against source before
  expensive execution. No change to existing production source.
- [ ] Preflight all S1 provenance and six baseline caches; snapshot this plan,
  scorecard, code, versions and archive hashes before runs. Refuse occupied
  run/output names. Official kit remote remains ee427a9 on this date.
- [ ] One source-default all3 run, no injected baseline. Capture shadow/refit,
  shares, splits and final vectors; compare exactly to S1 frozen artifacts.
- [ ] One extracted-assembly shared-process all3 run, no injected baseline.
  Compare default outputs and intermediate libraries exactly. Force alpha=.5
  only on frozen prediction libraries without label scoring; verify active
  source/assembly parity, nonleaves/parents, sentinel/mass/floor, sparse fallback.
- [ ] One unchanged official score.py run for each phase-1 schema using the
  extracted archive; capture raw predictions and compare to default/assembly.
  Bind current outputs to existing E025 absolute .002 and E041 references.
- [ ] Freeze verification, append measured results without changing scorecard
  arms, update experiment/status/log, commit task files and push existing origin.

At most three all3 suites: default, shared assembly, official all3. Sequential
heavy execution only, CPU2 threads, no GPU/download/paid compute. Each suite
hard wall cap900s; official runs share one cumulative900s cap. Total expensive
suite wall cap2700s (45min). Own process-tree memory cap8GiB, stricter than hosted
16GB. Watchdog starts before numerical imports; parent includes process launch
and ends after result writing. Abort owned process tree on cap/monitor failure.
Existing S1 injected-baseline run cannot certify the new execution paths, which
justifies these new executions. No repeat of a successful identical suite.
Any correctness, parity, runtime, memory or official failure stops qualification;
preserve partial outputs and diagnose without parameter changes or blind retry.

Allowed labels: previously exposed synthetic phase1 TRAIN for the unchanged
visible-row selector/refit, synthetic DEV for fixed release comparison only.
No synthetic TEST, E056 proxy arrays, calibration or hidden competition labels.
Strong claims remain restricted to this fixture and installed CPU environment.

Technical PASS and useful DEV exploration are separate. If all checks pass,
E057 is eligible for a bounded user-controlled DEV exploration; it remains
parked/unsubmitted and E041 remains incumbent until actual evidence warrants
change. Active fixture is structural evidence, never efficacy or activation
evidence for the hidden channel. No S3 action follows a PASS.
