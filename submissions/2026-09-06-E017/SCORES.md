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
(noised sandbox, consistent with exact).

## v3 revision after hosted failure (2026-09-06)

The v1 upload (4-config grid, ~465 s local) came back **submission
failed** — the campaign's first hosted failure. Sanitized error code
pending from the submissions panel; leading suspect is TIMEOUT (we have
never observed hosted wall-clock; E012-family at ~200–250 s local
passed, 465 s local may exceed 900 s hosted if the worker is ~2×
slower). v2 ({64, 256} extremes) was built and DISCARDED: with it the
unhcr selector fell back to the baseline — blind A/B on the main
target. **v3 (shipped)**: grid {64×2, 128×2+dropout} — exactly the
configs the full grid selected (unicef baseline = control, wb/unhcr
128×2), reproducing v1's selections bit-for-bit at ~340 s local
(−27%). Same pre-registered readings apply. If v3 also fails with a
timeout-class code, the emergency fallback is pinned per-instrument
configs (zero selection cost, ~E012 runtime) — prepared but not
preferred, since it would let the sandbox choose for real data.

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
| 914419 | 2026-09-06-E017.zip | 2026-09-04 12:16:49.178086 +09:00 | Failed | not reported | not reported | not reported | not reported | false |
| 914481 | 2026-09-06-E017.zip | 2026-09-04 14:11:47.114577 +09:00 | Finished | 0.6000000000 | 0.5200000000 | 0.4900000000 | 0.7900000000 | false |

[Complete score ledger](../SCORES.md) and [sanitized source](../hosted-scores/2026-09-27.json).
All score precision fields are 2. Failed attempts have no scores; never substitute zero.
