# Experiment log

## 2026-08-09

- Repo scaffolded per SIMULACRABENCH.md §8, git initialized, CLAUDE.md added.
- Official site checked (situatedevals.org/simulacrabench + GitHub org `SituatedEvals`): starter kit NOT published yet — launch is 2026-08-10. Only `website` repo exists; page source has no kit links. **TODO tomorrow: register (Google Form), clone starter kit, verify submission pipeline end-to-end on official synthetic sandbox, replace provisional sandbox.**
- Built local log-loss harness (`src/eval/`): mean log-loss pooled over masked cells (assumption — verify pooling vs per-item averaging against official kit), Track A (MCAR cell mask) and Track B (respondent holdout, demographics visible) splitters, provisional synthetic sandbox with all announced item types incl. skip-logic "not shown" level, per-item marginal baseline. 8 tests pass.
- Baseline numbers on provisional synthetic sandbox (n=5000, seed=42, 20% mask):

  | Model | Track A | Track B |
  |---|---|---|
  | uniform | 1.1206 | 1.1537 |
  | marginal (Laplace α=1) | 1.0856 | 1.0987 |
