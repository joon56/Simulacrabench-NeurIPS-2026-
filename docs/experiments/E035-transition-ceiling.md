# E035 — H2 ceiling: evidence transition tables (oracle T on a structured sim)
parent: E034
status: rejected
date: 2026-09-16

## Hypothesis

The evidence layer mixes a candidate's one-hot answer into the belief
at λ. If a co-respondent's or the same household's later answer differs
SYSTEMATICALLY (spouse says "2" where the respondent says "3"; intention
drifts one step between rounds), a per-item transition row T[twin
answer → respondent answer] carries more than the one-hot, and the λ
replay would recalibrate on top. Before any estimator: measure the
ceiling with the TRUE T (from known sim pairs) on a sim where
disagreements are structured, and confirm no harm where they are not.

## Domain check

Pre-registered 2026-09-16 BEFORE the run. (a) technical: in the E022
layer the one-hot evidence already receives a per-item λ; the marginal
value of T is the part of the disagreement mass that a fixed mapping
concentrates. The λ mixture with the model absorbs unstructured
disagreement already, so the ceiling is bounded by how structured real
disagreement is. (b) background: panel drift on intention items is
plausibly directional (return-intention timing slips later), household
co-respondent disagreement on shared-fact items should be near zero.
(c) readings: oracle-T gain on the structured sim (s = 0.7 — a strong
regime) > +0.005 ⇒ build an estimator from provisional pairs (E021
style); ≤ +0.005 ⇒ park without an estimator (E030 lesson).

## Change

None in `src/models`. `tests/test_transition_ceiling.py`: structured
sim (`inject_structured`), oracle T from known pairs
(`true_transition`), E022 layer with ev → ev·T (`layer_with_transition`).

## Result (unhcr household sim, log score, phase 1)

| sim | E025 | oracle-T Δ |
|---|---|---|
| unstructured (s = 0, ρ ∈ [0.2, 0.8]) | −0.5551 | **−0.0013** |
| structured (s = 0.7, same ρ) | −0.5702 | **+0.0032** |

The structure itself costs E025 0.015; the oracle table recovers a
fifth of it. Known pairs: 800 (visible both sides).

## Decision

**Rejected at the ceiling.** +0.0032 with the true transition table
in a strong structured regime, and a small loss where disagreement is
unstructured (Laplace-smoothed T is noisier than the one-hot). An
estimator from provisional pairs would recover less. Together with
A005 (base model at the sandbox Bayes ceiling), E030 (signature recall
ceiling +0.0025) and E023 (λ/K saturation), every axis the local
harness can measure is now closed: further phase-1 gains can only
come from real-data-only hypotheses read as leaderboard A/Bs
(readable when they lift unhcr by ≥ +0.01, which moves the best from
0.63 to 0.64 and reveals per-instrument scores).
