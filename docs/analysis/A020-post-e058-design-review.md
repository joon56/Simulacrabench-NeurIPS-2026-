# A020 — Post-E058 controlled interaction design review
date-started: 2026-09-26
status: done
relates-to: A019 / E058 / prospective E059

## Goal and scope

Produce one actionable S1 handoff while preserving E058's fixed-active-family
STOP and all prior exposure. Input HEAD:
`1d223340d4e1fa3993b411dc5daafab9cb37d0cd`.
The latest user authorized continued review and recording rejected approaches.
This S0 performs document/source review, byte hashes and documentation only.
No model-cache deserialization, response projection, fit, prediction run, score,
submission, S3 work, commit or push. E059 is prospective, not reserved or run.

## Attempt log (chronological; design dispositions, not new experiments)

### v1 — Reopen E058 by changing its active mask: rejected

The original learned active set is empty. Changing that set inside E058 would
change its registered intervention. The existing identity certificate remains
valid and its STOP remains final. No threshold relaxation, favorable seed,
new head selection, marker deletion or E058 script rerun is justified.
This rejects the proposed procedure, not interaction efficacy on UNHCR.

### v2 — New base fit and new calibration: rejected for this task

The comparator frame and its cached first stage already exist. Refitting adds
training variation and recalibrating changes a second mechanism. A011's measured
replay mismatch is not proof a repair helps. No gain from such a repair has been
measured here. A missing or unusable cache must stop the proposed study, not
silently expand it into another base-fit/calibration project.

### v3 — Resume the cached full renderer across sessions: rejected

`src/eval/recursive_candidates.py:cached_renderer` owns in-memory memo closures.
`scripts/screen_e058.py:freeze` persisted state and raw baseline, not that
renderer. Calling a fresh renderer would fit again. A zero-base-fit handoff
cannot rely on that path. No renderer or fitted cache was executed here.

### v4 — Three-arm leaf-evidence comparison: retained for S1

Keep R, the E058 generic E041 baseline, unchanged. Construct A with additive
donor32 evidence and B with the same evidence construction plus pair terms.
Freeze first-order learned weights, candidate identities/order, original lambda
pairs, concentration buckets, base and parent beliefs across A/B.

The inherited section selector compares marginal/retrieval mixtures, not the
final deployment output (`src/models/supervised_retrieval.py:fit_sections`).
Thus its negative result is relevant adverse evidence, but it does not decide
the proposed separate comparison. Finite learned weights and retrieval share
exist even for the nonselected section. Do not change the stored active mask.

The mechanically eligible outputs are the leaves with positive original lambda:
EHREAS_BIR (.1,.1), EHREAS_OTH (0,.1), EHREAS_COR (0,.1). HOSPITALIZED is
unchanged and these leaves have no descendants. For each eligible row/item:

```
R = (1-lambda) * G + lambda * e_legacy
A = R + lambda * (e_additive - e_legacy)
B = R + lambda * (e_pair - e_legacy)
A_half = R + 0.5 * (A - R)
B_half = R + 0.5 * (B - R)
```

The common G stays fixed; no full renderer or new base fit is needed in this
algebra. Beta0 must reproduce A, not R. Unchanged outputs must remain exact R.
Probability validity and floating arithmetic still require S1 engineering
checks before scoring. This is a source-derived construction, not a completed
real-cache parity test or measured output change.

Query donor32 was never materialized by E058's inactive replacement path.
S1 must build it once from the saved GIVEN signatures and initial weights using
the exact existing candidate_indices rule, then freeze it for A/B. Training
donor32 is already captured. Neither is an enlarged or outcome-selected pool.

Use a single fixed half mixture, rather than the earlier proposed alpha grid.
This is a prospective simplification before any new responses: it retains
E058's largest registered shrinkage arm, removes alpha selection, and limits
the effective changed evidence share here to .05. It is not an optimality claim
or a threshold change to E058. Both B_half-R and B_half-A_half must qualify.
No automatic promotion of A if only A happens to improve.

### v5 — Byte-level provenance check: PASS; semantic check deferred

All 59 source hashes in E058 preflight match. Five local artifact hashes also
match, with no deserialization: first-stage.pkl, masked-frame.pkl, library.npz,
evaluation-keys.parquet and fit-keys.parquet. Detailed values:
[verification.json](A020-outputs/verification.json).
The E058 directory contains only those three E058 data artifacts and
library-started.json; no oracle/selection/audit marker was observed.
This checks recorded artifacts, not arbitrary unlogged access elsewhere.

No Python/WSL/bash process was returned by Get-Process. Win32_Process CIM access
was unavailable during the preceding review; no claim of system-wide process
visibility is made. No computation worker was started by this S0.

## Findings

1. [consistent] E058 closes the frozen inactive family, not the interaction
   hypothesis. New outer labels remain unopened according to the ledger and
   stage artifacts. Existing legacy evidence remains active in three leaves.
2. [consistent] A three-arm comparison separates a conditional beta increment
   from the bundled change relative to E041. It cannot establish superiority
   over all additive models: first-order weights remain fixed.
3. [consistent] Only a separate candidate construction can exercise this
   question; the E058 activation policy and STOP must not be rewritten.
4. [unchecked] Pair features might be constant within all useful query pools,
   donor labels might make evidence invariant, beta might fit to zero, or both
   gains might fail. S1 must stop at the earliest decisive gate, including
   before fit/response access where output invariance is provable.
5. [unchecked] Existing cache contents have not been decoded in A020. S1 must
   validate masking, groups, array alignment, evidence, weights and algebra.
   Hash agreement establishes provenance, not scientific efficacy.
6. [consistent] Reused inner roles are row-disjoint, not newly certified
   SSUID-disjoint training roles. Honest outer SSUID boundaries remain essential.
   Bootstrap intervals condition on the frozen trained/qualified policy; they
   omit training variation, earlier design choices and domain shift.

## Exposure and prospective decision

Preserve original5922 fit rows and inner roles. Old non-fit labels, including
calibration1866 and consumed E055/E056 evaluations, remain closed. Preserve A019
oracle1918/1124SSUID, selection2007/1130, audit2074/1177. Their GIVEN prediction
use already occurred in E058. Historical plus E058 use is17999 persons and
12339SSUIDs; full-source aggregate exposure also remains. No new independent
dataset or universally untouched holdout claim. This redesign is explicitly
informed by E058 inactivity and frozen lambda diagnostics.

S1 must register a new study before cache use or fitting. Proposed scope:
zero base fits, one beta optimizer, no refit, fixed half mixture, staged
oracle/selection/audit and two required comparisons. Oracle is only an exact
screen of the finite frozen output family, not an upper bound over all beta.
Selection requires both paired group-clustered means >2SE. Audit uses two
paired SSUID-bootstrap97.5% central intervals; require both lower bounds >0.
Bonferroni gives nominal simultaneous95% coverage if the marginal bootstrap
intervals are adequate; this is an approximation, not a finite-sample guarantee.
Exact formulas, thresholds, stage access and resources are in the handoff.

Main-task outcome: **S1 handoff ready for a bounded research study**, conditional
on its semantic preflight. No estimator was fitted or qualified here. No S2
candidate, release qualification, actual UNHCR gain or TEST choice follows.
The backup channel review was not activated because the main design is coherent
and its recorded artifacts are present. No second experiment is authorized by
the handoff if its gates fail; report the scoped failure and return to S0.

## Artifacts and preservation

- [Copy-ready S1 prompt](A020-outputs/s1-handoff.ko.md)
- [Byte-level verification](A020-outputs/verification.json)
- [E058 closeout](E058-outputs/closeout.md)
- [E058 exposure ledger](E058-outputs/exposure-ledger.md)
- [A019 exposure audit](A019-sipp-model-exposure.md)
- [A011 limits](A011-replay-bias-diagnostics.md)

E041 incumbent/E025 fallback retained; E057 parked; prior STOPs preserved.
S3 remains stopped and A018 remains user-unconfirmed. Existing user changes in
.gitignore, .claude/skills/paper-session/SKILL.md, .claude/settings.local.json
and trip/ remain outside this work. Documentation is left uncommitted under the
current no-commit/no-push constraint; latest permission added recording only.
