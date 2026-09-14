# E034 — probe P3: evidence layer off on unhcr (component contribution)
parent: E033
status: parked
date: 2026-09-16

## Hypothesis

Measurement. E032/E033 established that content prediction carries
most of E025's unhcr skill on both item groups. P3 asks WHICH component
carries it: with the household evidence layer switched off (λ = 0, the
net + ladder + gate recursion + E010 agreement stand alone) on the
unhcr schema only,

    Δ_unhcr = 3 · (Grand_E034 − 0.633) = −(evidence layer's real-data
    contribution inside the E025 stack).

The E018 reading (unhcr 0.78 → 0.87, later 0.89 with E019/E022/E025)
was taken in a weaker stack; the contribution inside E025 is what
matters for the next lever: evidence-driven content skill ⇒ the lever is
match coverage (phase 2's larger pool helps; twin-answer transition
tables act only on matched rows); model-driven ⇒ the lever is
P(item | GIVEN) on unmatched rows.

## Domain check

Pre-registered 2026-09-16 BEFORE submission. (a) technical: the clean
sandbox has no household structure, so E034 ≈ E025 there (E018 measured
−0.0003 for the layer); the household sim shows the layer's value under
injected twins. Assembled file = src composition (parity below). (b)
background: the leaderboard history is the domain here — the layer
bought +0.11 unhcr over E012-era stacks; the two CATI rounds recur the
same households, so the matched fraction is large. Expected Δ_unhcr
−0.09 to −0.12 ⇒ **Grand 0.59–0.60**. (c) readings:
  - Grand ≥ 0.61 (Δ_unhcr ≥ −0.07) ⇒ the layer contributes less than
    its history suggests inside E025 (the net absorbed part of it);
    content skill is model-driven ⇒ base-model levers on unmatched rows.
  - Grand 0.59–0.60 ⇒ as history ⇒ both; evidence transition tables
    (matched rows) and base-model work both have room.
  - Grand ≤ 0.58 (Δ_unhcr ≤ −0.15) ⇒ content skill is mostly evidence
    ⇒ lever = the evidence layer: recall (more matches), sharper λ on
    concentrated rows, transition tables.

## Change

`submissions/2026-09-16-E034/main.py`: E025 assembly; on the unhcr
schema `layer_fn` returns ({}, {}); other schemas untouched.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

Parity (src composition vs assembled) and household-sim contribution:
see SCORES.md.

## Decision

Measurement; verdict = the reading, recorded in SCORES.md.
