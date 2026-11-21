# A030 source and access register

Checked 2026-09-27 UTC. One release: `UNHCR_JOR_2023_VAF_HOST_v2.1`.
12 core documents including failed target and used search-index metadata pages.
Count unique substantive documents, not URL variants/retries. Public search output
is indexed evidence; crawler dates do not establish current live-page content.
Other datasets' incidental snippets were not followed or used as channel evidence.

| ID | Official source | Access and use |
|---|---|---|
| D01 | [Study description](https://microdata.unhcr.org/index.php/catalog/1030/study-description), [root variant](https://microdata.unhcr.org/index.php/catalog/1030) | Direct study request403; root tool retrieval failed. Official indexed root/study text available: release identity, modules, sampling, dates, citation. No complete live snapshot saved. |
| D02 | [Related materials](https://microdata.unhcr.org/index.php/catalog/1030/related-materials) | Direct retrieval failed/403, repeated URL attempt did not help. Questionnaire attachment not obtained. Count failed core target conservatively. |
| D03 | [Data dictionary overview](https://microdata.unhcr.org/index.php/catalog/1030/data-dictionary) | Direct retrieval failed; official indexed file names/counts available. No rows downloaded. |
| D04 | [Report landing](https://data.unhcr.org/en/documents/details/109075), [PDF](https://data.unhcr.org/en/documents/download/109075) | Landing accessible; publish/upload2024-06-03. Web-tool PDF retrieval internal error; ordinary anonymous PowerShell download HTTP200, content type pdf. Stored below. |
| D05 | [General terms](https://microdata.unhcr.org/index.php/terms-of-use) | Direct403, indexed terms available. Licensed application approval and general restrictions. Not an executed catalog1030 agreement. |
| D06 | [Variable index page690](https://microdata.unhcr.org/index.php/catalog/?from=2023&page=690&ps=100&to=2024&view=v) | Indexed target-release question labels: health/education and related variables. No numbered cross-section routing conditions. |
| D07 | [Variable index page700](https://microdata.unhcr.org/index.php/catalog/?from=2023&page=700&ps=100&to=2024&view=v) | Indexed target-release marital/spouse conditional wording. Labels are not executable skip rules. |
| D08 | [Case Form](https://microdata.unhcr.org/index.php/catalog/1030/variable/f3/f3_V3?name=Form) | Indexed labels and aggregate counts encountered; no direct variable-page opening. Used only to record exposure and form variants. |
| D09 | [IndHeadOfHousehold](https://microdata.unhcr.org/index.php/catalog/1030/variable/f2_V34) | Indexed valid/invalid/category counts encountered; no direct variable-page opening. Not asked/sentinel evidence. |
| D10 | [RegStatus](https://microdata.unhcr.org/index.php/catalog/1030/variable/f2_V24) | Indexed valid/invalid/category counts encountered; no direct variable-page opening. Not record-level access. |
| D11 | [Variable index page692](https://microdata.unhcr.org/index.php/catalog/?from=2023&page=692&ps=100&to=2024&view=v) | Indexed householdindex label encountered. Label does not establish key uniqueness/cardinality. |
| D12 | [Vulnerability Assessments collection](https://microdata.unhcr.org/index.php/catalog/VUL) | Official indexed list attaches Licensed data files to exact HOST2023v2.1 entry. This is item-level evidence, not the generic license filter. `?page=1` is duplicate listing. No other dataset followed. |

D04 same-title official alternate URL:
https://www.unhcr.org/sites/default/files/2024-07/2024%20Socio-Economic%20Survey%20on%20Refugees%20in%20Communities%20in%20Jordan%20%E2%80%93%20VAF.pdf
Indexed text available, direct web request429; no retry/download. Same bibliographic
report, byte identity not established. Not another dataset or release.

## Saved document

- `vaf-host-2024-report.pdf`: 2,048,958 bytes,146pages.
  SHA256 `5785bd893da1f77f9a121671fc6aa788e0446a32355d3a62a056d3c8f4da9565`.
- `report-extracted.txt`: pypdf text extraction with page delimiters.
  SHA256 `a4a83b57a94215eff2489a6c002bc41656f22a775cc00244f5f77c0b4270d70e`.
- Acquisition: ordinary anonymous `Invoke-WebRequest` to D04 PDF with output
  under A030-outputs; no credentials/cookies/auth bypass. Existing global
  Python3.13/pypdf extracted text; no installs or scientific imports.
- Actual focused reads: TOC, introduction/methodology/limitations pp12–21,
  demographics p22, annex p136; document-wide keyword lookup and annotation URI
  inspection (none). Extraction is not an assertion of full human review.

## Search limits and negative findings

Queries constrained to official catalog1030/release identity, questionnaire,
dictionary, access and the matching official report. Broad search fallback
returned other releases/sites; these were not opened for investigation.
No matching questionnaire, executable skip map, missing-value codebook or
release-specific signed terms obtained. This is an acquisition limit, not proof
that these documents do not exist. Search closed at12 core documents; no automatic
retry series, neighboring catalog1098/793 substitution or access request.
