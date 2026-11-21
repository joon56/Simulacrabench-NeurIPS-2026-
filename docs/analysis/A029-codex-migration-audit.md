# A029 — Claude to Codex workspace migration
date-started: 2026-09-27
status: done
relates-to: A027 / A028; operational maintenance, no model experiment

## Goal and authority

User requested a whole-folder survey and practical additions/corrections for
continued Codex work. This explicitly authorizes repository maintenance, including
small operating tools and their isolated checks. It does not authorize research,
S2 packaging, S3/TEST choice, protected-response access or git publication.
HEAD at entry: `1d223340d4e1fa3993b411dc5daafab9cb37d0cd`.
Workflow remains `2026-09-27-r3`; the role/evaluation contract is unchanged.

## Coverage

- File-path inventory across every root folder, hidden/ignored files included,
  excluding `.git` internals: **148,426 paths**, successful exit 0. Inventory is
  a point-in-time list including a few audit files created during collection.
  `.venv` accounts for 32,639; `tmp` for 114,491. Empty `docker/` was checked via
  directory listing. Git HEAD/status were inspected separately.
- Initial sandbox inventory returned 35,221 paths and exit 2 due to denied
  temporary/cache directories. A permitted read-only enumeration resolved that
  coverage gap. No ACL or sandbox policy was changed.
- [Folder counts](A029-outputs/inventory-summary-full.json) and
  [project paths](A029-outputs/project-paths.txt) retain compact evidence. Large
  raw path/error lists reside in ignored `tmp/a029-inventory/`; no need to put
  14 MB of dependency filenames into project history.
- Whole owned Python tree: **168 files parsed**, no syntax errors (src54,
  scripts55, tests58, notebooks1; includes two new maintenance files).
  [Static source audit](A029-outputs/source-audit.json) records each path and
  import roots. AST parsing is not execution or functional verification.
- Reviewed operational entry files, root configuration, shared study skill,
  dependency declarations, index, study guide entry, historical plan references,
  current templates, representative execution entry points and allowed prior
  environment records. Not every historical line was semantically re-reviewed.
- Surveyed inline Markdown file links in **206 docs files**, without opening
  linked data/artifacts. Two frozen E060 registration copies retain links relative
  to their original location; use [A025](A025-submission-oriented-review.md) for
  their intended destination. Frozen registrations were not changed to repair
  navigation. [Link survey](A029-outputs/document-links.json).
- Response data, CSV contents, Parquet, model caches, checkpoints, archives,
  output PDFs/images and `trip/` contents were **not read or hashed**. Third-party
  dependency contents were not reviewed; package metadata only. No claim of a
  complete security, statistical or model-correctness audit.

## Findings and disposition

| Finding | Action / limit |
| --- | --- |
| A028 root AGENTS fixed discovery, but project skill existed only under `.claude` | Added `.agents/skills/paper-session/SKILL.md` wrapper; shared body retained |
| Study protocol assumed WebFetch and automatic study commit/end-of-day push | Changed to available web tools and active user authorization; updated guide and CLAUDE summary |
| Implementation tier demanded running code regardless of current scope | Retained implementation deliverable; unrun checks explicitly unvalidated, no implicit fit permission |
| No root onboarding README; docs index omitted current operating entry points | Added README, Codex/Windows runbook and index links |
| Status mixed current tasks with obsolete prospective E059/E060 and old git instructions | Archived original bytes; condensed status into current decisions, next task and exposure boundaries |
| Basic requirements omitted scipy/sklearn/torch/threadpoolctl used by source | Added opt-in requirements-models.txt; preserved basic list and installed environment |
| Ordinary sandbox cannot launch current venv base interpreter | Read-only permitted launch confirms Python3.13.14 and package metadata; document permission diagnosis, no rebuild |
| Skill validator defaults to cp949 and fails on Korean UTF-8 | Rerun with `-X utf8` succeeds; no global locale or vendor script edit |
| `check_*`, harness and blanket pytest can execute research | Added fixed-allowlist document/package checker; document execution boundaries |
| Local settings and temporary files lacked repository ignore entries | Appended `.claude/settings.local.json` and `/tmp/`; original ignore rules preserved |
| Old plan files still contain then-authorized push/tree steps | Added plans/README routing to current contract; historical plans unchanged |
| `src/eval/oracle.py:13` hardcodes this workspace path | Recorded portability debt; frozen scientific source preserved, no unrelated refactor |
| Some historical docs use wiki links or dated mechanics | Current index gains ordinary operational links; no retrospective rewriting of evidence |
| No project hooks, MCP configuration or Codex-specific model settings found | No invented migration targets, blanket permission grants or automation added |
| Actual all-session loading/obedience not observable from repository files | Remains unverified; new sessions/read receipts still required, as in A028 |

Official local skill discovery was checked against
[OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills).
No optional plugin installation or global Codex configuration change was needed.

## Attempt log

1. Read repository entry sequence, inspected HEAD/dirty files/jobs and reserved
   unused A029. Captured 76 permitted existing text/source identities in
   [entry.json](A029-outputs/entry.json); this is not a blanket data manifest.
2. Sandbox path enumeration incomplete; permitted metadata-only retry completed.
   Protected file names in inventory are not response access or a new role grant.
3. Static imports/entry-point inspection found missing model dependency recipe,
   Claude-only skill discovery and obsolete study instructions. Chose a thin
   skill adapter, shared protocol corrections and a stdlib operating checker.
4. New checker tests first failed because implementation was absent; after
   implementation, five generated-document tests passed. No old fixture rerun.
5. Skill format checks initially failed on Windows default cp949; explicit
   UTF-8 invocation passed for both skill entries. Research environment unchanged.
6. First real workspace check correctly found two not-yet-created A029 artifact
   links. Final artifact creation resolves them; final report is retained beside
   the initial failure. This checks wiring, not policy enforcement by a host.
7. A combined patch initially rejected duplicate operations on docs/index.md;
   retried as a scoped update. No historical file was replaced from git HEAD.
8. Preserved the previous status byte-for-byte in
   [status-before-migration.md](A029-outputs/status-before-migration.md) before
   shortening the current entry. No historical outcome or exposure was revised.

## Validation, preservation and next use

- [Workspace report](A029-outputs/workspace-check.json): fixed-document wiring,
  SHA256 and installed dependency metadata; no scientific imports or git calls.
- [Verification](A029-outputs/verification.json): tests, skill checks, entry-hash
  comparison, actual changed files and execution limits.
- User's pre-existing study content and ignore rules remain except for named
  scope/portability corrections. No existing model, experiment, source snapshot,
  historical A/E output or `docs/tree.md` was edited. Entry hashes check the
  selected preservation set, not uninspected protected data bytes.
- E041 incumbent/E025 fallback, E057/E060 parked; E058 STOP/E059 STOP_SELECTION
  and prior STOP/HOLDs persist. A_half not promoted. A018 TEST unconfirmed,
  S3 stopped, S2 has no new candidate. No exposure role reassignment: prior
  17,999 people/12,339 SSUID union, A022 original roles and protected audit/
  calibration boundaries remain. No fit/predict/score, protected data/cache
  access, ZIP work, upload, commit or push.
- Repository wiring is ready for future Codex sessions. No new scientific handoff
  is created by this maintenance task. Existing A027 metadata-only S1 prompt
  remains available under its original boundary; it was not executed here.
- A fresh session's actual skill discovery/reading remains a runtime observation
  to record when that session is used, not a reason to launch another research
  session or claim every chat now complies.
