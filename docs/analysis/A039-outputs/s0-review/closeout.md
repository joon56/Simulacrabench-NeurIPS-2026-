# A039 S0 result decision

2026-10-01. **ACCEPT_HEADER_RESULT / EMPIRICAL_HOLD / AWAIT_SPECIFIC_METADATA**.
This closes S0 review of a completed information task, not another experiment.

## Accepted evidence and its limits

All34 allowed document/source identities in the union of S1 verification's
source-after and artifact hashes match current files. HEAD remains a43f437.
The saved comparison supports six exact header/labels name-and-order matches,
no duplicate column names, and differences from DDI in every file. Counts are
196/74/22/183/586/430. S1 reports33357 application-requested header bytes and
zero requested bytes past the first LF. Its boundary-fixture record reports9 PASS;
the worker took0.1209324s, and recorded session elapsed797.7621292s fits40minutes.

S0 reviewed saved records and hashes; it did not observe the original process,
inspect actual CSVs, rerun the reader/tests or independently certify every access.
S1 supplies concrete tool-read references, beyond a template-only compliance claim.
No contradictory recorded evidence was found. Peak memory was not measured.

The label-table omission explanation for legacy hierarchy names is now resolved:
the old names are absent from actual headers too. That is an export-schema fact,
not evidence of data corruption, missing observations or an invalid dataset.
The supplied documents describe Form and some breakoff/refusal/DK states. They
do not define ID_main as a household key or give a complete route-specific map
from exported blanks to asked/not-asked/editing states.

## Minimum facts that change the next decision

| Priority/input | Why needed | Sufficient targeted answer / owner |
|---|---|---|
| 1. ID_main unit and scope, relation to Form | Avoid treating related/repeated households as independent evaluation units | Release documentation or custodian explanation of same-household grouping across forms/files, including whether repeated IDs/households can occur; no actual IDs requested |
| 1b. Family-to-case assignment for FamilyRegistered/NotRegIDFamilyType | This named route spans family and case files; household membership alone does not assign a case to one family | Documented released columns/composite or explicit statement that this linkage was not retained; only required for this route |
| 2. Asked/missing/edit mapping for the proposed route(s) | Avoid labelling every blank NA_GATED or interpreting breakoff/edit artefacts as approximate-gate errors | Release-specific codes/rules for NotRegIDFamilyType and/or WGQSeeing plus relevant upstream controls; identify states that were collapsed or cannot be distinguished |

Both grouping and observable-outcome meaning are needed before designing an
independent study. A correct join alone does not resolve missingness; a documented
missing code alone does not establish independent households. The custodian or an
identified release-specific document can supply the semantics. The user can pass
on such documentation or choose to send the existing narrowed questions. S0 owns
reviewing the answer and fixing the next scope; no automatic contact occurs.

ID_ind's label does not prove a stable anonymous person key. It becomes necessary
if a future design relies on person linkage/deduplication; do not require all
person-identification details before a narrower household grouping explanation.
Form categories are file-specific in the DDI; code1 means Long in one sharing
file and Short in the other. No universal numeric recode is established.

The age example needs the meaning/transformations of released IndAge and the
WGQSeeing asked-state rule, not original dates of birth or all raw calculation
inputs. Missing those raw inputs does not alone disqualify released age.
RestaurantInKindExternalOrders is an observed export difference but not a current
decision-critical question. A complete all-variable cleaning history is not an
entry requirement if a documented, prospectively fixed subset answers the named
mechanism; such a subset would still need its own justified study contract.

## Why no further local execution now

| Possible next action | Information gained / limitation | Decision |
|---|---|---|
| Repeat header audit or document extractor | Already answered schema membership, no new semantics | Do not run |
| Read key values/count duplicates | Could test a documented cardinality rule, cannot identify what ID_main means or reveal unknown same-household IDs | Do not commission before a meaningful key contract; prohibited in this S0 |
| Inspect blank rates or fit a model | Could describe an ambiguous mixture, not distinguish never-asked from editing or establish gate disagreement | Do not run; HOLD remains |
| Obtain the two targeted metadata answers | Can determine whether a specific route and grouping protocol are designable | Recommended next input, via an existing release-specific source if identified, otherwise optional custodian inquiry |

No newly identified official location/document resolves these questions in the
reviewed package. That is not proof no such documentation exists elsewhere.
No renewed public search, data exploration or mandatory user inquiry is inferred.
The two-question [optional draft](custodian-questions.en.md) uses S1's narrowed
questions rather than restarting the broader A032/A038 inquiry. No attachment of
microdata, ID values or respondent records is needed. Draft remains unsent.

## Resume / close conditions

- A release-matched explanation of grouping/linkage permits S0 to specify a
  separate minimum-column key check. It does not clear asked-state ambiguity.
- A route-specific missing/edit explanation permits a scoped observability
  review. If both required semantics are adequate, define separate technical
  validation and prospective roles/precision; do not start fitting automatically.
- If family-to-case mapping was removed, close that particular cross-file route
  unless another documented mapping exists. Do not infer all member-level research
  is impossible; its suitability would remain a distinct, justified decision.
- If necessary never-asked/nonresponse states were irreversibly merged for the
  chosen route and no defensible observed outcome remains, close that route for
  this gate/objective comparison. Do not invent NA_GATED from blanks or claim
  the entire UNHCR hypothesis was disproved.
- If no new input arrives, retain this closeout; no replacement A/E record or
  equivalent S1 review. A response saying the distinction is unavailable is also
  decision-relevant input. Provider response time is unknown; no gain forecast.

No new executable S1 handoff, S2 candidate or TEST recommendation is issued.
A037 remains a question, not an established suitable VAF channel: P differs from
R/E041; D-P and D-R address different comparisons. Cross-chapter presence in one
member file does not itself establish a hidden-parent or approximate-gate channel.
A023 implementation/full-cost and prospective precision conditions still remain.

## Preservation

This S0 reads permitted records/source identities only and writes this review
folder plus status/log. All S1 outputs, original A039 S0/A038 files, models,
snapshots, .gitignore and docs/tree.md are preserved. No raw header/key/response
access or rehash, fixture/test/fit/predict/score, web/contact, agent/session launch,
ZIP/submission/commit/push, S2/S3 or TEST selection.

S1 header access is inherited exposure, not erased. Public aggregates, user-
reported download/unzip-only history,17999 people/12339 SSUID model use, A022
original roles, E059 consumed oracle1918/1124 and selection2007/1130, protected
audit2074/1177 and calibration1866 remain. E041 incumbent/E025 fallback;
E057/E060/E061 parked, E058 STOP/E059 STOP_SELECTION and all STOP/HOLDs preserved.
A_half unpromoted, A018 user-unconfirmed, S3 stopped.

Evidence: [entry](entry.json), [review verification](verification.json),
[S1 closeout](../s1/closeout.md), [remaining questions](../s1/remaining-questions.ko.md).
