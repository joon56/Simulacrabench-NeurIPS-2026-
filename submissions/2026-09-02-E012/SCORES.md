# 2026-09-02-E012 — shared-trunk multi-head net + ladder + cond agreement

Experiment: E012 (adopted; parent E010). Code: self-contained merge of
hier_backoff + logit_blend helpers + cond_agree + shared_trunk (script-
assembled from the verified src modules, dead code stripped). One torch
MLP per instrument (one-hot GIVEN → 64-64 trunk → per-item heads + asked-
only conditional heads), blended with the backoff ladder; E010's
conditional gate-agreement unchanged. No bundled artifacts, no
requirements.txt (torch pre-installed). Zip:
`submissions/2026-09-02-E012.zip`, check_submission_zip OK.

## Local scores (2026-09-02, seed 0, phase 1)

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact (runner) | 0.4429 | 0.5006 | 0.4549 | 0.5629 | 0.5061 |
| E010 (LB 0.59) | 0.4418 | 0.4994 | 0.4447 | 0.5532 | 0.4991 |

Δ +0.0070 (threshold +0.005). Official score.py PASS ×3: 0.5000 /
0.4500 / 0.5600 (noised sandbox, consistent with exact). Wall-clock
~200 s local CPU ≪ 900 s. Tests 42 passed + 1 xfail (the E011 sim
assertion, kept strict as the null-result record).

## Leaderboard expectation (real data)

Reference: E010 LB = 0.59 (unicef 0.51 / wb 0.49 / unhcr 0.77).
Pre-registered 2026-09-02 BEFORE submission:

- Across-the-board gain expected; Grand ≈ 0.60–0.62. The established
  pattern (real GIVEN coupling > sandbox trait, 3 consecutive
  submissions) says real Δ ≥ sandbox Δ (+0.007).
- **wb is the falsifiable core**: sandbox says +0.0102, and the (b)
  domain claim (sectioned multi-factor instruments reward cross-item
  sharing beyond the 1-factor sandbox) predicts wb ≥ +0.01 on the LB —
  wb 0.49 → 0.50+ expected. wb flat AGAIN would kill the sharing story
  for wb specifically and redirect wb work to its per-item conditionals.
- unhcr + expected (213 heads; but 0.77 already high, U cheapest —
  even +0.01 is meaningful). unicef ~flat (12 heads, sandbox +0.001).
- Risk watch: torch net overconfident on real data where coupling is
  weaker than sandbox → the tuned w guard (interior values locally)
  should absorb it; any instrument −0.02 ⇒ inspect w chosen on real
  data is not the issue (not observable) — mitigate by lowering w grid
  cap or reverting to E010, and treat as evidence the net memorized
  visible-row idiosyncrasies.
