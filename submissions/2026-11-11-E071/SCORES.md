# Day-4 hosted scorecard (uploads planned 2026-11-11) — preregistered 2026-11-10

| Upload | Path | SHA256 (first 16) | Content |
|---|---|---|---|
| E071dev | submissions/2026-11-11-E071dev.zip | see manifest tmp/e071/2026-11-11-E071dev.manifest.json | seed 0; WB/UNICEF guarded (mix, per-head stack with out-of-fold S score, sent, temperature); UNHCR guarded regate+transfer / temperature |
| E071s2 | submissions/2026-11-11-E071s2.zip | see manifest | seeds 0,1 all instruments; WB/UNICEF guards as dev |
| E071w4 | submissions/2026-11-11-E071w4.zip | see manifest | WB seeds 0-3 + WB guard; UNICEF/UNHCR E041 |

Local (synthetic, kit aa03186): all PASS; dev 636 s, s2 663 s, w4 581 s (separate processes).
Guard picks on synthetic: WB mix50 (E lower +.0013); UNICEF rejected; UNHCR not applied.

Arms versus same-scale E041 (.3499339289 / .2335276584 / .8457264165; UNHCR boundary noise):
- Favorable: WB .2486 (old .50) or any higher instrument with unchanged others.
- Unresolved: equal.
- Adverse: lower (lone UNHCR .91 = weak evidence).
- Technical: Failed (not counted; fix and re-upload).
Decision use: the Final keeps internally validated components regardless of DEV ties; a
readable WB gain from s2/w4 would favor more seeds for WB in the Final.

## Actual results

(append below)

### 2026-11-12 user-supplied API fragment (pasted; not a live fetch). Uploaded on UTC day 11-12.

| ID | Filename | Created (UTC) | Status | Grand | UNICEF | WB | UNHCR |
|---|---|---|---|---|---|---|---|
| 1049341 | 2026-11-11-E071dev.zip | 2026-11-12T08:52:59.202376Z | Finished / Dev 29772 | 0.4763960013 | 0.3499339289 | 0.2335276584 | 0.8457264165 |
| 1049342 | 2026-11-11-E071s2.zip | 2026-11-12T08:53:39.717619Z | Finished / Dev 29772 | 0.4763960013 | 0.3499339289 | 0.2335276584 | 0.8457264165 |
| 1049343 | 2026-11-11-E071w4.zip | 2026-11-12T08:54:26.024303Z | Finished / Dev 29772 | 0.4699679353 | 0.3499339289 | 0.2335276584 | 0.8264422186 |

Arms: E071dev **Unresolved** (all equal); E071s2 **Unresolved** (all equal); E071w4 WB
**Unresolved**; its UNHCR runs byte-identical E041 code (SEEDS only for world_bank, no UNHCR
candidates; local raw delta 0) and reads old-scale .91 -> boundary noise again, not an effect.
Pure-E041-code UNHCR readings on the post-10-26 scorer: .92 x3 (E065a25, E065a50, E041
re-upload), .91 x2 (E067ws, E071w4). No UTC-day-11-11 uploads were made (3 slots unused).
