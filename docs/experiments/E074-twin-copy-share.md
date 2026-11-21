# E074 — Honest copy share from the best-matching labelled rows (`twin`)
parent: E073
status: parked
date: 2026-11-13

## Registration (before any hosted run)

Re-read of the hosted history (2026-11-13, [SCORES](../../submissions/SCORES.md)): on real UNHCR
only the neighbour-evidence axis ever moved the score — E018 same-round donors .79 -> .87,
E022 Fellegi-Sunter weights .88, E041 supervised section metric .92 — while base-model class,
capacity, gates, sentinel calibration, TabICL, trees and stacks all read as ties. E014
(cross-round donors only) gained nothing, so the useful donors are same-round near-duplicate
rows. Row order is excluded as a channel: the kit README states the rows were permuted before
ids were assigned ("Row position carries no information").

Three known weaknesses of how E041 uses its donors (source lines in
`submissions/2026-09-19-E041/main.py`):
1. the mixing share lambda is fitted against base predictions that are in-sample for the
   replay rows (E018 record: "lambda errs low"); for active sections only 800 replay rows;
2. two buckets per item (top posterior weight >= .5 or not) pool exact matches with weaker
   ones, so one lambda serves both;
3. the grid stops at .98.

`twin` (chain part, applied after E041's whole pipeline): evidence = answer shares among the
labelled rows tied at the best Fellegi-Sunter match score (5 candidates searched, self
excluded); final = (1 - r) * current + r * evidence with
r = .9995 * sigmoid(a + x.g [+ d_head]). x are label-free features of the match: per-field
disagreement with the best row, at least two / three labelled rows agreeing on the whole GIVEN
block, how alike the two best rows answer over all items (raw, and when both are exact, also
as a >= .98 flag), ties. `twin` = global coefficients; `twinh` adds per-head shifts (ridge).
Parameters maximize the officially floored log-likelihood on the S rows of the shadow run
(base predictions and donors both honest there: the S/E rows are hidden from that fit), ranked
by two-fold out-of-fold S score, confirmed on E (one-sided lower bound > 0), refitted on S+E
and applied to the all-visible run. Start: constant share .018, so no signal leaves E041
essentially unchanged and the guard rejects.

Related earlier work, all stopped on proxy channels or tied when hosted: E019 (cap .98 + two
buckets; hosted no visible gain), E042 (constant final blend; sim oracle +.0046 log, parked),
E047 (extra share <= .5 from entropy/agreement features per section; hosted tie), E050 / E053
(honest lambda selection; Adult-proxy oracles below gate). Differences here: match-quality
features (field disagreement, exact multiplicity, donor-donor agreement), ceiling .9995, 2,000
honest rows, evidence independent of E041's learned softmax. Prior for a readable gain is low
given those ties; the internal guard makes the attempt safe.

## Domain check

- Technical: label-free features only; S/E labels never enter the shadow fits; fitted parts
  ranked out of fold; refit on S+E after acceptance. Limit: the shadow bank has 6,279 rows,
  the final bank 8,279 (more exact matches at inference); the share is conditional on match
  quality, which should transfer, but this is unverified.
- Background: UNHCR CATI operations have known duplicate sources (re-dials, several numbers or
  registered cases per household); the schema keeps an excluded `include_final_analysis1`
  flag, consistent with rows that analysts would drop. Whether duplicates are literal copies
  (share near 1) or re-interviews (item-specific agreement) is unknown; the features let the
  data decide. Expectation before the run: unknown; no numeric forecast.

## Upload and arms (single noised/rounded readings; E041 bins: UNICEF .3499, WB .2335, UNHCR .8457)

E074t: UNHCR and WB candidates `twin, twinh, twin+cal, twinh+cal, cal, tpoolh`; UNICEF = E041.
- UNHCR >= .8650 or WB >= .2486: readable gain from the honest copy share -> first candidate
  of the Final.
- Equal bins (UNHCR .8457; .8264 is E041's own boundary reading): unresolved — rejected
  internally or accepted with a sub-bin gain; stays in the Final behind its guard.
- UNHCR <= .8071 or WB <= .2185: adverse (accepted internally, worse when applied to the
  all-visible run) -> dropped from the Final.
- Failed status: not counted; fix and re-upload.

## Results

**Local engineering, 2026-11-13 (fabricated and synthetic data; not efficacy evidence).**
Self-tests (tests/test_e074_twin.py via tmp/e074_selftest.py, model venv) PASS x5: evidence
and features on fabricated duplicate clusters; fitted share > .9 on cluster copies and < .35
on fresh profiles with an out-of-sample gain; inert without signal; stationarity of the fit;
chain application, reuse of stored parameters and out-of-fold scoring.

**Clean synthetic sandboxes (official scorer, kit aa03186).** First build (single cautious
start): PASS on all three, UNHCR 368.5 s / WB 104.3 s / UNICEF 27.6 s; every twin fit collapsed
to a share of about .001, every chain rejected, UNHCR 132,273 vectors equal E041.

**Duplicate-injection simulations (synthetic UNHCR sandbox; tmp/e074_make_sim.py and
tmp/e074_make_sim2.py; engineering evidence about the mechanism, not about real data).**
- Sim 1 — 40% of rows are same-wave copies of another row (whole GIVEN block, answers with 5%
  replaced): E041 already uses this structure (S log -.362 against -.552 on the clean table);
  with the single cautious start the twin share collapsed (a = -7.9, quality terms unmoved)
  and nothing was accepted: E074t = E041 = .4181 (new-scale skill). Diagnosis: the mean effect
  of a constant extra share is negative, the intercept falls first and the gradient of the
  quality terms vanishes. Repair (tmp/e074_patch2.py): a second start that trusts rows whose
  best match agrees on every field (a = 1, -3 per disagreeing field); the better optimum is
  kept. Self-tests PASS x5 after the repair.
- Sim 2 — 25% exact copies (2% of answers replaced) and 25% "siblings" (two GIVEN fields
  re-drawn, 50% of answers replaced), so one share per item cannot serve both: out-of-fold S
  gains twin +.0031, twinh +.0033, twin+cal +.0053, twinh+cal +.0056, cal +.0017, tpoolh
  +.0006 log; E lower bound for twinh+cal +.0042 -> accepted, refit on 2,000 rows, applied.
  Official scorer: E041 log -.388611 (old-scale skill .452594), E074t -.381541 (.462553):
  **+.0071 log, +.0100 old-scale skill**, 443 s against 271 s. The acceptance, refit and
  final-application path ran end to end.
Reading: where copy fidelity varies with match quality the estimator finds about one
leaderboard bin on synthetic data and is inert otherwise. Whether real UNHCR has that
heterogeneity is exactly what the hosted reading asks.

**Uploaded build (two-start fit), clean synthetic sandboxes, 2026-11-13.** ZIP checker OK;
official phase 1 PASS on all three: UNHCR 311.1 s, WB 104.9 s, UNICEF 27.0 s; all chains
rejected, UNHCR vectors equal E041 (0 of 132,273 changed). Identity and arms:
../../submissions/2026-11-13-E074/SCORES.md.

**Hosted, 2026-11-13 (user-pasted API fragment, owner `minjoonyoo`).** E074t ID 1050759:
UNICEF .3499339289 / WB .2335276584 / UNHCR .8457264165 = E041 on every value. Arm:
**Unresolved**. No readable gain from the honest copy share on real data.
