# 2026-09-14-E032 — PROBE P1: E025 with gated items → uniform

Experiment: E032 (measurement, parent E025). Code: the E025 assembly
(`predict_e025`, untouched) wrapped so every gated item's output vector
is the uniform vector; content items unchanged. Zip:
`submissions/2026-09-14-E032.zip`, check_submission_zip OK.

## Local (2026-09-14, seed 0, phase 1)

| | unicef | world_bank | unhcr |
|---|---|---|---|
| E025 exact | 0.5006 | 0.4548 | 0.5629 |
| E032 exact (predicted = direct = wrapper) | 0.1326 | 0.2159 | 0.1067 |
| gated share (schema) | 0.583 | 0.395 | 0.732 |
| u_G (uniform's own per-cell skill on gated items) | −0.066 | −0.063 | −0.009 |

Official score.py PASS ×3: 0.1300 / 0.2100 / 0.1100 (= predicted to the
grader's rounding). Runtime = E025's (32 / 80 / 161 s local, CPU training).

## How to read the leaderboard

skill_G = (skill_E025 − skill_E032) / share + u_G ; skill_C = (skill_E025
− share·skill_G) / (1 − share). Reference E025 LB: unicef 0.52 / wb 0.49 /
unhcr 0.89 (each ±0.01). Resolution: unhcr ±0.014 in skill_G; unicef
±0.017; wb ±0.025.

Pre-registered expectation (unhcr): E032 reads **0.20–0.22**
(skill_G ≈ 0.92–0.95 ⇒ skill_C ≈ 0.72–0.80). Grand will drop to ~0.2 —
irrelevant, the leaderboard keeps the best.

| E032 unhcr reading | skill_G | skill_C | remaining loss gated / content | next |
|---|---|---|---|---|
| ≤ 0.19 | ≥ 0.95 | ≤ 0.73 | ≤ 0.037 / ≥ 0.072 | content items are the lever: evidence transition tables, content-specific models |
| 0.20–0.23 | 0.90–0.94 | 0.75–0.86 | 0.04–0.07 / 0.04–0.07 | both matter; next probe splits gated cells by parent visibility |
| ≥ 0.24 | ≤ 0.89 | ≥ 0.89 | ≥ 0.08 / ≤ 0.03 | sentinel prediction is the lever; the gate cascade leaks (unshipped gating fixes?) — revisit gate decoding despite E028 |

unicef / wb: same arithmetic, recorded for completeness (both at the
field's ceiling).

## Actual leaderboard result

(pending)
