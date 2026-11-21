# E062 measured-cost semantics

Fixed limits: gross7200s including reading, writing and waits; final600s reserved;
all computational children together1800s, including the expected RED test and
preparation/evaluator; candidate fresh child through completed all3 output<=900s;
pipeline attempts9/neural attempts27. Deadlines remain those in entry.json.

Existing local environment only: Windows, AMD Ryzen7 5800X (8 cores/16 logical),
Python3.13.14, NumPy2.5.1, pandas3.0.5, Torch2.13.0+cpu. Each worker records actual
threadpool state in environment-*.json. Numerical threads2, torch interop2,
CUDA unavailable. No installation, cloud, GPU, billing or monetary expenditure.

## What is included

Each of E025/E041/candidate has one fresh process running all three instruments.
Parent wall begins before Popen and ends after child exit/cleanup. It includes
startup/import, authorized input identity and role checks, all model paths,
output validation and compression. Model `predict_seconds` is a nested stage,
not an additional quantity to sum with child wall. Parent preflight checks and
documentation time are covered by gross session wall, not child wall.

The source's two config fits plus selected full-visible refit are three neural
training calls per instrument. Refit occurs even for w=0. All3 therefore normally
uses three pipelines/nine neural calls; three procedures use nine/twenty-seven.
No separate middle refit. Configuration/weight search, ladder selection, gate
agreement, household/donor selection, lambda replay and recursive rendering are
inside pipeline wall. E041/candidate UNHCR additionally run the original metric
optimizer; the source trace records actual scipy minimize calls and iterations.
E025 and WB have no such metric optimizer. No model cache offsets this cost.

`calls-*.jsonl` records actual pipeline/neural entries, target-role checks,
selection/refit parameters, and selected inclusive stage spans. Rendering is
included in predict wall; no unsupported exact exclusive render time is claimed.
Tracing and resource observation overhead remain included. It is a local measured
cost for these complete inputs, not uninstrumented hosted performance.

## Memory and stop semantics

The existing Windows MemoryTree monitor observes owned controller and descendants
every .1s. For each metric it sums per-process peak RSS/private commitment; this
is conservative and can exceed the instantaneous concurrent sum. Each limit is
8GiB, separately. No other user's process is terminated. On an error or cap, the
controller terminates only its child tree and retains the failure receipt.
Sampling is not a proof of every unsampled instantaneous allocation.

Per-child reports record actual wall, cumulative wall, peak metrics, samples,
return code and any forced stop. Final summary uses those reports, not stage
extrapolation or an earlier E061 measurement. Gross and cumulative child time
are different clocks; no overlap is double-added to gross time.

## Limits of transfer

No H100, hosted900s, official release/all3 CLI or ZIP check was run. The candidate
source's local all3 limit is decided from its complete fresh-process receipt.
Host/runtime/dependency changes and source/assembly parity remain future S2
conditions after S0 review and separate applicable authorization.
