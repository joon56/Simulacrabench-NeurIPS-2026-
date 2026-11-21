# E076 Final scorecard — registered 2026-11-13 (before the Final phase opens)

Experiment record: ../../docs/experiments/E076-final-composition.md. Source: main.py in this
folder (E075 source plus E_Z, XSTACK_BY and expert q; tmp/e076_patch.py); builder
scripts/build_e070.py. Final phase: 2026-11-15 21:00 KST to 2026-11-20 21:00 KST, one
successful upload, failed attempts may be retried, exact scoring, 3600 s. Main account only
(owner `minjoonyoo`, team "Odyssey"). The upload and the final choice are the user's.

| Package | Path | Role |
|---|---|---|
| E076f | submissions/2026-11-15-E076f.zip | **first upload**: strict, no time fallback |
| E076fs | submissions/2026-11-15-E076fs.zip | second attempt only if E076f returns Failed: same composition, non-strict (any guard error keeps the seed-mean E041 output of that instrument), BUDGET_SECONDS 3300 |
| E041 | submissions/2026-09-25-E041.zip | last resort if both fail (hosted-proven model, phase-2 PASS locally) |

Composition of E076f / E076fs (E_Z 1.0; S1000 / E1000 guard; at most two chains E-tested):
- UNHCR: E041 seed 0; experts r, q; chains `xlpool, xlpoolh, xlpool+cal, xlpoolh+cal, qlpool,
  qlpoolh, qlpoolh+cal, rlpool, rlpoolh, rlpoolh+cal, xlpoolh+twinh, xlpoolh+twinh+cal, twinh,
  twinh+cal, cal`.
- WB, UNICEF: E041 mean of seeds 0, 1, 2; experts g, r, TabICL; chains `xlpool, xlpoolh,
  xlpool+cal, xlpoolh+cal, lpool, lpoolh, glpool, rlpool, rlpoolh, cal`.

Revision rules fixed in advance (development readings of 2026-11-14, arms in
../2026-11-14-E076/SCORES.md): q below r on UNHCR -> rebuild without q; E076p adverse ->
rebuild with E_Z 1.645. Any rebuilt package needs a fresh phase-2 local PASS and replaces the
identities below. No other change.

Reading of a Failed status: a failed attempt does not use the single success. Report the
HSCC code; timeout-type codes call for the lighter E076fs or a trimmed rebuild, exception-type
codes for E076fs. A Finished status ends the competition entry: nothing is uploaded after it.

## Identities and local validation (2026-11-13, kit aa03186 scorer, model venv, RTX 3070)

- E076f 103072701 bytes, SHA256 03547f3d6fc78a6a561b4a09152474aa0b403469d0b7a20d5dafed19bc3e7918
- E076fs 103072700 bytes, SHA256 1c5aa1fb381648a1f89529735f7561f6d8172eae938e2e1c5aabc8c1fc34d8aa
  (main.py differs from E076f only in STRICT = False and BUDGET_SECONDS = 3300)
- E041 fallback submissions/2026-09-25-E041.zip (main.py 22c91180...).

E076f, official **phase 2** (TRAIN+DEV visible, TEST scored) on the clean synthetic sandboxes,
all vectors valid, against E041 in the same phase:
- UNHCR PASS 583.5 s: E041 163 s, shadow E041 158 s, shadow r 57 s, shadow q 67 s, twin 3 s;
  `qlpool` accepted (out-of-fold S +.00018, E lower bound +.00016; exponents E041 .94 / q .07),
  final q 81 s; log -.548672 against -.548949 (+.000277).
- WB PASS 488.7 s: three seeds 212 s, shadow E041 43 s, g 16 s, r 34 s, TabICL 71 s; `lpool`
  accepted (S +.00282, E lower bound +.00202; exponents E041 .43 / TabICL .52), final TabICL
  95 s; log -1.084394 against -1.085917 (+.001523).
- UNICEF PASS 204.0 s: three seeds 66 s; `lpool` accepted (E lower bound +.00059); log -.795355
  against -.796320 (+.000965).
Sum 1,276 s locally. Old-scale skill deltas +.0002 / +.0008 / +.0006 (synthetic; engineering
evidence that the whole path runs and does not lose, not a forecast for real data).
Duplicate simulation in phase 2 (synthetic UNHCR with injected copies; acceptance, refit and
final-application path): `xlpoolh+twinh+cal` accepted (E lower bound +.0294; exponents E041 .21
/ r .43 / q .34), final r, q and twin evidence refitted, PASS 881.3 s, log -.353004 against
E041 -.390206 (+.0372).

E076fs, official phase 2, clean sandboxes: PASS x3, 1,228 s (UNICEF 207.2 / WB 445.3 / UNHCR
575.6 s); no fallback fired; vectors equal E076f on UNHCR and UNICEF (0 changed) and to 5e-8 on
WB (GPU float noise), logs identical to six decimals.
ZIP checker OK for E076f, E076fs and the E041 fallback; self-tests PASS on the E076f build
(E076 x5, E075 x3, E074 x5).

Hosted runtime estimate for E076f (E041-type parts about 1.25x local, CPU tree fitting
1.9-2.7x, TabICL 0.6-1.3x): 1,650-2,050 s for the chains accepted locally; 2,100-2,750 s if
every instrument accepts a chain that refits all its experts and E041 runs as slowly as on the
duplicate simulation. Budget 3600 s.

## Superseded before upload (2026-11-14)

E076f and E076fs were never uploaded and are moved to tmp/e076/superseded/. Readings of
2026-11-14: E076q in r's UNHCR bin (q stays), E076p equal to E041 (E_Z 1.0 stays) — neither
revision rule above fired. But E075ra read below n's bin on WB and UNICEF, and its arm,
registered on 2026-11-13 and kept "unchanged" by the development scorecard, drops r there.
The sentence "No other change" above left that earlier arm out; this note corrects it without
rewriting the registration. Successor package and scorecard: ../2026-11-15-E077/SCORES.md.

## Actual result

None: this package was not uploaded.
