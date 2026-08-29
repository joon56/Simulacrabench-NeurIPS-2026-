# A003 — eRPIS published marginals → machine-readable prior CSV
date-started: 2026-08-29
status: in-progress
relates-to: A001, E007 (planned prior-blended model)

## Goal

Turn the A001-transcribed eRPIS Sep-2025 percentage tables into a bundled
CSV (`data/priors/erpis_2025.csv`) mapped onto actual unhcr schema item
names, so a future model can use them as Dirichlet base measures. Only the
matching-fieldwork report (eRPIS Sep 2025) is used — A002 established both
competition rounds sit inside its window; the Flash Jan-2025 numbers are
deliberately excluded (different time point).

## Attempt log (chronological, append-only — dead ends stay)

### v1 — 2026-08-29: schema-name mapping + core-chain CSV
- Verified the intention chain in the schema: s3_11 (ungated root) →
  s3_12 (gated on s3_11 ∈ {No, DK}) → s3_13 (gated on s3_12 ∈ {Yes, DK})
  — matches the report's Q1 → hope-someday → within-5-years chain exactly,
  including gate directions.
- CSV rows written (49): s3_11 regional + per-country (Yes verbatim;
  No/DK split derived by applying the regional 76:6 ratio to the
  per-country remainder — marked `derived-residual-regional-ratio`);
  s3_12/s3_13 regional asked-only conditionals (verbatim); five
  s7b_1 reason items regional + per-country (housing/safety/services
  verbatim; 'employment'→livelihood and 'money'→no_resources marked
  `mapped-medium`); s4_7 work permit Yes=29 (`verbatim-partial`).
- Every row carries a `basis` column — the model layer must weight
  verbatim > derived > mapped-medium (or drop non-verbatim under a flag).

## Findings

1. The three-level intention chain maps 1:1 onto schema gates — the
   strongest possible anchor for a prior: the published conditionals are
   exactly the asked-only tables E006 already estimates. [consistent]
2. Mapping ambiguity is confined to the s7b_1 multi-select family label
   wording; core chain and safety/housing/services are unambiguous.

## Mapping TODO (for E007 session, not yet in CSV)

- s6_3_income_adequacy_lbl ← report 63/27/9/0 adequacy scale (verify
  option wording/order against schema values first).
- Day-laborer 63% (Eg 39/Iq 62/Jo 50/Lb 72) ← find the employment-type
  item (s4_16_employment_type_lbl, K=10) and the matching option label.
- Debt host 86% / debt Syria 12%, assistance UNHCR 52%/WFP 42%,
  income-varies 76%: locate exact items (s6_* family) and levels.
- HLP block per country (own property / documents / destroyed /
  inhabitable / at-risk): s3_* HLP items.
- unicef WGM microdata and STEP microdata downloads (A001 v2 targets) —
  separate priors, separate session.

## Artifacts

- `data/priors/erpis_2025.csv` (49 rows, basis-tagged, source-paged).

## Feeds into

- E007 prior-blended model: base-measure pseudo-counts per country
  (stratum cells), weight ∝ basis quality; FAQ disclosure: UNHCR eRPIS
  Sep-2025 report (public, data.unhcr.org 118532) as external data.
