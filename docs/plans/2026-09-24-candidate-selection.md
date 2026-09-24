# E050/E051 candidate selection and daily delivery plan

> For agentic workers: use subagent-driven-development for the bounded library
> implementation and requesting-code-review before release. User has approved
> the proposed workflow and delivery; execute without repeated confirmation.

**Goal:** Compare distinct named mechanisms before choosing today's submission.
**Architecture:** One frozen E041 fit per frame supplies cached recursive arms;
an independent direct content tree library shares the same fit/query partition.
Choose only after preregistered oracle and actual learned evaluation.
**Tech stack:** existing Python/numpy/pandas/torch/scikit-learn; no new packages.

## Global constraints

- Read E050/E051 registrations for exact fixed library and gate values.
- Old source and submission snapshots immutable. Add modules/scripts/tests only.
- Outer query PREDICT blocks hidden before every fit and donor bank.
- Controls exact E041/E025; clean skill difference <=.002; raw parity<=1e-12.
- ZIP checker and official score.py all3 PASS; shared execution <900s.
- No external fitted artifacts in production; no runtime network/data export.
- English code/docs/commits; preserve unrelated .claude/.gitignore/trip edits.
- Dated ZIP and snapshot under submissions/. Score arms before user upload.

## Tasks and progress ledger

- [x] Read history/A009; register E050/E051 before execution. Branch work/e050-submission.
- [ ] Build diagnostic library in src/eval/recursive_candidates.py with focused
  tests tests/test_recursive_candidates.py. e050_library(frame,schema) returns
  raw original vectors plus five mapped arm arrays and predicted components;
  identity must match E041 exactly. Cache private renderer globals; no imports
  from E049 and no original module mutation. e051_library uses same base and
  masked frame, fitting direct trees on visible rows only.
- [ ] scripts/screen_e050_e051.py runs actual E041 on observed Adult schema
  adapter and optionally clean/household. Save source/frame hashes, frozen
  library arrays and exact oracle results under docs/analysis/E050-outputs/.
  Adult5000 uses2600fit/800oracle/800selection/800audit; screen only oracle
  labels, leaving the learned-policy audit unread until its policy freezes.
  Do not fit selection policies before oracle passes. Use native schema values
  and GIVEN names; explicit generic stack invocation for observed schema only.
- [ ] Independently review component separability, caching, label isolation,
  class mapping and bound scope. Compare candidate evidence in one ledger.
- [ ] Register production details for the eligible winner, add new model module
  with meaningful masking/fallback/active tests, and measure actual learned
  selection and untouched audit gain. If both gates fail, record stops before
  designing any distinct alternative; do not relabel a failed family as success.
- [ ] Assemble winner from immutable E041/E025; clean all3 and active parity,
  official checker/score all3, full active budget if clean falls back.
- [ ] Record scorecard, experiment Result/Decision, submission index, status,
  log top, analysis, tree; review final artifacts, commit experiment IDs, push.

## Validation commands

Run library tests with `.venv/Scripts/python -m pytest tests/test_recursive_candidates.py -q`.
Run screen with `.venv/Scripts/python scripts/screen_e050_e051.py --case adult --seed 51`
and the preregistered seed52, logging long processes under tmp/.
Use scripts/check_daily_retrieval.py and the official archive verifier for the
selected source/snapshot. Freeze source dependency hashes before expensive runs.
Report actual learned effects separately from oracle/engineering checks.
