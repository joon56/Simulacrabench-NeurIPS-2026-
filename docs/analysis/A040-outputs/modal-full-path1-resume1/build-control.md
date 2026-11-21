# A040 resume1 — BUILD_BUDGET_CONTROL_UNRESOLVED

Decision before any remote resource request. The required whole-preparation bound
of USD1 is not established. Do not build, transfer, allocate H100, or execute models.
This is an evidence/control gap for this recipe, not proof that Modal is incapable.

## New facts and source trace

Authenticated workspace joon56; default environment main; image builder2025.06.
Normal SDK billing summary reports October metered/billed0. EnvironmentGetBudget
returned PermissionDeniedError. That does not prove a particular permission or
plan cause. Remaining credits and workspace gross/net limits are not independently
visible in the successful summary. Applied credits0 is not remaining credits0.
No settings changed. See account-read.json.

Installed SDK1.6.0 source review (paths relative to its site-packages/modal):

- `_image.py:2694`: run_function forwards cpu/memory/timeout to
  `_Function._from_local(is_builder_function=True)`. `_functions.py:1171` and
  `_resources.py:10` carry tuple request/maximum fields into the Function proto.
  Thus the earlier uncertainty about client-side tuple forwarding is resolved by
  source reading; no server enforcement test was run. Public run_function types
  still advertise scalar soft requests. It exposes neither retries nor a whole
  image lifetime/startup_timeout setting. Generic guide wording about any Function
  kwargs does not override this installed signature.
- `_image.py:2170`: builder2025.06 with from_registry, no add_python and no setup
  commands can reduce the base definition to FROM alone. It avoids extra setup RUN
  layers, but still requires registry import through ImageGetOrCreate. No exact
  Python3.13.14 Linux image digest or dependency resolution was acquired.
- `_image.py:653-805`: context/dependency resolution and ImageGetOrCreate precede
  the asynchronous build-result join. Image/ImageGetOrCreateRequest fields have
  no aggregate dollar/resource-time/cancellation bound. This is a finding about
  the inspected interface, not all provider internals.
- `_image.py:447`: ImageJoinStreaming uses55s polls; its three-error retry limit
  applies to fetching logs. It does not bound remote build attempts or total time.
- `cli/app.py:370-408`: AppStop is a real stop operation; runner.py handles client
  disconnect. Neither inspected path establishes a numeric whole-build billing
  cessation bound covering registry pull/snapshot services. No stop RPC was sent.

Official [timeouts](https://modal.com/docs/guide/timeouts) distinguish execution
attempts from startup/scheduling and permit timing overrun. [Preemption](https://modal.com/docs/guide/preemption)
documents automatic Function restart; exact builder retry accounting remains
unconfirmed. Do not equate retries0 or client wait timeout with whole-work cost.

## Routes assessed, without resource creation

1. Plain pip_install/run_commands chain: lacks exposed whole-builder resource and
   time caps. A shell timeout covers its child command only. Rejected for this gate.
2. FROM-only fixed base plus one capped run_function installer: client tuple path
   exists. Single installer economics are small, but pull, startup, snapshot,
   server retry multiplicity and cancellation tail lack a combined bound.
3. CPU preparation Sandbox plus filesystem snapshot: CPU Sandbox lifetime can
   cover installation inside that container. It still needs an initial image,
   and snapshot/retention/transfer costs must be covered. Snapshot API timeout
   cannot be treated as a documented cap for the whole external billing path.
   [Snapshot docs](https://modal.com/docs/guide/sandbox-snapshots) describe TTL and
   deletion; this does not itself establish USD1 preparation coverage.

A locally built registry image likewise still requires Modal import and a fixed
Linux artifact; it is not an evidenced zero-cost escape. No registry account,
new provider, Docker install, build, or download was attempted.

## Explicit cost obligation

For sequential stages j, the needed bound is:

`Cprep <= sum_j (N_j * T_j * (p_cpu * CPUmax_j + p_ram * GiBmax_j))
         + Cpull + Csnapshot + Ctransfer + Cretention + Ccancel <= USD1`.

N includes automatic retries; T includes separately billable startup, live idle
and termination tail. A common absolute deadline in installer code cannot bound
work performed before it starts or after it exits. Unknown terms stay unknown.

Illustrative partial arithmetic only, using [published pricing](https://modal.com/pricing):

- One Function attempt,1 physical core/8GiB, assumed600s execution plus600s
  startup: `(0.0000131 + 8*0.00000222)*1200 = USD0.037032`.
  This is not a complete bound: repeat count, snapshot and cancellation excluded.
- One CPU preparation Sandbox,1core/8GiB/1800s:
  `(0.00003942 + 8*0.00000667)*1800 = USD0.167004`.
  Initial image import and external snapshot charges are not proved covered.
- Prior conditional H100 contract retained: USD2.965933453125 for2400s at
  original CPU/RAM caps. Adding preparation1 and shutdown/other reserve1 gives
  USD4.965933453125. This arithmetic is conditional, not posted usage or PASS.

The unassigned preparation difference (e.g. USD0.832996 for route3) is a margin,
not evidence that unknown terms fit. The separate USD1 shutdown reserve cannot
silently replace the USD1 preparation rule. No account-specific rate verified.

[Budgets](https://modal.com/docs/guide/budgets) describes workspace usage/spend
limits; the user-reported usage30 is not a per-task1/5 cap. Environment budgets
are documented for Team/Enterprise and do not cover all invoice components.
No budget lowering/raising, plan upgrade, environment creation or account-wide
settings workaround was performed. A monitored dashboard balance is not the
requested resource/time control.

## Required control and stop procedure

Before a future request, obtain provider-backed coverage for the missing terms:
which image import/layer/snapshot stages are billed; resource maxima; aggregate
attempt limit; server-enforced total lifetime; and maximum post-cancel liability
or equivalent bounded charge. Agent integrates those facts into the inequality;
user is not asked to design a builder. A provider's generic speed claim is insufficient.
Any inquiry requires separately authorized contact; none sent here.

If these facts establish a recipe: freeze all source/image/pins, record local
request intent, capture app/image/task IDs as returned, issue each approved request
once, monitor against the absolute task and budget deadlines, stop exact owned IDs
on first fault, confirm terminal state and reconcile posted usage. Ambiguous RPC
response permits lookup/cleanup only. This procedure remains a specification;
without a bounded cancellation tail it is not an implemented cost guarantee.

Current action: no remote creation; therefore no IDs or cancellation charges.
Return S0 with exact gap. Do not repeat unchanged searches, setup or science.
