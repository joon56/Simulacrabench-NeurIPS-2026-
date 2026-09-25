# A018 independent static review and resolution

Read-only reviewer inspected A018 code, comparison and disclosure, without
models, proxy labels, edits or commits. No high-severity defect found.

1. Official CLI orchestration used per-instrument timeout3600 and checked the
   all-three total afterward. Subprocess timeout on Windows could leave child
   predictors alive. Completed execution was359.449s official/364.340s inclusive,
   so no limit was reached. Preserved official_release.executed.py unchanged;
   future runner uses the remaining all-three budget and kills only its owned
   process tree on timeout. No rerun or changed model result.
2. Shared-process memory counters measured true lifetime peaks, but initial
   enforcement checked after each instrument. Actual peak values remained
   below1.61GB throughout, making the successful measurements valid. Preserved
   verify_release.executed.py (hash equals preflight verifier hash). Future
   workers add a polling watchdog using OS lifetime peaks, exiting125 at16GB;
   counter-read failure fails closed. Parent timeout kills its owned tree.
3. E025 historical official validation was over-described as freshly bound to
   current scorer/data. Its old report binds main/ZIP but retains no raw official
   vectors/scorer/data hashes. Corrected scorecard, method and analysis: fresh
   equality is to A012's frozen-main reference, not modular-source or historical
   official raw vectors. Historical official-minus-A012 UNICEF/WB differences
   +.000007983303/-.000012753036 remain unexplained. Old report hash is in final
   provenance. E041 has stronger freshly re-executed official/source parity.

The first two missing guard functions were reproduced with two failing tests.
Corrected guards passed real-process tests for early memory exit, killing a
grandchild on timeout, and refusing launch when the budget is exhausted. No
model fit or data access in these tests. Existing five phase-2 guards also pass.
Final test output is recorded in verification-checks.txt.

Executed diagnostic bytes are preserved separately from improved reusable
tools. Neither predictor, its candidate set, its score thresholds nor any
historical experimental verdict was modified in response to review.
