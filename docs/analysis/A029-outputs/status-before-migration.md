# STATUS — current decisions and handoff

Updated: 2026-09-27. Read CLAUDE.md first, then this file, then the newest three
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
- Latest user-reported submission: **E060 Grand .64, no best update**; individual
  scores/upload timestamp/submission ID not supplied; uploaded bytes unconfirmed.
  Registered unresolved arm: E041 retained, E060 parked.
  [Reading/S0 handoff](analysis/E060-outputs/s2/post-result-handoff.ko.md).
  E045/E047/E049/E052/E057 also read .64 without an update; effects
  remain unresolved. E044 .63 was adverse under its registered arm. Keep E041.
- E054 is prepared but **parked and unsubmitted**; A013 found limited readable
  probe value. It is not an improvement candidate or automatic next submission.
- Current-day slot availability is unverified; E060 upload date/time unknown.
  Historical .65 leaderboard screenshot is not a current winning-score forecast.

## Latest research decision

- [E059](experiments/E059-leaf-donor-interactions.md) fixed-lambda donor pair
  comparison **STOP_SELECTION**. Technical preflight/10 fixtures PASS; base
  fits0, beta fit1 (.02293s), fixed R/A_half/B_half. Oracle both positive;
  selection B_half-R passes2SE but B_half-A_half fails. Audit remains unopened;
  oracle/selection now consumed. No A promotion, S2 candidate or UNHCR gain claim.
  Four monitored stages21.117s; peak aggregate commitment.495GiB.
  [Closeout](analysis/E059-outputs/closeout.md),
  [exposure](analysis/E059-outputs/exposure-ledger.md),
  [S0 handoff](analysis/E059-outputs/s0-handoff.ko.md).
- [E058](experiments/E058-donor-pair-interactions.md) fixed-donor GIVEN pair
  interaction **STOP**. [A019](analysis/A019-sipp-model-exposure.md) exposure
  audit PASS; one fresh generic E041 fit on original5922 rows,5999 disjoint
  query rows. Original active learned sections0, so beta fits0 and41993 output
  vectors exact baseline. Label-free finite-library oracle upper1e-12 below
  unchanged1e-10 gate; no new oracle/selection/audit response opened or score
  computed.12 tests and frozen verification PASS. Whole local run20.267s,
  conservative fit12.978s, peak aggregate commitment.660GiB. This inactive
  family STOP is not an interaction efficacy estimate or UNHCR impossibility.
  [Closeout](analysis/E058-outputs/closeout.md),
  [exposure ledger](analysis/E058-outputs/exposure-ledger.md). No S2 candidate.
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
  User now reports Grand.64/no update: no readable improvement, effect/activation
  unresolved. No incumbent/TEST promotion or repeat-upload recommendation.
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

- **A028 entry audit: root AGENTS added; workflow revision2026-09-27-r3.**
  [Audit and evidence limits](analysis/A028-workflow-entry-audit.md).
  Prior A027 proved document consistency, not every session's actual loading.
  Root Codex entry now points to shared files; all templates require actual-read
  revision/role/scope receipts with workflow digest and read evidence. Current
  S0 read observed; historical S1/S2 references are recorded, new r3 loading by
  other chats remains unverified. Existing chats must reread on resumption;
  no fresh Codex process or S3 was launched to claim runtime coverage.
  Next S1 prompt below remains valid (current r2-or-later); metadata task not run.
- **A027 persistent workflow revision2026-09-27-r2 applied locally.**
  [Revision record](analysis/A027-workflow-role-revision.md),
  [next S1 information-task prompt](analysis/A027-outputs/s1-channel-metadata-handoff.ko.md).
  CLAUDE/workflow/session-prompts now fix role transitions, four task-type entry
  conditions and a concrete missing-input task instead of repeated same-input HOLD.
  S0 does not execute S1/S2 by inference. Next proposed S1: one bounded60-minute
  public-document review of existing Jordan VAF catalog1030 and official coding/
  routing/access metadata; no response download, fit or score. Prompt prepared,
  not executed. Empirical A023/A024 HOLD remains; A026 findings are preserved.
  User starts the next session with that prompt; S0 does not start the search.
  No model/package/tree/commit/push/S3/TEST actions. Same-checkout instructions
  updated; other checkouts have not been synchronized.
- **S0 A026 complete — no new S1 execution handoff.**
  [Post-E060 strategy decision](analysis/A026-post-e060-strategy-review.md).
  Existing records provide no new effect evidence to raise E060's priority.
  Repeated flat interventions are not independent estimates of one zero effect.
  No E060 rescue/repeat, E054 probe revival or automatic A023 implementation.
  Next useful input: existing hosted provenance/instrument metadata, or a named
  compatible channel/access/role/precision dossier. Metadata alone is not efficacy.
  A023/A024 empirical HOLD remains; no ready distinct S1 study identified.
  Backup is missing-condition closeout, not another fit or repeated diagnostics.
  S0 remains strategy/records/handoff only; prior E060 work does not authorize
  S1/S2 execution here. No experiment, scoring, protected access or package work.
- **E060 hosted .64/no update: unresolved; parked, E041 retained.**
  [A025 candidate comparison](analysis/A025-submission-oriented-review.md),
  [E060 registration](experiments/E060-content-target-retrieval.md).
  UNHCR-only content-target metric fitting; original selector/seed/donors fixed.
  11 tests, source/assembly/official all3 raw parity and ZIP checker PASS.
  UNICEF/WB exact controls; UNHCR42820 changed vectors, synthetic delta E041
  -.000019774/E025-.000505919; tolerances PASS, no target efficacy claim.
  Assembly319.319s, official338.093s; total1046.456s includes failed46.575s
  harness attempt, one documented technical retry. Peak commitment1.907GiB.
  [ZIP](../submissions/2026-09-27-E060.zip),
  [scorecard](../submissions/2026-09-27-E060/SCORES.md),
  [closeout](analysis/E060-outputs/closeout.md),
  [post-result S0 handoff](analysis/E060-outputs/s2/post-result-handoff.ko.md).
  User report establishes no readable new best; exact effect/hosted prediction
  identity/active sections remain unknown. Technical and synthetic PASS do not
  establish hosted improvement. Next: S0 decision questions only; no new study,
  same-policy retry or seed/head/threshold rescue. No TEST promotion/S3 restart.
  Entry51 permitted manifest hashes and local ZIP match; actual uploaded bytes
  unconfirmed. Result appends change four document hashes, not the original
  manifest/verification or source/ZIP. Existing dirty files/tree preserved;
  no protected Parquet/cache access, model execution, commit or push. E057 parked,
  E058 STOP/E059 STOP_SELECTION, all prior STOPs and A023/A024 HOLD remain.
- **S0 A024 complete — empirical HOLD; no next S1 execution prompt:**
  [Channel/role/precision review and resumption inputs](analysis/A024-channel-precision-review.md).
  Existing records identify no authorized observed channel for cross-section/
  approximate-gate evaluation. SIPP masks collapse; schema/stubs/sandbox do not
  supply observed effect variance. Original roles and all response boundaries
  remain. Prospective frozen-choice D-P/D-R analysis and conservative two-claim
  multiplicity option documented; numeric precision inputs still absent.
  Resume after a named channel/access dossier, compatible roles and justified
  effect/precision assumptions; adapter/parity/real cost require separate scope.
  A023 permitted hashes105 matched at entry; four Parquet hashes inherited only.
  No fit/response/key/Parquet hash/test rerun/commit/push/S2/S3. HEAD unchanged.
- **A023 technical boundary/cost contract PASS; empirical HOLD:**
  [Candidate/information contract](analysis/A023-candidate-boundary-contract.md),
  [full cost accounting](analysis/A023-cost-accounting.md),
  [closeout](analysis/A023-outputs/closeout.md),
  [S0 handoff](analysis/A023-outputs/s0-handoff.ko.md).13 stub tests PASS;
  no production fit/optimizer/response/key/cache/predict/score operations.
  Schema-only3 candidates, active items0/61/135; all213 outputs retained.
  Normal target comparison base2/neural6; metric up to16, plus ladder/lambda/
  rendering/failures and all3 costs. Real runtime/memory remain unmeasured.
  Actual fitting-only adapter/parity, suitable observed channel, role approval
  and evaluation precision/multiplicity unresolved. No automatic empirical run.
  A02279 permitted hashes match;4 Parquet hashes inherited without reread.
  Return to S0; no S2 candidate/E060/refit/commit/push/S3. Local/uncommitted,
  HEAD1d22334 unchanged, prior files/tree and every existing STOP preserved.
- **A022 key/role audit PASS; empirical HOLD remains:**
  [Result and scope](analysis/A022-remaining-role-audit.md),
  [verification](analysis/A022-outputs/verification.json). Whole prior-use SSUID
  exclusion leaves8700people/4975SSUID; original group roles fit4275/2453,
  calibration1368/779, oracle1333/764, selection842/478, audit882/501.
  No new roles or samples;8700 is not a new audit. Historical sample/query/roles
  reconstructed, protected hashes match. One verifier population-scope error
  corrected with recorded retry; same eligibility, no model responses read.
  Fits/predictions/scores/cache decodes0. Prior17999/12339 exposure unchanged.
  Historical [S1 builder/cost handoff](analysis/A022-outputs/s1-handoff.ko.md)
  completed as A023; do not repeat. Channel/precision and real cost unresolved;
  SIPP does not represent UNHCR cross-section/approximate-gate mechanism.
  No E060, commit/push, S2 candidate or S3. A022 local/uncommitted, HEAD unchanged.
- **A021 technical contract PASS; empirical research HOLD:**
  [R/P/D comparison and conditions](analysis/A021-selector-comparison-contract.md),
  [verification](analysis/A021-outputs/verification.json),
  [S0 handoff](analysis/A021-outputs/s0-handoff.ko.md).13 handwritten fixture
  tests PASS; public UNHCR155 PREDICT-parent gates/71 cross-section edges.
  Controlled P differs from exact R; D-P and D-R have separate interpretations.
  Actual fits/response access/predictions/scores/cache decodes all0. No E060,
  S2 candidate or effect claim. Independent empirical roles, real candidate
  construction and full cost plan unresolved. No automatic execution; audit
  remains closed. A021 files local/uncommitted, HEAD1d22334 unchanged; tree and
  prior A020/E058/E059/user files preserved. No commit/push/S3 this session.
- **S1 E059 complete; return to S0:** registered two-comparison gate failed;
  no further fit, audit opening or backup. All owned workers finished. Source
  HEAD1d22334 unchanged; E059 code/records plus pre-existing A020 records remain
  uncommitted under explicit no-commit/no-push scope. Preserve user changes.
  E060 is only prospective; check collision before any separately authorized study.
- **S0 A020 complete; its S1 handoff executed as E059:**
  [design review and rejected alternatives](analysis/A020-post-e058-design-review.md),
  [copy-ready prompt](analysis/A020-outputs/s1-handoff.ko.md).
  Proposes a separate three-arm leaf-evidence study: fixed R/E041, matched
  additive control and pair candidate, fixed half mixture, both comparisons
  required. S0 verified59 source and5 artifact hashes with no cache decode,
  fit, prediction or score. User then explicitly authorized E059 execution;
  its semantic/empirical results are above. Existing STOPs preserved; no S2
  candidate. Documents remain uncommitted; commit/push not authorized this session.
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
  PASS; three suites1624.724s total, no repeated successful fit. Hosted.64/no
  update recorded under the unresolved arm. Its post-result S0 handoff remains
  historical; user subsequently authorized the bounded E058 study below.
  User explicitly approved the previously blocked origin push; S2 release and
  hosted-result commits through25e0b33 pushed to origin/work/e050-submission.
  Local release PASS unchanged; external-transfer approval blocker resolved.
- **S1 A019/E058 complete.** Audit registration24803a1, experiment registration
  f537a79, executed code8bcdf51. Fixed-active-section family STOP certified
  without new evaluation labels. No S2 handoff, additional fit or automatic
  backup. Next research requires a separately scoped, preregistered decision
  addressing this limitation. E059 is expected only; check collisions first.
- **S3 A018 unconfirmed review artifacts:** E041 ZIP official phase2 PASSx3, raw
  source parity442425, all3 shared-process336.55s/peak commitment1.60GB.
  E025332.78s/1.56GB; its historical official provenance limits are disclosed.
  [Manifest](analysis/A018-outputs/freeze-manifest.json) binds files and methods.
  Its historical proposed release actions/dates remain in A018; they are not
  active instructions or a user-confirmed TEST schedule in this S1 handoff.
  These engineering records do not establish a user-confirmed TEST choice.
  Those archived jobs finished; E058 also closed with no active job. Preserve user changes.
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
