# A040 S0 — termination query contract review

2026-10-05 KST. Role S0, document/source review only.
Decision: **ACCEPT QUERY_ARGUMENT_CONTRACT_FAIL; TERMINATION STILL UNCONFIRMED**.
Recommend one separate S1 cleanup-only task with local helper validation before
its fresh remote window. Defer the prior conditional production-controller repair.

Read AGENTS → CLAUDE → status → newest3log → workflow2026-09-27-r4, then
sandbox-lifecycle-repair1 closeout/receipt/verification/ledger/helper and installed
SDK source. Workflow SHA256:
a83c6f4102f50d0b8919f0f2010acfd19954901e8e2a08e7771ef87831741642.
HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1. Existing dirty work preserved.
Normal session evidence and permitted hashes are in verification.json.

## What the records establish

The helper receipt records returned Client.from_env, then InvalidError at
WorkspaceNameLookup, elapsed1.2158657s. It does not contain the exception message.
Installed modal/_grpc_client.py:125-126 rejects timeout with non-None retry before
direct transport. The helper passes timeout=cap without retry=None at multiple
RPC sites. Its hash28019d3b2543e1f53d667b63af302b806e49b70e19bbe19aa25b2aaa735abd57
matches the saved manifest. This supports a local helper defect; it is not evidence
of account denial, service failure, absent Sandbox or a model/hardware failure.

Normal client initialization may have performed authentication/ClientHello calls;
its wire count is unknown. Do not call the entire S1 attempt RPC0. Sandbox query,
terminate, billing, new resource and science results are absent. Exit0 only means
a failure receipt was saved. No local production copy/repair was started.

The new helper otherwise supplies an exact-name, app-scoped, finished-inclusive
list design. Static protobuf source contains its principal SandboxInfo/list fields.
However, no actual wrapper-to-fake-transport validation was run. Installed
Sandbox.poll/terminate distinguish V1 and V2 and use the normal auth manager on V2;
the failed helper hardcodes V1 methods. Target ID/version remains unknown.
This is an unvalidated branch, not proof that the target is V2 or another live error.

## Decision and scope correction

Accept the failure verdict. The missing terminal fact is agent-obtainable through
a corrected bounded query; user-supplied ID/screenshot is an alternative source,
not automatically a new prerequisite. No new login, token or limit change follows
from this defect.

The previous S0 prompt insufficiently separated cleanup-helper preparation from
production-controller repair. It required terminal proof before phase2 but did
not require actual wrapper validation before the phase1 query. Correct that scope:
permit local cleanup-helper repair/validation first, then one existing-resource
query/necessary termination window. No production lifecycle repair in this task,
even after terminal confirmation. Preserve all previous failures and allowances.

Main: <=30min S1, local checks<=180s aggregate/30s each, CPU2/GPU0, followed only
on local PASS by one <=120s live metadata/necessary termination window. Per call
<=15s; protect final30s for evidence. Check every used wrapper/protobuf branch
against installed SDK, including version routing and unknown-status rejection.
Use named enums, record safe exception text/stage, and preserve terminal evidence
even if later billing retrieval fails. No actual endpoint/auth during local checks.

Backup: precise closeout plus official detail-screen evidence request if bounded
lookup cannot resolve the exact resource. No automatic alternative-cloud run,
new create/build, extended budget or silently repeated window. The previous
production-controller repair remains a future S0 decision.

This is operational cleanup, not progress evidence for TEST score. Repeated
infrastructure failures lower this route's current priority and justify withholding
new cloud measurement. They do not disprove TabICL or imply H100 is insufficient.

## State and costs

App ap-XiMVzlJgrNrCiFpIN1kB4W STOPPED/task0 remains a prior observation only.
Sandbox a040-resume5-20261005-094405-gpu terminal/ID and final charge remain unknown.
Past image completion im-XZ95GDfkfa6PwWUeFyciYM is preserved; no new model run.
Preparation12587.4312918s; science4process/1077.3504532s. Receipt time is included
in the latest712.9984114s, not added again. Prior aggregate0.00178978USD,
2400s planning reservation2.965933453125USD and attribution/posting uncertainty
remain. USD1/5 plans and cash0 unchanged; no live billing observation by S0.

E041 incumbent/E025 fallback; E057/E060/E061 parked. All scientific STOP/HOLD,
E058 STOP/E059 STOP_SELECTION/A039 HOLD, exposure17999/12339, aggregate/A022 roles,
E059 consumed oracle1918/1124 and selection2007/1130, protected audit2074/1177 and
calibration1866 remain. A_half not promoted; A018 user-unconfirmed; S3 stopped;
S2 candidate absent.

Only new S0 decision/prompt/verification and status/log are written. No helper
repair/import/test/RPC/model/payload/ZIP/commit/push/tree/subagent work here.

