# E057 — Honest UNHCR leaf-content selection and refit
parent: E056
status: parked
date: 2026-09-25

## Session contract and user authority

Input/current HEAD9284bf4d277e339a9ae4a334d6cf7ee7bde2c6ba, branch
work/e050-submission, no difference from requested baseline. No E057 collision;
reserved by this S1. Existing .gitignore, .claude/skills/paper-session/SKILL.md,
.claude/settings.local.json and trip/ are user-owned and preserved. Entry
Get-Process found no python/wsl job. Research clock begins08:56UTC, stops by
10:26UTC (90min). One heavy process, CPU2threads, no GPU/paid resource/download,
cumulative fit wall1200s and own process tree memory8GiB. No automatic backup.

User correction takes precedence over A018: S3 stopped; A018 TEST selection
and freeze are unconfirmed proposals. E041 is DEV incumbent, E025 fallback.
No S3 resumption, final TEST selection, existing submission edits, ZIP/method
creation or hosted upload. Existing E041/E025 source, E056 and prior STOPs
are preserved. Success means a procedurally validated research candidate,
not S2 release qualification or evidence of actual UNHCR improvement.

## Hypothesis, novelty and domain check

E056 establishes complementary errors for one SIPP leaf within a fixed sample.
Here test whether its content-only intervention has a feasible honest full
UNHCR predict procedure: visible-TRAIN selection, independent validation,
all-visible refit and the shared three-instrument execution contract.
Do not transfer BIR/.5 or pick analogous humanitarian questions after scores.
UNHCR approximate gates and different populations remain a transfer limit.
Content can have different GIVEN interactions from sentinel routing, but E041
already has conditional heads; independent tree complementarity is unproven.

Schema-only audit before response access:213 PREDICT,156 gated,145 gated
leaves,19 distinct parents, at most14 non-sentinel answer classes,17 GIVEN
fields with at most46 levels. Leaf means no item in the complete schema names
it as gate parent (including non-PREDICT children). Freeze every such PREDICT
leaf in schema order; no score-based target choice. Exact list/hash in
E057-outputs/schema-audit.json. Actual asked counts cannot be read from schema.
At most145 shadow plus145 refit trees; sparse/constant heads fall back.

## Frozen predictors and evaluation boundaries

Comparator submissions/2026-09-19-E041/main.py SHA256
22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073.
Source default is unchanged supervised_retrieval.predict (link_sharp with
supervised_layer and hh_cap.CONFIGS for UNHCR). Actual snapshot predict is
injected into the engineering run and checked against source-default outputs
using separately verified existing full-frame references where possible.
No modification of either implementation. Baseline controls are exact E041.
E056 executed code reference dbb0ac652d278810fe79e209ce14ae2cc0dce857.

E056 aggregate records only: oracle/selection/audit already development data.
No E056 rerun, new arm lookup, calibration access, SIPP/Adult source read or
new holdout claim. Existing synthetic TRAIN/DEV/TEST have prior engineering
exposure. This run uses only existing clean synthetic phase1 TRAIN and masked
DEV, one fixed dataset/seed. No synthetic TEST scoring or new simulator seed.
Real hidden DEV/TEST inaccessible; any future actual TRAIN selection stays
inside hosted predict. No telemetry or detailed-statistic encoding in scores.

## Complete selection and refit policy, fixed before scoring

UNHCR detection follows the existing E041 marker
s3_11_intent_return_12m_lbl. Non-UNHCR: invoke E041 once and return its original
list directly. No leaf, unsupported GIVEN vocabulary (>255 classes/unknown/
missing), partial PREDICT blocks, fewer than2000 complete visible rows or fewer
than200 selection/validation rows: exact unchanged E041. No new target features.

For supported UNHCR, enumerate complete visible positions. Permute with
numpy.default_rng(5701); n_selection=n_validation=min(1200,floor(n_visible/5));
selection first n, validation next n, fit remainder. Sort within each role for
stable frame order. At8279 TRAIN:5879 fit,1200 selection,1200 validation. Split
uses positions only, never labels or observed target activity. No grouping key
is supplied in this contract; respondent SE omits possible household/donor
dependence. Country/wave remain GIVEN, not post-hoc stratification targets.

Copy frame and mask ALL PREDICT cells on every non-fit row before shadow E041
and shadow trees. Both see exactly the same fit labels; all query GIVEN values
may be used as E041 already does. Preserve E041's known INNER replay limitation;
this outer protocol does not claim to repair it. Freeze shadow predictions for
selection/validation/original queries before opening selection labels.

One HistGradientBoostingClassifier per leaf on fit rows actually non-sentinel.
GIVEN only, public category order, all17 categorical features. Original E051
settings:40iterations,15leaves,learning_rate.1,L2=1,early_stoppingFalse,
random_state0,max_bins255. At least100 asked fit rows and2 observed classes;
otherwise exact E041 for that head. Align to complete schema answer order;
q=.99*tree+.01*(asked_counts+1)/(asked_n+K). Unknown/invalid target codes are
errors, not guessed recodes. No true parent or target enters inference features.

Raw intervention for leaf p=[answers,g], M=sum(answers): preserve g; replace
answers by(1-alpha)*answers+alpha*M*q. alpha grid{0,.25,.5}, constant per leaf.
alpha0 and M0 return original bytes. Parent/nonleaf/control outputs exact E041.
Final vectors retain row/schema order; no downstream rerendering. Apply official
normalization plus linear uniform floor. Report raw/post-floor sentinel and
mass roundoff; tolerance1e-12 on mass/floor, raw sentinel bit-exact.

Selection maximizes each leaf's official mean log score; exact ties smaller
alpha. Chosen nonzero survives only when mean paired log difference >2SE and
>0, SE=sample_sd(d,ddof=1)/sqrt(n). This is more conservative than E056's1SE
because145 leaves can overfit; it is NOT a formal familywise-error guarantee.
Freeze the entire share dictionary before independent validation. If allzero,
do not read validation labels; identity policy. Otherwise evaluate that single
fixed whole213-head distribution on validation exactly once. For each person,
d=mean213(log p_selected - log p_base)/U, with U=mean213(logK). Accept entire
policy only if mean(d)>2SE(d) and >0. Reject means set ALL shares to0, no
headwise pruning, second policy or retuning. This assesses the selected policy
on separate rows; it is operational protection, not valid inference for TEST.

Freeze accepted/rejected shares, then invoke unchanged E041 on full original
visible frame (TRAIN only in this rehearsal). Refit ALL eligible145 conditional
trees on the same full visible labels even for zero shares. This eager refit is
intentional: fixed complete-library cost and active-path engineering coverage
without a second fit or outcome-dependent timing underestimate. Do not retune
shares after refit. If a refit head is unsupported, use original E041 for it.
Final shadow-to-refit distribution change measured on common originally hidden
GIVEN rows, without their labels; this is not an honest performance estimate
of the refitted model. Validation labels enter refit ONLY after policy freeze.

Expected selection rejection/sparse/unsupported paths return exact E041 output;
unexpected fitting, leakage, probability or parity defects STOP the study and
preserve partial artifacts. Never hide a defect by silently accepting fallback.

## Cheapest gates and execution plan

1. Commit schema audit and this registration before any candidate fit/score.
2. Add src/models/conditional_leaf_content.py, scripts/check_e057.py and
   tests/test_e057_conditional_content.py. No old model or submission edits.
   Synthetic fixtures first: alpha0/zero mass, schema order/class alignment,
   unchanged parents, whole-block masking, disjoint fit/selection/validation,
   share freeze before refit, aggregate validation rejection, fallback, actual
   official floor parity. Injected active fixture is not empirical gain evidence.
3. One full clean phase1 rehearsal: one process imports dependencies, runs
   unicef/world_bank/unhcr candidate in sequence; no duplicate E041 fit for
   inactive fallback. Persist frame/source/data/split hashes and full predictions
   before scoring outer synthetic DEV. Refuse existing output paths before fits.
4. Force alpha=.5 on all eligible refit leaves using the ALREADY frozen full
   library, outside natural selection and without reading/scoring DEV truth.
   Check vector invariants/changed fractions; do not call this policy qualified.
   Report actual full eager-refit time, not some-head extrapolation.
5. Compare actual fullbase to validated E041 cache, and candidate to E025 cache.
   Cache reuse requires source/data/frame/cells/split/hash equality, no missing
   provenance quietly accepted. Invalid cache blocks comparison or permits one
   bounded fresh reference if <=1200s cumulative fit remains; no model tuning.
   Clean absolute skill difference <=.002 per instrument is release-performance
   screen; also report E041 delta. Exact source-default/snapshot confirmation
   may rely on previously frozen full-base vectors with matching source hashes;
   new module assembly parity remains a separate S2 check.

Monitor parent wall from before child creation; worker watchdog starts before
numerical imports, samples native Windows RSS/commitment every.2s. Own worker
and child tree cap8GiB, cumulative fit1200s across base calls/tree fits;
conservatively count entire base prediction as fit. Full-run local ceiling900s
including import/loading/all3/selection/validation/refit (timing through final
vector return); watchdog stops worker tree if exceeded. Save limits/exit/partial
artifacts;90min research cap monitored by session owner. No network/GPU in run.

PASS research feasibility requires structure/isolation tests, measured all3
runtime<900s/memory<8GiB, natural policy/fallback and forced-path validation,
E025 absolute.002 comparisons and unchanged E041 controls/parent/nonleaf vectors.
Synthetic gain or zero activation neither proves nor refutes hidden UNHCR gain.
No universal oracle needed over hidden target data: this is a scoped engineering
screen after E056, not a renewed proxy futility/adoption experiment. No new
score-tuned estimator is authorized by a synthetic oracle.

## Deliverables, stop and handoff

Save schema list, provenance, split hashes, label exposure, natural/fixed
policy decisions, full cost, checks and separate qualification dispositions
under docs/analysis/E057-outputs; row arrays under ignored external/e057.
Code/hashes/aggregate records only in Git. On any registered technical/resource
failure, preserve cause and exact resumption conditions; no backup/S3 research.
If feasible, write S2 validation handoff with remaining source/assembly parity,
ZIP checker, official all3, SCORES reading arms and hosted-resource uncertainty.
No ZIP/method/TEST artifact or upload in this session. Update log/status/tree;
commit owned work only. Existing push rejection cannot be bypassed; user has
not explicitly approved its named destination in this conversation.

## Result

Completed one registered phase1 engineering run. Original preregistration bytes
remain in [registration.md](../analysis/E057-outputs/registration.md), committed
before fitting as592da4c. Executed implementatione51b29f. No threshold, grid,
head list, seed or model change followed any score. No extra study or S3 work.

- Thirteen focused tests PASS (final pre-run console:13 passed in8.31s): schema
  order, excluded-child parent handling, exact alpha0/zero-mass identity, actual
  official floor parity, full answer-class alignment, sparse/constant fallback,
  whole-block masking, same base/tree fit roles, selection/validation/refit
  ordering, forced activation and exact full-refit fallback after rejection.
- Schema scope145 leaves/213 outputs/max14 answer classes confirmed. TRAIN8279
  split5879/1200/1200; outer DEV621; shadow query3021. Both stages considered
  all145 leaves;124 eligible trees fitted in each stage (248 total),21 fallback.
  Asked counts shadow8..5276, full8..7432. These are synthetic observations;
  real asked counts and resulting fit workload remain unknown from schema.
- Selection retained3 nonzero leaves. One frozen whole-policy validation:
  delta skill+.0000217454212122, SE.0000111234759201; fails >2SE
  (.0000222469518401). **All145 shares set to0**, without pruning or retuning.
  Final E041 and all eligible trees then refitted on all8279 visible rows.
  The failed guard is an expected exact-fallback path, not a technical defect.
- Natural policy changed0/132273 UNHCR vectors. Full base/returned vectors
  exactly match the hash-verified E041 cache on all189649 three-instrument cells.
  Parent/nonleaf/UNICEF/WB unchanged. Forced alpha=.5 fixture, never scored,
  changed77004/132273 vectors over124 leaves. Raw sentinel difference0;
  total-mass max4.44e-16, post-floor sentinel max2.22e-16. Complete output checks
  PASS; other21 heads fall back. Injected positive fixture tests the accepted
  path; actual synthetic run tests policy rejection and final refit identity.
- On common621 hidden GIVEN rows, shadow/full base mean TV.0170852
  (max.256286), tree mean TV.0645886 over124 heads. This establishes a refit
  distribution change, not the sign or size of any refit performance change.
  Independent validation evaluated shadow predictions, not a fresh final model.
- Frozen verifier PASS:60 source hashes, registration/schema/split/library
  hashes, all non-fit blocks masked, deterministic disjoint roles, event order,
  exact final-policy reconstruction132273 vectors and protected files unchanged.
  Zero new fits or label scores. Row-level artifacts remain ignored locally.

### Measured complete cost

One owned heavy worker, CPU2threads/no GPU. Whole parent-inclusive run564.661591s
(9m24.66s); dependency import4.522031s, all3 predictions frozen559.198550s,
worker including comparisons563.455129s. Rehearsal conservative fit544.353257s
(entire base-predict calls counted, not just optimizer time). Limits900/1200s PASS.
Supplemental aggregate across worker, both launchers and parent harness:
sum of OS lifetime RSS peaks1,828,978,688 bytes (~1.703GiB), commitment peaks
1,705,742,336 bytes (~1.589GiB), below8GiB. Worker-tree parent monitor max
RSS1,783,631,872 bytes; no abort, exit0. This is measured all3, not extrapolated
from SIPP or selected heads, and not a hosted runtime guarantee.
The two preceding focused-test passes include tiny110-row fixture fits; their
individual fit times were not persisted (latest entire test process8.31s).
They are outside the reported rehearsal fit counter. No other full model fit
occurred; test timing is a minor accounting limitation, not another efficacy run.

| Stage | Seconds |
| --- | ---: |
| UNICEF exact E041 call |37.1700|
| World Bank exact E041 call |98.6686|
| UNHCR shadow E041 |149.5534|
| UNHCR shadow tree batch,124 fits |16.8254|
| Shadow freeze to selection event, includes persistence |1.4206|
| Selection event to validation event, includes persistence |.0350|
| UNHCR full E041 refit |225.0955|
| UNHCR full tree batch,124 fits |17.0404|
| Complete UNHCR predict including diagnostic writes |413.0486|

Existing E025/E041 caches were reused only after56 prior source hashes, six
cache hashes and schema/data/frame/config/cells/truth/split bindings matched.
These are clean existing phase1 synthetic references, not additional fits.
Official floor/core metric arithmetic was used; official CLI was not run.

| Instrument | E057/E041 skill | E025 skill | Delta E041 | Delta E025 | Absolute.002 |
| --- | ---: | ---: | ---: | ---: | --- |
| UNICEF |.500648423071|.500648423071|0|0|PASS|
| World Bank |.454717307363|.454717307363|0|0|PASS|
| UNHCR |.562462728858|.562948873705|0|-.000486144847|PASS|

Data/source hashes: [preflight](../analysis/E057-outputs/preflight.json).
Split SHA256033a4939112860864e607048054610e4fbb7d881b1af2f20289fc7192ec74f8d;
frozen policy SHA256f0852180eef1d46472a23c3ac5764846cd5790e250f5c03f2392c1bf28116499.
Complete outputs and checks: [result](../analysis/E057-outputs/result.json),
[execution](../analysis/E057-outputs/unhcr-execution.json),
[verification](../analysis/E057-outputs/frozen-verification.json),
[exposure ledger](../analysis/E057-outputs/exposure-ledger.md),
[reproduction](../analysis/E057-outputs/reproduction.md).

### Interpretation and limits

Honest visible-row policy selection, whole-policy rejection, all-visible refit,
sentinel preservation and a complete local runtime are feasible on this fixed
synthetic phase1 channel. Engineering success neither establishes real UNHCR
gain nor disproves it. The near-threshold validation result does not justify
lowering the guard. Multiple leaf selection, respondent dependence, one fixed
training realization, approximate real gates and shadow/refit shift remain.
Natural allzero output does not test selected-active performance; the forced
path is structural only. No calibration/proxy response, unused E056 audit arm,
fresh seed or private DEV/TEST was accessed.

Domain verdict: content-only changes are structurally applicable to the public
UNHCR schema while keeping sentinel routing intact. Synthetic class activity
and scores cannot validate humanitarian conditional relationships. E056 remains
a scoped development precedent, not a transferable effect-size oracle.

## Decision

- **Research technical feasibility PASS, scoped.** New wrapper and frozen E041
  injection satisfy registered structural/resource checks. Historical unchanged
  source-default parity is hash-verified; new default-wrapper/standalone assembly
  parity, ZIP checker and official all3 remain unperformed S2 release checks.
- **Release-performance screen PASS only on exposed synthetic phase1.** Natural
  policy returns exact E041; this does not qualify forced alpha=.5 or claim gain.
- **DEV exploration pending S2 validation.** Further validation is worthwhile for
  the named conditional-content mechanism and honest actual-TRAIN procedure;
  no new DEV incumbent, release-qualified archive or upload recommendation here.
  [S2 handoff](../analysis/E057-outputs/s2-handoff.ko.md) specifies remaining gates
  and unresolved/failed readings. No synthetic-positive adoption argument.
- **Actual UNHCR improvement / final adoption unestablished.** E041 DEV incumbent,
  E025 fallback. S3 stopped; A018 remains unconfirmed by the user. Existing STOPs
  preserved; no new backup study, ZIP, method or TEST artifact. All owned jobs
  complete; user dirty files preserved. Commit owned records only. Push remains
  subject to the previously rejected named-destination approval, never bypassed.
