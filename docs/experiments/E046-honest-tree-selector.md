# E046 — Honest final-output tree selector
parent: E041
status: parked
date: 2026-09-22

## Hypothesis

An equally trained tree alternative, selected on fully masked respondents with
the deployment mixture and downstream gates included, can recover base-model
interactions suppressed by E040's contaminated and inconsistent comparison.

## Domain check

Registered before oracle execution and estimator implementation. A006 found
that E040 selected against a neural network refitted on selection labels and
used a different mixture at deployment. Correcting these defects establishes
a fair test, not evidence that trees improve HSCC. UNHCR's demographic and
household GIVEN fields describe heterogeneous populations and survey sections
(docs/domain.md and public schema descriptions); nonlinear interactions are
plausible, but neither their strength nor direction is established.

The historical E025 loss map (.79 base + .10 evidence = .89) motivates testing
the base, including root predictions that affect gated descendants. It is not
a decomposition of E041's .92. Keep E041's retrieval weights and calibration.
Only UNHCR changes; only the original 57 ungated heads receive trees.

Ceiling channel: existing observed Adult data with unchanged encoding and
profile deduplication, prespecified seeds45/46, 5000 rows split into 3000 fit,
1000 selection and 1000 audit. Fit the existing logistic proxy and categorical
HistGradientBoosting (40 iterations, 15 leaves, learning_rate .1) on identical
fit rows. For each target, oracle-select a fixed mixture from {0,.25,.5} on
audit labels, official .001 floor. This finite headwise oracle bounds the
proposed section-shared mixture family on this proxy benchmark only. Proceed
only if oracle skill gain / 3 > .005 on seed45 and >0 on seed46. Report also
section-shared selection-only choices and independent audit results, without
tuning from those results. If the gate fails, park without a production
estimator. Adult is not a survey-gating replica or an HSCC score forecast.

After a passing oracle: use one deterministic masked outer split of visible
UNHCR respondents, with separate selection and audit subsets, and fit all
E041 components and trees on the remaining rows. Blend only the neural full
heads: w*((1-v)*neural + v*tree)+(1-w)*ladder. Keep conditional heads and
E041 evidence fixed within a fit. Evaluate final outputs, including all gate
descendants and official flooring. Choose section-shared v from {0,.25,.5}
on selection, requiring positive paired respondent gain above max(.001,2SE).
Use an independent all-item audit acceptance check (gain > max(0,1SE)); an
unsuccessful check falls back to exact E041. No audit retuning. Refit selected
components on all visible rows with the same formula. Preserve E041 exactly
when no tree policy survives. Runtime and clean no-regression are hard gates.

## Change

Added scripts/oracle_e046.py only; no production estimator. No historical model
or snapshot is modified. See docs/analysis/E046-outputs/oracle-seed45.json and
oracle-seed46.json.

## Result

Seed45 headwise oracle gain +.000435418358 skill, +.000145139453 skill/3;
seed46 +.000052692697 skill, +.000017564232 skill/3. Exact finite-family
enumeration. Honest section selectors chose zero throughout; audit gain zero.
Split/label-mask invariance assertions passed, source and data hashes verified.
First run stopped on NumPy boolean JSON serialization; cast to native bool and
reran both fixed seeds without changing any numerical settings.

## Decision

PARKED at the oracle gate: seed45 is below .005. No estimator or submission.
This bounds only the registered finite tree mixtures on the Adult proxy; it
does not establish a real UNHCR ceiling or erase A006's validation defects.
Today's separately registered fallback is E047, query-adaptive final evidence.
