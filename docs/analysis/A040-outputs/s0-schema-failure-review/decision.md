# A040 S0 — official schema entry repair, 2026-10-02 KST

**RECOMMEND_SEPARATE_S1_SCHEMA_REPAIR_AND_FULL_PATH_RETRY.**
Accept LOCAL_FULL_PATH_FAIL as an input-preparation failure, with scientific
execution0. Original failure, local retry1 PASS and this failed full-path attempt
remain separate historical results. No S2 candidate.

## Root cause and official evidence

Reviewed full-path-local closeout, verification, resources, source-manifest and
generation-failure, plus generator/runner/layout source. Both generator and runner
read raw JSON directly; layout requires a runtime-only field. Spy fixtures supply
that field themselves and did not exercise the real entry boundary. The previous
S0 handoff should have explicitly required runtime-schema preparation and actual
all3 schema coverage. This was a preventable harness integration omission, not a
model or hardware result. First-error STOP was correctly applied by S1.

The official **local starter-kit source** resolves the missing contract:

- `external/starter-kit/make_sandbox.py:50` defines `load_schema(path, config)`;
  line70 unconditionally assigns `schema['gated_value'] = config['gated_value']`.
  It also validates options, parent references, dataset metadata and split counts.
  Do not replace it with a guessed default or setdefault: config overrides even an
  already present raw field. No raw JSON edits are required.
- `config.yml:15` defines `NA_GATED`; `options_for` at make_sandbox.py:147 appends
  the sentinel only for gated items, last, preserving declared option order.
- `score.py:633` invokes that same loader; lines353-354 serialize the normalized
  schema to the driver; the driver reads it and calls predict at line86 onward.
  `README.md:192` describes the runtime schema as the data file plus this config field.
- Original E041 accesses the runtime field, consistently with that contract.

Starter-kit local HEAD `ee427a94f6cc6a0d9d653b6be68c835a032e7552`; relevant source/
config/schema paths show no tracked modifications in the scoped status query.
File hashes identify the inspected bytes in verification.json. No live upstream
or hosted deployment identity claimed; no loader/model/test was executed by S0.
This is sufficient for the local repair contract. No organizer inquiry, new web
survey, sentinel invention or separate information-only S1 is needed.

## Decision, cost and next scope

Main: one separate S1 copies the failed code into a new attempt directory, shares
the official loader/config between generation and runtime entry, proves the
contract on all3 actual public schemas without models, then attempts the already
specified full-shape reference and candidate once each. Model/seed/head/context/
selection/refit/threshold/tolerance stay fixed. Existing installation, PyYAML6.0.3
and organizer runtime approval are available; no reacquisition/reapproval needed.

This change answers a concrete unresolved full-path question with no new real-label
exposure. Repeating the old spy alone would not; packaging/renting hardware now would
not. No scientific failure supports abandoning or retuning the candidate yet.
Success is not guaranteed, and further unrelated failure must not become an
unbounded repair loop. Backup is a failure/incomplete closeout only.

[Prepared S1 handoff](s1-schema-repair-handoff.ko.md): task120min; model-free checks
<=60s; full input generation1 attempt; reference<=900s then candidate<=900s, at
most2 scientific processes/1800s, existing RTX3070/CPU2/host16GB. Preserve first
unexpected-error stop; expected negative regression assertions are not unexpected
failures. No regeneration, additional scientific runs or post-result code rescue.

The earlier full-path contract continues:189649 all3 vectors, actual E041 controls,
UNHCR F6279/S1000/E1000 and final8279 context, separate natural S/E decision and
engineering forced-active path. RTX resource outcomes do not certify H100 timing;
local PASS is not empirical or release PASS. No automatic S2 or paid-resource step.

## Current evidence and preservation

Generator failed once before any response inputs/outputs; only fixed role-position
metadata exists. Scientific freeze was never reached. The source-manifest is
explicitly POST_FAILURE_EVIDENCE_NOT_SCIENTIFIC_FREEZE, not retrospective registration.
New model calls0. Historical scientific total remains2, child51.3160111s/
parent54.0961857s, fit230/predict232/load4. Model-free2.09376s and failed generator
tool wall.7898181s are preparation costs; full runtime/memory/parity remain unknown.

125 allowed preservation checks and19 post-failure code/document/schema identities
match.154 downloaded-source/checkpoint entries excluded. No prior fake responses,
model/cache, protected keys/Parquet/NPZ or VAF read/hash. Role metadata is not a
response record. Only this new S0 directory and status/log additions written;
failed source/role arrays/history unchanged. No tests, repair, generator/model call,
agents/contact/cloud/ZIP/upload/commit/push.

S0/r4 at C:\Users\USER\Desktop\SimulacraBench. Ordered entry reads in987e7c/9c8d23;
source/artifact evidence0d9e8c/38dc26/66715e/ea111d. Workflow hash in verification.
HEADa43f4379ec78dbc2de260463eef67bb1d567d7e1; dirty work preserved; no visible Python/uv
jobs in limited process-name check. Systematic-debugging/karpathy review continued.

E041 incumbent/E025 fallback; E057/E060/E061 parked; all STOP/HOLDs, A039,
A_half nonpromotion, A018 unconfirmed/S3 stopped retained.17999people/12339SSUID,
A022 original roles/aggregate history, E059 consumed oracle/selection and protected
audit2074/1177/calibration1866 unchanged. Installation and runtime-policy resolved.
