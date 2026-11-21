# A021 - Controlled selector comparison contract
date-started: 2026-09-26
status: done
relates-to: E041 / E058 / E059 / A020

## Scope and entry

Technical analysis only, sole owner root. A021 unused at entry; no E060 reserved.
HEAD1d223340d4e1fa3993b411dc5daafab9cb37d0cd. E059 is uncommitted and identified
by its preflight hashes, not HEAD: script31ee84558932e3ef45871c6b53919ec59882044f8fec57ba4635e2242712c5f2;
test746d52ed0de056d5789441c2df6f9bf0c70767638c2b9e765f019bc29e82e65c.
Both match;59 previous source hashes match. No relevant source diff from HEAD.
Existing A020/E059/user changes and tree are protected by entry hashes.
No Python/WSL process observed at entry; no other writer identified.

Session limit12:56UTC..13:56UTC,60min including reading and recording. CPU2,
aggregate2GiB RSS/commitment cap; monitored fixture subprocess only. No actual
fit, response read, real-data prediction/score, cache deserialization, optimizer,
download/install/GPU/paid resource, commit/push, submission or S3. File allowance
is exactly the five A021 paths plus status/log. No production changes.

Question: can P and D share candidate construction, information and decision
rules while differing only in objective? This tests an executable contract,
not selector efficacy. E058 STOP/E059 STOP_SELECTION remain; A_half not promoted.

## Source-derived information flow

| Mechanism | Current R/E041 source behavior | Controlled P/D consequence |
| --- | --- | --- |
| Legacy top10 | dup_link._topk_excl uses default NumPy argsort, last10, then filters nonfinite self; no explicit stable ID tie rule. Selected subset order follows argsort slice, not descending lexicographic order. | Freeze candidate pool identities/order; do not call top10 and top32 interchangeable. |
| Metric top32 | retrieval_oracle.candidate_indices sorts bank positions, sums GIVEN match weights, excludes self, argpartition selects32, lexsort orders selected set by descending score then ascending row ID. Boundary-tie membership is still argpartition-dependent; lexsort does not resolve ties outside the selected subset. | Same frozen pools for both policies; require exact source/version/data order in future execution. No claim of globally ID-stable top32 membership. |
| Selector's old comparator | fit_sections takes first10 of the top32 candidate array, using initial weights. It does not invoke legacy _topk_excl for that comparison. | A controlled P is not exact R, even if it uses marginal scoring. |
| Common weights | _sig_data_all derives rarity from GIVEN; estimate_weights provides common initial weights. Initial weights build metric pools and legacy top10 posteriors. | Any training output/pool construction shared and completed before P/D selection. |
| Learned weights/share | fit_sections fits section-specific weights and retrieval share on fitting queries/reference+.5 prior. Separate inner select chooses activity with gain>max(.003,2*row-SE). | P/D consume identical already-built candidate bundles; neither fits weights on its selection responses. |
| Activity/evidence | Inactive items retain legacy top10; active sections replace evidence with learned-weight posterior over candidate32. Runtime active pools use visible rows, not the earlier reference-only metric bank. | Candidate identity includes both the mask and its evidence procedure; no post-selection candidate creation. |
| Lambda rows | original_cal is visible capped6000(seed0). If any section active, union with replay. Active item lambda uses replay only; inactive item uses original_cal. Original_cal can overlap fitting/reference/inner-select. | Define both inactive and active calibration subsets prospectively and exclude outer selection from both. This changes P from R. |
| Lambda objective | _best_lambda maximizes log(max((1-lambda)*p_model+lambda*p_ev,.001)); p_model is full marginal model replay, not recursively deployed gate output. Grid0,.1,...,.9,.95,.98; strict improvement retains smaller lambda on ties; bucket needs30 rows. Base has already seen visible labels. | Shared lambda procedure stays fixed across P/D. Changing selector objective does not silently repair lambda objective/replay bias. |
| Concentration | _max_q of common-weight legacy top10; threshold>=.5. Used for calibration and deployed lambda pair even when learned top32 replaces evidence. | Freeze bucket from common legacy path. No learned-posterior rebucketing. |
| Base/gates | link_sharp blends ladder/neural full and conditional tables; gate agreement blends hard(parent asked mass times conditional + sentinel) with soft full distribution. Evidence is mixed after this, then stored as belief. Children read that final parent belief. | Full candidate rendering must recurse across sections. Fixed-parent leaf shortcut is invalid if an ancestor changes. |

Source anchors: supervised_retrieval.py:63/124/132/146; dup_link.py:30/50;
link_sharp.py:44/113/196/217; prob_link.py:77; retrieval_oracle.py:6;
logloss.py:floor_mix. These are source observations, not new production runs.
E059 held original lambda/parent fixed and mixed half. Actual section activation
also changes lambda replay eligibility; E059 A_half is not an E041 active mask.

## R/P/D separation

| Property | R, original procedure | P, controlled marginal policy | D, controlled deployment policy |
| --- | --- | --- | --- |
| Candidate universe | Independent per-section old/new proxy decisions, followed by replay/calibration | Fixed ordered whole-output candidate bundles C0,C1,C2,C3 | Exactly P's library, byte identity |
| Fit/calibration | Original internal visible-row splits; base replay in-sample | Disjoint fit/reference/calibration/selection/evaluation group roles | Same as P |
| Score | Section marginal/retrieval proxy | All-head pooled marginal/retrieval score of each complete candidate | All-head pooled recursively deployed score of same candidate |
| Gain/uncertainty | Section .003 and row-based2SE | Fixed .003 mean-log minimum, group-cluster2SE | Identical to P |
| Ties/fallback | Original source rules | Candidate list order; choose maximum then apply both strict guards; else C0 | Identical to P |
| Actual execution here | None | Tiny handwritten tables only | Same tables only |

D-P isolates the objective within this controlled library/procedure. D-R is a
whole-procedure comparison including pools, calibration allocation, activity,
uncertainty and candidate granularity; do not attribute D-R entirely to objective.
C0 is the controlled inactive fallback, not a promised exact R output. P cannot
simultaneously be exact R and satisfy this whole-candidate/group-separated
comparison; this incompatibility is explicit, not an implementation defect.

## Fixed candidate and role contract

Fixture heads s1_parent and s2_child deliberately cross the E041 section regex
boundary. Four masks, ordered: C0 empty, C1 parent section, C2 child section,
C3 both. This is a two-head mechanical library, not enumeration on UNHCR.
Each candidate includes mask, fixed evidence tables, lambda pairs, legacy bucket,
marginal probabilities, complete recursive deployment probabilities and source
role metadata. Handwritten tables stand in for training products; no fitted
generator or optimizer exists. Common retrieval share.5 is a toy constant.

Roles: reference, fitting, calibration_legacy, calibration_replay, selection,
evaluation; all disjoint at group level. Donor IDs must be reference IDs and
cannot be the query. Candidate builder receives only calibration labels and
handwritten probability tables; it rejects labels from any other role. Fitting/
reference roles supply provenance for fixed artifacts, not learned data here.
All candidate rows have identical ordered heads/options and query IDs across
P/D. An empirical implementation must additionally verify actual fitting access.

For each candidate, inactive item lambda calibrates on both calibration subsets;
active item lambda calibrates only on calibration_replay. Both are excluded from
base/metric fitting and policy selection in the controlled design. This mimics
the activity-dependent eligibility relationship, not R's overlapping row sets.
Use original lambda grid, objective and tie policy on fixed full marginal model
probabilities/evidence, with frozen common buckets. Fixture minimum bucket size1
exercises the mechanism on tiny tables; production30 remains an unresolved
empirical feasibility requirement, never lowered to get a real result.

The factory takes no selection/evaluation labels. Compute every candidate's
lambda and both output representations first. Serialize the complete library to
immutable JSON text + SHA256. Selector verifies hash, uses only selection labels,
returns a frozen choice bound to that hash. Evaluation accepts only evaluation
labels and a frozen choice; no callbacks into construction or selection.

P representation: (1-r)*fixed reference marginal+r*candidate evidence per head.
D representation: recursive soft/hard gate mixture then candidate lambda evidence
mix. Thus lambda is fixed for every P/D candidate even though P's proxy does not
score that deployed lambda. No winner-conditioned lambda construction is allowed.
Official normalization then .001 uniform floor precedes log scores in both.
Pool every query/head cell equally. Cluster SE for per-person mean difference m:
sqrt(G/(G-1)*sum_g(S_g-n_g*m)^2/N^2); require G>=2 and m>max(.003,2SE).
No guard relaxation or marginal-specific threshold. Same cell count/ordered
candidates/group boundaries/rules and access rights; both representations fully
materialized under one common compute budget. No asymmetric early stopping.

## Plan and rejected designs

Apply karpathy-guidelines and test-driven-development to this approved design;
plan remains in the permitted A record. First write failing fixture tests, then
pure calculation helpers. Verify immutable candidates, role/group leakage guards,
label perturbation isolation, lambda-zero/unchanged paths, leaf algebra, cross-
section parent propagation, nonadditive whole-output gains, official score,
shared-objective selection identity and a mechanical P/D disagreement example.
Check public schema with the exact grouping regex; count all PREDICT-child gates
with PREDICT parents and cross-section subset. No schema predictions.

Rejected: (1) treating P as exact R despite altered candidate/role/guard semantics;
(2) choosing a mask then constructing its lambda with those same selector labels;
(3) using E059 leaf replacement when parents can change; (4) summing standalone
section gains as if recursive effects were additive; (5) changing .003/2SE while
claiming objective-only attribution; (6) reopening E059 audit or reassigning old
calibration to create a new evaluation. Reasons: confounding, leakage, wrong
recursion or violated exposure contract. No empirical mechanism is rejected here.

## Future empirical conditions - HOLD

No authorized independent role assignment/data channel or production candidate
builder is ready. **Empirical research on hold.** Technical PASS, if obtained,
cannot authorize fitting or a new E experiment. Required before a future study:

1. Preregister exact finite candidates on the target schema, role sizes/group
   unit, candidate construction and all guards before any new label access.
   Four fixture masks are not an empirical UNHCR proposal. Resolve sparse
   calibration buckets with original zero fallback, not a reduced minimum.
2. Validate all base/metric/weight/donor/lambda training uses T/reference/C only;
   fully mask S/E PREDICT blocks first. Freeze all candidate bundles before S.
   Freeze P/D choice before independently authorized E. No post-E policy change.
   Account for candidate multiplicity and two D-P/D-R comparisons prospectively;
   this fixture's2SE guard is not a family-wise efficacy confidence statement.
3. Minimal no-refit comparison design would build one common base pipeline on T
   for P/D, then calibrate on C and select on S. Exact R would need its own
   original pipeline with all development T+C+S visible and E masked. Thus two
   base-pipeline builds, not two neural optimizer calls: existing tuning may
   invoke multiple internal fits, which must be instrumented and bounded before
   approval. P/D share one library; do not fit separately for each objective.
   R has the same overall development information but different allocation;
   that difference belongs to D-R's whole-procedure interpretation.
4. Default proposed evaluation keeps P/D's selected shadow parameters frozen.
   Optional deployment refit adds one shared P/D base-pipeline build on expanded
   development rows plus weight/lambda rebuilding under fixed masks. This
   changes donor availability, training size, buckets and probabilities; selection
   performance is not refit performance. Register refit and evaluate its entire
   procedure independently, without reselection. Not performed or approved here.
5. Profile import, all internal base/metric fits, donor construction, every
   candidate's lambda replay, whole recursive rendering, selection, optional
   refit and all instruments in one shared process; count fits and sample tree
   RSS/commitment. Record failure/fallback and caps before running. No measured
   empirical runtime, memory or gain forecast exists from this fixture.
6. Leak/parity/resource failure stops technical qualification. Valid but absent
   independent roles/cost budget keeps research on hold. A future registered
   positive D-P and D-R independent comparison could support further target
   research, not automatic S2/TEST adoption. Null/inconclusive/adverse outcomes
   follow their original registered arms; no audit rescue or threshold change.

Exposure inherited: E059 oracle1918/1124SSUID and selection2007/1130 consumed;
audit2074/1177 unopened, unavailable for E059 rescue/A confirmation here.
Calibration1866/older roles unchanged. Model use17999people/12339SSUID plus source
aggregate exposure; new seed/chat does not create independent data. Approximate
UNHCR gates differ from the fixture; cross-section edges show dependency paths,
not actual signal strength or evidence that D helps.

## Verification result

**TECHNICAL_PASS for the controlled fixture contract; EMPIRICAL_HOLD.**13 tests
passed in.09s. The monitored verification wrapper took.611116s (tool process
wall.850098s); peak aggregate RSS72802304bytes and commitment42692608bytes.
CPU2 environment and2GiB cap respected. These are fixture checks, not a model
runtime forecast. Full session close time and elapsed cap are in verification.

Public UNHCR schema SHA256
b1175b6bdbd96e90a4defd83af20a38d711c6eca9fe3ce880109ff244abe80d9.
PREDICT-parent edges155; cross-section71, partitioned3->7a:21,3->7b:39,3->7c:11.
One additional PREDICT child has a GIVEN parent. All71 cross-section connections
come from s3_11_intent_return_12m_lbl. Counts match the previous S0 definition;
they are neither pass criteria nor effects. Complete edge list in verification.

Mechanical counterexample: same frozen library chooses C1 under P and C0 under D.
Labels and probability tables were directly written, including a selection
parent/child response combination that need not obey the toy exact gate. This
is a mechanics example, not a data-generation model, prevalence estimate or
evidence either policy improves UNHCR. The example can favor either representation
by construction; no empirical conclusion or favorable-seed search follows.
Same objective/rules/library gives identical choices. Parent and child changes
produce nonadditive whole-output gains in the separate handwritten fixture.

Isolation checks reject forbidden calibration labels, query donors and crossed
role groups. Library serialization breaks mutable input aliases; hashes reject
post-freeze edits. Evaluation-label changes affect only fixture evaluation, not
candidate construction or selection. This does not certify an unimplemented
training data pipeline; real fitting, actual probabilities and full production
source/assembly parity remain untested. Manual probability tables cannot detect
hidden upstream label use in a future implementation; that requires instrumentation.

Original lambda formula and official score.py:474 normalization/floor were
checked from source; fixtures call newly written scalar arithmetic only. No
production model function, optimizer, old cache or prediction/score array opened.
All real fit/response-read/prediction/score counters0. Expected missing-module
test failed first; the completed13-test suite passed on its first full run.

Executed computational commands:

```powershell
.venv/Scripts/python.exe -m pytest tests/test_a021_selector_contract.py::test_module_exists -q
.venv/Scripts/python.exe scripts/check_a021_selector_contract.py
```

First command is historical RED before implementation. The checker runs only
the new fixture tests and reads public schema/source hashes; it never resumes a
study. No new dependencies. Final script SHA256
855b3c165eacb289693706bbe820899c2a4c2c586aec35cb72da67264ad97456;
fixture SHA25638c55742e6da09a3bc7a0b87321ae5977f522440b586e476884045df9ac4dc3c.
New files: this contract, scripts/check_a021_selector_contract.py,
tests/test_a021_selector_contract.py, A021-outputs/verification.json and
A021-outputs/s0-handoff.ko.md. Only status/log additionally changed this session;
the prior dirty tree belongs to E059 and was not regenerated here. Hashes and
working-tree state are recorded in verification.json (excluding its self-hash).

E041/E025, E057 parked, earlier STOPs, S3 stopped/A018 unconfirmed and no-S2 state
preserved. HEAD unchanged; all work deliberately uncommitted, no push. Next S0
must decide whether independent data/roles, real candidate construction and a
bounded full-procedure cost plan are available. Until then, hold empirical work;
no automatic experiment, E060 reservation, audit opening or A_half promotion.
