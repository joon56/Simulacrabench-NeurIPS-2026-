# A018 — Frozen TEST selection and delivery

Date: 2026-09-25. Integration owner: S3 session, restricted to A018 outputs
until concurrent-session ownership is resolved. Input HEAD: 4166130.
Existing dirty user files, A017 outputs and E056 work are not owned by S3.

## Prospective contract — fixed before additional evaluation

Decision: select one existing predictor for TEST and preserve a separate fallback.
No new model, ensemble, calibration, hyperparameter search, hosted upload or
private response access. Main task: compare qualified candidates, close phase-2
engineering gaps and freeze matching model/method/release artifacts. Backup:
unchanged E025 if E041 fails a mandatory technical or resource gate; if both
fail, declare delivery blocked rather than weaken a threshold.

Comparison set: E025, E041, E044, E045, E047, E049 and E052, at their historical
dated submission bytes. These have completed submission qualification, not
necessarily phase-2 qualification. E044 remains an adverse control, not promoted
because it is included. E054 is an intentional measurement ablation, excluded
from performance selection. E042/E043/E046/E048/E050/E051/E053/E055 have no
qualified replacement release; E056 is ongoing research, excluded even if a
concurrent proxy result arrives. Older superseded variants add no distinct
supported finalist beyond E025; their historical records remain unchanged.

Selection order (qualitative, no invented gain forecast):
1. Valid archive, exact predictor provenance/parity, three-schema official
   phase-2 validation, no hidden-label access, compatible licensing/disclosure.
2. Absolute clean phase-2 skill difference <= .002 per instrument versus E025,
   plus relevant E041 comparison. This is release policy, not transfer evidence.
3. Target relevance and actual hosted evidence, including adverse/flat readings,
   selection exposure and conflicting observed/synthetic channels. A single
   rounded DEV best is insufficient by itself; no claim of a precise TEST gain.
4. TRAIN+DEV retraining behavior, activation/rollback semantics, calibration
   leakage, reproducibility, full-run time and memory, and dependency burden.
5. Prefer E041 if it closes engineering gaps and no alternate has stronger
   transferable evidence with comparable risk; otherwise E025. No extra fits of
   flat/adverse candidates merely to rank synthetic scores.

Known evidence before this protocol: status/log, A012 phase-2 scorecards,
E041 method and source, experiment qualification summaries through E055.
E041 hosted .64/.52/.49/.92 versus E025 .63/.52/.49/.89, user-reported;
E044 .63 adverse; E045/E047/E049/E052 .64 without best update unresolved.
A012 phase-2 E041-E025 0/0/-.000508448996; 442425-vector exact parity;
367.177 s separate-process official total. None is confidential TEST evidence.

Allowed data: public schemas and existing synthetic TRAIN/DEV/TEST fixtures.
Synthetic TEST already exposed for engineering, never called untouched.
No Adult/SIPP label access, new proxy score, or E056 score access in this task.
Model runtime may use visible TRAIN+DEV labels and all GIVEN values; whole
synthetic TEST PREDICT blocks must be masked before predict. New local results
may reject unsafe delivery, never tune predictors or reselect on sandbox gain.

Compute cap: one heavy process at a time; at most two unchanged all-three
single-process rehearsals (E041/E025), plus one official all-three E041 run,
35 minutes total model execution. Existing unchanged official/source evidence
may be reused only after hashes and raw parity are reverified. Each full run
must finish <3600 s and local process peak working set/private commitment
<16,000,000,000 bytes; report Windows CPU limitations and lack of hosted H100
measurement. Stop our own worker on the limit. No competing fits permitted.

Engineering change cutoff: 2026-11-12 00:00 UTC / 09:00 KST. Preferred user upload
by 2026-11-13 00:00 UTC / 09:00 KST. Current artifact freezes at this session's
manifest timestamp. Before cutoff, reopening needs a separately registered
decision and full revalidation; after cutoff only organizer-required contract
fixes with logged revalidation. Live rules must be checked again at upload.
Official API checked this session: TEST Nov 1 00:00 UTC to Nov 14 00:00 UTC,
one submission/team, 3600 seconds. No TEST upload is authorized here.

## Execution plan

- [ ] Freeze candidate/source/archive and scorer/data hashes; save minimal
  official schedule/terms evidence and inspect candidate records.
- [ ] Reverify A012 frozen parity/provenance; rehearse E041/E025 sequential
  three-instrument calls in one process and record peak memory/activation.
- [ ] Check final archive layout and official phase-2 all-three results.
- [ ] Resolve release-license scope; reconcile and visually verify four-page
  E041/E025 methods with code, development disclosures and current rules.
- [ ] Record selection, residual uncertainties, exact paths/hashes, immutable
  freeze manifest and result/failure arms; preserve fallback separately.
- [ ] After integration ownership is confirmed, update handoff, verify files,
  commit only owned work, push and check remote HEAD. Never upload to TEST.

## Results

Pending authorized checks. This section will record outcomes without changing
the prospective comparison set, gates or caps above.
