# E032 — probe P1: gated items → uniform (loss map, gated vs content)
parent: E025
status: parked
date: 2026-09-14

## Hypothesis

Not a model change — a measurement. Replacing every gated item's vector
in the E025 output with the uniform vector removes exactly the gated
items' contribution: skill' = skill − share·(skill_G − u_G), with share
(156/213 unhcr, 30/76 wb, 7/12 unicef) and u_G (the uniform vector's
own per-cell skill on those items) exact from the schema. One
leaderboard reading therefore gives E025's mean per-cell skill on gated
items (skill_G) and, by subtraction, on the ungated content items
(skill_C) — the first real-data loss map. The sandbox cannot provide
it: its per-cell skills (unhcr gated 0.61 / content 0.42) are artifacts
of random marginals.

## Domain check

Pre-registered 2026-09-14 BEFORE submission. (a) technical: the
arithmetic is validated locally — predicted probe skill = direct
replacement = wrapper on all three sandboxes (unhcr 0.1067), inversion
recovers skill_G exactly (`src/models/probes.py`). Resolution on unhcr:
±0.01 reading ⇒ ±0.014 in skill_G. (b) background: on unhcr, gated
cells are dominated by the sentinel ("never asked"), which the gate
recursion predicts almost deterministically from a visible or
well-predicted parent; the E002→E005 history (0.41 → 0.63) is mostly
that. Content answers (return intention, needs, coping) are the hard
part. Expectation: skill_G ≈ 0.92–0.95, skill_C ≈ 0.72–0.80 on unhcr.
(c) readings — the map, not a verdict: remaining loss on gated cells =
0.732·(1 − skill_G), on content cells = 0.268·(1 − skill_C).
  - skill_G ≥ 0.95 ⇒ gated loss ≤ 0.037, content loss ≥ 0.07: the
    missing +0.03 lives in the 57 content items ⇒ next hypotheses go to
    content prediction (evidence transition tables, content-specific
    models), not gate math.
  - skill_G ≈ 0.90–0.92 ⇒ gated loss 0.06–0.07 ≈ content loss: the
    gate cascade still leaks — the "<5 gating changes" the organizers
    have not shipped, or approximate gates E010 does not capture ⇒ next
    probe splits gated cells by parent visibility.
  - skill_G ≤ 0.88 ⇒ gated cells are WORSE than content cells; the
    sentinel prediction is the lever ⇒ revisit gate decoding with a
    sentinel-rate model (E028's sim said null — the map would overrule).

## Change

`src/models/probes.py`: `uniform_on`, `decompose`, `uniform_skill`,
`read_probe`, `gated_items`. `submissions/2026-09-14-E032/main.py`:
E025 assembly + the probe wrapper (E025 renamed `predict_e025`).

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | unicef | world_bank | unhcr |
|---|---|---|---|
| E025 | 0.5006 | 0.4548 | 0.5629 |
| share / u_G | 0.583 / −0.066 | 0.395 / −0.063 | 0.732 / −0.009 |
| sandbox skill_G / skill_C | 0.565 / 0.410 | 0.542 / 0.398 | 0.614 / 0.424 |
| E032 probe (predicted = direct = wrapper) | 0.1326 | 0.2159 | 0.1067 |

Official score.py: see SCORES.md.

## Decision

Measurement; verdict = the map, recorded in SCORES.md after the reading.
