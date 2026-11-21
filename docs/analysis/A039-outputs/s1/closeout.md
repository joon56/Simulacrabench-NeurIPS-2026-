# A039 S1 — actual VAF export header reconciliation

2026-10-01 KST. **HEADER_DIVERGENCE relative to DDI; all six headers exactly
reconciled with bundled VAR/LABEL tables.** This is export-structure evidence,
not data corruption, an approved join, a gate-error observation or empirical PASS.
Return to S0; no S2 candidate or automatic next execution.

## Observed file facts

One read per explicitly named CSV, Python unbuffered binary FileIO, one byte per
request through the first LF inclusive. Six valid UTF-8, no BOM, CRLF headers.
No response bytes requested after that boundary; OS cache/prefetch is outside
this application-level claim. Header SHA256 includes CRLF; it is not a full CSV
hash. File size and mtime are stat metadata, not row counts or content identity.
No alternative loader or repeated actual-header read was used.

| Physical file suffix | Header columns | Label rows | DDI variables | Header bytes |
|---|---:|---:|---:|---:|
| main | 196 | 196 | 197 | 4220 |
| case | 74 | 74 | 80 | 1450 |
| family | 22 | 22 | 27 | 373 |
| member | 183 | 183 | 189 | 4418 |
| sharing_group_long | 586 | 586 | 591 | 13173 |
| sharing_group_short | 430 | 430 | 435 | 9723 |
| Sum of file-level occurrences | 1491 | 1491 | 1519 | 33357 |

These are column/metadata occurrences, not distinct questions, respondents,
households, samples or evaluation units. Within each file: no duplicate header
names or leading/trailing name whitespace; no corrections were applied. Each
header equals its label table's VAR sequence exactly. DDI common-name relative
order is also identical. Full name sequences, bidirectional differences, duplicate
checks and header-only hashes are in [header comparison](header-comparison.json).

| File | Actual-header-only versus DDI | DDI-only versus actual header |
|---|---|---|
| main | ID_main | householdindex, index |
| case | ID_main | householdindex, sharingindex, familyindex, caseindex, CaseCalculatedIndexLoop, index, parent_index |
| family | ID_main | householdindex, sharingindex, familyindex, FamilyCalculatedIndexLoop, index, parent_index |
| member | ID_main, ID_ind | householdindex, sharingindex, familyindex, caseindex, individualindex, individualCalculatedIndexLoop, index, parent_index |
| sharing_group_long | ID_main | householdindex, sharingindex, SharingGroupIndex, RestaurantInKindExternalOrders, index, parent_index |
| sharing_group_short | ID_main | householdindex, sharingindex, SharingGroupIndex, RestaurantInKindExternalOrders, index, parent_index |

A038's discrepancy therefore occurs in actual exported names, not only in omitted
label descriptions of still-present legacy indices. An export/anonymisation
crosswalk may explain it; no such mapping is established by these headers.
The absent restaurant variable is a specific column difference, not proof that
equivalent information cannot be encoded elsewhere.

## Documented meanings versus unresolved semantics

- **ID_main: UNRESOLVED.** Present in all six headers. Its label is the literal
  metadata text `0` in main and blank elsewhere. That is not a respondent value
  or a definition equating it with householdindex. Uniqueness, form scope,
  cross-file linkage and independence remain UNKNOWN.
- **ID_ind: PARTIAL.** Present only in member. The label says `Calculate UNHCR
  Individual Number`; DDI has no exact-name definition. The text does not establish
  anonymisation, stability, uniqueness or equivalence to individualindex. No
  actual identifier value was accessed and no linkage is approved.
- **Form: DOCUMENTED meaning, unverified values.** Present in all six headers.
  Guide pp4/13 describes Long/Short, and file-specific DDI categories support
  that meaning. DDI has 1=Long/2=Short for main/member/case/family, only1=Long for
  sharing_group_long and only1=Short for sharing_group_short. Numeric codes are
  file-specific documentation, not inspected CSV values or a shared-code guarantee.
- **Legacy hierarchy: DOCUMENTED in guide, export crosswalk UNRESOLVED.** Guide
  pp4/13 describes household/sharing/family/case/individual indices and Form
  composites. None of those five exact index names is in any actual header.
  Guide advice is not an executable join contract for renamed v2.1 fields.

**Missing/routing/edit semantics: PARTIAL.** Actual headers contain breakoff_1 in
both sharing files, breakoff_2 in family, breakoff_3 in case, breakoff_4 in member,
and breakoff_5 in main. Blank-form instructions explicitly describe interruption
and continuation; the cached DDI documents main breakoff_5 as 1=BreakOff/2=Continue,
while the other listed breakoff variables have Continue and generic Missing value.
These metadata differences do not establish observed frequencies, lost states or
the meaning of each response blank. A questionnaire control is not a complete
cell-level editing/missing-reason audit trail.

Ordinary response coding does carry some distinctions: member WGQDepression's
DDI categories include 3=DontKnow and6=Refused, separately from generic Missing
value. WGQSeeing also has a generic Missing value category. These entries do not
specify a literal CSV missing token or distinguish structural skip, interruption,
other missingness and imputation. No reviewed document establishes a comprehensive
per-cell edit/imputation mapping. Lexical matches in the JSON are only candidates
(including false matches such as credit/reason words), not proven flags. Absence
of a dedicated flag name does not rule out information in ordinary columns/codes.

## Named A032 examples

Both cached blank forms give the following definitions; no expressions evaluated.
Full selected definitions and parent/repeat conditions are preserved in
[document mapping](document-mapping.json).

| Item | Form row / original chapter | Actual physical file | Documented condition |
|---|---|---|---|
| FamilyRegistered | 103 / Family Information | family | TargetCase = No |
| NotRegIDFamilyType | 129 / CaseInformation | case | FamilyRegistered = No |
| IndAge | 189 / IndBioData | member | calculated age; depends on indStilLive_yn, IndAge_yn, ind_age, IndDOB and today() |
| WGQSeeing | 242 / HEALTH | member | IndAge >= 5 |

FamilyRegistered/NotRegIDFamilyType requires a documented family-to-case mapping;
ID_main alone does not supply that mapping. IndAge/WGQSeeing spans questionnaire
chapters but resides in one physical file. It is not evidence for a hidden-parent
or cross-file mechanism. Direct item presence does not resolve upstream controls:
IndAge_yn, ind_age, IndDOB and FileNumberFromSample are absent by exact name;
CaseStatus, indStilLive_yn and breakoff controls occur at their documented levels.
Long-form ancestors also reference calculated repeat indices absent from the
export. The short-form ancestor expressions differ. No proxy column, inferred
value or invented section replaces a missing dependency.

## Execution, identity and limits

HEAD a43f4379ec78dbc2de260463eef67bb1d567d7e1, branch work/e050-submission.
Workflow2026-09-27-r4. Ordered read evidence and SHA256 in [entry](entry.json).
All18 current S0 baseline-document hashes matched verification's **after** values;
the older before-status/log hashes describe S0's own changes, not a rollback target.
S0 records, A038 records, source data, models, .gitignore and docs/tree.md preserved.

New in-memory boundary fixtures9 PASS after an expected missing-module RED.
No existing research test/checker/scorer rerun. Header comparison worker wall
0.1209324s; parent command elapsed0.3773634s. One synchronous standard-library
Python process, no parallel workers/numerical libraries/GPU/installation. CPU1 by
single-thread design; no affinity or whole-machine utilisation claim. Peak memory
was not measured. Conservative total-session budget and closeout timing are in
[verification](verification.json); no learned model or scientific cost is implied.

Executed commands, repository root:

```powershell
.venv/Scripts/python.exe -X utf8 -B docs/analysis/A039-outputs/s1/test_header_reader.py
.venv/Scripts/python.exe -X utf8 -B docs/analysis/A039-outputs/s1/header_reader.py
```

Successful results are saved. Do not rerun the actual-header read to reproduce
this report; the tool rejects an existing result. Further analysis here used
only the saved header metadata and existing document extraction, not the CSVs.
No original XML/XLSForm/PDF extraction rerun was needed. Common terms are the
dated A032 snapshot, not the user's application or a new downstream-use ruling.

Next: [S0 handoff](s0-handoff.ko.md), [remaining questions](remaining-questions.ko.md).
No inquiry sent. This finite header task is complete; no key audit, role split,
fit, objective comparison, S2 release or TEST action is authorized. E041 incumbent,
E025 fallback, E057/E060/E061 parked, all existing STOP/HOLDs unchanged.
