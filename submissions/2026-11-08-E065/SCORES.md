# E065 hosted scorecard — preregistered before upload (2026-11-08)

Packages (heavy ZIPs kept under tmp/ to stay out of git):

| Upload | Path | Bytes | SHA256 |
|---|---|---:|---|
| E065a25 (fixed alpha .25, strict) | tmp/e065/2026-11-08-E065a25.zip | 103058012 | 1694bbad61606b3d6beaf7954c3c6ad4370701cce9b428d71f12cf71def9548d |
| E065a50 (fixed alpha .5, strict) | tmp/e065/2026-11-08-E065a50.zip | 103058013 | d86947bf5d7c0ecf416d9dbca235fd545468836e4da080e30bf5b82edcc05ef6 |
| E065guard (A045 guarded, strict) | tmp/e065/2026-11-08-E065guard.zip | 103058011 | e842759e783dcf7c9bb2ac0c4856225df6a199d9a1e64115cd0bf66a5638d925 |
| E041 same-scale control | submissions/2026-09-19-E041.zip (original upload bytes) | 13557 | 1502ebad20e85ae57db617fa6d202b9e199594c1c043acd6d0d1d52102362a50 |

Why a control: the platform scorer changed on 2026-10-26 (crowd-marginal reference, kit
aa03186). E041's 09-19 values (.6433/.52/.49/.92) may be on the old scale. Compare E065
only with a same-scale E041 reading: either a fresh E041 upload or E041's current API
values if the user confirms they were rescored. UNICEF/UNHCR in all E065 builds call
byte-identical E041 code, so they also report E041's current-scale control values.

Day-1 plan (2026-11-08, registered before upload; user confirmed E041's listed values were
not rescored): upload E065a25, E065a50 and E066. E066 changes UNHCR only, so its WB value
is the same-scale E041 WB control; the E065 uploads' UNHCR values are E041's UNHCR control
for E066. A separate E041 re-upload is not needed. Guard ZIP held for a later slot.

Reading arms (per variant, versus the same-scale E041 control):
- Favorable: WB higher, UNICEF and UNHCR equal to control. Noisy positive evidence for
  this fixed alpha on real WB data; not an exact gain or TEST selection.
- Unresolved: WB equal. Effect below public resolution or absent; no zero-effect claim.
- Adverse: WB lower with equal controls.
- Mixed: UNICEF or UNHCR differ from control (unexpected; identical code): record, no
  WB attribution, check rounding-boundary noise before any conclusion.
- Technical: Failed status / HSCC code. Failed uploads do not count toward limits;
  fix and retry within the day.
Decision use: the best favorable alpha (or guard if it beats fixed variants) becomes the
Final candidate only after a phase-2 local PASS of the exact package with the current kit.

## Actual results

(append below; keep the arms above unchanged)

### 2026-11-08 user-supplied API fragment (pasted in this conversation; not a live fetch)

| ID | Filename | Created (UTC) | Status / phase | Grand | UNICEF | WB | UNHCR |
|---|---|---|---|---|---|---|---|
| 1041540 | 2026-11-08-E065a25.zip | 2026-11-08T05:04:40.742718Z | Finished / Development 29772 | 0.4763960013 | 0.3499339289 | 0.2335276584 | 0.8457264165 |
| 1041542 | 2026-11-08-E065a50.zip | 2026-11-08T05:05:12.316631Z | Finished / Development 29772 | 0.4763960013 | 0.3499339289 | 0.2335276584 | 0.8457264165 |

Scoring program e9f1131f-383a-43f4-89a0-6440004c5668 (E064 used f3015fb3-...): values are on
the post-10-26 crowd-marginal scale. a25 and a50 are identical on all four strings.
UNICEF/UNHCR are E041 code, so pairing with E041's old .52/.92 gives conversion factors
U/R = 1.354304 (UNICEF) and 1.928420 (UNHCR) — consistent with the README conversion
`1 + (released - 1) * U / R`. WB reading waits for the same-scale control (E066's WB,
E041 code). Arm not yet assigned.

| 1041566 | 2026-11-08-E066.zip (WB control) | 2026-11-08T05:24:07.995216Z | Finished / Development 29772 | 0.4763960013 | 0.3499339289 | 0.2335276584 | 0.8457264165 |

**Arm assigned 2026-11-08: Unresolved for E065a25 and E065a50.** The same-scale E041-code
WB value (E066) equals both E065 WB strings, with UNICEF/UNHCR equal: no readable WB change
at either alpha. Not a zero-effect claim. WB conversion factor U/R = 1.502887 follows from
E041's old .49. Guard ZIP not uploaded.
