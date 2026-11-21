# WB76 TabICLv2 contract — fixed proposal

2026-10-26. Candidate identity: `WB76-TABICLV2-GLOBAL-01`.
**PROPOSED / MODEL_EXECUTION_NOT_AUTHORIZED.** This is an S1 information result,
not an E registration, implementation, technical PASS or scientific allowance.
The [batch proposal](proposed-batch.ko.md) fixes the prospective execution envelope.
Current readiness: **MODEL_BATCH_NOT_EXECUTION_READY / DEPLOYMENT_SPECIFIC_INPUT**.
The pre-fit gate below is an unresolved input, not a recommendation to approve or
start the420min batch now.

## Decision, novelty and evidence

Test one different pretrained tabular prior over all76 WB PREDICT distributions,
mixed with the actual final E041 probabilities. UNICEF and UNHCR remain E041
exact controls. This is a distinct WB population/input/selection procedure, not
a reduction of A040's frozen UNHCR213 policy to rescue its timeout. E062 changed
16 ordinal heads inside a shared network; this proposal changes none of those
network definitions. A040 HOLD/LOCAL_RESOURCE_LIMIT and E062 parked stay intact.

Potential complementarity is unmeasured. E012's joint-learning benefit is
counterevidence to separate heads; E048's negative standalone results and E049's
oracle-to-selector gap are counterevidence to assuming a pretrained expert helps.
The user's leading WB.50 is a noisy public comparison, not an oracle or recoverable
gain estimate. No new TabICLv2 oracle, independent audit, effect or win forecast exists.

Evidence reused, without rerunning or opening numeric/model artifacts:

- [A040 contract](../../A040-outputs/s1/contract.md),
  [observation plan](../../A040-outputs/s1/observation-plan.md),
  [costs](../../A040-outputs/s1/cost-accounting.md),
  [source register](../../A040-outputs/s1/source-register.md).
- [Tiny retry1](../../A040-outputs/local-technical-retry1/closeout.md): local
  class alignment/one-load/shared-state checks, including K15/K11; not K26/full cost.
- [RTX full path](../../A040-outputs/full-path-resume1/closeout.md): E041 reference
  and completed control/final-R parity, but candidate stopped at900s before final
  expert/output/state checks completed. These narrower facts remain narrower.
- [Runtime-policy resolution](../../A040-outputs/s0-policy-resolution/decision.md):
  user-supplied organizer clarification already permits delivered-visible fitting,
  internal selection/check and refit. The old policy ambiguity is not reopened.
- E062/E064 S2 closeouts and E064 numeric-identity record supply historical release
  costs and named synthetic identities, not a GPU baseline or permission to read them.

## Frozen assets and environment boundary

Comparator R: `submissions/2026-09-19-E041/main.py`, inherited SHA256
`22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073`.
Release baseline: `submissions/2026-09-09-E025/main.py`, inherited SHA256
`00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9`.

Reusable adapter: `docs/analysis/A040-outputs/full-path-resume1/adapter.py`.
Related static composition: `orchestration.py`, `observer.py`, `schema_entry.py`
and `runner.py` in that directory. They are research prototypes. Existing UNHCR
dispatch, role mapping,426-call assertions and output labels must not be reused
as WB semantics. New implementation is prospective and preserves old files.

TabICL2.2.0 source pin: `0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3` at
`tmp/a040-local-technical/source/tabicl-0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3/src`.
Checkpoint: `tmp/a040-local-technical/acquisition/tabicl-classifier-v2-20260212.ckpt`,
HF revision `4dcd344ece2c00be9e831fdd35bed57b5ad83e19`,110368038bytes, inherited
SHA256 `bdc7dbd5e4ff21f8f0456fcf90c6b7cdf72dbea960f2d05b19bec19f9b3d4ed0`.
Code BSD3 and weight BSD3 evidence are separate; retain both notices/provenance.
No weight bytes, package imports or live environment were inspected here.

Proposed model interpreter: `tmp/a040-local-technical/venv/Scripts/python.exe`,
the34 pins in A040 `full-path-resume1/requirements.lock.txt` (historically
Python3.13.14,torch2.8.0+cu126,numpy2.2.6,pandas2.2.3,scikit-learn1.6.1).
Proposed controller/scorer: existing `.venv/Scripts/python.exe`; historical E064
preflight records PyArrow25.0.1. These are two explicit roles, not equal environments.
The official scorer's `--python` argument can use the model interpreter; its
driver receives staged JSON and does not require PyArrow. Actual identities and
availability must pass the future entry gate. No install, environment replacement,
GPU fallback for the expert, cloud or dependency download is proposed implicitly.

At candidate module import load one verified local checkpoint, before any
instrument call and after network isolation. `allow_auto_download=False` and
explicit local path; no training optimizer for expert weights. Fresh per-head
encoders/contexts, shared immutable model/config only; clear caches between heads,
sequential estimators, no KV cache or persisted response-derived cache.

Frozen expert settings: n_estimators8; norm_methods none,power; feature shuffle
latin; class shuffle shift; seed42; temperature.9; average_logits true;
support_many_classes true; batch_size8; kv_cache false; cuda; AMP true; FA3 false;
offload false; n_jobs2; verbose false. No context/head/ensemble/seed/temperature sweep.
The hierarchical K>10 path is required, not permission to drop large-class heads.

## Public WB schema and complete output

Direct public `external/starter-kit/data/world_bank.json` accounting:
106 items =9 GIVEN+76 PREDICT+21 EXCLUDE;30 PREDICT gated;655 complete probability
columns;max K26;19 heads with K>10. The40 gates across all schema items include10
EXCLUDE gates. TRAIN5195/DEV520/TEST1212; phase1 WB39520 vectors.

Complete-K histogram:3:3,4:5,5:12,6:12,7:18,8:2,9:1,10:4,11:3,13:6,14:3,
15:2,18:1,25:2,26:2. Counts derive from declared values plus sentinel for gated
PREDICT items; they do not describe observed label frequencies.

GIVEN in schema order: group,user.age,user.gender,user.country,user.educationLevel,
user.hadJob,user.employmentStatus,user.wageOfSimilarEmployees,user.lowestAcceptablePay.
No key, role, other PREDICT, asked indicator or target-derived feature. WB describes
individual job seekers with self-report, timed tasks and follow-up components;
content nonresponse and gate sentinel are ordinary outcomes, not interchangeable.
All GIVEN features remain categorical under the frozen adapter, including bin labels.

Use current approved official load_config/load_schema/options_for semantics.
Raw WB JSON lacks `gated_value`; never guess it. Record raw schema/config/loader
identities separately from canonical runtime schema/options/order. Sentinel is
the final slot only when that PREDICT item has a gate. EXCLUDE stays out.

For each head map labels to complete schema indices, then scatter predict_proba
through integer `classes_`; absent observed classes receive raw0. One observed
class uses a full-width one-hot without neural context call. Zero usable context
returns the retained R head exactly; all-constant GIVEN, invalid/NaN fit labels,
bad classes/alignment, invalid probabilities or partial visibility are technical
errors, not occasions to invent labels or quietly shrink the policy. Unknown or
missing query GIVEN uses the F-fitted encoder's existing -1 route; no query fit.

Return raw valid vectors in original row position then schema PREDICT order.
Normalize R/q only for active mixing: `(1-alpha)*R + alpha*q`. Mixture occurs
after E041's final complete-distribution rendering; no subsequent gate rerender.
Scoring applies exactly once `.001+(1-K*.001)*p_normalized`; predictor returns
unfloored probabilities. Alpha0/rejected/small-visible/control branches return
original E041 lists with no normalization, reconstruction or new rounding.

## Fixed WB roles and decision

This proposal deliberately selects S1000/E1000, leaving F3195 of5195 visible rows.
One common alpha has only three choices, while1000 E respondents permit a
respondent-level paired guard. The tradeoff is39% of visible rows withheld from
shadow context, versus24% in A040. No claim that this split is optimal, sufficiently
powered or representative of the refit is made; no data-dependent resizing.

Identify visible rows solely from complete delivered PREDICT blocks. Sort original
positions, then one local `numpy.random.Generator(PCG64(4501)).permutation`;
first1000 S,next1000 E,remaining F. The new fixed seed identifies this prospective
WB procedure, not fresh exposure. Within each model context/query use original
sorted positions. Fewer than2001 complete visible rows: exact all-visible E041
fallback; no expert contexts or smaller split. Partial target blocks are invalid.

Before any shadow E041/helper/encoder sees data, mask the ENTIRE PREDICT block
outside F, including S/E/external query. Seal S/E labels in scoring-only buffers.
Expert shadow: F3195,ordered S+E2000 GIVEN queries. E041 shadow: F3195,all2520
masked query rows; retain only S/E probabilities. No query batch-invariance claim,
chunking change or answers from external DEV. Each of76 heads gets all eligible F.

After both fixed shadow outputs complete, open S once. Select one global alpha
from `{0,.25,.5}` by pooled once-floored log score over1000x76 cells; ties select
the smallest alpha. Freeze alpha before opening E once. For each E respondent,
`d_i` is mean over76 floored log-probability differences versus shadow R.
Accept only alpha>0 and `mean(d)-1.645*sample_sd(d)/sqrt(1000)>0`; zero variance
requires strictly positive mean. No E oracle, bootstrap search, extra grid,
head/router selection or threshold rescue. This approximate normal guard is not
a finite-sample95% guarantee; correlation within respondents is retained, and
cross-respondent independence is an assumption, not newly verified household data.
Approximate80%-power detectable log gain is2.487*sd(d)/sqrt(1000), with sd unknown.

Rebuild final E041 on all5195 visible rows regardless of decision. If accepted,
rebuild each expert context on all5195/query520 and retain selected alpha. Otherwise
skip final expert and return exact R. Refit context differs from shadow; E checks
the shadow procedure, not an independent final-refit estimate. Query answers never
open. UNICEF/UNHCR use E041 unchanged; local RNG objects and isolated definitions
must prevent TabICL import/selection from altering control RNG/global bindings.

The maximum S score is at most an optimistic selection-set bound for this fixed
three-alpha family. No fresh oracle currently exists and no E hindsight oracle
is allowed. Public DEV evaluates the whole guarded procedure; internal E is not
public DEV or a fresh external audit. Hidden activation may remain unknowable.

## Prospective qualification and deployment gates

New tiny checks target the actual changed boundary: all19 many-class heads/K26,
class omissions, K26 stock-versus-injected equality, shared-state isolation,
cross-role masking/sealed E, categorical unknowns, exact alpha0/small-visible
fallback, canonical ordering, import/RNG controls and floor-once arithmetic.
Do not repeat unchanged A040 K15 suites as fresh evidence. API checks do not prove
general isolation; actual full-path role instrumentation is also required.

One fresh full-shape engineering family exercises every declared class in fit
and scoring roles, including K26, with seed4500. It is generated once only after
authorization; query PREDICT truth is never generated. Dimensions match all three
phase1 instruments. Fixed control reference and maximal candidate each run once.
Force alpha.25 only in a separately named engineering output to exercise final
expert even if natural fake selection rejects. Reuse the same final R/q for
inactive/empty arithmetic, no extra full fit. Natural and forced outputs remain
distinct; fake gain is not efficacy. Require full189649 vectors, all controls/
fallback exact, input and frozen model-state preservation, complete counters and
whole-process resource PASS. A partial900s run does not qualify.

Scored release uses only the three explicitly named historical synthetic Parquet
files in the batch proposal. Fresh GPU-compatible E025/E041/source outputs are
required; old CPU NPZ outputs are not reused. Whole source/assembly/extracted raw
parity, controls exact E041, E025 absolute skill difference<=.002 each instrument
and candidate-E041>=-.002 each instrument, ZIP checker and stock score.py all3
shared900s are mandatory. This is exposed synthetic engineering/no-regression,
not an independent audit or target-population efficacy claim.

Deployment feasibility is an ENTRY gate before any checkpoint deserialization,
new model fixture or fit, not an issue first investigated after full-path costs.
Inspect existing source/metadata and retained official environment evidence only.
The current record does not yet establish the hosted psutil dependency; absent
complete evidence, return DEPLOYMENT_FEASIBILITY_HOLD without spending model calls.
Do not infer that a package absent from a published list is actually absent.

If that entry gate passes, bundle pinned TabICL source/checkpoint and
notices; load offline at import; establish required installed/vendored dependencies
and platform compatibility. A040's Windows pin inventory is not a Linux/H100 build.
In particular einops/psutil/tqdm are required upstream but not all expressly
guaranteed in the retained hosted package list. Stock score.py creates and installs
a fresh venv for nonempty requirements.txt. The only additionally proposed
pure-Python vendoring sources are existing
`tmp/a040-local-technical/venv/Lib/site-packages/einops` and `tqdm`, with their
`einops-0.8.1.dist-info` and `tqdm-4.67.1.dist-info` metadata/licenses. Their actual
source/license identities and import closure must be established at future entry;
no bytes or legal sufficiency are asserted here. This does not permit vendoring
psutil native binaries, replacing its API, or removing upstream imports.
Do not bypass the stock scorer, silently
remove required dependencies, copy Windows native binaries for Linux, or claim a
build was tested. With this no-install envelope, unresolved entry evidence yields
DEPLOYMENT_FEASIBILITY_HOLD before new model work; a subsequently discovered
deployment defect yields DEPLOYMENT_HOLD before a release-qualified ZIP. That is a concrete
possible stop, not an implicit environment/cloud repair allowance.

Minimum resumption input is either current authoritative hosted dependency
evidence covering required compatible psutil and the remaining import closure
(with any permitted pure-Python vendoring identities/licenses established), or
a separately authorized finite isolated installation/deployment-validation scope
that makes the stock scorer and package dependency path concrete. Neither input
is supplied by this task. No additional lookup, install or model work is launched.

All E041/E025, parked policies, STOP/HOLD,17999/12339 and aggregate/A022 roles,
E059 consumed oracle1918/1124 and selection2007/1130, protected audit2074/1177 and
calibration1866, A_half nonpromotion and A018 unconfirmed remain unchanged.
S3/TEST, upload, license grant and commit/push remain separate user decisions.
