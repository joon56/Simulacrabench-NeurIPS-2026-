# Day-2 hosted scorecard (uploads planned 2026-11-09) — preregistered 2026-11-08

| Upload | Path | Bytes | SHA256 | Changes |
|---|---|---:|---|---|
| E068 | submissions/2026-11-09-E068.zip | 16877 | 97a22a86e43ebcd3cf4e02852b140c97d3004e81e9cb2fc9a8b664ffd74cdf6d | UNHCR re-gating (+E066 transfer) |
| E067h50c | submissions/2026-11-09-E067h50c.zip | 103059004 | 5399ab8783f84ad53ebf6a7db082cc39c4c8cae117bff2e2ebe481c1282f8d79 | UNHCR TabICLv2 expert, alpha .5 scaled by E041 uncertainty |
| E067ws (E069) | submissions/2026-11-09-E067ws.zip | 103060875 | 1201bd48c415c34c20f4637947f9ea97d52be5bf302a87243788fc01898b25e5 | WB sentinel from direct classifier where the gate is approximate |
| reserve: E067r1 | tmp/e067/2026-11-09-E067r1.zip | ~103 MB | 282c83225738e111a1a6b606acc0eef8df8753cc62d8a50ba26436e9d9c58da5 | 2-seed E041 mean (all), WB guarded expert, E066 transfer |

Controls (same post-10-26 scale): day-1 E041-code values UNICEF .3499339289, WB
.2335276584, UNHCR .8457264165. E068 and E067h50c leave UNICEF/WB on E041 code;
E067ws (E069) leaves UNICEF/UNHCR on E041 code. Slot 3 changed from r1 to E069 on
2026-11-08 after the World Bank gate analysis (before any upload); r1 kept as reserve.

Arms (each changed instrument versus its control; unchanged instruments must match):
- Favorable: higher. E068: re-gating helps; E067h50c: expert helps on uncertain cells;
  E067r1: seed mean and/or guarded WB expert readable.
- Unresolved: equal (no zero-effect claim).
- Adverse: lower; drop that change from the Final unless it is internally guarded.
- Mixed: an unchanged instrument differs (check rounding-boundary noise first).
- Technical: Failed status / HSCC code; fix and retry the same day (failures not counted).
If used, E067r1 is primarily the hosted rehearsal of the Final code paths (seed loop, guard,
transfer); a tie is the expected reading.

## Actual results

(append below; keep the arms above unchanged)

2026-11-09: user reports E068 uploaded (ID/time not yet supplied). The two TabICL ZIPs were
moved from tmp/e067/ to submissions/ unchanged (sizes and SHA256 re-checked); they are
listed in the local .git/info/exclude to stay out of commits (>100 MB GitHub limit).

### 2026-11-09 user-supplied API fragment (pasted; not a live fetch)

| ID | Filename | Created (UTC) | Status | Grand | UNICEF | WB | UNHCR |
|---|---|---|---|---|---|---|---|
| 1044276 | 2026-11-09-E068.zip | 2026-11-09T11:46:16.213152Z | Finished / Dev 29772 | 0.4699679353 | 0.3499339289 | 0.2335276584 | 0.8264422186 |
| 1044286 | 2026-11-09-E067h50c.zip | 2026-11-09T11:49:50.332517Z | Finished / Dev 29772 | 0.4763960013 | 0.3499339289 | 0.2335276584 | 0.8457264165 |
| 1044290 | 2026-11-09-E067ws.zip | 2026-11-09T11:50:37.519531Z | Finished / Dev 29772 | 0.4699679353 | 0.3499339289 | 0.2335276584 | 0.8264422186 |

UNHCR .8264422186 = old-scale .91 (1 - .09 * 1.928420); .8457264165 = old .92.
Arms as registered: E068 **Adverse** (UNHCR one bin below the day-1 control); E067h50c
**Unresolved** (equal to the day-1 control); E067ws WB **Unresolved**, but its UNHCR, which
runs byte-identical E041 code (build constants checked inside the uploaded ZIP), also reads
.91 -> **Mixed**: the registered first check is rounding-boundary noise. Across ~16 hosted
readings of E041-code or near-E041 UNHCR, 13 read .92 and 3 read .91 (E061, E068, ws);
with the DEV Laplace scale (~.00088 old-scale for 621 held-out respondents) this is
consistent with E041's old-scale UNHCR sitting just above .915 (~.916, estimate).
Single UNHCR readings therefore cannot separate small effects; the E068 adverse reading is
weak evidence. Next: same-scale E041 re-upload and an E067h50c replicate on 11-10.
