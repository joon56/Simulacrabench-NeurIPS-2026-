# E050/E051 diagnostic library implementation

Implemented only new bounded diagnostic tooling:

- `src/eval/recursive_candidates.py`
- `scripts/screen_e050_e051.py`
- `tests/test_recursive_candidates.py`

No old model/snapshot edits, no production selector, no commits, no full oracle
experiment launched by this worker. Root owns launch, decisions and release.

## Frozen protocol

Root's pre-execution correction is implemented: observed Adult seeds51/52,
5000 rows = 2600 FIT / 800 ORACLE / 800 SELECTION / 800 AUDIT. All2400 query
PREDICT blocks hidden before either model sees the frame. Script computes
labels only for ORACLE, preserves predictions for all2400, and never scores
selection/audit. Clean and unchanged household seed13 are diagnostic cases.

Adult uses existing `tests/e041_external.py` fixed preprocessing and schema
vocabulary protocol. Adapter preserves strings, changes public `options` to
native `values`, sets `gated_value='NA_GATED'`, and adds no gates. Source IDs
are retained only in provenance. Generic invocation uses the actual
`link_sharp.predict(..., layer_fn=supervised_layer, configs=hh_cap.CONFIGS)`
stack; it never passes Adult through the marker-based E025 fallback.

## Library interfaces

`e050_library(masked_frame, schema)` returns a dict:

- `base_raw`: original canonical E041 vector list, untouched.
- `base`: item -> query-by-class ndarray, in complete public class order.
- `arms_raw`: arm -> canonical raw vector list.
- `arms`: arm -> item -> query-by-class ndarray.
- `query`: positional frame indices, ordered ascending.
- `predicted`: PREDICT heads in schema order.
- `options`: full schema classes, including gated sentinel.
- `components`: disjoint lists of PREDICT names, including all heads.
- `diagnostics`: fit/query/evidence counts, original lambdas, E041 layer data.

Arms ordered `identity`, `zero`, `half`, `toward_one`, `one`. Identity aliases
the exact original raw vectors. Each other arm fully rerenders the unchanged
gate recursion with shared fitted products and captured evidence. Missing
lambda defaults to zero; transformations affect both buckets only where
evidence was captured. Empty evidence remains empty, with no dormant donor
extraction. Private copied function globals cache first-stage training,
probability maps, ladder selection/building and conditional agreement once
per frame; source module functions remain unchanged. No E049/PFN import.

`e051_library(masked_frame, schema, frozen_e050)` uses the same interface,
plus `tree` arrays. Arms are `tree_0`, `tree_0.25`, `tree_0.5`. Zero aliases
original E041 raw outputs. HistGBM parameters match registration; GIVEN-only
schema-coded features; classes>255 explicitly ordinal; fit-visible rows only;
trained classes map into complete schema order; singleton heads are one-hot
before .01 mixing with Laplace-smoothed fit-only marginal. CPU threads2.

`component_oracle(arms, oracle_labels, components)` consumes only already
sliced oracle arrays/labels. It chooses one constant arm per component,
pooling all component heads and oracle respondents. First arm is baseline.
Reported metrics include exact component and whole-arm bounds with official
.001 normalization/mixing floor, uniform reference, delta skill and skill/3.
No query-wise or continuous oracle is claimed.

Component exactness: every gate's variable PREDICT parent is joined with its
PREDICT child, including cross-section names. GIVEN parents remain fixed
observed boundaries. Recursion has no other cross-head belief dependency;
fitted products/evidence do not change across arms. Thus concatenating each
component's global-arm outputs equals rendering mixed component choices.
Regression test executes both methods through real `link_sharp` recursion.

## Frozen artifacts and commands

Default `docs/analysis/E050-outputs/{case}-seed{51|52}-*`:

- `libraries.pkl`: raw/mapped arrays, query alignment, diagnostics.
- `arrays.npz`: all family/arm/item arrays.
- `manifest.json`: source dependency hashes, masked frame/schema hash, input
  file hash and row identities for Adult, partition positions, package
  versions, timings, diagnostics, pickle/NPZ hashes.
- `oracle.json`: oracle-only results, explicit audit-not-evaluated flag.

All arrays and hashes are written before first oracle scoring. Cache hits
require matching protocol/source/frame hashes and verified pickle checksum.
Changed provenance is rejected instead of overwriting frozen results.

Run from repository root using existing environment (interpreter requires
sandbox escalation in this environment):

```
.venv/Scripts/python.exe -m pytest tests/test_recursive_candidates.py -q
.venv/Scripts/python.exe scripts/screen_e050_e051.py --case adult --seed 51
.venv/Scripts/python.exe scripts/screen_e050_e051.py --case adult --seed 52
.venv/Scripts/python.exe scripts/screen_e050_e051.py --case clean
.venv/Scripts/python.exe scripts/screen_e050_e051.py --case household
```

## Verification

TDD initial RED:9 tests failed due to missing new modules. Implementation
run:8 passed,1 strict floating-point assertion failed at .6000000000000001
versus .6; test corrected to tolerant numeric assertion. Final suite:
**11 passed in6.57s**. CLI `--help` succeeds without running fits.

Coverage: cross-section components/GIVEN boundaries, exact baseline renderer
identity, fit-once private globals/no mutation/fresh per-frame caches,
composition versus mixed full recursion, both lambda buckets, no dormant
evidence, absent-evidence exact fallback, whole-block label masking/rejection
of partial masks, actual HistGBM class mapping, singleton/unseen class floor,
>255 ordinal limitation, official oracle flooring and pooled constant-arm
scope, Adult string schema adapter, all2400 arrays persisted before800-only
oracle scoring, checksum and matching-cache reuse.

Costly E041 fit products are fixed in renderer unit tests; recursion itself
is real. Full actual E041 versus immutable snapshot parity on UNHCR, actual
observed oracle numbers and total runtime remain root's integration checks.
