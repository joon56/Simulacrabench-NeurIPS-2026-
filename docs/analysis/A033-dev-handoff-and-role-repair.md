# A033 — S0 DEV decision, feedback access and role correction
date-started: 2026-09-27
status: complete — S1_HANDOFF_READY / NO_EXECUTION
relates-to: A026 / A027 / A032 / E041 / E060

## Current authority and inputs

The user requested three S0 deliverables: choose a DEV experiment while VAF
approval is pending, investigate legitimate access to non-best instrument scores,
and diagnose/correct recurring S0 role overreach. S0 remains the executor of
document/source research, operating edits and handoff only. No S1/S2 execution.
Initial workflow r3; this task prospectively adopts r4. Ordered entry reads and
126 permitted baseline hashes are in [entry](A033-outputs/entry.json).
HEAD1d223340d4e1fa3993b411dc5daafab9cb37d0cd, work/e050-submission, dirty preserved.
No selected research process observed; process-name checks are not a global lock.

New user evidence: VAF access application **submitted, approval pending**. The
exact submitted text/approval conditions are not supplied; A032 inquiry draft
must not be reported as sent. User can currently see only Grand for non-best
submissions. Missing E060 instrument scores are not a user reporting omission.

Main deliverable: one distinct, bounded S1 exploratory candidate contract.
Fallback if it fails qualification: scoped failure/cost closeout and retained
incumbent; no second speculative model or unchanged VAF search. Platform and
workflow tasks are explicitly requested supporting deliverables. S0 cap90minutes;
zero scientific execution. Candidate input/source hashes in
[candidate-inputs](A033-outputs/candidate-inputs.json); no Parquet/cache rehash.

## DEV alternatives and decision

| Hypothesis / route | Support | Counterevidence / limits | Verification scope and cost | Decision |
|---|---|---|---|---|
| Tie a gated neural head's conditional logits to its ordinary full-head logits | E012/E041 explicitly train separate full and conditional linear heads from the same GIVEN representation. They can encode different relative probabilities for the same ordinary answers. Tying removes that freedom without new data, a new blend coefficient or extra model fits. | Inconsistency magnitude and target harm unmeasured. Independent heads may provide useful finite-sample flexibility; tying changes gradients and can hurt. Neural coherence does not guarantee final ladder/gate/evidence coherence or better TEST score. | Existing synthetic channel can check algebra, actual output change, no-regression and whole-run resources. No qualified real-data oracle exists for target gain. Same2 configs+1 refit per instrument per stack; bound and measure, no new seed/grid. | **Main S1 candidate**, one fixed UNHCR-only parameter-sharing intervention. Technical qualification for possible DEV exploration, not local/TEST adoption. |
| Change base capacity, repeat seed/temperature ensemble, or another broad tree blend | Different base errors could matter; earlier capacity contributed to historical E025. | E015/E017/E026 already explore capacity; E029 weak local variance/temperature evidence; E039 high CPU cost, E040/E046/E051 further tree evidence. No new observation justifies reopening these exact axes. | Extra fits and full release cost; Grand-only feedback remains coarse. | Not selected. Do not rename an old knob as a new mechanism. |
| Another donor/lambda/replay/content-target variant | E041 had a favorable hosted reading; interaction/content reasoning remains plausible. | E044 adverse; E045/E047/E049/E052/E057/E060 flat; E050/E053/E055/E058/E059 scoped STOPs. No new evidence for threshold/head/seed rescue. | Repeats costly selection and weakly resolved hosted comparisons. | Not selected; old STOPs unchanged. |
| A023 deployment-objective study on VAF | A032 now provides real questionnaire/DDI/linkage documents. | Approval pending, missing/edit provenance and natural approximate-gate observability unresolved; roles/precision/adapter/full cost still missing. | Provider-dependent, no response execution currently allowed. | Keep empirical HOLD; no repeat document search while waiting. |

This is a newly scoped exploration, not a claim that A026 was wrong on its then
reviewed evidence. The new user direction requests candidate selection beyond
waiting for VAF, and source review identifies a distinct parameter-sharing axis.
No expected Grand gain or winning probability is invented.

## Frozen main intervention

For a gated item with K ordinary outcomes, existing full logits are
`z_full=(z_1,...,z_K,z_sentinel)` and a separate head yields conditional logits.
Candidate keeps the full head and uses `z_cond=(z_1,...,z_K)` from that same head.
Thus `p_cond=softmax(z_cond)` equals the full distribution conditioned on an
ordinary outcome, before scoring-floor transformation. Use stable logits rather
than division by a nearly zero ordinary probability mass. Sentinel stays a
learned outcome; no deterministic schema gate is imposed on approximate data.

Keep the current pooled full CE plus masked conditional CE, including its cell
count denominator, auxiliary weighting and early-stop/config selection policy.
The change is the sharing of parameters/gradients, **not deleting conditional
loss, changing sentinel weight, replacing retrieval loss or retuning temperature**.
No extra full-versus-tied architecture tournament: the new candidate uses tied
heads; its original two width/depth configs remain unchanged. No warm-start mix,
post-hoc repair, penalty coefficient, seed sweep or head subset search.

UNHCR only. Ungated heads keep their output definitions, but shared-trunk
training means their numerical predictions may change; all213 heads are checked.
UNICEF/WB delegate unchanged E041/E025 control paths. Existing E041 retrieval,
selection, lambda rules, ladders and recursive rendering algorithms stay intact.
Lambda values may change when recalculated against the new base under unchanged
rules; this is a whole-pipeline comparison, not a frozen-lambda causal claim.

Novelty boundaries:
- E012/E025 already have conditional modeling; that factorization is not new.
- E056/E057 add independent conditional trees and preserve selected leaf sentinel
  mass; this adds no tree and makes no sentinel-preservation claim.
- E060 changes donor metric fitting targets; this leaves that objective alone.
- A023 changes selection objective/candidate libraries; this does not perform P/D
  selection or claim to resolve its empirical HOLD.
- E029 changes seed count and temperature; both remain fixed here.

Population coherence identity motivates regularization; it is not evidence of
a finite-sample gain. The final mixture contains ladders, soft gates and evidence,
so the neural identity is not asserted for the final output. Conditional-head
tests must target the neural boundary they actually establish.

## S1 acceptance and reading contract

The [copy-ready S1 handoff](A033-outputs/s1-tied-heads-handoff.ko.md) specifies
exact inputs, new files, synthetic roles, limits and stop arms. E061 is proposed
but no E061 record/model/test is created here; S1 must check collision at entry.
It may execute only after the user opens the receiving S1 and directs it to run.

Engineering qualification requires: stable coherent probabilities; preserved
label boundaries; unchanged controls; nonidentical UNHCR deployed vectors;
no-regression versus E025 and E041 under prospective .002 skill tolerances;
bounded resources and scoped review. A source-only PASS is a candidate for S2,
not a submission ZIP or final release qualification. Official CLI/assembly/archive
checks remain in S2; source validation uses official score primitives without
importing packaging scripts. No S2 candidate exists until S1 actually passes.

No informative target-domain oracle is available: the observed protected proxies
are reused/incompatible, and VAF is pending. A synthetic oracle would not bound
ERPIS gain. Do not inspect protected labels or manufacture a favorable simulator
to satisfy an oracle formality. Synthetic DEV is repeatedly exposed engineering
evidence, not independent confirmatory evidence or a forecast of Grand.

Hosted arms are frozen prospectively: a confirmed new best is favorable noisy
evidence for this complete configuration; stable Grand/no update is unresolved
and parks it; a worse reported Grand is adverse for this run and preserves E041;
technical failure concerns qualification and does not establish model harm.
No repeat solely for noise reduction, stronger tying (already exact), or tuning
to the outcome. Per-instrument values are optional: if unavailable, use the
Grand-only arm and retain attribution uncertainty. Displayed tie/new-best
inconsistencies require provenance review, not manufactured precise deltas.

## Platform investigation

[Participant guide](A033-outputs/codabench-score-access.ko.md) records exact live
public settings and pinned upstream source. Force_Best and hidden output/detail
settings explain absent controls. Upstream My Submissions renders one primary
score but its authenticated owner-scoped list serializer includes a scores array.
Inspecting the response already delivered to one's own page is a legitimate
possibility; availability on this deployment is unverified. No user login,
private submission endpoint, download or score was accessed by S0.
Do not alter leaderboard state, try administrator endpoints or extract hidden
logs to obtain diagnostics. If no instrument keys are returned, stop and ask
organizers about supported feedback; no contact was sent by this task.

## Role failure: cause, accountability and repair

Primary cause was **assistant execution/authority interpretation**, not a need
for the user to repeat prohibitions. r3 AGENTS/CLAUDE/workflow already said broad
progress language did not switch an established S0. A032 nonetheless treated
"perform all resumption inputs ... start work" as an explicit S1 transition.
An assistant role announcement cannot make that interpretation authorized.
The user's subsequent clarification confirms a separate S1 was expected.

E060/A025 had the same family of error earlier; A026 acknowledged it and A027
added explicit role rules. A032 occurred after those rules existed. Both errors
are visible in this conversation and records, so attributing them solely to a
Claude-to-Codex migration or missing AGENTS would be unsupported.

Contributing document ambiguity: workflow also said "one main conversation by
default" and allowed already-authorized transitions without defining evidence
of a same-chat instruction. Combined with broad progress language and autonomy,
this made over-interpretation easier. It did not cancel the existing prohibition.

**Correction to A032 authority claims:** its entry/record/log characterization
as an explicitly user-authorized S1 transition was the assistant's erroneous
interpretation. Preserve original bytes/manifests and document this dated
correction; public artifacts/exposure remain real, but their existence is not
proof of proper role routing. A032's no-fit/no-submission result remains true.

r4 repairs shared workflow plus AGENTS, CLAUDE and Korean templates:
1. S0 persists across follow-ups; separate S1/S2 is the execution default.
2. Named broad phrases explicitly retain S0. Agent must route, not self-authorize.
3. A same-chat transition/exception names executor and allowed operations; record
   the actual user instruction before crossing the boundary. No magic phrase.
4. Explicit S0 platform research/operating edits remain allowed without opening
   scientific execution. No additional permission ritual for routine S0 work.
5. Ready handoff ends the authoring S0's execution chain. No subagent workaround.

Prompt examples live in [session-prompts](../session-prompts.ko.md), so the user
can use one short S0-retention sentence or an explicit same-chat exception.
These are clarifications, not a technical tool lock. Other live chats must reread
r4; their compliance is not claimed from editing these files. No scheduler,
hook, subagent, global setting or model code was changed.

## Preservation and completion

Existing E041 incumbent/E025 fallback, E057/E060 parked, every STOP including
E058/E059 STOP_SELECTION, A023/A024 HOLD, A_half nonpromotion, A018 unconfirmed
TEST and stopped S3 remain. Prior17999/12339 exposure and A022 original roles,
E059 consumed oracle/selection and protected audit/calibration are unchanged.
VAF application is user-reported pending, not approved; no new VAF data inquiry
or response access in this task. Public Codabench metadata/source exposure only.

Writes: A033 artifacts plus AGENTS/CLAUDE/workflow/session-prompts/status/log.
No scientific execution, fixture/test run, protected response/Parquet/cache
read/hash, model change, experiment E creation, archive work, tree update,
contact/account action, commit/push, S2/S3 or TEST selection. Git status warned
that a global ignore file was unreadable; explicit allowed hashes independently
track preservation. [Final verification](A033-outputs/verification.json).
