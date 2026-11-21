# E063 closeout — 2026-10-09

**LOCAL_TECHNICAL_PASS_FOR_S0. E063 remains parked pending S0 review.**
One fixed UNHCR round-conditioned metric was implemented and passed the registered
synthetic technical gates. This is not actual UNHCR efficacy, DEV adoption,
E025 release regression, S2 qualification or TEST selection.

## Observed result

| Instrument | R skill | H skill | H−R | Changed raw vectors |
|---|---:|---:|---:|---:|
| UNICEF | 0.5006484230707156 | 0.5006484230707156 | 0 | 0/17856 |
| World Bank | 0.45471730736298255 | 0.45471730736298255 | 0 | 0/39520 |
| UNHCR | 0.5624627288576414 | 0.5624803077254883 | +0.0000175788678469 | 46405/132273 |

UNHCR log score R−0.5520636156180775, H−0.552041435442851,
delta+0.0000221801752265. Maximum raw difference0.13446233163832838.
Both control arrays and their serialized NPZ hashes are identical. Each arm
produced189649 canonical vectors; official shape/finite/nonnegative/positive-sum
checks passed, largest raw sum error2.8615613700821996e−7 (<1e−6).

H eligible: F wave1/2=465/735, S=323/477, bank5479, replay800, K32.
Natural H active7/8, identical active set to R: sections2,3,7b,7c,4,5,6.
Section7a inactive. Thirty-seven item lambda pairs changed. Round weights differ
in every fitted section; full fixed descriptive values are in
[metric-observations.json](metric-observations.json). No head/round is promoted.

All three H−R skills meet the frozen−.002 lower bound. Eight of sixteen fixed
section×wave descriptive log differences are negative; the range is
−0.0008824432392193 (section4/wave2) to+0.0005585372228050 (7c/wave2).
These declines remain in the [complete comparison](attempts/score-01/comparison.json);
no threshold, tolerance, seed, support rule or policy changed after observation.
The very small synthetic whole-score increase is engineering evidence only.

## Technical work and failure history

New model, focused tests and bounded controller implement the one registered
35-coordinate H. Original E041 source/model/snapshot stays unchanged; original
predict directly supplies controls/whole-instrument fallback without duplicate fit.
Algebra, F-only optimizer isolation, raw wave dispatch, K32/legacyK10, masking,
actual entry, replay/lambda30/zero, global all213 recursion and fallback raw parity
passed. These are ten unique new cases, with fixed neural/base doubles where
specified; forced activation is separate from the natural all3 outcome.

Expected missing-module RED is preserved in tests-01. Tests-02 had9 PASS and
one test-observer argument-index failure. Test-only repair corrected query/codes/
bank/initial positions; the affected forced-active case passed in tests-03.
Unchanged successes were not repeated. Model/runner/policy/assertions/tolerances
were unchanged after tests-02. No scientific failed arm or scientific restart.

After unit qualification, prepare froze permitted source/code/runtime/package/
synthetic/masked-frame/role hashes. Fresh R then fresh H ran sequentially under
one freeze. All six new raw outputs were frozen before evaluator-only DEV truth.
Actual trace checked24 neural-target role boundaries and every F/S/bank identity/
metric F-slice. Original base S/L reuse and in-sample replay remain disclosed;
there is no independent audit or A021 D-P/D-R claim.

Implementation and historical commands:
[implementation-contract.md](implementation-contract.md).
Immutable policy: [registration.md](registration.md);
[freeze-01.json](freeze-01.json); [unit-qualification.json](unit-qualification.json).
No prior raw output/model cache or protected responses were read.

## Measured full cost

| Stage | Wall seconds | Peak owned RSS GiB | Peak owned private GiB |
|---|---:|---:|---:|
| Three new test processes, failures included | 59.369999 total | 0.3797 max | 0.3936 max |
| Input/environment prepare | 14.815140 | 0.6162 | 0.6701 |
| Fresh R all3 | 331.947906 | 1.2846 | 1.3954 |
| Fresh H all3 | 327.633190 | 1.3000 | 1.4232 |
| One evaluator process | 20.785463 | 0.6488 | 0.6975 |

Total computational stage wall754.551699s/1800; all3 combined659.581097s.
Scientific processes2; pipelines6; neural training18; metric optimizers16.
Neural473.350976s and optimizer0.683826s are nested components, not extra cost.
No scientific restart; numerical CPU2/GPU0/heavy1, each all3<900s, both memory
caps<8GiB. Monitor started before numerical import. Every resource_stop COMPLETE.
Focused child max40.080262s<60; focused total<300. No remaining named local jobs
at post-run observation. Full exact records: [cost-time-ledger.json](cost-time-ledger.json).

Stage timing includes startup/import, full three instruments, input/output work,
trace, external monitor and cleanup; single runs are no future runtime guarantee.
Monitor uses .1s polling and conservative sums of process peaks; maximum scheduler
gap was not separately logged. Whole-machine/GPU/H100 memory is not measured.
Three empty tracked package markers were separately inventoried after R began;
they match clean HEAD empty bytes and contain no initialization. This supplement
does not pretend they were separately hashed in the original60-file freeze:
[package-marker-identity.json](package-marker-identity.json).

## Preservation and scope decision

Current workflow2026-10-05-r5, SHA256
a577942675e16a732339e586c14796104dda704693568439ae28670cc7fb7b23;
ordered actual-read receipt in entry.json. HEADa43f4379 unchanged; existingdirty104
retained. Before shared updates all60 permitted source/document hashes and all
three frozen new code hashes matched. Shared status/log receive additive result
entries only, with original-byte recovery verified in verification.json.
Only authorized E063 paths and status/log were written; no tree/model/snapshot/
old research changes, commit/push, remote, install, web, subagent, ZIP or upload.

Return S0 for review. E063 parked, no new S2 candidate. Remaining separately
authorized S2 work, if S0/user later decide to proceed: clean E025 absolute−.002
per-instrument and E041 release comparison; source/assembly parity; ZIP checker;
official all3 shared900s/memory; SCORES pre-result interpretation and bytes
provenance. Same inputs/policy do not mean those checks were completed here.

E041 incumbent/E025 fallback; E057/E060/E061/E062 parked. E062 public tie
UNRESOLVED. All STOP/HOLDs including E058/E059/A023/A024/A039/A040 retained.
Exposure17999/12339SSUID, aggregates/A022 roles, E059 consumed oracle1918/1124
and selection2007/1130, protected audit2074/1177 and calibration1866 unchanged.
A_half not promoted; A018 user-unconfirmed; S3 stopped. No automatic follow-on.

