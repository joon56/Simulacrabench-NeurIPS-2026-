# B01 repair history

All repairs retain scientific source, inputs, seeds, selection, criteria and caps.

1. Preflight first attempt failed in0.2807729s, before numeric imports/arrays/model
   calls: old E063 manifest reader expected a `files` list; actual E064 manifest
   is a `hashes` mapping. Trace in preflight.log; original code preserved in
   failures/preflight-01/release.py, original resource receipt retained.
   Changed both E064 manifest readers to the observed `hashes` field. New preflight2
   stage uses the corrected reader against the actual frozen completion/raw files;
   PASS25.6694599s. No successful assembly test repeated; no scientific retry.
   New stage name preserves failed files; assembly prerequisite points to successful
   preflight2. Failure plus retry counted in aggregate computational allowance.

Preparation script records initial mechanical adaptation only; later minimal
reader/provenance edits are in the frozen release.py. It is not an idempotent or
authorized rerun command. Frozen production inputs were never changed.

2. Read-only independent review found the final memory-sample PASS predicate
   omitted the memory threshold. No observed overrun: completed assembly peak
   RSS1959260160/private1490571264bytes, both below8589934592. Assembly/model/input/
   raw evidence remains valid. Preserved original controller byte-for-byte in
   controller-repair1/release-before.py, then introduced resource_success used by
   actual monitor, including final peak. One new stdlib test method covers7
   acceptance/rejection cases, PASS0.3078458s under monitor. No assembly/S1 repeat.
   Original release-freeze preserved; controller-repair-freeze links predecessor
   hash and only new controller/test identities. No model/observer/assembly bytes
   changed. New source freeze applies to later evaluation/package/official stages.

Administrative-only errors: one read-only PowerShell report used an unsupported
direct foreach pipeline; parsing failed before reads/writes and it was rerun with
an explicit collected array. One documentation-helper patch had a stale context
line; apply_patch rejected it without changes, then the intended single hunk was
applied. Neither affected running source, outputs, scientific counts or policy.
These helper operations stay within the conservative administrative charge.

Conservative focused accounting: two new test processes plus one repaired
preflight cycle (three focused/repair cycles total). Include both failed and
successful preflight wall in the focused/repair300s account as well as the same
aggregate3600s account; no double addition to total. Original resource receipts'
focused field counts only test processes; final ledger reports the broader scope.
