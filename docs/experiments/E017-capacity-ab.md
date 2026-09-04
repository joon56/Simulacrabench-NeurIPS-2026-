# E017 — pre-registered leaderboard A/B: trunk capacity on real data
parent: E015
status: rejected
date: 2026-09-05

## Hypothesis

E015's per-instrument architecture grid (width {64,128,256} × depth
{2,3} + dropout, holdout-selected) gains on REAL data despite its local
+0.0001, because the sandbox's 1-factor generator provably caps what
capacity can show locally (E009/E011/E015 — three independent nulls)
while the campaign's most replicated pattern is real GIVEN-answer
structure exceeding the sandbox's (E005 2×, E008 3–5×, E010 invisible
locally yet +0.03 real). With the linkage line closed (E013/E014), the
0.92-vs-0.78 unhcr gap has capacity as its leading surviving
explanation — and the ONLY instrument that can measure it is a
leaderboard slot.

## Why this is a legitimate slot spend (rule 4 audit)

Rule 4 forbids spending submissions on UNVERIFIED changes. E017 is not
an unverified change — it is a pre-registered MEASUREMENT of a verified-
safe change: locally the model is +0.0001 vs E012 (no regression
anywhere, suite green), so the downside is bounded at noise, while the
information value is the entire capacity research direction (three
parked experiments wait on this bit). E015's park verdict explicitly
named this A/B as the revive path.

## Pre-registered readings (BEFORE submission)

Reference: E012 LB = 0.60 (unicef 0.52 / wb 0.49 / unhcr 0.78).

- unhcr and/or wb up ≥ +0.02 ⇒ real multi-factor capacity exists and
  the sandbox hid it ⇒ REOPEN the capacity ladder (wider grids, per-
  instrument depth, embeddings) as the main line; treat local nulls as
  uninformative for this axis from now on.
- everything flat (±0.01) ⇒ capacity axis dead ON REAL DATA TOO ⇒ the
  0.92 gap is NOT model capacity ⇒ remaining suspects: unhcr structure
  (sentinel families, joint branch decoding) and calibration; stop
  spending on architecture.
- any instrument down ≥ 0.02 ⇒ the holdout architecture selection
  overfits real visible rows ⇒ pin DEFAULT_CONFIG permanently.
- unicef is the control: its selector picked the small config locally;
  a unicef move ⇒ selection instability, discount the whole reading.

## Change

No new model code: submission = `src/models/trunk_select.py` over the
E012 stack (assembled self-contained). Local scores (2026-09-03 run):
0.4436 / 0.5006 / 0.4548 / 0.5633, 3-inst 0.5062 (+0.0001).

## Result

(v1 upload failed on the platform — first hosted failure; v3, the grid
cut to the full grid's winners at ~340 s local, ran.) **Leaderboard:
Grand 0.60 — unicef 0.52 / wb 0.49 / unhcr 0.79** (E012: 0.52/0.49/0.78).

## Decision

**Capacity direction CLOSED (the flat arm, taken strictly).** Scored
against the pre-registered readings: unicef control clean ✓ (0.52,
selector stayed small); wb flat — the instrument whose 128×2 config got
its chance moved nothing; unhcr +0.01 sits INSIDE the pre-registered
flat band (±0.01) and below the +0.02 bar that was defined in advance
as the minimum evidence of real capacity gains. Reading: architecture
is not where the 0.92 gap lives; stop spending slots and development on
model size. The +0.01 whisper is noted but not actionable — the
pre-registration explicitly anticipated and discounted it (noise scale
±0.01–0.02). Residual suspects for the gap, carried forward:
within-round duplicate rows (a linkage axis E013/E014 never tested —
their candidate pools were strictly cross-round), joint decoding of the
overlapping s3_11 branches, and per-item calibration.
