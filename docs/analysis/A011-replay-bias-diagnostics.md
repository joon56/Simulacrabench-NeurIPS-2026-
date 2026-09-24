# A011 — Paired replay-bias and E052 uncertainty diagnostics
date-started: 2026-09-24
status: complete
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

### v2 — Frozen E052 uncertainty, no fitting

Executed scripts/audit_e052_uncertainty.py, exit0. Existing frame/endpoint hashes
and E052 main/ZIP/source dependency hashes match. Clean621respondents: paired
delta+.000167291023, descriptive95% respondent interval[-.000008922,.000342004].
Household847respondents: delta-.001080278441, interval[-.001457195,-.000701348].
All respondents have at least one changed prediction; improved/worsened counts
289/332 clean and339/508 household. Positive bootstrap fractions .966/0 are
resampling summaries, not posterior probabilities of a beneficial model.

Clean gain remains uncertain even within this simulator. Household adverse
direction is stable under respondent resampling; shared-donor/family dependence
is not preserved, so this interval can be too narrow. Neither interval models
training variability, post-hoc selection or humanitarian transfer. Keep E052's
original exploratory designation and hosted arms; no tuning or replacement.

### v3 — Replay implementation clarification, before fitting

Derivatives are of log score: positive means local pressure toward more donor
evidence. Legacy objective clips base truth probability at EV_FLOOR, then clips
the mixture; official objective normalizes full vectors before uniform flooring.
At lambda0 or a clipping kink, report the right derivative. Item/bucket reports
cover CAL, CTRL and pooled groups with>=30rows; all descriptive, no fitted policy.
Gate-base derivatives hold the captured parent beliefs fixed; they are own-item
partial derivatives, not total derivatives through descendants. Bootstrap also
ignores shared-donor/family dependence. Neither limitation changes the protocol.
Before fits, archival format is deterministic gzip pickle for full captures
and compressed NPZ for dense diagnostic views (partitions/full-heads/derived
arrays), avoiding hundreds of thousands of redundant per-vector NPZ members.
Both file hashes are frozen before scoring; no scientific family change.

### v4 — Observed Adult53 paired run

Completed exit0; honest4200fit versus included4600fit,400CAL/400CTRL scored.
Full-head included-minus-honest mean log/cell: CAL+.014893901655
(95% interval[.011365883,.018483769]); CTRL-.001185326726
([-.003997693,.001714797]); contrast+.016079228381
([.011554718,.020506471]). This is measured membership-associated optimism,
conditional on these fits and the imperfect common-control adjustment.

Honest captured evidence exists for all800rows and8targets; the absent-evidence
contingency does not fire. Official objective CAL mean own-item lambda slope:
honest full+.030191168, included full+.013457460. Every eligible CAL item/bucket
slope declines in the included arm, but none of the8 signs flips. Thus this
run shows weaker pressure for evidence, not proof a different grid weight
would be selected or improve held-out skill. Existing lambda is .1 for income,
zero for other heads. Gate mismatch is numerical zero, as expected with no gates.
Fits14.153s/8.953s with concurrent diagnostic work. No new weights fitted.
Source/arrays/provenance: docs/analysis/A011-outputs/adult-*.

## Findings

All three registered runs completed, exit0. Each scores400CAL/400CTRL;
original DEV answers remain unscored. Honest/included fit counts are7479/7879
clean,8471/8871 household,4200/4600 Adult. Fit times272.149/227.790s,
366.401/320.732s and14.153/8.953s respectively, with concurrent work.

Membership-associated optimism, official mean log probability per cell:

| Channel | CAL included minus honest | CTRL included minus honest | CAL minus CTRL | Descriptive95% interval of contrast |
| --- | --- | --- | --- | --- |
| Clean UNHCR | +.004386031 | -.000109470 | +.004495501 | [.003609352,.005398042] |
| Household13 | +.004522387 | -.000177763 | +.004700150 | [.003656624,.005863511] |
| Observed Adult53 | +.014893902 | -.001185327 | +.016079228 | [.011554718,.020506471] |

All three contrasts are positive. This quantifies an existing mismatch; it
does not identify the cause of hosted plateaus or measure recoverable skill.
The included arm has400 extra training rows and may select different training
parameters. The control contrast does not eliminate that confounding.

Official own-item lambda slopes on CAL, averaged across captured evidence:

| Channel | Honest full head | Included full head | Honest deployment gate base | Eligible item/buckets | Membership sign flips | Gate-base sign flips |
| --- | --- | --- | --- | --- | --- | --- |
| Clean UNHCR | -.007994228 | -.011952149 | -.010714615 | 426 | 36 | 13 |
| Household13 | -.004219451 | -.008138004 | -.001793717 | 426 | 21 | 37 |
| Observed Adult53 | +.030191168 | +.013457460 | +.030191168 | 8 | 0 | 0 |

Signs are descriptive local derivatives at the existing weights, not tests of
a fitted policy. All three CAL averages decline under label inclusion, but
gate-base adjustments move pressure in opposite directions in the two UNHCR
simulations. Hence neither globally increasing evidence nor globally removing
gates follows from this audit. Some individual slopes are near zero; counts
are not significance-filtered. CTRL and pooled results, both signs, all items
and intervals remain in the full JSON; no favorable subset was selected.

The honest deployment gate base versus full head improves gated CAL log/cell
by+.002818418 in clean but worsens it by-.004268412 in household. CTRL effects
are+.002416525/-.002039824. Nongated and Adult differences are numerical zero.
The reconstructed base already includes ancestors' original evidence through
their beliefs. These are not E052 comparisons or a gate-removal oracle.

Legacy versus official flooring also changes some local signs. Across CAL
honest/included/gate bases, sign differences are12/10/10 of426 clean,
5/9/6 of426 household,0/0/0 of8 Adult. The full legacy CAL membership/gate
flip counts are36/11 clean,25/34 household,0/0 Adult. No floor-only estimator
or selected lambda grid was fitted, and these counts do not establish gains.

E052's frozen uncertainty remains as recorded in v2: clean interval includes
zero and household is adverse under respondent resampling. No new result
justifies tuning E052, promoting it to phase2 or forecasting Grand .65.

Verification: root's11 focused tests PASS6.51s; implementer's combined22
replay/recursive tests PASS6.82s. Independent code, artifact and arithmetic
review is archived alongside the outputs. Preserve original captures, dense
arrays, pre-score manifests, run logs and review. Hash verification binds
unchanged E052 main/ZIP and complete source tree to its original release.

## Artifacts and next decision

New diagnostics live only in scripts/, tests/ and docs/analysis/A011-outputs/.
No src or submission file changes. E052 remains tomorrow's fixed exploratory
artifact; E041 remains incumbent and E025 remains phase2 fallback.

Next model ID remains E053. The next justified research target is a separately
preregistered, whole-pipeline held-out replay family using actual deployment
probabilities and official scoring. First define its finite recursive family
and measure a scoped oracle on frozen, honest outputs; E050's failed family
must not be silently reopened. Only a passed gate permits a learned correction,
with calibration, selection and audit rows separated before first-stage fits.
Budget the extra fit and measure refit distribution shift. Today's captures
are already inspected and cannot become a new untouched selection/audit set.
If a distinct family lacks measured headroom, stop before another package.
