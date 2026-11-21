# A040 cleanup-only closeout

**STOP_TERMINATION_UNCONFIRMED / REMOTE_WINDOW_EXHAUSTED_BEFORE_QUERY.**
Local wrapper and SDK entry defects were repaired in this S1 under workflow r5.
The authorized single remote window expired before a query could run. It was not
reset. No new remote resource, query, termination, or billing observation.

Read receipt: S1 cleanup-only technical, workflow2026-10-05-r5, SHA256
a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23.
Ordered reads AGENTS.md, CLAUDE.md, current status, newest3 log entries, workflow,
then s0-query-contract-review amendment/base scope/decision. Entry tools61c339/
9aca66 and entry.json retain evidence. Current user's r5 resumption permits routine
in-scope corrections, not timer renewal or production-controller work.

Actual SDK timeout/retry rejection reproduced with transport0. Corrected calls
pass retry=None. Fixed protobuf cases cover identity/ambiguity/unknown status,
V1/V2 wait/termination/auth, max1 termination, timeout/cancel and retained terminal
evidence on billing failure. See regression-history.md for the20-case evidence
limit and test-double correction; do not interpret as20 separately saved PASSes.

First live helper at12:14:19.5405169Z failed in0.756681s before Query.run: the SDK
synchronizer rejected a bound method. The missing CLI-boundary check was an agent
implementation error, not an account/service/model verdict. A plain async wrapper
fix was reproduced and validated locally (ENTRY_DISPATCH_PASS, exit0). At attempted
continuation, less than the reserved30s remained; parent refused before launch.
The original outer deadline12:16:19.5405169Z stayed fixed. No second live process.

Exact target remains workspace joon56/main, App ap-XiMVzlJgrNrCiFpIN1kB4W,
Sandbox name a040-resume5-20261005-094405-gpu. ID and terminal result unknown.
Historical App STOPPED/task0 is not fresh Sandbox evidence. Final attributed cost
also unknown. closeout-terminal-status.json is an administrative record, not a
fabricated SDK receipt. No termination-billing-receipt.json was produced.

Original source.diff/pre-remote-freeze/window/live failure are preserved. The first
helper is reconstructed from the saved diff and matches its frozen SHA; separate
entry-repair.diff shows the later correction. No production12 changes. Local
checks used3.1790341s total, four children, CPU2/GPU0; cumulative preparation and
science remain separate in cost-time-ledger.json. No new remote charge observation.

Return to S0 for the remaining exact-resource evidence decision. Existing window
is closed; no automatic cleanup retry, production lifecycle repair or new H100 run.
Evidence may be obtained from the exact official detail screen, or a separately
authorized metadata-only allowance using reviewed helper/entry boundaries.
Any next scope must preserve old failures, no new resources and max1 needed
termination after exact identity/running confirmation. No S2/release qualification.
