# E053 pre-fit design review

Date: 2026-09-24. Read-only review; no fitting, source edits, or scoring.
Reviewed CLAUDE.md, current status/latest three log entries, A011 findings,
E050 registration, recursive_candidates.py, supervised_retrieval.py,
link_sharp.py, prob_link.py, and official-metric reproduction.

## Verdict

Proceed with a narrowly registered diagnostic. This is a mathematically distinct
family, but shares E050's broad scientific hypothesis of misallocated evidence.
Do not call it a new donor model or an already demonstrated calibration repair.
The distinct changes are (1) uncensoring a fixed existing query donor recipe when
legacy replay sets every lambda to zero, and (2) independent absolute weights per
item/concentration bucket instead of one of five transformations shared across
both buckets and a connected gate component. E050 explicitly prohibited dormant
evidence extraction and bucket-specific selection. Its failed oracle does not
bound this larger/different family. Continuous optimization alone would be a weak
justification for reopening E050; uncensored availability is the stronger change.

A011 demonstrates membership-associated optimism, not recoverable gain. Adult53
had evidence for all eight heads and only income had nonzero legacy lambda;
therefore missing evidence is not established as the dominant failure mechanism.
Do not predict oracle success from the positive Adult derivatives.

## Smallest defensible oracle

Use the actual generic E041 stack on the existing ungated Adult adapter, with
one honest whole-block masked fit for each registered split. Freeze base B,
uncensored evidence E, original lambdas, original final E041 F, concentration
flags, and donor/metric provenance. For every item j and existing bucket b,
optimize one scalar lambda in [0,.98]:

    P_rj(lambda_jb) = (1-lambda_jb) B_rj + lambda_jb E_rj.

Require B and E to be finite nonnegative unit-sum distributions before invoking
concavity. On complete fit donors this should hold; check rather than silently
renormalizing a different recipe. Missing/zero-sum evidence means unchanged B,
not invented evidence. Concentration remains the original initial-metric
_topk_excl posterior flag, even when a selected section metric replaces E.
Changing that bucket definition would be another unregistered mechanism.

For fixed unit-sum endpoints and official floor f, realized probability is
q_r(lambda) = f + (1-K_j*f)[B_rj,y + lambda(E_rj,y-B_rj,y)].
Sum log q is concave and separable across item/buckets. Its derivative is
sum d_r/q_r and its second derivative is -sum(d_r/q_r)^2. Check endpoint
derivatives; otherwise solve the unique derivative root by bounded bisection.
Flat objective: choose legacy lambda or zero deterministically. Report numerical
optimality tolerance and an upper-bound certificate using endpoint derivative
signs or the tangent residual. Do not label an arbitrary optimizer return exact.

Compare pooled official log score against frozen original E041 F, using schema
U and delta_skill/3 only as the registered proxy screen. The family contains
E041 on this ungated schema: original lambdas lie in [0,.98] and dormant items
use zero. Assert reconstruction parity before exposing labels. Do not optimize
an extra mixture on top of F; lambda denotes the absolute base/evidence weight.

Keep the previous >.005 delta_skill/3 threshold on BOTH seeds. Failure stops this
Adult diagnostic family before learned estimator or ZIP. Success establishes
only oracle capacity; it authorizes separately specified held-out calibration
and audit, not adoption or a forecast for UNHCR. Selection/audit stay unscored
in today's oracle-only task.

## Capture implementation constraints

The production function computes metric fits, selected sections and replay
lambdas before `if not lam: return {}, {}`. Query donors are constructed only
AFTER this return. Thus "capture before the return" alone cannot recover query
evidence: retain the already fitted state and execute the exact existing query
recipe even when lambda is empty. Do this in diagnostic isolation, with no second
metric/base fit and no force-positive-lambda side effect.

Keep initial weights, active sections, learned weights, visible donor pool,
tie-breaking, candidate count, posterior construction, item options and query
positions identical. If legacy evidence exists, require exact evidence/bucket
parity. If it does not, record this as newly materialized dormant evidence,
not evidence the original run already returned. Original F must retain the
legacy empty layer in this case. Record original active selection independently
of new oracle lambdas. No `supervised_retrieval.predict` dispatch on Adult:
that wrapper otherwise routes to E025 because the UNHCR marker is absent.

Require no-gate schema assertion. Freeze all arrays/source/data/partition hashes
BEFORE oracle labels reach optimization. Use the cached renderer or equivalent
single-fit capture; verify original renderer endpoint parity without refitting.

## Split and leakage plan

Use fixed cached Adult samples seeds54/55, deduplicated profiles, existing
binning/vocabulary only, and 2600 fit / 800 oracle / 800 selection / 800 audit.
Mask all 2400 query PREDICT blocks before ladder selection, neural tuning/refit,
metric fitting/selection, replay, agreement fitting and donor construction.
Source IDs are provenance only. GIVEN values may remain visible as in deployment.
Every donor must belong to the 2600 fit rows; outer query labels must not enter
any internal E041 split. Assert pairwise row-ID disjointness within each split.

Seeds54/55 are not independent datasets and can overlap each other and prior
Adult experiments/A011. Archive exact source-row intersections by current role
versus prior scored roles when available. If prior manifests cannot reconstruct
exposure, explicitly state that limitation. New random seeds do not create an
untouched research population. Selection/audit are unscored in this experiment,
not globally untouched confirmation. Sample/vocabulary adaptation based on the
public source is already disclosed; no label-informed new filtering.

A later learned protocol must resolve the oracle/calibration role explicitly:
either preregister reuse of oracle rows to fit fixed bucket weights, with the
separate selection guard and once-only audit, or introduce a distinct calibration
partition/fit before claiming independent calibration. Reuse is exploratory but
not direct audit leakage when selection/audit labels remain hidden. The current
four-way diagnostic is sufficient for oracle-only work and does not by itself
specify a deployable calibration estimator.

## Limits and bounded alternatives

Adult has no gates, so its exact separable oracle cannot bound the proposed
nonlinear full-recursive UNHCR family. Changing a parent lambda changes descendant
bases; freezing those bases and maximizing each item separately is not a valid
recursive upper bound. Passing or failing Adult must be reported with this scope.
A registered procedural stop may still use Adult failure, but it is a decision
rule, not proof of no humanitarian headroom.

If attribution matters, report three preregistered oracle summaries from the
same frozen data: original E050 five-arm family; independent continuous buckets
using only originally returned evidence; independent continuous buckets with
uncensored evidence. These expose availability versus weight-flexibility effects.
They are nested ablations where applicable, not three chances to alter the gate.
No further fitting is needed. Keep the uncensored family as the sole primary gate.

For a later gated study, smallest defensible option is a fixed finite recursive
library containing identity and explicit new policies, followed by exact
component-wise finite oracle only where component independence is proved.
An arbitrary continuous joint optimizer on recursive gates supplies a feasible
lower bound, not a certified ceiling. A universal per-cell perfect-answer bound
would be too loose to justify the mechanism. Avoid another broad transform grid.

## Required pre-score checks

- Fit/query partition and donor membership; fully hidden query answer blocks.
- Frozen original E041 raw-vector parity and original-lambda reconstruction.
- Capture parity when legacy layer is nonempty; no base/metric refit when empty.
- Unit sums, finite probabilities, correct option order, original bucket flags.
- Concave solver against a dense synthetic reference and boundary/flat cases.
- Pooled official flooring/normalization and complete item/bucket accounting.
- Hash-bound artifacts before label access; selection/audit scorer never called.

No fatal logical blocker for this scoped diagnostic. Fatal blockers would be
claiming its ungated oracle bounds full recursive UNHCR, silently creating a new
donor recipe, treating new seeds as independent untouched data, or using a
nonconcave normalized-mixture objective while claiming the separable proof.
