# B01 exact execution commands (consumed stages, not permission to repeat)

All from repository root, existing Python only; monitor starts before numerical
imports. New commands use saved local code, not old S1 runners.

```powershell
& .venv/Scripts/python.exe -X utf8 -B docs/analysis/E064-outputs/s2/release.py run tests
& .venv/Scripts/python.exe -X utf8 -B docs/analysis/E064-outputs/s2/release.py run preflight
& .venv/Scripts/python.exe -X utf8 -B docs/analysis/E064-outputs/s2/release.py run preflight2
& .venv/Scripts/python.exe -X utf8 -B docs/analysis/E064-outputs/s2/release.py run assembly
& .venv/Scripts/python.exe -X utf8 -B docs/analysis/E064-outputs/s2/release.py run evaluate
& .venv/Scripts/python.exe -X utf8 -B docs/analysis/E064-outputs/s2/release.py run package
& .venv/Scripts/python.exe -X utf8 -B docs/analysis/E064-outputs/s2/release.py run official
```

`preflight` is the preserved failed attempt; `preflight2` is its affected retry.
Later commands are planned until their resource and completion receipts exist.
No overwrite/repeat of a successful stage. Entry/release-freeze identify exact code,
inputs, output paths, environment and historical receipts. Official driver commands
and captured logs appear in official stage artifacts. Shared official900s includes
three CLI parents/drivers plus import/startup/output/driver overhead.

Stock checker is invoked inside package stage against actual ZIP. It has a tiny
two-visible-row no-neural/optimizer smoke call, counted separately from all3 fits.
No additional parity-only scientific execution. Prior S1 commands remain consumed.
