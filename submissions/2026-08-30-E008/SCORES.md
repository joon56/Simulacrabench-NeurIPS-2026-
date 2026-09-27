# 2026-08-30-E008 — full-GIVEN logistic blend + backoff ladder + soft gating

Experiment: E008 (adopted; parent E006). Code: self-contained merge of
`src/models/hier_backoff.py` + `src/models/logit_blend.py`. No bundled
artifacts, no requirements.txt (scikit-learn pre-installed in the hosted
image). Zip: `submissions/2026-08-30-E008.zip`, check_submission_zip OK.

## Local scores (2026-08-30, seed 0, phase 1)

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact (runner) | 0.4418 | 0.4994 | 0.4447 | 0.5532 | 0.4991 |
| E006 (LB 0.55) | 0.4385 | 0.4772 | 0.4196 | 0.5382 | 0.4783 |

Official score.py PASS ×3: 0.5000 / 0.4500 / 0.5500 (noised sandbox,
consistent with exact). Wall-clock ~182 s total
(≪ 900 s). Tests 27/27. Tuned blend weights (sandbox): 0.6 / 0.9 / 0.8 /
0.6 — all interior, smooth concave holdout curves.

## Leaderboard expectation (real data)

Reference: E006 LB = 0.55 (unicef 0.50 / wb 0.48 / unhcr 0.66).
Pre-registered 2026-08-30 BEFORE submission:

- Clear gain expected — sandbox Δ +0.021 is 2× the E006 step, and the
  E005/E006 leaderboards showed real GIVEN-answer coupling is STRONGER
  than the sandbox trait, so the real Δ should be ≥ the sandbox Δ.
  Expected Grand ≈ 0.57–0.59.
- **world_bank moves for the first time since E002** (flat 0.48 across
  three submissions): its 30-column GIVEN block holds banded psychometric
  scores (g-factor / many-weak-predictors — exactly what the logistic
  sees and the 3-column ladder cannot). wb staying flat at 0.48 ± noise
  DOES falsify the (b) domain claim → next lever is C/regularization or
  feature interactions, not more depth.
- unhcr largest absolute gain (72 GIVEN columns; 155 PREDICT gate
  parents multiply parent-belief improvements; cheapest U). unicef
  smallest (7 GIVEN, ladder already used 3 of them).
- Risk watch: logistic on real data could be overconfident where real
  coupling is weaker than sandbox trait_scale=2.0. The interior blend
  weight is the guard. Any instrument dropping > 0.02 ⇒ suspect
  overconfident logits → re-tune with C grid {0.1, 0.3, 1.0} and/or
  per-item w before the next submission.

## Actual leaderboard result (2026-08-30)

**Grand 0.58 — unicef 0.51 / world_bank 0.49 / unhcr 0.74**
(E006: 0.50 / 0.48 / 0.66). Scorecard vs pre-registration:

- Grand 0.57–0.59 ✓ (0.58, center of the band).
- unhcr largest absolute gain ✓ — +0.08, ~4–5× the sandbox Δ (+0.015);
  third consecutive submission where real GIVEN-answer coupling beats
  the sandbox trait, now the strongest instance.
- unicef smallest ✓ (+0.01).
- world_bank +0.01: NOT falsified (condition was flat at 0.48) but NOT
  confirmed either — +0.01 sits inside the ±0.01–0.02 noise. The
  psychometric many-weak-predictors claim stays OPEN; needs a second
  data point (a wb-targeted change) before believing or dropping it.
- No instrument down ⇒ no overconfidence signal; C=1.0 and single-w
  guard held.

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
| 908518 | 2026-08-30-E008.zip | 2026-08-30 19:28:44.662665 +09:00 | Finished | 0.5800000000 | 0.5100000000 | 0.4900000000 | 0.7400000000 | false |

[Complete score ledger](../SCORES.md) and [sanitized source](../hosted-scores/2026-09-27.json).
All score precision fields are 2. Failed attempts have no scores; never substitute zero.
