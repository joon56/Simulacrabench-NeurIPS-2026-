# E041 external observed-data oracle

This is an external method screen on observed census rows, **not an HSCC
forecast, trained E041 gain, or evidence of household recurrence**.

## Source and lawful access

Becker, B. & Kohavi, R. (1996). *Adult*. UCI Machine Learning Repository.
[Dataset and license](https://archive.ics.uci.edu/dataset/2/adult),
[DOI](https://doi.org/10.24432/C5XW20),
[download](https://archive.ics.uci.edu/static/public/2/adult.zip).
UCI states CC BY 4.0 and identifies these as records extracted from the
1994 Census database. Page/license checked and archive downloaded on the
execution environment's date, 2026-09-18. No login or restricted-data access.
No synthetic observations, target correlations, or duplicates were injected.

Archive extracted to `tmp/e041/adult/`; only `adult.data` is used.
`tmp/.gitignore` excludes the raw files. Source `adult.data` SHA-256:
`5b00264637dbfec36bdeaab5676b0b309ff9eb788d63554ca0a249491c86603d`.
Redistribution/credit follows [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Fixed schema and split

GIVEN: age bands (17–24, 25–34, 35–44, 45–54, 55–64, 65+), education,
race, sex, native-country. Targets comprise three sections:

- Family: marital-status and relationship.
- Employment: workclass, occupation, hours-per-week bands (1–34, 35–40,
  41–49, 50+).
- Finances: income above $50K, positive capital-gain, positive capital-loss.

Raw age, education-num, fnlwgt, hours-per-week, capital-gain and capital-loss
are excluded. No raw copy of a target is GIVEN. Missing `?` is an ordinary
category. No gates are invented. Target category sets are schema metadata;
no held-out frequency is used. Known sex/race/country fields are used only
for this research evaluation, not decisions about individuals.

Remove identical **modeled full profiles** before sampling: 32,561 source
rows become 19,561 distinct profiles. This includes distinct people whose
coarsened answers happen to coincide, so the resulting prevalence is not a
population-representative Adult estimate. It deliberately removes exact
profile repetition as an explanation for the result. Randomly sample 5,000
profiles; order defines 3,000 TRAIN/reference, 1,000 selection, 1,000 evaluation.
Seeds 41 and 42 are fixed-protocol replications on the same source dataset.
Source line IDs are identity checks only, never features.

## Methods and exclusion checks

Baseline: one categorical logistic regression per target, one-hot GIVEN,
`C=1`, 400 maximum iterations, 1% smoothed TRAIN-marginal backoff. All fits
exclude both selection and evaluation rows. Retrieval ranks TRAIN references
by the sum of exact GIVEN agreements weighted by negative log TRAIN category
frequency (add-one smoothing). Keep 32 candidates; stable TRAIN-order ties.
The full selection/evaluation sets are absent from the reference bank.

Fixed global retrieval selects one shared K in {8,16,32} and temperature in
{0.5,2,8} on selection log score. The global blend also selects one shared
retrieval weight in {0,.25,.5,.75,1}. Selection and evaluation are separate.

Two **label-informed, pre-estimator oracles** use frozen candidates/base:

1. Policy oracle chooses one of those 45 complete policies for each query
   section. The same K, temperature and blend applies to every section item.
2. Convex oracle assigns one simplex of weights over all 32 donors plus base
   for each query section. Each donor supplies its complete section answers.
   No independent correct donor is selected per cell. Mixture EM optimizes
   section mean log probability; its first-order concave dual gap certifies
   the remaining optimization error.

Both oracles intentionally see evaluation targets. Their gain is candidate
family headroom, **not attainable prediction accuracy**. Small sections with
2–3 targets make the convex bound especially permissive. A learned GIVEN-only
selector still needs independent evaluation. Adult has no approximate survey
gates, so this does not validate that part of the competition pipeline.

Assertions check split identity exclusion, unique profiles, simplex weights,
floor compliance, and that masking every query target preserves candidates,
retrieval scores and baseline predictions exactly. Official floor mixing
uses `src.eval.logloss.floor_mix`. Log score pools eight equally observed
targets; `U=1.51358503744`, `skill=1+log_score/U`. Dividing a skill difference
by three is only an arithmetic proxy, not a Grand Prize prediction.

## Measurements

| Seed / method | Log score | Skill | Skill gain vs selected global blend | Gain / 3 |
|---|---:|---:|---:|---:|
| 41 logistic / selected blend | -1.009983 | .332721 | .000000 | .000000 |
| 41 pure global retrieval | -1.128955 | .254118 | -.078603 | -.026201 |
| 41 section policy oracle | -.872032 | .423864 | +.091142 | +.030381 |
| 41 section convex oracle | -.211992 | .859941 | +.527219 | +.175740 |
| 42 logistic / selected blend | -1.027553 | .321113 | .000000 | .000000 |
| 42 pure global retrieval | -1.145160 | .243412 | -.077701 | -.025900 |
| 42 section policy oracle | -.894204 | .409215 | +.088101 | +.029367 |
| 42 section convex oracle | -.234197 | .845270 | +.524157 | +.174719 |

Both global selectors chose retrieval weight zero. Mean convex certification
gaps are 2.733e-9 and 2.106e-7 nats. Single-process benchmark times were
2.72 and 3.80 seconds, at most two numerical-library threads. These timings
cover this small external script only, not E041 production runtime.

Earlier first screen used 64 candidates: seed41 policy/convex skills
.425634/.925834. Candidate bank was then narrowed to 32 to match planned
E041 scope, before training an estimator. Its permissive convex result was
not used to predict a competition gain; initial raw JSON retained in
`tmp/e041/e041-external-oracle-seed41-k64-initial.json`.

Domain check: observed census demographics and work/finance answers permit
conditional prediction; source provenance supports their reality. Nothing
here establishes refugee-survey structure or household duplication. Positive
oracle gap on both splits permits testing a supervised matcher; poorer
fixed retrieval and zero selected weight show that useful weighting has
**not** yet been learned.

Reproduce from repository root after downloading the source:

```powershell
.venv/Scripts/python.exe tests/e041_external.py
.venv/Scripts/python.exe tests/e041_external.py --seed 42 --output docs/analysis/A008-outputs/e041-external-oracle-seed42.json
```

Full results and schema: `e041-external-oracle.json` and
`e041-external-oracle-seed42.json`. No production model, status, experiment
record or daily log is modified by this helper.
