# 2026-09-09-E025 — E022 evidence layer ∘ E017 capacity grid

Experiment: E025 (adopted as a leaderboard-backed composition; parent
E022). Code: E022 assembly + per-instrument trunk selection from
{64×2, 128×2+dropout} (E017 v3's grid). Zip:
`submissions/2026-09-09-E025.zip`, check_submission_zip OK.

## Local scores (2026-09-08, seed 0, phase 1)

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact (runner) | 0.4436 | 0.5006 | 0.4548 | 0.5629 | 0.5061 |
| E022 (LB 0.63 / unhcr 0.88) | 0.4429 | 0.5006 | 0.4549 | 0.5627 | 0.5061 |

Sandbox is blind to capacity (E009/E011/E015); the composition's local
role is parity of the evidence layer (held) and runtime. Official
score.py PASS ×3: 0.5000 / 0.4500 / 0.5600 (parity exact on the three
instruments; sample 0.4432 vs 0.4436 = torch CPU reduction noise). **Wall-clock 297 s local on CPU** — above the
observed hosted-failure point (E019: 240 s local timed out once; E018
passed at 250 s). Mitigation: training runs on the worker's H100 when
`torch.cuda.is_available()` (the kit's own baseline uses the identical
pattern; README: "the worker has one H100"), which removes the net
training cost (~140 s of the 297 s); CPU fallback exists. **If this
submission times out: pin per-instrument configs (no selection) and
resubmit; the GPU path is then assumed dead and every later design
must fit ~130 s local on CPU.**

## Leaderboard expectation (real data)

Reference: E022 LB = 0.63 (0.52 / 0.49 / 0.88); E017 read unhcr +0.01
over its base. Pre-registered 2026-09-08 BEFORE submission:

- **unhcr ≥ 0.89** (Grand likely rounds to 0.64) ⇒ E017's +0.01 was
  real and the two gains add — capacity re-enters the toolbox as a
  leaderboard-backed refinement; next stack candidates are the rest of
  E017's grid and E024 (evidence-input base) as an A/B.
- **unhcr 0.88** ⇒ E017's +0.01 was noise; capacity axis closed for
  good; E025 harmless (keep E022 as the base).
- **unhcr ≤ 0.87** ⇒ interaction harm (wider net + evidence mixing);
  revert to E022.
- unicef/wb flat expected (selector keeps unicef small; wb's 128×2 read
  flat in E017).
