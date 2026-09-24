# A011 — Paired replay-bias and E052 uncertainty diagnostics
date-started: 2026-09-24
status: in-progress
relates-to: A006 / A009 / E041 / E050 / E052

## Goal and authorization

User will submit E052 tomorrow and authorized further experiments now. Preserve
E052 main/ZIP and the complete src tree, including its recorded dependency hash.
This is measurement of an existing validation mechanism, not a new estimator,
candidate family, oracle-gate relaxation, production model or replacement ZIP.
E050/E051 stops and their unscored selection/audit slices remain unchanged.

## Design registered before execution

The A006 mechanism is known but its magnitude has not been measured: replay
evaluates full-head base predictions on rows included in base refitting; actual
prediction mixes evidence with a gate-adjusted base. Loss-map relevance is the
historical E025 .79 base + .10 evidence allocation and .079 gated residual.
Those numbers neither decompose E041 nor quantify recoverable gain. A known
validation mismatch can be protective shrinkage; repairing it need not improve.

Three fixed channels: clean UNHCR, unchanged household seed13, and cached public
Adult sample seed53,5000 deduplicated profiles with existing adapter. Adult is
observed and contains no fabricated gates. It measures fitting membership but
cannot validate humanitarian gate semantics. It can overlap earlier source
samples and is not an independent untouched study. No new data download.

Within each channel, select400 calibration and400 common-control rows from
fully visible TRAIN using permutation seed5301. Original DEV rows remain hidden
and their answers are never scored in this audit. For Adult all5000 begin visible.
Two base fits are deliberately contrasted:

- Honest: hide the complete PREDICT block of calibration and control rows.
  Run the actual generic E041 stack, capturing full-head model_dists, original
  query evidence, concentration flags, lambdas and final recursive predictions.
- Included-label diagnostic: calibration labels are visible; controls remain
  fully masked. Fit the same base stack, capture full-head probabilities on both
  groups, return an empty evidence layer. This intentionally contaminated arm
  is NEVER treated as an out-of-sample score or production candidate.

The second fit has400 more training rows. Report paired mean log-probability
differences on calibration and common control separately, and their contrast.
The contrast helps expose membership-specific optimism but is not a perfect
causal adjustment for training-volume/hyperparameter-selection effects.
Use official floor/normalization, schema order, and fixed whole-row partitions.
Capture all arrays and source/frame/partition hashes BEFORE scoring them.

For the honest fit only, recover the exact pre-own-evidence deployment base
from F=(1-lambda)*G+lambda*e, using the unchanged effective lambda/evidence.
The existing grid ends at .98; do not invert lambda1. Compare this G with the
honest unconditional full head. Reconstruction and probability checks required.
Keep the same honest donor evidence in both membership arms when measuring
evidence-weight pressure. Report the derivative of the EXISTING replay objective
and the official floor objective at the EXISTING lambda. Aggregate by item/bucket
only when >=30 query rows, as in legacy replay. No optimized weights or selector
are fitted. Missing captured evidence remains missing, not re-extracted.

Report all effects, both signs, and per-gated/ungated groups. Paired respondent
bootstrap1000 draws, seed5302; resample calibration and control independently
for the difference of their mean paired effects. Intervals are descriptive,
conditional on fitted models, and ignore training variability/multiple testing.
No significance-driven follow-up or production adoption this turn.

This audit is not an oracle for a new correction. Since no new estimator is
built, no failed oracle is bypassed. Any future repair still needs its own
preregistered scope, oracle, held-out learned gain and submission checks.

## Independent frozen-E052 task

Without fitting or changing outputs, use original clean/household endpoint
pickles and original truth/frame hashes to compute paired respondent bootstrap
intervals for E052-E041 skill, seed5302,1000 draws. Freeze endpoint hashes and
report affected-row fraction. This is post-hoc uncertainty analysis of already
seen simulations, not confirmatory evidence or a reason to tune E052. Retain
the adverse household direction and the original hosted reading arms.

## Reading rules

- Positive membership contrast: this channel exhibits excess optimism on rows
  included in fitting. It does not quantify a recoverable hosted gain.
- Small/negative contrast: do not assume membership dominates local calibration.
- Full-head versus gate-base differences quantify objective mismatch, not a
  guaranteed advantage from new lambdas. Gradient sign reversals indicate a
  changed local pressure only, not an improved policy.
- Missing evidence in Adult: report limitation explicitly; no donor fabrication.
- E052 interval excluding zero: simulator direction is more stable across sampled
  respondents, but still does not establish humanitarian-survey transfer.

## Attempt log

### v1 — Registration and upstream check

Read CLAUDE/status/latest3 log entries and A006/A009. Starter-kit fetch succeeds;
HEAD and origin/main remain ee427a94f6cc6a0d9d653b6be68c835a032e7552. No new
gating release and no kit worktree change. E052 remains the prepared submission.

## Findings

Pending fixed-protocol runs. No measured improvement claimed.

## Artifacts and next decision

New diagnostics live only in scripts/, tests/ and docs/analysis/A011-outputs/.
No src or submission file changes. Record results, tests, review and private
origin push. New model experiment ID remains E053.
