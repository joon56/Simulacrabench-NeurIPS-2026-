# A040 whole paid cost and proposed portability boundary

Information only. Nothing below is an executable run command or acquisition
authorization. [Options](options.md) and [source register](source-register.md).

## Cost unit and lifecycle

[D4 billing](https://docs.lambda.ai/public-cloud/billing/) specifies one-minute
increments, from launch passing health checks until provider termination, including
idle time. One minute is the published billing quantum; a separate minimum charge,
deposit/card requirement or account fee was not established. Filesystems bill used
GiB monthly in hourly increments and survive instance termination; their displayed
$0.20 example is not a verified current rate. Filesystem ingress/egress is stated
uncharged; broader transfer/third-party network charges are not established here.
Taxes depend on billing location. No account-specific total quote was obtained.

The design proposal uses listed root storage and no persistent filesystem.
Avoid interpreting that design as proof every additional storage/transfer charge
is zero; owner must confirm the selected instance quote before any launch.
If a filesystem is later requested, its tariff, retained size and deletion owner
must be added, with user approval. No automatic persistent resource creation.

Define T_paid in seconds, including paid startup, setup, install/build, weight
transfer/acquisition and verification, environment/port checks, fresh reference,
fresh candidate, output verification/export, idle and termination acknowledgment.
For one contiguous instance, planning compute cost = r*ceil(T_paid/60)/60.
This conservative minute rounding is cost arithmetic, not an authenticated invoice.
Add storage, other transfer/service charges, applicable tax and payment/FX charges.
Setup duration, available installation artifacts, effective bandwidth, shutdown
latency and those add-ons are unknown; **no total upper bound is presently known**.

| Assumed billed compute duration only | PCIe r=$3.29/h | SXM r=$4.29/h |
|---|---:|---:|
|30minutes|$1.645|$2.145|
|60minutes|$3.29|$4.29|
|120minutes|$6.58|$8.58|

These are arithmetic sensitivities using [D1](https://lambda.ai/pricing), not
budgets, setup estimates or expected runtime. Two900s scientific caps total30min
of allowed child windows; that is not the full billed session, nor guaranteed
completion. Failed preparation/runs also consume paid time. No rental return on
investment can be inferred from fake S/E acceptance.

[D6 lifecycle](https://docs.lambda.ai/public-cloud/on-demand/creating-managing-instances/)
requires provider Terminate to end instance billing; guest shutdown/poweroff may
leave it billed in Alert, and suspend is not offered. A future approved session
needs an owner/controller outside the offline scientific process, an absolute
paid deadline derived from the user's all-in spend cap with agreed reserve,
termination confirmation and a final resource/billing check. Process timeout alone
does not terminate the VM. Export/teardown must fit that deadline; failed export
cannot justify spending past it. These controls have not been configured or tested.

## Environment differences and minimum future port

This is a source-grounded technical plan; no code changed. Existing
`full-path-resume1/runner.py` and `watchdog.py` were read as text only.
The local provenance records Python3.13.14, torch2.8.0+cu126, numpy2.2.6,
pandas2.2.3, sklearn1.6.1, scipy1.15.3, psutil7.0.0 and34 frozen package versions.
The lock is a version inventory, not Linux wheel hashes. TabICL2.2.0 is source
commit0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3. Public checkpoint SHA256 remains
bdc7dbd5e4ff21f8f0456fcf90c6b7cdf72dbea960f2d05b19bec19f9b3d4ed0,
attributed to the earlier provenance; bytes not reopened now.

| Difference | Required future work before scientific invocation |
|---|---|
| Windows executable/paths and fixed ROOT layout | New isolated target paths and read-only allowlisted transfer map; preserve every original artifact/latch. No blanket workspace/cache upload. |
| Runner rejects GPU names without3070 | Explicit new H100 assertion, exact selected variant/UUID and one whole GPU; no generic bypass. |
| Windows Python binaries vs Linux wheels | Freeze Python3.13.14 and existing package/source/model versions where reproducible; record Linux-specific transitive CUDA dependencies and artifact hashes. Missing pins/builds return S0, no silent latest install. |
| Vendor driver/toolkit versions unknown | Capture exact target driver/runtime and compatibility before model work; no compatibility PASS from product name or the provider's example PyTorch output. |
| Windows `GlobalMemoryStatusEx`, `memory_info().private` | Define Linux physical availability and per-tree committed-memory accounting before execution; RSS/PSS/cgroup resident memory is not automatically Windows private commitment. If equivalence/enforcement cannot be specified, HOLD. |
| Windows `CREATE_NO_WINDOW` and process enumeration | POSIX process-group/cgroup ownership, controller-inclusive sampling, descendant cleanup and evidence after first error; no unrelated process termination. |
| Old absolute deadline and manifest paths | New output manifest and fresh once-only invocation records, explicitly authorized later; do not reset/overwrite old records or resume partial predictions. |

VM host225GiB is provisioned capacity, not permission to use it. Prospective caps
remain16,000,000,000 host bytes, CPU2, one GPU and one heavy child. Proposed Linux
mechanism: dedicated cgroup/container covering scientific watchdog and descendants,
memory limit in exact decimal bytes with swap disabled; two eligible vCPUs bound by
affinity/cpuset and two-thread libraries; one device exposed. An outer observer must
be accounted for rather than hiding its memory. Sum owned-tree RSS and defined
private/committed metric each1s; record GPU allocated/reserved/capacity separately.
Cgroup charged memory alone is not proof of the original commitment contract.
Kernel/cgroup permissions, counters and measurement semantics are unverified.
Their review/validation belongs to a separately authorized portability scope.

## Setup and offline scientific phases

[D5](https://docs.lambda.ai/public-cloud/on-demand/managing-system-environment/)
documents Docker/toolkit and administrative environment management. Inference:
an isolated container or namespace is a plausible mechanism, subject to target
permissions and later checks. Avoid inheriting moving system-site packages.

During separately approved setup, only allowlisted sources/dependencies/checkpoint
and the exact three frozen fake inputs would be staged and verified, then frozen.
Source/checkpoint acquisition is currently zero and forbidden. Do not upload
credentials, response datasets, unrelated keys/caches or a recursive repository copy.

Before scientific import, use OS-level no-network isolation for the child and all
descendants, with no host-network/docker-control socket or credentials mounted;
local read-only inputs and writable new outputs only. Setup/control/export remain
outside that isolated process. Python audit hooks and HF offline flags remain
additional checks, not native-egress proof. The provider's inbound SSH firewall is
not an outbound/no-network boundary. Prove fail-closed behavior later with separately
authorized nonmodel boundary checks; none run here. Do not disable the management
path needed for termination. Exact isolation flags/kernel behavior need target
review; no validated cloud network recipe is claimed.

## Future scientific scope, only after S0/user decision

New target reference once and candidate once, sequential, each capped900s including
fresh process/import/load/all3/render/serialization and instrumentation. Reference
must pass first. Same frozen input bytes, context/head/model/options/seed/alpha-grid/
guard/tolerance; shadow/refit policy unchanged. No smaller context, fewer heads,
new optimization, extra run or deadline extension. Do not hard-code acceptance or
alpha.5 from the previous fake run: retain the identical frozen selection procedure.

Record environment/code/input identity before either process; hash checkpoint
before load only in that future approved scope. Target reference is the exact
comparator for target candidate controls, alpha0 and fallback. Cross-OS/GPU results
need not be bit-identical to RTX outputs; document that separately. Do not relax
within-target exact parity or numeric assertions after seeing differences.

Complete213 shadow and213 final heads when active, canonical189649 all3 vectors,
all class/order/raw/floor checks, final weights/buffers and input fingerprints,
load/call/failure/fallback counters, native offline evidence, natural S/E decision,
separate forced-active engineering render, inactive/empty fallback and new-reference
parity. Include all overhead in the capped process. First error/limit ends the
attempt and returns S0, preserving partial records without a new retry.
Past LOCAL_RESOURCE_LIMIT stays historical even if a later H100 run passes.

This does not authorize tiny-suite repeats, actual responses or hosted scoring.
H100 completion would still not prove real ERPIS benefit or S2 release readiness.
Any later S2 requires S0/user direction plus assembly/source parity, ZIP checker,
official all3, clean E025 absolute.002 per-instrument/E041 comparisons and SCORES
interpretation/provenance. No S2/S3/TEST decision made here.
