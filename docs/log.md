# Experiment log

Daily record. Domain literature: [[domain]] · kit mechanics: [[starter-kit-notes]].

## 2026-08-11 (later)

- **Launch postponed to Aug 17** (website commit 2026-08-11 04:12 UTC, "Update launch date to August 17, 2026"; timeline heading changed "Eight months" → "Four months"). Registration opens with launch — no registration or leaderboard submission possible until then.
- Starter kit repo still public and unchanged (last push 8/10) — our clone is a pre-launch draft. All facts derived from it (skill metric, floor, 900/3600 s, submission caps, schemas) must be re-verified against the kit on Aug 17.
- Draft inconsistencies visible in kit commit history: rules v0.8 "92 submissions" vs config.yml cap 20; contact address mismatch; tutorial commit still uses "Track B" wording the README dropped.
- Tutorial commit (8/5) leaks a useful signal: in the kit's own experiments, **skip-logic handling was the single largest gain (M1 0.98 → M2 0.76 log score), more than any modelling step** — confirms the strategy priority; and naive Bayes underperforms because one latent trait per respondent makes answers conditionally dependent (double-counting evidence).

## 2026-08-11

- **Competition launched.** Starter kit found: <https://github.com/SituatedEvals/notebooks>, cloned at `external/starter-kit/` (gitignored). Official name: Humanitarian Survey Completion Competition (HSCC). Leaderboard/rules/registration on Codabench (org 4076).
- Pipeline verified end-to-end on all four schemas with the official grader (`score.py`, marginal_counts baseline, phase 1, noised skill scores): sample PASS 0.45, unicef PASS 0.19, world_bank PASS 0.25, unhcr PASS 0.32. Run times ~25 s each, far under the 900 s limit.
- Major corrections vs the original briefing (CLAUDE.md updated accordingly):
  - No Track A/B. Single task: held-out respondents, `GIVEN` visible, all `PREDICT` cells scored.
  - Leaderboard metric is **skill** = 1 + log_score/U (0 = uniform, 1 = perfect), plain mean over three instruments; log score pooled over cells.
  - Grader floors vectors by mixing with flat vector, floor 1e-3 — no self-flooring needed.
  - Compute: 1× **H100**, 16 GB RAM; **900 s/instrument (phase 1)**, 3600 s (phase 2) — not A100 10/100 min.
  - Phase-1 scores noised (Laplace ε=10, rounded 0.01); **max 20 submissions total** per participant on top of 1/day.
  - Gated items: extra final option slot for sentinel `NA_GATED`; predicting who gets skipped scores like any answer.
- Local harness updated to mirror official metric exactly (`floor_mix`, `uniform_reference`, `skill` in `src/eval/logloss.py`); pooling-over-cells assumption confirmed against `score.py`. 10 tests pass.
- Next: register (Google Form + Codabench, user action), first leaderboard submission with marginal baseline to validate the official pipeline, then start on structure-aware models (respondent-trait / low-rank on GIVEN block).

## 2026-08-09

- Repo scaffolded per SIMULACRABENCH.md §8, git initialized, CLAUDE.md added.
- Official site checked (situatedevals.org/simulacrabench + GitHub org `SituatedEvals`): starter kit NOT published yet — launch is 2026-08-10. Only `website` repo exists; page source has no kit links. **TODO tomorrow: register (Google Form), clone starter kit, verify submission pipeline end-to-end on official synthetic sandbox, replace provisional sandbox.**
- Built local log-loss harness (`src/eval/`): mean log-loss pooled over masked cells (assumption — verify pooling vs per-item averaging against official kit), Track A (MCAR cell mask) and Track B (respondent holdout, demographics visible) splitters, provisional synthetic sandbox with all announced item types incl. skip-logic "not shown" level, per-item marginal baseline. 8 tests pass.
- Baseline numbers on provisional synthetic sandbox (n=5000, seed=42, 20% mask):

  | Model | Track A | Track B |
  |---|---|---|
  | uniform | 1.1206 | 1.1537 |
  | marginal (Laplace α=1) | 1.0856 | 1.0987 |
