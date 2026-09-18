# A006 - Development ranking: validation audit
date-started: 2026-09-18
status: done
relates-to: E025 / E039 / E040 / E023 / E030 / E035 / E037

## Goal

Reassess whether the recorded nulls justify closing development search,
following the user's explicit priority change to improving DEV rank.
The execution clock precedes the supplied September 21 handoff; the audit
examines the files and historical outcomes as supplied, not new hosted results.

## Attempt log

### v1 - Source and submission audit

- Read E023, E030, E035, E037, E039 and E040 records; traced model fitting,
  weight selection, and final prediction in shared_trunk.py, tree_blend.py,
  link_sharp.py and hh_sharp.py. Checked the E040 assembled snapshot too.
- Found asymmetric validation in E039/E040 and different tuning/deployment
  mixture formulas. These are static implementation findings; no improvement
  measurement or new model training was performed in this audit.
- Checked item-share arithmetic with 57/213 ungated UNHCR items.
- Reviewed scikit-learn's official stacking guidance on out-of-fold predictions:
  https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.StackingClassifier.html
- Verdict: retain the historical flat score; withdraw the claim that it
  establishes a ceiling for trees or for every real-data base model.

### v2 - Full-history review corrects the item-scope interpretation

- See A007 for the complete submission ledger and conditional next-submission
  plan. The v1 statement below that E040 leaves 156 gated items untested is
  withdrawn: it fits trees for 57 ungated heads, but link_sharp propagates
  parent beliefs into gated predictions. Schema traversal finds 155 gated
  descendants reachable from those 57 roots, including 73 direct children of
  s3_11_intent_return_12m_lbl. Reachability is not measured score improvement.
- The 57/213 arithmetic is valid only for an isolated direct effect with
  downstream predictions fixed, not as a bound on E040's total effect.
- E018 already documented in-sample replay bias. The new proposal tests that
  known tradeoff and the final-output objective; it is not a newly discovered
  source of signal. Removing conservative bias can also increase variance.

## Findings

1. [consistent: statistical validation; no population assumption required]
   **E040 does not compare equally held-out predictions.** Trees fit fit_rows.
   tree_blend.predict calls shared_trunk.tune_and_train, whose return is the
   final network refitted on ALL complete visible rows. It then evaluates
   that returned network on eval_rows, which were included in its refit.
   The tree is out-of-sample while the net is in-sample. This can bias the
   blend toward the net; whether it changed the real-data selected weight is
   unknown. This is internal validation contamination, not access to DEV
   answers. Both source and submissions/2026-09-20-E040/main.py contain it.

2. [consistent: algebra]
   **The tree mixture being selected is not the mixture deployed.** Writing
   n=network, l=ladder, t=tree, tuning evaluates
   (1-v)*(w*n+(1-w)*l)+v*t. Prediction instead uses
   w*((1-v)*n+v*t)+(1-w)*l, before any gating/evidence layers.
   These coincide only in special cases. Tree weight becomes w*v at
   inference. The corrected experiment must tune the same final distribution
   it will emit, including downstream processing when relevant.

3. [consistent: metric arithmetic]
   **E040's claimed sensitivity was too optimistic.** It affects 57/213
   items. A +0.01 average per-cell skill improvement on that subset, using
   the instrument-wide U convention of probes.py, is only +0.002676 UNHCR
   and +0.000892 Grand. That can easily be hidden by rounding/noise. It also
   leaves the 156 gated items untested. Flat does not mean zero everywhere.

4. [consistent: validation mechanism; score benefit unchecked]
   **E025 evidence replay is not cross-fitted.** The self-excluded candidate
   evidence is compared with base distributions fitted on all visible rows,
   including replay queries. This may favor the base and suppress useful
   lambda, but the sign and size of the final effect are unmeasured. For
   gated items, replay uses unconditional full-head base distributions while
   deployment mixes evidence into the gate-adjusted base. EV_FLOOR clipping
   in replay also differs from the grader's uniform-mixture floor.
   E023 tested K and a second weight iteration, not these issues.

5. [consistent: scope of an upper bound]
   **Several 'ceilings' are conditional experiment results.** A005 is a
   generator-specific Bayes reference; it says nothing about real-data
   optimality. E030 bounds a particular adjacency-credit experiment on an
   injected drift distribution. E035 uses a specified transition family on
   an injected structure. E037 is finite-sample cross-fitted isotonic
   calibration, not a universal oracle over all calibration procedures.
   Their null results remain valid within those scopes; broad closure does not.

## Prioritized next work, not an adopted model change

1. Reproduce the two tree-selection defects with row-membership and
   probability-algebra checks. No submission needed. Preserve E039/E040
   snapshots and implement any repair as a new experiment, never overwrite
   rejected modules. Require a common held-out split and identical selection
   and inference formulas before interpreting a tree result.
2. Audit an out-of-sample, final-distribution evidence selector. Mask all
   PREDICT cells on validation rows and remove their labels from model fits
   and candidate pools. Use another split to evaluate selected weights;
   inspect the candidate-pool-size difference from deployment. Benchmark
   runtime before contemplating a UNHCR-only submission.
3. Reconsider asked-answer prediction for gated items only if a validated
   candidate exists. The estimated 0.079 gated loss is larger than the
   0.031 ungated loss; it includes content errors, not just sentinel errors.
   Merely choosing a different architecture is not evidence of a gain.

### Loss-map explanation and pre-implementation ceiling channel

The replay hypothesis targets how the established +0.10 evidence contribution
is combined with the 0.79 base; it does not assume an undiscovered household
structure. The tree repair targets invalid selection on the 0.79 base, not
a new claim that trees explain the leading teams.

First use existing held-out synthetic rows and frozen, equally out-of-sample
candidate predictions. Truth-optimized weights over a specified, identical
mixture family give an optimistic empirical bound for that family on those
rows. Evaluate learned weights on separate rows; no oracle settings enter
the submission. A bound below the adoption bar rules out that local channel,
not real-data headroom. No additional household structure needs to be injected
to detect leakage or mixture inconsistency.

We cannot measure the real-data ceiling before a hosted run with current
access. In-container validation on visible TRAIN labels can choose ordinary
model weights, but its detailed results stay inside the enclave; the returned
aggregate score is the only external transfer reading. Static defects justify
reopening validation, not promising a score increase or bypassing the
pre-submission requirements. Any eventual submission changes UNHCR only,
pre-registers interpretations, and passes no-regression, parity, ZIP and
three-schema official checks within the shared 900-second budget.

## Artifacts

- This analysis record; updated docs/status.md and top of docs/log.md.
- Model code, submission snapshots and measured scores unchanged.

## Feeds into

DEV-ranking work takes priority over further phase-2 polishing. E025 remains
the incumbent and prepared phase-2 fallback. No new E-series experiment is
adopted, no score gain is claimed, and no leaderboard slot was consumed.
