# E045 - Candidate union with guarded learned reranking (UNHCR only)

Status: **HOSTED RESULT REPORTED: Grand .64, no best update.** The preregistered
unresolved arm applies; E045 stays parked and E041 remains incumbent. Individual
instrument scores are unavailable. Incumbent E041 Grand .64 /
UNICEF .52 / World Bank .49 / UNHCR .92. E044 removal control read Grand .63.

## Preregistered intervention

Preserve E041's learned metrics and activation. Active sections may add up to
32 donors found with the learned metric to the original 32 set, deduplicate,
and refit a diagonal metric on fit rows. Select expansion against unchanged
E041 K32 learned evidence on separate selection rows only if gain exceeds
max(.003, 2 paired respondent standard errors). Replay and inference use the
same policy. Original replay/lambda procedure remains; downstream effects are
part of this pipeline intervention. Inactive/rejected sections retain E041.
UNICEF and WB remain unchanged. External Adult records are validation only;
no external records, fitted models or weights enter the archive.

Oracle and full protocol: docs/experiments/E045-union-retrieval.md. Passing the
oracle establishes permissive headroom, not learnability or an HSCC forecast.
Selection retains the known marginal-proxy/full-stack mismatch and inherited
in-sample base replay; this experiment does not claim to repair either.

## Pre-registered reading arms

| Grand / best update | Interpretation | Next action |
|---|---|---|
| >= .65 | Favourable expansion pipeline reading | Inspect instrument scores and controls; preserve new best, validate phase 2 separately |
| .64 with best update | Favourable within displayed precision | Record triple and retain winning snapshot; no exact causal attribution |
| .64 without update | Unresolved at displayed precision, or selector inactive | Keep E041; do not infer a universal retrieval ceiling or run a blind K grid |
| .63 | Adverse reading near resolution | Keep E041; deprioritize this union configuration and examine selector transfer |
| <= .62 | Larger adverse reading | Keep E041; stop this expansion configuration |
| FAILED | No valid statistical reading | Diagnose locally; failed attempt does not consume daily slot under recorded rule |

.64 is the incumbent reference and .65+ the target, not a calibrated forecast.
Only UNHCR changes: Grand deltas translate approximately x3, subject to
rounding/noise. Individual scores unavailable without a best update must stay
unavailable. Do not infer hidden UNHCR values from displayed Grand arithmetic.

## Validation results

| Check | Measured result |
|---|---|
| Observed oracle, seeds 43/44 | Certified marginal skill/3 +.007834132 / +.009196164; preregistered gates PASS |
| Actual observed audit, seeds 43/44 | Skill +.000426 / +.000495; both paired 95% intervals include zero |
| Clean UNICEF / WB | .500648423 / .454717307; every probability exactly equals E041/E025 |
| Clean UNHCR | E045 .562397862; E041 .562462729; E025 .562948874 |
| Clean no-regression | PASS; delta -.000064867 vs E041 / -.000551012 vs E025 |
| Clean mean delta vs E041 | -.000021622 |
| Clean union activity | Sections3/4/5/6; maximum raw probability difference vs E041 .264736391 |
| Existing household sim, seed13 | .552012531 to .551945260; UNHCR delta -.000067271 |
| Tests | 23 PASS; original donor retention, zero duplicate mass, gradients, label isolation, replay and fallback |
| ZIP checker | PASS; root main.py only |
| Official phase-1 and source/archive parity | PASS x3; every raw probability exactly equals source on all schemas |
| Official local runtime | 395.852 s total; rounded components 37.671 / 93.269 / 264.913 s; shared budget 900 s |

Neither local channel qualifies for adoption at mean delta > .005. The
user-authorized exploratory submission still requires every official check,
exact assembly parity and clean <=.002 no-regression versus E041/E025.
The observed oracle is much less constrained than the actual estimator;
its gain must not be used as a predicted Grand improvement.

Archive SHA256: `215da373111e8109db908b7568906d6c6b39a1962265a2ecd47a9f2f3362fba3`.
Main SHA256: `fb2daa757e8503a8846e528165f855fd94dde1c454aab79065f8b290c55c61f4`.
Source dependency hash: `cf65c6413368133ba1f5955503e2cf85963ec186b8f90b0eb5976a1b7eeedd0f`.
Raw evidence: docs/analysis/E045-outputs/ and adjacent verification.json.
Baseline caches were revalidated against the current frame and pinned snapshot
hashes. Their timing fields are historical, not newly measured. No model
settings changed after the observed audit or simulation. The first official
verification attempt failed only while writing a relative log path under the
kit's working directory; the verifier resolved the path and its full rerun
passed. Two numerical threads; 406.730 s verification wall time. This local
measurement is not a hosted worker speed guarantee. E041 stays DEV incumbent;
E045 remains parked after the unresolved hosted reading recorded below.

## Actual hosted result

User reported **Grand 0.64, no best update** on 2026-09-21. UNICEF, World Bank
and UNHCR scores are unavailable. This is a completed scored submission, not
a failed attempt. Source: user report, not an independent platform fetch.
Exact upload time, submission ID and hosted runtime were not provided.

Apply the preregistered **.64 without update** arm: keep E041 and park this
E045 configuration. Candidate expansion did not produce a best update. Equal
displayed Grand does not establish equal underlying scores, zero UNHCR effect,
or an E045 UNHCR score of .92. Rounding/noise and possible selector inactivity
remain indistinguishable; local activation does not establish hosted activation.

The observed Adult oracle showed permissive candidate headroom, not a learned
HSCC gain. Actual observed gains were small and inconclusive before submission;
this result does not justify a universal retrieval ceiling. Keep learned weight
use supported by the E044 comparison. Do not spend subsequent slots on a blind
candidate-count grid; prioritize auditing selection against final predictions
or a separately screened mechanism. E041 remains DEV best .64/.52/.49/.92;
E025 remains the validated phase-2 fallback. Archive/model bytes unchanged.

## API score reconciliation - 2026-09-27

Source: user-supplied My Submissions JSON, recorded 2026-09-27.
This supplement supersedes missing-score/ID/time statements above for the IDs
listed here; the earlier registration, interpretation and local checks remain
historical. Values below are released API scores, not unnoised raw scores.
Created time is platform submission metadata, not the snapshot directory date.
Current leaderboard membership is not a historical best-update event log.
The uploaded ZIP bytes/hash and hosted runtime are not verified by this response.

| Submission ID | Filename | Created (KST) | Status | Grand API | UNICEF API | World Bank API | UNHCR API | On leaderboard at snapshot |
|---|---|---|---|---:|---:|---:|---:|---|
| 937555 | 2026-09-21-E045.zip | 2026-09-21 22:37:10.711224 +09:00 | Finished | 0.6433333333 | 0.5200000000 | 0.4900000000 | 0.9200000000 | false |

All four released values equal E041 ID 933094 in this snapshot. Keep the
existing unresolved/parked disposition; no exact-zero effect or identical
hosted predictions follow. No re-fit, retry, TEST promotion or S3 resumption.

[Complete score ledger](../SCORES.md) and [sanitized source](../hosted-scores/2026-09-27.json).
All score precision fields are 2. Failed attempts have no scores; never substitute zero.
