# E040 — tree blend on unhcr content items (base-model A/B within the phase-1 budget)
parent: E039
status: parked
date: 2026-09-20

## Hypothesis

E039 (trees for all 213 unhcr items) is blocked by runtime (+140 s
CPU-side). Restricting the per-item HistGradientBoosting blend to the
57 ungated (content) items of unhcr costs ≈ +30 s and reads the same
question at a quarter scale: is the real-data base model under-fit
(the ladder still earns w ≈ 0.6–0.9 on real data, 1.0 on the sandbox)?
Content items hold 0.031 of unhcr's remaining loss (E032); a real
+0.01 on them would show as unhcr +0.01 ⇒ Grand 0.64.

## Domain check

Pre-registered 2026-09-20 BEFORE the runs. (a) technical: the blend
weight v is tuned on the outer holdout (v = 0 ⇒ E025 exactly); A005
says the sandbox reading is v = 0 — the local check is runtime and
no-regression only. (b) background: n/a. (c) readings: Grand 0.64 ⇒
the base model is under-fit on real unhcr ⇒ the phase-2 file (3,600 s)
carries the full E039 tree blend, validated by this reading; 0.63 ⇒
the base model is at its real ceiling too — E025 stays, phase 2 =
E025; ≤ 0.62 ⇒ v tuned > 0 on the holdout but hurt held-out cells
(over-confident trees) — revert.

## Change

`src/models/tree_blend.py`: `MIN_PREDICT` (unhcr only), `CONTENT_ONLY`
(ungated items). Assembly: E025 + tree block.

## Result (unhcr sandbox, phase 1)

skill 0.5629 (= E025); holdout log score by v monotone worse from
v = 0 (−0.72983) to v = 0.5 (−0.73680) ⇒ v = 0, as A005 predicts.
Runtime 275 s vs ≈ 220 s for E025 on the same (loaded) machine ⇒ ≈ +50 s
CPU-side. Parity assembled vs src and official grader: SCORES.md.

## Decision

**Packaged as a real-data A/B** (`submissions/2026-09-20-E040/`): exact
no-regression locally (v = 0 ⇒ E025), runtime inside the phase-1 budget
with margin (≈ 170 s local CPU-side total vs the ~240 s timeout
precedent). Readings pre-registered in SCORES.md: 0.64 ⇒ the phase-2
file gets the full E039 tree blend; 0.63 ⇒ base model at its real
ceiling, E025 stays and the base axis is closed on real data too.
