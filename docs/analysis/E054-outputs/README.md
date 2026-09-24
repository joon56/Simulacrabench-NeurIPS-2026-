# E054 technical qualification archive

Fresh source fits and official extracted-ZIP runs are recorded in verification.json
under submissions/2026-09-24-E054/. Source caches contain both original E041 and
probe vectors, persisted before scoring. Only public synthetic labels are used.

artifact-review.py is the exact successful no-fit reviewer script, executed as
tmp/e054_artifact_review.py; copy it to that location to rerun from the repository
root. Its relative-root calculation intentionally preserves the executed version.
artifact-review-result.json records758740checks PASS and zero model fits.
The initial execution failed only when reading a UTF-8 BOM in the method manifest;
the archived script includes the utf-8-sig reader fix. No model/archive changed.

The original verification manifest predates this README, reviewer script/result
and preparation.log copies. These supplementary files are outside its hash set.
Frozen E025/E041 cache dependencies remain at the recorded tmp/e043-eval paths;
their hashes are in the manifest. The archived fresh vectors independently support
source/ZIP parity and probe arithmetic, but rerunning the complete historical-base
check requires those original caches.
