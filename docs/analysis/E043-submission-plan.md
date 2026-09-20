# E043 Daily Submission Plan

> Execute the user-approved candidate-search design in this session using
> subagent-driven-development for independent review. No further approval
> is needed for local preparation; no automatic hosted upload.

**Goal:** Prepare one technically verified, preregistered exploratory archive
for 2026-09-20, based on E041, choosing the agreed control if the oracle stops
candidate-search implementation.

**Architecture:** E041 remains immutable. First compare old/new candidate
oracle families on observed data. Gate failure routes to E044: remove only
the learned weights from E041 evidence construction, retaining the learned
activation mask and recalibrating the unchanged lambda procedure. This is a
conditional weight-use ablation, not a complete removal of metric training.

**Stack:** Existing Python, numpy, scipy, torch, official kit; no new package.

## Constraints

- Existing model modules/snapshots unchanged, new module for chosen arm.
- Archive `submissions/2026-09-20-E0XX.zip`, matching source/SCORES directory.
- UNHCR only; exact UNICEF/WB fallback. No hidden-data diagnostics exported.
- Shared phase-1 900 s; clean regression <=.002 versus both E041 and E025.
- Keep local adoption distinct from the user's exploratory slot objective.

## Tasks

- [x] Register E043 and measure observed-data candidate oracle before estimator.
  Reuse `tests/e041_external.py` source/splits and `mixture_oracle` bounds;
  record new-pool lower minus old-pool upper, not total oracle headroom.
- [x] Choose the registered branch and write its experiment/scorecard before
  fitting/scoring. Test self exclusion, no-effect fallback, and intended
  single intervention before adding production code in a new model module.
- [x] Run `.venv/Scripts/python.exe -m pytest` on the relevant E041 and new
  invariant tests. Evaluate the whole chosen pipeline, clean and household,
  with comparison values computed from frozen snapshots and current frames.
- [x] Assemble by script from immutable E041; verify its embedded E025 prefix.
  Run clean source prediction and the extracted ZIP under official score.py,
  all three schemas. Assert every-vector parity <=1e-12, fixed controls and
  sum runtime <900 s. Hash source/frame caches to prevent stale comparisons.
- [x] Independent review of intervention scope and evidence interpretation.
  Update experiment Decision, SCORES, status and TOP of daily log; preserve
  submission table rows restored on main. Render tree, commit scoped changes,
  push today's branch. Return the exact archive path and honest reading arms.

## Execution notes

- E043 gate failed: new-versus-old oracle skill /3 +.000962822 / -.000392472
  on the two frozen observed splits. No production candidate-search code.
- E044 control registered before implementation. Red test: module absent;
  green: 15 E041/E044 invariant tests pass. Parent model modules unchanged.
- Clean source E044 .500648423/.454717307/.562294713; UNHCR delta versus
  E041 -.000168016 and E025 -.000654161; exact control vectors unchanged.
- Independent review confirmed intervention scope and immutable assembly.
  Fixed verifier gaps: pin both baseline code hashes, require both comparisons,
  recheck their frame hashes and recompute deltas from official predictions.
- Copied layer globals share the in-memory diagnostics dictionary. This does
  not alter parent function bindings or inference decisions; documented in
  snapshot README instead of introducing an unrelated predictor change.
- Household sim E044 versus E041 +.003090025 UNHCR skill; no audit-driven
  changes. ZIP checker PASS, official x3 PASS, every-vector parity exact x3,
  total official local runtime 371.022 s. Final artifact is E044, not E043.
