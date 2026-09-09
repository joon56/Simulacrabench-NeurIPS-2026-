# E026 — E022 layer ∘ full E017 capacity grid (4 configs)
parent: E025
status: parked
date: 2026-09-09

## Hypothesis

E025 (2-config grid) read unhcr +0.01 and confirmed the hosted GPU
training path. Restoring E017's full grid — adding {256×2+dropout,
128×3+dropout} to the per-instrument selection — lets the data pick a
larger trunk where it pays; E017's own 4-grid run picked 128×2 on the
SANDBOX, but the sandbox is provably blind to capacity, so the real
selection may differ. Expected unhcr +0.00 to +0.01 (0 if 128×2 stays
the real winner); Grand crosses to 0.64 at unhcr 0.90.

## Domain check

Pre-registered 2026-09-09 BEFORE the run. (a) selection over 4 configs
on the outer holdout CE is mild pressure (E015/E017 precedent; unicef
kept the small config there — the control); the λ replay recalibrates
on whatever base wins. (b) as E015/E025: sectioned multi-factor
instruments favor width/depth; real > sandbox coupling is the
campaign's most replicated pattern. (c) local: layer parity only
(sandbox blind to capacity); runtime — CPU-side unchanged (~130 s
local), training ×4 absorbed by the H100 (E025 ran at ~300 s local-CPU
equivalent without timeout); CPU fallback would be ~450 s local and
would time out on a bad day — accepted risk, timeout fallback = E025.
Readings: unhcr 0.90 ⇒ a wider/deeper config won somewhere real —
keep the grid, consider width 512 next; 0.89 ⇒ 128×2 is the real
optimum, capacity axis complete; ≤ 0.88 ⇒ selection instability,
pin E025's configs.

## Change

`src/models/hh_cap4.py`: E025 with CONFIGS = E017's four.

## Result

Clean sandbox identical to E025 (0.4435 / 0.5006 / 0.4548 / 0.5629 —
the sandbox selects 128×2 again). ~430 s local CPU (4 trainings per
instrument); hosted H100 absorbs training. Parity exact; zip OK;
score.py PASS 0.50/0.45/0.56.

## Decision

**Adopted as a leaderboard-backed composition** (capacity axis
re-opened by E025). Submission `submissions/2026-09-10-E026/`;
readings in SCORES.md.
