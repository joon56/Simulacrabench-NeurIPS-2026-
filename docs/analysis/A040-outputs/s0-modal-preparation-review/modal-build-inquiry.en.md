# Modal preparation cost-control inquiry — unsent draft

Subject: Bounding image preparation charges before a small H100 validation run

Hello Modal Support,

I use the Starter plan with included compute credits. Before launching a small
H100 validation job, I need to keep total image preparation within USD1 in credits
and avoid out-of-pocket charges. SDK version is1.6.0; configured image builder
is2025.06. No image build or Sandbox has been launched for this task.

We can cap a Sandbox's CPU, RAM and lifetime, but have not established coverage
for the image preparation that happens outside it. Could you clarify:

1. Which registry-import/pull, image-build, startup, layer/snapshot, storage and
   transfer stages are separately billed, and which are included or unbilled?
2. Is there a supported end-to-end cost cap, or a combination of resource,
   lifetime and attempt limits, covering those stages and automatic retries?
   Do such controls apply to a FROM-only image and a capped run_function build?
3. When a build/app is cancelled, which operation stops all associated billable
   work? Is there a documented maximum additional charge or stopping delay?
   Does a workspace spend limit of USD0 stop all out-of-pocket charges for these
   stages, and can gross preparation usage itself be capped at USD1?

A documented preparation recipe with equivalent cost control would also help.
If a strict USD1 preparation ceiling is not supported, please say so; we can
leave the job unlaunched rather than assume an estimated cost is a guarantee.

Thank you.

---

S0 note: Draft only. No message sent, contact identity verified, account change
requested or execution authorized. No tokens, data or model artifacts attached.
