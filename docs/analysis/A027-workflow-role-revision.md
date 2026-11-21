# A027 — Persistent session roles and research entry revision
date-started: 2026-09-27
status: done — DOCUMENT_REVISION_ONLY
relates-to: A015 / A024 / A026 / E060

## Goal and authorization

The user asked to correct the repeated HOLD/rejection workflow and raised the
risk of fixing only future prompts. Persist the agreed separation of S0 strategy,
S1 research/information and S2 packaging in shared instructions. Current scope:
workflow documents and a concrete future S1 handoff; no research execution.

HEAD1d223340d4e1fa3993b411dc5daafab9cb37d0cd, work/e050-submission. Existing dirty
changes remain. A027 collision checked clear; no observed Python/pytest/uv/WSL/
bash jobs. [Entry](A027-outputs/entry.json) records63 permitted text/source hashes.
Main task is the persistent contract revision; backup is resolving any remaining
instruction conflicts within these documents, not another model or data search.

## Design and attempt log

### v1 — Identify the operating gap

Existing workflow/session-prompts already named S0/S1/S2/S3, but allowed multiple
task types in one conversation without a clear transition boundary. Broad S1
execution and automatic git instructions in templates encouraged scope drift.
Oracle/validation language did not clearly distinguish acquiring information
from establishing an empirical effect. A026 listed missing inputs but supplied
no bounded way to obtain them. These are operating defects, not evidence that
E058/E059 gates should be lowered or that E060 is effective.

Compared three fixes: prompt-only reminders (easy but prone to divergence), a new
parallel rule document (another conflict source), and the existing canonical
workflow plus aligned entry/templates (chosen). No new framework, agent scheduler
or code is needed. The existing A-series location is used instead of introducing
another planning-document hierarchy. Existing user authorization covers these
document edits; no repeated approval or commit is inferred from skill defaults.

### v2 — Persistent revision 2026-09-27-r2

- CLAUDE entry links the role/task-type contract and prohibits automatic S0
  execution transitions. End-of-day git work obeys current user scope.
- Workflow defines role boundaries, explicit already-authorized transitions,
  four research types with different entry/exit conditions, and a repeated-HOLD
  rule that requires a decision-changing input/acquisition task or exact trigger.
- Korean templates apply that contract. S1 information acquisition does not need
  prior positive effects; S0 does not build/train/package; S1 does not silently
  become S2; S2 result intake does not launch another experiment; a proposed TEST
  choice is not user confirmation. No template overrides no-commit/no-push scope.
- Entry and handoff summarize role, type, decision, allowed operations, cap,
  outcome actions and authority. A new model/ZIP is not the success definition
  for every session. Existing STOPs, data roles and research evidence stay intact.

### v3 — Concrete future information task, not execution

[S1 handoff](A027-outputs/s1-channel-metadata-handoff.ko.md) scopes one60-minute
public-document review of the existing UNHCR Jordan VAF catalog1030 lead and
its official questionnaire/codebook/access documentation. No new broad search,
microdata, private responses, request submission, fit or scoring. It can establish
documented incompatibility, missing access or sufficient metadata for a later
design review. It cannot certify observed approximate gates or empirical power
from metadata alone. Findings return to S0; there is no automatic adapter/study.

Difference from A024/A026: those read existing local records and did not recheck
the public source; this future task would obtain new current primary metadata.
Historical403 is not current access evidence. The prompt is prepared, not run;
no website visited or new source availability claimed in A027. This new information
task does not revoke A026's no-ready-empirical-study verdict or A023/A024 HOLD.

## Verification and limits

Review the shared documents against concrete scenarios: broad S0 progress request;
named metadata-only S1; independent-label confirmatory study; separately scoped
exploration without an informative proxy; repeated same-input HOLD; S2 result
intake; explicit already-authorized transition; no-commit/no-push session.
Check text consistency, local links, whitespace, HEAD and preserved hashes.
No model tests or scientific runs are necessary for this documentation change.
See [verification](A027-outputs/verification.json).

These files are persistent instructions in this checkout, not a runtime permission
enforcer or a guarantee that every agent obeys them. Future sessions must read
them and report actual actions. Commit/push is not authorized: another checkout
will not receive this local revision until a later authorized synchronization.

## Preservation and next action

Only CLAUDE/workflow/session-prompts/status/log and new A027 records are changed.
Historical A026/A025/E060 records/manifests and all model/submission bytes remain
untouched; docs/tree.md and existing user changes are preserved. No network,
data/cache/Parquet/ZIP access, fit/score/test, commit/push, S3 or TEST selection.

E041 incumbent/E025 fallback, E057/E060 parked, E058 STOP/E059 STOP_SELECTION,
A023/A024 empirical HOLD, all earlier STOPs, A_half nonpromotion and A018 user-
unconfirmed persist. Prior17999people/12339SSUID and A022 role inventory/exposure
remain unchanged. Next session, when invoked by the user, is S1 information
acquisition using the linked complete prompt. S0 does not execute that prompt.
