# E041 - Supervised section-specific retrieval (UNHCR only)

Status: **READY FOR ONE EXPLORATORY DEV SUBMISSION, per the user's subsequent
slot-use direction.** Technical validation and clean no-regression passed;
local performance adoption failed and remains failed. Not uploaded or adopted.
The previous DO NOT SUBMIT recommendation is superseded by the exploration
decision below; no code, archive bytes or measured results changed.
Prepared on execution date 2026-09-18 for the next day. The repository's
supplied historical handoff extends beyond this clock; this directory name
does not assert a new hosted result or alter historical submission dates.

## Frozen comparison and change

Baseline: E025, Grand .63 / UNICEF .52 / WB .49 / UNHCR .89.
Main SHA256: 00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9.

UNHCR's neighbour metric is learned per schema question section from answer
log loss. Separate donor-bank, fitting-query, selector and new-metric replay
partitions prevent supervised target reuse. Sections without adequate selector
gain keep incumbent evidence. UNICEF and World Bank call frozen E025.

The internal section selector uses a marginal/evidence proxy, not the full
incumbent pipeline. E025's in-sample base replay and its concentration buckets
remain. Full-stack checks below are required; fixing new metric-label reuse
does not turn the entire incumbent into an out-of-fold calibrated model.

No external model or data is bundled. Public UCI Adult census observations
(Becker & Kohavi, doi:10.24432/C5XW20, CC BY 4.0) were used only for independent
development screening. No Adult-trained weight is loaded by the submission.
Source and outcomes: docs/analysis/A008-outputs/e041-external-source-method.md
and e041-external-learned.md. It is not a humanitarian survey or DEV forecast.

## Pre-registered hosted reading arms

Written before upload; there is no hosted E041 outcome yet.

The subsequent user requested using expiring slots for verification even when
an improvement candidate is unavailable. These arms now govern one exploratory
test. They are operational decisions under rounding/noise, not significance
tests or proof of a particular causal mechanism.

| Returned Grand / update | Interpretation | Next action |
|---|---|---|
| .65 or higher, controls stable | Large positive candidate reading; not proof of the matching mechanism or winning | Inspect newly visible instrument triple, freeze best, examine complementarity |
| .64, controls stable | Tentative positive reading; noise/rounding still matter | Inspect best-update triple; retain snapshot if it becomes best, do not claim exact delta |
| .63 with a best update | Possible within-rounding improvement, as E022/E025 showed | Record actual triple before deciding |
| .63 without update | Unresolved or too small to read, not exact zero | Park this metric configuration; do not spend slots on small weight-grid changes |
| .62 | Adverse but near the reading resolution | Keep E025; stop this configuration without diagnosing the mechanism from this result |
| .61 or lower | More clearly adverse at the recorded resolution | Keep E025; deprioritize this retrieval implementation |
| FAILED | No score, no daily slot consumed under the recorded rule | Diagnose locally; never interpret as a null model result |

Planning anchor: Grand .63. A .64/.65 reading is a success scenario, not a
measured prediction. Do not infer hidden instrument scores as exact values.

## Required local checks

| Check | Measured result |
|---|---|
| Clean UNICEF, E025 / E041 | .500648423 / .500648423; every probability equal |
| Clean WB, E025 / E041 | .454717307 / .454717307; every probability equal |
| Clean UNHCR, E025 / E041 | .562948874 / .562462729; delta -.000486145 |
| Clean no-regression | PASS within .002; mean delta -.000162048 |
| Source / extracted archive parity | Exact probability equality, all three schemas |
| Official phase-1 score.py | PASS x3; skills .500648423 / .454717307 / .562462729 |
| ZIP checker | PASS, main.py at root, no external weights/data |
| Official local CPU time | 36.882 + 88.656 + 195.066 = 320.605 s, two threads |
| Invariant tests | 11 passed |
| Existing household sim UNHCR | .554038343 / .552012531; delta -.002025811 |
| Observed Adult audit, two seeds | +.000594835 / +.000427069 skill; both 95% intervals include zero |
| Performance qualification | FAIL; neither clean mean gain nor directional-sim adoption bar met |

Local synthetic and external scores are not leaderboard predictions. Runtime
is a local measurement, not a hosted guarantee. E025 remains the best measured
submission. Local adoption failure is unchanged. The user's subsequent
direction permits one exploratory submission to measure real-data transfer;
it does not convert these local results into positive evidence.

## Exploration decision after user feedback

Question: does this exact supervised section-retrieval pipeline produce a
readable DEV improvement over E025, despite weak local transfer evidence?
E034 measured evidence OFF, not learned section relevance. E023 changed
fixed matching settings; it did not train the supervised section metric.
The .79 base plus .10 evidence loss map makes the evidence path relevant but
does not imply .04 recoverable gain. E041 tests the complete pipeline, including
its bank split, selector and replay changes; it cannot identify which change
causes a result.

Alternatives considered: repeat broad component ablations (already measured),
or wait for the independent pretrained base (not implemented/validated).
For the already prepared next-day artifact, choose one E041 exploratory A/B
over leaving the slot unused. This is a judgment under the user's preference
for exploration, not a measured claim of optimal information gain.

UNHCR only, frozen E025 controls, unchanged ZIP. Grand .63 without a best
update is inconclusive, not proof that retrieval is exhausted. Operationally
park this exact configuration and move to a materially different family;
do not follow with a daily weight grid. .64/.65 are favourable scenarios,
not forecasts; .63 is only the incumbent planning anchor. No upload performed.

Archive: `output/dev/E041.zip`.
SHA256: `1502ebad20e85ae57db617fa6d202b9e199594c1c043acd6d0d1d52102362a50`.
Main SHA256: `22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073`.
Exact checks/times: adjacent `verification.json`. Experiment decision:
`docs/experiments/E041-supervised-retrieval.md`.

## Actual hosted result

Not submitted. No daily slot used.
