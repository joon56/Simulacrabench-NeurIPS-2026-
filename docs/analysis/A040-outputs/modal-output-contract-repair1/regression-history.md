# Output contract regression history

Cycle1 reproduced the frozen exporter error `Output export manifest mismatch`
using the independently confirmed producer keys/counts. Reference metadata was
saved before rejection. Original exporter SHA256
`8e0cfd474416aa586af9f7ec936c20c7d4fbf0c1888d2d770cc10c4d038027d0` was asserted.
Expected-error reproduction passed; it is not an old-exporter compatibility PASS.
Outer process0.6453308s, internal0.2519824s, exit0.

Cycle2 exercised the repaired production `sandbox_stage.execute/export_mode`
with only process/filesystem/payload/billing endpoints injected. Fourteen checks
passed: one normal reference/candidate pair; ten invalid reference envelopes;
three invalid candidate envelopes. Normal world_bank filename/key and exactly
three count keys confirmed; candidate adds two hash/files only. Invalid reference
export always recorded reference1/candidate0. Equal-total wrong counts and float
counts were rejected. Missing/extra keys, corrupted hash and missing output files
were rejected. Outer1.9560776s, internal1.5679469s, exit0.

Total2cycles/2.6014084s outer (internal1.8199293s), versus120s/max3cycles.
No third cycle or unchanged successful repeat. Original39-case/15-case suites
and successful scientific fixtures were not run or imported.

Before cycle1, automatic approval review rejected the proposed process because
the test read/hashed the whole old reference/result.json; the reviewer could not
rule out actual output arrays. No process was started by that rejected request.
Safer revision removed direct old result/fixture access from tests, added a guard
against that entire old directory, and used only the already inspected metadata
extract: instrument/vectors, reference counts and hash-key names. Its SHA256 is
asserted before testing. The subsequent guarded command was approved. No token,
permission expansion or indirect old-array access was used. Original metadata
identity remains in prior-identity.json; test expectations do not originate in
consumer constants. Candidate extra names are extracted from producer source AST.

Evidence: regression/cycle1-result.json, cycle2-result.json and outer process/
stdout/stderr receipts. Complete source snapshots and per-case events/exported
protocol envelopes are in `tmp/a040-modal-output-contract-repair1/cycle1-source`,
`cycle2-source`, `cycle1`, `cycle2`. These are small protocol artifacts. Output
bytes `[]` are not computed predictions; count metadata is not a measured model run.

Executed commands:

```powershell
& docs/analysis/A040-outputs/modal-output-contract-repair1/run_focused.ps1 -Cycle 1 -Mode reproduce
# Minimal consumer repair and new source-manifest freeze between these commands.
& docs/analysis/A040-outputs/modal-output-contract-repair1/run_focused.ps1 -Cycle 2 -Mode verify
```

Wrapper: existing SDK Python, UTF-8, hidden process,40s limit per invocation,
exclusive new cycle paths and absolute14:48:27Z task deadline. Commands are a
record, not authorization to repeat completed checks. Future reproduction needs
a separately authorized fresh output/deadline; existing snapshots are immutable.
