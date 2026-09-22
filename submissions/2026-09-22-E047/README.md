# E047 - Query-adaptive final evidence

Status: **technically ready for exploratory submission #28; no hosted upload.** Archive:
[2026-09-22-E047.zip](../2026-09-22-E047.zip).

Sixteen tests, ZIP checker and official phase1 all3 PASS. Clean probabilities
exactly E041; source/archive parity0 for both clean and actual active-household
cases. Official combined CPU time515.180s against900s shared budget. Scores
and hashes: [SCORES.md](SCORES.md), [verification.json](verification.json).

Keep E041 as the first-stage model. On UNHCR only, predict a section-specific
extra evidence share for each respondent from label-free confidence and
agreement features. The share is at most .5 and acts after the existing final
gate/evidence prediction. Separate correction-fit, selection and audit rows
are masked before every shadow first-stage fit. Rejected corrections return
exact E041. UNICEF and WB use E041 unchanged.

E046's prior tree screen failed its preregistered oracle gate; no E046 model
or submission was made. E047 is separately registered and has a different
adaptive family. Its observed oracle passed, but actual learned gains were
small/inconclusive: seed47 +.000274 skill, seed48 fallback0. No .65 forecast
or local model adoption is claimed. The scorecard contains hosted readings
registered before submission and the complete technical results.

No external records, fitted external parameters or extra dependencies are
bundled. The existing UCI Adult data is used only for offline screening and
disclosed in [SCORES.md](SCORES.md). E041 stays DEV incumbent at
.64/.52/.49/.92; E025 stays the separately validated phase2 fallback.

Reproduce from the repository root:

```powershell
.venv/Scripts/python.exe scripts/oracle_e046.py
.venv/Scripts/python.exe scripts/oracle_e047.py
.venv/Scripts/python.exe scripts/evaluate_e047_observed.py
.venv/Scripts/python.exe -m pytest tests/test_adaptive_final_evidence.py tests/test_e047_assembly.py -q
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E025 --snapshot submissions/2026-09-09-E025/main.py --output-dir docs/analysis/E047-outputs
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E041 --snapshot submissions/2026-09-19-E041/main.py --output-dir docs/analysis/E047-outputs
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E047 --module src.models.adaptive_final_evidence --compare E041,E025 --output-dir docs/analysis/E047-outputs
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E041 --snapshot submissions/2026-09-19-E041/main.py --case household --schemas unhcr --output-dir docs/analysis/E047-outputs
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E047 --module src.models.adaptive_final_evidence --case household --schemas unhcr --compare E041 --output-dir docs/analysis/E047-outputs
.venv/Scripts/python.exe scripts/assemble_e047.py
.venv/Scripts/python.exe scripts/verify_daily_retrieval.py --experiment E047 --date 2026-09-22 --output-dir docs/analysis/E047-outputs
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E047-assembled --snapshot submissions/2026-09-22-E047/main.py --case household --schemas unhcr --compare E041 --output-dir docs/analysis/E047-outputs
.venv/Scripts/python.exe scripts/check_e047_active_parity.py
```

Baseline caches are reused only when current input and pinned snapshot hashes
match; cached timings are historical. New source caches bind every local src
Python dependency. Verification uses extracted ZIP bytes and the official
three-schema scorer, then compares every output probability with source.
