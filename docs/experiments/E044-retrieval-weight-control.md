# E044 — Conditional retrieval weight-use control
parent: E041
status: parked
date: 2026-09-20

## Hypothesis

Replacing learned section weights with the initial common weights only when
constructing evidence will lower E041's DEV score if learned reranking is
responsible for a readable part of its hosted improvement.

## Domain check

Registered before production implementation or scoring, following E043's
failed candidate-search oracle. Technical: retain E041's metric fitting,
learned section activation, K=32, donor search, row partitions and replay
algorithm. In active sections replace the softmax agreement weights with
the original initial weights for both replay and held-out evidence. Lambda
is recalibrated through the same procedure; its changed values are downstream
effects of the intervention. Inactive sections, controls and base are intact.
This is a conditional ablation of learned weight USE, not all supervision:
the activation mask still depends on the learned metric. No new estimator
is fitted, so this diagnostic does not require claiming a positive oracle
ceiling. No per-cell hidden-data statistic is exported.

Background: UNHCR schema domains can value different GIVEN attributes. E041's
positive full-pipeline reading is compatible with that but also changed K,
selector and replay. E025's .79+.10 map establishes evidence relevance, not
an E041 decomposition. Removing weight use while retaining those procedures
helps distinguish two operational paths: invest in learned metrics if score
drops, or inspect retained K/selection/replay if the result stays comparable.
No assumption of duplicate households, panel recurrence or exact routing.

Measurement channels: full clean synthetic harness for correctness and
no-regression versus both E041/E025 (absolute <=.002), existing household sim
for direction only, then one UNHCR-only hosted reading. The user prioritizes
using an expiring slot for information even without positive local adoption.
The actual scorecard is preregistered before upload; E041 .64/.52/.49/.92 is
the reference. No strong numerical prediction is justified; .63-.64 is a
planning scenario, not a confidence interval. A flat reading cannot prove
that learned metrics never help. E041 remains incumbent until a new best.

## Change

New `src/models/retrieval_weight_control.py`, invariant tests and immutable
E041-based `submissions/2026-09-20-E044/` plus adjacent ZIP. Existing model
modules and snapshots must remain byte-identical.

## Result

Clean phase-1 source results, current frames and both frozen snapshots:

| Instrument | E025 | E041 | E044 | E044 minus E041 |
|---|---:|---:|---:|---:|
| UNICEF | .500648423 | .500648423 | .500648423 | 0 |
| World Bank | .454717307 | .454717307 | .454717307 | 0 |
| UNHCR | .562948874 | .562462729 | .562294713 | -.000168016 |

UNHCR delta versus E025 -.000654161; three-instrument mean delta versus E041
-.000056005. Both clean no-regression checks pass; every control probability
is identical. Fifteen invariant tests pass. Source/code and frame hashes bind
each comparison cache, and baseline hashes are pinned. Raw clean outputs are
in `../analysis/E043-outputs/clean-E044-unicef,world_bank,unhcr.json`.

Existing household sim seed13: E041 .552012531, E044 .555102556,
delta +.003090025 skill / +.003898846 log, mean equivalent +.001030008.
This is below the +.005 three-instrument adoption bar. Directional result is
consistent with E041's earlier negative household-sim comparison, not evidence
that the same intervention will improve actual DEV. No post-result tuning.
Raw output: `../analysis/E043-outputs/household-E044-unhcr.json`.

ZIP checker PASS; official phase-1 scorer PASS x3, exact every-vector
source/archive parity on each schema. Combined official local times 371.022 s
(42.009 / 106.256 / 222.758), two numerical threads with partial simulation
overlap. This is not a hosted timing guarantee. Independent review confirmed
the one intervention, immutable E041 prefix and oracle interpretation; both
baseline SHA pins and mandatory comparison checks were added to the harness.
No hosted E044 reading yet.

Reproduce from the repository root (existing dependencies and sandbox):

```powershell
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E041 --snapshot submissions/2026-09-19-E041/main.py
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E025 --snapshot submissions/2026-09-09-E025/main.py
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E044 --module src.models.retrieval_weight_control --compare E041,E025
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E041 --snapshot submissions/2026-09-19-E041/main.py --case household --schemas unhcr
.venv/Scripts/python.exe scripts/check_daily_retrieval.py --label E044 --module src.models.retrieval_weight_control --compare E041 --case household --schemas unhcr
.venv/Scripts/python.exe scripts/assemble_e044.py
.venv/Scripts/python.exe scripts/verify_daily_retrieval.py --experiment E044
```

## Decision

Parked pending the hosted reading; technically ready as a preregistered
measurement, packaged as submission #26. Neither clean mean -.000056005 nor
household-sim mean +.001030008 clears the +.005 adoption bar. Preparing the
probe under the user's exploration policy is not adopting an improved model.

Domain verdict: the fixed initial metric helps the injected-household channel
but is slightly worse on clean data. This is consistent with the earlier E041
simulation loss, not evidence about the direction on actual UNHCR. Read only
the pre-registered arms after upload. Keep E041 .64/.52/.49/.92 as incumbent.
