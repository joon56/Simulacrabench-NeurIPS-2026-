# A039 — actual export headers versus documentation

2026-10-01, S0. **HANDOFF_PREPARED_NOT_EXECUTED**.

One separate S1 information task: inspect only the first header record of six
named VAF CSVs and reconcile it with existing labels/DDI/routing documentation.
No respondent values, keys, row counts, distributions or joins. This is new
evidence relative to A038, which compared documentation representations only.

Question: does the actual exported schema use the distributed label names, the
older hierarchy/index names, or a different layout? Can the existing documents
explain it, and which precise linkage/missing-state questions still need answers?
The current discrepancy is not proof that provider contact is necessary or that
the files are unusable. Header inspection also cannot establish key meaning,
uniqueness, independence, missing-state frequencies or actual gate disagreement.

Main: bounded header/document comparison, 40 minutes total, one process/CPU1,
GPU off, no dependencies installed. At most128KiB header bytes per CSV, at most
768KiB across six files. No model compute. Backup: if safe header access fails,
record the exact boundary/format failure and stop; no alternate data loader.

Why before further inquiry: actual export names can eliminate guessed mappings
or show that the label tables omit documented keys. It narrows the next technical
task or provider questions at low cost and without response exposure. If headers
merely match the label tables, report that finite result and unresolved semantics;
do not launch another same-scope audit. This is a prerequisite information task,
not a winning-method claim or predicted score improvement.

Public access clarification: user reports XML, KOBO, reports and guide available
without approval; actual microdata obtained after approval. Bundled labels are
metadata by content, not independently established public downloads. User reports
download/unzip only, no row inspection or aggregation. Prior public aggregates and
A038 metadata exposure remain. Header access in future S1 must be logged as access
to metadata inside a response file, not as zero file access or a full-file audit.

Correction to earlier document request: A032 already stores a public common terms
page (`terms-of-use.html`), acquired2026-09-27 per source-register. Use that existing
record; no need to demand that the user reproduce it. It is not the user's actual
approved application or proof of today's specific downstream permissions. This
task does not train, publish or distribute a model or the microdata.

Results: HEADER_RECONCILED, HEADER_DIVERGENCE or TECHNICAL_HOLD; separate semantic
state DOCUMENTED/PARTIAL/UNRESOLVED. All outcomes return to S0. No automatic key-
value audit, response analysis, empirical PASS, S2 or TEST action follows.
Original A037 objective question and A023/A024 empirical HOLD remain unchanged.

Deliverable: [copy-ready S1 prompt](s1-handoff.ko.md). User starts it in a separate
S1; authoring this prompt does not execute it. S1 owns `A039-outputs/s1/`; S0
entry/plan/handoff/verification remain separate. Original A038 files stay intact.

Evidence: [entry and allowed-document hashes](s0-entry.json),
[document verification](s0-verification.json). No actual CSV opened in this S0.
