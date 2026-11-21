# E063 implementation and evidence map

## One candidate and unchanged endpoint

`src/models/round_metric_retrieval.py` imports the identified original
`supervised_retrieval` module. UNICEF/WB and every unsupported whole-instrument
case call its original `predict` directly. Supported UNHCR calls original
`link_sharp.predict` with only the new round layer and unchanged
`hh_cap.CONFIGS`. No second common fit or outer refit.

For section s, x[q,k,j] is the original GIVEN exact-match vector of the fixed
initial-search K32. Raw schema wave "1"/"2" maps explicitly to r=0/1.
pi[q,k]=softmax_k(sum_j x[q,k,j]*w[s,r,j]).
The original all-cell floored probability and eta share loss are retained:
p=.001+(1-K_i*.001)*((1-sigmoid(eta))*prior_truth+sigmoid(eta)*evidence).
Add .001 mean((mu-v0)^2)+.001 mean(Delta^2), mu=(w1+w2)/2, Delta=w1-w2.
Each w gradient gets .001*(mu-v0)/17 and +/- .002*Delta/17 in addition to
its own round's likelihood gradient. At w1=w2, loss equals original common
loss and the sum of both w gradients equals its gradient. This objective
endpoint does not make the entire procedure bit-exact R; direct original
function dispatch supplies that endpoint.

Selection retains F-fitted old-share grid and single H optimizer, S threshold
gain > max(.003,2*SE), original K32 ordering and distinct legacy K10 evidence.
F+S match tensors are materialized; only F slices and waves[F] enter minimize.
S labels do influence original selection; base final refit includes all visible
TRAIN and replay remains in-sample. This is no independent audit.

Full-frame eligibility runs before base/H fit: raw wave supported everywhere,
17 GIVEN, F and S each at least30 of each wave, bank width32; original
visible<500/no-query cases dispatch R. Unknown/one-wave support is not inferred
from factorization codes. No labels used to choose wave support beyond original
visible/query missingness role detection.

Round layer copies original partition, replay, lambda and output flow; only
fit objective/posterior dispatch differs. Original cal union, active-item replay
restriction, legacy concentration bucket, minimum30/zero lambda, all213 recursive
parent/child rendering stay intact. Weights, activity and final lambdas may differ.
No H-C selector, sentinel removal or wave-specific lambda.

## Registered artificial checks and repair

tests-01: expected RED before module exists, one test. tests-02: ten registered
unique tests, nine PASS and forced-active observer FAIL. Failure was test-only:
_replace_evidence positional query/codes/bank/initial indices were one too high.
Attempt source/logs/resources preserved. tests-03 reruns only that affected test:
PASS. No model/runner, tolerance, policy or assertion changed after tests-02.

Coverage: common loss/gradient reduction; fixed finite differences/bounds;
donor-constant cancellation/rank reversal; F-only optimizer arguments under
S-label mutation; fallback original-function identity/call count; actual small
fallback raw parity; K32 original identity/order/self exclusion and separate K10;
actual H entry, cal/Q conditional evidence and global all213 recursive renderer;
fixed31/29 replay buckets showing minimum30/zero; production projection/masking;
budget exhaustion and six-output gate. Fixed base/neural doubles in artificial
integration checks, not trained models. Forced activation is not natural activity.

Artificial calls are kept separate from full-stack training: tests-02 includes
two fake optimizer invocations, two small real render/base-entry paths with
training disabled, and one forced-active path; tests-03 repeats only that failed
forced-active path. Neural training and actual scipy minimization in these
fixtures:0. Support tests mock original.predict and require exactly one dispatch.
Math function evaluations and fixed evidence/renderer calculations are fixtures,
not empirical experiments.

## Data and runtime boundary

Only three explicitly permitted synthetic parquet files are identity-checked.
Every content read requests role TRAIN or DEV, never TEST. Model preparation
projects TRAIN generated columns, DEV GIVEN plus synthetic row-order metadata;
then completely masks DEV PREDICT before entry and removes EXCLUDE features.
The controller records every projected request. Official runtime schema and
canonical order are used, not guessed raw gate-sentinel options.

Model-worker runtime trace checks actual neural target row hashes, F/S/bank role
hashes and optimizer F slice widths. It counts base pipelines, neural _train_on
and scipy minimize attempts before those calls, including failures. Logs record
selection, fits, replay/lambda, output timing and all resulting weights. Tracing
is measurement overhead included in current wall time, not an estimated
production-speed result. Common R is source execution, not E041 snapshot parity.

Prepare freezes registration/source/package/runtime schema/masked-frame/row-role
identities. R and H must use the same freeze. All six new outputs and source
identities freeze before evaluator DEV truth projection. Official in-process
check/normalization/floor .001/score is applied once per arm/instrument;
no score.py CLI, old successful suite or cached raw predictions is run/read.

External parent monitor starts before numerical child import, samples its owned
tree every .1s, records conservative sum of per-process peak RSS/private, and
enforces both 8GiB limits plus stage/aggregate/absolute deadlines. CPU numerical
threads2/GPU0; stages sequential. Recorded stage wall includes source verification,
startup, child, monitoring and cleanup. Normal scientific budget is R/H all3:
2 processes /6 pipelines /18 neural fits /16 section optimizers. Artificial
counts are separate; all computational stage wall shares1800s. No timing
extrapolation from individual heads or old experiments.

## Reproduction commands (historical recipe, not fresh authorization)

PowerShell, repository root; each attempt directory is exclusive and previous
attempts are never overwritten:

```powershell
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e063_round_metric.py tests --attempt 1 --only tests.test_round_metric_retrieval.MetricTests.test_common_reduction
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e063_round_metric.py tests --attempt 2
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e063_round_metric.py tests --attempt 3 --only tests.test_round_metric_retrieval.EntryTests.test_forced_active_all213_actual_entry_replay_and_renderer
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e063_round_metric.py prepare --attempt 1
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e063_round_metric.py R --attempt 1
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e063_round_metric.py H --attempt 1
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e063_round_metric.py score --attempt 1
```

Registration, unit qualification and freeze must precede corresponding commands.
Expired session deadline and completed-arm gates prohibit casually replaying this
recipe. Original failures remain evidence, not instructions to recreate them.

