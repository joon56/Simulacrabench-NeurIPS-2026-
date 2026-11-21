# E062 — WB16 ordinal conditional heads
parent: E041
status: parked
date: 2026-10-07

## Registration before implementation and scores

State: REGISTERED, not qualified/adopted. Current user delivered the A041 S0
implementation handoff to this S1 and explicitly designated World Bank. Preserve
all prior research, dirty work and STOP/HOLDs. No E062 record/output/source collision
at entry. The A041 contract is fixed, SHA256
c65c4eb4eb75a1a15fda8416c5c7988f6ef47464460ac9b195201675cac20ca8.
Initial registration is distinct from the later executable/source/input/split freeze.

## Question, mechanism and domain check

Can one WB16 affine conditional-logit head procedure preserve the two E041 control
instruments and pass full-output, engineering regression and local cost contracts?
Public score-bin ordering motivates the functional family, not equal distances,
unimodality, nonresponse semantics or known headroom. Ordinary softmax is already
a valid distribution. This is distinct from E011 post-hoc smoothing, E030 GIVEN
distance, and E061 UNHCR tying. E011 null and all prior verdicts remain.
Nonresponse factorization, asymmetric initialization, trunk spillover and config/w/
lambda decisions jointly change; no isolated causal claim about ordering.

Fixed targets: sc_nstd_{extra,agree,consc,stability,open,gm,pp,s_aware,s_manage,
soc_aware,realistic,invest,artistic,social,enterp,convent}. All16 are ungated PREDICT.
Exact order: <2.5,2.5-3.0,3.0-3.5,3.5-4.0,4.0-4.5,4.5-5.0,Not answered.
WB schema mismatch is a stop, never a partial-head rescue.

## One immutable candidate policy

Five logits t, nonresponse logit g. r=sigmoid(t), m=sigmoid(g), S0=1,
Sk=product(r[:k]), S6=0; qj=S(j-1)-Sj, pj=(1-m)qj, pM=m.
Use stable log-sigmoid prefix sums as seven full-head logits. Cross entropy remains
one categorical NLL per cell; keep pooled denominator including existing conditional
auxiliary cells. No new floor/clamp/prior/smoothing/loss or head fallback.
Create entire original nominal net first; copy target rows0..4 and6 without new
random draws, discard row5. Trunk/non-target parameters and RNG remain exact.
Sparse/empty risk sets have unidentified content parameters, not a new fallback.

Preserve configs(64,2,0)/(128,2,.1), torch seed0, Adam lr.003/weight_decay.0001,
500epochs/patience30/improvement1e-5, outer Bernoulli.2 seed0 and inner.2 seed1,
strict config ties/order, w grid0:.1:1 and existing ties, final all-visible refit
(also when w0), ladder/gate/donor/lambda minimum30/zero fallback. No intermediate
outer-fit refit. WB60 other outputs may change. Exact E041 UNICEF/UNHCR controls.

## Channel and roles

Only three already-exposed starter-kit _sandbox respondents.parquet files are
authorized for hash verification and TRAIN/DEV reads. Exact hashes in entry.json
come from the user and E061 frozen-inputs metadata. Parquet filters request only
TRAIN/DEV; no TEST row values/analysis. Complete query PREDICT masked before model
entry; EXCLUDE removed; GIVEN-only model features. DEV truth stays evaluator-only.
Inner training/stop/outer selection/final refit roles follow unchanged production
rules. Lambda replay reuses fit labels; not independent validation. Synthetic is
engineering, not actual WB efficacy or an upper bound. No fresh target oracle.
Adult/SIPP/VAF/protected roles/old caches or predictions remain inaccessible.

## Frozen gates and ordering

1. New affected tests only, small tensors/backward, no optimizer fit: seven-output
   math/order/sum, extremes +/-1000, finite logp/gradients, sparse/empty risk sets,
   Not answered gradient, exact NLL/pooled count, mask, both configs' untouched
   parameters/RNG, inactive and existing small-fit fallback. float64 atol/rtol1e-10;
   float32 atol1e-6/rtol1e-5. Original parameter/RNG equality exact. No tolerance rescue.
2. After PASS freeze source/input/runtime schema/split identity/deadlines. Clean
   E025, clean E041, candidate each all3 once in separate fresh processes, no cache.
   Freeze all nine raw outputs before any engineering score. Expected vectors:
   UNICEF17856, WB39520, UNHCR132273, total189649 per procedure. Schema order, shape,
   finite/nonnegative/positive mass, sum error<=1e-6. Controls max raw difference0.
3. Only then official in-process normalize/floor(.001)/score. Candidate-E025 AND
   candidate-E041 skill>=-.002 for every instrument. WB whole skill/log score is
   primary; fixed16/other60/Not answered breakdowns descriptive only. No +.005 gate,
   synthetic gain requirement, head selection, new seeds or result-dependent policy.

EXPLORATORY_SOURCE_QUALIFIED requires technical/parity/resources/regression PASS
and at least one exact changed WB vector. All same: NO_OP. Technical defect:
TECHNICAL_FAIL; cap: RESOURCE_LIMIT; regression: REGRESSION_HOLD; missing validation:
INCOMPLETE. Small losses are reported. No iid-cell significance or power claim.

## Aggregate costs and stop policy

Conservative gross budget start2026-10-07T12:39:40Z, rounded before first observed
entry read (first returned clock12:39:56Z), no waiting deductions. Deadline14:39:40Z;
computation cutoff14:29:40Z leaves10min records. CPU numerical threads2/GPU0/heavy1.
Owned controller+descendants RSS and private commitment each<=8GiB; sample.1s using
existing Windows MemoryTree. Parent monotonic plus absolute deadline watchdog.
Candidate fresh worker startup/import through all3<=900s. All computational child
wall, including failed tests/preparation/scoring, cumulatively<=1800s. Pipeline
attempt<=9, neural _train_on attempt<=27, all failures charged. Other selection,
metric, render and validation costs included. Nested spans are not added to wall.
Existing monitor source is reused, no new infrastructure/environment.
First scientific error stops its owned worker. Ordinary implementation repair and
affected verification remain in this session under r5, only within remaining fixed
budgets/attempts. No successful unchanged repeats, new policy or fit allowance.

## Deliverables and disposition

New wb_ordinal_heads.py, focused tests/check script, E062 outputs: entry/registration,
freeze and raw identities, call/resource/error ledgers, comparison, verification,
exposure/closeout/S0 handoff. No original model/snapshot/tree edit, ZIP/remote/install/
commit/push/subagent/S2/S3. S0 reviews before any S2; source/assembly parity, ZIP
checker, official all3 release, clean release comparisons and SCORES arms remain.
E041 incumbent/E025 fallback; E057/E060/E061 parked; E058/E059/A039/A040/all STOP/HOLD,
17999/12339/A022/consumed and protected E059 roles, A_half/A018/S3 states preserved.

## S1 result — 2026-10-07

EXPLORATORY_SOURCE_QUALIFIED on the registered synthetic engineering channel;
status remains parked pending S0 review. No release qualification/adoption.
Thirteen affected tests pass; initial expected RED preserved. Nine pipelines,
twenty-seven neural fits, sixteen metric optimizers; all nine outputs frozen
before evaluator scores. Controls exact E041, WB35613 vectors changed.
Whole-WB skill+.0002723772 versus E041/E025; target16 log score-.0007987550,
other60+.0009093584. UNHCR-E025-.0004861448. All fixed -.002 gates pass.
Target16 decline prevents interpreting the aggregate gain as ordinal efficacy.
Candidate all3 startup/import through exit357.522443s<900s; computational child
wall1123.196596s<1800s. CPU2/GPU0, RSS/private below8GiB. No further fits.
[Closeout](../analysis/E062-outputs/closeout.md),
[Verification](../analysis/E062-outputs/verification.json),
[S0 handoff](../analysis/E062-outputs/s0-handoff.ko.md).
Immutable initial registration remains in E062-outputs/registration.md. No
policy/seed/head/grid/tolerance change; no old source/snapshot/tree modification,
ZIP/remote/commit/push/S2/S3. All prior STOP/HOLD/exposure/TEST states retained.
