# E074 hosted scorecard — preregistered 2026-11-13 (before any E074 upload)

Experiment record: ../../docs/experiments/E074-twin-copy-share.md. Source: main.py in this
folder (E073 source plus the `twin` / `twinh` chain parts, tmp/e074_patch.py); builder
scripts/build_e070.py. Main-account upload only (owner `minjoonyoo`, team "Odyssey").

| Upload | Path | Content per instrument |
|---|---|---|
| E074t | submissions/2026-11-13-E074t.zip | UNHCR / WB: guard over `twin, twinh, twin+cal, twinh+cal, cal, tpoolh` (honest copy share from the best-matching labelled rows; no tree expert); UNICEF = E041 |

Identity (second build, after the two-start repair of the fit): 103070541 bytes, SHA256
05370e6ed3d0e40f3d42a59330981334542fc425480c01cef12b1139fac8ba57 (rendered main.py inside the
ZIP SHA256 1061c636...; e041_core.py = E041 22c91180...; ZIP kept out of git via
.git/info/exclude). The first build (SHA256 73f74e21..., single cautious start) was never
uploaded and is superseded.

Local (kit aa03186 scorer, model venv, RTX 3070): ZIP checker OK; official phase 1 PASS on all
three clean synthetic instruments, vectors valid; wall UNHCR 311.1 s, WB 104.9 s, UNICEF 27.0 s
(443 s; no CPU tree fitting, twin search about 2 s). On the clean tables every twin fit
collapsed to a share of about .001 and every chain was rejected: UNHCR 132,273 vectors equal
E041 (0 changed). Self-tests PASS x5 on fabricated duplicate clusters. Duplicate-injection
simulations (synthetic, mechanism only): copies of one fidelity (run with the first build) ->
nothing accepted, output = E041; copies of two fidelities (this build) -> twinh+cal accepted (E lower bound +.0042), official log
-.388611 -> -.381541 (+.0100 old-scale skill), 443 s; the acceptance, refit and
final-application path ran end to end.
Hosted runtime estimate: same parts as E073c (two E041 fits per guarded instrument), below
the 900 s budget by the E073s precedent (571 s local finished).

Same-scale E041 controls: UNICEF .3499339289 (old .52), WB .2335276584 (old .49), UNHCR
.8457264165 (old .92; E041 itself reads .8264422186 about two times in five).

Arms (single noised/rounded readings, each instrument read separately):
- UNHCR >= .8650 or WB >= .2486: readable gain from the honest copy share -> first candidate
  of the Final.
- Equal bins (UNHCR .8457, or .8264 = E041's boundary reading): unresolved — rejected
  internally or accepted with a sub-bin gain; stays in the Final behind its guard.
- UNHCR <= .8071 or WB <= .2185: adverse (accepted internally, worse on the all-visible run)
  -> dropped from the Final.
- Failed status / HSCC code: not counted; fix and re-upload.
No numeric expectation is stated: related hosted attempts (E019, E047) read as ties, and no
real-data evidence exists for this estimator.
Upload window valid under either daily-reset convention: 2026-11-13 09:00 to 21:00 KST.

## Actual results

(append below; keep the arms above unchanged)

### 2026-11-13 user-supplied API fragment (pasted; not a live fetch)

| ID | Filename | Created (UTC) | Status | Owner / team (fact sheet) | Grand | UNICEF | WB | UNHCR |
|---|---|---|---|---|---|---|---|---|
| 1050759 | 2026-11-13-E074t.zip | 2026-11-13T09:13:43.162468Z | Finished / Dev 29772 | minjoonyoo / "Odyssey" | 0.4763960013 | 0.3499339289 | 0.2335276584 | 0.8457264165 |

Equal to E041 on all four values. Arm: **Unresolved** — the twin chains were rejected
internally or accepted with a sub-bin gain. With E073c and E073xm of the same day, UNHCR read
old-scale .92 three times out of three (pure E041 reads .92 about three times in five; the
chance of three such readings without any change is about .2, so this is not evidence of a
gain).
