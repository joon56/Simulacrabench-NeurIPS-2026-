# A022 — Remaining SIPP evaluation-role eligibility audit
date-started: 2026-09-27
status: done — PASS_KEYS / EMPIRICAL_HOLD
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

## Result and exposure ledger

Corrected audit PASS; [machine verification](A022-outputs/verification.json).
Exact original12000 sample, both original role namespaces, original5922 fit
keys and fixed A0195999 query keys/roles reconstructed. All source/key and
protected stage-marker hashes matched before/after; E059 audit marker absent.
Protected model-use union remains17999persons/12339SSUID. Excluding their whole
SSUIDs removes30431 eligible people and leaves8700people/4975 complete SSUIDs,
with zero protected-unit overlap. No new sample or role assignment was made.

| Original A014 household role in remainder | People | SSUID |
| --- | ---: | ---: |
| fit | 4275 | 2453 |
| calibration | 1368 | 779 |
| oracle | 1333 | 764 |
| selection | 842 | 478 |
| audit | 882 | 501 |

This is an inventory, not an authorized empirical split. In particular8700 is
not a new audit size. Historical calibration1866/1354SSUID and E059 audit2074/
1177SSUID stay protected. E059 oracle1918/1124 and selection2007/1130 remain
consumed development evidence. No old role is reassigned or reopened.
Original person-level role counts are separately retained in verification;
they do not justify person-level splitting across household boundaries.

Decoded only SSUID/PNUM/MONTHCODE and unchanged eligibility fields THHLDSTATUS/
TAGE_EHC, plus existing key-role metadata. No hospital/reason response, model
GIVEN field, imputation flag, prediction/score array or model cache decoded.
Fit/prediction/score/cache-decode counters all0. Prior source aggregate exposure
remains. This verifies recorded group exclusion, not a new independent source,
unlogged-use absence, adequate statistical precision or real UNHCR efficacy.

Canonical remainder digest:
`9e6953db73bb9ba471e5882aa82081f32ba94e4b7caaabe08b71c9b8b854d993`.
No residual keys saved. Successful audit1.820896s including imports, two threads;
this is not a model runtime estimate. No fit-memory profile was performed.

## Technical deviation, preserved

The initial sandbox launch could not access the existing Python interpreter;
no audit ran then. First actual projection failed a verifier assertion: A014's
all-month role totals were incorrectly compared with eligible-only totals.
Original source proves the different populations. Preserved original
[registration](A022-outputs/registration.md), initial script and
[technical retry record](A022-outputs/technical-retry.md). Corrected only this
scope comparison, with identical eligibility, roles, exclusions and thresholds.
Two actual projections total, one technical retry; no hidden successful rerun.
All corrected checks passed. No existing research STOP was amended.

## S0 decision and alternatives

**Keep A021 empirical HOLD.** Key availability is resolved conditionally on
recorded history; role suitability, precision, actual candidate construction
and full cost remain unresolved. A019's former1000people/500SSUID entry gate was
for its own study. Do not silently transplant it, lower it to pass842/882, or
claim these counts suffice. A future protocol must justify precision before
opening responses, retaining original lambda bucket minimum30/zero fallback.

| Next option | Evidence and objection | Scope/cost and disposition |
| --- | --- | --- |
| Technical candidate-construction and budget contract | A021 establishes controlled P/D mechanics and UNHCR cross-section paths; real builder and internal fit accounting absent | Main: one bounded technical S1, stubs/fixtures only; can resolve implementation feasibility, never efficacy |
| Immediate residual SIPP empirical trial | Whole unused SSUIDs remain; SIPP groups collapse to one section and exact gates do not represent UNHCR cross-section/approximate-gate mechanism; precision unqualified | Defer; no labels/fits; do not rename sections to manufacture the missing mechanism |
| Use all8700 as new audit or reuse E059 audit/calibration | More apparent sample, but violates existing role/exposure boundary | Reject design, no execution; not an empirical rejection |
| Role/channel feasibility closeout if construction is not identifiable | Can document exactly which observed channel/mechanism and cost conditions are missing without spending responses | Justified backup within same technical S1; HOLD, no substitute empirical run |

Static cost evidence: hh_cap.CONFIGS has two neural configurations;
shared_trunk.tune_and_train normally invokes two tuning _train calls and one
final _train. Two base pipelines therefore imply six neural calls on this normal
path, before metric optimization, ladder, lambda and rendering. This is static
accounting, not measured actual fits/time or a bound on fallback paths. A021's
common P/D plus original R design is prospective, with no refit authorized.

Next title: **HSCC · S1 · 실제 후보 생성 경계와 전체 비용 명세**.
[Copy-ready prompt](A022-outputs/s1-handoff.ko.md). This S0 does not execute that
handoff. No E060, production modification, fitting, evaluation-response access,
actual prediction/score, commit/push, submission or S3. E041 incumbent/E025
fallback/E057 parked, E058 STOP/E059 STOP_SELECTION/all prior STOPs, A_half
nonpromotion, A018 user-unconfirmed and no S2 candidate remain unchanged.
