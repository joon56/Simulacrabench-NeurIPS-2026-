# E064 S1 closeout — LOCAL_TECHNICAL_PASS_FOR_S0

2026-10-11 KST. **Technical contract passes; candidate remains parked for S0.**
UNHCR synthetic skill **declines by0.000084353601793**, within the preregistered
per-instrument-.002 bound. This is not improvement evidence, actual UNHCR efficacy,
independent audit, E025 release qualification or S2/DEV/TEST adoption.

Implemented [conditional_gradient.py](../../../src/models/conditional_gradient.py)
through the original UNHCR tune hook. Original independent heads, constructor,
forward values/RNG/CE/denominator remain. Only conditional input is detached;
conditional parameters keep learning. Exact original local training/tune arithmetic
is checked by AST; renderer/metric are original functions. Controls delegate R.
No original model, experiment, snapshot or tree changed.

## Observed fixed comparison

| Instrument | R skill | H skill | H-R | Changed raw vectors |
| --- | ---: | ---: | ---: | ---: |
| UNICEF | .5006484230707156 | .5006484230707156 | 0 | 0/17856 |
| World Bank | .45471730736298255 | .45471730736298255 | 0 | 0/39520 |
| UNHCR | .5624627288576414 | .5623783752558484 | -.00008435360179303028 | 132225/132273 |

UNHCR log-score H-R=-.00010643334286619677; maximum raw coordinate difference
.05873684199021589. Both arms return all189649 ordered vectors; all213 UNHCR heads
checked. Maximum sum error across both arms/all instruments2.8615613700821996e-7.
Official in-process normalization/floor.001/skill applied once to each raw output,
after six raw hashes/source freeze and only then evaluator DEV truth projection.
[Exact comparison](attempts/score-01/comparison.json), [raw freeze](attempts/score-01/frozen-predictions.json).

10 unique focused checks pass: initial state/order/RNG and both-config forward/CE,
float64 branch gradients1e-10, head/Adam updates, None versus zero, G0/local factory,
original train/tune flow and controls, tiny all213 fallback/empty query, split/config2/
fresh refit, whole-PREDICT masking/GIVEN-only features, output-freeze/budget gate,
actual observer and F-only/minimum30 boundaries. Test methods group some checks;
there are10 unique methods, not one test per phrase. Failed absent-module RED retained.

Expected invariant hashes agree: UNICEF5/WB8/UNHCR16 keys, including actual metric
weights/activity, donor identities/order, replay eligibility/concentration, evidence,
ladder/agreement. No missing executed counterpart. Both UNHCR metric active sets
are[0,1,3,4,5,6,7]. Twelve item lambda pairs differ. Both choose128x2/dropout.1,w.9;
R final refit110epochs versus H121. H's three real UNHCR fits use the new class;
12 target-role checks per arm match frozen original inner/outer/final roles.
These are full-policy differences, not pure direct-gradient final effects.

## Whole execution and limitations

| Stage | Measured controller-stage wall seconds |
| --- | ---: |
| Initial denied launcher + new checks (including RED) | 85.3014061 |
| Projection/environment preparation | 15.5874986 |
| Fresh R all3 | 379.9942503 |
| Fresh H all3 | 376.8413191 |
| Separate evaluator | 19.6531967 |
| Total | **877.3776708 /1800** |

Scientific processes2/restarts0; pipelines6/neural18/metric16, refit included.
Each all3 startup/import/all instruments/output fits900s. Numerical CPU2/GPU0,
heavy1; maximum observed monitor gap.131023s. Conservative owned-tree high-water
RSS/private1.301285/1.415653GiB, below8GiB each. Neural fit function wall544.1614663s;
metric minimize wall.6247666s. These nested timings are not added again to total.
Small fixture calls and budgets are separate in [cost ledger](cost-time-ledger.json).
No partial-head extrapolation or old cache timing substitution.

Initial sandbox launcher access failure occurred before Python/controller/model
entry. Same existing Python file was confirmed and reused with process permission;
no installation/environment replacement. Its0.1777746s is counted, memory unmeasured.
All qualified numerical workers had external monitoring before imports. Memory
numbers sum per-process high-water counters; not a simultaneous allocator peak.
[Failures/repairs](regression-history.md), [reproduction and consumed attempts](reproduction.md).

Exposure remains the already exposed synthetic engineering channel. No valid new
efficacy oracle/current E041 loss map; original S/L reuse/in-sample proxy replay
remains. Small synthetic loss neither proves actual harm nor falsifies the full
UNHCR hypothesis. No response subgroup/head search, new seed, changed tolerance,
lambda/metric policy or successful-arm rerun after results.

Source/input/runtime/role identities are [entry](entry.json), [freeze](freeze-01.json)
and per-attempt source copies. E041 source executed; submission snapshot/assembly
parity was not executed. Existing protected records/source bytes retained; shared
status/log receive result-only additions. Final preservation/jobs/receipts are in
[verification](verification.json). No commit/push/remote/ZIP/S2/S3 work.

## S0 decision remaining

S0 reviews whether this technically valid fixed policy warrants a separate S2
release task despite a small negative synthetic result. No automatic S2 handoff.
Remaining: clean E025 per-instrument-.002 and E041 release comparison; source/
assembly/extracted parity; ZIP checker; official all3/shared900s-memory;
bytes provenance and preregistered SCORES favorable/adverse/unresolved/technical/
HOLD reading. Each needs its separate scope. Actual hosted result remains unmeasured.

E041 incumbent/E025 fallback; E057/E060/E061/E062/E063 parked; E064 parked.
E062/E063 UNRESOLVED; E058 STOP/E059 STOP_SELECTION/A023/A024 empirical HOLD/
A039/A040/all STOP/HOLD.17999/12339SSUID and A022 roles/aggregate disclosures;
E059 consumed1918/1124 and2007/1130; protected2074/1177 andcalibration1866 preserved.
A_half not promoted/A018 user-unconfirmed/S3 stopped/no new S2 candidate.
