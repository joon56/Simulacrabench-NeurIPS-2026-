# E054 — E041 gated-item loss probe information gate
parent: E041
status: parked
date: 2026-09-24

## Hypothesis

One UNHCR-only gated-uniform E041 probe can resolve which item group has more
remaining pooled loss, after display rounding and public noise uncertainty.

## Domain check

Registered before analysis, fits or packaging. Historical E025 loss .079 gated
plus .031 ungated is not E041's map. E041 gained displayed UNHCR .03, but its
allocation is unknown. Gated items contain both asked answers and sentinels;
large gated loss does not identify gate decoding as the cause. A011 measures
replay mismatch; E053's ungated proxy stopped without naturally exercising
dormancy or concentrated buckets. No new estimator or fabricated gates here.

## Fixed measurement and algebra

Run unchanged E041; replace only final UNHCR gated-item vectors with full
uniform probabilities. Preserve every other vector, without propagating the
replacement through descendants. Let H be baseline UNHCR skill, P probe skill,
s the gated item fraction and u their mean uniform cell skill using global U.
Let A=s*(1-u). Weighted remaining loss: L_G=A-H+P; L_C=1-A-P.
These sum to1-H. They are losses relative to skill1, not recoverable gain or a
mechanistic sentinel/content decomposition. Public floor implies small strictly
positive group lower loss bounds; include those instead of assuming zero.

Only baseline reported Grand .64 and instrument .52/.49/.92 are available.
Treat these as rounded, noised readings, not exact values. Read schema item
counts/options, DEV counts, official floor and epsilon; never reconstruct
the random privacy draws. Both plausible Grand paths are evaluated: round
the mean of noised instrument scores, or round the mean of individually
rounded noised instrument scores. Grand implementation remains unverified.
Use public Laplace tail bounds with a union bound for six instrument draws
(baseline and probe), familywise alpha=.05. This is a conditional sensitivity
envelope, not an unconditional confidence claim for a best-selected baseline.
Include an explicit best-selection caveat and a conservative30-prior-submission
sensitivity (93 draws including the probe) before recommending a slot.

## Pre-registered decision

Enumerate displayed probe Grand readings and feasible true skill allocations
using the baseline constraints, unchanged controls, score-floor bounds and
loss identities. Report linear-program minima/maxima of L_G,L_C and L_G-L_C.
Information gate passes only if at least one physically feasible reading arm
under BOTH reporting orders yields the SAME priority with the complete
interval for L_G-L_C above+.015 or below-.015, including the93-draw sensitivity.
This corresponds to a meaningful Grand-equivalent loss imbalance>.005, not
a forecast that repairing that amount is possible. Any other reading is
unresolved. Feasible informative tails do not imply they are probable.
No post-result threshold, reporting-order or noise-bound relaxation.

PASS authorizes packaging a measurement with predeclared arm readings,
intended-change arithmetic, unchanged base/controls, exact source/archive
parity, ZIP checker and official all3 checks. STOP produces no module/ZIP.
Actual hosted submission always remains with the user; no automatic upload.

## Result

Pending schema-only resolution analysis. No score forecast.

## Decision

Parked pending information gate. E041 remains incumbent; no final promotion.
