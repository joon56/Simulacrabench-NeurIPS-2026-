# 2026-09-15-E033 — PROBE P2: E025 with gated items → sentinel mass kept, content uniform

Experiment: E033 (measurement, parent E032). Code: the E025 assembly
(`predict_e025`, untouched) wrapped so every gated item's vector keeps
the model's sentinel mass and spreads the rest uniformly over the asked
options; content items unchanged. Zip: `submissions/2026-09-15-E033.zip`,
check_submission_zip OK.

## Local (2026-09-15, seed 0, phase 1)

| | unicef | world_bank | unhcr |
|---|---|---|---|
| E025 exact | 0.5006 | 0.4548 | 0.5629 |
| E033 exact (direct = wrapper) | 0.3502 | 0.3613 | 0.5076 |
| Δ (sandbox, not a prediction) | −0.1504 | −0.0935 | −0.0554 |

Official score.py PASS ×3: 0.3500 / 0.3600 / 0.5100 (= local to the
grader's rounding). Runtime = E025's (32 / 76 / 175 s local, CPU training).

## How to read the leaderboard

Δ = skill_E033 − skill_E025 (E025 LB: 0.52 / 0.49 / 0.89, each ±0.01).
s_sent = skill_G + Δ / share, with skill_G from E032 (unhcr 0.892, wb
0.747, unicef 0.654) and share 0.732 / 0.395 / 0.583.

Pre-registered expectation (unhcr): **Δ −0.04 to −0.10** (E033 reads
0.79–0.85).

| E033 unhcr | Δ | s_sent | reading | next |
|---|---|---|---|---|
| ≥ 0.86 | ≥ −0.03 | ≥ 0.85 | content adds little inside gated cells; leak = sentinel prediction | H1: replay-calibrated sentinel mass (predicted-parent regime) |
| 0.79–0.85 | −0.04 … −0.10 | 0.76–0.84 | both sides carry skill | H1 first, then content hypotheses |
| ≤ 0.78 | ≤ −0.11 | ≤ 0.74 | content inside gated items is the bulk of gated skill; residual leak likely content | content hypotheses (evidence transition tables) first |

unicef / wb recorded for completeness.

## Actual leaderboard result

(pending)
