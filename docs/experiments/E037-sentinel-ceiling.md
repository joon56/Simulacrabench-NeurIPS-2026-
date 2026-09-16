# E037 — H1 ceiling: sentinel-mass recalibration in the predicted-parent regime
parent: E028
status: rejected
date: 2026-09-18

## Hypothesis

E032/E033 left open whether E025's sentinel ("never asked") mass is
miscalibrated when the parent itself is predicted (all PREDICT cells
blank for a held-out row). H1 would fit a per-item calibrator of the
sentinel probability on a held-out-style replay of visible rows. Before
building it: the CEILING — recalibrate the sentinel mass per item with
the held-out TRUTH itself (isotonic, cross-fitted 2-fold by row so the
map is not evaluated on the rows it was fit on). No replay-based
calibrator can beat a truth-fitted one.

## Domain check

Pre-registered 2026-09-18 BEFORE the cross-fitted run (the in-sample
run had already shown +0.0124 on the CLEAN sandbox, which exceeds the
A005 GIVEN-only bound of ≈ +0.0035 log — so the in-sample number is
isotonic optimism, not signal). (a) technical: the model's sentinel
mass is a·hard + (1−a)·soft with a replay-shrunk agreement; if it is
calibrated, an isotonic map is the identity plus noise and cross-fitted
gain ≤ 0. (b) background: the E028 overlap sims are the only local
regime where the sentinel is genuinely mispredicted (No/DK respondents
answering the Yes branch); E028's structural model gained +0.0121 there
and read flat on the leaderboard. (c) readings: cross-fitted gain on
the clean sandbox ≈ 0 and on the light overlap ≤ +0.003 ⇒ H1 dead;
heavy overlap > +0.005 ⇒ only worth it if the real overlap were heavy,
which E028 already showed it is not.

## Change

None in `src/models`. `tests/test_sentinel_ceiling.py`
(`recalibrate_sentinel`, strict-xfail gain test).

## Result (unhcr, log score, phase 1)

| sim | E025 | in-sample isotonic | cross-fitted isotonic |
|---|---|---|---|
| clean sandbox | −0.5515 | +0.0124 | **−0.0150** |
| overlap light (30% of round-2 No) | −0.5669 | +0.0133 | **−0.0143** |
| overlap heavy (70% No+DK, both waves) | −0.6221 | +0.0243 | **−0.0035** |

## Decision

**Rejected at the ceiling.** Even with the truth, a per-item
recalibration of the sentinel mass loses out of sample on every sim;
E025's sentinel mass is already as calibrated as ~1.4k rows per item
allow. The in-sample/out-of-sample gap (≈ 0.027) is the optimism of a
free monotone fit, a reminder that "calibration" gains must be
cross-fitted before they count. With E037 the last map-supported
phase-1 hypothesis is closed; phase-1 modelling stops unless the
organizers ship the pending gating changes (re-run the harness then).
