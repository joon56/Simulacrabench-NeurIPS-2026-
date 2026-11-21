# E063 S2 identity-check omission and scoped repair

One preflight bookkeeping defect, not a model/policy/numerical failure. The
initial entry hash map omitted the current E025 snapshot path. E025's expected
snapshot identity in E062 frozen-inputs and its completion/raw manifest were
present; preflight's `snapshot_source_hashes_verified` overstates the separate
current-byte check for this one file. Original entry/preflight/reuse/freeze are
preserved. Do not read the original statement without this correction.

At2026-10-09T14:46:22.662100Z, after candidate assembly had launched but before
evaluator/ZIP/official, the explicitly allowed E025 snapshot was hashed against
the user's fixed00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9.
Exact match; E062 frozen-inputs identity also agrees. Evidence:
baseline-identity-supplement.json, identity-repair-freeze.json and transcript
32d5a2/2dfaef. Timing is explicitly late, never retroactively preregistered.

Affected boundary is reference provenance. E025 snapshot is not imported or
executed by the candidate; original E041/H/source/input/renderer and12raw
identities were already checked. No dependency bytes changed, no prior model
success invalidated, no baseline fit or reserve all3 consumed. Current snapshot
and supplement freeze were checked again before evaluator and official entry.
Only this actual identity check was added; no success suite repeated.

Workflow r5 permits fixing an owning S2 helper prerequisite with fixed scope,
data/policy/criteria/budgets and preserved evidence. Final qualification relies
on the corrected current identity and already completed reference provenance,
not a false claim all current snapshot hashes were checked before model start.
S0 receives this ordering limitation alongside the technical result.

Administrative non-model events: truncated large tool outputs reread narrowly;
E062 manifest metadata reader used `files` instead of `entries`, then corrected;
one authoring apply_patch context mismatch made no edit; a later metadata lookup
exposed the omitted E025 key. No experiment/policy/tolerance/assertion change,
scientific restart, resource failure or protected-data access resulted.

Final document-only attempt a280cf stopped before writing verification/manifests:
the metadata helper used strip() on porcelain output, removing the first line's
leading status space and falsely flagging an existing paper-session skill path.
No file was removed or restored. Preserve status leading spaces with rstrip of
line endings only; recheck the affected dirty-path comparison, no scientific rerun.

Final document-only attempt fdb213 then stopped on link validation: copied
status/log backups and insertion fragments retain paths relative to docs/,
not their archival S2 location. Preserve backup bytes and partial verification
as verification-document-attempt-01.json. Validate new shared additions in their
actual docs/ destination, snapshot scorecard in its destination, and standalone
new S2 documents. Do not rewrite old history or rerun model checks for relocation.
