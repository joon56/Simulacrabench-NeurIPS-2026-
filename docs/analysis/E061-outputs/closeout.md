# E061 S1 closeout

**EXPLORATORY_SOURCE_QUALIFIED.** Technical, prospective synthetic regression
and local resource gates pass. S2 source candidate only; no release/package
qualification, actual ERPIS benefit or TEST adoption established. E041 stays
incumbent. The synthetic result is slightly worse, not an improvement claim.

## Actual execution and result

One frozen candidate, one scientific worker, one phase1 call per instrument
for candidate/E041/E025. No scientific retry, threshold/head/seed adjustment,
existing cache read or protected response access. All nine vector sets frozen
before any official DEV score. Focused tests9/9 pass; prior expected missing-
module RED and first8-test suite retained. One additional negative access test
and warning cleanup preceded the final source freeze, not a post-score change.

| Instrument | E061 skill | E041 skill | E025 skill | E061 minus E041 | E061 minus E025 |
|---|---:|---:|---:|---:|---:|
| UNICEF | .500648423071 | .500648423071 | .500648423071 | 0 | 0 |
| World Bank | .454717307363 | .454717307363 | .454717307363 | 0 | 0 |
| UNHCR | .562391878130 | .562462728858 | .562948873705 | -.000070850727 | -.000556995575 |

Every delta satisfies the prospective lower bound-.002. No+.005 requirement
was added; no gate was weakened after results. Metrics use official
check/floored/score functions and original config; no official release CLI.
[Comparison](comparison.json) preserves full precision and all vector checks.

- UNICEF/WB raw vectors exactly equal frozen E041: max difference0.
- UNHCR132225/132273 final vectors differ>1e-10; maximum entry difference
  .16454842686653137. No forced activation. All213 predicted heads included.
- All568947 vectors across9 calls satisfy official shape/finite/nonnegative/
  positive-total checks. Largest raw sum error2.8615613700821996e-7, below1e-6.
- Conditional/full neural identity, schema option mapping, extreme sentinel
  logits, shared gradient and unchanged CE mask/denominator tests pass.
  Final ladder/gate/evidence output is not asserted to satisfy neural identity.
- Actual _targets entry checks36; no held-out row reached training targets.
  A deliberate small-fixture forbidden access was rejected. This does not claim
  that all pre-existing upstream statistical limitations have been repaired.
- Candidate/E041 each selected7 of8 retrieval sections, same indices
  [0,1,3,4,5,6,7]; nonzero lambda items91 versus82. This is the unchanged policy
  recalculating against different bases, not a frozen-lambda controlled effect.

## Whole-run resources and calls

| Stack | UNICEF predict s | WB predict s | UNHCR predict s | Sum predict s | Neural calls | Metric optimizer calls |
|---|---:|---:|---:|---:|---:|---:|
| E061 | 36.943 | 101.529 | 190.915 | 329.388 | 9 | 8 |
| E041 | 33.761 | 102.195 | 225.119 | 361.075 | 9 | 8 |
| E025 | 32.577 | 100.825 | 240.133 | 373.535 | 9 | 0 |

Candidate complete stage **340.093s**, measured by parent including interpreter
startup, numerical/source imports, all3 input preparation, calls and artifact
writes; below900s. Worker internal stage339.914s; import/preflight4.431s.
Stage also imports reference modules, making that cost conservative for candidate
alone. Per-function times include tracing overhead and are not separate runs.

Scientific worker parent wall1083.500s. All computational workers including
expected RED and both focused-test suites1098.523s, below1800s.9 full-stack calls,
27 actual neural calls,16 metric optimizer calls; no fallback/retry calls.
Neural epochs1379/1393/1393, sum4165; full-fit/validation/refit rows and selected
epochs/configs in [call summary](call-summary.json), complete [events](calls-01.jsonl).
Metrics used original50-iteration cap; realized iterations16,14,25,17,15,13,14,11
for both candidate/E041. Tests performed six autograd.grad evaluations in total,
six injected fake train calls, zero optimizer steps, excluded from actual fits.

Owned controller+worker tree conservative peak **RSS1.990929GiB /
private-commitment1.513561GiB**, each below8GiB. Windows counters sampled.1s;
sum of each process's peak counters, not instantaneous whole-system RAM.
Numerical pools and torch intra/inter-op threads<=2; CPU only, no GPU.
No monitor failure/cap. Worker exited0, no research worker observed after close.
[Resources](run-01-resources.json), [environment](environment-01.json).
Local CPU cost is not a hosted H100/runtime guarantee.

## Interpretation and limits

Parameter tying is implemented and exercised at full schema scale. It changes
UNHCR outputs while preserving controls and meeting registered engineering gates.
On this reused exact-gate synthetic DEV it slightly reduces skill. Neither this
loss nor passing the tolerance establishes benefit/harm on actual approximate-
gate ERPIS. No independent audit, target oracle or valid target confidence
interval was created. Original E041 selector-proxy/in-sample replay limitations
remain. No hidden instrument score, activation or Grand gain is forecast.

Removing separate conditional Linear modules also changes RNG consumption
before dropout; fixed torch seed0 is retained. This consequence was registered
before the run. The complete procedure, including chosen epoch and recomputed
lambda, is compared; no isolated-gradient or frozen-lambda effect claim.

## Artifacts, reproduction and next action

### HEAD and score-record reconciliation at closeout

Entry HEAD was `1d223340d4e1fa3993b411dc5daafab9cb37d0cd`; closeout HEAD is
`a43f4379ec78dbc2de260463eef67bb1d567d7e1`. S0's commit at
2026-09-27T12:37:15Z changed only36 submission score documents. It preceded the
scientific worker start12:39:50Z, but this S1 detected the HEAD change only at
final identity verification. The initial HEAD-equality check failed; outputs
were preserved and closeout writes paused. The user then explained S0's
authorized score-only commit/push and directed document-only completion.
Local commit metadata is observed; S0 push is user-reported, not remotely
reverified here. Original entry/registration/frozen results remain unchanged.
Permitted source identity and changed-path checks are recorded in manifest;
no model, test, prediction or score was rerun after this new information.

The user-supplied API record, reconciled by S0 in
[SCORES](../../../submissions/SCORES.md),
[reported values](../../../submissions/hosted-scores/2026-09-27.json) and
[verification](../../../submissions/hosted-scores/2026-09-27-verification.json),
identifies E060947705 as Finished: Grand0.6433333333, UNICEF0.52, WB0.49,
UNHCR0.92. All released values equal E041; no best update. Instrument-score/ID
uncertainty is resolved, uploaded-byte identity is still unverified. These are
released values, not unnoised/pre-rounding scores. E060 stays parked/effect
unresolved; E041 incumbent. No E061 candidate, seed, threshold, criterion or
scientific verdict changed. This evidence adds no respondent-data exposure.

- Model: `src/models/tied_content_heads.py`, SHA256
  `f9449d41d30041f6e9714c7a25777965ec4d25cfa2563b018fb08c94dde20833`.
- [Registration](registration.md), [entry](entry.json), [source review](review.md),
  [AST check](source-review.json), [frozen inputs](frozen-inputs.json),
  [phase1/split identities](phase1-inputs-01.json),
  [frozen vectors](frozen-predictions-01.json), [exposure](exposure-ledger.md),
  [final manifest](manifest.json). Executed code copies saved as `.py.txt`.
- Exact executed commands from repository root:
  `.venv/Scripts/python.exe -X utf8 -B scripts/check_e061_tied_heads.py tests --attempt 2`
  then `freeze --attempt 2`, then `run --attempt 1` on the same script.
  RED/first test commands and outputs are retained. Existing output files are
  intentionally exclusive-create; do not rerun this successful experiment or
  overwrite artifacts. A separately authorized reproduction needs a new output
  scope and the same frozen inputs, not a scientific retune.

Next: [S0 result review](s0-handoff.ko.md), following the user's routing correction.
S0 must decide whether to hand off to S2. The existing [S2 draft](s2-handoff.ko.md)
is reference material pending that decision, not an active task. Scientific
verdict and frozen outputs are unchanged. If routed, remaining: source/assembly parity,
ZIP checker, official all3, complete package runtime/resources and SCORES reading
table/provenance. No S2 operation is executed here. No ZIP/method/TEST artifact,
upload, commit or push. `docs/tree.md` intentionally unchanged; E061 link deferred
under user scope. Session deadline/HEAD/preservation verified in manifest.

E041 incumbent/E025 fallback; E057/E060 parked; E058 STOP/E059 STOP_SELECTION,
every earlier STOP/HOLD and A_half nonpromotion preserved. A018 TEST remains
user-unconfirmed, S3 stopped. Protected exposure/roles unchanged. VAF approval
pending; no VAF acquisition. Successful main arm needs no backup study.
