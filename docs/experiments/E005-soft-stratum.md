# E005 — soft gating on stratum-backoff tables (E003 + E004)
parent: E003, E004
status: adopted
date: 2026-08-28

## Hypothesis

Composing E004's stratum backoff with E003's agreement-weighted gating
keeps E004's full sandbox gain (ã≈1 locally) while removing the real-data
risk E004 alone creates: respondent-specific parent beliefs activate the
unhcr gate cascade over gates that are only approximately true (agreement
median 0.83) — hard coupling there converts each violated cell into a
near-floor loss.

## Domain check

Pre-registered via E003/E004 (see those files — this experiment inherits
both). Instrument-specific note: 155/156 unhcr gates sit on PREDICT
parents (A002 finding 2), so E004 is the first model where the softening
can matter at all; expected locally: clean sandbox ≡ E004, violation sim
clearly better than E004.

## Change

`src/models/soft_stratum.py` (composes stratum_backoff + soft_gated_marginal;
gated prediction = ã·hard_stratum + (1−ã)·soft_stratum_marginal).
Submission build: `submissions/2026-08-28-E005/main.py` (self-contained,
verified identical output via runner). Full suite: 19 tests pass.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | sample | unicef | world_bank | unhcr | mean | Δ vs E002 (3-inst) |
|---|---|---|---|---|---|---|
| E002 | 0.3210 | 0.3232 | 0.2909 | 0.4297 | 0.3412 | — |
| E004 | 0.4333 | 0.4593 | 0.4105 | 0.5347 | 0.4595 | +0.1202 |
| this | 0.4333 | 0.4593 | 0.4105 | 0.5347 | 0.4595 | **+0.1202** (≡ E004, ã≈1) |

Violation sim (unhcr, 17% flipped): E004 −0.8880 vs this −0.8458 →
**+0.0422 log / +0.0334 skill** under violations, at zero clean-sandbox
cost. Wall-clock: 0.7 + 3.9 + 13.0 + 83.3 ≈ 101 s total ≪ 900 s.
Official score.py: PASS 0.4600 / 0.4100 / 0.5300 (unicef/wb/unhcr).

Reproduce: `PYTHONPATH=. .venv/Scripts/python src/eval/runner.py src/models/soft_stratum.py`

## Decision

**Adopted.** Δ(3-inst mean, sample excluded) = +0.1202 > +0.005, and the
violation simulation shows the safety layer active exactly where E004
needed it. This is the 2026-08-28 leaderboard submission. Leaderboard
expectations (real data, qualitative): unhcr should gain most if the
stratum rule picks country×wave as A002/A001 predict; the reported triple
tests that pre-registration.
