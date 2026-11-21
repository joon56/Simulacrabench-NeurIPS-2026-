# E066 — UNHCR wave-coded sentinel transfer
parent: E041
status: parked
date: 2026-11-08

## Registration (before any hosted run)

Source: A047 UNHCR read-only review (subagent), checked against the local schema text.
`external/starter-kit/data/unhcr.json` (ee427a9) dataset description: "In five multi-select
families (6.4, 6.6, 6.11, 7A.7, 7B.1, 59 items) round 1 wrote 0 for respondents the routing
skipped rather than marking them skipped at all, so for those items the sentinel appears on
round-2 rows only." Prefixes s6_4_, s6_6_, s6_11_, s7a_7_, s7b_1_ match 68 PREDICT items,
all values ('0','1') except one ('0',); none is a gate parent. Kit commit 30dd72d (10-25)
removed this sentence from the description; whether the delivered data changed is unknown.

Mechanism: E041 keeps sentinel mass on wave-1 held-out cells of these items, where the
sentinel cannot occur under the documented coding. Move that mass to "0" (skipped wave-1
respondents are coded "0"). The truth-class probability of every affected cell can only rise
if the coding holds. Runtime guard on the delivered visible rows: change an (item, wave)
cell only when that wave has >= 300 visible rows, none with the sentinel, and the other wave
has sentinels. Otherwise exact E041. Synthetic sandbox gates are exact, so the local channel
cannot exercise the real coding; local runs must equal E041 exactly unless a flag triggers.

Distinct from E028 (wholesale gate decode, read flat; confounded) and E063 (wave metric).
Expected size depends on E041's residual wave-1 sentinel mass m, unknown: the review's
algebra gives about +.004 / +.010 / +.023 old-scale UNHCR skill for m = .03 / .07 / .15
(assumption-based, not a forecast).

Hosted arms (UNHCR versus the same-day E065 uploads, whose UNHCR is E041 code):
- Favorable: UNHCR higher, UNICEF and WB equal to E041-code values.
- Unresolved: UNHCR equal (residual m below resolution, or data recoded so no flag fired).
- Adverse: UNHCR lower: coding assumption wrong on held-out rows or a defect; revert.
- Technical: Failed.
E066's WB value also serves as the same-scale E041 WB control for the E065 readings.

Package: submissions/2026-11-08-E066.zip, 15684 bytes, SHA256
e1b7469a49dedce5abcfd52f8999861246530c1be0be00ebb7e73319b8cb75a1 (main.py, e041_core.py =
E041 bytes, starter-kit license). Unit tests: tests/test_e066_wave_sentinel.py 4/4 PASS.

## Results

**Local engineering, 2026-11-08.** ZIP checker OK; official score.py (ee427a9) phase 1
PASS on all three schemas through the model venv; all 189649 vectors identical to E041 in
the same environment (no flag fired on exact-gate synthetic data, as expected). Wall:
UNHCR 177 s, UNICEF 29 s, WB 66 s. Local privatized WB display .45 versus E041's .46 at the
identical exact skill .454929 (rounding-boundary noise), a reminder for hosted readings.

**Hosted, 2026-11-08 (user-supplied API fragment).** ID 1041566, Finished, Development
29772, created 2026-11-08T05:24:07.995216Z: Grand .4763960013 / UNICEF .3499339289 /
WB .2335276584 / UNHCR .8457264165, all equal to the same-day E065 uploads whose UNHCR is
E041 code. **Arm: Unresolved.** Either the residual wave-1 sentinel mass is below public
resolution or no flag fired on the delivered data (the 10-25 description change leaves
both open). No zero-effect claim; no amplified diagnostic probe (would encode data
properties into scores, against the project rule).
