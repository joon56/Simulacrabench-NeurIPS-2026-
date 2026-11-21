# A032 official-document source and access register

Checked2026-09-27UTC; one target release UNHCR_JOR_2023_VAF_HOST_v2.1.
14 selected documentary resources below, counting the two archive members and
failed/empty targets conservatively. Search-result snippets outside this set are
incidental exposure, not additional channel investigations. Limit20/60minutes.
See verification for exact local bytes/hashes and elapsed time.

| ID | Source | Acquisition / use |
|---|---|---|
| D01 | [Catalog1030](https://microdata.unhcr.org/index.php/catalog/1030) | Browser-tool failures/403 followed by one ordinary anonymous PowerShell request200; saved catalog1030.html. Actual release identity and navigation links read. |
| D02 | [Related materials](https://microdata.unhcr.org/index.php/catalog/1030/related-materials) | Anonymous200, related-materials.html. Lists questionnaire3831, guide3832, report3837. No response-data link followed for download. |
| D03 | [Study JSON](https://microdata.unhcr.org/index.php/metadata/export/1030/json) | Anonymous200; catalog1030-metadata.json. Study-level metadata, not variable codebook. |
| D04 | [DDI export](https://microdata.unhcr.org/index.php/metadata/export/1030/ddi) | Anonymous200; catalog1030-ddi.xml.1,519 variable definitions,6 file descriptions; public counts/categories also present and exposed. No respondent records. |
| D05 | [HOST KOBO archive](https://microdata.unhcr.org/index.php/catalog/1030/download/3831) | Official related-materials category Questionnaire.200; questionnaire-source.zip. Two filenames inspected before extracting only these XLSX documents. This is a source distribution archive, not a submission ZIP. |
| D06 | VAF_Host_2023_LongXLS_final.xlsx inside D05 | Empty form definition; settings ID UNHCR_VAF_2023_Long/version2310162710. No macros or formulas executed. |
| D07 | VAF_Host_2023_ShortXLS_final.xlsx inside D05 | Empty form definition; settings ID UNHCR_VAF_2023_Short/version2312062333. No macros or formulas executed. |
| D08 | [Researcher guide](https://microdata.unhcr.org/index.php/catalog/1030/download/3832) | Official related-materials Technical document.200; researcher-guide.pdf,14pages; pypdf text saved with page markers. Focused reads pp1–9,12–14; not a claim of full visual review. |
| D09 | [General terms](https://microdata.unhcr.org/index.php/terms-of-use) |200; terms-of-use.html. Licensed-data sections4–7 distinguish research purpose, team, onward disclosure and publication review. General text is not user's executed release-specific approval. |
| D10 | [Get microdata landing](https://microdata.unhcr.org/index.php/catalog/1030/get-microdata) |200 with zero-length body; access-landing.html intentionally empty. No credentials, form submission, account, license acceptance or microdata download. Cannot infer actual login/application state. |
| D11 | [Jordan VAF working group](https://data.unhcr.org/en/working-group/54) | Browser page read. Old2015/2017 forms are not release substitutes; no such downloads. |
| D12 | [Dictionary overview](https://microdata.unhcr.org/index.php/catalog/1030/data-dictionary) | Official indexed names/counts re-encountered. DDI now provides stronger local variable metadata; neither source establishes independence. |
| D13 | [Official2023 TOR lead](https://www.unhcr.org/jo/wp-content/uploads/sites/60/2023/03/Annex-A-TOR-RFP-6-2023.pdf) | Indexed search lead about survey development; direct browser retrieval failed. Not downloaded or used as deployed questionnaire/routing evidence. |
| D14 | [Existing official HOST report](https://data.unhcr.org/en/documents/download/109075) | Previously acquired in A030; inherited evidence and permitted hash verification only. No new report download. Catalog attachment3837 is a same-title pointer; byte identity with A030 PDF not asserted. |

The web tool also failed on an export URL guess; the later successful endpoints
above came from actual catalog links. Browser failure and PowerShell success
are reported separately. No credentials, restricted-link tokens, spoofed headers
or authentication bypass used. One incidental search result contained an access
token-like parameter; it was not opened or used.

## Extraction and provenance

XLSX documents were read as ZIP/XML with Python standard library: sharedStrings,
workbook sheet relationships and cell values, preserving Excel row/column labels.
Sheets are survey, choices, settings. No spreadsheet formula evaluation. PDF
text extracted by already installed pypdf; no package installed. The reusable
extract_metadata.py reads only the resulting questionnaire-cells.json and DDI,
records raw conditions and exact-name matches, and writes routing-metadata.json.

One CP949 stdout failure occurred while printing Arabic labels. Reconfigured
stdout UTF8 and continued metadata inspection. This was document processing,
not scientific fit/fixture execution. All referenced source and output hashes
appear in verification.json; protected Parquet/key/cache hashes are inherited
only, never reread or revalidated here.

Full documents remain local and uncommitted. Public availability was not treated
as a license to publish the source bundle, disclose microdata, deploy derived
weights or accept any agreement for the user.
