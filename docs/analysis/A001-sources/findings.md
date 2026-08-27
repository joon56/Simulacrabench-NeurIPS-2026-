# A001 - Primary-source identification of the three HSCC instruments

Research date: 2026-08-27. All claims cite the owning primary source (data.unhcr.org / unhcr.org / ReliefWeb mirror of UNHCR / wellcome.org / worldbank.org / microdata.worldbank.org / peer-reviewed). Anything not confirmed against a primary source is explicitly marked **unverified**.

Method note: the Flash RPIS (Feb 2025), the eRPIS report (Sep 2025), the Wellcome Global Monitor 2018 full report, and the STEP 2014 methodology paper were downloaded and read in full (PDF text extraction); percentages below are transcribed from those documents, not from secondary write-ups.

---

## Thread 1 - UNHCR RPIS / ERPIS (Syrian refugees, Egypt-Iraq-Jordan-Lebanon)

### (a) Identified program - confidence: HIGH (near-certain)

The competition's "UNHCR ERPIS v1.3" maps onto UNHCR's **Enhanced Refugee Perceptions and Intentions Survey (eRPIS)**, a UNHCR x World Bank joint CATI (phone) panel survey of Syrian refugees in Egypt, Iraq, Jordan, Lebanon, successor to the RPIS series run since 2017. The match is exact on: name ("Enhanced RPIS"), mode (phone), countries (4), population (Syrian refugees), and **wave-1 sample size 6,316** = the competition's first round. Wave 2 (planned Oct-Nov 2025) plausibly supplies the competition's ~4,033 second round - **the 4,033 figure itself is unverified** (no public wave-2 findings report found as of 2026-08-27; only a wave-2 methodology note, per search results dated 26 Apr 2026).

- eRPIS wave 1: **6,316 refugees interviewed by phone, 25 May - 5 Jul 2025**, representative at country and regional level; first-time panel design recontacting households from prior socio-economic assessments (VASyR 2024 Lebanon, VAF 2023 Jordan, SEVAT 2022 Iraq, Egypt Vulnerability Assessment 2024); World Bank partnership; data collection by NAMA Strategic Intelligence Solutions. Source: eRPIS report pp. 3, 8, 18 (https://data.unhcr.org/en/documents/details/118532).
- The competition treats "2 CATI rounds as independent cross-sections" - the real eRPIS is a two-wave **panel** (same households). Deliberate simplification worth remembering: real wave-2 marginals will be strongly correlated with wave 1.

### (b) Key reports - titles, dates, URLs (series, newest first)

| Report | Fieldwork | Published | URL |
|---|---|---|---|
| eRPIS wave 2 Methodology Note | Oct-Nov 2025 (planned) | 26 Apr 2026 | on data.unhcr.org - **direct URL unverified** (found only via search summary) |
| **Enhanced Regional Survey on Syrian Refugees' Perceptions and Intentions on Return to Syria** (eRPIS wave 1), Sep 2025 | 25 May - 5 Jul 2025, n=6,316 | 11 Sep 2025 | https://data.unhcr.org/en/documents/details/118532 - PDF: https://data.unhcr.org/en/documents/download/118532 |
| ERPIS Methodology Note (online appendix: sampling, weighting, panel design) | - | 9 Sep 2025 | https://data.unhcr.org/en/documents/download/118503 |
| **Flash Regional Survey on Syrian Refugees' Perceptions and Intentions on Return to Syria** | Jan 2025 (4,500 contacted, n=3,368 reached) | 6 Feb 2025 | https://data.unhcr.org/en/documents/details/114221 - https://www.unhcr.org/media/flash-regional-survey-syrian-refugees-perceptions-and-intentions-return-syria - mirror: https://www.3rpsyriacrisis.org/wp-content/uploads/2025/02/UNHCR_Flash_Intention_Survey2025.pdf |
| **Ninth Regional Survey (RPIS)**, Jun 2024 | Apr-May 2024, n=3,266 | 30 Jun 2024 | https://data.unhcr.org/en/documents/details/109624 - https://reliefweb.int/report/lebanon/ninth-regional-survey-syrian-refugees-perceptions-and-intentions-return-syria-rpis-egypt-iraq-jordan-lebanon-june-2024 - PDF: https://www.3rpsyriacrisis.org/wp-content/uploads/2024/07/Intention_Survey_RPIS_2024.pdf |
| Eighth Regional Survey (RPIS), 2023 | Feb 2023 | 2023 | https://data.unhcr.org/en/documents/details/100851 |
| Country-level follow-up: "UNHCR Jordan: Analysis on Returns to Syria" (Jan 40% -> Jun 22% intent in Jordan) | 2025 | 2025 | https://data.unhcr.org/fr/documents/download/121095 |

Series cadence confirmed by the Flash report's own trend charts: rounds fielded Oct/Nov-Dec 2017, Mar-Jun 2018, (Jordan: Jul & Nov 2018), Nov 2018-Feb 2019, Mar 2021, Mar 2022, Feb 2023, Mar-Apr 2024, Jan 2025 (Flash report p. 8).

### (c) Published aggregate marginals usable as priors - where and what format

**No public microdata**: searched the UNHCR Microdata Library (microdata.unhcr.org) - no RPIS/eRPIS entry exists (the Europe intentions survey, catalog 1342, is a different population). All marginals live as **percentage figures inside the PDFs** (no Excel annexes found). The two must-mine documents:

1. **Flash RPIS Feb 2025 PDF** - the richest single source. Contains, with exact answer-option wording matching a gated Q1->Q2->Q3 chain:
   - Q1 "Do you intend to return to Syria in the next 12 months?" (Yes / No / I don't know-undecided). Regional 2025: **27 / 55 / 18**; regional 2024: **1.7 / 94 / 4.3**.
   - Q2 (asked only if Q1 = No/DK) "Do you hope to return within five years?" 2025: **53 / 25 / 22**; 2024: 36.8 / 50.1 / 13.1.
   - Q3 (asked only if Q2 = No/DK) "Do you hope to return one day?" 2025: **43 / 38 / 19**; 2024: 30.2 / 55 / 14.8. Composite "overall hope": 80% (2025) vs 57% (2024).
   - Per-country Jan 2025 Q1 (Yes/No/DK): Egypt **42/41/17**, Iraq **12/75/13**, Jordan **40/47/13**, Lebanon **24/55/21**, plus the full 2017-2025 per-country time series (p. 8).
   - Barriers (multi-select, regional and per-country Eg/Iq/Jo/Lb): housing-property 61% (65/24/66/69); safety-security 53% (54/84/51/45); economic 48% (47/46/36/54); services 38% (48/26/41/40).
   - Companions: all family 69%, all+extended 18%, alone 11%; house ownership 61% yes; house status: fully destroyed 51 / partially destroyed-uninhabitable 30 / intact 9 / inhabitable 7; debt in host country 77%.
2. **eRPIS Sep 2025 PDF** - June 2025 marginals:
   - Q1 next-12-months: regional **18 / 76 / 6** (Yes/No/DK); per-country Yes: Egypt 29, Iraq 4, Jordan 22, Lebanon 14.
   - Hope one day (gated on Q1 = No/DK): 75/21/4; within 5 years (gated on hope = Yes): 83/8/9; overall hope 80/17/3. Per-country hope: Egypt 86, Iraq 55, Jordan 80, Lebanon 80.
   - Reasons not returning (regional/Eg/Iq/Jo/Lb): housing 36/24/31/36/37; employment 28/29/32/23/30; safety 12/25/12/12/11; money 7/2/9/9/6; services 6/8/8/7/5.
   - HLP block per country (own property, all documents, no document, destroyed, inhabitable, at-risk): Egypt 30/63/29/51/24/57; Iraq 36/42/51/46/14/69; Jordan 25/45/47/41/23/63; Lebanon 42/40/53/55/9/74.
   - Socio-economic block: main earner employed 96%; day laborer 63% (Eg 39, Iq 62, Jo 50, Lb 72); valid work permit 29%; income varies month-to-month 76% (51% significant); income adequacy: significant difficulty 63 / some difficulty 27 / covers-no-saving 9 / can save 0; humanitarian assistance last 3 months: UNHCR 52%, WFP 42%; debt in host country 86%, debt inside Syria 12%; safety concerns about return 77%; remittances received <10%, sent to Syria ~15%.
   - Demographics: 37% female respondents, 72% heads of household, 85% households with children, 28% single caregivers, 14% female-headed.

These map almost one-to-one onto the competition's return-intention branches (the three overlapping s3_11 branches = the Q1/Q2/Q3 skip chain) and socio-economic items - directly usable as per-country per-round Dirichlet priors.

### (d) Pre-registrable domain expectations (Thread 1)

1. **The Assad-fall discontinuity sits between the 2024 round and everything after - NOT between the two competition rounds.** Both eRPIS waves are post-Dec-2024. 12-month intention: 1.7% (Apr-May 2024) -> 27% (Jan 2025) -> 18% (Jun 2025). If the competition's two rounds are eRPIS waves 1 and 2, expect the later round's "yes" share *lower or similar* (intenders progressively leave the frame - Jordan fell 40% -> 22% between Jan and Jun 2025), not a dramatic jump. Sources: Flash RPIS p. 5; eRPIS p. 8; Jordan analysis https://data.unhcr.org/fr/documents/download/121095.
2. **Country ordering of 12-month return intention is stable: Egypt >= Jordan > Lebanon > Iraq.** Jan 2025: 42/40/24/12; Jun 2025: 29/22/14/4. Iraq is always the floor (respondents mostly originate from insecure NE Syria). Sources: Flash RPIS pp. 6, 8; eRPIS p. 8.
3. **"Hope to return one day" is high and stable (~80% regional; Egypt 86, Jordan/Lebanon 80, Iraq 55)** even while 12-month intention moves - long-horizon items get confident priors, short-horizon items hedged per round. Sources: eRPIS pp. 4, 9; Flash RPIS p. 5.
4. **Gated follow-ups carry most of the mass through the skip chain**: ~76-82% of respondents flow into the "hope" follow-ups; conversely items asked only of intending returnees (destination, companions) have ~18-27% eligibility. Within those: place of origin 85-88%, all family members 87-93%. Sources: Flash RPIS pp. 11-12; eRPIS pp. 5, 9.
5. **Socio-economic marginals are extreme, not uniform**: main-earner employment ~96%, day-laborer modal (63%), work permit 29%, host-country debt 77-86%, "significant difficulty meeting needs" 63%, property destroyed/damaged among owners 81-87%. Majority-class prediction at 0.6-0.9 confidence on these items should beat uniform by a wide margin. Sources: eRPIS pp. 5, 13-17; Flash RPIS pp. 4, 10.

---

## Thread 2 - UNICEF "Faith & Immunisation"

### (a) Identified source study - confidence: MEDIUM-HIGH on item content, LOW on framing

Best match: **Wellcome Global Monitor 2018** (Wellcome Trust x Gallup World Poll; >140,000 respondents, 144 countries, fielded 2018) - the only large multi-country primary study combining in one instrument: (i) vaccine attitude items (safety/effectiveness/importance, 5-point agree scale, Vaccine Confidence Project wording), (ii) trust-in-religious-leader-for-health-advice as an answer option, (iii) a religion-vs-science module, and (iv) a heard-of-vaccine screener + parent screener producing exactly the kind of gating the competition instrument has (19 items / 8 gated). Report: https://wellcome.org/reports/wellcome-global-monitor/2018 (full 132-page PDF read).

Caveats, stated honestly:
- WGM samples ~1,000 per country; the competition's 10 countries x ~2,000 (19,846 rows) matches no WGM configuration. The 10-country list is **unverified / not identifiable** from public sources - plausibly a fictional subset or synthetic expansion.
- "UNICEF" branding: UNICEF has no public multi-country *survey* named "Faith & Immunisation". UNICEF faith work is programmatic (faith-leader engagement, e.g. https://www.unicefusa.org/stories/bringing-faith-community-together-global-vaccine-equity); UNICEF's vaccine-confidence flagship is *State of the World's Children 2023: For every child, vaccination* (https://www.unicef.org/eca/reports/sowc2023-eca), which charts VCP/WGM-style confidence data. The WGM vaccine items are explicitly "based on the questions asked in the Vaccine Confidence Project" (WGM 2018 report p. 107) - expect the instrument's items to look like WGM/VCI regardless of the UNICEF label.
- WGM 2020 (2nd wave, 113 countries, COVID-era) is the fallback if wording looks pandemic-era; both waves catalogued at Princeton DSS: https://dss.princeton.edu/catalog/resource6001.

### (b) Key reports / URLs

- WGM 2018 full report (incl. full questionnaire, pp. 129-130): https://wellcome.org/reports/wellcome-global-monitor/2018 - Chapter 5 "Attitudes to vaccines": https://wellcome.org/insights/reports/wellcome-global-monitor/2018/chapter-5-attitudes-vaccines
- Questionnaire wording (verified from report pp. 129-130): Q20 trust-most for medical/health advice {family-friends, doctor-nurse, religious leader, famous person, traditional healer, none, DK, Ref}; Q23 heard-of-vaccine screener {Yes/No/DK/Ref} - **gates Q24-Q26**; Q24/25/26 "Vaccines are important for children to have / are safe / are effective" {Strongly agree, Somewhat agree, Neither, Somewhat disagree, Strongly disagree, DK, Ref - administered as agree/disagree then intensity probe}; religion module: "Has science ever disagreed with the teachings of your religion?" then "When science disagrees with the teachings of your religion, which do you believe?" {Science / Teachings of your religion / It depends} - gated on religious identification.

### (c) Published marginals usable as priors

- **Full microdata is free and machine-readable**: WGM 2018 individual-level dataset (CSV/SPSS) + country crosstab tables downloadable from the report page (https://wellcome.org/reports/wellcome-global-monitor/2018), CC-BY; also archived at UK Data Service (2018 + 2020 waves; see https://dss.princeton.edu/catalog/resource6001). This is the single best machine-readable prior source of all three threads - per-country full response distributions for every item including DK/Refused shares.
- Report-level global marginals (WGM 2018 ch. 3-5): vaccines safe **79% agree / 7% disagree / 11% neither / 3% DK**; effective **84% agree (63 strongly + 21 somewhat) / 5% disagree**; important for children **92% agree**; heard of vaccine 89% yes (Southern Africa only 44% - huge screener-gate effect); parents reporting children vaccinated 92 / 6 / 2; trust-most for health advice: doctor-nurse 73, family-friends 14, religious leader 2, traditional healer 3, famous person 2; religion-vs-science (among religious with perceived conflict): religion 55 / science 29 / depends 13.

### (d) Pre-registrable domain expectations (Thread 2)

1. **Importance > effectiveness > safety, everywhere.** Agreement that vaccines are important for children (92% global) exceeds effectiveness (84%) exceeds safety (79%) in every WGM region - the ordering held even in Eastern Europe (80/65/50). Expect the same per-country ordering in the competition data. Source: WGM 2018 ch. 5 pp. 109-110, 119.
2. **"Strongly agree" is modal in LMICs; scepticism concentrates in high-income/European populations.** Safety strongly-agree: South Asia 85%, Western Africa 75%, vs Western Europe 36% (France: 33% *disagree* safe - world max). If the 10 countries are LMICs (UNICEF framing), skew priors hard toward the agree end. Source: WGM 2018 pp. 110, 114.
3. **Trust-in-religious-leader for health advice is a minority option everywhere** (global 2%; regional max ~5-8%, Central/Western Africa); doctor/nurse dominates (65-89% by region). A "whom do you trust most" item should put >=60% mass on health workers in every country. Source: WGM 2018 ch. 3 pp. 70-71.
4. **Religion beats science in stated conflict, in LMICs**: religion-over-science shares: North Africa 87%, Western Africa 84%, Eastern Africa 80%, Southeast Asia 76% vs Western Europe 19%. For faith-attitude items in an LMIC country set, expect pro-religion modal responses. Source: WGM 2018 ch. 4 pp. 97-98.
5. **Screener gates are highly asymmetric by country**: "heard of a vaccine" yes ranges 44% (Southern Africa) to 98% (ANZ / N. America) - NA_GATED sentinel rates should vary across countries far more than within-country attitude marginals do. Source: WGM 2018 ch. 5 p. 109 (Chart 5.1).

---

## Thread 3 - World Bank youth "Skills Assessment"

### (a) Identified program - confidence: MEDIUM (program family), LOW (exact survey)

Best program-level match: the **World Bank STEP Skills Measurement Program** (Skills Toward Employment and Productivity): 2012-2017, 17 countries/economies, target population urban adults 15-64, long multi-module questionnaire, public microdata. Sources: https://microdata.worldbank.org/index.php/collections/step ; Pierre, Sanchez Puerta, Valerio & Rajadel (2014), *STEP Skills Measurement Surveys: Innovative Tools for Assessing Skills*, https://documents1.worldbank.org/curated/en/516741468178736065/pdf/897290NWP0P132085290B00PUBLIC001421.pdf (read in full; also https://openknowledge.worldbank.org/handle/10986/19985).

Match quality, honestly assessed:
- **Matches**: World Bank ownership; "skills assessment" of labor-market populations; long instrument (7 questionnaire modules + literacy assessment + interviewer impressions = order-100 items); heavy skip logic (employment module gates dozens of items on work status; reservation-wage / job-search items asked only of non-workers - consistent with 40 gated items); 3-country subsets with ~7k rows are arithmetically natural. Per-country n (STEP 2014 paper, Table 4 p. 62): Armenia 2,992, Bolivia 2,435, Colombia 2,617, Georgia 2,996, Ghana 2,987, Kenya 3,894, Lao PDR 2,845, Macedonia 4,009, Sri Lanka 2,989, Ukraine 2,389, Vietnam 3,405, Yunnan 2,017.
- **Mismatches**: STEP's direct cognitive assessment is a **reading-literacy test scored on the PIAAC scale (ETS design)** - *not* digit span or Corsi block (STEP 2014 paper pp. 10, 13-14, 61). STEP targets all urban adults 15-64, not specifically "youth job-seekers".
- **Where digit span / Corsi-style tests actually live in World Bank work**: skills-measurement methodology research and youth-employment impact evaluations, not STEP. Key primary source: Laajaj & Macours, *Measuring Skills in Developing Countries* (World Bank Policy Research WP 2017; J. Human Resources 56(4), 2021) - administered Raven's, forward/backward digit span and related cognitive batteries to ~900 respondents in western Kenya with a test-retest design; cognitive measures reliable and internally consistent (digit-span subconstructs among the weaker, test-retest < 0.6), technical-skill self-reports very noisy. PDF: https://jhr.uwpress.org/content/wpjhr/56/4/1254.full.pdf - WB slides: https://pubdocs.worldbank.org/en/133191495654716261/B3-ABCA-Skills-Macours.pdf - replication data: https://www.openicpsr.org/openicpsr/project/124141/version/V1/view. Digit-span instruments also appear in WB microdata (Mexico returns-to-capital experiment, https://microdata.worldbank.org/index.php/catalog/2028 ; Ghana Socioeconomic Panel with digit span + Raven's, https://microdata.worldbank.org/index.php/catalog/2534).
- **Conclusion**: treat the competition instrument as a *composite*: STEP-shaped questionnaire + impact-evaluation-style cognitive battery. **No single real WB survey matching "106 items, digit span + Corsi, 3 countries, ~7k youth job-seekers" was found - the exact country triple is unverified and should not be assumed.** (Candidate pairs/triples of the 12 STEP samples reach ~6.9k rows, e.g. Ghana 2,987 + Kenya 3,894 = 6,881, but nothing confirms which.)

### (b) Key reports / URLs

- STEP microdata collection (free public-use files, questionnaires, weights, per country): https://microdata.worldbank.org/index.php/collections/step - e.g. Georgia 2013: https://microdata.worldbank.org/index.php/catalog/2013 ; Macedonia 2013: https://microdata.worldbank.org/index.php/catalog/2568 ; Philippines 2015-16: https://microdata.worldbank.org/index.php/catalog/3182
- Methodology + module inventory + sample sizes: STEP 2014 working paper (URL above).
- Example STEP-based analytics with published tables: Colombia skills paper https://documents1.worldbank.org/curated/en/954461468189869519/pdf/Adults-Cognitive-and-Socioemotional-Skills-and-their-Labor-Market-Outcomes-in-Colombia.pdf ; Kenya STEP jobs working paper https://documents1.worldbank.org/curated/en/295641532463546573/pdf/128788-STEPESKenyaWorkingPaperFinalMayFULL.pdf

### (c) Published marginals usable as priors

- **STEP microdata itself** (free per-country download) is the prior source - full response distributions for every questionnaire item: 31 personality items (Big Five/grit-style frequency scales), 7-item risk-preference scale, education/employment modules, literacy scores. Format: Stata/CSV public-use files + PDF questionnaires.
- Laajaj-Macours replication data (openICPSR 124141) gives realistic digit-span and Raven's score distributions for an African sample.
- No public dataset provides Corsi-block norms for WB youth samples - **unverified territory; treat Corsi-item priors as weakly informed** (structural prior only: monotone-decreasing success by span length).

### (d) Pre-registrable domain expectations (Thread 3)

1. **Cognitive test items are internally consistent and positively inter-correlated; personality/technical self-reports are not.** Laajaj & Macours: cognitive measures (Raven's, digit span, math) reliable and internally consistent; self-reported skills noisy with low test-retest (digit-span subconstructs < 0.6; technical skills worst). Expect a usable low-rank/latent structure across cognitive items, and flatter, noisier structure across attitude/personality items. Source: https://jhr.uwpress.org/content/wpjhr/56/4/1254.full.pdf
2. **Digit-span outcomes are monotone in span length** - success probability declines with sequence length; adjacent-length items are strongly dependent, and stopping rules gate later items on earlier failures (likely a large share of the 40 gated items). Source: battery structure in Laajaj & Macours; digit-span instruments in WB catalogs 2028 / 2534 (URLs above).
3. **Self-reported agree/frequency-scale items skew toward the agree end (acquiescence) in LMIC samples** - expect asymmetric Likert marginals rather than centered ones. Source: Laajaj & Macours JHR (measurement-error/acquiescence findings in the same program).
4. **Employment-module gating follows work status and is complementary**: job-detail items (occupation, wage, employer type) gate on working; job-search / reservation-wage items gate on *not* working - the two gated blocks' sentinel rates must sum coherently within a respondent. Source: STEP household questionnaire module inventory (STEP 2014 paper, Table 1 pp. 12-14).
5. **Country identity dominates cognitive-score distributions** (STEP sample sizes were sized by national literacy rates; ECA samples score far above African samples on the shared PIAAC-linked scale) - condition cognitive items on country first. Source: STEP 2014 paper pp. 61-62.

---

## Cross-thread notes for modelling

- **Thread 1 is the only thread where the competition's rounds map to identifiable real fieldwork windows** (Jun 2025 and Oct-Nov 2025), both post-Assad-fall; the famous 1.7% -> 27% discontinuity happened *before* the competition's window. Do not encode a between-round jump of that size; encode the Jan->Jun-style decay plus the stable country ordering instead.
- **Machine-readable priors, ranked**: (1) WGM 2018 microdata (full per-country distributions, CSV, free, CC-BY); (2) STEP public-use microdata (full per-country distributions); (3) UNHCR eRPIS/Flash - PDF percentage tables only, hand-transcribed above (no microdata, no Excel annexes found; the UNHCR Microdata Library does host the eRPIS *frame* surveys VASyR/VAF/SEVAT, usable as socio-economic proxies per country).
- **Unverified items recap**: eRPIS wave-2 n=4,033 and its findings report; exact eRPIS wave-2 methodology-note URL; the UNICEF instrument's 10-country list; any real WB survey exactly matching the "Skills Assessment" (country triple, Corsi inclusion); whether competition option sets match the real questionnaires verbatim.