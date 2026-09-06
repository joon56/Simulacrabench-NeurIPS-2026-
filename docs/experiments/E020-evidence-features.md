# E020 — twin evidence as network INPUT (learned combination)
parent: E018
status: rejected
date: 2026-09-07

## Hypothesis

E018 mixes twin evidence into the belief with a per-item scalar λ —
"copy the twin's answer with probability λ, else trust the model".
E019's flat leaderboard says real twins are NOISY (a copy model is
wrong often), so the scalar mixture leaves signal on the table:
(i) a twin's answer that is wrong is usually NEAR the truth (ordinal
neighbours, adjacent categories) — the mixture cannot spread mass
around the twin's answer; (ii) a twin's answer to item A carries
information about the respondent's item B (cross-item) — the mixture
only uses A for A. Feeding the posterior-weighted evidence vectors of
ALL items as extra INPUTS to the shared-trunk net (alongside the GIVEN
one-hots), trained on visible rows whose evidence is built with self
excluded, lets the network LEARN the combination per item and across
items. Replay-consistent by construction: training inputs are built
exactly as test inputs.

## Domain check

Pre-registered 2026-09-07 BEFORE implementation.

- (a) Technical: evidence input width ≈ Σ_items K_i (unhcr ~1,300 dims)
  on ~8k rows — overfitting risk handled by the existing early stopping
  + weight decay and by keeping the ladder blend w as the outer guard.
  Rows with no evidence (no visible pool) get zero vectors — the net
  learns that regime too. The E018 λ-mixture is dropped (the net
  subsumes it); everything downstream (ladder blend, gates,
  conditional agreement) unchanged.
- (b) Background: household co-respondents and re-contacts agree on
  facts (roster, documents, housing) and correlate but differ on
  attitudes/intentions — exactly "near, not equal" and cross-item
  structure; a learned map is the natural estimator, a copy mixture is
  not.
- (c) Local evidence plan — instrument first: (0) re-calibrate the dup
  sim with 40% answer perturbation (E019's flat means the 10% sim was
  too clean); sanity: E019 ≈ E018 on the noisy sim (reproduce the real
  flat). Then (1) noisy-sim scored: E020 > E018 by > +0.005 log;
  (2) clean runner within ±0.002 of E012/E018 (no twins ⇒ evidence
  inputs are k-NN summaries the net can ignore or use); (3) runtime
  ≤ ~130 s local (post perf-pass ceiling).

## Change

`src/models/ev_net.py` (planned): evidence vectors for ALL rows (visible
with self exclusion, held-out vs visible pool) computed BEFORE training;
`_given_matrix` output concatenated with the evidence block; net
trained/evaluated/retrained as in E012 on the widened input; predict
uses the net's probabilities as before, no λ layer. Perf-pass code
(vectorized matcher/evidence, GPU training) assumed.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

Instrument step (0) FAILED first: on the 40%-perturbed dup sim E019
still beats E018 by +0.0187 log — the real leaderboard was flat, so
answer-noise on copied rows is NOT what real twins look like. Then
E020 on the same sim: **−0.0211 log vs E018** — when the generating
process is copy+noise, the scalar mixture is the right estimator and
a 1,300-dim evidence input on 8k rows is a worse one.

## Decision

**Rejected on sim; the sim itself is re-diagnosed.** Reinterpretation
of the E018/E019/E020 trio: real matches are HOUSEHOLD CO-RESPONDENTS,
not copies — roster GIVEN columns (child counts, governorate, origin,
country) match exactly, individual columns (age, education, marital,
relationship) differ, and answers correlate per item (facts high,
attitudes low) rather than copy. That explains E018's gain, E019's
flat (no exact-twin regime exists), and E020's failure (no copy
structure to learn from either). Next: a household sim with exactly
that structure, and E021 = data-estimated column weights (Fellegi–
Sunter m_j iteration) so household matching stops penalizing the
individual columns that legitimately differ.
