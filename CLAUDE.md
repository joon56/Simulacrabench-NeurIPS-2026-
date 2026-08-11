# CLAUDE.md — SimulacraBench / HSCC (NeurIPS 2026 Competition)

Working folder for SimulacraBench, officially the Humanitarian Survey Completion Competition (HSCC). Original briefing: `SIMULACRABENCH.md` (Korean, partially outdated — this file wins on conflicts). Official site: <http://situatedevals.org/simulacrabench> · Starter kit: <https://github.com/SituatedEvals/notebooks> (cloned at `external/starter-kit/`, gitignored) · Leaderboard/rules/forum: Codabench org 4076 · Contact: h4upt@stanford.edu

## Task summary (per official starter kit README)

Three unpublished survey instruments (UNICEF 19 items/12 scored, World Bank 82/73, UNHCR ERPIS 230/213 with 142 gated). Train respondents arrive complete; **test respondents show only their `GIVEN` block — every `PREDICT` cell is blank and scored** (cross-respondent generalization; there are no separate Track A/B).

- Item classes: `GIVEN` (visible, never scored), `PREDICT` (held out, scored), `EXCLUDE` (never shown).
- **`NaN` means exactly one thing: held out, predict it.** Genuine non-response ("Prefer not to answer", "Refused") is an ordinary level.
- **Gated items get one extra final slot for `schema["gated_value"]` (`NA_GATED`)** — "never asked" is a real scored answer. Predicting who gets skipped is worth as much as predicting what they say. Option order comes from the schema, never from the data.

## Metric (leaderboard = skill)

- Per cell: log(p) of the realized answer, averaged over all blank cells (pooled, not per-item).
- **`skill = 1 + log_score / U`**, U = mean over scored items of log K (K includes gate sentinel; schema-only). 0 = uniform guess, 1 = perfect. Leaderboard = plain mean of the three instruments' skills.
- Vectors are renormalized and mixed with a flat vector so no probability falls below `scoring.floor` = 1e-3 — no need to floor your own numbers, but a confidently wrong cell still costs log(1e-3). Hedge where evidence is thin.
- **Phase-1 scores are noised** (Laplace, ε=10, rounded to 0.01) and pooled — no per-item breakdown. Local harness is the only precise signal.

## Submission constraints

- Zip with `main.py` + pinned `requirements.txt` **at top level**. `predict(frame, schema)` returns one probability vector per blank cell — row-major over test rows, items in `schema["items"]` key order (not `frame.columns` order), no zeros/negatives, each summing to 1.
- `predict()` must be pure: no files, sockets, processes, or imports outside `requirements.txt`. Network is removed before import.
- Compute: **1× H100, 16 GB RAM. Phase 1: 900 s per instrument; Phase 2: 3600 s.** Same `predict()` must PASS all three schemas.
- Phase 1: 1 leaderboard submission/day, **max 20 total per participant**. Phase 2: single final submission + 4-page method description (`docs/method-4p.md`).
- External pretrained weights: publicly downloadable, pinned commit hash, declared before phase 2, packaged in the image (no network).
- Data exfiltration / re-identification attempts = disqualification (contractual, third-party enforceable).

## Local pipeline (verified end-to-end)

```
# from external/starter-kit/
python make_sandbox.py --schema data/sample.json --out _sandbox/sample
python score.py --submission baseline/marginal_counts --data _sandbox/sample --schema data/sample.json --phase 1
```

Sandbox has the real shape (same columns/options/skip logic) but invented marginals/dependencies: **a model tuned to the sandbox will not transfer; a pipeline debugged against it will.**

## Key dates (2026)

- **Aug 17: public launch (postponed from Aug 10 on 2026-08-11).** Registration opens with launch.
- Aug 17 – Oct 31: phase 1 (dev). Nov 1–14: phase 2 (final), single submission.
- Dec: NeurIPS Sydney session. Top-3 = proceedings co-authorship.

**Pre-launch caveat:** the cloned starter kit is a pre-launch draft (last push 2026-08-10, before the postponement). On Aug 17: `git pull` the kit, re-verify README/config.yml facts above (metric, floor, timeouts, submission caps, schemas), and diff against this file. Known draft inconsistencies in kit commit history: rules doc v0.8 says 92 submissions vs config.yml `max_submissions_per_participant: 20`; contact address neurips-un-benchmark@stanford.edu vs h4upt@stanford.edu; stale phase dates.

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

## Operating discipline (how every modelling decision is made)

1. **No claim without a number.** Every modelling change is justified only by held-out skill on the local harness. No merge without measured improvement.
2. **Structure before parameters.** Exhaust deterministic structure (skip-logic gate coupling, chain closure) before adding learned components — the organizers measured gating alone at 0.98 → 0.76 log score.
3. **Overconfidence is the cardinal sin.** A confident wrong cell costs log(1e-3) ≈ −6.9 nats vs ≈ −1.4 for an honest hedge. When uncertain, shrink toward the marginal; check calibration before any submission.
4. **Submissions are ammunition** — 20 total. Never spend a leaderboard submission on unverified changes; record expected score before submitting, compare after.
5. **Complexity must pay rent.** A complex model is adopted only after beating the calibrated simple stack on the local harness, within the wall-clock budget (profile it).
6. **Everything is logged** — hypothesis → result → conclusion in docs/log.md. An unreproducible experiment didn't happen.

## Rules for working here

- **All code, comments, and commit messages in English.**
- Never hardcode assumptions about the real data — develop only against the synthetic sandbox and published shard statistics.
- Local validation harness is the source of truth between daily submissions; don't waste the 1/day leaderboard submission on unverified changes.
- Log every experiment in `docs/log.md`; snapshot every submission in `submissions/`.
- Strategy priority: exact skip-logic handling → calibrated simple models (IRT + low-rank + smoothing) → hybrids. LLM persona-prompting is log-loss-unfavorable without calibration post-processing.
- `external/starter-kit/score.py` is the official grader — use it for final validation of any submission; keep `src/eval/` for fast in-process iteration and mirror its skill metric exactly.
