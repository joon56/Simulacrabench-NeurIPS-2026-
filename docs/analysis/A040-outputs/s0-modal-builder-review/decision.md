# A040 S0 — resume4 builder delivery review

2026-10-05 KST. **ACCEPT_PREPARATION_FAILURE / RECOMMEND_BOUNDED_LOCAL_SOURCE_DELIVERY_REPAIR**.
Remote execution remains unauthorized in this review. One narrowly bounded S1
local repair is worthwhile; no automatic remote retry or broader infrastructure
project. [Proposed S1 prompt](s1-builder-source-contract.ko.md).

## Receipt

S0 result/source review under workflow2026-09-27-r4, SHA256
`a83c6f4102f50d0b8919f0f2010acfd19954901e8e2a08e7771ef87831741642`.
Read AGENTS, CLAUDE entry, status, newest three log entries, workflow routing,
then resume4 named records. Unchanged instruction sections read in preceding
reviews remain applicable; workflow research/evidence/preservation sections were
also reread. This is not evidence that another chat loaded these instructions.
HEAD `a43f4379ec78dbc2de260463eef67bb1d567d7e1`; existing dirty work retained.
Local python/pythonw/uv metadata check returned no rows; no remote job audit.
Allowed: documents/source inspection, selected source/document hashes, S0 records.
No model, imports/tests, payload, RPC, build, ZIP, commit/push or subagents.

## Findings and limits

Resume4 source12 matches its freeze and the prior source-manifest SHA256
`0060ed98fc7e3c9ecc5625bd24f5c276971b026817dbb06c92fc2744dec83815`.
Configuration hash also matches. Builder stdout records a failure importing
`controller_core` before `install_pins` runs. Remote base identity succeeded;
dependency image did not. App `ap-zr5WBi06SAuzc6om241Y32` was recorded STOPPED/task0.
No Sandbox, payload validation/transfer, H100, boundary or science. S0 did not
repeat account/status/cleanup requests. Existing termination evidence suffices.

Pinned installed Modal1.6.0 source supports the following causal diagnosis:

- `sdk_endpoint.py` passes the module-defined `controller_core.install_pins` to
  `run_function(..., include_source=False)`.
- `_image.py:2695` forwards this flag into `_Function._from_local`.
- `_functions.py:771` makes the entrypoint mount empty when the flag is false.
- `_utils/function_utils.py:358` mounts one defining file for a FILE function,
  but can mount a package for a PACKAGE function. Actual function classification
  and resulting inventory therefore matter; blindly enabling source is inadequate.
- `controller_core.py` imports asyncio at module entry; the installer body uses
  stdlib modules. Source inspection found no additional local module dependency.
  Later Sandbox upload cannot satisfy an earlier builder import.

The missing source mount is a concrete implementation defect consistent with the
remote traceback. S0 has not demonstrated that changing the flag completes a real
build. Previous mock endpoints bypassed this transport/import boundary. Their
PASS results remain valid only within their tested scope. The previous S0 review
also failed to inspect this prerequisite before recommending remote work.

## Priority and next decision

Recorded S1 preparation/controller time is9080.7295157s, about2h31m; science remains
4process/1077.3504532s from earlier local work. These are recorded task times, not
all project labor or GPU billing. H100 execution is still0. Worker12.6109304s
already includes cleanup2.1232256s and lies within the session ledger; do not add
them twice. This S0 review is separate from that inherited S1 ledger.

Another unchanged remote attempt has little information value. Abandoning TabICL
as ineffective would also be unsupported: no target efficacy or H100 feasibility
observation was produced. One local repair has value because a specific delivery
defect can now be checked against the actual SDK rather than an invented endpoint.
That value is conditional feasibility information, not a predicted Grand gain or
proof this is the globally best research route. Sunk preparation time is not a
reason to continue indefinitely.

Main: at most45min S1, focused local checks<=120s total and<=2 cycles, fix only the
defining-module delivery on a new source copy. Prefer include_source=True only
after actual SDK construction proves FILE classification and exactly one project
source file, controller_core.py, at the expected remote module location. Preserve
the installer body/pins and all science. Check isolated import from those exact
staged bytes, with installer execution and RPC blocked. Inspect the real builder
function/dependency mount inventory, not merely the supplied flag or a fake image
returning success. Small negative controls must expose the original omission.

No new preparation framework, repeated39/15/14 suite, model fixture or remote smoke
test. Backup: preserve failure and closeout. If minimal source-only delivery cannot
be established within the cap, stop and lower this infrastructure route's priority;
do not commission the same repair/review again without new named evidence. If PASS,
return a new source identity and the remaining remote conditions for S0 review.
No existing run allowance is automatically renewed.

## Budget and preservation

USD1 preparation/USD5 cumulative remain monitored plans, cash authority0. Do not
restore the superseded exact-invoice guarantee prerequisite or request a provider
email/account increase for this local defect. Latest recorded billing0 and old
component0.00001152USD retain attribution/posting uncertainty. Management value
0.6502900821875501 includes unused0.65 allowance; it is not observed cost. User
reported credits30/spend0/usage30 are not newly authenticated in S0.

Linux/dependencies/native enforcement, final112-file identity, real builder import,
H100900s, cleanup/billing, whole-path output and release are still unverified.
E041 incumbent/E025 fallback; E057/E060/E061 parked; all STOP/HOLD including E058,
E059 STOP_SELECTION and A039 remain. Exposure17999/12339SSUID, aggregates/A022 roles,
consumed oracle1918/1124 and selection2007/1130, protected audit2074/1177 and
calibration1866 unchanged. A_half nonpromotion, A018 user-unconfirmed, S3 stopped,
S2 none. Existing failures, sources/manifests/latches/tree untouched.

Read/hash/preservation evidence: [verification](verification.json).
