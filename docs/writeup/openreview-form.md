# OpenReview submission sheet: team Odyssey (2026-11-18)

Invitation: `NeurIPS.cc/2026/Competition/SimulacraBench/-/Submission`
Deadline: **2026-11-20 10:59 UTC = 19:59 KST** (form closes 30 minutes later).
Report source: `docs/writeup/report.tex` + `refs.bib` (organizers' template; NeurIPS 2026 style,
at most 4 pages of main text, references and appendix unbounded).

## Field values

| Field | Value |
|---|---|
| title | Donor-Retrieval Survey Completion with Additions Validated Inside the Run |
| authors | Minjoon Yoo (Yonsei University). OpenReview profile of the author; the PDF prints the institutional address |
| team_id | Odyssey  (exactly as on the Codabench leaderboard) |
| keywords | survey completion, record linkage, retrieval-augmented tabular learning, calibration, stacking, in-context tabular model |
| TL;DR | A calibrated base with donor retrieval over visible respondents; pooled tree and TabICL experts, a copy share and a calibration are applied only if a validation run inside the submission confirms them. |
| abstract | see below |
| pdf | compiled `report.tex` |
| code_url | https://github.com/joon56/Simulacrabench-NeurIPS-2026-/tree/17565e871703be0b221095fad320d238587d6674/submissions/2026-11-15-E077/release |
| code_license | BSD-3-Clause |
| base_models | TabICL v2 classifier (checkpoint tabicl-classifier-v2-20260212.ckpt; Hugging Face jingang/TabICL revision 4dcd344ece2c00be9e831fdd35bed57b5ad83e19) |
| external_data | see below |
| data_use_attestation | to be confirmed by the team |
| email_sharing | to be confirmed by the team |
| data_release | to be confirmed by the team |
| license | CC BY 4.0 (only option) |

### abstract (178 words)

Held-out respondents are completed from their GIVEN block by a calibrated base predictor and additions that are admitted only by the validation run inside the submission. The base predictor uses hierarchical backoff tables, a shared-trunk network with a softmax head per item, soft coupling to the declared skip logic, and donor evidence (the answers of the most similar visible respondents under Fellegi-Sunter agreement weights, sharpened on UNHCR by section-specific metrics learned from the visible rows). On top of the base predictor, each instrument may receive one transform chain built from one or more of these parts: a log-linear pool with gradient-boosted tree experts or a pretrained in-context tabular model (TabICL v2), a copy share for exact matches, and a reliability calibration. The chain is fitted on 1,000 respondents hidden inside the run and applied only if 1,000 further hidden respondents confirm it. The test-phase skill is 0.479 (UNICEF 0.343, World Bank 0.234, UNHCR 0.860). In development, 24 variants never read above the base by one display step, so we claim nothing about the size of the additions' contribution.

### external_data

None enters the submitted pipeline: the predictor is fitted inside the run on the visible
rows of the official release only, and the archive contains no parameter, prior, table or
weight derived from any other dataset. Development-only resources, none of whose rows,
outputs or fitted artifacts are in the submission:
- UCI Adult (Becker & Kohavi, 1996), https://archive.ics.uci.edu/dataset/2/adult, 48,842
  records, CC BY 4.0 - recoded offline proxy benchmark for method studies that were not adopted.
- U.S. Census Bureau 2023 SIPP public-use file,
  https://www.census.gov/data/datasets/2023/demo/sipp/2023-data.html - offline proxy for a
  gated-item study that was not adopted.
- Organizers' synthetic sandbox (starter kit) - engineering checks.
- UNHCR Jordan 2023 Vulnerability Assessment Framework, host-community survey
  (UNHCR_JOR_2023_VAF_HOST_v2.1, UNHCR Microdata Library, obtained under the author's approved
  access): only the release documentation (DDI metadata, researcher guide, questionnaire
  forms, variable-label tables) and the header line of the six data files were inspected, to
  judge whether the dataset could inform the UNHCR instrument. No response record was read,
  nothing was linked to the competition data, and nothing from it enters the submission.

## Report status (2026-11-18)

All fields of `report.tex` are filled; `report.pdf` is compiled (6 pages: main text ends on
page 4, then references and appendix). Public code: commit 17565e871703be0b221095fad320d238587d6674
on branch `work/e050-submission` (pushed; raw files verified against MANIFEST.sha256).
Organizer baseline row: 0.0000 on every skill, because the crowd-marginal baseline scores exactly 0
by construction (starter-kit README, website); the leaderboard shows no separate entry.
Style option: `[main, final]`, because the official neurips_2026.sty does not compile with `[final]`
alone, as the organizers' template has it.

## Checks before submitting

- Compile with `neurips_2026.sty`; main text (Sections 1-5) must end on page 4 or earlier.
  If it runs over: move the "Experts" paragraph of Section 1.4 and the detail of Section 1.7
  to Appendix A first.
- Test numbers in Table 3 must equal the leaderboard entry: 0.4790691441 / 0.3427149262 /
  0.2344919185 / 0.8600005877 (shown rounded to four decimals).
- Bibliography: the TabICL (ICML 2025, PMLR 267) and TabR (ICLR 2024) entries were checked
  online on 2026-11-18; the six older entries are standard references written from memory.
