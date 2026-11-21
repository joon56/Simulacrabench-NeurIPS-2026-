# Day-3 hosted scorecard (uploads planned 2026-11-10) — preregistered 2026-11-09

| Upload | Path | Bytes | SHA256 | Purpose |
|---|---|---:|---|---|
| E041 control | submissions/2026-09-19-E041.zip (original 09-19 bytes) | 13557 | 1502ebad20e85ae57db617fa6d202b9e199594c1c043acd6d0d1d52102362a50 | same-day E041 baseline |
| E067h50c replicate | submissions/2026-11-09-E067h50c.zip (unchanged) | 103059004 | 5399ab8783f84ad53ebf6a7db082cc39c4c8cae117bff2e2ebe481c1282f8d79 | UNHCR expert, second reading |
| E070dev1 | submissions/2026-11-10-E070dev1.zip | 103060948 | 06a361c05a98d33ee779d193e00f092f1abdbf07f0cc06839f60364184d90b31 | hosted rehearsal of internal guards |

Arms:
- E041 control UNHCR .8457 (old .92): day-2 E067ws .91 was rounding-boundary noise. UNHCR
  .8264 (old .91): E041-code UNHCR now reads .91 again (persistent shift or boundary drift);
  then same-day comparisons use this control. UNICEF/WB expected .3499 / .2335.
- E067h50c replicate versus the same-day control: control .91 and h50c .92 -> second .92
  reading while E041 reads .91, favorable evidence (still noisy). Both .92 -> tie. h50c .91 ->
  no evidence of benefit.
- E070dev1: Technical first (Finished within 900 s). WB/UNICEF/UNHCR versus the same-day
  control: higher = the internal guard accepted a helpful chain on real data; equal = no
  readable change; lower = adverse (UNHCR .91 alone weak). Internal choices are not observable.

## Actual results

(append below; keep the arms above unchanged)

### 2026-11-10 user-supplied API fragment (pasted; not a live fetch)

| ID | Filename | Created (UTC) | Status | Grand | UNICEF | WB | UNHCR |
|---|---|---|---|---|---|---|---|
| 1046001 | 2026-09-19-E041.zip | 2026-11-10T12:10:50.975624Z | Finished / Dev 29772 | 0.4763960013 | 0.3499339289 | 0.2335276584 | 0.8457264165 |
| 1046003 | 2026-11-10-E070dev1.zip | 2026-11-10T12:11:24.263850Z | Finished / Dev 29772 | 0.4763960013 | 0.3499339289 | 0.2335276584 | 0.8457264165 |
| 1046004 | 2026-11-09-E067h50c.zip | 2026-11-10T12:11:59.754009Z | Finished / Dev 29772 | 0.4763960013 | 0.3499339289 | 0.2335276584 | 0.8457264165 |

Arms: E041 control UNHCR old .92 -> the day-2 E067ws .91 reading was rounding-boundary noise
(consistent with E041 UNHCR just above .915). E067h50c replicate equals the control: **tie**
(second .92 reading; no readable expert benefit). E070dev1: **Technical PASS on the platform**
(Finished) and **Unresolved** on all three instruments; internal guard choices unobservable.
