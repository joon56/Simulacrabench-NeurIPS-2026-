# 2026-09-03-E013 — cross-round respondent linkage over E012

Experiment: E013 (adopted; parent E012; organizer ruling 2026-09-02
permits within-dataset row matching — email quoted in log.md). Code:
script-assembled merge of hier_backoff + logit_blend helpers +
cond_agree + shared_trunk + cross_link. Fuzzy 1:1 cross-round matching
on the GIVEN signature; per-item shrunk answer-stability mixes the
visible twin's answer into the E012 belief; MIN_PAIRS=30 guard. No
bundled artifacts, no requirements.txt. Zip:
`submissions/2026-09-03-E013.zip`, check_submission_zip OK.

## Local scores (2026-09-02, seed 0, phase 1)

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact (runner) | 0.4429 | 0.5006 | 0.4549 | 0.5629 | 0.5061 |
| E012 (LB 0.60) | 0.4429 | 0.5006 | 0.4549 | 0.5629 | 0.5061 |

**Identical to E012 by design** — sandbox rows are independent, the
matcher finds ~1 spurious collision, guards keep the layer off.
Adoption evidence is the panel-sim pair (E013 file): +0.2293 log
(exact-copy twins) and +0.2003 log (twins with GIVEN drift — fuzzy
recall). Official score.py PASS ×3: 0.5000 / 0.4600 / 0.5600 (noised sandbox,
consistent with exact ≡ E012). Tests: 47 passed + 1 xfail.

## Leaderboard expectation (real data)

Reference: E012 LB = 0.60 (unicef 0.52 / wb 0.49 / unhcr 0.78).
Pre-registered 2026-09-02 BEFORE submission:

- **unicef and world_bank MUST stay flat** (no round column → layer
  structurally inert there). Any move > noise ⇒ bug, diagnose
  immediately.
- **unhcr is the entire experiment**: if the panel hypothesis is right
  (match fraction 0.6–0.8, within-window stability high), expected
  unhcr 0.85–0.92 ⇒ Grand ≈ 0.62–0.65. This would be the largest
  single-submission jump of our campaign and would confirm the
  leaders-at-0.92 mechanism.
- Partial outcomes are informative, pre-registered readings:
  unhcr 0.80–0.84 ⇒ matching works but recall low (real drift exceeds
  MAX_MISMATCH=2 → E014: widen fuzziness with stronger uniqueness
  guards). unhcr flat (±0.01) ⇒ either rounds share few respondents
  (panel hypothesis wrong — then 0.92 leaders use something else,
  re-open analysis) or signature columns drift too much for matching.
  unhcr DOWN ⇒ false matches injected noise ⇒ raise MIN_MARGIN /
  restrict to exact matching.
- Wall-clock: linkage adds seconds; total ≈ E012 (~220 s local) ≪ 900 s.
- Kit watch: organizer announced "<5 gating changes" to unhcr still
  unshipped — if a kit update lands before this submission, re-run the
  full harness first.
