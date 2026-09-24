# E053 implementation review before fits

Reviewed 2026-09-24: registration a452465, scripts/screen_e053.py,
tests/test_e053_oracle.py, supplied diff, and original donor/renderer functions.
No production edits or model fits performed by reviewer.

## Verdict

No blocking scientific or implementation defect found for the registered ungated
Adult oracle. Proceed after recording the archival clarifications below. This
review does not authorize a learned calibrator, gated ceiling claim, or package.
The parent reports 13 focused tests passed; I inspected these tests but did not
repeat that suite.

## Capture and baseline

Private FunctionType namespaces preserve the original implementation while
capturing signature, initial weights and section fit exactly once. The dormant
branch executes the existing query recipe from those frozen products. It does
not refit or force positive legacy lambdas. Selected learned evidence replacement
uses the original implementation and the concentration flag stays attached to
the initial posterior. The wrapped top-k and replacement candidate calls check
that every outer donor is a fit row. The original layer return remains the
renderer input, so dormant materialization does not change the baseline.

The generic renderer avoids Adult's E025 wrapper dispatch. A second cached render
checks frozen endpoint parity without refitting. Raw original-lambda
reconstruction provides a separate algebraic check at tolerance 1e-12.
Nonempty capture is compared to the original layer in tests, including an active
section. Dormant active-section behavior is not explicitly tested, but static
control flow reuses the same checked replacement function and is sound.

## Oracle and missing evidence

Endpoint validation followed by explicit normalization matches registration.
The scalar log objective is concave, endpoint derivatives and bisection select
the global optimum, and the tangent maximum is an upper bound in exact
arithmetic. This is a floating-point numerical certificate, not interval-
arithmetic proof; the registered pooled 1e-9 tolerance is appropriate here.

Taking max(identity bucket mean, optimized bucket mean) implements the declared
additional identity option. Assigning the bucket upper mean to each bucket row
then summing preserves its cell-weighted bound. Missing/zero evidence cells keep
original F and still count in pooled score. The exact identity option prevents
normalization roundoff from manufacturing a negative attainable gain. PASS uses
attained score and STOP uses upper score as registered.

The original five-arm ablation matches E050 on this ungated schema, where each
item is its own connected component. Its lambda=1 arm means it is not strictly
nested in E053's [0,.98] family. Do not describe all three ablations as nested or
assume the primary oracle must dominate that five-arm score. The registration
does not make that erroneous claim.

## Roles, leakage and freeze order

The 2600/800/800/800 contiguous role construction is disjoint by construction.
All 2400 query answer blocks are masked before build_library. Internal E041
training/calibration sees fit labels only. prepare reads schema vocabulary and
prior source IDs but does not score outer labels. Oracle labels are mapped only
after capture, dense arrays and manifest writes finish. Score calls select the
first 800 query rows, matching the oracle positions; selection/audit are not
scored. Both seeds must still be run operationally, because each CLI invocation
runs only one seed.

Known-role overlap indexing is correct: E050 uses interval endpoints; A011 uses
explicit position lists; the other E053 sample uses the same fixed role slices.
A011 roles observed in its manifest are CAL400, CTRL400, FIT4200, DEV0. The
inventory is correctly labeled nonexhaustive. Upstream load_observed removes
modeled duplicates before sampling, preserving original source-line IDs.

## Archival improvements before fits

1. Bind the consumed E050/A011 manifest bytes to hashes in the new manifest and
   validate their source-file digest matches the current Adult source where
   available. Otherwise the exposure inventory cannot independently identify
   which prior manifests were consumed, despite being reproducible today.
2. Record the registration commit/hash and test-file hash alongside existing
   source hashes. The supplied registration commit already establishes the
   external chronology; adding it makes each run self-describing.
3. Capture currently records donor-membership check count, fitted signature,
   weights/section products, and evidence, but not actual donor indices or
   posterior arrays. These can be reconstructed without new fitting. Archiving
   query donor indices/posteriors (or their hashes plus query/bank positions)
   would make the intended donor provenance directly inspectable. This is an
   auditability gap, not evidence of wrong donors or invalid oracle arithmetic.
4. Add explicit source-ID uniqueness and query-position equality assertions if
   touching prepare/build bookkeeping. Current fixed loader and role slices
   already imply these properties; no observed leakage defect.

These are bounded provenance improvements, not reasons to alter the family,
splits or threshold. No additional broad test run or model fit is requested.

## Independent verification performed

Compared all 51 src files named in the A011 Adult manifest against their archived
SHA-256 hashes using PowerShell: all 51 match, zero mismatches. No src change.

Attempted an optional 80-case independent scalar optimizer probe and metadata-
only prepare check, but neither executed: `python` is absent in this tool's PATH;
the workspace .venv launcher refers to an unavailable Python313 executable.
No numerical-probe pass is claimed. Static derivation and inspected focused
tests support the numerical assessment above; the parent has a working runtime.

## Resolution after targeted pre-fit update

Rechecked current screen_e053.py before any E053 fit. All material archival
recommendations are resolved:

- Both E050 manifests and the A011 manifest are now byte-hashed and their Adult
  source digests checked against the current cached source before fitting.
- Current source IDs are explicitly checked for uniqueness.
- Outer query donor records retain function name, query positions, donor-bank
  positions, and copied function result. This captures initial top-k indices and
  posterior weights plus learned-section candidate IDs. The existing fitted
  state retains learned metrics, permitting exact posterior reconstruction.
- The focused test file is included in source hashes.
- Registration bytes are read before fitting, separately hashed, and copied to
  a per-seed registration artifact before any oracle scoring. Later Result edits
  to the live experiment document cannot invalidate that archived preregistration.

The parent reports the final focused suite passed 13 tests in 5.29 seconds; this
review did not repeat it. No statistical family, baseline, partition or gate
changed. The remaining suggested explicit query-position equality assertion is
optional: the fixed mask and deterministic np.flatnonzero order already imply
it. The lambda=1 non-nesting interpretation is acknowledged for final reporting.

No remaining pre-fit blocker found. Preserve the registration snapshot without
adding results between the two seed runs, or document any differing snapshot
bytes explicitly. No additional fitting or source edits were performed here.

## Parent execution of independent probe

Parent ran the supplied probe with the working project venv, exit0:80 scalar
checks passed; maximum independent score difference1.7763568394002505e-15.
Both metadata-only split checks and51 unchanged source hashes passed.
No model fits or observed-label scores were computed by the probe.
