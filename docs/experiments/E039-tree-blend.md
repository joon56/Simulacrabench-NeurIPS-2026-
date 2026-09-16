# E039 — gradient-boosted trees as a second base model (blend on the holdout)
parent: E025
status: parked
date: 2026-09-19

## Hypothesis

A005 puts the shared-trunk net at the sandbox's GIVEN-only Bayes
ceiling, so no base-model change can show locally — but on real data
the ladder still earns blend weight (w ≈ 0.6–0.9 vs 1.0 on the
sandbox), i.e. the net leaves real GIVEN interactions on the table.
Per-item HistGradientBoosting on the integer-coded GIVEN block, mixed
into the full-head distribution at a per-instrument weight v tuned on
the outer holdout (v = 0 ⇒ E025), could recover part of that on real
unhcr. Locally the expected reading is v = 0 (A005); the real test is a
leaderboard A/B, which requires the phase-1 runtime budget.

## Domain check

Pre-registered 2026-09-19 BEFORE the run. (a) technical: trees fitted
once on the fit split (no refit), 213 items × ~0.4 s; the blend weight
is the calibration guard. Expected local: v = 0, skill = E025;
runtime the real question — the CPU-side budget is ≲ 150 s local (E019
timed out at ~240 s local total). (b) background: n/a. (c) readings:
runtime ≤ +40 s local ⇒ package as an A/B; more ⇒ park for phase 1
(phase 2 has 3,600 s but no way to validate a single-shot change).

## Change

`src/models/tree_blend.py` (`_fit_trees`, `_tree_proba`, `predict`
with the `_Mixed` wrapper through `link_sharp`'s `tune_fn` hook).

## Result (unhcr sandbox, phase 1)

skill 0.5629 (= E025), holdout log score by v: 0 → −0.55088, 0.1 →
−0.55114, 0.2 → −0.55196 … 0.5 → −0.55743 — monotone worse, v = 0
chosen. Runtime 357 s vs ~200 s for E025 on the same machine: **+140 s
CPU-side** (fits + probabilities for 213 items).

## Decision

**Parked.** As A005 predicts, the sandbox cannot show a base-model
gain (v = 0); and the CPU-side cost (+140 s local ⇒ +500 s on a slow
hosted worker) breaks the phase-1 budget, so it cannot even be read as
an A/B. A content-items-only variant (57 items, ≈ +35 s) would fit but
tests only the 0.031 content pool. Revisit only if a phase-1 A/B shows
the base model moving on real data by another route.
