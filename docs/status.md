# STATUS — current decisions and handoff

Updated: 2026-09-25. Read CLAUDE.md first, then this file, then the newest three
log entries. The user adopted [workflow.md](workflow.md); session prompts are
in [session-prompts.ko.md](session-prompts.ko.md). Details belong in linked records.

## Current position

- Goal: win final TEST; use DEV for informative, technically qualified exploration.
- DEV incumbent: **E041, Grand .64 / UNICEF .52 / WB .49 / UNHCR .92**, user-reported.
  [Scorecard](../submissions/2026-09-19-E041/SCORES.md),
  [ZIP](../submissions/2026-09-19-E041.zip). Local performance qualification failed
  before the hosted improvement; do not use proxy failure as a universal veto.
- TEST selection remains open. E041 passed A012 phase-2 engineering qualification;
  E025 remains the prepared fallback. [E041 preparation](../submissions/phase2-E041-preparation/SCORES.md),
  [E025 preparation](../submissions/phase2-E025-preparation/SCORES.md).
- Latest user-reported submission: E052 Grand .64, no best update; individual
  scores unavailable. E045/E047/E049 also read .64 without an update; effects
  remain unresolved. E044 .63 was adverse under its registered arm. Keep E041.
- E054 is prepared but **parked and unsubmitted**; A013 found limited readable
  probe value. It is not an improvement candidate or automatic next submission.
- Current-day slot availability is unverified. No new upload reported in setup.
  Historical .65 leaderboard screenshot is not a current winning-score forecast.

## Latest research decision

- [A014](analysis/A014-observed-gated-channel.md) accepted SIPP as an observed
  exact-gate structural proxy: 39,131 eligible people; not approximate UNHCR.
- [E055](experiments/E055-coupled-star-replay.md) finite coupled oracle STOP:
  person/group delta skill/3 +.000113126178 / +.000102390016, below its registered
  +.005. Recursion and both buckets exercised; frozen results independently
  verified. Calibration/selection/audit scores unopened. No calibrator or ZIP.
  This closes that registered proxy study, not all target-domain calibration.
- [A011](analysis/A011-replay-bias-diagnostics.md) measured replay/deployment
  mismatch, not its causal effect or a repair gain. E050/E051/E053 stops likewise
  have explicit family/data scope. Historical validation defects in
  [A006](analysis/A006-dev-validation-audit.md) do not prove recoverable headroom.

## Active work and next session

- Workflow setup: A015 v2; adopted documents, session catalog, aligned rules and
  templates. No experiment or training job launched by this setup. Check active
  jobs and working tree before beginning new work; this is not a process lock.
- Integration ownership transfers at handoff. One writing session per checkout;
  subagents are bounded reviewers/workers, not competing session managers.
- **Next: S0 coordinator.** Compare materially different hypotheses using A009,
  A006 and the latest scoped stops; choose one main task and a justified backup,
  then generate a concrete S1 prompt. No replacement candidate is yet established.
- Next available experiment **E056**; reserve centrally before creating it.
  Next analysis ID A016; workflow continuation stays within A015.
- Keep E055's STOP; do not add favorable seeds or silently lower its threshold.
  New exploration may have different justified criteria registered beforehand.

## Reminders that change decisions

- Historical E025 UNHCR map: .79 base + .10 evidence = .89; residual .079 gated
  + .031 ungated. This is **not E041's decomposition** or measured recoverable gain.
- Technical checks, no-regression policy, exploratory submission and final
  adoption are distinct. +.005 is a historical local default, not universal 3 sigma.
- Assumption-injected simulations cannot establish target transfer. Calibration
  requires held-out/cross-fitted evidence; no relabeling exposed rows as untouched.
- Measurement A/Bs change UNHCR only; no hidden per-instrument score or activation
  is inferred from flat Grand. Use preregistered favorable/adverse/unresolved arms.
- Every package: clean E025 no-regression within absolute .002 per instrument,
  relevant E041 comparison, source/archive parity, ZIP checker, official all3
  schemas and SCORES preregistration. Intentional probes disclose their ablation.
- Profile the whole shared runtime budget; local speed is no hosted guarantee.
  On starter-kit changes, revalidate affected assumptions and release checks.
- User controls upload, one authorized account only. Failed uploads follow the
  recorded no-slot-consumption rule; verify platform status. Preserve prior files.

## TEST preparation and history

- A012 E041 official phase-2 skills .490197771/.462029505/.564665365;367.177s local;
  exact source/archive vectors442425. Paired E025 deltas0/0/-.000508449. Engineering
  qualification is not a hosted performance or runtime guarantee.
- E041 four-page method is prepared; E025 originals retained. Reconcile any new
  development/disclosure and release license before final delivery. Use
  [phase-2 runbook](phase2-preparation.md); reverify official dates before finalization.
- [A015 diagnosis and adoption record](analysis/A015-workflow-self-audit.md).
  [Full pre-setup status archive](analysis/A015-outputs/status-before-workflow.md)
  preserves all previous loss maps, closed axes, results, timing and date caveats.
  [Log](log.md) is newest-first; [tree](tree.md) indexes all experiments.
