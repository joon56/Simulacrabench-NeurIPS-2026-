# E033 — probe P2: gated items keep the sentinel mass, content uniform
parent: E032
status: parked
date: 2026-09-15

## Hypothesis

Measurement, not a model change. E032 read unhcr's gated cells at
per-cell skill 0.892 — no easier than content cells, unlike the
exact-gate instruments — so 72% of the remaining unhcr loss sits in the
156 gated items. P2 asks what E025 gets from CONTENT inside those
cells: for every gated item the model's sentinel mass is kept and the
remaining mass is spread uniformly over the asked options; content
items are untouched; the transform is applied to the UNHCR schema only
(per-instrument scores are hidden unless the best improves, so the
Grand reading must isolate one instrument: Δ_unhcr = 3·Δ_Grand). Then

    Δ_P2 = skill_E033 − skill_E025 = −share · (skill_G − s_sent)

with s_sent the gated cells' per-cell skill from sentinel knowledge
alone. Small |Δ| ⇒ E025 extracts little from content on gated items
(inherently unpredictable, or most gated cells are sentinel cells) ⇒
the recoverable gated loss is on the sentinel side ("who is skipped");
large |Δ| ⇒ content inside gated items carries much of E025's skill
and its residual is part of the leak. No dataset statistic is read:
only model-component contributions.

## Domain check

Pre-registered 2026-09-15 BEFORE submission. (a) technical: direct =
wrapper on unicef (0.3502); unhcr sandbox Δ −0.0554, wb −0.0935,
unicef −0.1504 (sandbox content is random-marginal, so these are not
predictions of the real Δ). (b) background: ERPIS gated blocks are
asked of subsets (returnees' intentions, those with children, those
who received assistance); the asked-content items are substantive
(intention timing, obstacles, needs) and on real data are the ones the
household evidence layer predicts well when a twin exists. Expected
real Δ on unhcr: −0.04 to −0.10 (content inside gated items worth
0.05–0.14 per cell). (c) readings:
  - |Δ| ≤ 0.03 (s_sent ≥ 0.85) ⇒ content adds little inside gated
    cells; the gated leak is sentinel prediction ⇒ hypothesis H1:
    replay-calibrated sentinel mass in the predicted-parent regime
    (blank visible rows' PREDICT block, run the model, fit a per-item
    sentinel calibration against the realized sentinel indicator);
    channel = E028's branch-overlap sim + an approximate-gate sim.
  - 0.04 ≤ |Δ| ≤ 0.10 ⇒ both sides carry skill; H1 first (cheaper),
    then content-side hypotheses.
  - |Δ| ≥ 0.11 (s_sent ≤ 0.74) ⇒ content inside gated items is where
    E025 earns its gated skill; the residual leak is content ⇒ content
    hypotheses (evidence transition tables) before H1.

## Change

`src/models/probes.py`: `sentinel_only`, `sentinel_only_vector`.
`submissions/2026-09-15-E033/main.py`: E025 assembly + P2 wrapper.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | unicef | world_bank | unhcr |
|---|---|---|---|
| E025 | 0.5006 | 0.4548 | 0.5629 |
| E033 (unhcr-only; direct = wrapper) | 0.5006 | 0.4548 | 0.5076 |

Official score.py: see SCORES.md.

## Decision

Measurement; verdict = the reading, recorded in SCORES.md.
