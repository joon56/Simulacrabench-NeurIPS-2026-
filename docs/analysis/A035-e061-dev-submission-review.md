# A035 — E061 fixed DEV submission recommendation

Date: 2026-09-28. Role: S0 document review only.
Decision: **RECOMMEND_FIXED_DEV_SUBMISSION_USER_CONTROLLED**.
User confirms account/available DEV slot and decides whether to upload.
No agent login/upload or automatic model adoption is authorized or performed.

## Release acceptance

The reported **RELEASE_QUALIFIED_FOR_USER_REVIEW** is supported by the reviewed
records. All142 permitted document/source hashes in the S2 manifest match;
the manifest itself is additionally identified. The scorecard's preregistered
bytes remain an exact prefix of its current version. No ZIP, NPZ, Parquet,
model cache or response file was opened/rehashed. Artifact size/hash and raw
parity are accepted from S2's identified evidence, not newly measured by S0.
[Entry and scope](A035-outputs/entry.json),
[S2 verification](E061-outputs/s2/verification.json),
[preservation](E061-outputs/s2/final-preservation.json).

Fixed artifact: `submissions/2026-09-28-E061.zip`, reported16508bytes.
Reported SHA256:
`4b89e619987d568034bf8a70a7ffda190af483c083ad5921eec9f5a8d843f8c6`.
Snapshot main.py matches the manifest's permitted source identity:
`d1363c7c38d0754d29bb11acdf40a6e14013220b289e4d711196d1271299d0c0`.
Source candidate remains `f9449d41d30041f6e9714c7a25777965ec4d25cfa2563b018fb08c94dde20833`.

| Required evidence | Reviewed result |
|---|---|
| Assembly boundaries | Four new tests PASS; E041 prefix and tied names separated |
| Source/assembly/extracted output | All189649 raw vectors equal, maximum difference0 |
| Controls / intervention | UNICEF/WB exact;132225 UNHCR vectors differ from E041 |
| Regression | UNHCR delta E041-.000070851/E025-.000556996; registered gates pass |
| Official release | Original ZIP checker and score.py all3 PASS |
| Whole-run cost | Assembly402.348s; official all3 suite600.936s, each below900s |
| Resource accounting | S2 workers1053.358s; S1+S2 2151.881s; RSS2.273/private2.451GiB |

Expected initial missing-assembler RED is separately identified and included
in cost, not an unresolved failure. Pre-run pending wording in preserved
intermediate records is resolved by final official/resources/verification.
S2's source review is root self-review, not independent replication. Local CPU
qualification does not guarantee hosted H100 cost or efficacy. S0 reran none
of the checks and does not claim new scientific evidence.

## Why submit rather than repeat or hold research

This is the fixed parameter-sharing question accepted in A034. The intervention
is exercised, controls are preserved, packaging is qualified and source costs
are bounded. An additional local run would not answer target transfer. Waiting
for VAF approval is not necessary for this separate DEV exploration.

There is no positive synthetic gain: UNHCR .5623918781304167 is slightly below
both local comparators. That reused exact-gate channel is engineering evidence,
not a valid ERPIS futility test. Sharing logits may regularize or remove useful
flexibility; changed RNG consumption, refitting and lambda choices remain part
of the complete policy. No numeric expected gain or winning probability exists.

A single DEV observation can change an operational decision under the existing
arms. It cannot reliably resolve every small gain/loss or isolate a neural
mechanism. Repeated E041-level historical readings reduce enthusiasm for minor
nearby variants, but do not establish that this distinct fixed candidate is
identical on target data. This recommendation is based on novelty and completed
qualification, not past compute spending or a need to fill a slot.

Keep the original [SCORES arms](../../submissions/2026-09-28-E061/SCORES.md):

- Verified new best: favorable noisy evidence for the whole candidate; S0 review,
  no automatic incumbent or TEST replacement.
- Same Grand/no best update: unresolved, E061 parked and E041 retained.
- Comparable Grand decline: adverse for that run, not a universal refutation.
- Failure/timeout: technical outcome, not statistical inferiority.
- Conflicting identity/reading: provenance review before interpretation.

Use reported institution scores when supplied. The E041 comparison is Grand
.6433333333 / UNICEF.52 / WB.49 / UNHCR.92, a released reading rather than an
unnoised target. E060's equal values remain inconclusive. Do not reinterpret
extra Grand decimals as extra hidden instrument precision. No repeated same
policy uploads for noise reduction or outcome-driven seed/head/threshold rescue.

## User action and result owner

Account authorization, current DEV slot, actual upload time/ID/bytes and hosted
effect remain **unconfirmed**. The user was asked about slot availability;
no answer is assumed. This is an operational prerequisite, not a new empirical
HOLD. If unavailable, preserve the same fixed ZIP and wait for availability;
do not create another candidate or rerun release checks merely because time passed.

If the user elects to submit, select the exact dated ZIP above in Development.
Preparation date is not upload date. Record what is available:
account/slot confirmation (no credentials), selected file path/name and any
local hash actually checked, submission ID, platform created time with timezone,
status/failure code, Grand, best-update indication, and reported institution scores.
An API result excerpt containing only these fields is sufficient. Unknown fields
stay unknown; a local hash/file-name match alone does not prove remote bytes.

After a result, return to the **same S2** for append-only result intake using the
[result-only prompt](A035-outputs/s2-e061-result-intake.ko.md). No new S1 or
release execution is needed. S2 reports the registered reading back to S0.
This prepared prompt is not executed until the user supplies actual evidence.

## Preservation and closeout

Only A035/status/log changed. S1/S2 scientific artifacts, manifests, scorecard,
source, snapshot, ZIP and tree remain untouched by S0. HEADa43f437 remains.
E041 incumbent/E025 fallback; E057/E060/E061 parked. All STOP/HOLDs, including
E058 STOP/E059 STOP_SELECTION and A023/A024 empirical HOLD, remain. A_half is
not promoted; A018 TEST is user-unconfirmed and S3 stopped.
Prior17999people/12339SSUID, aggregate exposure, A022 original roles and E059
consumed oracle1918/1124/selection2007/1130 versus protected audit2074/1177 and
calibration1866 remain. No response/cache access, scientific execution, login,
upload, git mutation or TEST selection. [Verification](A035-outputs/verification.json).
