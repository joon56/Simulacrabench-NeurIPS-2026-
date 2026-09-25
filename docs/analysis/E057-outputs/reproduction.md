# E057 reproduction and verification

Run from repository root in PowerShell using the existing `.venv` environment.
Python/package versions and exact source/input/cache hashes are in
`preflight.json`. Baseline is `submissions/2026-09-19-E041/main.py`; no package
or environment was changed. Execution code was frozen at `e51b29f` after
registration commit `592da4c` (input HEAD `9284bf4`).

Commands actually used, in order:

```powershell
.venv/Scripts/python.exe -m pytest tests/test_e057_conditional_content.py -q
.venv/Scripts/python.exe -c "from scripts.check_e057 import MemoryTree; import os; print(MemoryTree(os.getpid()).sample())"
.venv/Scripts/python.exe scripts/check_e057.py preflight
.venv/Scripts/python.exe scripts/check_e057.py run
.venv/Scripts/python.exe scripts/verify_e057.py
```

The first four commands precede any full-run result inspection. The verifier
uses frozen artifacts only: no fit, no label scoring and no alternate policy.
Preflight/run/verifier refuse their existing output paths. Preserve all original
outputs; do not delete them to rerun this experiment. A later explicitly scoped
reproduction needs a separate checkout/output root and equivalent local inputs.

Prerequisites: unchanged starter-kit source, its existing three synthetic
`_sandbox/*/respondents.parquet` files, all sources listed in the preflight,
the E054 verification manifest, and six verified clean E025/E041 phase1 pickle
references under `tmp/e043-eval/`. The cache binds schema/config/frame/cells/truth
and phase1 split, plus predictor source. Changed or absent provenance is a hard
error, not permission to reuse an approximate cache. No E056/Adult/SIPP arrays
are needed or opened. Row-level E057 outputs remain ignored under
`external/e057/`; these are required for frozen verification, not committed.

The monitored worker starts before numerical imports. Parent watchdog includes
process launch in its 900s limit; worker watchdog also caps conservative fit
wall at 1200s. Native Windows counters include worker descendants and retain OS
lifetime RSS/commitment peaks. A supplemental PowerShell monitor sums lifetime
peaks for the four observed owned Python processes (worker, launchers, harness),
with the same 8GiB limit. This sum is a conservative process aggregate, not a
simultaneous working-set estimate. Monitoring infrastructure and tool-server
memory are not model memory. Monitor failures/technical errors stop the run.

The local rehearsal injects the actual immutable E041 snapshot into the new
wrapper. Historical source-default parity is carried forward only after all
56 recorded source hashes and six cache files match. Fresh parity of the new
default module and eventual standalone assembly, ZIP checker and official
`score.py` all3 execution remain S2 work. Local metric arithmetic uses the
official `floored` and `uniform_reference`; this is not an official CLI pass.
