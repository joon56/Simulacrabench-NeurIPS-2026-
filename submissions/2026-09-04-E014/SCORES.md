# 2026-09-04-E014 — soft posterior cross-round evidence mixing

Experiment: E014 (adopted, E003 route; parent E013 parked). Code:
script-assembled merge incl. prob_link. Rarity-weighted signature
scores → softmax posterior over top-10 other-round candidates →
posterior-mixed candidate answers as evidence → per-item λ calibrated
on visible-row replay. No hard matching, no uniqueness requirement —
collisions share mass; no signal ⇒ λ→0 ⇒ inert. Zip:
`submissions/2026-09-04-E014.zip`, check_submission_zip OK.

## Local scores (2026-09-03, seed 0, phase 1)

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact (runner) | 0.4429 | 0.5006 | 0.4549 | 0.5627 | 0.5061 |
| E012 (LB 0.60) | 0.4429 | 0.5006 | 0.4549 | 0.5629 | 0.5061 |

Sims: heavy-drift panel **+0.1556 log** scored; collision sim keeps
213/213 items armed (E013's failure regime). Official score.py PASS ×3:
0.5000 / 0.4500 / 0.5600. Tests 51 passed + 1 xfail. Parity exact.
Same-day context: E015 (trunk capacity grid) parked at +0.0001.

## Leaderboard expectation (real data)

Reference: E012/E013 LB = 0.60 (0.52 / 0.49 / 0.78). Pre-registered
2026-09-03 BEFORE submission. This submission is a designed experiment
on the round-overlap question — every outcome is informative:

- unicef/wb flat (no round column → untouched). Any move ⇒ bug.
- **unhcr UP (≥ +0.02)** ⇒ rounds overlap; E013 died on signature
  collisions, soft posteriors fixed it. Follow-up: tighten (raise K,
  refine weights) toward the 0.92 ceiling.
- **unhcr flat (±0.01)** ⇒ overlap CONCLUSIVELY dead (soft matching
  with self-calibration finds nothing) ⇒ abandon the linkage line,
  re-open the 0.92 mechanism question (capacity A/B as its own
  pre-registered experiment is next).
- unhcr down > 0.01 ⇒ λ calibration overfit visible rows — not
  expected (8k rows per item, coarse grid); would trigger a λ cap.
- k-NN residual note: λ may arm slightly even without overlap (k-NN
  vs net ≈ 0 on sandbox but real data may differ mildly) — a +0.01
  unhcr move is ambiguous between weak overlap and k-NN; only ≥ +0.02
  counts as overlap evidence.
