# Observed gated-household channel: bounded source scout

Date:2026-09-24. Documentation research only; no respondent download, adapter,
score, fitted model, account registration or competition-data access.

## Candidate and verified facts

The US Census Bureau publishes2023 SIPP survey microdata in downloadable SAS,
Stata and delimited formats, with a data dictionary and input examples. Its
public availability makes a local observed-data channel worth auditing; it
does not establish similarity to humanitarian surveys. [Official release](https://www.census.gov/data/datasets/2023/demo/sipp/2023-data.html).

The primary file has person-month records, potentially12 per person. Household
variables are copied across members and person variables across months. Some
published fields are recodes rather than direct questionnaire answers. These
features create genuine dependence but also trivial leakage if handled badly.
[2023 users' guide, chapter3](https://www2.census.gov/programs-surveys/sipp/tech-documentation/methodology/2023_SIPP_Users_Guide_AUG26.pdf).

The2023 dictionary supplies per-variable universes and status flags, including
not-in-universe, reported, and several forms of imputation. Its introductory
missing-code note specifically describes internal data, so public-file missing
values must be checked rather than assumed to have identical encoding. Some
universes combine several conditions. [2023 dictionary](https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2023/2023_SIPP_Data_Dictionary.pdf).

## Why this is a candidate, not validation already obtained

Inference: documented households and universes could exercise dependence and
conditional questions without inserting them into Adult or a simulator.
US income/program-participation data differ substantially from ERPIS refugees,
CATI collection, approximate gates and the hidden GIVEN selection. Successful
SIPP learning would remain a proxy result, not a UNHCR upper bound or forecast.
Public recoding/imputation can create additional artifacts unrelated to E041.

## Next bounded audit before any model experiment

1. Freeze a release/source checksum and inspect a bounded metadata/data extract.
   Confirm public missing/sentinel/refusal codes and a small documented question
   block whose universes can be represented truthfully. Never invent a gate to
   force the channel to resemble UNHCR; reject unsupported universe mappings.
2. Keep one prespecified reference month and one row per person. Avoid training
   on another month of the same person's held-out answers. Anonymized record
   keys serve split/provenance checks only, never GIVEN inputs or donor scores.
3. Prespecify both respondent-held-out and household-held-out evaluation to
   separate same-household evidence from broader prediction. A household split
   tests robustness; it need not mimic the competition's respondent split.
4. Freeze GIVEN/PREDICT definitions and exclude algebraic target recodes,
   imputation flags that expose the target, direct copies and answer-derived
   features. Record natural concentration/bucket occupancy before selecting
   any method. Do not subset rows for a favorable model result.
5. Require a specific named repair and a valid coupled oracle before fitting
   its estimator. In-sample optimism alone does not identify a useful repair.
   Keep model selection and audit roles separate from calibration.

The immediate deliverable of that audit is an accepted/rejected channel with
its encoding/partition provenance, not another submission. No new experiment
ID or score expectation is assigned here. This provides a concrete alternative
to more Adult seeds or reliance on E054's weak reporting resolution.
