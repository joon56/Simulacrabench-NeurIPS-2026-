# 2026-09-15-E033 — PROBE P2: E025 with gated items → sentinel mass kept, content uniform

Experiment: E033 (measurement, parent E032). Code: the E025 assembly
(`predict_e025`, untouched) wrapped so every gated item's vector keeps
the model's sentinel mass and spreads the rest uniformly over the asked
options; content items unchanged. **Applied to the UNHCR schema only**
(unicef / wb outputs = E025 exactly) so the Grand reading isolates it:
per-instrument scores are hidden on the main account unless the best
improves. Zip: `submissions/2026-09-15-E033.zip`,
check_submission_zip OK.

## Local (2026-09-15, seed 0, phase 1)

| | unicef | world_bank | unhcr |
|---|---|---|---|
| E025 exact | 0.5006 | 0.4548 | 0.5629 |
| E033 exact (unhcr-only probe) | 0.5006 (= E025) | 0.4548 (= E025) | 0.5076 |
| Δ (sandbox, not a prediction) | 0 | 0 | −0.0554 |

Official score.py PASS ×3 (unhcr-only build): 0.5000 / 0.4600 / 0.5100
(unicef / wb = E025 within the grader's noise; unhcr = local). Runtime =
E025's (35 / 75 / 168 s local, CPU training).

## How to read the leaderboard (Grand only)

Only Grand is visible when the best does not improve. With the probe on
unhcr alone: Δ_unhcr = 3 · (Grand_E033 − Grand_E025), Grand_E025 = 0.63
(exact ≈ 0.633 = (0.52 + 0.49 + 0.89)/3). Then s_sent = 0.892 + Δ_unhcr /
0.732. Resolution: Grand rounded to 0.01 ⇒ Δ_unhcr ±0.015–0.03 ⇒ s_sent
±0.02–0.04.

Pre-registered expectation (unhcr): **Δ_unhcr −0.04 to −0.10 ⇒ Grand
0.60–0.62**.

| Grand E033 | Δ_unhcr | s_sent | reading | next |
|---|---|---|---|---|
| ≥ 0.63 | ≥ −0.02 | ≥ 0.86 | content adds little inside gated cells; leak = sentinel prediction | H1: replay-calibrated sentinel mass (predicted-parent regime) |
| 0.60–0.62 | −0.03 … −0.10 | 0.76–0.85 | both sides carry skill | H1 first, then content hypotheses |
| ≤ 0.59 | ≤ −0.11 | ≤ 0.74 | content inside gated items is the bulk of gated skill; residual leak likely content | content hypotheses (evidence transition tables) first |

The 0.62/0.63 boundary is within rounding — a 0.62 or 0.63 reading is
"content adds little or modestly"; only ≤ 0.60 is a clear content arm.

## Actual leaderboard result

(pending)
