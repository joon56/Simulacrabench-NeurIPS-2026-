# A019 — SIPP model-exposure entry audit
date-started: 2026-09-26
status: done
relates-to: E041 / E055 / E056 / prospective donor-interaction research

## Contract fixed before key projection

User authorizes an entry audit, then only on PASS a single fixed donor-pair
interaction study. Input HEAD eaed6a5a4b618acba27e378a17ef56267c08129c matches
S0. No E058/A019 collision found. A019 records the audit; E058 is NOT reserved.
Audit clock10:00:54UTC; deadline10:30:54UTC. Zero fits/new scores. Preserve
user changes in .gitignore, .claude/skills/paper-session/SKILL.md,
.claude/settings.local.json and trip/. No active Python/WSL observed at entry.

Read only SSUID, PNUM, MONTHCODE, ERESIDENCEID, THHLDSTATUS and TAGE_EHC from
the existing A014 Parquet. Hash raw files for provenance without decoding
response columns. No target, unused prediction arm, score array or existing
pickled model cache is opened. Existing requested aggregate A014/E055/E056
records are historical development exposure, not new response scores.

Reconstruct E055's first12000 eligible persons by its original
SHA256(NUL-joined E055-sample-v1,SSUID,PNUM). Verify exact sample/source hashes
and person/group role counts against both E055 manifests and E056 manifest.
Group-fit5922 is the only future permitted fitting subset. Exclude every SSUID
in the whole12000 from future evaluation, across both views and all roles.
Preserve calibration1866 and all prior consumed roles; no label reassignment.

Repository/code/history audit identifies A014 preprocessing and E055/E056 as
the only recorded SIPP model runs. A014 analyzed full-extract aggregates but
did not fit models. E057 and its S2 use synthetic data, not new SIPP fits.
Search tracked code/history plus ignored diagnostic scripts; classify matches
and preserve hashes. Inability to establish a bounded complete history is STOP.

Before seeing remaining counts, fix new selection: sort remaining SSUIDs by
SHA256(NUL-joined A019-evaluation-sample-v1,SSUID), tie-break SSUID; take a
prefix of complete groups until the next group would exceed6000 persons.
Do not skip an oversized boundary group or split a group to fill the cap.
Assign whole groups independently by first8 bytes of
SHA256(NUL-joined A019-evaluation-role-v1,SSUID), big-endian integer modulo3,
mapping0 oracle/1 selection/2 audit. Require each role >=1000persons AND
>=500SSUIDs. No alternative namespace, seed, sample or dataset after counts.

PASS requires provenance, exclusions, intact groups and all three size gates.
Otherwise STOP with A-record only, no E number. All keys/row mappings stay in
ignored external/a019; tracked records hold aggregates and hashes only.
Same A014 source/preprocessing/aggregate exposure remains; never call this a
new independent dataset. Model-use exclusion and unopened model scores are
separate claims. No new scientific efficacy conclusion from this audit.

## Attempt log

- Entry/read-only history audit: current tracked source hits only A014 audit,
  E055/E056 screens and fixture tests. Git source-history matches only commits
  2a52f18,df10864,527ddd2. Initial sandbox scan encountered permissions in old
  temporary grader environments; authorized elevated read resolved the scan.
  Third-party site-package substring hits are not SIPP project use.
- Key projection completed10:06UTC, within30min;6.8364s command wall, zero fit
  and zero new score. Eligible39131people/17314SSUIDs. Used12000people/8908SSUIDs
  excludes24432people; remaining14699people/8406SSUIDs. New complete-group
  prefix5999people/3431SSUIDs: oracle1918/1124,selection2007/1130,audit2074/1177.
  No group crosses roles or historical use. All minimum counts PASS.
- Both E055 and E056 manifests match exact source and reconstructed sample/roles.
  Ignored tmp/verify_e055_artifacts.py is frozen verification only, not a new fit
  or sample; official Census input-example.py is documentation, no recorded run.
  History and current code search find no other project SIPP model use. Scope of
  this evidence is repository-recorded work, not arbitrary unrecorded activity.
- Existing A014 extraction and earlier verifiers materialized full-source
  responses for preprocessing/checks. Thus unused-for-model is NOT never-seen.
  This distinction is retained in E058; no new independent dataset claim.
- PASS permits E058 registration. E056 calibration and all old non-fit labels
  remain unopened. Artifacts: A019-outputs/entry-audit.json, scripts/audit_a019_exposure.py;
  keys/hashes under ignored external/a019 only. No scientific efficacy verdict.
