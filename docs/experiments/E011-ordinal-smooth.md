# E011 — ordinal kernel smoothing along the option axis
parent: E010
status: rejected
date: 2026-09-02

## Hypothesis

Applying a per-item discrete Gaussian kernel over the RANKS of
numeric-parsing options to the blended distributions (full-table and
asked-only conditional), with bandwidth h selected per item on the
internal holdout from {off, 0.5, 1.0, 2.0}, improves real skill —
mostly world_bank (24 ordinal PREDICT items: spans K=15, counts K=12–13,
numeric scales) — because every current component pools across cells or
respondents but nothing pools across ADJACENT OPTIONS, and real span,
count, and scale answers are unimodal/decaying (Woods 2011 digit-span
norms, Kessels 2000 Corsi, count data generally; A001/A004) so thin
conditional cells misallocate mass among neighbours that a kernel can
repair.

## Domain check

Pre-registered 2026-09-02 BEFORE implementation.

- (a) Technical: kernel smoothing over ordered categories = standard
  small-sample ordinal density estimation; the per-item off-option and
  holdout selection make the model degenerate to E010 exactly when no
  ordinal structure exists. Detection is STRICT float-parse of option
  labels (≥ K−1 numeric, K ≥ 4): coded labels ('98. I don't know') fail
  the parse, so non-response codes can never be smoothed toward
  substantive values; K=24/25 sector items are nominal and excluded.
  Worded Likert labels are deliberately left out in v1.
- (b) Background: wb is a STEP-shaped battery (A001) — spans and counts
  dominate its high-K items; their real distributions are unimodal or
  decaying, exactly the structure a rank kernel encodes. unhcr roster
  counts and any numeric unhcr/unicef items ride along for free.
- (c) Local evidence plan (A004: the sandbox couples trait to options
  with RANDOM per-option loadings — no order structure BY CONSTRUCTION;
  E010 adoption route): (1) clean runner must equal E010 within ±0.002
  — holdout selection should pick h=off almost everywhere (watch
  point: report how many items engage on pure noise); (2) synthetic
  ordinal sim — regenerate the numeric items of a sandbox frame from a
  discretized Gaussian whose mean depends on a GIVEN column — must show
  a clear E011-over-E010 gain; (3) the clean run doubles as the no-loss
  bound. Adoption is real-data motivated on (1)+(2), as E003/E010.

## Change

`src/models/ordinal_smooth.py` (planned): E010 predict + kernel layer.
Per PREDICT item whose options strict-parse numeric: kernel matrix
M_h[i,j] ∝ exp(−(rank_i − rank_j)² / (2h²)) over the numeric options
(sorted by parsed value; non-numeric options and the gate sentinel stay
identity — mass moves only within the numeric block). h per item by
held-out log score of M_h·(blended dist), grid {off, 0.5, 1.0, 2.0},
using the instrument-level w from E008/E010 tuning. Applied to both the
full-table and conditional blended vectors before gate math (separate
kernels — different option lists).

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

Clean sandbox: identical to E010 to 4 decimals on all four schemas —
evidence (1) met; the off-by-default guard works (a handful of items
engage on noise with mean prediction deviation < 5e-3).

Ordinal sims (the pre-registered positive-evidence channel) — attempt
log, append-only:

- **sim v1** (mean additive in ONE GIVEN column, σ=1.5 ranks, wb):
  Δ +0.0003 log. Diagnosis: the driver column is in the ladder AND the
  logistic, cells are fat (~1,000 rows), the planted structure is fully
  captured by existing conditioning — the sim never exercised the
  thin-cell regime the kernel exists for.
- **sim v2** (mean = non-additive (3·i1+i2) mod 7 over TWO GIVEN
  columns → only deep/thin cells (~150 rows, K≤15) see the signal;
  7 items engaged): **Δ +0.0000 log.** Even in a deliberately favorable
  thin-cell construction, κ-backoff toward parents plus the logistic
  absorbs enough that option-axis pooling has nothing left to repair at
  n ≈ 5k rows.

## Decision

**Rejected.** The pre-registered evidence standard (clear sim gain) is
not met after two sim designs, the second built specifically to favor
the mechanism. Honest conclusion, mirroring E007: option-axis pooling
headroom is ≈ 0 at phase-1 data volumes — the cell-axis pooling (κ
ladder) and respondent-axis pooling (logistic) already exhaust it.
Forcing a more extreme sim (20-row cells, K=25) could manufacture a
gain but would say nothing about wb's actual regime. Domain check
verdict: the (b) unimodality claim stands, but the (a) thin-cell
premise fails quantitatively — wb cells are not thin enough. Code kept;
revive only if phase 2 or a diagnostic shows genuinely thin scored
regimes (e.g. asked-only conditionals under 100 rows).
