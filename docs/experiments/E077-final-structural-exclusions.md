# E077 — Final revision: r dropped on WB / UNICEF; structural exclusions (`det`) tried and removed
parent: E076
status: adopted
date: 2026-11-14

## Registration (2026-11-14, after the last development readings, before any score of this source)

Development closed with E075ra, E076q and E076p (scorecards in submissions/2026-11-14-E075 and
submissions/2026-11-14-E076): r alone old-scale UNICEF .49 / WB .46 / UNHCR .91, q alone .50 /
.46 / .91, the UNHCR guard under E_Z 1.0 equal to E041. Twenty-four sprint uploads, no readable
gain over E041. r / q are not the missing lever: on UNHCR they sit in n's bin, on the two
instruments without donor structure the retrieval features cost two to three bins.

Two changes to the Final (E076f is superseded and was never uploaded):

1. **r is removed from WB and UNICEF.** This is the E075ra arm registered on 2026-11-13
   ("below n's bin: the extra features hurt -> r dropped", read per instrument). The E076
   Final scorecard listed only two revision rules and said "no other change"; that sentence
   left this earlier arm out by mistake. The earlier arm governs. UNHCR keeps r and q as
   guarded candidates (arm "equal to n's bin"); E_Z stays 1.0 (E076p not adverse); q stays
   (same bin as r).

2. **New guarded chain part `det`** — this goes beyond the E076 sentence "revised only by the
   arms" and is registered here as a new prospective decision. It is not derived from any
   development reading (none can read it) and is accepted only by the in-run guard.
   Rule (second version, see the attempt log): for gated heads only. Where at least 200
   labelled rows share one GIVEN value, or one pair of GIVEN values, and every one of them
   carries the gate value (the item was never asked there) or none does (always asked),
   although the other side would be expected at least 30 times at the instrument-wide rate,
   the gate-value probability of held rows in that stratum is bounded below by 1 - 3 / (n + 2),
   respectively above by 3 / (n + 2) ("rule of three", the 95 % bound for an event unseen in n
   rows). The asked answers keep their proportions; rows inside their bounds are returned bit
   for bit. Labels of held rows are never read; in the shadow run the counts come from the F
   rows only.
   Why: project rule "structure before parameters". E041 deliberately softens every UNHCR
   gate and then mixes donor answers in, so an answer that the routing excludes for a GIVEN
   stratum keeps probability whenever donors differ in that field. Measured on the synthetic
   UNHCR sandbox (phase 1, E041): the one item whose declared parent is GIVEN
   (`s2_3_boys_6_17`) gets P(sentinel) .71 on rows where the sentinel is certain (loss .35 per
   cell) and .02 where it is impossible. On WB / UNICEF the declared GIVEN-parent gates are
   already at the floor. The schema declares one GIVEN parent on UNHCR and states that some
   gates are inferred and that conditions on several items do not fit its one-parent format;
   routing on household composition (GIVEN roster counts) or country would be exactly such
   undeclared structure. Pair strata cover two-field conditions.

Also: candidate chains with one and the same S score count as one candidate (an inert `det`
variant must not use up the second E test).

## Domain check

- Technical: the bound is a 95 % upper limit, not a point estimate, and it acts only on the
  asked / not-asked dimension, where routing is deterministic by design; a stratum whose true
  rate is merely extreme is left almost untouched because a calibrated base already sits
  inside the bound. The guard measures the net effect on honest rows. The final run has more labelled rows than the shadow run, so a few more strata pass
  the 200-row line; the rule is the same.
- Background: CATI instruments route on household composition (children of school age,
  working-age members, elderly) and on country of asylum; such routing makes whole answer
  sets impossible for known GIVEN values. How many UNHCR items follow GIVEN-only routing is
  unknown; the description says the three s3_11 branches depend on answers, not on GIVEN.
  Expectation: unknown, plausibly below one bin. No forecast.

## Attempt log (append-only)

- **v1, built and measured 2026-11-14, discarded before any package was validated.** Rule: any
  answer unseen in a stratum of >= 200 labelled rows with expected count >= 30 was bounded by
  the rule-of-succession value 1 / (n + K), on every head. Clean UNHCR sandbox, phase 2:
  179,975 bounded cells in the shadow run and an S score .00215 log **below** E041 for `det`
  alone (every `+det` variant negative); the guard rejected all of them and the package
  output equalled E076f (`qlpool` accepted, +.000277). Diagnosis: among thousands of strata
  the zero counts are mostly sampling zeros of answers that are rare there but possible; a
  point estimate under a uniform prior ignores that selection and is over-confident by a
  factor of two to four. The guard worked, but an over-confident rule does not belong in the
  package (project rule: overconfidence is the cardinal sin).
- **v2, built and measured 2026-11-14, removed.** Gated heads only, the asked / not-asked
  dimension only, 95 % bound 3 / (n + 2); stated before the run: if v2 also scores below E041 on
  S locally, `det` is removed. Self-tests PASS x3 (tests/test_e077_det.py on
  tmp/e077/det-attempt/build-f-v2). Clean UNHCR sandbox, phase 2: 14,944 bounded cells, `det`
  alone -.000001 against E041 on S, `xlpool+det` +.000100 against `xlpool` +.000151, `qlpool+det`
  +.000132 against `qlpool` +.000180 — about .00005 below the same chain without it. The guard
  again accepted `qlpool` (+.000277). **Removed from the package by the stated rule; no third
  version.** The one declared GIVEN-parent item does gain, but other gated heads whose
  stratum rates are merely extreme lose as much. Code kept:
  submissions/2026-11-15-E077/det-attempt/main.py, tmp/e077_patch.py, tests/test_e077_det.py.
  Not tested on real data; the question whether real UNHCR has GIVEN-only routing that E041
  dilutes stays open.

## Local qualification criterion (fixed before the phase-2 runs were read)

Official phase 2 PASS on all three clean sandboxes with valid vectors; no instrument more
than .0005 log below E041 in the same phase (a null chain can pass the 1.0 rule); the
acceptance, refit and final-application path exercised on the duplicate simulation.

## Final package E077f (upload after 2026-11-15 21:00 KST, main account, one success)

Source: submissions/2026-11-15-E077/main.py, a byte copy of the E076 source (no `det`, no
other code change); the package differs from E076f in two build constants only (CANDIDATES
and XSTACK_BY of WB / UNICEF). E_Z 1.0, S1000 / E1000 guard, at most two chains E-tested,
strict, no time fallback.
- UNHCR (unchanged from E076f): E041 seed 0; experts r, q; chains `xlpool, xlpoolh,
  xlpool+cal, xlpoolh+cal, qlpool, qlpoolh, qlpoolh+cal, rlpool, rlpoolh, rlpoolh+cal,
  xlpoolh+twinh, xlpoolh+twinh+cal, twinh, twinh+cal, cal`.
- WB, UNICEF: E041 mean of seeds 0, 1, 2; experts g, TabICL (r removed); chains `xlpool,
  xlpoolh, xlpool+cal, xlpoolh+cal, lpool, lpoolh, glpool, cal`.
Fallbacks: E077fs (same composition, non-strict, BUDGET_SECONDS 3300), then
submissions/2026-09-25-E041.zip.

## Results

**E077f, official phase 2, clean synthetic sandboxes, 2026-11-14 (engineering evidence only).**
PASS x3, 1,117 s: UNHCR 556.0 s, `qlpool` accepted, log +.000277 against E041, vectors
bit-identical to E076f; WB 392.2 s, `lpool` (TabICL) accepted, +.001523; UNICEF 168.6 s, `lpool`
accepted, +.000965. Criterion met (no instrument below E041). Duplicate simulation in phase 2:
`xlpoolh+twinh+cal` accepted, +.0372, 907.8 s — acceptance, refit and final application
exercised. E077fs PASS x3, 1,163 s, same vectors (WB to 5e-8). Self-tests PASS x13, ZIP checker
OK. Identities, runtime estimate and the upload ladder: ../../submissions/2026-11-15-E077/SCORES.md.

Reading: removing r from WB / UNICEF changes nothing on the sandbox (its pool exponent was 0
there) and saves about 160 s; the package is E041 plus candidates that must pass an honest
in-run test. No local or hosted evidence supports more than sub-bin gains.

## Decision

- Local: technically qualified (phase-2 PASS x3, criterion met, acceptance path exercised).
- DEV exploration: none possible (development closed 2026-11-14 21:00 KST).
- TEST: **E077f was uploaded by the user as the Final on 2026-11-15 (ID 1053618, Finished):
  Grand .4790691441, UNICEF .3427149262, WB .2344919185, UNHCR .8600005877 (exact TEST skill).**
  "Adopted" here means: this is the submitted entry. No improvement over E041 is claimed; the
  TEST score has no E041 counterfactual and the guard's decisions are not observable.
  `det`: removed, parked.
