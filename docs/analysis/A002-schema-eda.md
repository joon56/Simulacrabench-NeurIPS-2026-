# A002 — schema EDA (structure + domain mapping)
date-started: 2026-08-27
status: in-progress
relates-to: E003, E004, A001

## Goal

Extract everything the four schemas (the only REAL information available
locally) say that bears on modelling: item taxonomy, option-cardinality /
U-leverage structure, gate network topology, stratum candidates for E004,
and a mapping of A001's 15 pre-registered domain expectations onto concrete
schema items — each mapping tagged consistent / surprising.

Constraint honored: sandbox CONTENT is random — any content-level analysis
is pipeline rehearsal only and is tagged as such. Real-data conclusions come
only from schema structure + A001 published sources.

## Attempt log (chronological, append-only — dead ends stay)

### v1 — 2026-08-27: structural pass, notebooks/a002_schema_eda.py
- Parse all four schemas (utf-8 — cp949 default bit on first try, dead end
  recorded: always `open(..., encoding="utf-8")` on this machine; same for
  stdout on Windows console).
- Outputs: per-instrument class counts, cardinality/U decomposition, gate
  network stats (parent class split, chain depth, fan-out), stratum
  candidate table (low-cardinality GIVEN), item-type heuristic taxonomy.
- Report artifact: docs/analysis/A002-outputs/structural-report.md
- Verdict: kept. dataset.description fields turned out to carry far more
  than expected — fieldwork windows, round sizes, preprocessing rules.

### v2 — 2026-08-27: targeted item-text extraction (inline, not scripted)
- Dumped: unhcr s3_11 + its direct children (s7a/s7b families), all 19
  unicef items with gates and full option lists, wb sc_* cognitive battery
  + EXCLUDE list + group/employmentStatus gate families.
- Purpose: map A001's 15 pre-registered expectations onto concrete items.
- Verdict: kept; three A001 expectations REVISED by schema evidence (below).

## Findings

1. **[surprising → A001 exp. 1 REVISED] Both unhcr rounds are inside ONE
   fieldwork window (May–June 2025, 67 interview dates).** Round 1 = 6,316
   (exactly eRPIS wave 1), round 2 = 4,033 — but round 2 is NOT the Oct–Nov
   2025 wave 2: the description places both round labels in the same
   two-month window. Consequences: (a) NO temporal decay between rounds —
   expect round marginals nearly identical up to sampling; (b) the published
   eRPIS Sept-2025 tables describe EXACTLY this fieldwork → they are direct
   priors for BOTH rounds, stronger than we assumed. Evidence: schema
   dataset.description (primary, overrides A001 inference). Also: no panel
   key exists in the file — rounds are genuinely unlinkable.
2. **[consistent] unhcr s3_11 = eRPIS Q1 verbatim** ("intend to return...
   next 12 months", No/Yes/DK) — ungated root with 73 direct children
   (s7a reasons multi-select if Yes, s7b if No, s7c if DK), chains to
   depth 4, 155/156 gate parents PREDICT. Published per-country marginal
   for exactly this item (Yes: Eg 29 / Iq 4 / Jo 22 / Lb 14; regional
   18/76/6) — predicting s3_11 well via prior+stratum unlocks the entire
   cascade. E004's real target is now precisely identified.
3. **[consistent] unhcr composition favors calibrated binaries**: 144/213
   scored items binary-ish, U = 1.2618 (lowest of the three) → per-cell log
   gains/losses amplified in skill units; 132k cells. Socio-economic
   one-sided marginals from A001 (employed 96%, debt 86%) apply to many.
4. **[consistent, sharpened] unicef = COVID-era faith/vaccine survey**, 10
   countries named (Brazil, Egypt, Guatemala, Iraq, Kenya, Mali, Nepal,
   Nigeria, Pakistan, Zambia — LMIC-heavy per WGM exp. 2). Gate structure
   nearly deterministic: 6/8 gates on GIVEN parents (Q13 child-under-5 →
   Q14–Q18; Country → Q01 age, Egypt excluded), only Q08→Q09/Q10 on a
   PREDICT parent. WGM expectations map cleanly: Q11/Q15 (influencer:
   health worker vs religious leader — expect health-worker-modal but note
   the sample is religion-affiliated, could shift), Q14 (importance —
   expect Very-Important-modal ~90%+). A001 WGM-2018-as-source demoted to
   "wording ancestor"; COVID-era UNICEF study with this exact country list
   is the v2 research target.
5. **[surprising → A001 exp. revision] wb country conditioning is weak,
   not dominant**: country recorded for only 38.8% of rows (SA 80.4% of
   those); 'Not answered' is a level. A001 exp. "country-first for
   cognitive scores" does not transfer to this instrument — better stratum
   candidates: user.employmentStatus (card 9, GIVEN, gates 6 items
   complementarily — Laajaj-Macours structure confirmed verbatim),
   group (feedback RCT arm, card 5, GIVEN, gates 19 PREDICT items
   deterministically), user.hadJob, user.age, user.educationLevel.
6. **[consistent] wb = impact-evaluation composite confirmed**: full
   psychometric battery as banded subscale scores (Big Five/GM/PP/EI/RIASEC
   all K=7), cognitive tasks (Corsi K=8, digit span f/b K=15, matrices,
   CPT, TMT, mirror tracing, BRET risk task), feedback-arm randomisation
   (1,229 subsample) + 6-month tracer (471, tr_* items). EXCLUDE list =
   mostly raw duplicates of banded scores (leak-prevention), confirming
   bands are the modelling unit. Southern-Africa online single-session.
7. **U decomposition**: unicef U=1.5620 (12 items, K 2–8), wb U=2.0184
   (76 items, K up to 26 — sector items K=25/26 are the headroom monsters),
   unhcr U=1.2618. wb's wide-K items (sectors, planned courses) are where
   a good prior buys most raw log-score per cell.
8. **Pipeline notes for the predictor**: unhcr round-2-only sentinel
   families (6.4/6.6/6.11/7A.7/7B.1, 59 items) confirmed in description —
   wave is GIVEN, so sentinel-rate-by-wave is directly conditionable;
   s3_5_family_in_syria_lbl is ungated with 'Not recorded' level;
   GATE_CORRECTIONS.md (6 problem gates) still absent from kit.

### v3 — 2026-08-27: sandbox structural verification (pipeline rehearsal only)
- Role splits match schema["split"] exactly on all three real sandboxes;
  TEST rows present locally (they will NOT ship in phase-1 real data).
- Gate-consistency on visible TRAIN rows: 0 violations out of 119,080 /
  155,850 / 1,291,524 checked parent-child pairs (unicef/wb/unhcr).
- Verdict: kept. Confirms with numbers that sandbox gates are EXACT —
  unhcr's real approximate-gate failure mode (agreement median 0.83) is
  structurally invisible locally; E003's violation simulation is the only
  local probe. No content conclusions drawn (sandbox content is random).

## Artifacts

- notebooks/a002_schema_eda.py — reproducible; regenerates the report.
- docs/analysis/A002-outputs/structural-report.md
- v2/v3 inline dumps reproducible from the schema JSONs (commands logged in
  session; structural report carries the durable numbers).

## Feeds into

- E004 stratum rule + Domain check pre-registration; E003 agreement-weight
  design (which items/families); U-leverage informs where calibration
  effort pays.
