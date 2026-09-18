# E041 - Supervised section-specific retrieval (UNHCR only)

Status: **DO NOT SUBMIT: performance qualification failed.** Technical archive
validation completed. Preserved for review; not uploaded, not an adopted model.
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

| Returned Grand / update | Interpretation | Next action |
|---|---|---|
| .65 or higher, controls stable | Large positive candidate reading; not proof of the matching mechanism or winning | Inspect newly visible instrument triple, freeze best, examine complementarity |
| .64, controls stable | Positive transfer evidence at this resolution | Retain candidate pending full record; do not claim exact delta from rounded scores |
| .63 with a best update | Possible within-rounding improvement, as E022/E025 showed | Record actual triple before deciding |
| .63 without update | Unresolved or too small to read, not exact zero | Park this metric configuration; do not spend slots on small weight-grid changes |
| .62 or lower | Adverse reading | Keep E025 incumbent and inspect calibration/selection mismatch |
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
submission. Do not use the pre-registered hosted arms as a reason to upload
after failing the local gate.

Archive: `output/dev/E041.zip`.
SHA256: `1502ebad20e85ae57db617fa6d202b9e199594c1c043acd6d0d1d52102362a50`.
Main SHA256: `22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073`.
Exact checks/times: adjacent `verification.json`. Experiment decision:
`docs/experiments/E041-supervised-retrieval.md`.

## Actual hosted result

Not submitted. No daily slot used.
