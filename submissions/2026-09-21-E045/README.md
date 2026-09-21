# E045 - Candidate union with guarded supervised reranking

Status: **READY FOR ONE EXPLORATORY DEV SUBMISSION.** Archive:
[2026-09-21-E045.zip](../2026-09-21-E045.zip). No hosted upload or result.
Checker and official phase-1 x3 PASS; every source/archive probability exactly
matches. Clean no-regression versus E041/E025 passes, controls identical,
23 tests pass. Combined official local time 395.852 s against 900 s shared budget.

E041 remains DEV incumbent at .64/.52/.49/.92. E045 targets UNHCR only. It keeps
E041 learned weights, activation and original 32 candidates, adds up to 32
distinct candidates searched with those weights, and fits an expanded metric.
A separate selection split chooses expanded evidence only when its proxy gain
exceeds max(.003, two paired respondent standard errors). Otherwise E041
evidence remains. Replay uses the same candidate policy as inference, with the
unchanged lambda fitting procedure. Downstream recalibration is part of the
intervention; inherited in-sample base replay is not repaired here.

Observed Adult oracle passed two prespecified splits. Those records are only
external validation: no Adult rows, fitted parameters or downloaded models
are included in the archive. Actual observed audit gains are small and their
intervals include zero; clean and household changes are slightly negative.
No local adoption or expected .65 score is claimed. See [SCORES.md](SCORES.md)
for preregistered readings and all measured results.

Reproduce from repository root:

```powershell
.venv/Scripts/python.exe scripts/oracle_e045.py
.venv/Scripts/python.exe scripts/evaluate_e045_observed.py
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E041 --snapshot submissions/2026-09-19-E041/main.py --output-dir docs/analysis/E045-outputs
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E025 --snapshot submissions/2026-09-09-E025/main.py --output-dir docs/analysis/E045-outputs
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E045 --module src.models.union_retrieval --compare E041,E025 --output-dir docs/analysis/E045-outputs
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E041 --snapshot submissions/2026-09-19-E041/main.py --case household --schemas unhcr --output-dir docs/analysis/E045-outputs
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E045 --module src.models.union_retrieval --compare E041 --case household --schemas unhcr --output-dir docs/analysis/E045-outputs
.venv/Scripts/python.exe scripts/assemble_e045.py
.venv/Scripts/python.exe scripts/verify_daily_retrieval.py --experiment E045 --date 2026-09-21 --output-dir docs/analysis/E045-outputs
```

Frozen baseline caches are reused only if both the frame hash and pinned
snapshot hash match. Cached baseline timings are historical. New source caches
bind the complete local source tree; changing that tree invalidates them.
