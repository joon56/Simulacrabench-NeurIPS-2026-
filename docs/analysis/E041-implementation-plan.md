# E041 Submission Implementation Plan

> Execute in this session. The user's request to produce tomorrow's submission
> authorizes implementation of the previously presented retrieval design.

**Goal:** Produce a verified, self-contained UNHCR-only candidate archive, or
record a measured rejection rather than label an unqualified model ready.

**Architecture:** A small section-specific metric reranks GIVEN-based donor
candidates. It is fitted with query-excluded answer loss and compared with
the incumbent on disjoint respondents. A first implementation uses weighted
categorical agreement rather than a large neural retriever; this is a bounded
supervised metric family with no extra package or downloaded model dependency.

**Tech stack:** Python 3.13, numpy, scipy/torch, pandas; existing official kit.

## Constraints

- Preserve existing model modules and submission snapshots.
- CPU-only local environment; hosted H100, shared 900-second budget, 16GB RAM.
- No hidden labels, identifier features or diagnostics exported by submission.
- UNHCR only; other instruments call the unmodified E025 implementation.
- Keep external validation data outside the archive; disclose its use.
- Separate retrieval fitting, selection and audit respondents. No cross-fold
  label access through donor banks. Match full-output official scoring.

## Tasks

- [x] Register domain reasoning and run a constrained oracle before estimator.
  Obtain a public observed dataset if possible; record limitations if blocked.
- [x] Write failing tests for donor self-exclusion, fold isolation, probability
  ordering, official-floor equivalence and exact E025 fallback.
- [x] Implement the smallest supervised metric after the oracle screen in
  src/models/supervised_retrieval.py. The same metric is deployed; section
  selection still uses a proxy base and does not satisfy full-stack objective
  parity. This limitation is recorded; no performance adoption is claimed.
- [x] Evaluate on separate respondents; run clean three-schema comparison and
  an existing directional sim. Record actual deltas and timing, including a
  second split for any surprising gain. Stop a failed branch with its results.
- [x] Assemble main.py by script from E025 plus the new module; compare every
  emitted probability, not just aggregate skill. Freeze code before validation.
- [x] Build ZIP with main.py at root; run official ZIP checker and score.py
  for unicef/world_bank/unhcr in phase 1. Use isolated extraction outside repo
  imports for the archive check. Hash outputs and archive in verification.json.
- [x] Write SCORES.md with decision arms before any upload, update experiment
  Decision, status and log, render tree, review diff and push scoped files.

## Commands and completion evidence

Use .venv/Scripts/python.exe with required execution permissions. Run
`-m pytest tests/test_supervised_retrieval.py -q` for invariants, then
`scripts/check_e041.py` for measured records and parity. Final checker:
`external/starter-kit/tools/check_submission_zip.py <zip>`.
Official scorer uses `--submission <extracted-dir> --data <sandbox-dir>
--schema <schema.json> --phase 1` once per real schema. A candidate is not
ready until every command passes and the performance criterion is met.

## Measured outcome

Archive built and technically verified: official scorer PASS x3, exact source
parity x3, 320.605 s CPU total, 11 invariant tests. Clean no-regression passes
but improvement does not: mean delta -.000162048; existing household sim
UNHCR delta -.002025811. Observed external gains are small and inconclusive.
E041 is rejected and the artifact is marked DO NOT SUBMIT. E042's narrow
fallback oracle also missed its registered threshold, so no estimator followed.
This completes the measured-rejection path, not a qualified winning submission.
