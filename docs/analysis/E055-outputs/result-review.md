# E055 independent frozen-artifact result review

Date: 2026-09-24. No model fits or implementation changes. Independent verifier
uses NumPy/pandas plus Python stdlib, not the production oracle/scoring functions.
Only registered oracle roles are scored. Calibration, selection and audit labels
are not scored. Source row identifiers and individual responses are not emitted.

## Person view: verified STOP

1,850 oracle respondents. Independently recomputed finite-family maximum and
selected composition both exactly match recorded log sum -4381.7237853352.
Independent delta_skill/3 is +0.00011312617812220527, versus registered +.005
gate. Difference from reported delta is floating-point arithmetic only.

All 56 source dependency hashes, registration/source/archive hashes, exact
sample hash, role positions, schema projection, GIVEN values, whole-block
masking, and fit-only donor references pass. All 144 raw parent scenarios are
finite, nonnegative, positive-mass. Original identity arrays match capture.
The decompressed masked archive payload exactly matches pre-fit pickle hash;
re-pickling loaded pandas objects is noncanonical and was not used as integrity
evidence. Selected composition reconstructed from saved arrays matches score;
original execution additionally records zero raw renderer parity error.

Natural bucket occupancy is 1,845 diffuse / 5 concentrated. Evidence exists for
every head/row and original evidence layer returned, so dormant materialization
did not occur. Comparing frozen parent endpoints 0 and .98 changes all 1,850
child vectors in every reason head: recursive gate mechanism was exercised.
Selected oracle changes five parent vectors, five vectors in each of DT/BIR/OS/
COR, and all 1,850 vectors in each of NST/OTH. This is not a dormant no-op result,
but five concentrated rows provide little coverage of that regime.

## Group view: verified STOP

1,872 oracle respondents. Independent finite maximum is -4513.333636868137,
within 9.1e-13 log-sum units of recorded value. Selected composition matches
recorded score exactly. Independent delta_skill/3 is +0.0001023900164058839;
the recorded +0.00010239001640583943 differs only by summation rounding.

All integrity, schema, source, masking and donor checks above pass for this
view too, including conservative SSUID role consistency. Both views use the
same fixed sample but overlapping roles and are not independent replications.
All 144 parent scenarios are valid. Selected raw renderer parity recorded by
original execution is zero.

Bucket occupancy is 1,355 diffuse / 517 concentrated. All heads have evidence
for all 1,872 rows; original layer returned, no dormant materialization.
Comparing parent endpoints changes every row in every reason head. Selected
oracle changes 517 parent vectors; DT changes 1,872, OTH 1,810, and BIR/OS/NST/
COR each 517. BIR log-score contribution worsens by 1.88000936 despite positive
pooled gain; this is consistent with jointly optimizing the whole star rather
than requiring each head to improve.

## Scoped decision

Both views STOP under the preregistered requirement that both views pass.
No downstream learner or submission package is justified by this study. This
bounds only the fixed twelve-point, constant-item/bucket, frozen-donor recursive
family on this edited SIPP sample. It is not a bound on continuous weights,
different predictors/refits, complex gates, or hidden humanitarian-survey skill.

Reproduction: run `verify-frozen-artifacts.py person` and
`verify-frozen-artifacts.py group` with the project Python environment. Verifier reads immutable
local artifacts and emits aggregate `sipp-*-independent-verification.json`.
Its hash is recorded in each verification result.
Both results use the same final verifier SHA256:
`d06e6d78fe60b3c76f69eacedaa4be3dd5880590fae0879462d0562413e7a593`.

Final consistency rerun removed an extra verifier EOF blank line and corrected
its provenance check to use the immutable archived registration. The live E055
experiment record legitimately gained Result/Decision/status updates after both
runs; its current bytes are not the preregistration hash target. Both archived
registrations still match their original recorded hash. Both no-refit checks
were rerun successfully; results and scope are unchanged.
