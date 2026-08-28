# Submission protocol and score log

Submissions are ammunition: 1/day in phase 1 (the 20-total cap was removed
2026-08-18; the noised leaderboard still can't rank close variants —
CLAUDE.md discipline rule 4). Every leaderboard submission follows this
protocol:

1. **Before submitting** — the candidate must PASS `score.py` locally on all
   three real schemas, beat the current best on the local harness, and have
   its wall-clock measured. Snapshot the exact code into
   `submissions/YYYY-MM-DD-<name>/` (copy of main.py + requirements.txt +
   the local scores).
2. **Record the expectation** — add a row to the log below with the local
   skill numbers BEFORE the leaderboard result comes back.
3. **After the result** — fill in the reported (noised) score and note the
   local-vs-leaderboard gap. A drift in that gap is itself information
   (phase-1 noise is Laplace ε=10, rounded to 0.01 — expect ±0.01–0.02).

## Log

| # | Date | Snapshot | Local skill (sample/unicef/wb/unhcr) | Expected LB | Reported LB | Notes |
|---|------|----------|--------------------------------------|-------------|-------------|-------|
| 2 | 2026-08-28 | 2026-08-28-E005 | 0.4333 / 0.4593 / 0.4105 / 0.5347 | all three > E002's LB (0.45/0.43/0.41); unhcr largest gain expected (cascade + low U); drop below 0.41 on unhcr ⇒ softening insufficient | | E005 soft-stratum (E003+E004); zip OK, score.py PASS ×3, ~101 s; 19 tests |
| 1 | 2026-08-27 | 2026-08-27-E002 | 0.3210 / 0.3232 / 0.2909 / 0.4297 | n/a — first real-data measurement (sandbox skills don't transfer; qualitative expectations in SCORES.md) | **0.43** (unicef 0.45 / wb 0.43 / unhcr 0.41) | E002 gated marginal; pipeline validated end-to-end. unhcr 0.41 = real-data marginal (E002 ≡ marginal there) → largest headroom. Real marginals far sharper than sandbox; noise ±0.01–0.02. |
