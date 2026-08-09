# CLAUDE.md — SimulacraBench (NeurIPS 2026 Competition)

Working folder for the SimulacraBench competition. Full briefing: `SIMULACRABENCH.md` (Korean). Official site: <http://situatedevals.org/simulacrabench> · Contact: h4upt@stanford.edu

## Task summary

Probabilistic completion of a survey response matrix: unreleased UN microdata (21 countries, ~61k respondents, ~150 items). For each masked cell, predict a probability distribution over response levels.

- **Metric: mean test log-loss** (strictly proper, calibration-sensitive). Accuracy is NOT the metric — calibration IS the score. Well-calibrated simple models beat overfit complex ones.
- Item types: binary, nominal, ordered Likert, multi-select, binned continuous. **Skip-logic gating is treated as a separate response level** — mishandling it in preprocessing loses points; handling it correctly is likely free score over baselines.
- **Track A**: within-respondent imputation (MCAR-masked items per training respondent).
- **Track B**: cross-respondent generalization (held-out respondents, only sociodemographics given).

## Submission constraints

- Docker image or Python script + environment file, implementing the specified API. Run in an offline sandbox — **no outbound network**. Training inside submission code on unmasked matrix parts is allowed.
- Compute: 1× A100. Wall-clock: **10 min/submission (dev phase)**, **100 min (test phase)**. Maintain a light 10-min version and a separate extended test-phase version.
- Dev phase: 1 leaderboard submission per day (daily rotating 10% shard). Test phase (Nov 1–14): single final submission.
- External pretrained weights allowed only if publicly downloadable + pinned commit hash + declared before test phase.
- Every submission needs a 4-page method description (`docs/method-4p.md`).
- Data exfiltration attempts = disqualification.

## Key dates (2026)

- **Aug 10**: public launch + registration (Google Form) — register immediately.
- Aug 10 – Oct 31: dev phase. Nov 1–14: test phase, leaderboard frozen.
- Dec: NeurIPS Sydney session. Top-3 per track = proceedings co-authorship.

## Folder structure (keep to this)

```
data/            # schema + synthetic sandbox only (real data never leaves closed environment)
notebooks/       # EDA, item-type analysis
src/preprocess/  # encoding, skip-logic handling
src/models/      # irt / lowrank / diffusion / hybrid
src/eval/        # local log-loss harness (reproduces official metric)
submissions/     # dated submission snapshots + leaderboard score log
docker/          # submission image definitions
docs/            # method-4p.md, log.md (daily experiment log)
```

## Rules for working here

- **All code, comments, and commit messages in English.**
- Never hardcode assumptions about the real data — develop only against the synthetic sandbox and published shard statistics.
- Local validation harness is the source of truth between daily submissions; don't waste the 1/day leaderboard submission on unverified changes.
- Log every experiment in `docs/log.md`; snapshot every submission in `submissions/`.
- Strategy priority: exact skip-logic handling → calibrated simple models (IRT + low-rank + smoothing) → hybrids. LLM persona-prompting is log-loss-unfavorable without calibration post-processing.
