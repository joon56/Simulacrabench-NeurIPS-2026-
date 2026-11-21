# E062 S1 closeout — WB16 conditional ordinal heads

**EXPLORATORY_SOURCE_QUALIFIED; S0 review required.** Preregistered source-level
technical, exact-control, local-resource and per-instrument regression gates pass.
This is neither actual WB efficacy nor release/TEST qualification. No S2 work began.

## Observed results

Already-exposed synthetic TRAIN/DEV; official in-process floor .001 and skill/log
score functions. All nine raw outputs froze before evaluator DEV-answer access.

| Instrument | Clean E025 skill | Clean E041 skill | E062 skill | E062−E025 | E062−E041 |
|---|---:|---:|---:|---:|---:|
| UNICEF | .5006484231 | .5006484231 | .5006484231 | 0 | 0 |
| World Bank | .4547173074 | .4547173074 | .4549896845 | +.0002723772 | +.0002723772 |
| UNHCR | .5629488737 | .5624627289 | .5624627289 | −.0004861448 | 0 |

Each difference exceeds the fixed −.002 gate. The UNHCR loss versus E025 is
retained and reported; its output is exactly E041's control. UNICEF and UNHCR
candidate–E041 raw max difference0, including identical serialized raw hashes.
WB35613/39520 vectors change; max absolute raw difference .16004160046577454.
Thus this is not NO_OP. Each procedure emits UNICEF17856/WB39520/UNHCR132273,
total189649 vectors; canonical shape, finite/nonnegative/positive mass and raw
sum-error<=1e-6 checks pass. Largest observed sum error across nine outputs is
2.8615613700821996e-7. Raw zero entries are permitted; official final floor is
applied only in the evaluator, while original selection-time floor is preserved.

**The target16 did not improve.** Descriptive mean log-score differences versus
E041: target16 −.0007987550 (8320 cells); other60 +.0009093584 (31200 cells);
target16 Not answered −.0044084735 (831 cells); substantive −.0003982108 (7489).
Whole-WB log score changes from −1.1005776279 to −1.1000278723 (+.0005497556).
The small aggregate rise comes from the other60 aggregate, not positive target16
performance. These fixed diagnostics do not trigger head removal, threshold
changes, extra seeds, smoothing or another run. No causal decomposition follows.

## Mechanism and technical evidence

One frozen candidate: five conditional continuation logits plus separate
Not answered logit, stable seven-category log probabilities, original pooled
categorical NLL. Original nominal network constructed first, target rows0..4/6
copied without new RNG draws. Exact untouched initial parameters/RNG confirmed
for both configs. Original model files and E041/E025 snapshots remain unchanged.
See [implementation and reproduction](implementation-contract.md) and source.diff.

Ten candidate-contract tests and three added harness tests pass. They cover both
dtypes' formula/NLL/gradient, extreme logits, missing categories/empty risk sets,
Not answered gradient, pooled denominator, full query mask, exact target schema,
both configs' initialization, small-fit fallback, and w=0 final-refit orchestration.
The fallback/refit tests use fake endpoints and do not prove statistical behavior.
An initial expected six-versus-seven-column RED is retained, not hidden or omitted
from cost. No old successful scientific/test suite was repeated.

Actual model entry uses DEV GIVEN only, EXCLUDE removed and all query PREDICT
missing. Thirty-six neural target-role checks match frozen hashes. WB split:
inner-train3280/inner-stop832/outer-selection1083/final-refit5195. Unchanged
seed/config/optimizer/early-stop/w/ladder/gate/donor/lambda policies. WB final
selection: both procedures width128/depth2/dropout.1 and w1; E041 epoch193,
candidate epoch184. Choices in call-summary.json remain
UNICEF width64/dropout0/w1/epoch115 and
UNHCR width128/dropout.1/w.9/epoch110. No middle refit or conditional rescue.
All nine final refits occurred. Lambda fit-label reuse is not independent audit.

## Complete local costs

| Fresh worker | Startup/import/all3/validation/save/exit wall | Neural fits | Metric optimizers | Peak owned RSS bytes | Peak owned private bytes |
|---|---:|---:|---:|---:|---:|
| E025 | 324.9765975s | 9 | 0 | 1353572352 | 1473900544 |
| E041 | 342.9659210s | 9 | 8 | 1397698560 | 1532755968 |
| E062 | 357.5224430s | 9 | 8 | 1404985344 | 1559068672 |

Candidate complete local wall357.522443<900s. All computational children,
including failed RED50.0355171s, passed tests11.5743991s, preparation14.5843591s,
three model workers1025.4649615s and evaluator21.5373587s:
**1123.1965955/1800s**, eight children. Pipeline9/9, neural27/27, metric16;
all16 metric optimizer results report success. No attempt allowance remains for
another model/instrument run. No additional fits are proposed in this S1.

Numerical threads2, GPU0, one heavy worker, existing Windows/Ryzen5800X environment.
Peak conservative owned-tree RSS1.3085GiB/private1.4520GiB, each below8GiB.
.1s observation; no forced termination or scientific failure. See
[resource-summary.json](resource-summary.json), [cost semantics](cost-contract.md),
environment records, per-attempt receipts and actual call traces. Inclusive
stage spans are not double-counted. WB predict alone is102.1126451s versus
E04188.5649233s; neither number substitutes for complete all3 cost.
Gross entry12:39:40Z, unchanged deadline14:39:40Z, computation cutoff14:29:40Z;
final recording completion and exact gross wall are in closeout-receipt.json.

## Interpretation, preservation and next decision

The application procedure and complete local engineering path are demonstrated.
There is no fresh WB oracle. Already-exposed synthetic results do not establish
real WB improvement or an upper bound, and no iid-cell significance is claimed.
Nonresponse separation, asymmetric initialization, shared-trunk changes and
selection/refit jointly change this procedure; the results do not isolate order.
The observed target16 decline materially limits the motivating efficacy claim.

Return to S0 with the source-qualified record. S0 decides whether bounded S2
release validation is worth authorizing; there is no automatic handoff to S2 or
incumbent adoption. Remaining: source/assembly parity; ZIP checker; official all3
shared900s/memory on the actual release environment; fresh clean E025/E041 release
comparisons with per-instrument absolute.002; complete SCORES interpretation table
(Grand/each instrument, noisy/rounded published values distinguished). Hosted
WB effect and final adoption remain separate. No expected Grand is manufactured.

HEADa43f4379 unchanged; allowed original source/document/schema/tree identities
match, protected files deliberately not rehashed. Existing dirty work preserved;
shared status/log get additive result entries only. All STOP/HOLD/exposure roles
and E041 incumbent/E025 fallback/parked E057/E060/E061 states remain. E058 STOP,
E059 STOP_SELECTION/A039/A040 unchanged, A_half not promoted, A018 unconfirmed,
S3 stopped. No ZIP, snapshot/tree modification, remote/install/GPU, commit/push,
subagent or S2/S3. [Exposure ledger](exposure-ledger.md),
[verification](verification.json), [error history](error-repair-history.md).
