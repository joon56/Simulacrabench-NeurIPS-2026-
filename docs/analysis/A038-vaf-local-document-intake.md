# A038 — VAF local document intake

Date: 2026-09-30. Role: S0, document intake under A037; no S1 execution.
Decision: **RELEASE_IDENTIFIED / EXPORT_MAPPING_UNRESOLVED / EMPIRICAL_HOLD**.

## What changed

The user supplied `UNCHR_data/` and identified its root XML as unrestricted
metadata. Local document identity is `UNHCR_JOR_2023_VAF_HOST_v2.1`, edited,
cleaned and anonymised. The earlier user-reported approval establishes access
approval; it does not by itself document every downstream use. No portal lookup.

Inventory: 24 files: one XML, two PDFs, two blank KOBO XLSForms, six variable-label
CSVs, twelve response CSV/DTA files (six table names in two formats), and one
working-children callback XLSX. Inventory is filenames/sizes, not verified response
schemas, row counts or unique samples. The agent did not extract an archive.

Four document pairs match A032 byte-for-byte:

| Local document | Existing A032 document | SHA256 |
|---|---|---|
| Root release XML | `catalog1030-ddi.xml` | `f5ea139f2be32e84d544c612560584487b2cd955bd776f0b4945b792009373e1` |
| VAF researcher guide.pdf | `researcher-guide.pdf` | `381372b27e64ca48e169d42917fece4342559959053fa46d135015a94076f6d6` |
| Long KOBO form | `VAF_Host_2023_LongXLS_final.xlsx` | `8ebae920a94af0198ce4061f118b797fabc485f60850118e7e2af63fa59fbdc5` |
| Short KOBO form | `VAF_Host_2023_ShortXLS_final.xlsx` | `c2958235b940e47524983e9ff133b408ce78238a476e5a58e0860a2b7cf6880f` |

The guide's existing text extraction was reused; forms were not re-extracted and
the earlier extractor/fixtures were not rerun. The other PDF was inventoried only.
These familiar documents are not new evidence that the old scientific gaps closed.

## New metadata discrepancy

The six explicitly named `*_labels_*.csv` tables contain `VAR,LABEL` metadata.
Their variable names were compared with the corresponding DDI file descriptions.
No `*_data_*` CSV/DTA headers, rows or key values were read.

| Table | DDI variables | Label rows |
|---|---:|---:|
| main | 197 | 196 |
| case | 80 | 74 |
| family | 27 | 22 |
| member | 189 | 183 |
| sharing_group_long | 591 | 586 |
| sharing_group_short | 435 | 430 |
| Total | 1519 | 1491 |

Every label table introduces `ID_main`; member also introduces `ID_ind`. DDI
instead lists hierarchy/index fields such as `householdindex`, `sharingindex`,
`familyindex`, `caseindex`, `individualindex`, `index` and `parent_index`, varying
by table. Both sharing-group label tables also omit the DDI variable
`RestaurantInKindExternalOrders`. Full metadata differences and document hashes
are in [document comparison](A038-outputs/document-comparison.json).

**Fact:** the supplied documentation representations differ. **Inference:** an
export/anonymisation mapping may explain this. **Unverified:** actual response
headers, key semantics, join cardinality, household separation and whether label
tables fully describe the data. Do not equate `ID_main` with `householdindex`, infer
independence from names, or apply the old Form/index join blindly. This finding is
not evidence of corrupt data, actual gate errors or an unusable dataset.

## Applicability and next action

| Condition | Current evidence | Minimum input and owner |
|---|---|---|
| Release identity | Local XML/forms/guide identify the intended v2.1 | Established at document level; actual response conformity unverified |
| Permitted local research | User reports approval; XML citation clause supplies no full use contract | User supplies accepted application and applicable use terms already received; no fresh application presumed necessary |
| Export and repeat linkage | DDI/guide and distributed label names differ | Release-specific crosswalk explaining `ID_main`, `ID_ind`, Form, case/family/sharing-group relationships; provider documentation, then bounded S1 verification if warranted |
| Asked/missing/edit meaning | A032 has natural routing definitions, but no resolved export treatment | Release-specific missing/skip/edit mapping, or explicit statement that distinctions were not retained; provider/document source |
| User exposure | Agent has read metadata only | User states download/unzip only versus row inspection/aggregation; pending answer stays unknown |
| Evaluation design | No verified groups, independent roles, paired variance or precision | S0 can design roles after linkage/observable outcomes are established; later authorized S1 checks only |

Main remains the A037 question: a fixed-library selection-objective comparison,
D-P versus D-R, with P distinct from original R/E041. Access and exact document
identity have advanced; the channel is still not established for that mechanism.
Public document counts are not evaluation sample sizes or power estimates.

Next useful input is the **export-specific crosswalk and missing/edit specification**,
plus the applicable terms/application. First use any already delivered accompanying
documentation; ask the provider only for facts absent there. The precise provider
question is: how do the distributed ID_main/ID_ind and Form relate to the guide's
hierarchy, and how are routing skips, refusal/DK, ordinary missingness and edits
represented in v2.1? No inquiry was sent.

An actual-data S1 should not be commissioned as unrestricted EDA. If metadata and
use scope support it, its first bounded task would verify documented headers and
linkage using explicitly permitted columns, with no response outcomes, models or
scores. Key uniqueness alone cannot establish key meaning or missingness semantics.
That task is not yet authorized or launched here. No executable S1 prompt is
issued before the missing input fixes its scope. Do not repeat the same public
search, A032 extraction or this HOLD review without material new input.

If the required distinctions were not retained, close this channel for this
particular gate/objective comparison; do not declare all VAF research impossible
or silently substitute another research question. TabICLv2 remains a reserve
idea, not an automatic fallback. No expected DEV/TEST improvement is estimated.

## Access and preservation

New access: file paths/sizes; public XML metadata; six VAR/LABEL tables; hashes of
four identified documentation files and those six metadata tables. Public XML
aggregates were already exposed in A032. New metadata reads are recorded; no new
row-level sample or independent audit is claimed. User prior row exposure unknown.
Response CSV/DTA, callback XLSX, response identifiers, caches and protected historical
data were not read or hashed. No fit/predict/score/test/ZIP/web/agent execution.

`/UNCHR_data/` was added to `.gitignore` to keep the local supplied folder out of
ordinary untracked-file staging. Original ignore content is preserved; no files
were moved, staged, committed or pushed. This is not access control or removal
of any already tracked file. Existing dirty work and docs/tree.md are preserved.

E041 incumbent/E025 fallback; E057/E060/E061 parked. E058 STOP,
E059 STOP_SELECTION, A023/A024 empirical HOLD and all existing STOP/HOLDs remain.
Preserve 17999 people/12339 SSUID exposure, A022 original roles, E059 consumed
oracle1918/1124 and selection2007/1130, protected audit2074/1177 and calibration1866.
A_half unpromoted; A018 user-unconfirmed; S3 stopped; no S2 candidate.

Receipt/baseline: [entry](A038-outputs/entry.json). File-name-only inventory:
[inventory](A038-outputs/inventory.json). Scoped document preservation:
[verification](A038-outputs/verification.json). HEAD remains a43f437.
