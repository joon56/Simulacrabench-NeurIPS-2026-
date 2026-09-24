# E052 helper and screen independent review

Date: 2026-09-24. Scope: `src/eval/evidence_routing.py`,
`tests/test_evidence_routing.py`, and `scripts/screen_e052.py` against the E052
registration, implementation plan, mechanism review, and incumbent renderer.
No production code changes, fitting, or expensive screens were performed.

## Findings

- Critical: none found.
- Important: none remain. The initial release-tooling issue was that a rerun
  could overwrite frozen case artifacts. After both real screens completed,
  a guard was added that refuses any existing endpoint pickle, NPZ, manifest,
  or result before loading a case or fitting. Independently reviewed and tested;
  issue closed. No actual overwrite occurred, and helper semantics are unchanged.
- Minor: the committed tests do not explicitly cover per-item missing evidence,
  zero-mass evidence, missing lambdas, or input immutability. Independent review
  probes covered these paths successfully; no semantic defect found.

## Verified semantics

- The private renderer caches the original E041 fit, probability maps, ladders,
  and gate agreement. The original supervised evidence layer runs once.
- The second render suppresses evidence at every ancestor. Final composition
  uses the original own-item evidence and original concentration-bucket lambda.
- Original layer object references are retained. Ungated and GIVEN-parent heads,
  zero effective ancestor evidence, zero agreement, and own lambda one preserve
  original raw vector objects where unchanged.
- The independent reference changes belief storage in the original recursive
  renderer, rather than reproducing the helper's composition formula. It
  exercises two successive PREDICT gate edges and both concentration buckets.
- Partial query blocks fail before fitting. No selector, guard, additional
  donor extraction, or production-source mutation was introduced.
- The screen checks frozen E041 snapshot hash, cache source hash, frame hash,
  and exact raw baseline parity. It saves both fixed endpoints before scoring,
  uses the unchanged clean/household case loader (household seed 13), and calls
  the existing exact constant-component two-arm oracle. Depth, section, item,
  helpful-cell and harmful-cell diagnostics are descriptive only.

## Verification evidence

- Implementer reported 16 tests passing (5 E052 tests plus 11 existing recursive
  library tests); the parent independently confirmed all 16 in 7.61 seconds.
- Independently executed 24 deterministic randomized mocked-stack probes with
  seed 52. Varied per-item absent evidence, zero-mass evidence, missing lambdas,
  both buckets, and lambdas in `{0, .13, .72, 1}`. Every endpoint matched the
  independently modified recursive renderer at absolute tolerance `1e-15`.
- Each probe also verified normalized finite nonnegative vectors, byte-equal
  serialized frame/schema/evidence/lambda inputs, and unchanged source function
  references. All passed. These probes did not train a real model.
- Initial sandbox Python launch failed because the base Python executable was
  inaccessible there. The same lightweight probes succeeded with the approved
  escalated interpreter invocation; this was an environment issue.
- After the preservation correction, independently ran only the four new guard
  cases: **4 passed, 5 deselected in 5.50 seconds**. Each verifies early refusal
  and preservation of existing bytes. The implementer reported all 20 relevant
  tests passing in 4.77 seconds.
- Independently checked the retained executed screen hash:
  `d74d19c7a4fc9813a47c18389318b42adfd63be7722f2fe08917a19c14ada36b`.
  Both real manifests match it. The guarded current script has separate hash
  `0ffe35a9e9933959d82708fa94b16727f2ac0fd1c1762f1f3b4e60018197fcd9`.
- Read both recorded screen results: raw E041 parity is exactly zero in both;
  clean delta skill is `+0.00016729102297663445`, household delta is
  `-0.0010802784411780841`. Component oracle skill/3 is respectively
  `0.0000557636743255388` and `0`. Neither clears `.005`; no selector is
  justified. Fixed-endpoint packaging remains exploration, not adoption.

All-instrument checks, production fallback/dispatch, source/archive parity and
runtime remain outside this helper-review scope. No real fit was rerun.
