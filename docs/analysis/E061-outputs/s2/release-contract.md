# E061 S2 implementation and release contract

Frozen before any S2 model execution. User-authorized A034 handoff is the design.
Root is sole writer after explicit user confirmation. Workflow r4, entry.json
records actual reads, identities and strict deadline. No git actions.

## Fixed architecture and implementation steps

1. Add only assemble_e061.py and check_e061_release.py, with new assembly-boundary
   tests. Preserve E041 bytes as prefix; bind its final predict as the control.
   Copy the source link_sharp renderer with tune_fn into a separately named
   function. Rename every E061 top-level function/class and its references.
   Map module references explicitly; never overwrite _Net/_train/_train_on/
   tune_and_train or E041's stored predict functions.
2. Run new namespace/control/AST/import and tiny no-fit network parity tests.
   Expected missing-assembler RED is counted; no original successful suite rerun.
3. Recheck allowed frozen identities, Python/numerical versions, CPU2/GPU-off,
   phase1 rows/masking/split hashes and nine allow_pickle=False reference arrays.
   No identity repair by refitting. Freeze assembled source + contract + SCORES.
4. One assembly all3 worker, exact official contract and max raw deviation
   <=1e-10 from frozen candidate; raw sum error<=1e-6. Controls<=1e-10 versus
   E041, UNHCR at least one difference>1e-10. All heads retained. Use frozen
   E041/E025 arrays and scores, no baseline prediction. Per-instrument absolute
   E025 skill delta<=.002 and candidate>=E041-.002. No positive-gain gate.
5. Package exclusive new snapshot/ZIP; root main.py + NOTICE.txt only.
   Extract under s2; require byte identity. Official ZIP checker then original
   score.py CLI phase1 for each of three instruments. Preserve official logs,
   require PASS and raw predictions<=1e-10 from S1, skill agreement<=1e-12.
   Original official file is never edited; three subprocess startup times and
   preparation/verification overhead count in one<=900s monitored suite.

## Data and instrumentation

Only three named synthetic Parquet files and nine explicitly authorized S1 NPZ.
Read Parquet with TRAIN/DEV filter. Validate against S1 hashes/row/split/frame
identities before predicting. Official CLI receives a phase1-only staging copy
under s2, derived from those same rows (no regenerated data/new seed/TEST read).
Models receive official sample_rows masked frame, not DEV PREDICT truth.
This is exposed synthetic engineering evidence, not an independent audit.

Measure neural/metric/full-stack entries including failures with a stdlib-only
observer. The observer configures identical CPU2 torch settings, checks _targets
row boundaries and logs counts; it does not replace predictions/loss/selection.
It is outside the submitted archive. Run original score.py with the extracted
main; package imports must not need repository paths. All instrumentation and
staging overhead remains included in measured worker wall time.

## Resources and stop rules

Whole session <=120min with fixed conservative deadline14:20Z; worker cumulative
<=2400s includes tests, preflight, packaging/checker and all failures. Each
assembly/official all3 suite <=900s including startup. One heavy worker, CPU2,
GPU disabled; owned controller+descendant RSS/private commitment each<=8GiB.
Windows MemoryTree sampling .1s; unavailable counters/cap/timeout STOP.
Only owned worker descendants may be stopped.

Default6 full-stack/18 neural/16 metric calls. Maximum9/27/24 only with recorded
specific assembly/harness defect and preserved failed attempt, same time budget.
No result-driven repair, forced activation, alternative model or baseline refit.
Success means RELEASE_QUALIFIED_FOR_USER_REVIEW, never hosted improvement or
automatic adoption. Failure backup is <=30min closeout inside the same deadline.

## Preservation and release reading

Original S1 source/results/manifests, old snapshots and tree untouched. Existing
A034 status/log additions are normal; new S2 status/log append is separately
identified. Entry hashes bind protected text/source and authorized references.
Keep17999people/12339SSUID, A022 roles, E059 consumed oracle/selection and protected
audit/calibration; all STOP/HOLDs and A_half nonpromotion. E041 incumbent,
E025 fallback, E057/E060 parked; E061 parked pending user review. A018 unconfirmed.
No upload/login/commit/push/S3/TEST work. Read SCORES for frozen hosted arms.

## Completion evidence

Persist source/archive manifests, fixture logs, per-suite resources/call counts,
raw parity/output contracts, official scores, exposure ledger, closeout and S0
handoff. Sum S2 measured costs with S1 historical1098.5227877s and9/27/16 calls.
Do not rerun a successful stage without a documented changed/invalid boundary.

