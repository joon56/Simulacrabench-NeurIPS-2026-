# E003 — soft (agreement-weighted) gate coupling
parent: E002
status: adopted
date: 2026-08-28

## Hypothesis

On unhcr the schema-stated gates are approximate (agreement median 0.83,
range 0.29–0.98). Mixing E002's hard coupling with the observed sentinel
rate per item, weighted by a beta-binomial-shrunk per-item agreement
estimate from visible rows, should (a) leave sandbox skill unchanged (gates
exact → weight ≈ 1) and (b) avoid log(1e-3) losses on gate-violating real
cells — measurable locally only by simulating violations.

## Domain check

Pre-registered 2026-08-28, before implementation. Background domain: the
schema's own description states real unhcr gates are approximate (agreement
median 0.83, range 0.29–0.98; five multi-select families sentinel-marked in
round 2 only; six gates listed in the missing GATE_CORRECTIONS.md). CATI
practice (A001: round 1 uses the CATI skip marker, round 2 leaves cells
empty) predicts low agreement concentrates in the 59 round-2-only
multi-select items rather than spreading uniformly. Expected locally:
sandbox gates are exact (A002 v3: 0 violations / 2.57M pairs) → ã≈1 → E003
must equal E002 within noise (Δ ≥ −0.002); the violation simulation is the
only local evidence channel and must show a clear soft-over-hard gain.
Verdict after run: see Decision.

## Change

`src/models/soft_gated_marginal.py`: E002 + per-item agreement
ã_i = (k_i + α·m)/(n_i + α), α = 20 fixed (untunable locally — sandbox has
no violations), m = instrument median; prediction = ã_i·hard +
(1−ã_i)·full-marginal. Tests: `tests/test_soft_gating.py` (forced ã=1 ≡
E002 exactly; natural sandbox ã > 0.99; violation sims). Spec followed:
`trip/tasks/T2-E003-soft-gating.md`.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | sample | unicef | world_bank | unhcr | mean | Δ vs parent |
|---|---|---|---|---|---|---|
| clean sandbox | 0.3210 | 0.3232 | 0.2909 | 0.4297 | 0.3412 | **0.0000** (bit-identical) |

Violation simulation (17% of gated child cells flipped in both visible and
hidden rows, seed 1, log score):

| | hard (E002) | soft (E003) | Δ log score |
|---|---|---|---|
| sample, 17% violated | −1.0437 | −1.0369 | +0.0067 (2 gates only) |
| unhcr, 17% violated | −0.9590 | −0.9301 | **+0.0289** (= +0.0229 skill at U 1.2618) |

Same mechanism on stratum tables (E005 context): E004 hard-stratum −0.8880
vs E005 soft-stratum −0.8458 under 17% violations → **+0.0422 log,
+0.0334 skill** — the safety layer matters MORE once parents are predicted
respondent-specifically.

Reproduce: `.venv/Scripts/python -m pytest tests/test_soft_gating.py -s`

## Decision

**Adopted (real-data motivated).** Clean-sandbox condition met exactly
(Δ = 0.0000 ≥ −0.002; ã≈1 locally as pre-registered) and the violation
simulation shows a clear gain that grows under stratum conditioning. The
local harness CANNOT show the real benefit (sandbox gates exact — A002 v3);
adoption rests on the schema's own statement that real unhcr agreement is
0.83 median, 0.29–0.98 range. Domain check verdict: consistent with
pre-registration. Diagnostic queued for after first real submission: the
real ã distribution over the 59 round-2-only multi-select items.
