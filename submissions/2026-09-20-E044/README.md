# E044 conditional weight-use control

Archive: [2026-09-20-E044.zip](../2026-09-20-E044.zip).
Purpose: one UNHCR-only informational A/B against E041's .64/.52/.49/.92.
**Reported result: Grand .63, no best update; individual scores unavailable.**
E044 is rejected for adoption; E041 remains DEV best.
Technical validation: ZIP checker PASS, official phase-1
PASS x3, every-vector source/archive parity exact, clean no-regression versus
E041 and E025. Official local runtime totals 371.022 s. Consult
[SCORES.md](SCORES.md) for preregistered interpretation and all measured results.

E041 fitting, section activation, candidate identities, K=32 and lambda
procedure remain. Only learned section weights in replay/final evidence are
replaced with the initial common weights. Changed lambda values are an
intended downstream effect. This is conditional on the learned activation
mask and therefore does not remove all supervision.

The preregistered .63 adverse arm applies. Removing learned weight use was
unfavourable in this displayed reading; retain E041's learned weights. The
single rounded/noised result does not identify an exact UNHCR score or isolate
the weights from downstream recalibration. Result source is the user report;
no independent platform fetch or new upload was performed by this record update.

Source implementation copies E041's layer function binding and overrides only
evidence construction; parent function bindings are unchanged. The in-memory
diagnostic dictionary is shared, but does not affect prediction decisions or
write diagnostics outside the runner. The submission uses an equivalent
appended function override on the immutable E041 main.py prefix.

Rebuild: `.venv/Scripts/python.exe scripts/assemble_e044.py`.
Official verification: `.venv/Scripts/python.exe scripts/verify_daily_retrieval.py --experiment E044`.
Source caches required by verification are produced by `scripts/check_daily_retrieval.py`.
Exact reproduction commands and results are in the experiment record.
