# E041 phase-2 local preparation

Frozen E025 and E041 compared on the official clean synthetic sandbox with
`sample_rows(..., 2)`: all TRAIN+DEV respondents visible; whole TEST PREDICT
blocks scored. This is an engineering comparison, not a prediction of hidden
competition TEST results. No hosted upload or final-model promotion occurred.

| Instrument | Cells | E025 fresh skill | E041 source / official skill | E041-E025 | E025/E041 raw max abs | E041 official seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| UNICEF | 41,676 | 0.490197770701 | 0.490197770701 | 0 | 0 | 43.336 |
| World Bank | 92,112 | 0.462029504790 | 0.462029504790 | 0 | 0 | 102.183 |
| UNHCR | 308,637 | 0.565173813942 | 0.564665364947 | -0.000508448996 | 0.536418026159 | 221.658 |
| Mean | | 0.505800363144 | 0.505630880146 | -0.000169482999 | | 367.177 total |

E041 original assembled snapshot passed the official grader on all three with
`--phase 2`. Every raw official vector exactly equaled its E041 source vector;
source and official exact skills/log scores matched. Original E041 ZIP passed
the official checker and contains exactly the unchanged snapshot `main.py`.
The sum of official local inclusive scoring times, 367.177 seconds, is below
the shared 3,600-second phase-2 limit. The three runs each create a separate
local process, so this is a conservative rehearsal total, not a hosted runtime
or a measured 16 GB memory bound.

The registered absolute local difference gate is `abs(E041-E025) <= 0.002`
per instrument; all three pass. UNHCR's small adverse synthetic direction
does not predict real TEST rank. E025 remains the phase-2 fallback; E041
remains the DEV incumbent. This comparison alone does not select a final model.

Fresh E025 scores differ slightly from its September rehearsal: UNICEF
-0.000007983303, World Bank +0.000012753036, UNHCR unchanged. Current paired
frames, schema/data hashes and scorer are identical within each instrument;
fresh E025 values are the comparison reference.

`verification.json` holds per-instrument scores, cell counts, frame/schema/data
hashes, timing, and original E041 main/ZIP hashes. `supplemental-verification.json`
holds the corrected absolute gate, all artifact hashes, full E041 source
dependency-tree hash, package versions, and vector comparison. Source and
official raw predictions and logs are under `docs/analysis/A012-outputs/`.
The executed verifier copy there was saved before a post-run preflight/threshold
correction to the reusable script. Supplemental provenance was collected after
the fits; it is not a pre-fit attestation. Source workers scored their frozen
baseline predictions before persisting vectors. No fitted calibration candidate
or oracle selection used this order.
