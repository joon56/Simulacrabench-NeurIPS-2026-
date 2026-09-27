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

## Actual leaderboard result (2026-09-15)

**Grand 0.55** (best unchanged at 0.63). Δ_grand = −0.08 (exact
reference 0.633 ⇒ −0.083) ⇒ **Δ_unhcr ≈ −0.24 to −0.25, unhcr ≈ 0.64–0.65,
s_sent = 0.892 − 0.24/0.732 ≈ 0.56** (±0.04). Far below the pre-registered
0.60–0.62 band: the clear CONTENT arm.

Reading. With gated content flattened, gated cells keep only 0.56 of
their 0.892 per-cell skill — E025 earns ~0.33 per gated cell from
predicting what the asked respondents say. Since a sentinel cell is
untouched by the transform, s_sent ≈ 0.56 also bounds the sentinel-cell
fraction from below (perfect sentinel prediction on a fraction f of
cells gives at most ≈ f): asked cells are a substantial minority of
gated cells and E025 predicts their content well (≥ 0.75 per asked
cell). Revision of the E032 narrative: gated ≈ content per cell is not
proof that sentinel prediction is bad — gated cells are a mix of easy
sentinel cells and asked-content cells that behave like content items.
The loss split sentinel/content inside gated items is NOT identifiable
from P1+P2 (needs the sentinel fraction, a dataset statistic we do not
probe for). What IS established: content prediction carries most of
E025's unhcr skill on both item groups, so the largest addressable pool
is content — the 57 content items (loss 0.031) plus the asked cells of
gated items (part of 0.079).

Next: P3 (E034) switches the evidence layer off on unhcr — is the
content skill evidence-driven (⇒ lever = match coverage, helped by the
phase-2 pool) or base-model-driven (⇒ lever = P(item | GIVEN))?

## API score reconciliation - 2026-09-27

Source: user-supplied My Submissions JSON, recorded 2026-09-27.
This supplement supersedes missing-score/ID/time statements above for the IDs
listed here; the earlier registration, interpretation and local checks remain
historical. Values below are released API scores, not unnoised raw scores.
Created time is platform submission metadata, not the snapshot directory date.
Current leaderboard membership is not a historical best-update event log.
The uploaded ZIP bytes/hash and hosted runtime are not verified by this response.

| Submission ID | Filename | Created (KST) | Status | Grand API | UNICEF API | World Bank API | UNHCR API | On leaderboard at snapshot |
|---|---|---|---|---:|---:|---:|---:|---|
| 925831 | 2026-09-15-E033.zip | 2026-09-14 18:08:58.435880 +09:00 | Finished | 0.5500000000 | 0.5200000000 | 0.4900000000 | 0.6400000000 | false |

[Complete score ledger](../SCORES.md) and [sanitized source](../hosted-scores/2026-09-27.json).
All score precision fields are 2. Failed attempts have no scores; never substitute zero.
