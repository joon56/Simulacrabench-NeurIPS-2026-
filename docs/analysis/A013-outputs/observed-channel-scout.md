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

## Follow-up: concrete metadata triage, 2026-09-24

Official dictionary checked again, printed pages20,35-41,1135-1141:
EAWBRENT depends on EAWBMORT; EFOOD4 on EFOOD3; EFOOD5/6 use several food
answers. These are household fields. Decision: do not use their person-row
copies as the primary evidence for a respondent-level calibration improvement.
A separate household-unit analysis could be valid but tests a different task.

The person-level EHREAS_DT/BIR/OS/NST/OTH/COR block is restricted to THOSPNIT
at least1. This is a concrete candidate for auditing a naturally gated block.
AHREASON and topcoding summaries are audit metadata, not proposed predictors.
This is dictionary-level suitability only: public missing encoding, counts,
recoding, temporal duplication and usable GIVEN inputs are still unverified.
No data extract, accepted validation channel, oracle or candidate exists yet.
[Dictionary](https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2023/2023_SIPP_Data_Dictionary.pdf).

Immediate sequence: inspect a bounded public extract without scoring models;
freeze one reference month, whole-person and household split keys, inputs and
all natural output levels; decide whether the block can test coupled routing
without fabricated sentinels. If it cannot, reject this channel rather than
construct favorable gates. If it can, preregister the exact recursive family
and its oracle before estimator fitting. Restrict the initial suitability
audit to one work session; do not make open-ended dataset hunting a prerequisite
for every future candidate. Metadata screening is now complete; data audit
remains the next executable deliverable.
