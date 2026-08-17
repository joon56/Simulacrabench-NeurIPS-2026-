# E002 — gate-aware marginal
parent: E001
status: adopted
date: 2026-08-17

## Hypothesis

Skip logic is deterministic: per respondent,
P(child = NA_GATED) = 1 − P(parent ∈ observed_if), with the respondent's own
parent belief (one-hot when visible). Enforcing this coupling should beat the
pooled marginal wherever gate parents are visible for held-out rows.

## Change

`src/models/gated_marginal.py` (built 2026-08-12, re-scored on launch kit):
plain marginal + per-respondent gate coupling, substantive mass =
P(asked) × asked-only conditional, chain closure automatic.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | sample | unicef | world_bank | unhcr | mean | Δ vs parent |
|---|---|---|---|---|---|---|
| gated_marginal | 0.3198 | 0.3267 | 0.2568 | 0.2988 | 0.3005 | **+0.0470** |

Reproduce: `.venv/Scripts/python src/eval/runner.py src/models/gated_marginal.py`

## Decision

Adopt: +0.047 ≫ +0.005 threshold. Per-instrument breakdown is the structural
finding: unicef +0.178 (5/7 gates on GIVEN parents → deterministic), wb +0.010
(6/19), sample/unhcr ±0.000 (gates on PREDICT parents → parent belief falls
back to the crowd marginal → algebraically identical to E001). Gate coupling
is a *multiplier on parent predictability*: unhcr's 143 gates pay only once a
model predicts parents respondent-specifically — that is the branch to grow
next (GIVEN-conditioning / backoff).

First-leaderboard-submission candidate.
