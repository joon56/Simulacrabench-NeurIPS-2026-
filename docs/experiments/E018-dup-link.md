# E018 — full-pool visible-row evidence (within-round duplicates + k-NN)
parent: E014
status: adopted
date: 2026-09-05

## Hypothesis

Extending E014's evidence layer from cross-round-only candidate pools to
ALL visible rows (self excluded) captures two signals the cross-round
design was structurally blind to: (i) within-round near-duplicate rows —
household co-respondents sharing the roster block, CATI re-dials,
double-entered records — whose TRAIN copy is an answer key for a DEV
row; (ii) a stronger k-NN residual (twice the candidate pool, and
same-round neighbours are more comparable than cross-round ones). The
per-item λ replay calibration is unchanged, so no signal ⇒ λ→0 ⇒ inert.

Scope honesty, pre-registered: the 0.92 arithmetic (avg 90% on truth
needs ~71% of DEV rows twinned) says duplicates CANNOT be the leaders'
whole mechanism — this experiment hunts a partial gain (+0.01–0.02
unhcr plausible if a few % of rows are duplicated), not the gap.

## Domain check

Pre-registered 2026-09-05 BEFORE implementation.

- (a) Technical: the one new failure mode vs E014 is SELF-matching in
  the calibration replay (a visible query finding itself at similarity
  = max would inflate every λ toward 1 and poison held-out rows). Self
  must be excluded from the candidate pool by construction and unit-
  tested. Calibration bias direction is otherwise conservative: the net
  is in-sample-confident on visible rows, which UNDERSTATES the
  evidence's value — λ errs low, never high.
- (b) Background: registration databases (ProGres) and CATI operations
  are known sources of duplicate/near-duplicate records (re-dials,
  multiple numbers per household, separately registered co-residents);
  deduplication is a standing UNHCR data-quality topic. Rate unknown —
  exactly what the λ replay measures from the data. Layer now applies
  to ALL instruments (no round column required); unicef/wb get the same
  self-calibrating treatment (expected λ≈0 there — watch point).
- (c) Local evidence plan: (1) clean runner within ±0.002 of E012
  (E014 precedent −0.0002; sandbox has no duplicates, k-NN redundant
  vs the net); (2) within-round duplicate sim — copy a fraction of
  rows inside one round with perturbed answers, roles straddling —
  large scored gain, and specifically LARGER than E014 on the same sim
  (cross-round pools cannot see within-round twins at all);
  (3) self-exclusion unit test. E003-route adoption; the leaderboard
  slot is the real-data experiment.

## Change

`src/models/dup_link.py` (planned): prob_link with the pooling
generalized — signature over ALL GIVEN columns (wave included: same-
round agreement simply adds weight), candidates = all visible rows,
self excluded; no round-column gate. Calibration replay, TOP_K softmax
posterior, λ grid, and the E012 stack all unchanged. Runtime budget:
pool doubles per query (~n_visible candidates); chunked matcher scales
linearly — profile against the ~350 s local working ceiling (E017 v1
lesson).

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

Prior check that motivated the day: the kit provably drops EXCLUDE
items from the delivered frame (`generated_items` — "never generated,
never shown"), closing the answer-key-in-the-file hypothesis for free.

Clean sandbox: 0.4429 / 0.5006 / 0.4549 / 0.5626 — unhcr −0.0003 vs
E012 (within ±0.002), others identical. Runtime guard added during
verification: calibration replay queries capped at 6,000 (λ on 6k
rows/item is plenty), total 250 s local — inside the hosted bracket
E017 established (hosted ≈ 1.94–2.6× local ⇒ worst case ~650 s).

Sims (unhcr sandbox): within-round duplicate sim (30% of round-1 rows
duplicated in-round, 10% answer perturbation, roles straddling) —
layer level: E018 arms 159 items at λ ≥ 0.5 where E014's cross-round
pools arm 40 (the blindness measured); scored full pipeline: **+0.0588
log over E012**. Self-exclusion unit-tested (a query row present in its
own candidate pool is masked; its duplicate, not itself, is the top
match). Tests 3/3 new.

Reproduce: `PYTHONPATH=. .venv/Scripts/python src/eval/runner.py src/models/dup_link.py`
and `.venv/Scripts/python -m pytest tests/test_dup_link.py -q -s`

## Decision

**Adopted (real-data motivated, E003 route; organizer-ruled legal).**
Clean no-regression + within-round sim gain + self-exclusion
correctness + conservative-bias λ calibration. Leaderboard readings
pre-registered in SCORES.md: unhcr (or any instrument) up ⇒ real
duplicates/k-NN residual exist at that rate; all flat ⇒ the duplicate
axis is dead too and the evidence-layer family (E013/E014/E018) closes
whole. Submission: `submissions/2026-09-06-E018/`.
