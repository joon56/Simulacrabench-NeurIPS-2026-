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
- **TEST choice is NOT user-confirmed.** User explicitly stopped S3 and clarified
  that [A018](analysis/A018-test-selection.md) is an unconfirmed review proposal,
  including its selected/frozen wording. E041 remains DEV incumbent; E025 is the
  existing fallback. Preserve A018 files; no S3 resumption in this S1 session.
- Latest user-reported submission: E052 Grand .64, no best update; individual
  scores unavailable. E045/E047/E049 also read .64 without an update; effects
  remain unresolved. E044 .63 was adverse under its registered arm. Keep E041.
- E054 is prepared but **parked and unsubmitted**; A013 found limited readable
  probe value. It is not an improvement candidate or automatic next submission.
- Current-day slot availability is unverified. No new upload reported in setup.
  Historical .65 leaderboard screenshot is not a current winning-score forecast.

## Latest research decision

- [E057](experiments/E057-unhcr-conditional-content.md) UNHCR procedure/runtime
  engineering PASS, research candidate parked. All145 schema leaves considered;
  124 shadow+124 refit trees. Selection3 leaves; independent validation fails
  preregistered2SE, so all shares0 and final all3 output exact E041. No retuning.
  Full run564.662s, conservative fit544.353s, aggregate peak RSS1.703GiB;
  13 focused tests and frozen verification PASS. E025 absolute.002 all3 PASS.
  Forced-active invariants PASS, no forced-policy score. Synthetic data cannot
  establish or refute real UNHCR benefit. **S2 local release qualification PASS:**
  [report](analysis/E057-outputs/s2/report.md), [scorecard](../submissions/2026-09-25-E057/SCORES.md).
  Default/assembly/official189649 vectors exact, active fixture PASS, official
  all3/checker/E025 absolute.002 PASS. Shared assembly540.508s/1.696GiB RSS;
  official suite556.545s/2.313GiB. ZIP21bce867... frozen, candidate still parked.
  Eligible for bounded user-controlled DEV exploration; no target gain,
  new incumbent, TEST choice, method change or upload. Account slot unknown.
- [E056](experiments/E056-conditional-leaf-content.md) positive conditional-content
  research screen: SIPP group audit delta skill +.000651952785,
  95% SSUID interval [+.000202805542,+.001195519933]. Only BIR alpha=.5 selected;
  parent/raw sentinel preserved. Diagnostic checks PASS; no production model,
  release qualification or S2-ready candidate. No humanitarian gain forecast.
  Oracle/selection/audit now exposed; calibration remains unscored. See
  [exposure ledger](analysis/E056-outputs/exposure-ledger.md).
- [A014](analysis/A014-observed-gated-channel.md) accepted SIPP as an observed
  exact-gate structural proxy: 39,131 eligible people; not approximate UNHCR.
- [E055](experiments/E055-coupled-star-replay.md) finite coupled oracle STOP:
  person/group delta skill/3 +.000113126178 / +.000102390016, below its registered
  +.005. Recursion and both buckets exercised; frozen results independently
  verified. Those scores were unopened at E055 close; E056 exposure is above.
  No E055 calibrator or ZIP.
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
- **S2 readiness checked:** [A017](analysis/A017-s2-readiness-check.md) found no
  new candidate. Frozen hashes96/96 match; E041/E054 ZIP checker freshly PASS,
  kit remote unchanged. Existing official/parity evidence retained without fits.
  No new archive, upload date or result; E054 remains parked.
- **S1 E056 complete.** Registration18ab9e6, executed codedbb0ac6. Zero new
  E041 fits; six trees .216s, four worker stages44.897s excluding imports,
  peak RSS.401GiB. Frozen arithmetic verified without new labels or fits.
- **S1 E057 complete.** Registration592da4c, executed codee51b29f. All owned jobs
  complete. **S2 complete:** freeze3f0f6ad, all remaining local release checks
  PASS; three suites1624.724s total, no repeated successful fit. Next is a
  user-controlled DEV decision/result loop using the frozen scorecard, not
  more identical local fitting. No automatic upload, backup or S3 resumption.
  E058 is only the expected next number; recheck collisions before reserving.
- **S3 A018 unconfirmed review artifacts:** E041 ZIP official phase2 PASSx3, raw
  source parity442425, all3 shared-process336.55s/peak commitment1.60GB.
  E025332.78s/1.56GB; its historical official provenance limits are disclosed.
  [Manifest](analysis/A018-outputs/freeze-manifest.json) binds files and methods.
  Its historical proposed release actions/dates remain in A018; they are not
  active instructions or a user-confirmed TEST schedule in this S1 handoff.
  These engineering records do not establish a user-confirmed TEST choice.
  Those archived jobs finished; E057 also closed with no active job. Preserve user changes.
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
- Both final methods have four visually checked pages, including Adult/SIPP/
  TabPFN development and replay limitations. Starter-kit notice preserved.
  Effective team source-license grant awaits owner choice before award-stage
  delivery; no whole-repository release. [Current runbook](phase2-preparation.md)
  records fresh official dates and exact selected/fallback delivery paths.
- [A015 diagnosis and adoption record](analysis/A015-workflow-self-audit.md).
  [Full pre-setup status archive](analysis/A015-outputs/status-before-workflow.md)
  preserves all previous loss maps, closed axes, results, timing and date caveats.
  [Log](log.md) is newest-first; [tree](tree.md) indexes all experiments.
