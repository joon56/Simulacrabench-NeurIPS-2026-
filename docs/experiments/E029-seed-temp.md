# E029 — net seed ensemble + per-instrument output temperature
parent: E025
status: parked
date: 2026-09-12

## Hypothesis

The shared-trunk net (E012/E025) is one early-stopped full-batch run
per instrument; the blend weight w is its only calibration knob. Two
holdout-decided refinements should each add a small, real amount of
skill on every instrument: (1) averaging N_SEEDS = 3 members trained
from different torch seeds removes the seed-specific part of the net's
error (the E010 seed probe measured selection stability, not net
variance); (2) an output temperature T on the member logits, tuned
jointly with w on the outer holdout, corrects the sharpness the inner
early-stop left behind. Both are exact no-ops at (1 seed, T = 1).

## Domain check

Pre-registered 2026-09-12 BEFORE the run. (a) technical: seed
averaging of small nets is a variance reduction with no bias term —
the gain is bounded by the disagreement between members; on the clean
sandbox (trait_scale 2.0, GIVEN → PREDICT dependence real) the runner
CAN see it, unlike the capacity axis, because the sandbox does have
between-seed variance. Temperature is a one-parameter recalibration;
with the holdout already picking w, its marginal gain is expected small
(≤ +0.002) and possibly zero (T = 1 chosen). (b) background: nothing in
the instruments bears on this — pure estimation. (c) local readings:
seeds-only Δ ≥ +0.002 on the 3-inst mean ⇒ real net variance; temp-only
picks T ≠ 1 on at least one instrument ⇒ early stop leaves miscalibration;
composed Δ > +0.005 ⇒ adopt on the runner (standard route, no sim
needed); +0.002–0.005 ⇒ stack into the next submission with another
sim-verified refinement (leaderboard resolves only ≥ +0.02 unhcr);
≤ +0.001 ⇒ park, the net stage is variance-saturated.

## Change

`src/models/seed_temp.py`: drop-in `tune_and_train` (architecture
selection unchanged; extra members trained for the winner; (T, w) chosen
on T_GRID × W_GRID by pooled holdout log score; final members retrained
on all complete rows and wrapped as one module returning log-mean
probabilities). `link_sharp.predict` gained a `tune_fn` hook (default =
the E012 function, bit-identical). Ablations: `predict_seeds_only`,
`predict_temp_only`, `predict` (both).

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

Parity: (1 seed, T_GRID=(1.0,)) reproduces E025 on unicef to 1e-10.

| | unicef | world_bank | unhcr | mean | Δ vs E025 |
|---|---|---|---|---|---|
| E025 | 0.5006 | 0.4548 | 0.5629 | 0.5061 | — |
| seeds only (N=3, T=1) | 0.5009 | 0.4551 | 0.5634 | 0.5065 | **+0.0004** |
| temp only (N=1, T grid) | 0.5006 | 0.4548 | 0.5629 | 0.5061 | ±0.0000 |
| both | 0.5009 | 0.4551 | 0.5634 | 0.5065 | **+0.0004** |

Selected (T, w) per instrument, printed from `tune_and_train`: T = 1.0
everywhere (N = 1 and N = 3); w = 1.0 on unicef/wb, 0.9 → 1.0 on unhcr
with the ensemble. Runtime: seeds-only 479 s, both 528 s local CPU
(7 trainings per instrument vs 3; E025 241 s) — hosted GPU absorbs it,
but locally it doubles the run.

Domain check verdict: consistent with the pre-registration's pessimistic
arm. The early-stopped full-batch net is already calibrated on the
holdout (CE early stop ⇒ T = 1 is the argmax), and between-seed
disagreement is small enough that averaging three members moves the
pooled log score by +0.0004 skill — the same order as the E010 seed
probe's selection spread (0.0003).

Reproduce: `.venv/Scripts/python src/eval/runner.py` on
`src.models.seed_temp.{predict_seeds_only,predict_temp_only,predict}`.

## Decision

**Parked.** Δ(3-inst mean) = +0.0004 for the composed model, T = 1
selected on all instruments — far below the +0.005 threshold and below
the +0.002 "stack it" bar pre-registered above. The net stage is
variance-saturated locally; the temperature knob is redundant with CE
early stopping + the w guard. Not worth doubling local runtime or
spending a leaderboard slot alone. Revival condition: a phase-2
stack where another refinement clears the threshold and hosted GPU
time is free — the ensemble is a pure no-risk add-on (self-tuning,
exact no-regression) that can ride along; on its own it stays parked.

