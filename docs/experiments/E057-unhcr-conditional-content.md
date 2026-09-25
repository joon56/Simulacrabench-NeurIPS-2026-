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

Pending. No synthetic response or new model score was inspected at registration.

## Decision

Pending engineering screen; no DEV recommendation or TEST adoption at registration.
