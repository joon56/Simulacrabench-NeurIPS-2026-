# E052 diagnostic implementation

New files: `src/eval/evidence_routing.py`, `tests/test_evidence_routing.py`,
`scripts/screen_e052.py`. Existing modules/snapshots unchanged. No production
wrapper, expensive screen execution, selector or commit performed by implementer.

## Interface

`routing_library(frame, schema)` fits the actual generic E041 stack once using
the private cached renderer, captures the original evidence/lambdas, renders
the fully evidence-free base recursion, and reapplies original own-item
evidence. Returns original raw E041 as `base_raw`, evidence-free recursion as
`base_routed_raw`, fixed output as `arms_raw['after_gates']`, mapped `arms`,
query indices, predicted items, options, PREDICT components, original
`evidence_rows`/`lambdas`, and label-free diagnostics. No normalization.

Original vector objects are preserved for ungated/GIVEN-parent heads,
lambda-one heads, unchanged parent asked mass, and exact candidate equality.
Partial query blocks are rejected before fitting. Production wrapper decides
the preregistered E041 fallback; diagnostic helper raises `ValueError`.

`screen_e052.py --case clean|household` uses unchanged official/HH-seed13 cases.
Requires existing frozen E041 cache; verifies frame, code, current snapshot
hash and exact vector equality. Freezes complete endpoint pickle, NPZ and
SHA256 source/frame/artifact manifest before scoring. Writes complete scalar
official scores, exact two-arm component oracle, changed-vector count/fraction,
and descriptive per-item/depth/section helpful/harmful cell effects. No policy
selected. Default output `docs/analysis/E052-outputs`. Screens intentionally
not executed by this implementation task.

## Validation

TDD: first four tests failed on missing diagnostic module; implemented helper
and all four passed. Fifth screen test failed on missing script; implemented
script. Final command:

`.venv/Scripts/python.exe -m pytest tests/test_evidence_routing.py tests/test_recursive_candidates.py -q`

Result: **16 passed in 5.01s**. Required escalated interpreter execution because
sandbox reports the existing Python313 target inaccessible.

Reference test modifies the original recursive renderer independently to
store each pre-evidence base in its routing beliefs, while returning its own
post-evidence output. It compares multi-depth results to the new two-pass
implementation, including both concentration buckets, lambda1, agreement0,
GIVEN boundaries, no evidence, and zero-weight evidence. Expensive model fits
are fixed test products; the actual ladder/recursive rendering executes.
Screen test checks endpoint freezing before oracle scoring, exact baseline
parity, descriptive cell accounting, and frame rejection before fitting.

## Post-screen overwrite guard

Independent review identified that a rerun could overwrite frozen artifacts.
After BOTH real clean/household screens completed, added fail-fast refusal if
any endpoint pickle, NPZ, manifest or screen result already exists for the case.
The guard executes before case loading or fitting. Four parametrized regression
tests failed before the guard and passed afterward. The wrong-baseline test now
uses a fresh output directory, preserving that distinct validation.

Final focused command result: **20 passed in 4.77s**. No real fit rerun; no source
helper or saved endpoint/score/manifest modified. Executed script retained as
`docs/analysis/E052-outputs/screen-executed.py`, SHA256
`d74d19c7a4fc9813a47c18389318b42adfd63be7722f2fe08917a19c14ada36b`.
Current guarded `scripts/screen_e052.py` SHA256
`0ffe35a9e9933959d82708fa94b16727f2ac0fd1c1762f1f3b4e60018197fcd9`.
The scientific outputs bind the retained executed script, not this later guard.
