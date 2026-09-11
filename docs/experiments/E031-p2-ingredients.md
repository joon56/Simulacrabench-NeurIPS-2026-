# E031 — phase-2 ingredients read on real data (replay cap lift + E029 ensemble)
parent: E025
status: rejected
date: 2026-09-13

## Hypothesis

Two phase-2 ingredients that the local instruments measure at ≈ 0 may
still be non-zero on real data, where GIVEN coupling is 3–5× the
sandbox's and the household structure is real rather than injected:
(1) lifting the calibration replay cap (CAL_QUERIES 6000 → all visible
rows: unhcr 8,279 in phase 1, 8,900 in phase 2) reduces λ estimation
noise per (item, concentration bucket); (2) E029's 3-seed ensemble
removes real between-seed net variance. Submitted as one pre-registered
A/B because the leaderboard resolves only ≥ +0.02 unhcr and both are
exact no-regressions locally.

## Domain check

Pre-registered 2026-09-13 BEFORE submission. (a) technical: both are
variance reductions with no bias term, self-tuning (λ and T/w are
chosen on visible rows at run time); the only real-data risk is
runtime (7 trainings per instrument, +38% replay queries on unhcr).
(b) background: nothing in the instruments bears on it. (c) local:
clean sandbox = E029's +0.0004; household sim cap lift +0.0000 (phase
1) / +0.0005 (phase 2, new `hh_inject_rho_p2` sim with twins in
TRAIN/DEV/TEST). Readings: unhcr 0.90+ ⇒ real variance larger than the
sims', seed count becomes a phase-2 knob; 0.89 ⇒ flat, both stay as
no-risk phase-2 defaults; ≤ 0.88 / timeout ⇒ budget, revert for phase 1.

## Change

`submissions/2026-09-13-E031/main.py`: E025 assembly + `CAL_QUERIES =
10**9` + the `seed_temp` block (`_Ensemble`, `_train_seed`,
`_member_probas`, `tune_and_train_ens`) + `tune_fn` hook; entry point
passes `tune_fn=tune_and_train_ens`. `tests/test_phase2.py`: phase-2
household sim helper and the recorded cap-lift null.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | unicef | world_bank | unhcr | mean | Δ vs E025 |
|---|---|---|---|---|---|
| E025 | 0.5006 | 0.4548 | 0.5629 | 0.5061 | — |
| E031 (assembled) | 0.5009 | 0.4551 | 0.5634 | 0.5065 | +0.0004 |

Household sim, unhcr log score, E025 with the cap at 6000 vs lifted:
phase 1 (9,271 visible) −0.5627 / −0.5627; phase 2 (9,965 visible)
−0.5541 / −0.5536 (**+0.0005**). Runtime unchanged by the cap (299 →
295 s, 338 → 332 s — the replay is not the dominant cost). Assembled
file parity vs src exact; zip OK; official score.py PASS ×3 (see
SCORES.md). Local runtime 711 s CPU under 3-way contention (528 s alone).

## Decision

**Rejected (flat).** E031 (both ingredients) failed on the hosted worker
with no HSCC code (memory ruled out locally: 1.82 vs 2.40 GB peak);
E031b (cap lift only, submitted the same day — failed submissions do
not consume the slot) read **Grand 0.63, no update (unhcr ≤ 0.89)**:
the replay cap lift is null on real data, as on both sims. The seed
ensemble is unread on real data; given its +0.0004 local ceiling and
the unexplained E031 failure, it is not resubmitted in phase 1 — it
stays a no-risk default for phase 2 only if the 3600 s run proves clean
locally. Phase-1 model of record stays E025. With E029–E031 this closes
the parameter/variance axis of the E025 stack on real data too; the
next slots go to probe submissions that map where unhcr's remaining
loss sits.
