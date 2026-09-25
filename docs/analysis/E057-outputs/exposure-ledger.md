# E057 evaluation exposure and scope

This is a UNHCR procedure/runtime engineering screen after E056, not a new
external-data or untouched-audit experiment. Frozen protocol: [registration.md](registration.md).

| Channel or role | Authorized use | Interpretation |
| --- | --- | --- |
| Public UNHCR schema | All 145 gated leaves fixed before scoring; all 17 GIVEN fields | Schema coverage only; actual asked-fit counts unknown until fit. |
| E056 oracle/selection/audit | Required existing aggregate records and source reviewed | Already consumed development evidence; no rescoring, unused-arm lookup or new audit claim. |
| E056 calibration; other Adult/SIPP roles | No response arrays, caches or new scores opened | No role reassignment, new holdout or seed search. |
| Existing synthetic TRAIN | Deterministic visible-row fit/selection/validation; later all-visible refit | Previously exposed engineering population, not independent evidence for real UNHCR. |
| Synthetic selection | Fixed grid and per-leaf 2SE guard after masked shadow predictions freeze | Selects one complete policy, without validation feedback. |
| Synthetic independent-validation role | One frozen complete policy, only if selection activates | Independent of this run's shadow fit/selection, not historically untouched data; reject all or accept all. No retuning. |
| Existing synthetic DEV | GIVEN-only inference, all instrument outputs frozen before one comparison | Already exposed engineering data; no adoption or transfer inference. |
| Existing synthetic TEST | Present in existing sandbox source; no TEST prediction/scoring in phase1 | Already exposed historically; not a new holdout. |
| Forced all-leaf alpha=.5 | Frozen refit predictions; output invariants only | Engineering fixture, never scored or substituted for selected policy. |
| Actual private DEV/TEST | No access | No claim of hidden gain, impossibility or selection. |
| Actual TRAIN, future hosted use | Selection/validation/refit inside predict only | No diagnostic telemetry or detailed-statistic encoding in submitted scores. |

Shadow base and trees receive the same frame with every non-fit PREDICT block
masked. Tree fitting uses actual asked rows only within its permitted fit role;
tree inference receives GIVEN features for every queried respondent, regardless
of their actual gate state. Independent-validation labels enter full refit only
after weights are frozen. Refit changes model distributions and is not itself
validated by the earlier shadow score.

The user authorized no new oracle here. E056's finite fitted library, data,
weights and exposure limits remain unchanged. E057 does not extend an external
oracle failure or success into a bound on the full private TEST population.

Row arrays, split positions, masked frames and complete prediction libraries
remain in ignored `external/e057/`. Tracked records contain hashes, aggregate
synthetic diagnostics and code only. Hash-verified existing E025/E041 phase1
references avoid extra baseline fits. Existing models, E056 outputs and
submission snapshots remain immutable.

S3 remains stopped. A018's selected/frozen wording is an unconfirmed review
proposal. E041 remains DEV incumbent; E025 remains the existing fallback.
No ZIP, method, TEST delivery artifact or upload is produced by this study.
