# E057 S2 release verification complete

Recorded2026-09-25. Input949884b; plan/code/scorecard/archive frozen at3f0f6ad
before expensive runs. S2 only: no upload, S3 resumption, TEST selection, method
rewrite, parameter search, new seed or new proxy study. Production source and
all previous ZIPs unchanged.

## Decision

E057 passes local technical qualification and release no-regression policy.
A single user-controlled DEV exploration is interpretable under the scorecard,
conditional on unchanged comparison/contract and an available authorized-account
slot. E057 remains parked/unsubmitted; E041 incumbent, E025 fallback.
No target improvement has been measured.

E056 supplied scoped evidence of complementary conditional content. E057 now
has verified visible-TRAIN selection/validation/refit mechanics, default and
standalone paths, active/inactive branches and full cost. Synthetic fallback
does not establish or refute hidden benefit. Internal detailed statistics are
not exposed by normal hosted predict. No expected Grand or activation forecast.

## Measured checks

| Requirement | Result |
| --- | --- |
| Provenance | Preflight97 hashes match; fixed source/data/frame/cells/config/splits and six E025/E041 caches; S1 package versions unchanged |
| Actual source default | No injected baseline; all3 outputs and UNHCR shadow/refit/selection/validation exact to S1 |
| Assembly parity | Immutable E041 prefix, isolated E057 names; all189649 raw source/assembly/official vectors exact |
| Active path | Full-policy toy fixtures plus unscored actual-library alpha=.5;124 heads/77004 changed vectors,21 sparse fallback; no alternate policy scoring |
| Invariants | Controls/parents/nonleaves exact; alpha0/sparse/zero mass/schema order checked; raw sentinel exact, max mass4.44e-16/postfloor sentinel2.22e-16 |
| ZIP and official | Fresh ZIP checker PASS; official phase1 all3 PASS |
| Official skill | UNICEF .5006484230707156 / WB .45471730736298255 / UNHCR .5624627288576414 |
| Release comparison | E025 deltas0/0/-.0004861448473750807, all absolute<=.002; E041 deltas all0 |
| Shared assembly | 540.508477s inclusive; peak tree RSS1,820,712,960 / commitment1,715,068,928 bytes |
| Official suite | 546.082929s summed scorer time;556.545433s inclusive; peak RSS2,483,646,464 / commitment2,282,479,616 bytes |
| Total budget | Default527.669855 + assembly540.508477 + official556.545433 =1624.723765s<2700; each suite<900s and memory<8GiB |
| Tests/review | Eight new release tests PASS;13 unchanged-source S1 tests retained. Independent static review: no blocking model/parity issue |

Memory sums live owned processes' OS lifetime peak counters, including harness
and launchers; a conservative aggregate, not an H100 measurement. Inclusive
timing covers startup/import/captures/checks/writes. Official CLI uses separate
processes; the assembly suite supplies the shared-process all3 observation.

## Identity and records

- [ZIP](../../../../submissions/2026-09-25-E057.zip), SHA256
  21bce8672ce3b3b659c9e8dfae551737c994ff64d4f57d54411c59ba77d0cba4.
- [main.py](../../../../submissions/2026-09-25-E057/main.py), SHA256
  42b1df23f4900c744e05bf7d54f12e20c20d61f9ec44584faca872df6ed17213.
- [Scorecard](../../../../submissions/2026-09-25-E057/SCORES.md),
  [verification](../../../../submissions/2026-09-25-E057/verification.json),
  [preflight](preflight.json), [default](default.json), [assembly](assembly.json),
  [official](official.json), runtime JSONs and per-instrument official logs.
- Row arrays stay ignored in external/e057-s2/; only hashes/aggregates committed.

## Scope and limitations

Scored roles: existing exposed synthetic phase1 DEV and the fixed procedure's
internal visible-TRAIN selection/validation. No new untouched audit, synthetic
TEST, E056/SIPP/Adult arrays or private competition response access. Natural
shares remain zero after the fixed2SE guard; no hidden activation/effect-zero
inference. Forced fixtures establish mechanics only.

Static review found overlapping missing-update scorecard wording. Before any
hosted result, clarified that missing update status is unresolved at Grand=.64;
nonconflicting comparable >.64/<.64 stays favorable/adverse. Contradictions,
incomparability or missing Grand take precedence. Original bytes preserved in
[scorecard-prerun.md](scorecard-prerun.md); [clarification](scorecard-clarification.md).
Missing instrument scores limit attribution and never reveal hidden activation.

[Environment notes](environment-notes.md) and [public API record](official-rules.json)
retain current DEV900s/one-per-day and unchanged kit ee427a9. Account slot unknown.
API top-level Python3.12 image versus kit-described submitted-code Python3.13
is an unresolved metadata distinction. Local CPU/library validation cannot
identify or guarantee actual hosted environment performance.

[Review](review.md) notes a future harness monitor-constructor cleanup gap.
Current supervisors initialized and completed successfully; constructor smoke
tests preceded assembly and official launch. No live verifier edits or retries.
Future harness reuse needs the stated cleanup hardening. Initial red test failed
on absent assembly module as intended; final eight tests PASS. Notice source
was corrected to actual starter-kit LICENSE before packaging/preflight; no failed
package or expensive run resulted. No environment installation or upgrade.

## Reproduction and next action

```powershell
.venv/Scripts/python.exe scripts/assemble_e057.py
.venv/Scripts/python.exe scripts/release_e057.py preflight
.venv/Scripts/python.exe scripts/release_e057.py run --suite default
.venv/Scripts/python.exe scripts/release_e057.py run --suite assembly
.venv/Scripts/python.exe scripts/release_e057.py run --suite official
.venv/Scripts/python.exe scripts/release_e057.py finalize
```

Historical commands: scripts refuse occupied outputs and enforce frozen hashes;
do not repeat successful fits. Final scorecard appends results/clarification;
execution-time hash refers to scorecard-prerun.md. closeout.json binds final
documents separately. No further fit justified for these unchanged artifacts.

For a user-chosen DEV upload, use this exact ZIP after checking account slot
and current contract. Record actual timestamp/ID/hash if available and bring
the result to this S2 chat. No upload or intended date set here. Apply the
scorecard and keep DEV-incumbent/TEST judgments separate. S3 remains stopped.
All owned workers finished; task-only commit/push with remote verification at
closeout. Unrelated user changes preserved.
