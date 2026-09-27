# 2026-09-06-E018 — full-pool visible-row evidence (within-round axis)

Experiment: E018 (adopted, E003 route; parent E014 parked). Code:
script-assembled merge incl. dup_link. Candidates = ALL visible rows
(self excluded, no round-column gate — every instrument gets the
layer); rarity-weighted signature scores → top-10 softmax posterior →
posterior-mixed answers as evidence → per-item λ from the visible-row
replay (capped at 6,000 queries for runtime). λ→0 ⇒ inert. Zip:
`submissions/2026-09-06-E018.zip`, check_submission_zip OK.

## Local scores (2026-09-05, seed 0, phase 1)

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact (runner) | 0.4429 | 0.5006 | 0.4549 | 0.5626 | 0.5060 |
| E012 (LB 0.60) | 0.4429 | 0.5006 | 0.4549 | 0.5629 | 0.5061 |

Sims: within-round duplicate sim scored **+0.0588 log**; layer-level
E018 arms 159 items vs E014's 40 on the same sim (the cross-round
blindness measured). Official score.py PASS ×3: 0.5000 / 0.4500 /
0.5600 (parity exact vs src). Wall-clock
250 s local — worst-case ~650 s hosted under the E017-established
bracket (1.94–2.6×).

## Leaderboard expectation (real data)

Reference: E012/E013/E014/E017 LB = 0.60 (0.52 / 0.49 / 0.78–0.79).
Pre-registered 2026-09-05 BEFORE submission:

- **Any instrument up ≥ +0.02** ⇒ real within-round near-duplicates
  (or a real k-NN residual) exist at that scale — tighten the layer
  (raise K, refine weights) next.
- **+0.01 moves** ⇒ weak signal, ambiguous with noise — one repeat
  before believing.
- **All flat** ⇒ the duplicate axis is dead and the evidence-layer
  family (E013 cross-round hard, E014 cross-round soft, E018 full
  pool) closes WHOLE: no form of row-matching pays on this build.
  Remaining 0.92 suspects would then be joint s3_11 branch decoding
  and calibration — and the possibility that the leaders' edge is
  something we have not conceived.
- Down > 0.01 anywhere ⇒ λ calibration failed conservatively-biased
  expectations — cap λ grid and diagnose before further layer work.
- unicef/wb now ALSO carry the layer (first time) — their flatness is
  no longer structural; watch them as live readings, not controls.

## Actual leaderboard result (2026-09-06)

**Grand 0.63 — unicef 0.52 / world_bank 0.49 / unhcr 0.87**
(reference: 0.52 / 0.49 / 0.78). Scorecard:

- **unhcr +0.09 — the ≥+0.02 arm fired at 4.5× its bar.** The largest
  single-submission jump of the campaign (E008's +0.08 matched).
  Within-round near-duplicates are REAL and abundant; the evidence
  layer's λ calibration priced them on visible rows and it transferred.
  Rough inversion: at λ≈0.9 mixing and our −0.278 base, +0.09 skill
  (−0.278→−0.164 nats) is consistent with roughly a third to half of
  DEV rows having a usable visible twin — a duplication rate far above
  the "accidental" range, i.e. plausibly structural in the build
  (households / re-contacts sharing a round).
- unicef/wb flat — live readings now: their λ tuned ≈ 0 on real data
  (no duplicate structure there), exactly as the self-calibration
  should behave.
- **The 0.92 mechanism is now essentially identified**: same axis,
  better tuned. Remaining gap 0.05. Known headroom in OUR layer:
  LAMBDA_GRID caps at 0.9 (a near-exact twin wants λ→0.97+), TOP_K=10
  posterior may be blunter than needed, weights are first-pass
  (−log u_j, no m_j iteration). Tightening = E019.

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
| 915640 | 2026-09-06-E018.zip | 2026-09-05 17:15:52.069438 +09:00 | Finished | 0.6266666667 | 0.5200000000 | 0.4900000000 | 0.8700000000 | false |

[Complete score ledger](../SCORES.md) and [sanitized source](../hosted-scores/2026-09-27.json).
All score precision fields are 2. Failed attempts have no scores; never substitute zero.
