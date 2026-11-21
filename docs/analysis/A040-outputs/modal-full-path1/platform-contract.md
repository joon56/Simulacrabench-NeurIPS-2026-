# Modal platform and cost preflight — preparation in progress

Read-only official documentation and installed Modal1.6.0 source,2026-10-02 KST.
This record is not boundary PASS, remote allocation evidence or a frozen run image.

| Condition | Evidence | Current status |
|---|---|---|
| Explicit H100, no H200 upgrade | [GPU guide](https://modal.com/docs/guide/gpu), H100! | Supported published selection; not allocated |
| CPU physical request/hard cap and MiB memory tuple | [Sandbox resources](https://modal.com/docs/guide/sandbox-resources); Sandbox.create SDK source | Named parameters exist; enforcement/affinity/swap not observed |
| GPU gVisor | [Sandbox lifecycle](https://modal.com/docs/guide/sandboxes) | Published runtime restriction; no nested-cgroup assumption |
| Outbound block before import, no tunnels/secrets | [Network guide](https://modal.com/docs/guide/sandbox-networking); SDK create | block_network and empty ports/secrets supported; native boundary untested |
| Lifetime/exec/terminate | [Sandbox API](https://modal.com/docs/sdk/py/latest/Sandbox) |2400s lifetime possible; no process or remote ID created |
| Spend vs usage | [Budgets](https://modal.com/docs/guide/budgets) | Spend is net of credits; usage gross. User report remains unverified until authentication |
| GPU/CPU/RAM rates | [Pricing](https://modal.com/pricing) | GPU.001097/s; Sandbox core.00003942/s; GiB.00000667/s; base region only |
| Build is separate preparation | [Images](https://modal.com/docs/guide/images); installed SDK _image.py | Whole preparation cost/cancellation not yet bounded |

SDK source facts: Sandbox.create constructs one SandboxCreate request, hydrates its
ID, then waits for scheduling; on scheduling failure it tries termination. This is
not an exactly-once end-to-end proof. Durable local request intent must precede the
call; record returned ID immediately, forbid reissue on ambiguous response, query
existing tagged/named resource and clean up. Remote atomic mode latch must precede
scientific spawn. Function retries=0 alone is insufficient. No controller implemented
or tested yet, no latch consumed.

Image.run_commands exposes commands/env/secrets/volumes/GPU/force_build, without a
public CPU/memory hard-cap or whole-builder timeout parameter. Image.run_function
has a step timeout and documented soft CPU/memory requests; its underlying
_Function supports request/limit tuples, but that fact alone is not a verified
whole-image cost cap. Base registry pull, layers, rescheduling and cleanup need
accounting. ImageGetOrCreate Image metadata has no simple whole-build budget field.
No assertion that every Modal build is unbounded or that no solution exists.
This session has not established the bounded recipe required by the USD1 gate.
Do not launch a build on the assumption that it is free or finishes quickly.

Prospective resource arithmetic: rate0.00123580560546875USD/s;
H100 lifetime2400s costs at most2.965933453125USD if the stated caps/rates hold.
Adding preparation1 and reserve1 gives4.965933453125USD, not a posted charge.
No chosen-region premium or non-preemptible execution. Remaining free egress,
account-specific rates and other concurrent usage remain unverified.

Normal SDK profile listing returned[] twice. User was asked to run the isolated
SDK's normal `modal setup` browser flow and confirm workspace/billing controls.
No raw config/token reads, other credential search or remote call was attempted.
After authentication, use normal profile/workspace and billing read APIs with
restricted output; do not dump tokens or account environment variables.

Future port scope remains new-copy paths/GPU assertion/POSIX watchdog and metrics,
one fresh target reference/candidate, full assertions. Frozen Linux dependency
resolution, image identity, actual quota/memory/network boundary, build controls
and once-only controller are unfinished. Original scientific modules are unchanged.
