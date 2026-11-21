# A040 — same-session repair autonomy amendment

2026-10-05 KST, S0 workflow correction. User request: ordinary agent-created errors
should be repaired autonomously instead of creating another S0/S1 handoff each time.
This is a prospective scope clarification, not a repaired helper or a remote result.

## Decision

Keep S0/S1/S2 role separation. Change the repeated first-error/session-return
pattern: the owning session investigates, fixes and verifies routine implementation
defects within the task, then continues. S0 had overconstrained the handoffs; the
general workflow already called for completion of authorized work. The new
workflow **2026-10-05-r5** makes the distinction explicit in both agent entry paths
and the Korean S1/S2 templates.

No extra approval is needed for those in-scope repairs. Preserve failures and
cumulative usage in the same task record. A scientific STOP, new data/model policy,
exhausted allowance or uncertain external side effect is not a routine retry.
The purpose of S0 review is to decide scope/strategy, not approve every correction.

## Application to the current cleanup task

Base scope remains [s1-cleanup-only.ko.md](s1-cleanup-only.ko.md).
Replace its blanket "unexpected first SDK/service error ends all repair" rule
prospectively with the r5 classification:

- Argument/import/encoding/logging/protobuf/SDK wiring defects: diagnose and repair
  within this same S1, run affected local checks, then continue the authorized
  cleanup path. Cover the actual dependency boundary before another live call.
- Identity or permission contradiction, possible duplicate mutation, missing
  terminal evidence after allowed cleanup, or exhausted budget: stop the affected
  external action and record the precise unresolved condition. Do not duplicate a
  possibly completed termination or create a replacement resource.
- Confirmed pre-transport rejection is recorded as such. Client initialization
  can still make normal authentication calls; do not infer wire0 for the process.
- The30min task budget,180s aggregate local checks/30s each,120s single remote
  window/15s calls, max1 exact-resource terminate, no creation and cash0 remain.
  Local correction does not restart those timers. Finished/expired prior attempts
  remain closed. This amendment creates no new scientific or paid-resource allowance.
- Production-controller repair, new App/image/Sandbox/H100 execution, model/data/
  cache access, ZIP/upload, commit/push and S2/S3 remain outside the cleanup task.

The pending cleanup task can be continued by its owning S1 under the user's
applicable execution instruction. This S0 changed documents only. It did not run
the helper, check Modal or terminate the Sandbox. Terminal/final cost remain unknown.
Historical STOP/HOLD/exposure/incumbent/parked/TEST decisions remain unchanged.

## Adoption and read evidence

Read existing AGENTS/CLAUDE/workflow and current templates/task scope; refreshed
status and latest3 logs. Prior revision2026-09-27-r4; entry HEADa43f4379ec78dbc2de260463eef67bb1d567d7e1.
Tool evidence f4f117/f95441/95fd91/d9a766. Entry dirty89; named local python/pythonw/uv
jobs0. This does not certify remote absence or other sessions' compliance.

Updated AGENTS.md, CLAUDE.md, docs/workflow.md, docs/session-prompts.ko.md and
status/log. Original failure helper and historical handoff stay unchanged.
Open chats must reread the new version once; document edits do not update their
context automatically. No new per-error handoff or separate planning project.

Verification: current r5 text reread (tool23822e); workflow SHA256
a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23.
Both agent entries and Korean templates contain the new rule; unchanged role/data/
aggregate-budget boundaries were reviewed. Removing only this turn's status/log
additions and status revision change reconstructs their exact prior CRLF/BOM hashes.
Historical cleanup prompt, failed helper and docs/tree.md hashes remain unchanged.
No research tests were needed or run for this document-only change.

