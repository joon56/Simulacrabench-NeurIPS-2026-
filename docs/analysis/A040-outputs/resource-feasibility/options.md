# A040 H100 options — documented, not acquired

**HOLD_SPECIFIC_INPUT / EXECUTION_NOT_AUTHORIZED.** Two concrete listings exist;
actual obtainable capacity, exclusive allocation, account authority and total budget
remain unconfirmed. RESOURCE_OPTION_DOCUMENTED describes this information artifact,
not readiness to execute. No provider or GPU selected on the user's behalf.

| Published single-GPU VM offering | Option1 | Option2 |
|---|---:|---:|
| Provider | Lambda On-Demand | Lambda On-Demand |
| GPU | H100 PCIe | H100 SXM |
| Advertised GPUs / VRAM each | 1 /80GB | 1 /80GB |
| vCPU / host RAM |26 /225GiB|26 /225GiB|
| Listed root SSD |1TiB|2.75TiB|
| USD per GPU-hour, tax extra |$3.29|$4.29|

Source: [D1 pricing](https://lambda.ai/pricing), independently consistent with
[D3 instance table](https://docs.lambda.ai/public-cloud/on-demand/), accessed
2026-10-02. With one GPU, GPU-hour and instance-hour rate coincide. These are
not the cheaper per-GPU rows requiring multiple GPUs or a cluster reservation.
Option1 has lower published spend per hour; no measured speed/value ranking.

Both are listed as one80GB GPU, rather than a named MIG slice. **The reviewed
documents do not explicitly guarantee MIG disabled, exclusive physical GPU use,
absence of time sharing, dedicated CPU cores or a particular CPU model.** Full,
non-shared GPU allocation is a required future condition, not a confirmed fact.
User/provider must establish allocation terms; later authorized preflight must
record device UUID, MIG state, GPU count/capacity and competing GPU processes.
Observed device state alone cannot establish all tenancy guarantees.

Published regions do not establish H100 stock in a selected region. New-account
quotas exist; inventory/quotas are exposed through authenticated management.
No access was attempted. [D6](https://docs.lambda.ai/public-cloud/on-demand/creating-managing-instances/)
User or institutional account owner must establish account eligibility, payment or
allocation authority, acceptable region and termination permission. No credentials
should be pasted into S0/S1 handoffs. Institutional access, if the user already has
it, is an alternative fact to provide, not a third researched proposal.

Documented baseline OS is Ubuntu22.04; image families also include24.04.
Their default Python is3.10/3.12, not our3.13.14. Exact image ID, CPU model,
driver, toolkit and container digest remain unverified. Neither option reproduces
Windows/RTX3070 by provisioning alone. [D3](https://docs.lambda.ai/public-cloud/on-demand/)
Docker and NVIDIA Container Toolkit support make isolated deployment plausible;
our offline/limit implementation remains a proposed port, not a provider guarantee
or tested environment. [D5](https://docs.lambda.ai/public-cloud/on-demand/managing-system-environment/)

No H100 runtime, gain estimate or success probability follows.641.0873s remains
completed expert predict calls plus CUDA synchronization on RTX3070, including
unseparated CPU/device/wait work. No remaining-head or hardware-speed extrapolation.
