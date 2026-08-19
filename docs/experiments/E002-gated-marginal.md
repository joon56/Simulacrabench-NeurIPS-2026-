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
| 08-17 kit | 0.3198 | 0.3267 | 0.2568 | 0.2988 | 0.3005 | **+0.0470** |
| 08-19 kit (schemas v1.1/v1.3, count roles) | 0.3210 | 0.3232 | 0.2909 | 0.4297 | 0.3412 | **+0.0535** |

Parent (E001 marginal) on 08-19 kit: 0.3210/0.1623/0.2387/0.4287, mean 0.2877.
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

**Caveat added 2026-08-19 (unhcr v1.3):** real unhcr gates are approximate
(gate-vs-data agreement median 0.83, min 0.29, per the schema description).
This model's hard coupling is exact-gate-optimal and sandbox-safe, but on
real unhcr data a gate-violating cell costs log(1e-3). Successor experiment
must soften the coupling toward observed sentinel rates before this
mechanism is trusted on unhcr. Sandbox cannot measure this (generator
enforces gates exactly).
