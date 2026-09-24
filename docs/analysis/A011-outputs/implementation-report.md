# A011 replay diagnostic implementation handoff

Files added: `scripts/audit_replay_bias.py`, `tests/test_replay_bias.py`.
No source model, old script, submission, environment, or commit changes.
No expensive fits executed by this worker.

Implementation follows preregistration 21931ab and fixed A011 protocol: clean,
household seed13, public Adult sample seed53/5000. Whole-row CAL400/CTRL400
split seed5301 comes only from visible TRAIN. Existing DEV labels never enter
scoring. Adult uses `load_observed` + existing `adapt_adult`, not old masked split.

Each arm uses its own `cached_renderer` namespace and unchanged `hh_cap.CONFIGS`.
Honest callback captures full heads, original evidence/lambdas and full recursive
outputs. Included-label callback captures both CAL/CTRL full heads and returns
empty evidence. Honest CAL and CTRL remain masked; included CAL labels remain
visible and CTRL remains masked. No new model or weight optimization.

Readonly captures and exact own-evidence inversion are checked before scoring.
Missing evidence stays missing. Official full-vector normalization and floor
apply to log-score contrasts and official gradients. Legacy gradients reproduce
clipped base truth probabilities and clipped mixture; positive slope means more
evidence pressure, with right derivative at lambda0/clipping kink. Gate-base
derivatives hold upstream beliefs fixed, not total descendant derivatives.

Reports include CAL/CTRL membership contrasts and their difference; gate/full
head log-score mismatch and total variation; all/gated/ungated and per-item
summaries; legacy/official slopes and sign flips for item/buckets with >=30 rows.
Respondent bootstrap1000 seed5302 samples CAL/CTRL independently, including
pooled gradient resampling that preserves partition sizes. Intervals condition
on fitted models, ignore training variation, shared donor/household dependence,
and multiplicity. No outcome-driven extension.

Capture format finalized before any fits: deterministic gzip-compressed
protocol5 pickle retains all captured evidence and full recursive outputs.
NPZ contains dense CAL/CTRL heads, derived diagnostic views and partitions,
avoiding hundreds of thousands of tiny evidence members. Manifest binds source,
frame, partition, compressed/uncompressed capture, NPZ hashes and package
versions. Existing artifact refusal occurs before loading/fitting. Capture,
NPZ and manifest precede label mapping/scoring.

Verification:

```
.venv/Scripts/python.exe -m pytest tests/test_replay_bias.py tests/test_recursive_candidates.py -q
22 passed in 6.82s
```

Tests cover whole-block masking/DEV retention; actual renderer callback and
included empty layer; inversion and lambda1 refusal; independent finite
differences including unequal vector sums; floor right derivative; constant
bootstrap contrast; gate/membership score signs and minimum bucket size;
missing evidence; artifact refusal before loading; compressed freeze and hashes
before scoring. Test-first run produced expected missing-module failures.

Independent reviewer reported no pre-fit blocker. Root notified final GREEN
and script/test freeze; root owns fixed fit execution and artifact review.
Sandbox Git verification hit dubious ownership; no global configuration edit
attempted. Root handles repository/hash checks in its authorized context.

CLI (root executes at most two simultaneous jobs, two threads each):

```
.venv/Scripts/python.exe scripts/audit_replay_bias.py --case clean
.venv/Scripts/python.exe scripts/audit_replay_bias.py --case household
.venv/Scripts/python.exe scripts/audit_replay_bias.py --case adult
```
