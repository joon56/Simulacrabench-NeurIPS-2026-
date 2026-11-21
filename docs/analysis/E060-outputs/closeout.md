# E060 — Content-target retrieval release closeout

Date: 2026-09-27. Owner: root. HEAD:
`1d223340d4e1fa3993b411dc5daafab9cb37d0cd`; branch work/e050-submission.
Disposition: QUALIFIED_EXPLORATORY_DEV_NOT_UPLOADED. Technical/release gates PASS;
natural-response efficacy unknown, no adoption. See verification.json.

## Decision and scope

The user requested work toward a new submission. A025 compared three approaches
and registered one distinct, bounded UNHCR metric-fitting experiment. It does
not reopen the A023/A024 empirical study, E059 selection or E057 tree search.
Sentinel target cells are excluded from metric fitting loss; full donor answer
distributions and the original all-cell selector remain. There is no ordinary-
answer conditional renormalization or hard-gate inference. The exact model and
release thresholds were frozen before full-data execution; no parameter search.

Only already-exposed synthetic phase1 data was fitted/scored. No valid independent
natural-response channel is claimed. This is a technically qualified exploratory
configuration if all gates pass, not an adopted improvement or TEST selection.
E041 remains DEV incumbent; E025 fallback. Expected hosted improvement is unknown.

## Measured local evidence

| Instrument | Candidate skill | E041 delta | E025 delta | Changed vectors vs E041 |
| --- | ---: | ---: | ---: | ---: |
| UNICEF | .5006484230707156 | 0 | 0 | 0 / 17856 |
| World Bank | .45471730736298255 | 0 | 0 | 0 / 39520 |
| UNHCR | .5624429548505255 | -.0000197740071158 | -.0005059188544909 | 42820 / 132273 |

Maximum UNHCR probability-vector entry change .09450195934036731. No actual active
section count was retained, so do not infer one. E025 absolute .002 all3 and E041
UNHCR loss .002 gates pass. The small negative synthetic delta is not an observed
target-population effect or a paired uncertainty estimate. UNICEF/WB controls
are exactly equal to both baselines. Source and assembly match all189649 vectors.

Seven objective/isolation tests and four assembly tests PASS. Generated arrays
cover gradients, original-objective fallbacks, role isolation and active/inactive
assembly behavior. They do not prove actual target efficacy or every leakage
boundary of the inherited pipeline. Original in-sample base replay and proxy-
versus-deployed selector limitations remain. Public approximate UNHCR gates make
hard sentinel inference inappropriate; no target-response domain finding exists.

## Execution cost and technical history

CPU2, one heavy suite at a time, no GPU. Source342.4691633s; shared-process all3
assembly319.3193997s. The earlier failed source attempt46.5746736s is preserved
and included in the registered2700s cap. It stopped before scoring at a harness
tuple-unpacking defect; one documented retry corrected only that validator and
output namespace. Model, seed, heads, thresholds and budget remained unchanged.
No successful suite or successful fixture was repeated.

Source and assembly each measured9 neural requests/9 attempts and8 metric
optimizer calls. Tiny fixtures made4 metric optimizer calls. Failed UNICEF
attempt implies3 neural calls from source structure, without persisted counters.
Official subprocess internals are not instrumented; do not report inferred
counts as measurements. Each monitored suite includes scoring/logging overhead
and must finish below900s; process-tree RSS and commitment must remain below8GiB.
Exact stage times, aggregate budget and sampled peaks are in verification.json.
Local measurements cannot guarantee hidden-data/H100 behavior.

Official extracted-ZIP all3 suite PASS in338.0928504s, raw predictions exactly
equal assembly/source. Total suites including failed attempt1046.456087s.
Largest sampled RSS1922732032 bytes (1.791GiB), commitment2048143360 bytes
(1.907GiB), both from official suite. ZIP checker PASS. All gates are complete;
no active Python/WSL/bash process observed at close. No further run is needed.

## Frozen deliverable and next action

- ZIP: `submissions/2026-09-27-E060.zip`, 14995 bytes.
- SHA256: `f5d77ba35fe6ffd7da098e36a86cb8e041692a50c79104ee9a26bea580e8064d`.
- main.py: `eb9fd1869c6c2cd7b856d163d5646981d3888197bbd3f27b384e099335ab7bc3`.
- ZIP root contains only main.py and NOTICE.txt; no fitted external artifact.
- [Scorecard](../../../submissions/2026-09-27-E060/SCORES.md) holds prospective
  favorable/adverse/unresolved/technical-failure arms. Upload remains user-owned;
  account slot/actual upload time/hosted score unknown. No automatic upload.
- [Next result session](s2-handoff.ko.md) verifies the artifact and records only
  supplied results. No need to restart research or repeat release checks now.

## Preservation and limitations

No observed source/key Parquet read/rehash, protected audit/calibration response,
observed fitted cache, new sample/role, E056 rerun, kit update or install. Inherited
17999/12339 observed-use union and A022 role inventory stay unchanged. See
[exposure ledger](exposure-ledger.md) for exact consumed/protected roles.

E058 STOP/E059 STOP_SELECTION and all historical STOPs, E057 parked, A023/A024
HOLD, A_half nonpromotion and A018 TEST user-unconfirmed remain. S3 stays stopped.
Prior permitted source/text/aggregate hashes103 matched again at final verification.
Existing user changes preserved, no commit/push or old snapshot edit.

Automatic approval review rejected docs/tree.md regeneration due to its explicit
prior protection. Command did not launch; tree/preview were not written. The
existing dirty tree remains unchanged. E060 is recorded through status/log and
its experiment file. No bypass or further tree attempt is authorized here.
