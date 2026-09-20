# E043 — Section-specific candidate search
parent: E041
status: parked
date: 2026-09-20

## Hypothesis

Using E041's learned section weights to retrieve candidates, not only rerank
the initial 32, adds useful answer evidence outside the shared shortlist.

## Domain check

Registered before today's oracle or implementation. Technical: freeze E041
metric fitting, section activation, K=32 and replay procedure; vary only the
GIVEN metric used to select donors for active sections. No query answers enter
inference. The metric remains trained on its original shortlist, so expansion
can introduce distribution shift; this is a known risk, not an extra fix.
Background: published UNHCR schema covers different domains (housing,
employment, protection, return intentions). Domain-specific similarity is
plausible without assuming repeated households or exact gates. E025's .79
base + .10 evidence map supports investigating this source; E041's .92 is
not decomposed and does not imply that the remaining .08 is retrievable.

Oracle first on observed Adult profiles, using the established fixed splits
and seeds 41 and 42. Fit E041 weights using only fitting rows and activate
sections using only selector rows. On untouched audit rows, compare the same
query-specific, section-shared convex oracle over held-out logistic base plus
32 donors: initial metric versus learned metric. Also report the union-of-pools
bound, clearly marked as a larger family not the proposed implementation.
Primary gate: seed41 new-pool feasible minus old-pool upper skill / 3 > .005;
seed42 must also be positive. This screens marginal candidate headroom, not
the permissive total E041 oracle or a forecast of HSCC skill. If the primary
gate fails, park E043 without production code and prepare the previously
discussed E041 metric-removal control under a new experiment ID.

If the gate passes: compare actual source predictions with frozen E041 and
E025 on clean schemas (absolute regression <=.002), reuse the existing household
sim and observed-data audit without post-audit tuning, then source/archive
parity and official score.py x3. A technically verified exploratory submission
may proceed despite a missed local adoption threshold under user direction.
Hosted readings against E041 .64: >=.65 positive; .64 inspect best update,
otherwise inconclusive; <=.63 adverse with rounding/noise limitations.

## Change

First implement only `scripts/oracle_e043.py`. Production work is conditional.
Preserve every prior model and snapshot. New archives belong in submissions/.

## Result

Observed Adult oracle, seeds 41 / 42: certified new-pool feasible minus
old-pool upper skill / 3 = +.000962822 / -.000392472. Primary threshold
>.005 failed and replication sign failed. Old/new feasible skill:
.868101/.870989 and .853549/.852371. Union feasible .903181/.883069 belongs
to a larger family, not the proposed K=32 replacement. Optimizer bound widths
are negligible (<3e-11 skill /3). Audit-label masking preserved fitted weights,
activation, candidate identities and base predictions. Outputs:
`../analysis/E043-outputs/oracle-summary.json` plus both seed records.

## Decision

Parked at the registered gate, without production implementation. Domain
verdict: plausible domain-specific relevance does not establish useful
incremental candidate recall on this observed channel. Not a universal HSCC
ceiling. Prepare E044's agreed conditional metric-use ablation for today's
exploratory slot; E041 remains DEV incumbent.
