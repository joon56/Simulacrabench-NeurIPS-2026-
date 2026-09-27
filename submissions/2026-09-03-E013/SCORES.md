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

## Actual leaderboard result (2026-09-03)

**Grand 0.60 — unicef 0.52 / world_bank 0.49 / unhcr 0.78** — identical
to E012 (leaderboard keeps E012's entry as best). Pre-registered
readings:

- unicef/wb flat ✓ — the layer is structurally inert there; no damage
  anywhere (the safety design worked: wrong hypothesis cost zero skill).
- **unhcr FLAT ⇒ the pre-registered flat arm fired.** Ambiguous between
  its two sub-readings, and the MIN_PAIRS guard makes them
  indistinguishable from outside: (a) the two rounds share few/no
  respondents (competition build deliberately disjoint — then the
  0.92 leaders use something else and that analysis re-opens), or
  (b) real cross-round GIVEN drift exceeds MAX_MISMATCH=2 (a child
  crossing an age band moves 2 roster columns at once; a different
  household member answering moves more), so the matcher never found
  the ≥30 visible-visible pairs needed to arm.
- Follow-ups decided: (1) zero-cost diagnostic — ask the organizer
  directly whether rounds share respondents (channel already warm);
  (2) E014 = looser two-stage probabilistic matching with runtime
  column-stability weighting, inert-by-guard as before — resolves the
  (a)/(b) ambiguity by construction: if E014 is also flat, overlap is
  dead and linkage is abandoned.

## API score reconciliation - 2026-09-27

Source: user-supplied My Submissions JSON, recorded 2026-09-27.
This supplement supersedes missing-score/ID/time statements above for the IDs
listed here; the earlier registration, interpretation and local checks remain
historical. Values below are released API scores, not unnoised raw scores.
Created time is platform submission metadata, not the snapshot directory date.
Current leaderboard membership is not a historical best-update event log.
The uploaded ZIP bytes/hash and hosted runtime are not verified by this response.

| Submission ID | Filename | Created (KST) | Status | Grand API | UNICEF API | World Bank API | UNHCR API | On leaderboard at snapshot |
|---|---|---|---|---:|---:|---:|---:|---|
| 912056 | 2026-09-03-E013.zip | 2026-09-02 20:00:59.280977 +09:00 | Finished | 0.5966666667 | 0.5200000000 | 0.4900000000 | 0.7800000000 | false |

[Complete score ledger](../SCORES.md) and [sanitized source](../hosted-scores/2026-09-27.json).
All score precision fields are 2. Failed attempts have no scores; never substitute zero.
