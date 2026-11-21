# A040 S0 — local controller repair before any new remote attempt

2026-10-03 KST. Accept **BLOCKED_SPECIFIC_INPUT / LOCAL_BUILD_LOGGING_FAIL**.
Recommend one separate, local-only S1 controller repair. No cloud retry in this scope.

## Evidence and limits of diagnosis

The eight requested records consistently show a UnicodeEncodeError: local cp949
cannot encode U+2022 from Modal progress output. It occurred during the base-image
result join, before the dependency installer. The base ultimately succeeded; the
complete dependency image, H100, target boundaries and both scientific runs did not.

Source review also finds unbounded cancellation gather and an AppStop await in
build_once.py. A failure during cancellation could delay reaching the finally block;
the source alone does not establish that this caused the observed warning/hang.
The public async client/private stub combination is a review target, not a proven
SDK defect. Repair must verify the selected SDK call path locally with mocks and
bounded exit behavior. Merely adding a UTF-8 launch flag is insufficient evidence
that cleanup works. No remote reproduction is needed for these local contracts.

App ap-CJkQ7byYW3D872nirY6KRM was stopped and its task query empty according to
saved CLI/API records. S0 did not query it. im-eWgRNij0VH6mzozlOzEyxy is only the
completed base, not a deployment-ready image. Reuse requires later scope and
identity/status verification; no mutable tag or saved image ID implies full pins.

Account summary0 and Deployed Apps0.00001152USD are both preserved, without
adding overlapping aggregates or claiming final cost0. Posting/attribution/cache
overhead remain unresolved. The monitored budget amendment still applies; no
return to exact USD1/5 proof, repeated login/budget RPC or supplier inquiry.

## Decision

A small controller repair has value because this defect prevents collecting any
model feasibility evidence and can be checked locally without cloud spend. It is
not a new scientific hypothesis or a reason to change model/context/guard settings.
Main: UTF-8 and bounded lifecycle/cancellation repair with focused local regression.
Backup: exact unresolved controller defect closeout. No alternative model or build.

The [S1 prompt](s1-local-controller-repair.ko.md) proposes a distinct30min repair,
local regression subprocesses<=120s cumulative, no model/GPU/network/account call.
These are new task limits when the user delivers the prompt, not leftover execution
rights. Previous active3312.1552137s remains in history; nominal preparation remainder
287.8447863s does not authorize another build. Prior scientific allowance remains
unused. Future remote scope/time/cumulative cost must be decided explicitly after
local evidence, without rewriting prior deadlines or resetting costs.

LOCAL_CONTROLLER_CONTRACT_PASS would mean only that the repaired local contracts
pass against the named mocks/redirected streams. It does not prove server cleanup,
dependency-image success, H100 feasibility, ERPIS effect or S2 readiness.

## Receipt and preservation

S0 strategy/review/handoff; ordered AGENTS/CLAUDE entry/status/latest3log/workflow
read a2a211; HEAD/dirty/jobs f95e65; task records e92d66; controller source362fc7.
Systematic debugging and minimal-change code-review guidance read a050b4; no
reproduction/implementation under S0. Workflow2026-09-27-r4, SHA256
a83c6f4102f50d0b8919f0f2010acfd19954901e8e2a08e7771ef87831741642.
HEADa43f4379ec78dbc2de260463eef67bb1d567d7e1 unchanged. Named local Python jobs
query returned no rows; no exhaustive account/workload claim. Selected document/
source hashes checked, not112 staging/checkpoint/input parity.

Only new S0 documents and additive status/log. No original code/manifest/latch,
model/snapshot/tree change, protected input, fixture, model import/fit/predict/score,
SDK/account/remote operation, termination, contact, agents, ZIP or commit/push.
E041/E025; parked E057/E060/E061; E058/E059 and every STOP/HOLD including A039;
17999/12339, A022 roles, E059 consumed oracle1918/1124 and selection2007/1130,
protected audit2074/1177 and calibration1866 preserved. A_half not promoted;
A018 unconfirmed, S3 stopped, no S2 candidate. [Verification](verification.json).
