# E025 — composition: E022 layer ∘ E017 capacity grid
parent: E022
status: adopted
date: 2026-09-08

## Hypothesis

E017's per-instrument architecture selection ({64×2, 128×2+dropout})
read unhcr +0.01 on the leaderboard and was filed as "flat" under the
±0.01 band; E022's sim-predicted +0.01 has since shown that a +0.01
unhcr reading is what a real +0.009 skill gain looks like. Stacking the
two independent gains (a better base on all rows; better evidence
mixing on matched rows) should add: unhcr 0.88 → ~0.89, Grand rounding
to 0.64.

## Domain check

Pre-registered 2026-09-08 BEFORE the run. (a) the two changes touch
disjoint stages (net architecture vs evidence layer); the λ replay
recalibrates against whatever base the net provides, so composition
cannot double-count. (b) unchanged from E015/E017 (sectioned
multi-factor instruments favor width) and E021/E022. (c) the sandbox
is provably blind to capacity (E009/E011/E015) — local check is parity
of the layer's behavior (household sim within noise of E022) and
runtime (config selection adds one training per instrument; ~220 s
local expected — above the comfort ceiling, mitigated by hosted GPU
training with CPU fallback; a timeout ⇒ pin per-instrument configs).
Leaderboard readings: unhcr ≥ 0.89 ⇒ both gains real, keep stacking
leaderboard-backed refinements; 0.88 ⇒ E017's +0.01 was noise, drop
the capacity axis for good; ≤ 0.87 ⇒ interaction harm, revert to E022.

## Change

`src/models/hh_cap.py`: link_sharp.predict gains a `configs` hook;
E025 = hh_sharp layer + CONFIGS.

## Result

Clean sandbox: 0.4436 / 0.5006 / 0.4548 / 0.5629 — the evidence layer's
behavior is unchanged from E022 (unicef/wb identical, unhcr +0.0002 from
the 128×2 pick); capacity itself is not locally measurable. Runtime
297–331 s local on CPU (two trainings per instrument + the wider final
net); the hosted H100 path is expected to absorb the training share.
Parity of the assembled submission exact; zip OK; score.py PASS
0.50/0.45/0.56.

## Decision

**Adopted as a leaderboard-backed composition** (E017's unhcr +0.01
re-read under the standard E022 validated). Timeout fallback
pre-registered in SCORES.md. Submission: `submissions/2026-09-09-E025/`.
