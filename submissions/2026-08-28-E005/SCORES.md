# 2026-08-28-E005 — soft-stratum (E003+E004 composed)

Experiment: E005 (adopted; parents E003 + E004, both adopted same day).
Code: self-contained build of `src/models/soft_stratum.py` (runner-verified
identical). Zip: `submissions/2026-08-28-E005.zip`, `check_submission_zip.py`
OK, no requirements.txt.

## Local scores (2026-08-28, seed 0, phase 1)

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact (runner) | 0.4333 | 0.4593 | 0.4105 | 0.5347 | 0.4682 |
| E002 baseline | 0.3210 | 0.3232 | 0.2909 | 0.4297 | 0.3479 |

Official `score.py` PASS ×3 (noised): 0.4600 / 0.4100 / 0.5300.
Wall-clock ≈ 101 s total (unhcr 83 s, dominated by runtime stratum
selection) ≪ 900 s. 19/19 tests pass. Violation sim (unhcr 17%):
soft-stratum beats hard-stratum +0.0422 log — the E003 layer is the
insurance for real approximate gates, invisible on the clean sandbox.

## Leaderboard expectation (real data)

Sandbox skills again do NOT predict LB numbers. Reference: yesterday's
E002 = 0.43 (0.45 / 0.43 / 0.41). Qualitative expectations, pre-registered:

- All three instruments should improve over E002 (GIVEN conditioning +
  cascade). unhcr has the most headroom (was pure marginal at 0.41; 155
  PREDICT-parent gates now active; low U amplifies gains).
- Stratum rule on real data is expected to select country×wave (unhcr),
  Country (unicef), and a non-country stratum (wb, country 38.8% recorded)
  — not directly observable, but a large unhcr move is the fingerprint.
- Risk logged: if unhcr DROPS below 0.41, suspect the softening was
  insufficient (α=20 too trusting of stated gates) — diagnostic: raise α /
  cap ã for the 59 round-2-only multi-select items.

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
| 905825 | 2026-08-28-E005.zip | 2026-08-28 20:24:21.138691 +09:00 | Finished | 0.5333333333 | 0.4900000000 | 0.4800000000 | 0.6300000000 | false |

[Complete score ledger](../SCORES.md) and [sanitized source](../hosted-scores/2026-09-27.json).
All score precision fields are 2. Failed attempts have no scores; never substitute zero.
