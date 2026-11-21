# SimulacraBench agent entry

This is the repository-wide entry point for Codex sessions in this checkout.
The user's current scope takes precedence over repository defaults. Do not infer
execution permission from a session label, historical prompt or general goal.

Before project work, read in order:
1. `CLAUDE.md`
2. `docs/status.md`
3. The newest three entries of `docs/log.md`
4. `docs/workflow.md`, then the current task's handoff

`docs/workflow.md` is the persistent role/task-entry contract;
`docs/session-prompts.ko.md` supplies templates, not a separate authority.
State a brief workflow receipt before substantive work: role, task type, current
workflow revision, actual read paths and allowed/forbidden operations. Record the
workflow SHA256 and read evidence in the normal session record; if writes are
forbidden, give the receipt in chat. A hash alone does not prove the file was read.
Follow workflow.md's read-receipt and resumption rules. Do not claim other chats
loaded the rules from this file merely because it exists.

S0 performs strategy, records and handoff only: no automatic experiment-code,
fit/predict/score, protected-response access or ZIP work. S1 follows its named
information/technical/empirical task; S2 follows a named release/result task.
S3/TEST selection and commit/push require the active user's applicable authority.
Preserve existing dirty work, prior STOP/HOLDs and evaluation exposure boundaries.
Do not run generic tests, fits, package checks or tree regeneration as startup.

An established S0 remains S0 across follow-ups. Under the user's r7 delegated
operation instruction, S0 dispatches bounded S1/S2 work to executor subagents;
manual copying into separate chats is optional. The parent does not itself run
model/release operations. Delegation does not create missing scientific, data,
budget or upload authority. The assistant cannot grant a transition by announcing it.
Before any cross-role operation, cite the user's actual same-conversation
transition or bounded exception; a general goal is not such evidence. Without
it, finish the S0 review/handoff and stop before execution, without repeatedly
asking the user to restate the standing separation. See workflow role routing.

Current workflow r7 (2026-10-26): S0 coordinates authorized subagents directly.
Root alone dispatches children; children do not redelegate. One executor may own
S1 and conditional S2, while a reviewer remains read-only. An approved batch's
gates proceed without new user handoffs. New scientific/data/budget scope still
needs applicable user authority. S3 needs its own scope; TEST choice/upload remain
separate. No indefinite background operation or new-day execution is implied.
Use the current control epoch/task ID in status's linked orchestration record.
Only one writer exists, including root. Root releases before a child accepts;
while the child writes, root/reviewers are read-only. Actual artifacts/jobs and an
explicit release are required before reassignment. Records are coordination,
not an atomic lock. Legacy independent chats must finish/release before cutover.

Workflow r6 foundation (2026-10-22): an executing session or assigned child may perform S1 and
conditional S2 sequentially within a user-approved, finite batch. The batch names
candidates, entry/transition gates, allowed inputs/outputs, new aggregate budgets,
attempt limits and result arms. Do not request a new S0 handoff at an already
authorized S1-to-S2 gate; record the gate and role receipt instead. Completed S1
work is reused when its identities/provenance hold, not repeated. This does not
turn the coordinating S0 into an executor. S3 preparation/comparison requires a
separate user instruction; final TEST choice/upload remain separate decisions.
Exactly one session owns writes to this checkout at a time. Record outgoing and
incoming owner, dirty files, running jobs and release of ownership before transfer.
The current approved batch and state live in docs/status.md and its linked record.

Repair autonomy from r5 (2026-10-05): the owning session fixes ordinary implementation errors
within its authorized task, verifies the affected boundary, and continues without
a new S0 handoff per error. Keep aggregate budgets, scientific/data policy and
attempt counts fixed; uncertain remote side effects require identity/cleanup before
any duplicate action. Preserve failures. Escalate scope/authority/budget decisions,
not routine repair. A stopped process does not automatically end the session.

Existing chats must explicitly reread current instructions when resumed after a
workflow change; do not assume file edits update an already-running context.

For Windows/Codex setup and the repository map, use `docs/codex-setup.ko.md`.
The optional `scripts/check_workspace.py` checks document wiring and package
metadata only; it is not a research/release test or proof of session compliance.
Repository skills live in `.agents/skills/`; paper-session loads its shared
protocol from `.claude/skills/paper-session/SKILL.md`. Do not copy Claude-local
permissions into Codex or enable automatic fit/test/package/push startup hooks.
