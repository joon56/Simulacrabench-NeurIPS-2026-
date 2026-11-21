# A023 — Source-derived execution counts and future instrumentation

No production function was executed. Every real time/memory value below is
**unmeasured**. Counts are source-path accounting, not a runtime prediction.
Input bytes are bound by A023 entry/session manifests. Source line numbers
refer to those bytes; the E041 snapshot is separately hashed and unchanged.

## Counting units and normal UNHCR path

One base pipeline means one `link_sharp.predict`-equivalent base construction:
ladder selection, shared-trunk tuning/final net, full/conditional tables and
agreement, followed by the retrieval layer and global rendering. It is NOT
one neural optimizer call. P/D share one controlled construction; exact R gets
one separate original construction. The no-refit minimum is therefore TWO
target-instrument base pipelines. Never train a third pipeline for D alone.

Public UNHCR: P=213 predicted items, G=156 gated predicted items, D=17 GIVEN,
D12=15 GIVEN of cardinality<=12, M=8 section groups (2,3,7a,7b,7c,4,5,6), C=3
prospective candidates. Maximum full answer width15 includes sentinel; the
earlier E057 leaf-only maximum14 concerns a different subset. These counts
say nothing about row availability, lambda bucket occupancy or effect size.

| Work unit | One target pipeline / shared P/D library | P/D plus R normal path | Source / instrumentation entry and exit |
| --- | --- | --- | --- |
| Base construction | 1 | 2 | `link_sharp.py:113–152`; pipeline ID, visible-role digest, start/end/status |
| Neural architecture tuning | 2 `_train` calls | 4 | `hh_cap.py:11` has (64,2,0),(128,2,.1); `shared_trunk.py:216–219` |
| Final neural training | 1 `_train` call on complete training rows | 2 | `shared_trunk.py:251–256`; selected config/epochs, all eligible fit rows |
| Total neural `_train` requests | 3 | 6 | AST verifies one call inside config loop and one after it; not six pipelines |
| Neural Adam steps | at most1500 requested across3 calls | at most3000 on normal CPU path | `_train_on:119–153`, MAX_EPOCHS500/PATIENCE30; log actual epochs/optimizer steps, early stop and each attempt |
| Greedy ladder selector | 1; <=42 `_eval_candidate` calls (15+14+13),5 kappas per call | <=84 calls /420 column-kappa settings | `hier_backoff.py:174–228`; trace each depth, considered column, internal holdout, rejection/stop |
| `build_ladder` invocations | <=3P prefix + P neural-blend replay + P+G final tables = <=1221 | <=2442 | `hier_backoff.py:208`, `shared_trunk.py:238`, `link_sharp.py:145–150`; count tables and rows separately |
| Neural/ladder blend grid | <=11P truth reductions | <=4686 reductions | `shared_trunk.py:228–248`; W_GRID from `logit_blend.py:30`; zero-cell branch distinct |
| Gate agreement fitting | <=G*D12=2340 candidate column evaluations; <=G final chosen-column rebuilds | <=4680 evaluations; <=312 final rebuilds | `cond_agree.py:49–107`; record valid parent-child pairs/empty split, scalar fallback |
| Common rarity/household weights | 1 GIVEN-only pass + provisional top10 | 2 independent passes | `dup_link.py:33–47`, `hh_link.py:29–47`; T-only controlled path, R original all-frame GIVEN |
| Section metric optimizer | M=8 fitting-only calls shared by all candidates | M_PD+M_R=16 | `supervised_retrieval.py:86–119`; `minimize` line97, iteration cap50, ftol1e-7 |
| Metric objective/gradient evaluations | log nfev/njev per optimizer; NOT equal to iterations | no explicit source bound on evaluation count from maxiter alone | same fitting loop; callbacks/line search and unsuccessful results counted |
| Old proxy share search |6 settings per section (48) |96 settings | `supervised_retrieval.py:93–95`; first10-of32, fixed order, fit-only |
| Lambda fitting | <=2PC=1278 bucket searches;12 grid values incl.0 | <=1278+2P=1704 searches; <=20448 value evaluations | `supervised_retrieval.py:199–221`, `link_sharp.py:36–51`; log candidate/head/bucket/eligible count/status, never export response statistics via scores |
| Whole output rendering | C candidates, both P and D representations on frozen S/E GIVEN queries | shared library plus separate R output | `link_sharp.py:180–251`; output cells/options/hash, recursive parent dependencies, no per-section shortcut |
| Policy selection | P once and D once on same S | 2; R has its own original section decisions | A021 fixed objective/rules; zero learner access, library digest unchanged |
| Independent evaluation | selected D/P and R on same authorized E | paired D-P and D-R | frozen policy IDs before E; no selector/constructor callback |
| Refit | 0 | 0 | A023 excludes it; source's final neural training above is already counted and is NOT optional deployment refit |

Lambda bound is deliberately conservative: reusable identical head states may
reduce work, but savings require exact artifact/role/bucket identity, not merely
the same head name. Every candidate is completely built before S, including
inactive heads. No asymmetric early cutoff based on P/D scores.

The controlled builder needs a future fitting-only extraction: original
`fit_sections` also scores selection rows and chooses activity. A direct call
does not implement this contract. Extract and preserve fitting arithmetic,
return old/new shares and metrics without reading S, then apply schema masks.
Current A023 stubs do not certify the correctness of that future extraction.

## Donor, evidence and rendering work that neural counts omit

Let B be reference size, F metric-fit queries, C0/C1 calibration sizes, Q the
combined S/E GIVEN-only query count, K10=10 and K32=min(32,B). These row counts
are **not assigned by A023**. A022 inventories do not authorize their use.

Controlled construction can share one common-weight pool32 per query role
across all candidates/sections and one legacy10 pool per role. Proposed frozen
plan: metric pool32(F), legacy10(C0+C1), learned32(C0+C1), legacy10(Q),
learned32(Q), plus preliminary legacy10 on T for common weights. Retain exact
query ordering and membership digests. No rebuilding pools from selector labels.
Memory/time counters include GIVEN encoding, provisional pairs, reference prior
counts, match tensors, softmax, evidence accumulation and array copies.

R additionally calls `candidate_indices` once for combined internal fit/select,
and up to twice more for active calibration/deployment; legacy top10 calls are
preliminary, calibration, and deployment (last skipped if no positive lambda).
Its active bank is full visible development, unlike controlled reference bank.
Its fixed caps FIT1200/SELECT800/REPLAY800/CAL6000 and seeds4101/0 remain source
properties of R, not authorized A023 splits. Internal role overlap with its
neural base remains a limitation, not silently repaired while claiming exact R.

Rendering bound for controlled library is C*Q*P cell vectors for each of P and
D (C=3,P=213), plus R's E*P vectors. Both policies can index the same frozen D
outputs on E; no second fit/render required simply because P chose them.
All heads, including unchanged sections and sentinel classes, enter pooled
objectives. Global recursion runs through final parent beliefs; changing s3
can alter sections7a/7b/7c. Source recursion is schema-order dependent and must
be checked on a future adapter; these stubs carry an order token, not vectors.

Important memory terms to measure, not predictions: dense one-hot float32
N*d_encoded; train/validation/optimizer states; full/conditional probabilities
N*(sum K+sum gated ordinary K); donor arrays Q*K32; metric matches/features
approximately F*K32*(P+D) elements; legacy chunk256*B*D boolean/weighted
temporaries and learned chunk128*B score matrix. NumPy broadcasting/copies,
autograd, ladder count tables, bank answers, retained candidates and R coexistence
can dominate. Never extrapolate SIPP tree times or a few heads to this sum.

## Branches, failure accounting and resource limits

| Branch | Work already incurred / additional work | Required future disposition |
| --- | --- | --- |
| neural fit_rows<10 or outer eval empty | 0 neural calls; ladder selection may already run | Record base-only path; no substitute split |
| neural pooled cells0 after tuning | 2 neural calls, no final call | Record missing neural model; do not count as normal3 |
| chosen blend w0 | final neural call still happens; deployment neural map can be skipped | Charge all3 calls; do not call it no-training fallback |
| CUDA exception | `_train` can call `_train_on` again on CPU; partial attempt adds cost, up to12 `_train_on` attempts for6 requests | GPU forbidden in A023; future GPU use needs separate authorization/accounting. CPU exception propagates |
| visible<500 or no held rows | original supervised layer delegates to `hh_sharp_layer` after same base | No metric optimizer, but common weights/lambda/evidence can still cost time |
| no GIVEN signature / too few donors | empty layer or lower-level failure/fallback, depending function | Record exact branch; controlled unsupported bank is HOLD/STOP, no invented rescue |
| provisional pairs<30 | returns rarity weights | No optimizer added; bucket minimum30 unchanged |
| metric nonfinite result | R retains initial weights and marks section inactive | Charge optimizer attempt. Controlled structurally active artifact unavailable; no silent mask replacement/retry |
| finite but optimizer unsuccessful | source checks finite x, not `success` | Preserve source semantics in prospective extraction and record termination; do not claim convergence |
| bucket fewer than30 / no valid labels | zero lambda for bucket/item | Charge preceding fits/pools; no smaller threshold |
| no positive lambda | layer returns empty before deployment evidence pools | Global base rendering still required; no statement about UNHCR efficacy |
| leak/freeze/parity/resource failure | failed and partially completed work remain charged | Technical STOP, preserve logs. No fresh seed, restart or E041 refit rescue |

Future instrumentation must use one shared wall clock from process start before
imports, plus process-tree RSS/commitment sampling. Counters increment BEFORE
attempts and include failed imports/fit attempts/line searches/pool builds.
Separate `_train` requests, `_train_on` attempts and Adam steps. Record monotonic
start/end, wall/CPU, memory peak, input-role/artifact hash and branch/exception.
Use an external watchdog that can terminate the entire owned tree, including
a blocking optimizer; a Python callback alone cannot bound imports/native calls.

Prospective no-refit UNHCR structural limits:2 base pipelines,6 normal CPU neural
requests,16 metric optimizers,3 candidate bundles,2 selectors,one E evaluation
stage; zero retries/refits. Ladder/lambda bounds above remain upper request counts,
not elapsed-time bounds. An actual empirical run still needs separately approved
numeric total wall/fit wall/memory limits and a justified dataset/role plan before
opening responses. A023's60min/2GiB covers only this technical session and tiny
fixtures; it is not evidence real training fits those resources.

## Three instruments and optional refit

The2 pipelines/6 neural calls apply to the UNHCR P/D-versus-R comparison only.
For a future all3 comparison with identical inputs and unchanged UNICEF/WB
controls, computing each control once adds2 pipelines/6 neural calls: total4
pipelines/12 normal neural calls. If two separate all3 processes are actually
run, count6 pipelines/18 neural calls plus duplicate import/control work. Do not
deduplicate different frames, splits, code, versions or output contracts.
Control paths still include their ladder/agreement/hh_sharp operations.

A single future hosted controlled candidate, without a simultaneous R comparator,
would need3 all3 pipelines/9 normal neural calls, plus controlled UNHCR metric/
candidate selection/calibration costs. Hosted compliance and runtime remain
unverified. No candidate is assembled or released here.

Optional expanded-data P/D refit would add at least1 target base pipeline/3
normal neural calls and a fresh metric/weight/pool/lambda/render build on enlarged
development roles under fixed masks. It alters donor availability, probabilities
and buckets; shadow results do not qualify it. It is excluded from the minimum
design, not a free reuse of source's already counted final neural fit. Any such
future refit needs independent procedure evaluation and its own budget.
