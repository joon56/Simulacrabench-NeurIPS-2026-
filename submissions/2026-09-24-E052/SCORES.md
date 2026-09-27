# E052 preregistered scorecard

Registered 2026-09-24 before any hosted submission or result. Proposed entry #30.
Parent: immutable E041 (.64/.52/.49/.92 reported best). Phase1, UNHCR only.

## Intervention and limits

Keep E041 fits, donor evidence, per-item concentration-bucket lambdas and gate
agreement. First render the complete base without evidence propagation, then
apply each item's original evidence mixture once to its own final answer.
Only PREDICT-parent evidence routing changes; UNICEF/WB and structurally
unaffected heads remain raw-exact. No learned selector or new calibration.

This fixed structural control is distinct from E050's recursive lambda arms
and E051's tree mixtures. Both failed their preregistered observed oracle gates
and stopped before estimators. E052 does not reverse those stops. Its local
component oracle only bounds an optional selector between two fixed endpoints.
Flat observed Adult has no gates and cannot measure this intervention's gain.
Existing clean and household simulations measure engineering and direction;
they do not establish HSCC transfer. The inherited in-sample E041 replay remains.

Historical E025 .79 base + .10 evidence and .079 gated residual motivate this
interaction test; these do not decompose E041 or quantify recoverable headroom.
Removing useful parent evidence can hurt. Submission requires technical
qualification and is exploratory, not local adoption.

## Hosted reading arms

Planning anchor Grand .64; .65+ is a target, not a calibrated forecast.

| Hosted reading | Interpretation | Next action |
| --- | --- | --- |
| Grand >=.65 with best update | Favorable complete-pipeline reading; inspect newly visible scores. No claim that correlated evidence was the proven cause. | Preserve winning bytes; separately validate phase2 and update method before promotion. |
| Grand .64 with best update | Improvement may be below displayed Grand resolution. | Preserve winning bytes and available instrument scores. |
| Grand .64 without update | No demonstrated best improvement; small gains/losses and zero remain unresolved. | Keep E041; park E052. No blind routing-intensity grid. |
| Grand <=.63 | Adverse intervention relative to the incumbent, subject to display/noise. | Keep E041 upstream routing; reject adoption. |
| Build/runtime/schema failure | Technical failure, not an accuracy result. | Repair and revalidate; established failed-submission rule leaves slot unused. |

UNHCR-only 3*Delta Grand is approximate, resolution about .015-.03. Do not
fill unavailable instrument scores or infer activation from a flat reading.

## Local verification

Fixed-endpoint diagnostics, before production packaging:

| Channel | E041 skill | E052 skill | Delta | Changed vectors |
| --- | --- | --- | --- | --- |
| Clean UNHCR | .562462728858 | .562630019881 | +.000167291023 | 25,911/132,273 |
| Existing household seed13 | .552012531240 | .550932252799 | -.001080278441 | 58,506/180,411 |

Original E041 vectors are raw-exact in both libraries. Clean delta versus E025
is -.000318853824. Both optional component-selector oracle bounds fail .005
skill/3: clean .000055763674, household0. No selector built. No post-result
intensity changes. Household direction is adverse; clean gain is small and
below adoption. This is a fixed exploratory submission, not a validated
positive candidate or evidence that removing parent information will transfer.

34 combined library/routing/wrapper/assembly tests PASS12.03s. Independent
semantic and release reviews found no code blocker. Twenty-four independent
randomized boundary/immutability probes also passed.

Clean naturally activates the intervention, so official UNHCR source/archive
comparison tests the real active path. Structurally unaffected heads must
remain exact. Combined execution must remain below900s for all instruments.

Final release checks PASS: ZIP checker, official phase1 all3, clean no-regression
against both frozen baselines, and every raw source/archive probability.

| Instrument | Official skill | Seconds | Source parity max abs |
| --- | --- | --- | --- |
| UNICEF | .500648423071 | 43.794317007 | 0 |
| WB | .454717307363 | 108.333282232 | 0 |
| UNHCR | .562630019881 | 250.667208672 | 0 |

Combined402.794807911s <900; verifier wall416.2904894s. Local CPU,2threads;
local timing does not guarantee hosted timing. Source predict total388.3703556s.
UNICEF/WB raw-exact E041/E025. UNHCR deltas remain +.000167291023/-.000318853824,
both within .002. Actual clean active comparison verifies25,911 changed vectors,
all132,273 vectors exactly match source and preregistered diagnostic endpoint,
and nongated/GIVEN-parent boundaries remain exact. Both diagnostic manifests
rehash successfully. See verification.json and the separate
../../docs/analysis/E052-outputs/active-assembly-parity.json.

Technically qualified for fixed exploration only. E041 stays incumbent; E025
stays phase2 fallback. No external fitted data or new runtime packages bundled.

- main.py SHA256: `a77e6529012d7539ce6d519d7eb33adca99b46bc71585c79771d8d2f8a05aa2c`
- ZIP SHA256: `158f2fa1d0f153b54cdab2e8c3ae33c02de6172b0079c471f5f34c2d8014cbaa`
- Source dependency SHA256: `062d32a74adf47746c0111bc64132655c9024f82e8b0c57f1640a4ead0237822`

## Actual hosted result

User reported Grand **0.64**, **no best update**, recorded2026-09-24.
UNICEF/WB/UNHCR scores are unavailable. Submission #30 completed with a score;
this was not a failed attempt. Platform submission ID, upload time and hosted
runtime were not supplied; no independent platform fetch or agent upload.
The recording date does not infer the exact upload date from the earlier
plan to submit tomorrow.

Selected preregistered arm: **Grand .64 without update**. No demonstrated best
improvement. Small gains, losses and zero remain unresolved at display/noise
resolution; do not infer hidden UNHCR .92 or whether the intervention was active.
Keep E041 as incumbent and park E052. No blind routing-intensity grid and no
phase2 promotion; E025 remains the phase2 fallback.

This tests the fixed ancestor-evidence routing control only. It neither proves
the original routing universally optimal nor resolves A011's replay-validation
mismatch, which E052 did not change. Next research remains separately scoped
whole-pipeline held-out calibration, with its own oracle and learned validation.
All pre-registered arms, local measurements, main.py and ZIP bytes are unchanged.

## External data disclosure

E050/E051 used UCI Adult only for offline screening, not runtime data or fitted
weights in this artifact. E052 uses unchanged official/household simulations.
The intended ZIP contains main.py only and fits competition-visible rows.

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
| 942742 | 2026-09-24-E052.zip | 2026-09-24 18:41:23.995173 +09:00 | Finished | 0.6433333333 | 0.5200000000 | 0.4900000000 | 0.9200000000 | false |

All four released values equal E041 ID 933094 in this snapshot. Keep the
existing unresolved/parked disposition; no exact-zero effect or identical
hosted predictions follow. No re-fit, retry, TEST promotion or S3 resumption.

[Complete score ledger](../SCORES.md) and [sanitized source](../hosted-scores/2026-09-27.json).
All score precision fields are 2. Failed attempts have no scores; never substitute zero.
