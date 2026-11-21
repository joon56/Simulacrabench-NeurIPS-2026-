# E061 — Tied full and conditional neural heads
parent: E041
status: parked
date: 2026-09-27

## Prospective registration and authority

S1 bounded exploratory DEV research, synthetic technical qualification only.
User supplied attachment619cfbe7-712b-4748-9ce1-9c4366b23648 with instruction:
"이 별도 S1 채팅에서 아래 범위의 구현·합성 기술 검증을 실행한다."
This receiving conversation previously executed S1 A030; it is not the A033
authoring S0. Writing an S0 delivery prompt in chat did not execute S0's task.
Executor root; no delegated writer or fit. E061/tied_content_heads names clear.
HEAD1d223340d4e1fa3993b411dc5daafab9cb37d0cd. Existing dirty work protected.

Started2026-09-27T12:23:01Z; session deadline14:23:01Z (120minutes).
Actual ordered tool reads: AGENTS, CLAUDE, status, newest A033/A032/A031 log,
workflow r4; A033 decision/candidate-inputs/verification/score-access guide.
Required E012/E029/E041/E056/E060 and shared_trunk/supervised_retrieval/
link_sharp/hh_cap plus frozen E041/E025 snapshot source inspected.
Workflow SHA256 a83c6f4102f50d0b8919f0f2010acfd19954901e8e2a08e7771ef87831741642.
Read evidence is actual Get-Content/rg output this session; hash alone is not
evidence of reading. Entry26 candidate hashes and all3 synthetic hashes match.
No selected research worker observed; two persistent Codex processes exist,
which alone neither prove a competing writer nor provide a global lock.
A033 status says its S0 task complete. Stop on observed competing writes/jobs.

## Hypothesis, domain and oracle boundary

Separate full and conditional heads may encode inconsistent ordinary-answer
relative probabilities from identical GIVEN features. Sharing their logits
removes parameters and may regularize; lost flexibility may instead hurt.
No observed real-data harm from this discrepancy has been established.
Actual ERPIS gates are approximate; sentinel remains learned, never forced by
schema. Synthetic gates are exact and cannot test that target mechanism.

This is not E056/E057 independent trees, E060 retrieval-target fitting, A023
selector objective or E029 seed/temperature tuning. Prior STOPs remain binding
for those studies. No informative ERPIS efficacy oracle is available. Public
metadata/synthetic truth do not upper-bound target gain; protected proxies,
audit/calibration and pending VAF responses are not available for rescue.

## Fixed candidate and implementation plan

One new module src/models/tied_content_heads.py. UNHCR dispatch uses original
E041 marker s3_11_intent_return_12m_lbl; UNICEF/WB delegate original E041 source.
Original link_sharp.predict's tune_fn hook injects a local training procedure;
original supervised_layer, renderer and hh_cap.CONFIGS remain unchanged.
No global monkeypatch or production source modification.

Neural full heads and trunk retain existing structure. Conditional logits index
the ordinary full-logit columns by schema meanings, excluding gated_value.
Compute softmax on logits, never divide by small ordinary probability mass.
Keep original pooled full+asked-only CE and denominator via shared_trunk helper.
The tied class uses original trunk/full-head constructor with no conditional
Linear modules. Removing those modules changes RNG consumption before dropout;
seed remains0. This is a deterministic consequence of tying, not a seed search.
Ungated UNHCR outputs may change via trunk learning. No raw sentinel-preservation
or final-mixture coherence claim. Validate all213 PREDICT heads.

Keep configs(64,2,0.0)/(128,2,0.1), LR.003, weight_decay.0001,
max_epochs500, patience30, early improvement1e-5, torch seed0,
outer holdout seed0/fraction.2, inner seed1/fraction.2. Copy only the necessary
train/tune wiring; preserve original config/w selection, all-visible refit and
CPU/GPU fallback algorithm. This session disables GPU. No extra fitting family.
Original ladder, donor ordering/ties, metric objective/optimizer50, grids,
lambda minimum30/zero fallback and recursive renderer retained. Recomputed
lambda may differ: whole-pipeline comparison, not frozen-lambda or D-P.

1. Write new focused invariant tests first; record expected RED without model.
2. Implement mapped tied heads/local train hook; run only new focused tests.
3. Review preserved arithmetic/role boundary; freeze implementation/tests/harness
   and input hashes before actual synthetic predictions or score access.
4. One bounded worker, candidate all3 then E041 all3 then E025 all3. Persist all
   vectors and prediction hashes before any DEV score. No existing cache reads.
5. Apply fixed criteria below; preserve results and prepare scoped closeout or
   S2 source handoff. No assembly/package/official CLI release run in S1.

## Data and evaluation roles

Only external/starter-kit/_sandbox/{unicef,world_bank,unhcr}/respondents.parquet,
byte identities verified against E057 preflight. Filter rows to TRAIN/DEV on
read; no synthetic TEST evaluation. No download/regeneration or alternative seed.
Use official sample_rows phase1: TRAIN visible, all DEV PREDICT blanked. Models
receive only masked frame/schema; external truth stays in harness, never model
features/selection/refit. DEV truth scored only after all vectors are frozen.
Existing synthetic DEV is exposed engineering material, not a new audit.
Small fabricated tensors/rows test invariants only, not empirical effects.

## Fixed acceptance and resource contract

- Neural conditional identity within1e-6; reversed ordinary option order,
  sentinel position mapping, extreme logits, shared gradients, asked mask/CE
  denominator, whole-block held-out isolation and control dispatch tests.
  Test-only mocked training makes no full-stack empirical calls; count gradient
  checks separately. No rerun of unrelated old fixtures.
- Compare frozen E041 snapshot2026-09-19 and E025 snapshot2026-09-09: at most
  one phase1 full-stack call per instrument/model,9 maximum. Use official
  check/floored/score functions only; no CLI, environment installation or ZIP.
- Every vector passes shape/finite/nonnegative/positive total and normalized
  sum within1e-6; official floor. UNICEF/WB max absolute candidate-E041<=1e-10.
  At least one final UNHCR vector differs>1e-10; otherwise NO_OP, no forced path.
- Per instrument candidate skill>=E025-.002 AND >=E041-.002. Prospective
  exploratory regression policy, not significance/efficacy proof; no +.005 gate.
- Candidate all3 measured wall<=900s including worker startup/imports and its
  calls. Entire computational worker wall<=1800s cumulative, including failed
  attempts and focused-test workers;120minute session bound. Full-stack calls9,
  neural training invocations27 maximum across attempts (2configs+1refit normal).
  Record actual epochs, metric optimizers, fallback attempts and phase times.
- CPU numerical threads2, no GPU/paid resource/install, one heavy worker.
  Owned controller+descendant process-tree RSS AND private/commitment<=8GiB.
  Windows MemoryTree counters sampled every.1s; sum per-process peak counters
  is conservative, not instantaneous whole-system RAM. Prelaunch monitor must
  work. Failure/cap stops only owned worker tree, preserves logs/results.
  Parent checks absolute deadline/worker wall; candidate stage watchdog checks
  its900s cap. No unmeasured resource PASS or H100 guarantee.
- STOP/TECHNICAL_FAILURE/NO_OP on failure, cap or data conflict. Only a proven
  implementation/harness defect permits documented retry within SAME cumulative
  bounds; no result-driven loss/head/seed/threshold modification.
- Passing means EXPLORATORY_SOURCE_QUALIFIED only. E041 remains incumbent;
  S2 assembly/source parity, ZIP checker, official all3 and total package cost,
  SCORES preregistration/provenance remain outstanding.

## Hosted readings, backup and preservation

Confirmed new best: favorable noisy evidence for whole candidate, S0 review.
Same Grand/no update: unresolved, park candidate. Lower Grand: adverse reading
for run. Failure/timeout: technical arm, not statistical inferiority. Optional
official instrument scores only; no reverse inference from Grand, no identical
noise-reduction resubmission or tuning. No automatic adoption/TEST selection.

On main STOP, backup only<=30minute failure/resumption/preservation closeout,
within session cap. No other model or VAF search. VAF application user-submitted,
approval pending. Prior17999people/12339SSUID and A022 original roles retained;
E059 consumed oracle1918/1124, selection2007/1130; protect audit2074/1177 and
old calibration1866. E041 incumbent/E025 fallback, E057/E060 parked,
E058 STOP/E059 STOP_SELECTION, all STOP/HOLDs and A_half nonpromotion remain.
A018 TEST user-unconfirmed, S3 stopped. No S2 candidate until qualification.

Only new module/test/check script/E061 record/outputs plus status/log writes.
No old model/snapshot/tree edits, no caches/real responses/key hashes, no
assembly/CLI release/ZIP/upload/commit/push/S2/S3. Tree link intentionally deferred.

## Results and disposition

Original registration remains byte-identical in E061-outputs/registration.md.
**EXPLORATORY_SOURCE_QUALIFIED** after9 focused tests and one frozen all3 comparison.
UNICEF/WB candidate-E041 raw difference0. UNHCR132225/132273 changed vectors;
skill.562391878130 versus E041.562462728858 and E025.562948873705. Both deltas
within registered-.002 bounds, but synthetic gain is not observed. Every vector
passes official check and registered normalization tolerance. No ERPIS efficacy
or neural-identity-at-final-mixture claim.

Candidate whole-stage340.093s; scientific worker1083.500s; cumulative test/fit/
evaluation workers1098.523s. Full-stack9/neural27/metric16 calls. Peak conservative
owned-tree RSS1.991GiB/commitment1.514GiB, threads2, CPU only. No scientific retry.
Actual call/epoch/selection/refit records, complete comparisons, source/data/split
hashes and preserved boundaries: [closeout](../analysis/E061-outputs/closeout.md).

Local technical/regression/resource gates PASS. DEV: qualified exploratory
source for [S2 release validation](../analysis/E061-outputs/s2-handoff.ko.md),
not package-ready or adopted. TEST: unselected. E041 stays incumbent, E025
fallback; all earlier STOP/HOLDs preserved. No S2 execution, ZIP, upload,
commit/push or tree edit. No backup triggered after main qualification.

## Hosted result supplement — 2026-09-29 KST

Original registration, S1 disposition and subsequent S2 release records remain
historical and unchanged. User-supplied API result ID949956, Finished,
Development/phase29772, filename2026-09-28-E061.zip, created
2026-09-28T13:57:41.742034Z (22:57:41.742034KST).

Grand API.6400000000 / UNICEF.52 / WB.49 / UNHCR.91 versus E041 ID933094
.6433333333 / .52 / .49 / .92. Released differences Grand-.0033333333,
UNHCR-.01; controls' reported scores equal. Both screen Grands rounding to.64
does not make the API results equal. Matching phase/status/score keys support
the registered **Comparable Grand decline** arm: adverse for this fixed run.
Both sources are user-supplied API records, not independently fetched;
uploaded bytes/hash and identical hosted scorer versions remain unverified.

DEV: E041 incumbent/E025 fallback, E061 parked. No readable new best over E041;
no separate best-update event supplied. TEST: unselected, no promotion; A018
user-unconfirmed, S3 stopped. No exact unnoised effect, identical target
predictions, isolated tying mechanism or universal hypothesis refutation follows.
Technical/synthetic release PASS is distinct from absent hosted improvement.

[SCORES](../../submissions/2026-09-28-E061/SCORES.md),
[API object](../analysis/E061-outputs/s2/user-reported-949956.json),
[result/provenance](../analysis/E061-outputs/s2/post-result.json),
[S0 result handoff](../analysis/E061-outputs/s2/post-result-handoff.ko.md).
No fit/predict/score/revalidation, model/ZIP change, same-policy retry or tuning.
All original exposure/STOP/HOLD boundaries retained; no tree edit/commit/push.
