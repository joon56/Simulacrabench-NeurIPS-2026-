# Registered producer/consumer output contract

S1 local output-boundary repair only. Entry2026-10-04T14:03:27Z;
deadline14:48:27Z.45min active; regression120s/max3cycles. First reproduce the
old exporter mismatch; then minimally repair new consumer and affected fixtures.
Backup: specific closeout. No remote/model/old suite invocation.

Independent producer evidence: `full-path-resume1/fixture-manifest.json` inputs
instrument/vectors, `full-path-resume1/reference/result.json` output_counts and
hash keys, and the unchanged `modal-local-integration1/linux_runner.py` source.
No paths to actual input or prediction arrays are followed. Input identities are
recorded in prior-identity.json; selected metadata in producer-metadata.json.

| Instrument key and filename stem | output_counts |
|---|---:|
| unicef |17856|
| world_bank |39520|
| unhcr |132273|

Exact keys and counts required, total189649. `wb` is not an accepted alias.
Candidate additionally requires hash/file stems `unhcr-engineering-alpha025` and
`unhcr-final-e041`; neither belongs in output_counts or its total.

Producer source: lines103-106 read reference `world_bank.json`; lines164-186 use
`row['instrument']` for output filename/hash/count, checking len against vectors.
Lines194-196 write the two candidate extras and add only their hashes.
The original fixed scientific runner remains byte-identical in the new copy.

Production change: new exporter requires canonical world_bank; outer final gate
compares the exact count mapping, including integer types, instead of its sum.
Source relocation is restricted to contract.REMOTE_DIR and launcher source prefix.
The producer's temporary output root stays unchanged; each future Sandbox is new.
No runner/model rewrite, alias permissiveness, threshold or scientific change.

Focused regression: old mismatch reproduction; normal reference/candidate export;
canonical world_bank file path; wb typo; missing/extra keys in hashes and counts;
equal-total wrong counts; duplicate candidate extras in counts; corrupt hash;
absent output; reference export failure blocks candidate. Same production
export_mode/execute path, only external endpoints injected. Expectations are
derived from original producer metadata/source, not consumer constants.
Small `[]` output bytes and complete metadata envelopes are protocol fixtures,
not189649 generated predictions. Actual Linux/native/H100900s/release unverified.
