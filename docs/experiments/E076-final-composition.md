# E076 — Final composition: guarded pools, pairing-aware retrieval trees (`q`), E-row quantile 1.0
parent: E075
status: parked
date: 2026-11-13

## Registration (2026-11-13, before any hosted run of this source)

User question (2026-11-13): is the last generated package fit to be the Final, and if not, build
the best one. Answer recorded here: the E075 packages are development probes (r alone; guards
on a subset of instruments under 900 s) — none of them is a Final package. The Final needs every
instrument, the 3600 s budget, TRAIN+DEV visible, and a decision rule suited to exact scoring.

Re-read of the evidence (hosted history, schema description, kit README):
- 21 sprint uploads tie E041; the leaderboard resolves only >= 1 old-scale bin. About 50
  entries sit above us (WB one bin, UNHCR one to two bins). On the marginal-reference scale our
  UNHCR loss is .1543 R against .1157 R for the leaders (25 % less): a structural gap.
- Only the donor-retrieval axis ever moved real UNHCR (E018, E022, E025, E041). The sprint
  tested how evidence is consumed (mixing, trees, pools, calibration, twin), not what the
  retrieval knows.
- Schema description: both rounds fall inside the same two-month window; EXCLUDE keeps
  `panel_hh_key`, `bc3_followup_permission_lbl`, `..._interviewed_before_lbl`. E013 (exact
  cross-round key) armed nothing and E036 (relation-specific lambda) read flat, so literal
  cross-round keys are not the mechanism; whether donors come in pairs is unknown.

Source changes (tmp/e076_patch.py; E075 source otherwise unchanged):
1. `E_Z` — build-time one-sided quantile of the E-row confirmation (was the literal 1.645).
2. `XSTACK_BY` — per-instrument expert sets for the multi-expert chains.
3. Expert `q` = r plus **label-informed donor pairing**. For every labelled row the best and
   second-best answer agreement with its 32 GIVEN-nearest labelled rows is turned into a robust
   z-score (median / MAD over those rows). A high z marks a row whose twin is already labelled
   ("completed pair"). Four donor-only fields enter E041's supervised section metric: "no twin
   at level z < 2.5 / < 3.5 / < 5" (non-negative weights add up to a graded bonus for unpaired
   donors, so no single threshold has to fit the real data) and "has a twin, z >= 5" (the
   opposite, cluster-like case); weights are learned by the unchanged `fit_sections` from a
   start of 0. The z of the three heaviest donors is also given to the trees. For labelled rows used as
   tree-training queries the donor's flag is computed without the asking row (second-best
   agreement when the best partner is the asker), so training and held-out rows see the same
   semantics. Rationale: if records come in pairs, a labelled row whose twin is also labelled
   cannot be the twin of a held-out row; removing such impostors concentrates the posterior on
   the true twin exactly where GIVEN alone is ambiguous. If records come in larger clusters the
   opposite sign is learnable (second flag). With no pairs both flags are constant and q = r.

Decision rule of the Final (prospective, stated before any score of this source): accept the
best S chain when mean(d) - 1.0 * sd(d) / sqrt(n) > 0 on the E rows (two chains tested at
most). Reason: the 1.645 rule was set for development probes that had to be readable through
a noised, rounded board; the Final is scored exactly, so the expected score is what matters. A
chain with true gain of one standard error passes with probability .50 instead of .26, a null
chain with .16 instead of .05 (harmless by definition), a chain one standard error below zero
with .02. This does not rewrite any earlier registration or verdict.

## Domain check

- Technical: the pairing flags read labels of labelled rows only; S/E rows are hidden in the
  shadow run, so their twins appear unpaired there exactly as the twins of TEST rows do in the
  final run. Regime difference: inside the metric fit a third of the labelled rows are queries
  (more donors look unpaired than at deployment), so the learned weight is conservative.
  Fabricated pair world with impostors (tests/test_e076_pairing.py): q -.996 against r -1.096
  log per cell (r cannot beat uniform there); rows without a visible twin pay -.07; without
  pairs q = r to .0002.
- Background: CATI re-contacts and duplicate registrations are plausible sources of paired
  records (E018 record); the description treats rounds as independent because no key links
  them, which does not exclude re-contacted households. Expectation: unknown. The real data
  already yield strong evidence from GIVEN alone, so ambiguity may be rare; no forecast.

## Development uploads of 2026-11-14 and arms (single noised/rounded readings)

Trio: E075ra (r alone, built 11-13), **E076q** (q alone, every instrument), **E076p** (UNHCR
guard over `rmix100, rlpool, rlpoolh, rlpool+cal, rlpoolh+cal, cal`, E_Z 1.0, BUDGET 830; UNICEF
and WB = E041). E075rp / E075rw are withdrawn before upload (same chains under the old 1.645
rule; the WB / UNICEF guard path was already exercised hosted on 11-13).
- E076q against E075ra, UNHCR: q at least one bin above r -> pairing information is real;
  q leads the Final's UNHCR pool. Same bin -> unresolved (inert or sub-bin); both stay guarded
  candidates. q below r -> the flags hurt on real data; q is removed from the Final.
  Against E041: UNHCR >= .8650 -> readable gain over the whole stack.
  WB / UNICEF: a second reading of the r family (flags expected inert there).
- E076p: UNHCR >= .8650 -> readable gain from the guarded choice under E_Z 1.0. .8457 / .8264
  -> unresolved. <= .8071 -> adverse: the Final returns to E_Z 1.645.
- Failed status: not counted; lighten and re-upload inside the window.
No numeric expectation is stated.

## Final package E076f (upload after 2026-11-15 21:00 KST, main account, one success)

Every instrument: E041 (seed mean over 0,1,2 on WB and UNICEF; single seed on UNHCR, whose
shadow run is single-seed) plus the S1000 / E1000 guard with E_Z 1.0, strict, no time fallback
(a failed Final attempt may be retried; a silent fallback could not be).
- UNHCR, experts r and q: `xlpool, xlpoolh, xlpool+cal, xlpoolh+cal, qlpool, qlpoolh,
  qlpoolh+cal, rlpool, rlpoolh, rlpoolh+cal, xlpoolh+twinh, xlpoolh+twinh+cal, twinh, twinh+cal,
  cal`.
- WB and UNICEF, experts g, r and TabICL: `xlpool, xlpoolh, xlpool+cal, xlpoolh+cal, lpool,
  lpoolh, glpool, rlpool, rlpoolh, cal`.
The composition is revised only by the arms above (q removed; E_Z back to 1.645).

## Results

**Local engineering, 2026-11-13 (fabricated and synthetic data; not efficacy evidence).**
Self-tests tests/test_e076_pairing.py (tmp/e076_selftest.py, model venv) PASS x5: completed
pairs flagged (61 % of visible rows; partner answers agree > .9), more learned-metric mass on
the twin's answer, q beats r where twins compete with impostors (-.998 against -1.096 log per
cell; rows without a visible twin pay -.07, the average gains +.10), q = r without pairs
(-1.1257 against -1.1253), chain grammar and build constants. With a weak pairing
signal (12 answers per record) the graded fields still gain: -.974 against -1.085. A first
version with two fixed thresholds (z < 3.5, z >= 5) was replaced before any package was
validated: a real twin whose z fell between or below the thresholds would have been read as
unpaired.

**q alone, official scorer, clean sandboxes (phase 1).** PASS x3, 168 s; logs equal r alone to
.0005 (no pairs on the sandbox, fields inert). Duplicate simulation with identical GIVEN copies:
-.356267 against r -.355996 (nothing for pairing to resolve there).

**E076p, phase 1.** PASS x3, 513 s; under E_Z 1.0 the clean UNHCR guard accepted `rlpool` (E
lower bound +7.8e-7) and the official log moved +.000110 against E041 — the 1.645 rule had
rejected the same chain on the same data (E075rp, lower bound -.00007). Duplicate simulation:
`rlpool+cal` accepted, -.354438 against E041 -.388611.

**E076f, phase 2 (TRAIN+DEV visible, TEST scored).** PASS x3, 1,276 s: UNHCR `qlpool` accepted
(+.000277 log against E041), WB `lpool` with TabICL (+.001523), UNICEF `lpool` (+.000965).
Duplicate simulation in phase 2: `xlpoolh+twinh+cal` accepted (exponents E041 .21 / r .43 /
q .34), +.0372, 881 s. Identities, runtime estimates and the upload ladder:
../../submissions/2026-11-15-E076/SCORES.md; development identities and arms:
../../submissions/2026-11-14-E076/SCORES.md.

Reading: the package runs end to end in both phases and its guard only passes chains with
positive honest evidence; every synthetic gain is far below one leaderboard bin. Whether r / q
carry more on real data is what the 2026-11-14 readings ask.

**Hosted, 2026-11-14 (user-pasted API fragment, owner `minjoonyoo`).** E076q ID 1051842:
UNICEF .3228478426 / WB .1884410501 / UNHCR .8264422186 = old-scale .50 / .46 / .91; r alone the
same day .49 / .46 / .91. UNHCR arm: same bin as r -> **unresolved**, pairing fields inert or
sub-bin; q stays a guarded candidate. E076p ID 1051845: equal to E041 on all four values ->
**unresolved**, not adverse; **E_Z 1.0 stays**. Development closed: 24 sprint uploads without a
readable gain.

**E076f superseded before upload (2026-11-14).** The E075ra arm removes r from WB and UNICEF;
the Final scorecard's "no other change" had left that earlier arm out. Successor:
[E077](E077-final-structural-exclusions.md).

## Decision

- Local: technically qualified (phase-2 PASS, self-tests, acceptance path exercised).
- DEV exploration: E076q and E076p uploaded by the user on 2026-11-14; both unresolved.
- TEST (as registered 2026-11-13): E076f is the prepared Final; the user uploads and decides.
  Revisions only by the registered arms.
- TEST (2026-11-14): E076f was not uploaded; superseded by E077f. Source, E_Z rule, expert q
  and XSTACK_BY carry over unchanged.
