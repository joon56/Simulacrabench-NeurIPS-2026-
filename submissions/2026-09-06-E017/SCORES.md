# 2026-09-06-E017 — pre-registered capacity A/B (trunk grid selection)

Experiment: E017 (parent E015 parked; the A/B its park verdict named).
Code: E012 stack with per-instrument trunk architecture selected from
{64×2, 128×2+do, 256×2+do, 128×3+do} on the internal holdout. This is
a MEASUREMENT submission: locally +0.0001 vs E012 (verified no-harm),
spent to read the one axis the 1-factor sandbox provably cannot measure
(three independent local nulls: E009/E011/E015). Zip:
`submissions/2026-09-06-E017.zip`, check_submission_zip OK.

## Local scores (2026-09-05, seed 0, phase 1)

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact (runner) | 0.4436 | 0.5006 | 0.4548 | 0.5633 | 0.5062 |
| E012 (LB 0.60) | 0.4429 | 0.5006 | 0.4549 | 0.5629 | 0.5061 |

Parity exact. Official score.py PASS ×3: 0.5000 / 0.4600 / 0.5600
(noised sandbox, consistent with exact). Wall-clock ~465 s
local (4 configs trained per instrument) — under the 900 s budget with
~2× margin; E012-family precedent says hosted ≈ local.

## Leaderboard expectation (real data) — the readings ARE the experiment

Reference: E012 LB = 0.60 (unicef 0.52 / wb 0.49 / unhcr 0.78).
Pre-registered in docs/experiments/E017-capacity-ab.md (2026-09-05):

- unhcr and/or wb ≥ +0.02 ⇒ real multi-factor capacity exists; REOPEN
  the capacity ladder as the main line; treat local capacity nulls as
  uninformative from now on.
- flat (±0.01) ⇒ capacity axis dead on real data too ⇒ the 0.92 gap is
  NOT architecture ⇒ redirect remaining slots to unhcr structure and
  calibration.
- any instrument ≤ −0.02 ⇒ holdout architecture selection overfits real
  visible rows ⇒ pin DEFAULT_CONFIG permanently.
- unicef = control (selector stays small there); a unicef move ⇒
  selection instability, discount the reading.

Context: same-day E016 (ladder MAX_CARD lift) rejected at +0.0002
local; its geography claim joins the A/B candidate pool but is NOT
bundled here (one change per A/B).
