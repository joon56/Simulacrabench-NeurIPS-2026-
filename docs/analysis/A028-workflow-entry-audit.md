# A028 — Workflow entry and actual-reference audit
date-started: 2026-09-27
status: done — ENTRY_WIRING_FIXED_OTHER_SESSION_READS_UNVERIFIED
relates-to: A027 / A026 / E060

## Question and finding

The user asked whether every session actually refers to the agreed workflow.
**No all-session runtime confirmation exists.** A027 verified documents, not
independent reads by every chat. Its statement about future application was too
strong without checking the agent entry route. This review distinguishes entry
wiring, actual reads and compliance with the resulting scope.

At entry this repository had CLAUDE.md but no root AGENTS.md/AGENTS.override.md.
The inspected global Codex AGENTS.md contains style/code guidelines only. The
inspected config.toml has no explicit project_doc_fallback_filenames or
project_doc_max_bytes setting; this is not a complete audit of effective managed
configuration. Local .claude/settings.local.json has a WebFetch permission entry,
not a workflow-loading hook. Existing user settings/skills were not changed.

Official Codex guidance describes per-run instruction discovery through global
and project AGENTS files, with override/fallback rules and size limits. Existing
runs need a refreshed instruction context; file creation does not prove a running
session loaded it. Source checked2026-09-27:
[OpenAI AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
No separate agent/CLI session was launched to test discovery. Other tools' native
loading behavior and other chats' raw runtime transcripts were not independently
audited; do not infer those from this Codex documentation.

## Evidence by session

| Session | Evidence inspected | Qualified conclusion |
| --- | --- | --- |
| Current S0 | Tool reads of shared files in this conversation; A026/A027 records; current revision reread during closeout | Direct current-session read evidence; no inference that reading alone guarantees compliance |
| Prior S1/A023 | Its entry.json includes the historical workflow SHA256 cd584b5d...; source-linked handoff/closeout | Historical file identity/reference evidence, not proof it loaded new r2/r3 instructions |
| Prior S0/A024 | Entry hash and explicit read-sequence record | Session-reported historical read; not an independent transcript audit |
| Prior S2/E060 result | S2 handoff and log document reading arms, manifest checks and scope | Historical session-reported application; new revision loading remains unverified |
| Next S1/A027 prompt | Explicit workflow read and r2-or-later instruction, no execution | Template coverage only; not started by this audit |
| S3 | Current status says stopped and A018 unconfirmed | Do not resume it to test instructions; no new read/selection claim |

No claim that all historical chats complied. E060's S0 overreach itself shows
that having a workflow reference does not guarantee appropriate execution.

## Fix and verification design

Added concise root [AGENTS.md](../../AGENTS.md) as the Codex repository entry.
It directs agents to CLAUDE/status/latest3log/workflow and the current handoff.
CLAUDE references the same read-receipt rule. Workflow/templates now use revision
2026-09-27-r3 and require actual read paths/revision/role/scope before substantive
work, plus time/HEAD/workflow digest/tool-read evidence in the normal session
record. Read-only scopes report in chat; no new analysis project is required.

Receipts are auditable session reports, not a technical lock. A checksum alone
proves neither reading nor understanding. S0 must distinguish observed tool reads
from claimed reads/template links/unknowns when reviewing a handoff. Missing
historical receipts are not backfilled. Current reads are not retroactively
described as automatic loading of the newly created AGENTS.md.

An already open chat must explicitly reread current files after a workflow change;
do not promise hot reload. A new Codex run in this checkout has a documented entry
route, but its actual receipt still needs checking. Other checkouts need the files
present; this session does not commit/push or synchronize them. No production
hook, launcher, remote agent, research worker or new Codex process was created.

The earlier A027 S1 prompt remains unchanged: it already says current r2 or later
and reads workflow.md. Its old hashes remain valid except for shared documents
deliberately revised now. S1 must record the actual r3-or-later read and retain
the metadata-only task; this entry fix grants no fitting/data/ZIP authority.

## Access and preservation

Read relevant repository instruction/entry records, the global style file, local
permission settings and only the two relevant config-key search results. Consulted
official OpenAI documentation only; no VAF search, survey data or protected files.
An initial skill-path miss was corrected to .system/openai-docs; a mistaken rg
PowerShell flag was removed. Neither error launched research or changed settings.

New AGENTS/A028 records; intentional edits only CLAUDE/workflow/session-prompts/
status/log. A027 history, handoff and verification stay unchanged. Existing tree,
user files, models, experiments, snapshots and all STOP/HOLD/exposure boundaries
preserved. HEAD1d22334; no fit/predict/score/tests/data-cache/ZIP/commit/push/S3/TEST.
[Entry](A028-outputs/entry.json) and [verification](A028-outputs/verification.json)
separate local wiring checks from unverified fresh-session loading.
