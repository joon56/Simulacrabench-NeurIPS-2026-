# HSCC research workflow

Adopted by the user on 2026-09-25, following A015. This is the shared operating
guide, not a prediction of winning. CLAUDE.md holds authoritative project rules;
this guide implements them. Existing experiment registrations and verdicts
remain immutable historical decisions. New criteria apply prospectively.

Role/entry revision: **2026-10-26-r7**. Delegated operation is recorded in
[A045](analysis/A045-outputs/decision.md). The r6 batch/ownership foundation is recorded in
[A044](analysis/A044-outputs/decision.md). Role design is recorded in
[A027](analysis/A027-workflow-role-revision.md); entry/read verification in
[A028](analysis/A028-workflow-entry-audit.md). This file holds the persistent
operating contract; session-prompts.ko.md is its reusable interface. Status holds
the current decision; historical handoffs record past scope, not standing grants.
The user's current instructions take precedence over repository defaults. Never
use a shorter prompt, an old handoff or silence to expand an established scope.

## Entry and session routing

Read CLAUDE.md, docs/status.md, then the newest three docs/log.md entries in
that order. Read this guide and the relevant experiment/scorecard afterward.
Do not reread the entire history unless a decision needs it.

### Required read receipt and resumption

Repository `AGENTS.md` connects Codex instruction discovery to this reading
sequence; CLAUDE.md contains the same entry requirement. Links and templates are
entry wiring, not evidence that a particular session actually read or obeyed it.

Before substantive work, give a concise receipt in commentary: working directory,
role/task type, workflow revision actually read, entry-file paths, allowed actions
and forbidden transitions. In the existing A/E entry record or handoff, include
the read time, HEAD, workflow SHA256 and evidence of actual tool reads (command/
tool result or transcript reference where available). Do not invent a transcript
ID. A digest identifies bytes; it does not prove reading or comprehension. For a
read-only task, keep the receipt in chat; no new file/analysis ID is required.

If the required files have not been read, perform those allowed reads before
research/package execution. If a required file is unavailable, report the exact
gap; do not assume compliance or silently use an obsolete handoff. This is a
local preparation requirement, not another permission question for authorized work.

Existing chats resuming after a workflow revision must reread AGENTS/CLAUDE and
the entry sequence, then report the current revision and scope before continuing.
On a role transition, confirm the user's applicable authority and refresh the
receipt. During unchanged continuous work, do not repeat the reading ritual each
turn. S0 checks incoming receipts/artifacts and classifies evidence as observed
tool read, session-reported read, template reference only, or unverified. Never
label all sessions compliant from file existence or a checksum alone. Missing
historical receipts remain missing; do not rewrite past records to fabricate them.

| Session | Use when | Required deliverable |
| --- | --- | --- |
| S0 Coordinator and prompt | Starting, resuming, reprioritizing, or reviewing strategy | One decision, main/justified backup, bounded handoff or exact missing-input closeout; document work only |
| S1 Research and information | Acquiring missing evidence, technical validation, or a named empirical study | Task-specific A/E record, scoped evidence and an action; a model/package is not required |
| S2 DEV package and result | A named candidate is ready, or a hosted result arrives | Candidate-specific release checks/archive, or result recording only; no independent model search |
| S3 TEST selection and delivery | Explicitly authorized finalist comparison, phase-2 hardening or selection | Scoped review/release work; a recommendation is not the user's confirmed TEST choice |

These are task types, not four daily meetings or four always-running agents.
Keep the operating conversation in S0. Under the user's delegated-operation
instruction, root dispatches a user-approved finite S1/conditional S2 batch to an
executor child using the saved contract; manual copy/paste is optional. A standalone
named S1 or S2 task remains valid when no batch is approved. Continue a
same-role task in its existing conversation when context remains manageable.
Handoff through identified files plus root's task message, not chat memory alone.
Child dispatch is authorized by the current orchestration instruction, not by a
role label; it stays inside the task envelope defined below.
Korean copy-ready prompts: [session-prompts.ko.md](session-prompts.ko.md).

One conversation may host different roles only when the user has authorized the
transition and its operations. A role label alone grants no data, fit, package,
upload or git authority. In an established S0, "continue", "make progress" or
"work toward today's submission" keeps S0 scope; do not infer S1/S2 execution.
Do not ask again when the user already authorized a concrete transition. State
the new role/scope before acting. A copied prompt starts only the operations it
explicitly allows; generating that prompt does not execute it in its authoring S0.

### Persistent role and action routing (r4)

In an established S0, all of the following keep S0 scope by default: "start
work", "perform all resumption inputs", "try various experiments", "prepare a
submission", and "continue until there is something to hand off". Interpret
these as goals for the coordinated workflow. Finish the available S0 work and
write the concrete execution contract; dispatch only authorized child work under
r7, and do not self-promote into S1/S2. The user
need not append prohibitions on every follow-up. General autonomy/finish-the-task
instructions apply inside the authorized role, not across this boundary.

A same-chat exception must identify this conversation as the executor and name
the operations: for example, "In this chat, switch from S0 to S1 and execute
the named handoff, excluding packaging/upload." An equivalent unambiguous user
instruction also counts; no magic wording is required. A role name alone, an
assistant's statement, a quoted historical prompt, or silence does not count.

Before the first operation outside the current role, record: current role,
requested operation, exact applicable user instruction, executor, allowed data
and output boundary. If same-chat authority is absent, route it to a handoff and
stop before that operation. For r7 delegation, this record identifies the child
and its applicable task authority; the parent retains S0 scope. Do not ask repeated
permission at an already approved child or stage boundary. A genuine instruction
conflict may require one focused clarification while independent S0 work proceeds.

| Requested operation in S0 | Action |
|---|---|
| Compare existing research, inspect permitted source, prepare an executable task | S0 performs review and writes S1 handoff; no import/run of research modules |
| Explicitly requested public platform/rule lookup or workflow repair | S0 performs that named document/source task; no implied model/data execution |
| Acquire a research dataset or build a research extractor/adapter | S0 scopes S1 acquisition/technical task; no direct execution by default |
| Fit, predict, score, run scientific fixtures, implement a model | S1 named task, after its own entry and permission boundaries |
| Assemble/check a submission archive or official release | Named S2 task, including a preauthorized conditional S2 stage in a separate execution batch |
| Upload, commit/push, resume S3 or select TEST | Require the applicable explicit user authority, not a prepared artifact |

Transition errors are corrected in a new dated operational record and current
status. Keep original manifests and scientific results intact; identify earlier
authorization interpretations as errors rather than silently rewriting history.
[A033 review](analysis/A033-dev-handoff-and-role-repair.md) documents the E060/A032
failure pattern. These instructions reduce ambiguity; they are not a technical
tool lock or proof that other running chats have read them.

S0 may review existing allowed documents, public metadata and permitted source,
compare hypotheses and write operating records/prompts. New data acquisition or
scientific execution belongs in an explicitly scoped task; protected response,
fit/predict/score, experiment-code and archive creation are not S0 defaults.
Standalone S1 returns a qualified named candidate to S0 for scoped S2 dispatch. Within an approved batch,
the same executor may enter the explicitly authorized S2 stage after recording
its fixed gates; this is not a silent or self-authorized role change.
S2 result intake does not restart qualification/fitting absent a documented defect
and authorized repair scope. S3 remains stopped until the user resumes it.

### Approved execution batches (r6)

S0 owns candidate priority, batch composition, fresh budget proposals, prospective
reading criteria and result judgment. A written handoff is a proposal until the
user authorizes that named execution envelope, directly or within an explicit
standing bounded scope. Root may then dispatch it without manual user transfer. The current S0
remains strategy/records/handoff only. S3 is separately approved and never a
conditional continuation of a DEV batch. TEST preparation/comparison is distinct
from user final selection and upload.

Every batch fixes before execution:

- finite candidate IDs and identities, completed stages, next uncompleted stage;
- allowed files/data roles, exact outputs and prohibited operations;
- S1-to-S2 gates and authority, including technical/release/empirical distinctions;
- fresh gross/compute/cost/attempt caps, per-run limits and cleanup reserve;
  old consumed allowances remain consumed; all repair/failure time is counted;
- reusable checks and source/input/environment/provenance validity conditions;
- favorable/adverse/unresolved/technical/HOLD arms, hard stops and scope-return rules;
- exclusive writer, incoming/outgoing ownership receipt and quiescent handover.

Do not add weak hypotheses to fill a batch. A batch can contain one already
implemented candidate and start directly at S2. Reuse unchanged completed work;
do not rerun successful implementation suites, source fits or official checks
without a documented invalidation and an applicable budget. Reuse requires both
identity and complete provenance; equal aggregate scores are not raw parity.

An authorized stage transition needs a recorded gate/role receipt, not another
user confirmation or S0 handoff. Routine errors follow r5 below within the same
batch. New hypotheses, inputs/roles, scientific policy or criteria, budgets,
unlisted candidates, paid resources, or exhaustion of a cap return to S0. No
unbounded retries, automatic upload, TEST choice or git operation. Child dispatch
uses r7 authority and never refreshes a consumed allowance.
If a named branch stops, preserve it and continue only another prospectively
listed independent branch; otherwise close the batch with the next decision.

### Delegated operation and automatic gates (r7)

The user adopted subagent operation on 2026-10-26 to remove manual transfers.
Root S0 may assign bounded document/source information work and review, and may
dispatch scientific/release work only under an applicable approved execution
envelope. Changing delegation does not approve undefined models, data roles,
execution budgets or S3 work. Root owns decisions; children own named execution.
Do not require a new user message for each agent, ordinary repair, result return
or preauthorized S1-to-S2 gate.

- Root alone creates/retasks children. No recursive delegation. Prefer one
  execution child for S1 and conditional S2 when this avoids transferring live state.
- Default one heavy job, no simultaneous fits. Parallelism is for independent
  read-only work on stable/frozen inputs. Respect available agent slots; do not
  keep idle role agents running merely to fill a roster.
- Each assignment names task ID/control epoch, role/type, actual user authority,
  source/input identities, allowed paths/actions, new aggregate caps, reuse gates,
  result arms, hard stops and artifacts. Unspecified permissions stay absent.
- Stage success means registered gates passed, not a child's optimistic summary.
  Root checks allowed artifacts/identity/provenance, usage and release. Review does
  not require rerunning unchanged fits or all successful tests.
- Repairs stay inside the same envelope and cumulative limits. New child/process/
  chat never resets budget, attempts, failures or exposure.
- On failure continue only a prospectively authorized independent branch, else
  return one decision/blocker to root. Root resolves ordinary in-scope choices;
  changed scientific/data/cost authority goes to the user once a concrete revised
  scope is ready. No endless repair/HOLD cycles.
- S3 is a separately approved scope, not necessarily a separate chat. It may use
  a child, but DEV success never activates it. Final TEST choice, upload, license
  grants, new paid resources and commit/push retain their user boundaries.
- Work runs while an authorized active run is coordinated. No daemon, unattended
  new-day campaign, automatic platform polling or guaranteed work after the
  runtime stops is implied. Resume from recorded state; do not duplicate uncertain
  actions or treat a dead agent as proof its jobs ended.

At cutover, reconcile/release existing independent writers. Then use one root
controller. Its linked state holds control_epoch, active_writer_task_id, writer
identity, dispatched task/agent, authority, status and artifact/release paths.
Executors accept only their current root assignment. Source hashes plus an old
release receipt cannot distinguish competing claimants. Legacy chats do not
restart from old prompts without fresh root assignment and valid user scope.
Records coordinate cooperating agents; they are not an atomic filesystem lock.
If another writer or uncertain ownership appears, suspend new writes/dispatch,
preserve both histories and reconcile. Do not kill another session's job.

## Research task types and entry conditions

Record one primary task type before work. Classification is prospective; changing
its name after failure does not relax a registered gate or erase exposure.

| Task type | Required before entry | Useful completion | Does not require or authorize |
| --- | --- | --- | --- |
| Information acquisition | Named missing fact and decision, sources/access boundary, bounded search/time, success/failure actions | A sourced answer, unsuitable-source decision, or exact access/metadata blocker | Positive model evidence, a complete power plan or fit permission merely to inspect authorized metadata |
| Technical validation | Concrete invariant/defect, frozen artifacts, authorized fixture/input scope and resource cap | Verified boundary/repair or technical failure with artifacts | Target efficacy; stub success never licenses protected labels or real training |
| Confirmatory empirical research | Identified population/mechanism, authorized independent roles/exposure, estimand/comparator, prospective precision/error plan, implementation and full-cost plan | Registered positive/adverse/inconclusive/technical verdict | Automatic transfer to another population, retrospective gate change or TEST adoption |
| Bounded exploratory DEV research | Distinct named intervention, prior-result novelty review, permitted channel and limitations, informative oracle where applicable, frozen release gates/costs and hosted reading arms | Qualified named candidate for S2, or scoped rejection/inconclusive closeout | A positive proxy effect as a universal entry condition, an uninformative oracle, or a relaxed historical STOP |

Information tasks are legitimate S1 work before the evidence needed for an
empirical study exists. A channel's license/access/documentation review is not
authorization to acquire responses. Record unknowns rather than manufacturing
approximate gates, independent roles or precision. If no informative oracle is
available for a distinct exploration, explain why before estimator construction;
do not treat this as an exemption from technical/release checks or useful readings.
Every type retains original data protections, user scope and prior STOP/HOLDs.

## Breaking repeated HOLD cycles

A HOLD must identify the missing input, why it changes a decision, how it can be
obtained, who can obtain it, the allowed operations, cost limit and resumption
trigger. S0 owns turning an obtainable missing input into a bounded S1 task;
do not make the user repeatedly invent the next research step. User-owned inputs
include actual submission reports, restricted-access approval, paid resources
and final choices. Agent-owned tasks can include authorized public-document
research, source review or a specifically scoped technical check.

If the same blocker returns with no material new evidence or changed scope, link
the existing HOLD instead of commissioning another equivalent review, fixture
suite or analysis record. A workflow correction is recorded once, not disguised
as new efficacy evidence. An information task must be able to change the next
action; if none can do so within the available authority/budget, close with the
exact trigger instead of inventing a model or repeating an empty handoff.

Success is a decision-relevant uncertainty reduced, a route ruled out within its
scope, a technical prerequisite resolved, or a qualified candidate—not a required
number of fits, daily ZIPs or automatic advancement through S0/S1/S2/S3. Stop a
bounded search at its registered limit; no endless channel search or same-policy
submission loop. Repeated flat readings can reduce priority without proving zero
effect or requiring every future exploratory family to pass A023's study design.

## Session contract

Before costly work record in the current A/E record: objective, comparator and
source hash, expected decision, inspected evidence, main task, justified backup,
resource cap, label roles allowed, and stop/continue arms. Use an A record for
non-model research and an E record for a model experiment; do not invent an E
just for a new conversation. Reserve IDs through the single integration owner.

At entry summarize: session role; research task type; decision; main/backup;
allowed and forbidden reads/actions; time/compute cap; exit/output; transition
authority. A handoff additionally gives exact files/HEAD and dirty-source hashes,
prior exposure, outcome-to-action mapping and what remains unauthorized. Keep
this contract concise; do not create a second planning project for a routine task.

If no time limit is supplied, finish one registered main task and at most one
justified backup, plus required validation/recording. Declare the compute cap
before fitting. This is bounded authorization, not a background scheduler or
a promise of unattended execution. Never silently start another day's work.

Continue routine authorized work without repeated permission questions. Ask
only for missing consequential constraints, conflicting instructions, new paid
resources, destructive actions or upload authorization not already supplied.
When a branch stops, complete its record and continue the ready backup within
scope; do not repeatedly end with an offer to do the already authorized next step.

### Repair autonomy within the current task (r5)

The user correction on 2026-10-05 distinguishes a process failure from a session
handoff. The owning S1/S2 repairs routine implementation defects and continues the
already authorized task. Do not return to S0 or ask the user for a new prompt for
each argument, import, encoding, logging, path or SDK-binding error.

First identify the cause, make the smallest in-scope change, verify the affected
boundary against the actual dependency, then continue. A mock that bypasses the
failed boundary is insufficient. Re-run only checks invalidated by the change;
do not repeat unrelated successful suites. Preserve the failed artifact and append
cause/diff/check/cumulative usage in the existing task record. Routine repairs do
not each need a new A/E ID, planning document or review session.

This autonomy applies while objective, data access, scientific policy, validation
criteria, authorized operations and aggregate time/cost/attempt limits stay fixed.
Local helper repair is allowed to resolve an unmet prerequisite when that helper
serves the authorized task; it need not wait for the fact it is meant to obtain.
Build frozen identities before the next affected operation and preserve old ones.

Return to S0 only for a decision outside those boundaries: new protected inputs,
changed model/seed/head/threshold/selection policy, changed success criteria,
new or exhausted scientific/resource allowance, unmet external authority, or no
credible repair path within the remaining budget. Unknown remote side effects
block duplicate creation/execution; continue only already-authorized diagnosis
and exact-resource cleanup until the state is resolved or its limit is reached.
Do not treat an ambiguous timeout as permission to repeat a mutation.

Do not put a blanket "first error ends the session" into new handoffs. Specify
which scientific/data/resource events require a hard stop; stopping a failed
process and preserving its evidence does not itself require a session handoff.
Engineering repair uses the existing aggregate budget. It never resets a deadline,
bill, exposure ledger, scientific latch or consumed invocation. If limits are
missing, use the session-contract default; do not invent a per-error approval gate.

Explicit current user hard stops still win. Historical STOP/HOLDs and failed
records remain historical; this rule does not silently restart a closed attempt.
The current A040 cleanup proposal uses the dated repair-autonomy amendment linked
from status; production-controller repair and new cloud measurement remain outside
that cleanup task. Other open chats must reread the current revision before applying these rules.

## Evidence and decisions

Track four separate decisions; no single PASS stands for all four:

1. **Technical qualification:** valid outputs, leakage controls, package parity,
   checker, official scorer and resource constraints.
2. **Release performance policy:** clean no-regression against the registered
   baseline/tolerance. This is not a proof of technical correctness or transfer.
3. **DEV exploration:** named target mechanism and outcomes that could change a
   decision, even when a proxy does not establish gain.
4. **Adoption/TEST selection:** evidence for the claimed population and setting,
   generalization limits, complexity and deployment behavior.

For every conclusion identify data/population, frozen model, parameter family,
metric, comparator, sampling unit and what uncertainty is not measured.
Separate oracle headroom, learned held-out gain and hosted observation.
The historical +.005 is a default local operational adoption bar, not a universal
significance cutoff or target-domain futility bound. Any different prospective
criterion needs rationale before score access, not a lower cutoff after failure.

Use a valid scoped oracle before building an estimator when it can bound the
proposed family. A failed registered gate stops that study. If the available
channel cannot represent the mechanism or target population, explicitly record
that limitation. It does not certify zero headroom on hidden data. A distinct
bounded exploratory design may proceed under the user's standing authorization,
with preregistered rationale and all release checks. Do not relabel a failed
study, add favorable seeds or rewrite its gate to turn it into a pass.

Qualitative candidate comparison: target relevance, supporting/contradicting
evidence, possible useful gain, downside, distinguishable hosted readings,
implementation cost and time remaining. Unknowns stay unknown; do not invent
expected gains, win probabilities or a numerical priority formula. A probe must
say which outcomes change the next action. A small improvement may still matter;
measurement resolution and practical value are different questions.

## Evaluation boundaries and novelty

- Register fit/calibration/selection/audit roles, group boundaries and previous
  exposure before fitting. Separate chats and new seeds do not erase exposure.
- Once audit scores influence design, those observations become development
  evidence for later work. Record the change; do not call them untouched again.
- Review the full decision path, including selection and refitting, not just one
  estimator. Report paired differences and appropriate uncertainty where feasible;
  state dependence and training variation omitted from any interval.
- A new family must name what changed and why earlier negative evidence does
  not already answer it. Renaming a coefficient sweep is not a new mechanism.
- Assumption-injected simulations are directional checks. Audited permitted
  public proxies can test structure, but their scores do not forecast Grand.
- An observed mismatch is not proof of its cause or the gain from repairing it.

## DEV release and result loop

Prefer a qualified, decision-relevant submission to an unused slot, consistent
with user preference. Do not require proxy certainty or fabricate a candidate
to fill the day. If no package is recommended, identify the failed qualification
or absent useful reading, and the next executable task.

Freeze the comparator and target instrument before implementation. Standing
measurement A/Bs change UNHCR only; other-instrument exploration needs an explicit
prospective attribution design and user direction. Verify unchanged controls.
Do not interpret hidden instrument values from a rounded Grand as exact scores.

Before every release: (a) clean no-regression against E025 within the standing
absolute .002 tolerance per instrument, plus the relevant E041 comparison;
(b) source/assembled single-file parity; (c) ZIP checker and official score.py
PASS for all three schemas. A deliberate probe's changed scored output cannot
be called no-regression: validate its unchanged underlying model separately
and disclose the intended ablation under an explicitly registered probe design.
This is not a blanket regression exception; E054 remains parked.

Preregister SCORES.md with favorable/adverse/unresolved/failed arms before upload.
Use submissions/YYYY-MM-DD-E0XX.zip and the matching source/scorecard directory.
Record the ZIP hash, intended date and actual upload timestamp separately.
Check slot status rather than assuming availability; use one authorized account.
Failed uploads do not imply statistical failure or consume a slot under the
recorded competition rule. Recheck current official rules if they change.
No upload is authorized merely by preparing a package.

On a result, use the registered arm and append actual values; preserve original
predictions/arms. Grand unchanged means no readable new best, not zero effect.
A best update is favorable evidence with noise/rounding, not proof of an exact
gain or isolated cause. Track DEV incumbent and TEST shortlist separately.

## Shared workspace and subagents

One named owner has write responsibility for the entire shared checkout, including
task-specific outputs, status/log/templates and ID allocation. Staging/committing
still requires applicable user authority. Before editing, inspect HEAD, branch, dirty files and active
jobs. A status owner field is coordination, not a real filesystem lock; a stale
field does not authorize killing a process or overwriting uncommitted work.

At transfer, the outgoing session records its owned paths, unfinished operations,
named process IDs/logs (or observed none), artifact identities and ownership
release. The incoming session reads that receipt and records acceptance before
writing. No receipt means no assumed ownership; never kill another session's job.
Use status plus the linked dated ownership record; these are coordination records,
not an OS lock. S0 → executing batch → separately approved S3 is sequential; a
different documented order is permitted. Idle/read-only sessions may not edit.

Never run independent writing chats in this checkout simultaneously. Prefer
read-only parallel review; use separately owned worktrees/branches for necessary
independent edits and integrate deliberately. Never edit sources used by a live
experiment or race two fits for the same output directory.
Different files or branch names in the same shared checkout are not an exception
to the single-writer rule; isolated work requires a genuinely separate worktree.

Subagents require applicable user authorization; the current r7 orchestration
instruction supplies delegation authority without repeated per-child approval.
Use bounded information/review or approved execution scopes, not an unrestricted
agent hierarchy. Root is the only dispatcher. Default to sequential execution;
one heavy job at a time. Any exception needs a separately approved resource scope.
Avoid duplicate tests or fits without a changed artifact or unresolved concern.

Each delegated task names: input commit/files, question, owned output files,
forbidden label access, resource cap and required evidence. Reviewers do not tune
on final audit labels. They return facts, limitations and blockers; agreement
between agents is not independent empirical evidence. Root resolves differences
and verifies deliverables. Only the current writer integrates files; root remains
read-only while an executor owns writes. Temporary agents do not replace versioned
workflow instructions or create persistent new chat sessions.

## TEST readiness and strategic review

For each finalist compare actual DEV evidence, validation limits, activation,
TRAIN+DEV refit changes, calibration, three-schema phase-2 behavior, full-run
runtime/memory observations, external-data/model disclosure and fallback.
An ensemble is a new candidate requiring its own evidence and runtime checks.
Freeze selection criteria, an engineering cutoff and the final artifact before
the upload window closes; verify official dates then. No .65 or winning forecast
follows from a historical leaderboard screenshot.

Review strategy after a hosted result, a materially new mechanism/rule change,
or a completed research cycle that leaves no candidate. Ask whether a diagnostic
changed a decision and whether another stage of it will do so. Protect time for
candidate construction and TEST engineering; do not impose an unmeasured fixed
time-allocation percentage. Repeated flat results lower a configuration's
priority without proving a universal ceiling.

## Close and handoff

Report: decision, measured facts, interpretation, unknowns, stop/continue reason,
artifact readiness and next action. Include HEAD, artifact hashes/paths, scored
roles, active jobs/logs, ownership and blockers when relevant. Link existing
A/E/SCORES records rather than copying all details into every file.

Keep status.md short: incumbent/fallback, active work/owner, last decision,
slot/result availability, next main/backup, nonnegotiable reminders and links.
Keep historical detail in log/experiment/analysis records. Commit/push only under
the active user's authorization; a template or session name is not such authority.
When authorized, commit task files only, push origin and verify remote HEAD.
Do not overwrite user-owned changes or treat repository instructions as a
technical access lock: verify actual actions and preservation at closeout.
