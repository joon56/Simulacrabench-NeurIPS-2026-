# E044 - Conditional retrieval weight-use control (UNHCR only)

Status: **HOSTED RESULT REPORTED: Grand .63, no best update.** The .63 adverse
arm applies; reject this configuration for adoption and retain E041.
All technical checks passed. Individual instrument scores were not disclosed.
Baseline E041: Grand .64 / UNICEF .52 / WB .49 / UNHCR .92, user-reported.

## Intervention and purpose

Keep E041 metric training, learned section activation, top32 candidates,
four-way row partition and base. For active sections, use the initial common
weights instead of learned weights in evidence softmax, for replay AND final
predictions. Refit lambda using the unchanged E041 procedure. This measures
conditional weight use plus its downstream lambda/parent effects. It does
not eliminate the learned activation mask or isolate fixed-lambda effects.
UNICEF and WB must remain probability-identical to E041/E025.

This follows E043's failed observed-data candidate-recall oracle. The user
prefers a technically validated informative submission over an unused slot.
This is an ablation, not a claimed .65 improvement candidate. No external
data or fitted external weights are bundled; previous Adult validation use
is disclosed in E041's scorecard and today's E043 oracle record.

## Pre-registered reading arms

| Grand / best update | Interpretation | Next action |
|---|---|---|
| >= .65, stable controls | Removing weight use has a favourable pipeline reading; noise and interactions still matter | Preserve new best; prioritize retained selection/replay and investigate harmful metric use |
| .64 with best update | Small favourable reading within displayed precision | Record instrument triple and retain winning snapshot; no exact effect claim |
| .64 without update | Effect unresolved at leaderboard resolution | Keep E041; next compare retained mechanisms rather than conclude metrics never help |
| .63 | Adverse reading consistent with useful learned weight use, near resolution | Keep E041; prioritize honest metric/selector research, no exact .03 attribution |
| <= .62 | Larger adverse reading | Keep E041 and its learned weights; deprioritize removing them |
| FAILED | No valid score; no effect inference | Diagnose locally; recorded rule says failed attempts do not consume the daily slot |

Grand .63-.64 is only a planning scenario, not a calibrated prediction or
confidence interval. Score can improve or worsen outside it. Do not infer
exact hidden instrument scores from rounded/noised Grand. Use newly visible
instrument scores when a best update occurs. Single-arm interventions remain
interpretable only as complete pipeline changes, not proof of a domain story.

## Required local checks

| Check | Actual result |
|---|---|
| Clean UNICEF / WB | .500648423 / .454717307; every vector equals both E041 and E025 |
| Clean UNHCR | E044 .562294713; E041 .562462729; E025 .562948874 |
| Clean no-regression | PASS; UNHCR delta -.000168016 vs E041, -.000654161 vs E025 |
| Clean mean delta vs E041 | -.000056005 |
| Existing household sim, seed13 | .552012531 to .555102556; +.003090025 UNHCR skill |
| Invariant tests | 15 passed; intervention, parent bindings, self-exclusion and split isolation |
| ZIP checker | PASS; only root main.py, no external model/data |
| Official phase-1 scorer | PASS x3; exact skills .500648423 / .454717307 / .562294713 |
| Source / extracted archive parity | Every vector exactly equal on all three schemas |
| Official local runtime | 371.022 s total; rounded per-schema times 42.009 / 106.256 / 222.758 s; shared budget 900 s |

The household sim mean equivalent is +.001030008, below the +.005 adoption
bar. Neither local result establishes a winning predictor. The archive is
prepared for measurement under the user's exploratory-slot preference.
Runtime used two numerical threads with another local simulation overlapping
part of the run; this is measured local timing, not a hosted speed guarantee.

Archive: `submissions/2026-09-20-E044.zip`.
SHA256: `310dd524b9c237f9d5e47c886a00e3105814a4f47cdcc906e9e5a8bce0e62936`.
Main SHA256: `d3c47c8e8f46abdd5683c6299787e3b37e7516661588f9b5cc59f791c52e55ea`.
No code change follows these readings. Exact technical evidence is in adjacent
`verification.json`; raw local/oracle outputs in `docs/analysis/E043-outputs/`.

## Actual hosted result

User reported Grand **0.63**, with **no best update**. UNICEF, World Bank and
UNHCR scores are unavailable; do not fill them from earlier submissions or
from arithmetic. Source: user report in this session, not an independent
platform fetch. Exact upload time, submission ID and hosted runtime were not
provided. This is a completed scored submission, not a failed attempt.

The preregistered **.63 adverse arm** applies. Relative to E041's displayed
.64, Grand is -.01. Because the intervention is UNHCR-only and local controls
were probability-identical, 3 * (-.01) = -.03 is an approximate UNHCR effect
translation, NOT an observed instrument delta. Rounded/noised scores and the
recorded instrument-scale resolution of about .015-.03 prevent an exact
effect claim or reconstructing a hidden UNHCR score such as .89.

Decision: reject E044 for adoption; keep E041 and its learned weights. The
result supports useful conditional learned weight use plus downstream lambda
and parent effects. It does not isolate fixed-lambda effects, remove learned
activation, or prove that all of E041's improvement came from its weights.
The positive household-sim direction did not transfer to the displayed DEV
reading. Next research should retain learned weights and prioritize honest
metric/selector validation; no repeated weight-removal grid. E041 remains
DEV best .64/.52/.49/.92; E025 remains the validated phase-2 fallback.
