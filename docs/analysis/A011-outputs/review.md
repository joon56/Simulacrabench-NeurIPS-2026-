# A011 independent review

Reviewer scope: read-only code/design review; no production edits or model fits.
Reviewed registration commit `21931ab`, A006/A009, both A011 scripts, replay
tests, E041 renderer/evidence implementation, and frozen E052 artifacts.

## Pre-run verdict

No blocker found. The deliberate included-label arm is correctly distinguished
from honest holdout evaluation. CAL is visible only in that arm; CTRL and the
original DEV blocks remain masked. The honest arm masks both CAL and CTRL before
base and donor fitting. Only CAL/CTRL labels are scored, after predictions and
their provenance are persisted. Adult uses the declared generic E041 renderer,
fixed seed 53 sample, and no artificial humanitarian gates.

The full-head capture occurs inside the actual renderer callback. The honest
captured evidence, concentration, and effective lambda are reused across
gradient comparisons. Missing evidence stays missing. The reconstruction
`G = (F - lambda * e) / (1 - lambda)` respects the existing lambda < 1 grid,
validates probabilities, and reconstructs the final prediction. Legacy
derivatives reproduce both clipping stages, with a right derivative at the
floor; official derivatives include full-vector normalization and uniform
flooring. Tests include finite differences with unequal vector sums.

No fitted calibrator, new selector, or oracle bypass appears in the diagnostic.

## Frozen E052 verification

Independent scalar per-cell calculation, without calling the audit runner,
reproduced both mean skill deltas and respondent-bootstrap intervals to 1e-15.
No fits were run. The original endpoint and frame hashes match. E052 main, ZIP,
and full Python source dependency hashes match both verification.json and the
uncertainty report. `git diff -- src` was empty.

- Clean: +0.000167291023; interval [-0.000008921584, +0.000342004096].
- Household: -0.001080278441; interval [-0.001457194538, -0.000701348160].

Clean interval includes zero. Household direction remains adverse under this
resampling scheme. Positive bootstrap fractions are descriptive frequencies,
not probabilities of hosted benefit. Affected-row fraction means at least one
exactly changed vector, not a minimum practically important effect.

## Required interpretation limits

- The included arm has 400 additional training rows; CAL-minus-CTRL does not
  isolate a pure causal membership effect from training-volume or tuning changes.
- Reconstructed gate-base gradients hold parent beliefs fixed. They measure
  own-item local pressure, not total derivative through descendant recursion.
- Respondent bootstrap ignores shared donor/family dependence, training
  variability, and multiple testing; 30-row groups remain descriptive.
- Adult has no humanitarian gate semantics and can overlap prior samples.
- No direction, interval, or sign reversal establishes recoverable hosted gain.

## Final replay artifact review

All three channels passed independent read-only verification after completion.
No model was fitted during review. Verified compressed and raw capture hashes,
NPZ hashes, every recorded current source hash, regenerated frame hashes,
partition identity, and every dense NPZ array against the full capture. Query
sets contain exactly CAL/CTRL plus original DEV for honest fits, and CTRL plus
original DEV for included fits. The included fit has exactly 400 extra rows.

All own-evidence mixtures reconstructed captured recursive predictions within
1e-12. Independent normalized/floored scalar arithmetic reproduced aggregate
membership and gate-mismatch means and CAL-minus-CTRL bootstrap intervals within
1e-12. Official CAL, CTRL, and pooled aggregate slopes for all three bases matched
central finite differences on the actual saved vectors (rtol 2e-5, atol 2e-7).
Legacy clipping and boundary behavior were checked against implementation and
the targeted finite-difference/right-derivative tests.

The partition hash records writable arrays before freezing; re-pickling the
read-only capture arrays changes pickle bytes. Writable copies reproduce the
recorded partition hashes exactly, and manifest row lists agree. This is a
serialization-state detail, not a partition discrepancy.

| Channel | Membership CAL | Membership CTRL | CAL minus CTRL | Descriptive 95% interval |
| --- | ---: | ---: | ---: | --- |
| Adult53 | +0.014893902 | -0.001185327 | +0.016079228 | [0.011554718, 0.020506471] |
| Clean | +0.004386031 | -0.000109470 | +0.004495501 | [0.003609352, 0.005398042] |
| Household13 | +0.004522387 | -0.000177763 | +0.004700150 | [0.003656624, 0.005863511] |

Units are mean log probability per scored cell, not skill or hosted gain.
Positive membership-associated optimism is measured in all three channels,
conditional on the declared fits and imperfect common-control adjustment.

Adult has captured evidence for all 800 rows and eight targets, and numerical
zero gate mismatch. In clean, gated pre-own-evidence base versus unconditional
head changes log score by +0.002818418 on CAL and +0.002416525 on CTRL. In the
household channel these changes are -0.004268412 and -0.002039824. The gate-base
comparison therefore has opposite directions across the two simulators.

Official CAL mean lambda slopes (honest full, included full, gate base):

- Adult: +0.030191168, +0.013457460, +0.030191168.
- Clean: -0.007994228, -0.011952149, -0.010714615.
- Household: -0.004219451, -0.008138004, -0.001793717.

These results do not support a universal instruction to increase evidence.
The reconstructed gate base includes unchanged evidence already propagated
through ancestor beliefs. It is not a gate-only ablation or total recursive
derivative. Descriptive CAL item/bucket sign flips are 36 membership and 13 gate
for clean, and 21 membership and 37 gate for household, out of 426 groups each;
they are not independently confirmed discoveries.

After all fits, E052 main/ZIP hashes still match the frozen values, current src
Python hashes match the captured pre-fit manifests, and git reports no src or
submission diff. E052 remains unchanged.

Final verdict: no blocking correctness or protocol issue found. The diagnostic
supports the stated validation mismatch and measured membership optimism only;
it neither establishes a deployable correction nor bypasses future preregistered
oracle, held-out learning, or submission checks.
