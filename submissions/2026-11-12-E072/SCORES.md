# Day-5 high-risk probes (uploads planned 2026-11-12) — preregistered 2026-11-11

| Upload | Path | Content |
|---|---|---|
| E072w | submissions/2026-11-12-E072w.zip | WB: E041 replaced by the TabICLv2 per-head expert (DIRECT mix100, no guard); UNICEF/UNHCR E041 |
| E072h | submissions/2026-11-12-E072h.zip | UNHCR: best S chain among stackc / conf50 / conf100 applied without the E test (expert n_estimators 4); UNICEF/WB E041 |

Local (synthetic, kit aa03186): both PASS; E072w 329 s (WB +.001679 log); E072h 768 s
(chose conf100, UNHCR +.000293 log). High-risk by design: no internal acceptance test.

Arms versus same-scale E041 (.3499339289 / .2335276584 / .8457264165):
- E072w WB higher (.2486 = old .50 or more): TabICL alone beats E041 on real WB -> raise the
  expert weight in the Final (guard grid up to 1, more expert estimators). Equal: no readable
  difference. Lower: the expert alone is worse; keep only guarded mixing.
- E072h UNHCR higher (.8650 = old .93 or more): forced uncertainty-scaled expert replacement
  helps on real UNHCR -> allow it in the Final guard and consider more estimators. Equal:
  unresolved (boundary noise). Lower: drop forced application; guarded use only.
- Technical: Failed (not counted).

## Actual results

(append below)
