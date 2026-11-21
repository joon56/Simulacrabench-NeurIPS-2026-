# E077 Final scorecard — registered 2026-11-14 (before the Final phase opens)

Experiment record: ../../docs/experiments/E077-final-structural-exclusions.md. Source: main.py
in this folder, a byte copy of ../2026-11-15-E076/main.py (the `det` attempt was removed and
is kept apart in det-attempt/); builder scripts/build_e070.py. Final phase: 2026-11-15 21:00 KST
to 2026-11-20 21:00 KST, one successful upload, failed attempts may be retried, exact
scoring, 3600 s. Main account only (owner `minjoonyoo`, team "Odyssey"). The upload and the
final choice are the user's. Supersedes E076f (never uploaded).

| Package | Path | Role |
|---|---|---|
| E077f | submissions/2026-11-15-E077f.zip | **first upload**: strict, no time fallback |
| E077fs | submissions/2026-11-15-E077fs.zip | second attempt only if E077f returns Failed: same composition, non-strict (any guard error keeps the seed-mean E041 output of that instrument), BUDGET_SECONDS 3300 |
| E041 | submissions/2026-09-25-E041.zip | last resort if both fail (hosted-proven model, phase-2 PASS locally) |

Composition of E077f / E077fs (E_Z 1.0; S1000 / E1000 guard; at most two chains E-tested):
- UNHCR (as in E076f): E041 seed 0; experts r, q; chains `xlpool, xlpoolh, xlpool+cal,
  xlpoolh+cal, qlpool, qlpoolh, qlpoolh+cal, rlpool, rlpoolh, rlpoolh+cal, xlpoolh+twinh,
  xlpoolh+twinh+cal, twinh, twinh+cal, cal`.
- WB, UNICEF: E041 mean of seeds 0, 1, 2; experts g, TabICL (r removed by the E075ra arm);
  chains `xlpool, xlpoolh, xlpool+cal, xlpoolh+cal, lpool, lpoolh, glpool, cal`.
The package differs from E076f in two build constants only (CANDIDATES, XSTACK_BY).

No development reading remains that could revise this package. A rebuild happens only after
a Failed status (lighter or repaired package, fresh phase-2 local PASS, new identity here).

Reading of a Failed status: a failed attempt does not use the single success. Report the
HSCC code; timeout-type codes call for E077fs or a trimmed rebuild, exception-type codes for
E077fs. A Finished status ends the competition entry: nothing is uploaded after it.

## Identities and local validation (2026-11-14, kit aa03186 scorer, model venv, RTX 3070)

- E077f 103072696 bytes, SHA256 7ebb1972e327adc57947a977baa188036ee28c6fd30bb860a357ed2a6cd62ac8
- E077fs 103072696 bytes, SHA256 020454e0a9044832ebf5784b1dbbfeac91f3dcbc66c9756a4fbfd28caf537fb6
  (main.py differs from E077f only in STRICT = False and BUDGET_SECONDS = 3300)
- E041 fallback submissions/2026-09-25-E041.zip, SHA256 bd5d2b7d... (main.py 22c91180...).
(e041_core.py = E041 22c91180... in each; ZIPs kept out of git via .git/info/exclude.)

E077f, official **phase 2** (TRAIN+DEV visible, TEST scored) on the clean synthetic sandboxes,
all vectors valid, against E041 in the same phase:
- UNHCR PASS 556.0 s: E041 159 s, shadow E041 151 s, shadow r 53 s, shadow q 61 s, twin 2 s;
  `qlpool` accepted (out-of-fold S +.00018, E lower bound +.00016), final q 83 s; log -.548672
  against -.548949 (+.000277); vectors bit-identical to E076f (0 of 308,637 changed).
- WB PASS 392.2 s: three seeds 160 s, shadow E041 41 s, g 14 s, TabICL 69 s; `lpool` accepted
  (S +.00282, E lower bound +.00202; exponents E041 .43 / TabICL .52), final TabICL 93 s; log
  -1.084394 against -1.085917 (+.001523).
- UNICEF PASS 168.6 s: three seeds 61 s; `lpool` accepted (E lower bound +.00059); log -.795355
  against -.796320 (+.000965).
Sum 1,117 s locally. Old-scale skill deltas +.0002 / +.0008 / +.0006 (synthetic; engineering
evidence that the whole path runs and does not lose, not a forecast for real data).
Duplicate simulation in phase 2 (synthetic UNHCR with injected copies; acceptance, refit and
final-application path): `xlpoolh+twinh+cal` accepted (E lower bound +.0294), final r, q and
twin evidence refitted, PASS 907.8 s, log -.353004 against E041 -.390206 (+.0372).

E077fs, official phase 2, clean sandboxes: PASS x3, 1,163 s (UNICEF 175.9 / WB 419.5 / UNHCR
567.3 s); no fallback fired; vectors equal E077f on UNHCR and UNICEF (0 changed) and to 5e-8 on
WB (GPU float noise), logs identical to six decimals.
ZIP checker OK for E077f, E077fs and the E041 fallback; self-tests PASS x13 on the E077f build
(E076 x5, E075 x3, E074 x5).

Hosted runtime estimate for E077f (E041-type parts about 1.25x local, CPU tree fitting
1.9-2.7x, TabICL 0.6-1.3x): 1,450-1,800 s for the chains accepted locally; up to about 2,350 s
if every instrument accepts a chain that refits all its experts and E041 runs as slowly as on
the duplicate simulation. Budget 3600 s.

## Actual result

### 2026-11-15 user-supplied API fragment (pasted; not a live fetch)

| ID | Filename | Created (UTC) | Status | Owner / team (fact sheet) | Grand | UNICEF | WB | UNHCR |
|---|---|---|---|---|---|---|---|---|
| 1053618 | 2026-11-15-E077f.zip | 2026-11-15T13:12:29.037830Z | Finished / Test 29773, on_leaderboard true (19827) | minjoonyoo / "Odyssey" | 0.4790691441 | 0.3427149262 | 0.2344919185 | 0.8600005877 |

This is the team's single successful Final upload: exact, unnoised TEST skill on the
marginal-reference scale (Grand = mean of the three, checked). The entry is closed; E077fs and
the E041 fallback were not uploaded and nothing may be uploaded after this.

What the number does and does not say:
- It cannot be split into components. E041 alone on TEST is unobservable, and which chains the
  in-run guard accepted is unobservable (no stdout on the platform; by project rule nothing is
  encoded into outputs).
- It is not comparable cell by cell with the development values (.3499 / .2335 / .8457):
  different respondents, 7.5-10 % more visible rows (the DEV rows return as donors), exact
  instead of noised and rounded scoring, and a phase-specific marginal reference. UNHCR is
  higher by .0143 and WB by .0010, UNICEF lower by .0072; no cause is claimed for any of them.
- Rank: not known from this fragment; read from the Test leaderboard when it is shown.
  **Final rank 47**, read by the user from the Test leaderboard and reported on 2026-11-21
  (not fetched by the assistant).

