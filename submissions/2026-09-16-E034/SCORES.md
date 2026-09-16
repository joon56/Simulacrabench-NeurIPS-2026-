# 2026-09-16-E034 — PROBE P3: E025 with the evidence layer OFF on unhcr

Experiment: E034 (measurement, parent E033). Code: the E025 assembly;
on the unhcr schema the household evidence layer is replaced by an
empty layer (λ = 0 — net + ladder + gate recursion + E010 agreement
only). unicef / wb = E025 exactly. Zip: `submissions/2026-09-16-E034.zip`,
check_submission_zip OK.

## Local (2026-09-16, seed 0, phase 1)

| | unhcr clean sandbox | household sim (log score) |
|---|---|---|
| E025 | 0.5629 | −0.5627 |
| E034 (evidence off) | 0.5633 (src composition = assembled, 0.563271 both) | −0.5860 (layer worth 0.0233 log with injected twins) |

Official score.py PASS ×3: 0.5000 / 0.4600 / 0.5600 (unicef / wb = E025;
unhcr = E025 within noise — the clean sandbox has no twins). Runtime ≤
E025's (42 / 92 / 188 s local, CPU training).

## How to read the leaderboard (Grand only)

Δ_unhcr = 3 · (Grand_E034 − 0.633); evidence contribution = −Δ_unhcr.

Pre-registered expectation: **Δ_unhcr −0.09 to −0.12 ⇒ Grand 0.59–0.60**.

| Grand E034 | Δ_unhcr | reading | next |
|---|---|---|---|
| ≥ 0.61 | ≥ −0.07 | layer contributes less than history inside E025; content skill is model-driven | base-model levers on unmatched rows |
| 0.59–0.60 | −0.08 … −0.13 | as history; both matter | transition tables (matched) + base-model work |
| ≤ 0.58 | ≤ −0.15 | content skill is mostly evidence | evidence-layer levers: recall, sharper λ, transition tables |

## Actual leaderboard result (2026-09-16)

**Grand 0.60** (best unchanged). Δ_unhcr = 3·(0.60 − 0.633) ≈ **−0.10**
(±0.03) ⇒ unhcr without the evidence layer ≈ **0.79**; the layer is
worth ≈ +0.10 inside E025 — the pre-registered middle arm, exactly the
E012→E025 history (0.78 → 0.89). Content skill is carried by BOTH the
base model (0.79 alone) and the evidence layer (+0.10).

Map after P1–P3 (unhcr): total 0.89; gated cells 0.892/cell, content
cells 0.885; sentinel knowledge alone leaves gated cells at 0.56; base
model alone 0.79; evidence +0.10. Remaining 0.11 has no single owner:
each component's next +0.01 is a separate piece of work.
