# E0XX — short-slug
parent: E0YY            <!-- tree edge: the experiment this branches from; "—" for roots -->
status: parked          <!-- adopted / rejected / parked / superseded-by:E0ZZ -->
date: 2026-MM-DD

## Hypothesis

One falsifiable sentence: what should improve, where, and why.

Name the target instrument/cells and the distinct mechanism versus earlier
experiments. Relate it to the historical E025 loss map where relevant without
pretending that map describes E041 or quantifies recoverable gain.

## Domain check

Pre-registered BEFORE running: what background domain knowledge (docs/domain.md,
published survey reports — not methods literature) predicts about this result,
one sentence with source. Filled in AFTER: consistent / surprising. Surprising
raises the evidence bar, never auto-rejects: rule out artifacts (leakage, coding
error, confound), replicate on a different seed/split/slice; if it survives,
consider adoption under the registered criteria and record the finding.

## Preregistered scope and decision

- Comparator, source hash, phase, data source and target population.
- Previous label exposure; fit/calibration/selection/audit roles and group units.
- Oracle scope: frozen components, parameter family and what it can/cannot bound.
  If no valid informative oracle exists, justify the limited channel and a
  distinct bounded exploratory design before implementation; do not relabel
  an old failed study. Follow CLAUDE.md and docs/workflow.md.
- Separate technical qualification, release performance policy, DEV exploration
  and TEST selection. State favorable/adverse/unresolved/failed arms and what
  each changes. The historical +.005 is a local default, not universal significance.
- Main task, ready backup, resource cap and stopping point. Allocate the ID before
  running; preserve registration bytes/commit separately from mutable results.
- Claim/decision each diagnostic can resolve. Do not expand diagnostics whose
  outcomes cannot change the next action.

## Change

What was built/modified (file paths). Small enough to attribute the delta to.

## Result

Identify the actual data, phase, split and comparator for every result. Separate
oracle headroom, learned held-out change, technical checks and hosted readings.
Mark unavailable cells explicitly. Include paired uncertainty where estimable,
its sampling unit and omitted sources of variation. Preserve all attempts.

Local three-instrument comparison when applicable:

| | sample | unicef | world_bank | unhcr | mean | Δ vs parent |
|---|---|---|---|---|---|---|
| this | | | | | | |

Reproduce: `.venv/Scripts/python src/eval/runner.py <model path>`
Raw runner output: `results/E0XX.json` (if saved)

## Decision

Apply the registered arms unchanged. Record: local qualification; DEV exploration
eligibility/actual reading; DEV incumbent impact; TEST shortlist/selection impact.
Distinguish facts, interpretation and policy. A scoped STOP is not a universal
ceiling; a flat rounded Grand is not exact zero. State the next action and what
new evidence could legitimately change priority. Never revise the threshold
after seeing a disappointing score. Read docs/workflow.md for shared rules.
