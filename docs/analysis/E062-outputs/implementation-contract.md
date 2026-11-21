# E062 implementation and reproduction

Source: `src/models/wb_ordinal_heads.py`. Initial policy: `registration.md`;
actual pre-pipeline source/data/schema/role freeze: `frozen-inputs.json`.
These are separate records. Entry remains unchanged; `source-supplement.json`
adds two previously read production dependencies before execution.

## Minimal intervention

The original nominal network is constructed first. Only the sixteen fixed WB
full heads are replaced by six affine rows copied from original rows 0..4 and 6.
Their forward output is seven normalized log probabilities: five continuation
logits and a separate Not answered logit. No random draw is added. The unchanged
pooled cross-entropy consumes these log probabilities as logits; normalization
is mathematically redundant. Stable log-sigmoid arithmetic avoids subtraction
of nearly equal probabilities. Existing `_proba_maps` applies softmax once.
There is no new output floor, clamp, prior, smoothing or auxiliary objective.

`_train`, `_train_on`, and `tune_and_train` preserve original training and selection
logic, with only an ordinal-index argument and the network factory changed.
The original source modules and both submission snapshots remain untouched.
WB uses the original link-sharp/hh-sharp pipeline, configs and final renderer;
UNICEF and UNHCR dispatch to E041's original supervised-retrieval source.
The full final pipeline is compared, including possible changes to the other
sixty WB heads through the trunk, config/w selection, and lambda replay.

No intermediate outer-fit refit is introduced. The selected inner-stop network
is used for outer selection; the final network refits all visible TRAIN rows,
including when selected w=0. Lambda replay is in-sample reuse, not a new audit.
The target schema must match all sixteen exact seven-class ungated heads.
Missing targets, altered class order, or gates do not permit partial rescue.

## Information and instrumentation

Model workers request Parquet TRAIN rows with generated columns, and DEV rows
with GIVEN columns only. They never request TEST rows or DEV PREDICT columns.
The adapter removes EXCLUDE columns and adds a completely missing DEV PREDICT
block before the official phase-1 sampling function. Frozen role and masked-frame
hashes must match in every worker. Source tracing verifies actual neural target
row indices against inner-train, inner-stop, outer-selection and final-refit
roles, without replacing the learning functions.

The evaluator starts only after three model completion/resource receipts and all
nine raw output hashes pass. It is the only worker requesting DEV answer columns.
It uses official `check`, `floored` and `score`, with floor .001, in process.
This is not the official CLI, ZIP checker or all3 release qualification.
Old predictions and model caches are not reused.

## Reproduction record — not repeat authority

Use the existing `.venv/Scripts/python.exe`, from repository root, with `-X utf8 -B`.
The controller sets numerical thread limits2 and disables CUDA. Successful work
must not be rerun in this session. Its exclusive output files/latches preserve
attempt history; a future independently authorized reproduction needs a new
output location, budget, deadlines and registration. Do not delete current latches.

Commands executed/planned in the fixed order:

```powershell
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e062_wb_ordinal.py tests --attempt 1 --only tests.test_wb_ordinal_heads.OrdinalTests.test_probability_and_nll
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e062_wb_ordinal.py tests --attempt 2
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e062_wb_ordinal.py tests --attempt 3 --only tests.test_wb_ordinal_heads.HarnessTests
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e062_wb_ordinal.py prepare --attempt 1
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e062_wb_ordinal.py E025 --attempt 1
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e062_wb_ordinal.py E041 --attempt 1
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e062_wb_ordinal.py candidate --attempt 1
& '.\.venv\Scripts\python.exe' -X utf8 -B scripts/check_e062_wb_ordinal.py score --attempt 1
```

Only corresponding resource/completion receipts prove a command completed.
`tests-01` is the intentionally failing initial shape test against the preserved
initial stub. `tests-02` covers ten new candidate contracts; `tests-03` covers
three later-added harness boundaries without repeating the earlier ten.
Small tensor/backward and fake-endpoint tests do not constitute optimizer fits.

## Verification boundaries

Tests cover both dtypes, independent probability/NLL/gradient formulas, extreme
logits, empty risk sets, Not answered gradients, unchanged pooled denominator,
both configs' exact unaffected initial parameters/RNG, masking, schema rejection,
small-fit fallback and w=0 final-refit orchestration. Underflow to raw zero at
extreme logits is expected and separately tested; official final floor remains.
Fake endpoints prove their bounded orchestration contract, not model efficacy.
No independent oracle is available; all synthetic comparisons are engineering.
