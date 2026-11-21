# Commands and replay boundaries

Executed in C:\Users\USER\Desktop\SimulacraBench using existing SDK venv Python.
No install, SDK import, live transport or model input is needed. Existing result
paths are exclusive: never overwrite or rerun into suite1/suite2. Commands below
document executed work, not automatic authority for a new session.

```powershell
& 'tmp/a040-modal-full-path1/sdk-venv/Scripts/python.exe' -X utf8 docs/analysis/A040-outputs/modal-controller-repair1/reproduce.py
& 'tmp/a040-modal-full-path1/sdk-venv/Scripts/python.exe' -X utf8 docs/analysis/A040-outputs/modal-controller-repair1/tests_local.py tmp/a040-modal-controller-repair1/suite2
& 'tmp/a040-modal-full-path1/sdk-venv/Scripts/python.exe' -X utf8 docs/analysis/A040-outputs/modal-controller-repair1/check_sdk_contract.py
```

Suite processes were launched with hidden Windows Start-Process and a45s outer
watchdog. Launcher gives each fake worker3s (blocked-loop case1s), kills only its
own worker, and bounds post-kill communicate2s. Whole measured regression includes
the expected original error and failed suite1; raw time receipts run1..run4 kept.
The now-existing suite2 path intentionally makes the displayed command refuse
overwrite. Future authorized reproduction needs a new output path and its own cap.
