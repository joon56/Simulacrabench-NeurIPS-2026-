# E047 preregistered scorecard

Registered 2026-09-22 before any hosted submission or result. Submission #28.
Parent: immutable E041 (.64/.52/.49/.92 reported best). Phase1, UNHCR only.

## Change and attribution

Keep E041 as the first-stage model and evidence generator. A section-specific
confidence model predicts a respondent-specific extra evidence share <=.5,
after all existing gate/evidence operations. Correction fit, selection and
audit respondents are excluded from shadow first-stage training. The final
E041 refit includes all visible rows. A selection guard
and separate overall audit can return exact E041. UNICEF/WB remain exact.
The final blend does not propagate again through gates.

This tests a query-adaptive final-output correction. It is not the stopped
E046 tree family or E042's constant per-item post-final correction. Confidence
features and all thresholds were registered before the E047 oracle/estimator.
The inherited E041 first-stage replay remains unchanged; the new correction
is evaluated honestly outside it. A full-data refit can change its inputs.

## Expected reading

Planning anchor: incumbent Grand .64. Target: .65+; no calibrated forecast.
Observed proxy feasible oracle skill/3 gains +.008792002 / +.008430994 do not
predict HSCC gains: oracle uses audit answers and can choose separately per
query/section. Learned results and technical checks are added below before
delivery. Exact hosted activation and probabilities will not be available.

| Hosted reading | Interpretation | Next action |
| --- | --- | --- |
| Grand >=.65 and best update | Favourable transfer of the complete correction pipeline; inspect the newly visible instrument scores. | Preserve snapshot as DEV contender; separately validate phase2 and method before adopting there. No claim every component caused the gain. |
| Grand .64 with best update | Improvement below displayed Grand resolution is possible; use any newly visible instrument values without inventing hidden precision. | Keep winning snapshot; evaluate a separately screened next mechanism. |
| Grand .64 without update | No demonstrated best improvement. Small positive/negative effects, zero and inactive selection remain unresolved. | Keep E041; park this configuration. Do not run a blind coefficient/threshold grid. |
| Grand <=.63 | Adverse pipeline reading relative to .64 reference, subject to rounding/noise. | Reject adoption, retain E041; audit transfer/refit issues before another correction. |
| Runtime/build/schema failure | Technical failure, no empirical model result and no daily slot consumed under the established rule. | Fix/revalidate the technical defect before retry; do not reinterpret as an accuracy result. |

For a completed scored UNHCR-only entry, displayed 3*Delta Grand is only an
approximate UNHCR translation (rounding/noise, roughly .015-.03 precision),
not a recovered exact instrument value. Never fill unavailable WB/UNHCR scores.

## Required local checks

Observed estimator: seed47 +.000273604 skill (descriptive interval includes0),
finances selected; seed48 exact fallback0. Audit was reused from oracle family
screening and later gates acceptance, so these are not selection-adjusted
estimates. No audit-driven settings changes. Sixteen meaningful objective,
masking, fallback and active source/assembly tests passed.

Clean source PASS: .500648423071/.454717307363/.562462728858, all raw vectors
exact E041. UNHCR delta vs E025 -.000486144847; both baselines within .002.
Source total491.1342037s (household diagnostic running concurrently). No clean
correction selected. Household source .554337041587 vs E041 .552012531240,
delta+.002324510347, sections7b/7c active;529.7275s. This is directional sim
evidence only, below the +.005 three-instrument mean adoption bar.

ZIP checker and official phase1 all3 PASS, every raw probability exactly source.

| Instrument | Official skill | Seconds | Source parity max abs |
| --- | --- | --- | --- |
| UNICEF | .500648423071 |36.547247410|0|
| WB | .454717307363 |92.483175039|0|
| UNHCR | .562462728858 |386.149091244|0|

Combined515.179513693s <900; verification wall526.7669924s. CPU-only Windows11,
torch2.13.0+cpu,2 threads. Diagnostic work overlapped part of verification;
local time is not a guarantee of hosted timing. Actual active-household
assembly also matches every probability (180411 cells, max abs0), skill
.554337041587,529.2693297s. See verification.json and
../../docs/analysis/E047-outputs/active-assembly-parity.json.

Baseline cache times are historical; reused only with matching current input
and pinned source hashes. No model adoption: clean mean delta0 versus E041,
sim mean equivalent+.000774837 below+.005. Technically ready for exploration.

- main.py SHA256: `2ffe07a845a42197aed61eafffde7af52746cd99f7f9f957f43693ed576cb57e`
- ZIP SHA256: `9c09c5abd1951c8a8f02739a92b5aca3b32027b038a1a25d7b88ea280f1a4151`
- Source dependency SHA256: `4673a4d3f3817b0a1b7b1795f0c60b8ad50b2766301c963762463457054970c8`

## Actual hosted result

User reported on 2026-09-22: **Grand .64, no best update.** Individual UNICEF,
WB and UNHCR scores are unavailable. This was a completed scored submission,
not a technical failure. Source: user report; no platform fetch, submission
ID, exact upload time or hosted runtime was provided.

Applied the preregistered **Grand .64 without update** arm: no demonstrated
best improvement; keep E041 and park this configuration. Equal rounded/noised
Grand cannot distinguish a small gain, a small loss, zero effect or inactive
hosted selection. Do not infer hidden UNHCR .92 or claim the correction was
disabled merely because clean sandbox selection rejected it.

The household sim gain and permissive observed oracle did not establish a
hosted improvement. This result neither closes every calibration method nor
justifies relaxing the selector threshold blindly. Retain E041's learned
retrieval; require a separately screened mechanism before another candidate.
E025 remains the validated phase2 fallback. Archive, code and local results
are unchanged.

## External data disclosure

Offline screening only: UCI Adult, Becker and Kohavi (1996), CC BY4.0,
https://archive.ics.uci.edu/dataset/2/adult (doi:10.24432/C5XW20), unchanged
deduplicated/coarsened protocol. No Adult records, fitted external parameters,
pretrained models or extra dependencies are bundled. Runtime fits use only
the competition-provided visible respondents and public schema.
