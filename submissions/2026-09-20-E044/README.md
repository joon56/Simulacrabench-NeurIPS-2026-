# E044 conditional weight-use control

Archive: [2026-09-20-E044.zip](../2026-09-20-E044.zip).
Purpose: one UNHCR-only informational A/B against E041's .64/.52/.49/.92.
**Ready for one exploratory submission:** ZIP checker PASS, official phase-1
PASS x3, every-vector source/archive parity exact, clean no-regression versus
E041 and E025. Official local runtime totals 371.022 s. Consult
[SCORES.md](SCORES.md) for preregistered interpretation and all measured results.

E041 fitting, section activation, candidate identities, K=32 and lambda
procedure remain. Only learned section weights in replay/final evidence are
replaced with the initial common weights. Changed lambda values are an
intended downstream effect. This is conditional on the learned activation
mask and therefore does not remove all supervision.

This file tests a mechanism, not a demonstrated path to .65. If the score
drops, retain E041; if it stays at .64 without update, the effect is unresolved
at leaderboard resolution. Any new best is inspected and preserved. No upload
has been performed as part of preparation.

Source implementation copies E041's layer function binding and overrides only
evidence construction; parent function bindings are unchanged. The in-memory
diagnostic dictionary is shared, but does not affect prediction decisions or
write diagnostics outside the runner. The submission uses an equivalent
appended function override on the immutable E041 main.py prefix.

Rebuild: `.venv/Scripts/python.exe scripts/assemble_e044.py`.
Official verification: `.venv/Scripts/python.exe scripts/verify_daily_retrieval.py --experiment E044`.
Source caches required by verification are produced by `scripts/check_daily_retrieval.py`.
Exact reproduction commands and results are in the experiment record.
