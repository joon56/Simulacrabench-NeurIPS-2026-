# Cleanup continuation contract

Authority: current user's explicit continuation; S0 cleanup-time-budget-continuation,
workflow2026-10-05-r5. Overall12:37:44Z to13:07:44Z; operational cutoff13:02:44Z.
This is new existing-resource cleanup allowance only. Historical windows unchanged.

The reviewed helper is copied byte-for-byte under original/. Its main, old window
and latch are not called. attempt.py imports Query/execute_on_sdk_loop and supplies
only this attempt's remaining deadline and save callback. Normal metadata identity,
version/status interpretation and terminate decision remain the reviewed Query body.
The callback persists one exclusive shared termination intent before any potential
mutation and separately preserves the first exact-ID terminal evidence.

runtime.py launches one hidden CPU2 child per explicit invocation. Immediately
before launch it freezes source hashes and the remaining allowance. Monotonic time
from before Popen through child reaping is charged, including import/auth/wait/cancel.
One second within the allowance is withheld for exit/reaping. Local work between
children remains in the30min task budget, not in the120s child allowance. Parent
state with an unclosed child blocks another launch. No automatic retry loop.

Original Query reserves30s for evidence. With<=30s remaining, full helper is denied;
only prior exact-ID read-only confirmation can start. Any recorded/possible
termination prevents full reentry; ReadOnlyQuery cannot call termination/discovery.
That optional read-only branch is source reviewed here; its actual SDK execution
is untested unless a later recorded attempt uses it. Original successful suites
are not repeated. Inspect receipt/failure/child exit before any in-scope repair.

New focused checks7 cover cumulative subtraction, idle exclusion, reserve exhaustion,
unclosed child rejection, durable single intent, possible mutation barrier, actual
child lifetime and timeout termination. These are stdlib timing/protocol checks,
not scientific or remote-success evidence. The initial absent implementation
assertion is preserved as the red check. No model/auth/network in these checks.

No new resource/build/GPU/science/controller repair/model/data access, commit/push,
S2/S3. Explicit exact-ID terminal is required; App state/absence/time do not suffice.
Billing remains optional after terminal and is a workspace aggregate with posting/
attribution uncertainty. Return to S0 after evidence or exact bounded failure.
