# E076 development scorecard — preregistered 2026-11-13 (before any E076 upload)

Experiment record: ../../docs/experiments/E076-final-composition.md. Source:
../2026-11-15-E076/main.py (E075 source plus E_Z, XSTACK_BY and expert q; tmp/e076_patch.py);
builder scripts/build_e070.py. Main-account uploads only (owner `minjoonyoo`, team "Odyssey").
Last development day: 2026-11-14 09:00 to 21:00 KST (development closes 21:00 KST).

Trio of the day (replaces the E075 trio; E075rp and E075rw were withdrawn before upload):

| Upload | Path | Content per instrument |
|---|---|---|
| E075ra | submissions/2026-11-14-E075ra.zip | every instrument: expert r alone (arms in ../2026-11-14-E075/SCORES.md, unchanged) |
| E076q | submissions/2026-11-14-E076q.zip | every instrument: expert q alone = r plus label-informed donor pairing; no E041 fit, no guard |
| E076p | submissions/2026-11-14-E076p.zip | UNHCR: guard over `rmix100, rlpool, rlpoolh, rlpool+cal, rlpoolh+cal, cal` with E_Z 1.0 (the Final's rule); UNICEF / WB = E041; BUDGET_SECONDS 830 |

Same-scale controls: E041 UNICEF .3499339289 / WB .2335276584 / UNHCR .8457264165 (old .52 /
.49 / .92; E041's UNHCR reads .8264 about two times in five); n alone (E073n) .3364 / .2185 /
.8264.

Arms (single noised/rounded readings, each instrument read separately):
- E076q against E075ra on UNHCR — q at least one bin above r: pairing information is real ->
  q leads the Final's UNHCR pool. Same bin: unresolved (inert or sub-bin) -> both stay guarded
  candidates. q below r: the flags hurt on real data -> q removed from the Final.
  Against E041: UNHCR >= .8650 -> readable gain over the whole E041 stack.
  WB / UNICEF: second reading of the r family (the flags are expected inert there).
- E076p — UNHCR >= .8650: readable gain from the guarded choice under E_Z 1.0. .8457 / .8264:
  unresolved. <= .8071: adverse -> the Final returns to E_Z 1.645.
- Failed status / HSCC code: not counted; lighten and re-upload inside the window.
No numeric expectation is stated: no real-data evidence exists for the pairing flags, and the
1.0 rule only changes which sub-bin chains pass.

## Identities and local validation (2026-11-13, kit aa03186 scorer, model venv, RTX 3070)

- E076q 103072639 bytes, SHA256 8dc963330fd6aa129e35029263a0095426cabf5f58d067c845907135525496b8
- E076p 103072641 bytes, SHA256 8217c109357456271ed30393d654766ff9d9049e3fa60f107c0abb0b3aebcb52
  (BUDGET_SECONDS 800; a first build with 830, SHA256 18637b8d..., was never uploaded: its
  worst case — guard decision just under the 705 s check plus the slowest tree refit — touched
  900 s)
(e041_core.py = E041 22c91180... in each; ZIPs kept out of git via .git/info/exclude.)

ZIP checker OK x2; self-tests PASS (E076 x5, E075 x3, E074 x5). Official phase 1 on the clean
synthetic sandboxes, all vectors valid:
- E076q: PASS x3, UNHCR 77.2 s / WB 45.0 s / UNICEF 45.3 s (168 s). Logs -.568377 / -1.160993 /
  -.823618 against r alone -.568172 / -1.161453 / -.824008: the sandbox has no paired records,
  the pairing fields stay inert. Duplicate simulation (copies with identical GIVEN, nothing
  for pairing to resolve): -.356267 against r -.355996, 74.7 s. Fabricated pair world with
  impostors (self-tests): q -.998 against r -1.096 log per cell; with a weak pairing signal
  (12 answers) -.974 against -1.085.
- E076p: PASS x3, UNHCR 423.2 s / WB 62.8 s / UNICEF 27.1 s (513 s). Under E_Z 1.0 the clean
  UNHCR guard accepted `rlpool` (out-of-fold S +.00012, E lower bound +7.8e-7), refitted on
  2,000 rows, refitted r on all visible rows (66.7 s): log -.551628 against E041 -.551737
  (+.000110); WB and UNICEF vectors equal E041 (0 changed). Duplicate simulation (run with the
  830 build, vectors of the two builds identical on the clean table): `rlpool+cal` accepted
  (E lower bound +.0235), -.354438 against E041 -.388611, 550.5 s.

Hosted runtime estimates (E041-type parts about 1.25x local, CPU tree fitting 1.9-2.7x):
E076q 320-460 s; E076p 725-820 s when a chain is accepted (the 800 s budget skips the final
tree refit after 680 s and returns E041, worst case about 875 s).

## Actual results

(append below; keep the arms above unchanged)

### 2026-11-14 user-supplied API fragment (pasted; not a live fetch)

| ID | Filename | Created (UTC) | Status | Owner / team (fact sheet) | Grand | UNICEF | WB | UNHCR |
|---|---|---|---|---|---|---|---|---|
| 1051842 | 2026-11-14-E076q.zip | 2026-11-14T03:38:38.267278Z | Finished / Dev 29772 | minjoonyoo / "Odyssey" | 0.4459103704 | 0.3228478426 | 0.1884410501 | 0.8264422186 |
| 1051845 | 2026-11-14-E076p.zip | 2026-11-14T03:39:49.059847Z | Finished / Dev 29772 | minjoonyoo / "Odyssey" | 0.4763960013 | 0.3499339289 | 0.2335276584 | 0.8457264165 |

E076q, old-scale bins UNICEF .50 / WB .46 / UNHCR .91; E075ra of the same day (ID 1051843) read
.49 / .46 / .91. Arms:
- UNHCR, q against r: same bin -> **unresolved** (pairing fields inert or sub-bin); both stay
  guarded candidates. The "q below r" arm did not fire. Against E041: below .8650, no readable
  gain over the stack.
- WB / UNICEF: second reading of the r family — WB the same bin as r, UNICEF one bin above r;
  both readings two to three bins below E041 and below n alone (.48 / .51).
E076p equals E041 on all four values. Arm: **Unresolved** — a chain was rejected internally or
accepted with a sub-bin effect; the adverse arm (UNHCR <= .8071) did not fire, **E_Z 1.0 stays**.
Side note, not evidence: the four guarded packages of 11-13 / 11-14 read UNHCR old-scale .92 four
times out of four; pure E041 reads .92 about three times in five (chance of four such readings
without any change about .13).
Development phase closed with these readings: 24 sprint uploads, no readable gain over E041.
Uploaded archives (E075ra, E076q, E076p) moved to tmp/uploaded/ after these readings.
