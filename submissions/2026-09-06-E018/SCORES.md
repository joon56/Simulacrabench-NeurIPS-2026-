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
