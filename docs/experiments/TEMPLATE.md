# E0XX — short-slug
parent: E0YY            <!-- tree edge: the experiment this branches from; "—" for roots -->
status: parked          <!-- adopted / rejected / parked / superseded-by:E0ZZ -->
date: 2026-MM-DD

## Hypothesis

One falsifiable sentence: what should improve, where, and why.

## Domain check

Pre-registered BEFORE running: what background domain knowledge (docs/domain.md,
published survey reports — not methods literature) predicts about this result,
one sentence with source. Filled in AFTER: consistent / surprising. Surprising
raises the evidence bar, never auto-rejects: rule out artifacts (leakage, coding
error, confound), replicate on a different seed/split/slice; if it survives,
adopt AND record as a potential genuine discovery.

## Change

What was built/modified (file paths). Small enough to attribute the delta to.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | sample | unicef | world_bank | unhcr | mean | Δ vs parent |
|---|---|---|---|---|---|---|
| this | | | | | | |

Reproduce: `.venv/Scripts/python src/eval/runner.py <model path>`
Raw runner output: `results/E0XX.json` (if saved)

## Decision

Adopt iff Δ(3-instrument mean, sample excluded) > +0.005 (~3σ of phase-sampling
noise, measured 2026-08-12). State the number, the verdict, and anything the
per-instrument breakdown says about *why*.
