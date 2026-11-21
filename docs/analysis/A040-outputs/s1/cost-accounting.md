# A040 full-cost specification — unmeasured

All figures below are **public schema arithmetic or source call counts**, not
timings, profiled memory, fabricated fixtures or fitted results. Fixed proposed
settings and future task caps are in [contract](contract.md). Policy condition
in [closeout](closeout.md) precedes any execution decision.

## Public dimensions

The machine-readable [inventory](schema-accounting.json) contains all213 UNHCR
head names, ordered options, content K, gate flag and complete K. No responses
or observed class frequencies were read.

| Complete K, including sentinel when gated | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| UNHCR heads | 25 | 124 | 15 | 13 | 12 | 8 | 5 | 3 | 4 | 2 | 2 |

213 heads,156 gated,17 GIVEN,834 total probability columns. Four K>10 heads:
`s3_4b_visit_month`15; `s3_8b_return_month`15;
`s3_23a_safety_rank1_lbl`11; `s3_23b_safety_rank2_lbl`11.
The earlier14-content-class maximum is not the complete-distribution maximum.
Actual observed classes and fallback counts cannot be determined from schema.

| Instrument | GIVEN / PREDICT | Phase1 visible / query | Phase1 output vectors | Phase2 visible / query | Phase2 output vectors |
|---|---:|---:|---:|---:|---:|
| UNICEF | 7 /12 | 14885 /1488 | 17856 | 16373 /3473 | 41676 |
| World Bank | 9 /76 | 5195 /520 | 39520 | 5715 /1212 | 92112 |
| UNHCR | 17 /213 | 8279 /621 | 132273 | 8900 /1449 | 308637 |
| all3 | — | — | **189649** | — | **442425** |

Phase2 numbers are a schema accounting exercise, not a TEST selection or
authorized future run. Phase1 receives TRAIN+DEV rows only; TEST rows are absent.

## Context and query counts, per UNHCR head

Proposed visible-only split:1000 S,1000 E, remaining F; seed4001, one permutation.
All PREDICT outside F masked before any shadow baseline/model fitting.

| Stage | Phase1 n context / q | Phase2 n context / q | Public calls per nondegenerate head |
|---|---:|---:|---|
| TabICL shadow | 6279 /2000 | 6900 /2000 | 1 context fit +1 predict_proba for ordered S+E union |
| Selection on S | 1000 evaluated rows | 1000 evaluated rows | 3 fixed mixture arrays, no model calls |
| Frozen check on E | 1000 evaluated rows | 1000 evaluated rows | 1 selected mixture vs retained R, no model calls |
| TabICL all-visible context rebuild if active | 8279 /621 | 8900 /1449 | 1 new fit +1 predict_proba; no weight update |
| E041 shadow whole frame | 6279 /2621 | 6900 /3449 | One whole pipeline, not per head; includes external query rows whose labels remain hidden |
| E041 final whole frame | 8279 /621 | 8900 /1449 | One whole pipeline, needed even if alpha0 |

E041 shadow returns558273 phase1 vectors (734637 phase2); retain S/E predictions
for selection/check and discard unused external-query shadow predictions. TabICL
does not score or fit on these external responses. Query batch definitions are
fixed; no claim that changing batch size/order preserves neural predictions.

## Normal accepted path, all3

| Component | Count | Evidence/meaning |
|---|---:|---|
| External checkpoint deserialize | **1** | Proposed import adapter; stock fit would reload per head and is unacceptable for this contract |
| TabICL wrapper fits | **426 maximum** | 213 shadow +213 all-visible; preprocessing/context construction, no neural optimizer with cache=False |
| TabICL predict_proba | **426 maximum** | 213 shadow +213 final; contextual inference includes the references again |
| Ensemble views | <=**3408** | <=8 per predict call; actual fewer if permutation library limited. Not3408 separately fitted pretrained networks |
| Outer TabICL module forward entries | <=**852** at fixed settings | At most2 normalization groups with <=8 views each, batch_size8. Not an upper bound on internal attention/hierarchical classification operations |
| E041 whole pipelines | **4** | UNICEF1 +WB1 +UNHCR shadow1 +UNHCR final1 |
| E041 `tune_and_train` | **4** | One per pipeline; fixed two-config family from hh_cap |
| E041 neural `_train` calls | **12** | 2 architecture trials +1 final fit per pipeline; distinct from4 top-level calls |
| E041 `_train_on` attempts | **12 normally; up to24 if each CUDA attempt retries on CPU** | Snapshot429–458; fallback consumes elapsed time, may still fail |
| UNHCR section L-BFGS-B minimizations | **16** | 8 sections ×2 E041 UNHCR pipelines; each maxiter50, not bounded to50 objective/line-search evaluations |
| Ladder selection | **4 top-level calls** | Internal prefix/kappa grid/holdout table construction remains real work; instrument durations/counters required |
| Final ladder table construction | **863** | 2×(213+156) UNHCR + (12+7) UNICEF + (76+30) WB; excludes tables built inside ladder/trunk selection |
| Legacy lambda replay | Up to2 buckets per applicable item per pipeline | UNHCR at most852 `_best_lambda` calls over shadow+final; minimum30 per bucket retained. Control-instrument legacy calls also timed, not claimed zero |
| Gate agreement, donor ranking, evidence, recursive rendering | **4 full pipelines**, plus internal replay | Source link_sharp/supervised_retrieval and immutable snapshot. No multiplication by3 merely because three alpha arrays are compared |
| Mixture selection / E check / final flattening | Once each | All213 final complete distributions; include floor, reduction, Python output construction/serialization cost |

The eight UNHCR groups are s2,s3,s7a,s7b,s7c,s4,s5,s6 with6,61,24,39,11,12,10,50
heads. Baseline-only E041 all3 has3 pipelines,9 neural `_train` calls,8 metric
minimizations normally. Added policy is one shadow E041 pipeline plus the expert,
not merely213 quick neural predictions. Source hashes, including the actual
E041 snapshot, are in [local-source-hashes](local-source-hashes.json).

If alpha0 or E rejects, skip the final213 TabICL fits/predicts; return retained
final E041. Shadow cost has already been incurred. Per-head singleton bypasses
reduce calls; they cannot be assumed in the budget. Empty/no usable context
falls back to the retained R head only under the predefined support rule.
Bad class alignment, cross-role leakage, nonfinite output, offline violation or
resource exhaustion is a technical failure, not a free fallback success.

Source reading confirms TabICL cache construction passes target y and class
permutations. No213-fold X-only cache amortization is credited. KV/repr cache is
disabled; model weights shared but context, encoders and normalization are rebuilt.
Frozen weights do not make contextual forward work free. Above-native-cap heads
can induce extra internal operations; exact count remains unmeasured/unreviewed.

## Clock and memory contract

Saved current official README agrees with900s DEV/3600s Final **whole run**,
one H100,8 cores,16GB host memory, Python3.13, fresh process and no network before
import. It does not state an H100 VRAM capacity; host16GB is not a VRAM budget.
README identifies config.yml as authoritative; later release must verify that
version as well. Current wording about runtime fitting remains unresolved.

`T_total = import/dependency initialization + checkpoint read/construct/transfer
+ controls + UNHCR shadow R + shadow ICL preprocessing/forward + S selection
+ E check + final R + optional final ICL context/forward + output assembly`.

All terms unmeasured in this session. Prebuilt package installation is off the
hosted clock but subject to a separate build limit; proposed local acquisition
and technical task setup also consume that task's wall allowance. No claim based
on the advertised single-target H100 speed or E048/E051 partial timings.

Future timings must bracket process start, imports, deserialization, instrument
calls, each E041 stage, each target context/forward, decisions and serialization.
Record cumulative fitting/preprocessing wall and inference wall separately.
Count failed attempts as well as successful calls; do not hide CPU retry/offload.
No parallel heavy jobs. Total elapsed is authoritative, not the sum of selected
fast samples. Instrument hooks themselves must stay in the measured run.

Memory: process-tree host RSS and private commitment sampled1s, plus CUDA peak
allocated/reserved and actual device capacity. Include model CPU/GPU copies,
encoder/ensemble arrays, retained base/query probabilities, transient embeddings,
output lists and loaded control models. One shadow probability matrix with
2000×834 float64 entries is13,344,000bytes; that is **not peak process memory**.
Head objects released sequentially, retained predictions only as needed. Explicit
offload_mode=False avoids hidden disk/host offload in the proposed expert; any
unintended file-backed cache is a failing deviation. No cache persisted from actual
hosted visible data. Runtime/peak-memory claims require measurements on the whole
declared shape and hardware. GPU allocations, model cap, internal hierarchy and
build compatibility remain future verification items.

The minimum future task specifies at most1920s cumulative model wall across
small suite + candidate all3 + comparator all3,60min task wall. None has run.
Phase2 whole-scale profiling is not part of that minimum task; no TEST feasibility
PASS follows from DEV-scale success.
