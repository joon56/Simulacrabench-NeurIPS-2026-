# E075 — Neighbour trees fed by E041's supervised retrieval (expert `r`)
parent: E074
status: parked
date: 2026-11-13

## Registration (before any hosted run)

All 21 sprint uploads read as ties with E041, including the three of 2026-11-13 (E073c
calibration, E073xm log-linear pool with the vote trees, E074t honest copy share). The two
largest real-data effects on UNHCR in the whole hosted history are
- the supervised section metric for donor retrieval: E025 .89 -> E041 .92 (old scale), and
- trees that learn from the donors' answers instead of a per-item mixing share: E025's
  Fellegi-Sunter retrieval with lambda mixing .89 -> E073n (same retrieval, trees) .91.
They have never been combined: E041 consumes the supervised retrieval with a per-item lambda,
the tree experts n / m consume the unsupervised retrieval. Pools of the two outputs (E073s,
E073xm) cannot recover that combination.

Expert `r`: the m trees (GIVEN, roster totals, three nearest rows by Fellegi-Sunter weights
with scores and agreement flags, soft votes of the ten nearest) plus, per head, E041's own
retrieval refitted on the context rows by E041's unchanged code (`fit_sections`, 32
candidates, self excluded): donor-weighted class shares under the learned section metric and
under the initial metric, and the weights and answers of the three heaviest donors. Learned
metrics of all sections are offered (no activation rule); the trees decide. Labels of query
rows are never read; context rows get leave-one-out features.

## Domain check

- Technical: same honesty as n / m (leave-one-out donors for training rows). The metric fit
  uses labels of 2,000 context rows that are also tree-training rows; 18 parameters per
  section, so the leak is negligible. More features per head (2K + 6) on the same 8k rows
  can add variance: on fabricated cluster data r is slightly worse than m (-.111 against
  -.059 log on copies) because the unsupervised retrieval is already perfect there.
- Background: no new population assumption; the supervised metric's real-data value is the
  hosted E041 reading itself. Expectation: unknown. The additive reading (.92 + .02) is naive
  and is not a forecast.

## Uploads and arms (single noised/rounded readings; development scores do not count for the Final)

E075ra — expert r alone on every instrument (no E041 fit, no guard), comparable with E073n
(n alone: UNICEF .3364 / WB .2185 / UNHCR .8264 = old .51 / .48 / .91) and E041
(.3499 / .2335 / .8457 = old .52 / .49 / .92):
- UNHCR >= .8650 (old .93), WB >= .2486 or UNICEF >= .3635: r alone beats the whole E041
  stack there -> r becomes the primary model of the Final on that instrument (pooled with
  E041 behind the guard).
- Equal to E041's bin: the supervised retrieval lifts the trees by about one bin (n alone was
  one bin lower) -> guarded pool of E041 and r in the Final.
- Equal to n's bin: retrieval features add nothing readable -> r only as one more guarded
  candidate. Lower than n's bin: the extra features hurt -> r dropped.
- Failed status: not counted; lighten and re-upload.

## Results

**Local engineering, 2026-11-13 (fabricated data; not efficacy evidence).** Self-tests
(tests/test_e075_retrieval.py via tmp/e075_selftest.py) PASS x3: feature shapes and
finiteness, learned-metric share on the truth high for cluster copies and low for fresh
profiles, valid distributions, copies learned, chain grammar (`rmix100`, `rlpool`, `regate`
unaffected).

**r alone, local (official scorer, kit aa03186; synthetic).** Clean sandboxes: PASS x3, UNHCR
70.0 s (expert fit 57 s), WB 48.4 s (41 s), UNICEF 37.4 s (31 s); UNHCR log -.568172 against
E041 -.551737 and n alone -.567220 (the sandbox has no neighbour structure and favours the
network, as for every tree expert). Two-fidelity duplicate simulation
(tmp/e074_make_sim2.py): r alone -.355996 against E041 -.388611 (+.0459 old-scale skill; the
guarded m-pool reached -.353962), 80.5 s. Mechanism and plumbing evidence only.

**Guarded packages, local (synthetic).** E075rp (UNHCR guard over r alone, r pools,
calibration): clean PASS x3, 525 s, rejected, equal E041; on the two-fidelity simulation
`rlpool+cal` accepted (E lower bound +.0224), -.354438 against E041 -.388611, 562 s. E075rw
(WB and UNICEF guards): clean PASS x3, 441 s, rejected, equal E041. Identities, arms and
runtime estimates: ../../submissions/2026-11-14-E075/SCORES.md.

**Hosted, 2026-11-14 (user-pasted API fragment, owner `minjoonyoo`).** E075ra ID 1051843:
UNICEF .3093047995 / WB .1884410501 / UNHCR .8264422186 = old-scale .49 / .46 / .91 (E041 .52 /
.49 / .92; n alone .51 / .48 / .91). Arms: UNICEF and WB below n's bin -> the retrieval
features hurt there, **r dropped on UNICEF and WB**; UNHCR equal to n's bin -> nothing readable
from the retrieval features, **r stays only as a guarded candidate on UNHCR**. E075rp / E075rw
were withdrawn before upload (E076p took the UNHCR guard slot).

## Decision

- Local: technically qualified only (no synthetic gain).
- DEV exploration: closed; r alone does not beat the E041 stack on any instrument.
- TEST: r is a guarded UNHCR candidate of the Final and nothing more
  ([E077](E077-final-structural-exclusions.md)).
