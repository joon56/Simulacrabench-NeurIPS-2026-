# E045 - Candidate union with guarded learned reranking (UNHCR only)

Status: **READY FOR ONE EXPLORATORY DEV SUBMISSION.** All required technical
checks pass; no local adoption claim. No hosted upload or result. Incumbent E041 Grand .64 /
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
E045 remains parked for adoption pending its preregistered hosted reading.

## Actual hosted result

Not submitted. No result or daily slot used by this preparation.
