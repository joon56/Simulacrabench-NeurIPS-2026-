# A014 - Observed person-level gated channel
date-started: 2026-09-24
status: complete
relates-to: A011 / A013 / E053 / E041

## Goal

Determine whether official SIPP2023 hospital responses support a faithful,
leakage-controlled observed test of calibration inside gate recursion.

## Attempt log

### v1 - Protocol before data inspection

User approved A013's sequence. Plan docs/plans/2026-09-24-A014.md fixes source,
month, target block, candidate inputs, partitions and accept/reject criteria.
The historical E025 .79 base+.10 evidence motivates examining calibration of
useful evidence; it is not E041's decomposition or recoverable-gain estimate.
A011 documents replay/deployment mismatch, not a demonstrated beneficial repair.
E053's ungated Adult stop does not test this natural parent-child channel.

No model fits, candidate scoring or new experiment registration at this point.

### v2 - Observed extraction and independent acceptance

Protocol ce097c5 preceded response inspection. Official ZIP109036604bytes,
SHA2569c5363d56aca2041db20d46d17b81e9be931eb5b18bd5f5238b367d2dd7fb74b;
one3,726,010,471-byte CSV streamed using21 selected fields.476744 person-month
rows,39513 month12 persons,39131 eligible,3593 hospitalized. No duplicate
person-month keys, invalid eligible parent/reason, ambiguous reason blank or
parent-child gate contradiction.35538 AHREASON0 rows have all six reasons
blank; flags1/2/3 have only1/2 answers. Imputed responses retained.

All six demographic candidates usable; no exact target copies. EEDUC/EMS
5598 blanks exactly match TAGE<15;33533 age>=15 rows have no such blanks,
confirmed independently. One reference month prevents
repeated annual responses appearing in different roles. SSUID groups do not
cross roles;17643 eligible monthly households,11404 with multiple persons.
Restricted response extract and keys remain ignored under external/sipp-2023/.

Six behavioral tests PASS after RED; independent metadata and cached-data/code
reviews PASS. Source hashes and original registration bytes retained before
the streaming run. See A014-outputs/data-audit.json, pre-run.json,
audit-registration.md, metadata-review.md and audit-review.md.

Decision: ACCEPT as an observed exact-gate structural proxy only. Processed US
annual hospital data do not reproduce approximate refugee-survey gates, prove
concentrated donor activity, or establish calibration headroom. Aggregates were
inspected before modeling; no untouched-population claim. No model scored yet.

### v3 - Conditional oracle registration

E055 registers the finite existing12-point E041 share domain with full star
recursion, distinct from E053 ungated separation. Resource cap12000 persons
selected by fixed ID hash, not response values, before model fitting. The two
A014 role views overlap and serve structural robustness, not replication.
Only oracle-role model scores will be opened first. Both skill/3 gains must
exceed+.005+1e-10 before any learned calibrator. See E055 for complete scope.

### v4 - Coupled oracle executed; conditional learner stopped

Reviewed implementation df10864 preceded both fits. Same fixed12000 people,
person/group oracle1850/1872. E055 full-star finite maxima yield skill/3
+.000113126178/+.000102390016, both STOP against+.005. Exact original and
selected renderer parity; all144 root scenarios frozen before oracle scores.
Natural concentrated counts5/517 and changed child vectors confirm recursion
was exercised; legacy evidence returned in both fits, no dormant materialization.
Independent frozen-artifact recomputation verifies results and data boundaries.

A014 channel acceptance remains valid. E055 rejects only its registered family
on this observed proxy; not a hidden UNHCR ceiling or proof calibration cannot
help elsewhere. No calibrator, source model or submission ZIP built. Calibration,
selection and audit model scores remain unopened. E041 retained, E054 parked.
