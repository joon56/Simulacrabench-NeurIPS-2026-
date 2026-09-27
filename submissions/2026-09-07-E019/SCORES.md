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

## Actual leaderboard result (2026-09-07)

First upload: **time limit exceeded** (same zip re-uploaded the next
day RAN — hosted worker speed varies day to day; ~240 s local is not
safe). Result of the run: **Grand 0.63, no update** — E019 ≤ E018,
i.e. unhcr within noise of 0.87. **The flat arm fired.** Reading per
pre-registration: real twins are noisier than the sim's 10%-perturbed
copies, so the real λ optimum already sat ≤ 0.9 and/or max-posterior
concentration does not separate an exact-twin regime on real data.
Consequence for the instrument: the within-round dup sim must be
re-calibrated with heavier answer perturbation before it is trusted
for further layer tuning — its +0.031 prediction did not transfer,
whereas E018's +0.06 prediction did (direction right, magnitude not).

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
| 916707 | 2026-09-07-E019.zip | 2026-09-06 18:46:52.818164 +09:00 | Failed | not reported | not reported | not reported | not reported | false |
| 916756 | 2026-09-07-E019.zip | 2026-09-06 19:12:13.692340 +09:00 | Finished | 0.6266666667 | 0.5200000000 | 0.4900000000 | 0.8700000000 | false |

[Complete score ledger](../SCORES.md) and [sanitized source](../hosted-scores/2026-09-27.json).
All score precision fields are 2. Failed attempts have no scores; never substitute zero.
