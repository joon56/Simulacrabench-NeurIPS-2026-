# E036 — λ per twin relation (same-round vs cross-round top candidate)
parent: E025
status: parked
date: 2026-09-17

## Hypothesis

On unhcr a held-out row's best candidate is either the same household
in the OTHER CATI round (panel recurrence) or a co-respondent in the
SAME round. The two relations disagree for different reasons — panel
drift on volatile items vs person-level differences on personal items —
so E022's one λ per (item, concentration bucket) pools two agreement
rates. Calibrating λ per (item, bucket, relation) in the same replay
(bucket = conc + 2·cross; fallback to the pooled bucket below 30 rows)
should lift unhcr where the two relations differ, and is exact
no-regression elsewhere (no round column ⇒ E025; one-round twins ⇒
cross buckets fall back ⇒ E025).

## Domain check

Pre-registered 2026-09-17 BEFORE the runs. (a) technical: the change
is a finer partition of an already replay-calibrated weight; harm is
bounded by the ≥ 30-row fallback and by the λ grid argmax being
per-bucket; the local sandbox cannot show the gain (no cross-round
twins) — only a panel sim with different copy rates per relation can.
(b) background: ERPIS re-contacts the same households across rounds;
intention and needs items are known to move between rounds while
household-composition facts do not, whereas a co-respondent (spouse,
adult child) shares facts but not personal items — the relation is
plausibly the strongest single predictor of per-item agreement. (c)
readings: clean sandbox identical to E025 (3 instruments); same-round
household sim identical; panel sim (cross twins ρ ∈ [0.7, 0.95] vs
same-round ρ ∈ [0.2, 0.5]) > +0.003 log ⇒ package as a real-data A/B.
Leaderboard: unhcr ≥ 0.90 (Grand 0.64, best updates, per-instrument
visible) ⇒ relation-specific agreement is real and worth ≥ +0.01;
Grand 0.63 no update ⇒ pooled λ already adequate, park.

## Change

`src/models/wave_lam.py` (`wave_lam_layer`, `predict`);
`link_sharp.predict` consumes integer buckets (`pair[int(conc)]`, bool
callers unchanged). `tests/test_wave_lam.py`: `panel_inject` sim
(twins split across rounds with relation-specific copy rates),
same-round parity test, panel gain test.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | unicef | world_bank | unhcr | mean | Δ vs E025 |
|---|---|---|---|---|---|
| E025 | 0.5006 | 0.4548 | 0.5629 | 0.5061 | — |
| E036 | 0.5006 | 0.4548 | 0.5629 | 0.5061 | 0 (identical) |

Household sims (unhcr log score): same-round twins only −0.5688 →
**+0.0010** (random cross-round k-NN candidates fill the cross buckets
even without cross-round twins; harmless); **panel sim** (`panel_inject`,
frac 0.4, half the twins in wave 2 with ρ ∈ [0.7, 0.95] vs same-round
ρ ∈ [0.2, 0.5]) −0.5556 → **+0.0105**. Runtime ≈ E025 (288 s local, 3
instruments, CPU training). Tests 2/2.

## Decision

**Adopted (E003 route)** — exact no-regression on the clean sandbox,
+0.0010 on the same-round sim, +0.0105 on the schema-anchored panel sim
(above the +0.005 threshold). Real-data A/B: `submissions/2026-09-17-E036/`.
Readings pre-registered in its SCORES.md: Grand 0.64 ⇒ relation-specific
agreement real; 0.63 ⇒ pooled λ adequate, park; ≤ 0.62 ⇒ thin buckets,
revert.

**LB 2026-09-17: Grand 0.63, no update ⇒ PARKED.** Pooled λ is adequate
on real unhcr; the relation-specific agreement the panel sim assumed
is not there at a readable size (≥ +0.01 unhcr). Second sim-only gain
(after E028) that did not transfer: sims that inject an assumed real-data
structure are directional channels, not evidence — a real-data A/B is
the only test, and it costs a slot.
