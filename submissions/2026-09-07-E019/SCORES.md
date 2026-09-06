# 2026-09-07-E019 — sharpened evidence layer (λ ceiling + concentration buckets)

Experiment: E019 (adopted; parent E018). Code: script-assembled merge
incl. link_sharp. Two changes over E018: λ grid extended to {…, 0.95,
0.98}; per-item λ split into (diffuse, concentrated) buckets at max
posterior weight ≥ 0.5, both replay-calibrated. Pool, scoring,
self-exclusion, caps, E012 stack unchanged. Zip:
`submissions/2026-09-07-E019.zip`, check_submission_zip OK.

## Local scores (2026-09-06, seed 0, phase 1)

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact (runner) | 0.4429 | 0.5006 | 0.4549 | 0.5626 | 0.5060 |
| E018 (LB 0.63) | 0.4429 | 0.5006 | 0.4549 | 0.5626 | 0.5060 |

Identical on the clean sandbox (no duplicates ⇒ inert). Dup sim (the
instrument whose ≥+0.02 arm fired at +0.09 on the real leaderboard):
**+0.0312 log over E018**. Official score.py PASS ×3: 0.5000 / 0.4500 /
0.5600 (parity exact vs src). Wall-clock
~240 s local — inside the hosted bracket.

## Leaderboard expectation (real data)

Reference: E018 LB = 0.63 (unicef 0.52 / wb 0.49 / unhcr 0.87).
Pre-registered 2026-09-06 BEFORE submission:

- **unhcr up ≥ +0.02** ⇒ the ceiling and/or the bucket split bind on
  real twins as on the sim; expected 0.89–0.91 (sim Δ +0.031 log ≈
  +0.025 skill at U 1.2618; real twin rate unknown, could be higher).
  Grand ≈ 0.64.
- unhcr +0.01 ⇒ real gain but smaller than sim (real twins noisier
  than the 10%-perturbed sim twins) — keep, next lever is K/weights.
- unhcr flat ⇒ the real λ optimum already sat below 0.9 and buckets
  didn't separate — real duplicates are noisier than assumed; revisit
  the perturbation level of the sim instrument.
- **unhcr DOWN** ⇒ λ=0.98 on false-but-concentrated matches — the
  exact risk pre-registered; response: raise CONC_SPLIT (0.5→0.8) or
  cap the concentrated grid at 0.95.
- unicef/wb flat (λ≈0 there on real data per E018).
