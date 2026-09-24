# E052 independent release review

2026-09-24. Read-only production review; only this report was written.

## Verdict

No code or scope blocker found. Final technical release qualification passes:
completed official all-three manifest and active assembly parity inspected.
E052 is a fixed exploratory routing control, not an adopted improvement. E041
remains incumbent. No fits, competition upload, or source changes performed.

## Critical

None found.

## Important

None found. Completed `submissions/2026-09-24-E052/verification.json` and
`docs/analysis/E052-outputs/active-assembly-parity.json` pass the registered
technical requirements. Initial pending checks were resolved in this follow-up.

## Minor

None requiring code changes. Root is updating status, plan checkboxes and
scorecard to reflect completed verification; this review does not replace that
record update, commit or private push.

## Reviewed evidence

- Read CLAUDE.md, current status, E050/E051/E052 experiment records, A010, E052
  implementation plan, scorecard, prior mechanism/diagnostic reviews, routing
  helper, private renderer, production wrapper, assembler, active-parity script,
  daily source/official verifier, and relevant existing E041 rendering code.
- Algebra matches the registered endpoint: preserve original fitted products,
  donor evidence and effective per-item/bucket lambda; recursively render base
  beliefs without any ancestor evidence, then apply unchanged own-item evidence.
  No donor refit, lambda retuning, guard, intensity grid or extra estimator.
- Cached renderer copies function globals and memoizes fitted inputs only within
  one invocation. Structural identity shortcuts preserve original raw vectors.
  GIVEN parents, ungated heads, lambda-one, zero agreement and absent/zero
  evidence are covered. Query positions follow schema item order.
- Wrapper rejects partial PREDICT blocks and missing GIVEN/required columns
  before routing fits, then delegates to original E041 behavior. Non-UNHCR and
  custom base options delegate directly. Valid-path errors remain visible.
- E041/E025 parent hashes are pinned and exact E041 bytes remain prefix. Assembly
  binds renderer to `_SHARP_PREDICT` and layer to `_E041_SUPERVISED_LAYER`.
  Original `LAST_DIAGNOSTICS` remains the E041 layer dictionary; wrapper names
  become `_E052_DIAGNOSTICS`. No global alias collision or recursive fallback
  found. Packaged archive contains only main.py, no E050/E051 selectors or trees.
- Independent bounded command:
  `.venv/Scripts/python.exe -m pytest tests/test_e052_submission.py tests/test_evidence_routing.py -q`
  returned **23 passed in 9.16s**. Fits are stubbed; real recursive rendering,
  independent modified-recursion reference, multi-depth/bucket boundaries,
  assembly execution, namespace isolation, argument-preserving fallback,
  artifact overwrite guards and deterministic packaging execute.
- Independently checked both diagnostic manifests with PowerShell SHA256:
  endpoints, NPZ arrays and every listed executed source file match. Historical
  screen hash correctly resolves to retained `screen-executed.py`; post-screen
  overwrite guard does not rewrite scientific provenance.
- Reviewed frozen E050/E051 oracle JSON and screen preparation: 2600 fit, 800
  oracle, 800 selection, 800 audit; whole 2400-query target block masked before
  fitting. Only oracle labels scored. E050 skill/3 0/.000013901722; E051
  .000417804354/.000380218507 fail registered .005 gates. No later selector is
  justified and no universal UNHCR ceiling is claimed.
- E052 records disclose clean +.000167291023 and household -.001080278441 skill,
  failed optional component selector bounds .000055763674/0, and unmeasured
  hosted transfer. They retain inherited replay limitations and distinguish
  fixed exploration under daily-slot preference from evidence of improvement.

## Frozen artifact identity at review

- main.py SHA256: `a77e6529012d7539ce6d519d7eb33adca99b46bc71585c79771d8d2f8a05aa2c`
- ZIP SHA256: `158f2fa1d0f153b54cdab2e8c3ae33c02de6172b0079c471f5f34c2d8014cbaa`
- Source dependency SHA256: `062d32a74adf47746c0111bc64132655c9024f82e8b0c57f1640a4ead0237822`

## Final verification follow-up

- Current main.py and ZIP independently rehashed: unchanged, matching both
  official and active-parity records. Source dependency identity agrees between
  all-three source, official and active-parity records.
- ZIP checker reports valid archive. Official phase 1 returns PASS for UNICEF,
  World Bank and UNHCR, each with raw source parity exactly zero. Both controls
  remain raw-exact versus E041 and E025. UNHCR skill is .562630019880618;
  deltas +.000167291022977 versus E041 and -.000318853824398 versus E025 satisfy
  the preregistered .002 no-regression bound.
- Official measured seconds 43.7943170071 + 108.3332822323 + 250.6672086716
  sum to **402.7948079109 seconds**, below 900. Verification wall time is
  416.2904894 seconds. Runtime sum independently reconciled within 1e-9
  (PowerShell JSON numeric parsing produces a negligible 1e-14 difference).
- Natural active-path record shows 25,911/132,273 changed vectors (19.589%),
  source parity zero, original frozen screen endpoint parity zero, and exact
  structural boundaries. Independently summed per-item changes to 25,911.
  Both diagnostic manifests are recorded verified; earlier independent file
  hashing also passed. Therefore parity exercises the real intervention.
- Root reports the complete combined suite **34 passed in 12.03s**; this review
  independently ran the 23-test release/routing subset above. No tests or fits
  repeated during final follow-up.

## Limits

Unit tests and source inspection establish semantics and packaging, not hosted
accuracy or hosted runtime. No expensive run repeated. Final official and active
raw parity evidence qualifies this fixed local artifact for exploratory
delivery. Record updates, commit and private push remain root-owned completion
steps. No phase-2 promotion or expected .65 claim.
