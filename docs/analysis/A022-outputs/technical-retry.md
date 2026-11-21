# A022 technical failure and correction, before retry

2026-09-27. Original registration and initial script preserved as registration.md
and audit_keys.initial.py.txt. No completed verification.json existed.

Sandbox execution could not access the Python313 base interpreter. No Python
audit ran in that attempt. The same existing interpreter ran after sandbox
escalation; no environment was installed or changed.

The first actual key projection halted at initial script line86: eligible person
role totals were compared to a014-partitions.json's complete month12 totals.
Source/key file hashes and eligible39131/17314 had passed. No historical/query
key Parquet had yet been decoded, and no residual inventory was reached.

Root cause established from scripts/audit_a014_sipp.py lines151-154,178-180,226-228:
the partition manifest stores all39513 month12 persons, not39131 eligible persons.
Both use the same original role algorithm. This is a verifier scope error, not a
source/hash discrepancy or evidence against data eligibility.

Correct only the population of the manifest check: compute/check original roles
on the full projected month frame, then carry those unchanged tags into the same
A019 eligibility filter. Source projection, exclusion rules, role namespaces,
counts, historical samples and every subsequent gate remain fixed. No model
response/GIVEN columns, cache, fit, score, seed search or new roles.

One technical retry is recorded as a deviation from the planned single scan.
The first attempt remains failed; only corrected checks can establish key PASS.
No statistical STOP or research threshold is changed. Any new unexplained
data/hash mismatch stops this audit; do not relax it to obtain PASS.
