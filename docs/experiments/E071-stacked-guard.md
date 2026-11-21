# E071 — Per-head expert weights and temperature inside the internal guard
parent: E070
status: parked
date: 2026-11-10

## Registration (before any E071 run)

Day 3 (IDs 1046001/1046003/1046004): E041 control, E070dev1 and the E067h50c replicate all
read .4763960013 / .3499339289 / .2335276584 / .8457264165. Nine hosted uploads over three
days produced no readable change; a single global expert weight is likely too blunt.

Changes relative to E070 (same split, shadow, E check):
- `stack` / `stackc`: per PREDICT head, choose the expert weight from {0, .25, .5, .75, 1}
  (plain or uncertainty-scaled mixing) by floored log score on S, using the shadow base and
  the F-fitted expert; apply the per-head weights to the final output after acceptance.
- `tempNN`: power calibration of the base distribution, p^(100/NN), renormalized.
- Up to the two best chains on S (above the S reference) are E-tested in order; the first
  with a positive one-sided lower bound is applied. Stack S scores are optimistic by
  construction (selected on S); the E test is the arbiter.

Builds (tmp/e071/, kit aa03186): dev (SEEDS 0; WB mix50/stack/stackc/sent/temp90/temp110;
UNICEF mix25/stack/temp90/temp110; UNHCR regate+transfer/temp90/temp110) — main hosted
rehearsal; s2 (SEEDS 0,1; WB/UNICEF stacks; UNHCR plain seed mean) — seed loop on the
platform; H (dev plus UNHCR conf50/stackc) — heavy, may exceed 900 s (a failed upload does
not count). Final builds add more seeds and are validated in phase 2 locally.

Hosted arms versus same-scale E041 values (.3499339289 / .2335276584 / .8457264165):
Favorable = higher on a changed instrument with unchanged others; Unresolved = equal;
Adverse = lower (a lone UNHCR .91 is weak evidence: boundary noise); Technical = Failed.

## Results

(appended after runs)
