# A001 — background domain packet (per-instrument source studies)
date-started: 2026-08-27
status: in-progress
relates-to: E003, E004, planned RPIS-prior experiment

## Goal

For each of the three instruments, establish the background domain: what real
survey program the instrument descends from, what its published reports say
about the population and response patterns, and which published aggregate
tables could serve as real-marginal priors (disclosure per FAQ required).

Motivation: discipline rule 7 — EDA and modelling conclusions must be
checkable against subject-matter knowledge before being built upon. This
packet is the lens for the schema EDA that follows (A002, planned).

Starting knowledge (from docs/domain.md §9, recorded 2026-08-19):
- unhcr = Enhanced RPIS v1.3 (Syrian refugees, Egypt/Iraq/Jordan/Lebanon,
  2 CATI rounds); published RPIS series since 2017, 9th round 2024, flash
  Feb 2025, ERPIS report Sept 2025 with matching fieldwork window.
- unicef v1.1 "Faith & Immunisation", 10 countries — source study NOT yet
  identified (study-guide item 16).
- world_bank "Skills Assessment", youth job-seekers, 3 countries — countries
  and source program NOT yet identified (study-guide item 17).

## Attempt log (chronological, append-only — dead ends stay)

### v1 — 2026-08-27: delegated web research (research skill / background agent)
- Brief: three threads — (1) UNHCR RPIS/ERPIS report series: exact titles,
  publication venue (UNHCR data portal / ReliefWeb), which items have
  published aggregate distributions (return intention, socio-economic
  conditions), per-country/per-round variation worth pre-registering;
  (2) identify UNICEF faith-and-immunisation source study (candidate space:
  Wellcome Global Monitor, UNICEF/faith-leader vaccine-confidence surveys);
  (3) identify World Bank youth skills program (candidate space: STEP Skills
  Measurement, S4YE surveys) and plausible country triple.
- Method actually used by the agent: web search + full-PDF text extraction of
  four primary documents (Flash RPIS Feb 2025, eRPIS report Sep 2025, Wellcome
  Global Monitor 2018 full report, STEP 2014 methodology paper); percentages
  transcribed from the PDFs, not secondary write-ups; unverifiable claims
  explicitly flagged.
- Output: `A001-sources/findings.md` (per-thread program ID + confidence,
  report URL catalogue, transcribed marginal tables, 5 pre-registrable
  expectations each = 15 total).
- Verdict: kept. Thread 1 near-certain; threads 2–3 partially identified with
  honest mismatch flags (see findings 4–5 below).

### v2 — 2026-08-27: cross-check against schema descriptions (with A002)
- The 08-19 kit's dataset.description fields are primary evidence the v1 web
  research did not use. Cross-checking revised three v1 conclusions:
  - **Expectation 1 (between-round decay) WITHDRAWN**: both competition
    rounds sit inside the single May–June 2025 eRPIS wave-1 window (round 2
    n=4,033 is NOT the Oct–Nov wave 2). Replacement expectation: round
    marginals near-identical; eRPIS Sept-2025 published tables are direct
    priors for BOTH rounds. (A002 finding 1.)
  - **Thread 2 reframed**: instrument is a COVID-era vaccine/faith survey
    with a named 10-country list (Brazil, Egypt, Guatemala, Iraq, Kenya,
    Mali, Nepal, Nigeria, Pakistan, Zambia); WGM 2018 demoted to wording
    ancestor. v3 research target: UNICEF/partner COVID vaccine-demand faith
    study with exactly these countries. (A002 finding 4.)
  - **Thread 3 expectation 5 (country-first) revised for wb**: country is
    recorded for only 38.8% of rows; stratum candidates are
    employmentStatus / group (RCT arm) / hadJob instead. (A002 finding 5.)
- Verdict: kept; demonstrates why rule 7 cuts both ways — the domain packet
  itself must be validated against the instrument evidence.

## Findings

1. **unhcr = UNHCR×World Bank eRPIS, near-certain.** Wave 1 = exactly 6,316
   CATI interviews, 25 May–5 Jul 2025 (report 11 Sep 2025); wave 2 fielded
   Oct–Nov 2025 (n=4,033 plausible, unverified). Real survey is a two-wave
   PANEL; the competition treats rounds as independent cross-sections —
   real wave-2 marginals will correlate strongly with wave 1. [consistent]
2. **The Assad-fall discontinuity is BEFORE the competition's data window.**
   12-month return intention: 1.7% (Apr 2024) → 27% (Jan 2025) → 18%
   (Jun 2025); both competition rounds are post-fall. Between-round movement
   is a DECAY (Jordan 40%→22%), not a jump. Without this check we would
   plausibly have encoded a huge round-2 jump — exactly the numbers-without-
   domain failure rule 7 exists for. [surprising vs naive assumption →
   evidence: primary UNHCR tables, adopted]
3. **Real per-country per-round marginals for the exact gated Q1→Q2→Q3
   return-intention chain are published** (transcribed in findings.md):
   country ordering Egypt ≥ Jordan > Lebanon > Iraq stable; "hope one day"
   ~80% stable while 12-month moves; socio-economic marginals extreme
   (main-earner employed 96%, host debt 77–86%). No microdata/Excel — PDF
   tables only. Direct Dirichlet-prior material. [consistent]
4. **unicef ≈ Wellcome Global Monitor 2018 item content** (VCI wording,
   heard-of-vaccine screener gate, religious-leader trust option,
   religion-vs-science module) — MEDIUM-HIGH on content, LOW on framing;
   10-country list unverifiable, possibly synthetic. **WGM 2018 microdata is
   free CSV (CC-BY) — best machine-readable prior of all three.** Global
   marginals: important 92 > effective 84 > safe 79 (ordering holds in every
   region); religious-leader trust ~2%. [consistent]
5. **world_bank = STEP-shaped composite, no exact real survey.** STEP matches
   ownership/length/skip-logic (public microdata per country), but STEP's
   cognitive test is PIAAC reading literacy, NOT digit span/Corsi — those
   live in WB impact-evaluation batteries (Laajaj & Macours JHR 2021:
   cognitive items internally consistent, self-reports acquiescence-skewed).
   Country triple unverified — do not assume. [surprising (no single source
   study) → treat as composite, priors per component]
6. 15 pre-registrable expectations catalogued in findings.md §(d) of each
   thread — these become the Domain check pre-registrations for A002 EDA and
   E004.

## Artifacts

- `docs/analysis/A001-sources/findings.md` — full cited findings, transcribed
  marginal tables, URL catalogue.

## Feeds into

- A002 schema EDA (planned): the 15 expectations are the domain lens.
- E004 Domain check pre-registration (country-first conditioning is now
  domain-backed for all three instruments: RPIS country ordering, WGM
  screener-gate asymmetry, STEP country-dominant cognitive scores).
- RPIS-prior experiment: transcribed PDF tables → bundled CSV priors.
  WGM 2018 / STEP microdata downloads are candidate follow-ups (v2).
- FAQ disclosure list (external data used): eRPIS/Flash RPIS reports,
  WGM 2018 (CC-BY), STEP public-use microdata, Laajaj & Macours replication
  data — disclose whichever actually enter the model.
