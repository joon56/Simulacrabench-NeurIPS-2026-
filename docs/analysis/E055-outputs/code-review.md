# E055 independent code review

Date: 2026-09-24. Static review of `scripts/screen_e055.py` and
`tests/test_e055_star.py` against preregistration commit `2a52f18`.
No real fits or scores run; implementer owns synthetic test execution.

## Initial review: corrections required before GO

1. **Important: incomplete frozen prediction artifact.** Initial `run` saved
   donor capture and identity, but excluded the renderer closure and did not
   serialize full/conditional model products or finite parent-scenario bases.
   Parent scenarios were first generated after oracle labels were mapped.
   Preserve all label-free parent scenario outputs before oracle label access,
   together with evidence, availability, buckets, identity and original shares.
   Then the frozen file reproduces the whole finite family without refitting.
2. **Important: incomplete invalid-probability rejection.** Initial validation
   ran through `_score` only on oracle rows. Invalid unscored query scenarios
   could escape, and NaN parity differences do not satisfy `> tolerance`.
   Validate every query row of each raw frozen scenario before label access.
   Reject nonfinite/negative provided evidence; do not treat NaN mass as absent
   evidence. Zero evidence mass may remain explicitly unavailable.

Both findings reported to root and implementer before execution. Initial
mathematics, masking, domain mapping, and no-interpolation renderer call are
otherwise sound. Final clearance requires inspecting corrections below.

## Additional guards requested

- Initialize optimum with explicit identity, then assert identity domination.
- Exact raw original-endpoint parity, with finite checks before comparison.
- Deterministic original-first complete-star ties and original empty buckets.
- Preserve query/role positions and relevant source dependency hashes.

## Checks already satisfied in initial code

- Adapter projects six GIVEN fields and seven PREDICT fields only; IDs, flags,
  hospital duration and eligibility fields cannot enter model schema/frame.
- Sample SHA256 payload and fixed 12,000 cap match registration; roles use
  A014 namespaces. Reset-index source, frame and roles remain aligned; oracle
  labels use query positions selected through corresponding role positions.
- All non-fit target blocks masked before generic E041 fitting. Original
  capture_layer validates fit-only donor references and retains original flags.
- Root pair enumeration uses original cached renderer, including soft gates.
  No interpolated parent path. Child mixtures use actual raw vectors followed
  by floor_mix, correctly handling unequal endpoint masses.
- Child rows without evidence retain their changed-parent base. Full parent
  plus child log sums determine the selected pair. Official pooled skill
  normalization uses class counts including each gate sentinel.
- Continuous policies, donor refits and additional base tuning are absent.
- Existing synthetic tests compare against exhaustive finite assignments with
  soft gates and nonunit evidence, cover absent-child propagation, and verify
  adapter projection plus whole-block masking. Test execution not duplicated.

## Final clearance

**Clear for root-controlled execution.** Re-reviewed corrected source after
implementer reported 10 focused A014/E055 tests PASS and py_compile exit 0.
No remaining critical or important issue found. No real fits or scores were
run by this reviewer; reported test results belong to implementer and were not
duplicated.

Corrected implementation resolves both important findings:

- All 144 mapped parent-scenario arrays and identity are written to a separate
  hashed NPZ before oracle labels are mapped. Evidence/capture, masked frame,
  role positions and source dependency hashes are also persisted first. Those
  products reproduce the finite family without the live renderer closure.
- Every raw original endpoint and parent-scenario vector is validated on every
  query row. Nonfinite/negative evidence raises immediately; zero-mass evidence
  remains unavailable. Exact original raw endpoint equality is required.

The oracle now starts from explicit identity and replaces it only for a strictly
greater score. Exact ties use original-first share order followed by ascending
grid values, and empty buckets keep original shares. Final selected composition
is checked against the actual renderer, with nonfinite parity rejected.
Outputs include baseline/oracle skill, per-head gains, bucket occupancy,
available/active evidence counts, and returned-versus-dormant status.

Reviewed file SHA256 values:

- screen_e055.py: `be1b41c66dfebf1ff873407db601fcc4029e8872366ca76016c39254402e14fe`
- test_e055_star.py: `c21595fa7c8a6ad447838b39345f0cedc4e7dfa872fcd7b032ccec9b8a84eafd`

Scope of clearance: faithful finite-family implementation and specified data
boundaries, conditional on root's final source hashes and successful runtime
checks. It is not a statistical result, proof of transfer, or approval of a
later learner outside the registered family.
