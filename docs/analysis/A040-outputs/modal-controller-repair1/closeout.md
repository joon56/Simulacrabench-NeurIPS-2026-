# A040 local controller repair — LOCAL_CONTROLLER_CONTRACT_PASS

2026-10-04 KST. S1 technical, local only. Return to S0; no remote retry authorized.

Original cp949/U+2022 failure reproduced. Repaired launcher preserves UTF-8 bullet,
Korean, exceptions and JSON in pipes and redirected files. Controller now bounds
cancellation/stop/query and whole cleanup, captures failures before the old try
boundary, preserves owned IDs and distinguishes ACK from terminal+task0. Hard
watchdog also bounds a blocked event loop. No create/build/stop retry was added.

Corrected focused suite15/15 PASS; separate actual SDK `_call_safely` AST checks
PASS. First suite failed on a new fake logger argument collision; failed source,
traceback and result are preserved. Minimal metadata-key repair preceded suite2.
Four measured top-level regression invocations,6.5996745s cumulative (limit120s).
No redundant successful suite repeat. Scientific/Linux60s allowance untouched.
Entry/deadline, active time and prior3312.1552137s accumulation: `verification.json`.

Real remote/account calls, SDK/model imports, protected/staging reads or hashes,
fit/predict/score and GPU work:0. Fake IDs only. Network/process audit guards and
synthetic negative probes accompany fake transport traces. This is not network
packet capture. No original remote App was re-queried or stopped. Existing work
and ten named historical artifact hashes preserved. HEAD remains
a43f4379ec78dbc2de260463eef67bb1d567d7e1; no commit/push.

The actual installed SDK source identifies loop mismatch as its warning condition;
the historical hang's exact cause remains unproven. The repaired adapter was
tested with async SDK-shaped mocks; no live SDK binding/server behavior was
validated. Private API compatibility, actual remote cleanup, complete dependency
image, H100900s, scientific effect and release remain unverified. Installer source
and image recipe preserved; real34 pins/staging/model were deliberately unopened.

See `diagnosis-and-contract.md`, `cleanup-state-table.md`, `source.diff`, hash
manifest, `regression-evidence/`, and `s0-handoff.ko.md`. Next action: S0 review of
the local repair and whether a separate bounded remote handoff is justified.
Local PASS does not authorize any remote run, S2/ZIP, S3/TEST or adoption.

Monitored USD1/5 planning/cash0 amendment retained. No new billing reading; old
summary0/component0.00001152 and unknown final attribution remain. E041/E025,
parked E057/E060/E061, every STOP/HOLD/exposure boundary, A_half nonpromotion,
A018 unconfirmed/S3 stopped/S2 none unchanged.
