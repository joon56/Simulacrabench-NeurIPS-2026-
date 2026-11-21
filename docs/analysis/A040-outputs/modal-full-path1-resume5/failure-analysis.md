# Resume5: Sandbox handle failure after create response

2026-10-05. **REMOTE_PREPARATION_FAIL / SANDBOX_HANDLE_LOOP_MISMATCH**.
Raw outcome: STOP_FIRST_ERROR. Termination: UNCONFIRMED. No repair/retry.

Observed: normal workspace/base gates passed; one image recipe completed as
`im-XZ95GDfkfa6PwWUeFyciYM`. Builder imported controller_core and ran the fixed
installer. Its pip inventory is preserved. Local payload verification accepted
112+12files/145605744bytes. At09:50:40.905Z sandbox_create began; first error
09:50:41.982Z. No Sandbox payload transfer/boundary/scientific command followed.

Source-supported diagnosis (read-only installed SDK1.6.0 inspection):

- live_binding.py binds raw `_Sandbox`; live_launcher.py runs a new asyncio loop.
  Endpoint.connect verifies its raw client's loop, not stream constructor loops.
- sdk_endpoint.py:57 awaits raw Sandbox creation. SDK modal/sandbox.py:599-602
  receives SandboxCreate response, takes its ID and calls _hydrate. At1227 the
  metadata hydrator constructs public StreamReader; modal/io_streams.py:573
  asserts running-loop equality with the synchronicity loop. Saved traceback
  fails there, before endpoint.sandbox assignment and persisted sandbox_id.
- Thus a create response was received. Sandbox allocation/GPU cost cannot be
  counted as zero. Actual Sandbox ID/hardware/scheduling/terminal state is unknown.
- Cleanup name recovery uses the same hydration path and also raises AssertionError.
  AppStop succeeds; repeated explicit App STOPPED(enum5)/task0 observations follow.
  Sandbox handle/returncode is absent. Cleanup60.0100353s exhausts its cap, and
  final billing cannot run. No supplemental post-cap remote operation was made.
- Prior local mount/import PASS covered that local boundary only. Actual builder
  success is new evidence; this downstream failure supplies no model/H100 outcome.

Owned resource: workspace joon56/main; App `ap-XiMVzlJgrNrCiFpIN1kB4W`, name
`a040-resume5-20261005-094405`; Sandbox name
`a040-resume5-20261005-094405-gpu`, ID unavailable. App terminal observed;
**Sandbox terminal UNCONFIRMED**. User promptly notified to locate that exact
Sandbox and confirm terminal state, terminating only it if live. Client exit1/
App ACK/task0 is not substituted for the missing Sandbox observation.

Cost limitation: fixed GPU accounting starts only after handle return. Raw
management0.6550409048674121USD omits any allocated Sandbox time. Session ledger
therefore keeps raw evidence and a separate full2400s Sandbox planning reservation.
This is not measured GPU time or actual charge. Raw posted_evidence0.00178978USD
is the maximum of observed metered summary/breakdown totals, not an attributed
invoice. Final billing is absent. No actual final cost or termination guarantee.

Next S0 decision: resolve owned terminal/billing evidence and assess a separate
bounded local create/recover/stream-boundary investigation. No new repair, retry,
budget, model/policy or role transition is authorized by this closeout.
