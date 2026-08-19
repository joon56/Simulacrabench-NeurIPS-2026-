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
| — | — | — | — | — | — | none submitted yet; launch 2026-08-17 |
