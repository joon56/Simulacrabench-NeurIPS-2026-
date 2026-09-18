# E041 actual learned metric: observed Adult screen

The production `fit_sections` matcher gives small positive audit differences
on both fixed seeds. Neither paired 95% interval excludes zero; this screen
does not establish a reliable improvement and does not clear a +.005
three-instrument-equivalent threshold. No parameters were changed after
examining audit scores. This is external evidence, not an HSCC forecast.

Revision v2 corrects the production selector's incumbent donor posterior
from top32 to top10, following core review. Learned candidate count remains
32. The external protocol is unchanged, including its fixed-top32 audit
comparator. This is a correctness correction, not audit-driven tuning.
Earlier measurements and documentation are preserved as
`e041-external-learned-v1.json` and `e041-external-learned-v1.md`.
Measured core SHA-256:
`c374daff2dd4972a384b164743011831c824bc757762baf24ef3192c2a53701e`.
The final snapshot's core hash is
`fb9a3da5dde1586d53ec7f9e9236158d3b1eefb90438e9b2bec9d98e1c73a886`;
only its documentation string changed afterward to clarify proxy selection
and tied candidates. Production behavior is unchanged by that edit.

## Specified protocol

Source, transformations, distinct-profile sampling and CC BY 4.0 attribution
remain as recorded in `e041-external-source-method.md`. Exactly the same
5,000 profiles and order are used for each seed (41 and 42):

- Rows 0–1999: reference bank, the only source of retrieved answers.
- Rows 2000–2999: supervised metric fitting queries.
- Rows 3000–3999: metric activation and final blend selection.
- Rows 4000–4999: untouched audit queries.

The same categorical logistic base is fitted to rows 0–2999 for every arm.
Its selection/audit predictions are out of sample. All retrieval candidates
come from the 2,000-row bank, including candidates for metric fitting queries.
Base training can see bank and fitting-query labels, but no selection/audit
label. Query answers are wholly hidden at inference.

Initial per-GIVEN weights are bank-only negative log collision probabilities,
matching the production rarity-weight form. Production `candidate_indices`
freezes 32 candidates. This differs from the preceding oracle's category
rarity and 3,000-row bank; these are separate scoped screens, not a direct
fraction-of-oracle-recovered calculation.

Call production `fit_sections` unchanged with default optimizer, penalty,
section activation threshold and iteration limit. Its learning objective
uses a bank marginal base; its selector compares learned and initial metrics
with fitted prior/retrieval shares. Activate only sections approved by that
selector, retaining initial weights elsewhere. At deployment, construct
section-shared softmax donor distributions using those approved weights.

Both the fixed and supervised arms separately select a section-shared blend
with the same honest logistic base. Alpha grid is `{0,.1,.25,.5,.75,1}`;
choice uses only selection log score. This selection set is also used for
core section activation. Audit rows remain separate from both decisions.
No refitting on selection rows, no per-cell donor choice, no oracle labels.

The external blend deliberately uses honest held-out logistic probabilities.
Production E041 retains E025's legacy lambda replay, including its separate
base-validation limitation. **This screen validates the learned metric in
the stated honest-base wrapper, not the whole E025/E041 production stack or
its replay calibration.** Approximate HSCC gates are absent from Adult.

## Audit measurements

| Seed / method | Log score | Skill |
|---|---:|---:|
| 41 logistic | -1.009983389 | .332721080 |
| 41 fixed retrieval + logistic | -1.009371402 | .333125410 |
| 41 supervised retrieval + logistic | -1.008471069 | .333720244 |
| 42 logistic | -1.027552730 | .321113314 |
| 42 fixed retrieval + logistic | -1.027159322 | .321373232 |
| 42 supervised retrieval + logistic | -1.026512916 | .321800301 |

| Seed | Supervised-minus-fixed log | Skill gain | Skill gain / 3 | Paired 95% skill interval |
|---|---:|---:|---:|---:|
| 41 | +.000900333 | +.000594835 | +.000198278 | [-.000054886, +.001244556] |
| 42 | +.000646406 | +.000427069 | +.000142356 | [-.000028212, +.000882351] |

Supervised gains over logistic alone are +.000999164 and +.000686987 skill.
Intervals use respondent-level paired log-score standard errors, scaled by
the schema-only `U=1.51358503744`; they are conditional on each trained model
and omit refitting uncertainty. Seeds reuse one source dataset and are not
independent dataset replications. The `/3` column is arithmetic only.

Core selected all three sections in seed 41 and family/employment in seed 42. Final
supervised alphas (family, employment, finances) were (.25,.1,.1) and
(.1,.1,.1). Fixed alphas were (.1,.1,.1) and (0,.1,.1). These choices precede
audit scoring. A small blend was preferred despite large oracle headroom.

Domain interpretation: observed census correlations provide enough signal
for slightly different section metrics. The measured audit differences are
too small and uncertain to support substantial transfer claims. They do not
explain the HSCC leaderboard gap or establish household recurrence.

## Verification and reproduction

Executable checks verified disjoint bank/fitting/selection/audit identities;
masking audit labels preserved fitted metrics and section activation exactly;
changing all selection labels preserved fitted metrics exactly; masking all
query labels preserved logistic and evidence predictions exactly. All
probability vectors sum to one. Official floor mixing and pooled skill are
shared with the preceding helper. Syntax compilation passed.

One process, at most two numerical-library threads; 2.20/2.24 seconds per seed
including repeated fits for leakage assertions, excluding import time. These
are external helper timings, not production runtime measurements.

```powershell
.venv/Scripts/python.exe tests/e041_external_learned.py
```

Complete numeric results, weights, core selector diagnostics and model source
SHA-256 are in `e041-external-learned.json`. Core model, earlier oracle,
status, daily log and experiment records were not changed by this task.
