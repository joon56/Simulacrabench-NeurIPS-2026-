# 2026-08-29-E006 — hierarchical backoff ladder (MRP-lite) + soft gating

Experiment: E006 (adopted; parent E005). Code: exact copy of
`src/models/hier_backoff.py` (self-contained). Zip:
`submissions/2026-08-29-E006.zip`, check_submission_zip OK.

## Local scores (2026-08-29, seed 0, phase 1)

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact (runner) | 0.4385 | 0.4772 | 0.4196 | 0.5382 | 0.4783 |
| E005 (LB 0.53) | 0.4333 | 0.4593 | 0.4105 | 0.5347 | 0.4682 |

Official score.py PASS ×3: 0.4800 / 0.4200 / 0.5400. Wall-clock ~95 s
total. Tests 23/23 (suite) — 4 new for the ladder.

## Leaderboard expectation (real data)

Reference: E005 LB = 0.53 (0.49 / 0.48 / 0.63). Pre-registered:

- Modest across-the-board gain expected (sandbox Δ +0.010); noise floor is
  ±0.01–0.02, so a flat result would NOT falsify the ladder — two flat
  results would.
- unicef expected to gain most (sandbox +0.018: religion/Country ladder
  depth pays); unhcr smallest headroom locally (+0.004).
- Real-data ladder should include country_asylum and/or wave on unhcr
  (A001/A002 domain prediction); a LARGE unhcr move either way would
  suggest the greedy pick changed — diagnose before building deeper.
- Risk: greedy selection on 20% holdout may overfit instrument-specific
  quirks; if any instrument drops > 0.02, revisit EVAL_CAP and selection
  stability (different seeds) before next submission.
