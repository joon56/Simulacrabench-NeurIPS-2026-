# E067 — Composable E041 additions (expert per instrument + UNHCR transfer)
parent: E065
status: parked
date: 2026-11-08

## Registration

One source (`submissions/2026-11-09-E067/main.py`, built by `scripts/build_e067.py`) that
composes the E065 TabICLv2 expert code path (any instrument, fixed alpha or the A045
guard) and the E066 transfer, controlled by build constants PLAN / UNHCR_FIX / STRICT /
BUDGET_SECONDS. Instruments not in PLAN return exact E041 output. Purpose: day-2 probes
(UNICEF expert) and the Final package without re-writing code per combination.

Regression gate: E067 with PLAN {"world_bank": .5} reproduces E065a50 WB raw vectors
exactly — PASS (39520/39520 identical, 2026-11-08, kit aa03186 scorer).

UNICEF probe E067u25 (PLAN {"unicef": .25}): ZIP checker OK; local synthetic UNICEF exact
skill .500984 versus E041 .500648 (+.000336, engineering only), expert 37 s, UNICEF wall
69 s. ZIP tmp/e067/2026-11-09-E067u25.zip, SHA256
2a99e5ce49b08073b0ae82423363f543edd3cf84c1471d9e9fefcb0bf7ceb5db.

Hosted arms for any E067 probe: compare each changed instrument with a same-day upload in
which that instrument runs E041 code; unchanged instruments must match. Favorable /
unresolved / adverse / mixed / technical as in E065. A Final package additionally needs a
phase-2 local PASS (kit aa03186, 3600 s) of the exact non-strict build.

## Results

**Phase-2 local timing, 2026-11-08 (kit aa03186, synthetic, TRAIN+DEV visible, TEST scored).**
Package maxp2: PLAN {"world_bank": "guard", "unicef": "guard"}, UNHCR_FIX, non-strict,
BUDGET 3000 (tmp/e067/2026-11-09-E067maxp2.zip, SHA256 4134a72c...c2f2). PASS on all three:
UNICEF 135 s (guard alpha .25, lower +5.4e-5, accepted; skill +.000270), WB 274 s (guard
alpha .5, lower +.00122, accepted; +.000968), UNHCR 187 s (0 flags; raw identical to E041).
Sum of separate processes ~596 s against the 3600 s Final budget. E041 phase-2 reference:
UNICEF 32 s, WB 67 s, UNHCR 187 s.

**Further local builds, 2026-11-08 (kit aa03186 scorer, synthetic; engineering only).**
- s2 (SEEDS 0,1; no expert): log delta vs E041 UNICEF +.000327 / WB +.001208 / UNHCR +.000181;
  wall 47 / 115 / 289 s. Cellwise probability mean cannot lower the expected log score of a
  single seed (Jensen; the grader floor is affine).
- h50c (UNHCR expert, alpha .5 scaled by E041 uncertainty (1-max p)/(1-1/K)): UNHCR wall 523 s
  (E041 147 s + expert 364 s). Offline synthetic grid from the dump: expert alone -.553143 vs
  E041 -.551737; mixtures within +.0007. First build failed (JSON `true` written into PLAN);
  build script fixed to write a Python literal; failure preserved in this note.
- r1 (SEEDS 0,1 + WB guard + UNHCR transfer): UNICEF +.000327 / WB +.003329 (guard alpha .5,
  E lower +.0013, accepted) / UNHCR +.000181; wall 52 / 314 / 297 s (~663 s all three).
- Source now also carries REGATE (E068 logic) and the E069 sentinel option; earlier builds keep
  their own frozen main.py copies.
