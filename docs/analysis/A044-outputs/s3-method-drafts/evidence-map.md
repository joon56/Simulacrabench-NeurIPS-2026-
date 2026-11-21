# Evidence map — S3-METHOD-DRAFTS-A044

Both new English PDFs are review drafts, each actually four pages. Their sources
are the task's allowed documents and two exact static main.py files. No cited
raw/data/cache/ZIP path was followed; no model or scorer ran. External links in
the PDFs are transcribed from retained records, not newly fetched sources.

| Draft claim / location | Direct permitted source | Scope and treatment |
|---|---|---|
| Task, official floor and pooled metric; phase split and runtime contract; both §1/§4 | [S3 E041 method](../s3-prep/method-e041-draft.md), [E025 notes](../s3-prep/method-e025-notes.md), [kit compatibility](../s3-prep/kit-compatibility.md), [rules](../s3-prep/rules-and-schedule.md) | Retained pinned f980ef5059360fcf977ed7971af5c00ee5c1962f public contract; not private deployment certification |
| E025 base, conditional gates, neural selection/refit, rarity/agreement evidence and replay; both §1-2 | [Exact E025 static main](../../../../submissions/2026-09-25-E025/main.py), [original E025 Markdown](../../../../submissions/2026-09-25-E025/method-4p.md), E025 notes | Static code and document reading only; E025 lacks the additional E041 section metric |
| E041 metric partitions, activation, candidate cap, legacy fallback and deployed-bank difference; E041 §2-3 | [Exact E041 static main](../../../../submissions/2026-09-25-E041/main.py), [original E041 Markdown](../../../../submissions/2026-09-25-E041/method-4p.md), S3 E041 method | 1200/800/800 caps, 32 candidates, 50 optimization iterations, weight range0-12 and threshold max(.003,2SE); no model import |
| Historical DEV readings and counterevidence; both §1/§3 | S3 method/notes, [A018](../../A018-test-selection.md), [S0 acceptance](../s0-e025-review/decision.md) | E041 released API ID933094 is retained user-provided evidence; E025 reading is historical user-reported. Rounding/noise persists; no new platform query or inference of E064 result |
| New E025 exact442425/official3, reusable E041 identity gate; E041 §3, E025 §4 | [Protocol](../s3-e025-provenance/protocol.md), [baseline reuse](../s3-e025-provenance/baseline-reuse.json), [comparison](../s3-e025-provenance/comparison.json), [closeout](../s3-e025-provenance/closeout.md), [verification](../s3-e025-provenance/verification.json) | Existing completed evidence read only. Numbers copied from aggregate comparison, not recalculated from raw. E041 not rerun |
| New E025429.930/450.277s and sampled2.035/2.067GB; E041 §3, E025 §4 | New provenance closeout and [budget ledger](../s3-e025-provenance/budget-ledger.json) | Source and official all3 each share900s; CPU2/GPU0; decimal GB. Overall recorded maximum sample gap0.221341s includes supervisor/other approved work, conservatively bounding the two arm maxima0.2213402/0.2201455 |
| E041 historical336.554/359.449s; E041 §3 | [Phase2 validity](../s3-prep/phase2-validity.md), A018, original E041 method/PDF | Historical scopes differ from new E025. No controlled timing comparison or new E041 fit claimed |
| Old E025 drift, A012 post-run collection and missing environment fields; both engineering sections | Phase2 validity, [revalidation plan](../s3-prep/revalidation-plan.md), baseline reuse and new provenance closeout | New connection closes the named modular/archive gap; old discrepancies remain unexplained |
| External material and notices; both §4 | [License inventory](../s3-prep/license-inventory.md), S3 method/notes, A018 | Disclose actual development use separately from bundled assets. No license text changed and no team grant made. Do not treat access approvals as redistribution permission |
| Date-only calendar, unavailable latest Terms and method obligation conflict; both §4 | Retained rules and S0 decision | Do not repeat original PDFs' obsolete November14 00:00UTC closing assertion. No fresh web request under this task |
| Exact local source/doc identity and inherited ZIP identity | [Document pairing](document-pairing.json), [preservation entry](preservation-entry.json), new provenance verification, phase2 validity | Current allowed main/MD/PDF files hashed; archive hash inherited only, not rehashed, uploaded or authenticated remotely |

PDF reference keys [1]-[5] are retained public URLs from the sources above.
[6] denotes permitted A018/S3-prep/original-method documents, and [7] the completed
E025 provenance documents plus S0 acceptance. The map makes those compact PDF
citations inspectable without implying that any downstream linked dataset was read.

## Original-document inspection and new-document verification

`original-pdf-inspection.json` and the two `*-original-extracted.txt` files record
read-only extraction of both historical four-page PDFs. Their original bytes
remain unchanged. The new drafts correct stale claims in new files only.

The copied renderer uses only document dependencies, reads this folder's Markdown
and writes this folder's PDF. Each candidate succeeded on attempt1; neither was
rerendered. The final PDF bytes equal its preserved successful attempt1 bytes.
`*-pdf-inspection.json` records actual four-page count, every page's extracted
text/spans/fonts/bounds, and six URI links per PDF. All eight pages were rendered
at130dpi and individually viewed. See `visual-review.json` for the page-by-page
assessment. The title banner includes the required em dash; Base14 Times,
Helvetica and Courier text rendered without visible replacement glyphs.

The original model and renderer were never executed. The five supervised document
runs were original-PDF extraction, E041 render, E025 render, E041 inspection/PNG
render and E025 inspection/PNG render. They are document operations, not research
tests or renewed submission parity checks.
