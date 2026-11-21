# C1 - execution versus imports/managed loop
Before either invocation. Hypothesis: execution of the builder path is needed;
fixed imports, guard, SDK and loop entry alone will exit normally.
Single changed boundary: omit production execution after imports, enter the same
SDK synchronizer with a trivial coroutine instead.
Arms: c1-baseline builder_fail; c1-loop import_loop. Expected: baseline native
failure and loop exit0 localizes downstream; both fail localizes import/loop/guard.
No RPC/auth/models. Existing short builder failure only, not success/stall.