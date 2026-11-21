# A022 — Remaining SIPP evaluation-role eligibility audit
date-started: 2026-09-27
status: in-progress
relates-to: A019 / A021 / E059

## Registered scope before key projection

User authorized the next task proposed by S0: audit remaining keys and exposure,
protect existing roles, and determine whether a future evaluation channel can
be specified. Input HEAD1d223340d4e1fa3993b411dc5daafab9cb37d0cd; A020/E059/A021
remain uncommitted. No model fit, prediction, score, PREDICT-response read,
model-cache deserialization, commit/push, submission or S3. No E060 creation.

One bounded audit, 30-minute session cap, one sequential key scan using existing
Python/Arrow/Pandas with two numerical threads. No model imports or installs.
Source projection is exactly SSUID, PNUM, MONTHCODE, THHLDSTATUS, TAGE_EHC.
The last two are the unchanged A019 eligibility fields, not model predictors
in this audit. Hospital/reason responses, six model GIVEN fields and imputation
flags are not projected. Existing key files expose only IDs and role metadata.
File hashes read bytes for provenance without decoding other columns.

Reconstruct the original eligibility rule, original12000-person E055 sample,
both A014 role namespaces and A019 fixed5999 queries. Exclude the union of all
historical and query-use SSUIDs, including unopened reserved roles. Retain the
whole remainder: no new sampling namespace, seed, head or response inspection.
Report actual counts, canonical key digest, group completeness/disjointness,
and remaining original A014 role tags. Do not assign new roles or reserve rows.

PASS_KEYS requires matching source/key manifests, exact historical sample and
roles, exact A019 query reconstruction, no protected-unit overlap and an intact
remainder. Count or hash inconsistency is STOP; do not adjust eligibility.
There is no newly invented minimum count or power claim. Any future study must
choose and justify role compatibility and size/power criteria prospectively.
Full-source aggregates have been exposed; residual key eligibility does not
make this an independent new dataset or confirm target-domain suitability.

Recorded-use scope: tracked and current scripts/source/tests/analysis records,
known ignored audit scripts and preserved stage markers. Cannot certify arbitrary
unlogged activity. Expected recorded model users remain E055/E056 and E058/E059;
A021 was fixture-only. Preserve original calibration1866 and E059 audit2074.

## Planned deliverables

Archive the exact audit source and aggregate result in A022-outputs. No person
keys in tracked outputs and no residual Parquet or role assignment is created.
Record protected hashes before/after and the access ledger. Update this record,
status/log only. Existing study bytes and tree remain unchanged. No automatic
candidate implementation, fitting or additional branch follows this audit.
