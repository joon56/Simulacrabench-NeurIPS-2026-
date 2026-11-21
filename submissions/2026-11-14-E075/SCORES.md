# E075 hosted scorecard — preregistered 2026-11-13 (before any E075 upload)

Experiment record: ../../docs/experiments/E075-retrieval-trees.md. Source: main.py in this
folder (E074 source plus expert r, tmp/e075_patch.py); builder scripts/build_e070.py.
Main-account uploads only (owner `minjoonyoo`, team "Odyssey"). These are the last three
development uploads (window 2026-11-14 09:00 to 21:00 KST; development closes 21:00 KST).
Development scores do not count for the Final ranking, so expert-alone probes are admissible.

| Upload | Path | Content per instrument |
|---|---|---|
| E075ra | submissions/2026-11-14-E075ra.zip | every instrument: expert r alone (neighbour trees fed by E041's supervised retrieval); no E041 fit, no guard |
| E075rp | submissions/2026-11-14-E075rp.zip | UNHCR: guard over `rmix100, rlpool, rlpoolh, rlpool+cal, rlpoolh+cal, cal`; UNICEF / WB = E041; BUDGET_SECONDS 830 |
| E075rw | submissions/2026-11-14-E075rw.zip | WB and UNICEF: the same guard; UNHCR = E041; BUDGET_SECONDS 880 |

Same-scale controls: E041 UNICEF .3499339289 / WB .2335276584 / UNHCR .8457264165 (old .52 /
.49 / .92; E041's UNHCR reads .8264 about two times in five); n alone (E073n) .3364 / .2185 /
.8264 (old .51 / .48 / .91).

Arms (single noised/rounded readings, each instrument read separately):
- E075ra, per instrument — above E041's bin (UNHCR >= .8650, WB >= .2486, UNICEF >= .3635):
  r alone beats the whole E041 stack there -> r primary in the Final on that instrument
  (pooled with E041 behind the guard). Equal to E041's bin: the supervised retrieval lifts the
  trees by about one bin over n -> guarded pool in the Final. Equal to n's bin: nothing
  readable from the retrieval features -> r only as one more guarded candidate. Below n's
  bin: the extra features hurt -> r dropped.
- E075rp — UNHCR >= .8650: readable gain from the guarded choice among r alone, pools and
  calibration -> the Final uses it on UNHCR. .8457 / .8264: unresolved. <= .8071: adverse
  (accepted internally, worse on the all-visible run) -> dropped.
- E075rw — WB >= .2486 or UNICEF >= .3635: readable gain there -> the Final uses it on that
  instrument. Equal: unresolved. WB <= .2185 or UNICEF <= .3364: adverse -> dropped there.
- Failed status / HSCC code: not counted; lighten and re-upload inside the window.
No numeric expectation is stated: the two real-data effects being combined (supervised
retrieval, tree consumer) were measured separately, never together.

Identities and local validation: appended below once each package has passed.

## Identities and local validation (2026-11-13, kit aa03186 scorer, model venv, RTX 3070)

- E075ra 103071537 bytes, SHA256 5cf41bcb661d5599e843d2ed2b837f1410fdebe8884bc44704f248e26fe41d03
- E075rp 103071569 bytes, SHA256 b8ba24e3df1e8c3fad8d5aac9a94542238da6b75bd69f8442096b474d6f1ea34
- E075rw 103071572 bytes, SHA256 f2e6ab0c4c5df15816798b6b38bd4822c6ba6c6e8e427b56c15208a1ba10ac97
(e041_core.py = E041 22c91180... in each; ZIPs kept out of git via .git/info/exclude.)

ZIP checker OK x3; self-tests PASS (E075 x3, E074 x5 on the E075 build). Official phase 1 on the
clean synthetic sandboxes, all vectors valid:
- E075ra: PASS x3, UNHCR 70.0 s / WB 48.4 s / UNICEF 37.4 s (156 s). Synthetic UNHCR log -.568172
  against E041 -.551737 (n alone -.567220): on the sandbox every tree expert is below the
  network, as before.
- E075rp: PASS x3, UNHCR 419.9 s (E041 181 s, shadow E041 164 s, shadow r 54 s) / WB 72.7 s /
  UNICEF 32.8 s (525 s). Out-of-fold S: rlpool +.00012, r alone -.019; E lower bound -.00007 ->
  rejected; all three instruments equal E041 (0 changed).
- E075rw: PASS x3, UNICEF 86.7 s / WB 156.0 s / UNHCR 198.2 s (441 s); both guards rejected
  (WB E lower bound -.0005); all three instruments equal E041 (0 changed).
Two-fidelity duplicate simulation (synthetic; mechanism and acceptance path only): r alone
-.355996 against E041 -.388611 (+.0459 old-scale skill, 80.5 s); E075rp accepted `rlpool+cal`
(exponents E041 .27 / r .69; E lower bound +.0224), refitted r on all visible rows (57 s) and
scored -.354438 (+.0481), 562 s.

Hosted runtime estimates (E041-type parts about 1.25x local, CPU tree fitting 1.9-2.7x):
E075ra about 300 s; E075rp 710-780 s when a chain using r is accepted (the 830 s budget skips
the final expert fit after 705 s and then returns E041); E075rw 660-800 s.

## Change of the upload trio before any upload (2026-11-13, late)

E075rp and E075rw were withdrawn before upload and moved to tmp/e075/reserve/ (never
uploaded; their arms above stay as registered and unread). The trio of 2026-11-14 is E075ra
(unchanged), E076q and E076p — registration and arms in ../2026-11-14-E076/SCORES.md and
../../docs/experiments/E076-final-composition.md. Reason: E076p carries the same UNHCR chains
under the Final's E-row rule (E_Z 1.0), and E076q spends the third slot on an untested
structural hypothesis (label-informed donor pairing) instead of a second guard rehearsal.

## Actual results

(append below; keep the arms above unchanged)

### 2026-11-14 user-supplied API fragment (pasted; not a live fetch)

| ID | Filename | Created (UTC) | Status | Owner / team (fact sheet) | Grand | UNICEF | WB | UNHCR |
|---|---|---|---|---|---|---|---|---|
| 1051843 | 2026-11-14-E075ra.zip | 2026-11-14T03:39:11.408070Z | Finished / Dev 29772 | minjoonyoo / "Odyssey" | 0.4413960227 | 0.3093047995 | 0.1884410501 | 0.8264422186 |

Old-scale bins: UNICEF .49 / WB .46 / UNHCR .91 (E041 .52 / .49 / .92; n alone .51 / .48 / .91).
Arms, per instrument:
- UNICEF: below n's bin (two bins) -> **the extra features hurt; r dropped on UNICEF**.
- WB: below n's bin (two bins) -> **the extra features hurt; r dropped on WB**.
- UNHCR: equal to n's bin (.8264, which is also E041's own boundary reading) -> **nothing
  readable from the retrieval features; r stays only as one more guarded candidate**.
r alone does not beat the E041 stack anywhere. On the two instruments without donor structure
the 2K + 6 retrieval features per head cost two to three bins against plain neighbour trees.
E075rp / E075rw were never uploaded (arms unread).
