# Local repair contract — before regression

Authority: latest user request plus s0-modal-logging-review handoff. S1 technical.
Entry 2026-10-04T12:02:45Z; hard task deadline12:32:45Z. Local sequential regression
subprocess wall cumulative<=120s; one suite<=45s. No models, SDK import, account or
network calls. Existing SDK1.6.0 source only; injected fake SDK-shaped transport.

First reproduce U+2022 cp949 failure. Then verify the repaired launcher/controller:
UTF-8 stdout/stderr and exception/result in both pipes and files; success; Unicode
failure; cancellation-resistant task; stop timeout/failure; ACK/running; stopped
with nonzero tasks; stopped+zero tasks; lost create response; pre-build failure;
query timeout; event-loop blocking watchdog. One create/build/stop maximum per
controller; ID unknown never causes discovery/recreate. No automatic request retry.

Fixture phase timeout0.12s, cancellation grace0.03s, cleanup total0.35s; parent
watchdog3s (blocking-case1s). These are model-free regression scales, not future
remote execution policy/deadlines. Preserve original installer function and image
recipe; pass requirements/deadline explicitly, never read34 pins or112 staging.

Only complete named local contracts permit LOCAL_CONTROLLER_CONTRACT_PASS. Failure
or missing evidence gets exact closeout. Expected-error cases and repairs allowed
inside120s; no redundant successful repeats. Prior active3312.1552137s remains.
Historical scientific/Linux60s budget unchanged. No remote/release qualification.
