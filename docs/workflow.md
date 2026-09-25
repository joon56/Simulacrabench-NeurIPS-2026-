# HSCC research workflow

Adopted by the user on 2026-09-25, following A015. This is the shared operating
guide, not a prediction of winning. CLAUDE.md holds authoritative project rules;
this guide implements them. Existing experiment registrations and verdicts
remain immutable historical decisions. New criteria apply prospectively.

## Entry and session routing

Read CLAUDE.md, docs/status.md, then the newest three docs/log.md entries in
that order. Read this guide and the relevant experiment/scorecard afterward.
Do not reread the entire history unless a decision needs it.

| Session | Use when | Required deliverable |
| --- | --- | --- |
| S0 Coordinator and prompt | Starting, resuming, reprioritizing, or reviewing strategy | One decision, main task, backup, bounded work scope and next-session prompt |
| S1 Research and experiment | Testing a named mechanism or fixing a validation defect | Preregistered experiment/analysis, scoped evidence and next action |
| S2 DEV package and result | A named candidate is ready, or a hosted result arrives | Verified immutable archive/scorecard, or recorded reading and recommendation |
| S3 TEST selection and delivery | Comparing finalists, phase-2 hardening, final selection | Candidate comparison, frozen selection rationale, method and release checks |

These are task types, not four daily meetings or four always-running agents.
Use one main conversation by default; start a new conversation for a new family,
a distinct deliverable, or unwieldy context. Handoff through files, not chat memory.
Korean copy-ready prompts: [session-prompts.ko.md](session-prompts.ko.md).

## Session contract

Before costly work record in the current A/E record: objective, comparator and
source hash, expected decision, inspected evidence, main task, justified backup,
resource cap, label roles allowed, and stop/continue arms. Use an A record for
non-model research and an E record for a model experiment; do not invent an E
just for a new conversation. Reserve IDs through the single integration owner.

If no time limit is supplied, finish one registered main task and at most one
justified backup, plus required validation/recording. Declare the compute cap
before fitting. This is bounded authorization, not a background scheduler or
a promise of unattended execution. Never silently start another day's work.

Continue routine authorized work without repeated permission questions. Ask
only for missing consequential constraints, conflicting instructions, new paid
resources, destructive actions or upload authorization not already supplied.
When a branch stops, complete its record and continue the ready backup within
scope; do not repeatedly end with an offer to do the already authorized next step.

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

One integration owner writes shared status/log/template files, allocates IDs,
stages and commits. Before editing, inspect HEAD, branch, dirty files and active
jobs. A status owner field is coordination, not a real filesystem lock; a stale
field does not authorize killing a process or overwriting uncommitted work.

Never run independent writing chats in this checkout simultaneously. Prefer
read-only parallel review; use separately owned worktrees/branches for necessary
independent edits and integrate deliberately. Never edit sources used by a live
experiment or race two fits for the same output directory.

Use subagents only for a bounded independent task alongside useful primary work:
domain/source review, code/statistical review, or frozen-artifact verification.
Default to sequential work when delegation adds overhead. At most one heavy fit
at a time unless the integration owner has checked shared CPU/GPU/RAM budgets.
Avoid duplicate tests or fits without a changed artifact or unresolved concern.

Each delegated task names: input commit/files, question, owned output files,
forbidden label access, resource cap and required evidence. Reviewers do not tune
on final audit labels. They return facts, limitations and blockers; agreement
between agents is not independent empirical evidence. Root resolves differences,
verifies deliverables and alone integrates. Temporary agents do not replace
versioned workflow instructions or create persistent new chat sessions.

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
Keep historical detail in log/experiment/analysis records. Commit task files
only and push origin; verify remote HEAD. Do not overwrite user-owned changes.
