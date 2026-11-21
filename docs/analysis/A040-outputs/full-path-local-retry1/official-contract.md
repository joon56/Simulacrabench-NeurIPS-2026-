# Official runtime schema contract and bounded repair

Source: local official starter-kit HEAD `ee427a94f6cc6a0d9d653b6be68c835a032e7552`.
No upstream update or hosted deployment identity claimed. Exact file hashes are
in `frozen-inputs/manifest.json` and `schema-manifest.json`.

- `external/starter-kit/make_sandbox.py:35` loads the explicitly supplied config
  and checks phase privacy settings. Line50 defines `load_schema`; line70 assigns
  `schema['gated_value'] = config['gated_value']` unconditionally. It validates
  declared nonempty/string/non-null options, sentinel exclusion, gate parents,
  dataset metadata and complete split counts. No local defaults replace errors.
- `config.yml:15` is the sentinel authority. `options_for` at line147 retains
  declared option order and appends the config sentinel once only for gated items.
- `score.py:627/633` uses those loaders; `stage` at line338 serializes the runtime
  schema at lines353-354. Its embedded driver reads that JSON at line81 and calls
  `main.predict(frame,schema)` at line86. The scorer/main/generator were not run.

`schema_entry.runtime_entry` directly delegates to those official loader functions.
The new generator and runner both call it. It reads public source/config/schema
only; it neither generates responses nor scores nor imports a model. It returns
the runtime schema plus raw/config/loader hashes, ordered item/options metadata
and an ordered compact UTF-8 JSON runtime hash. Raw/runtime hashes are distinct.
The runner checks equality with metadata recorded at generation before prediction.
That runtime assertion remains unexecuted because resource preflight blocked.

All3 actual public-schema entry test passed in0.8901341s, including unchanged
injected role/branch/logger tests. Direct official/helper JSON equality, item/
GIVEN/PREDICT/option order, exact widths/splits and189649 output-vector arithmetic
were checked. Raw UNICEF/WB omit the field; UNHCR supplies it. Altered metadata
copies verify that config overrides all three raw cases. Eleven expected negative
cases preserve errors (ten invalid schemas and one invalid config); original
files unchanged. AST checks verify both call-site bindings without importing the
side-effectful scientific runner. This is not actual-model or whole-run PASS.

`source.diff` records only new common entry/test, calls and metadata checks,
attempt paths and deadline. Adapter/orchestration/observer/telemetry/old role tests/
dependency lock remain byte-identical. Existing assertion ASTs unchanged. No
change to model settings, generation values, seeds, splits, alpha/guard or tolerance.
