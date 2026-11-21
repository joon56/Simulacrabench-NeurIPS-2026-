# A040 S0 — bounded Modal H100 handoff

2026-10-02 KST. **HANDOFF_READY; H100 execution not started or qualified.**

Main: one separate S1 technical attempt on Modal, with preparation and resource
enforcement before fresh reference/candidate processes. Backup: a specific-input
or technical-failure closeout, including termination and cost reconciliation.
No alternate model, provider search, automatic retry or S2 work.

## Decision and authority

The user created a Modal account, registered a payment method and supplied a
Starter screenshot showing $30 credits, $0 spend and a $42.50 usage limit.
After instructions to set spend limit $0 and usage limit $30, the user reported
confirmation. The final settings have **not** been independently inspected.
No actual GPU allocation, available quota or target environment is verified.

Following the proposed first-attempt ceiling of $5 credits, the user said:
“그럼 이제 H100사용할 수 있게 되었으니까 작업 진행하자.” This supports preparing
the bounded next task. It does not override the standing separate-session rule.
The [S1 prompt](s1-modal-full-path.ko.md) becomes the execution instruction when
the user delivers it to S1; writing it here does not launch that session.
Modal access replaces the previously missing provider choice, not the historical
Lambda investigation or its verdict. Existing installation/rule resolutions stand.

## Why this work

The fixed RTX3070 candidate reached its900s cap before completing the final
expert. Reference and partial controls passed; model feasibility on H100 remains
unknown. A complete bounded target run can settle an actionable engineering
question before further candidate/release investment. Another unchanged local
run cannot answer it; model/context reduction would be a different intervention.
There is no quantified winning probability, expected score gain or H100 speedup.

The hypothesis still has weak efficacy evidence. Fake S/E acceptance establishes
procedure execution only. Spending a small capped amount to resolve feasibility
is justified; consuming all $30 or launching a search is not. Failure closes this
attempt. Success returns to S0 with deployment/release and efficacy gaps intact.

## Prospective target contract

Use a one-shot Modal Sandbox, H100 explicitly (no automatic H200 substitution),
one GPU, two model threads/logical CPUs, one physical CPU request/hard cap.
Document actual affinity, quotas and GPU allocation; no MIG/shared assumption.
Native outbound blocking precedes scientific imports. A local durable launch
record prevents ambiguous remote-call failures from causing a second launch.
Do not treat Function retries=0 as protection against platform crash restarts.

This is a new Linux resource contract, not proof of Windows memory equivalence:
container memory request/hard cap15258MiB =15,999,172,608bytes, no swap;
measure whole-container and owned-process RSS/private accounting separately.
The original Windows private-commitment16GB result remains unchanged. Do not
call Linux RSS/cgroup usage Windows private commitment. If the target cannot
enforce or expose the required boundary, close before scientific execution.

Fresh reference then candidate, once each, each900s including import/load/all3/
validation/output; no partial-state continuation. GPU container lifetime<=2400s,
total task<=120min, preparation<=60min, new model-free port checks<=60s cumulative.
Caps are ceilings, not extra runs. Actual target CPU/memory semantics and all
environment differences are frozen before import, not selected after results.

## Cost and shutdown

All-in task cap **USD5 of included credits; USD0 cash charges**. No purchase,
subscription upgrade, additional credits or higher account limits. Existing user
confirmation is carried forward; S1 checks accessible billing state for mismatch.
If authentication needs user interaction, request that action only; never tokens.

At consulted list prices, one H100 + one physical CPU +15258MiB in Sandbox costs
about$0.001236/sec, or$2.97 for2400s. This is a resource-rate illustration, not an
invoice or a measured runtime. Sandbox CPU/RAM pricing differs from Functions.
Allow at most$1 for preparation/build/transfer and reserve$1 for shutdown, billing
uncertainty and other accounted overhead. Freeze an upper-bound ledger before
remote work; reduce the allowed window if needed. No premium region, nonpreemptible
premium, parallel container or unbounded build. Insufficient cost control means
HOLD before spending, not a larger budget. A delayed dashboard is not a cost guard.

S1 owns stopping and verifying its exact Sandbox; the account owner is fallback
if authentication/connectivity prevents it. Save remote IDs immediately, export
logs while alive, terminate and confirm terminal state/remaining workloads.
Retain a billing reconciliation item if posted usage lags. Process exit alone
does not prove the remote container stopped. Do not leave a detached service.

## Evidence and preservation

Read AGENTS/CLAUDE/status/newest3log/workflow, resource-feasibility records,
full-path-resume1 closeout/input-reuse/registration and official Modal docs.
Workflow2026-09-27-r4; actual read evidence and selected hashes in
[verification](verification.json). HEADa43f4379ec78dbc2de260463eef67bb1d567d7e1.
Only this S0 directory and additive status/log are written. No scientific input,
checkpoint, old output/cache, protected response or key read/hash; no imports,
tests, login, install, transfer, paid operation, fit/predict/score, ZIP or git write.
Named Python/pythonw/uv query returned no rows; not an exhaustive job audit.

E041 incumbent/E025 fallback; E057/E060/E061 parked; E058 STOP/E059 STOP_SELECTION
and all STOP/HOLD preserved. A039 separate; A_half not promoted; A018 user-unconfirmed;
S3 stopped/S2 none. Exposure17999people/12339SSUID, aggregates/A022 original roles,
E059 consumed oracle1918/1124 and selection2007/1130, protected audit2074/1177 and
calibration1866 remain unchanged. These restrictions also apply to the S1 prompt.

## Official sources consulted

- [Pricing](https://modal.com/pricing): H100$0.001097/s; Sandbox physical CPU$0.00003942/s/core and memory$0.00000667/s/GiB. Starter included credits; no guaranteed task cost.
- [Budgets](https://modal.com/docs/guide/budgets): usage and net spend limits differ. Account-specific settings still require confirmation.
- [GPU](https://modal.com/docs/guide/gpu): H100! prevents the documented H200 auto-upgrade.
- [Sandbox resources](https://modal.com/docs/guide/sandbox-resources): physical cores, MiB, request/limit pairs and billing by higher requested/actual consumption.
- [Sandbox lifecycle](https://modal.com/docs/guide/sandboxes): lifetime, exec and terminate; GPU uses gVisor. No nested VM/cgroup capability assumed.
- [Network boundary](https://modal.com/docs/guide/sandbox-networking): block_network prevents outbound traffic. S1 must verify its actual configuration and native probe.
- [Retries](https://modal.com/docs/guide/retries): Function crash rescheduling is distinct from exception retry configuration.
- [Sandbox API](https://modal.com/docs/sdk/py/latest/Sandbox): explicit lifetime/resource/network parameters. Freeze actual SDK compatibility in S1.
- [Resources](https://modal.com/docs/guide/resources) and [timeouts](https://modal.com/docs/guide/timeouts): do not rely on default bursting or timeout assumptions.

These documents support platform design choices, not observed target behavior.
