# CLAUDE.md — SimulacraBench / HSCC (NeurIPS 2026 Competition)

Working folder for SimulacraBench, officially the Humanitarian Survey Completion Competition (HSCC). Original briefing: `SIMULACRABENCH.md` (Korean, partially outdated — this file wins on conflicts). Official site: <https://simulacrabench.org> · Starter kit: <https://github.com/SituatedEvals/public> (cloned at `external/starter-kit/`, gitignored) · Leaderboard: <https://www.codabench.org/competitions/17822/> · Terms/forum: Codabench org 4076 · Contact: team@simulacrabench.org. (Pre-launch URLs situatedevals.org and the `notebooks` repo are dead.)

## Task summary (per official starter kit README)

Three unpublished survey instruments (schema v1.0 at launch): UNICEF 19 items / 12 scored / 7 gated (19,847 rows); World Bank 106 / 76 scored / 19 gated (6,927 rows); UNHCR ERPIS 285 / 213 scored / 143 gated (10,349 rows). Visible respondents arrive complete; **held-out respondents show only their `GIVEN` block — every `PREDICT` cell is blank and scored** (cross-respondent generalization; there are no separate Track A/B).

- Item classes: `GIVEN` (visible, never scored), `PREDICT` (held out, scored), `EXCLUDE` (never shown, stays in schema — filter on `class`, don't assume columns line up).
- **Respondent roles, fixed at dataset build:** one `respondents.parquet` with a `role` column ∈ {`TRAIN`, `DEV`, `FINAL`}. Phase 1: `TRAIN` visible (thinned to `data_fraction` 0.30 — visible rows only, scored cells never thinned), `DEV` masked and scored. Phase 2: `TRAIN`+`DEV` visible with answers, `FINAL` scored. `FINAL` rows are not shipped at all in phase 1, so the phase-1 leaderboard can't leak the final answer key. Scored set is fixed within a phase → leaderboard entries directly comparable.
- **`NaN` means exactly one thing: held out, predict it.** Genuine non-response ("Prefer not to answer", "Refused") is an ordinary level.
- **Gated items get one extra final slot for `schema["gated_value"]` (`NA_GATED`)** — "never asked" is a real scored answer. Predicting who gets skipped is worth as much as predicting what they say. Option order comes from the schema, never from the data.

## Metric (leaderboard = skill)

- Per cell: log(p) of the realized answer, averaged over all blank cells (pooled, not per-item).
- **`skill = 1 + log_score / U`**, U = mean over scored items of log K (K includes gate sentinel; schema-only). 0 = uniform guess, 1 = perfect. Leaderboard = plain mean of the three instruments' skills.
- Vectors are renormalized and mixed with a flat vector so no probability falls below `scoring.floor` = 1e-3 — no need to floor your own numbers, but a confidently wrong cell still costs log(1e-3). Hedge where evidence is thin.
- **Phase-1 scores are noised** (Laplace, ε=10, rounded to 0.01). Leaderboard shows per-instrument skill and the mean, but never per-item detail. Local harness is the only precise signal.

## Submission constraints

- Zip (≤ 1 GB, no zip-inside-zip, no folder wrapping) with `main.py` **at the archive root**; build with `cd my_submission && zip -r ../sub.zip .`. Validate the archive with `python tools/check_submission_zip.py sub.zip` before spending a submission.
- `requirements.txt` is **optional** — the hosted image (Python 3.13) pre-installs numpy, pandas, pyarrow, scipy, scikit-learn, torch, torchvision, Pillow, transformers, sentence-transformers, tokenizers, sentencepiece, tiktoken, huggingface_hub, accelerate, safetensors, bitsandbytes, autoawq, protobuf, and `torch_measure` (organizer IRT/latent-trait lib). Only declare what the image lacks, **pinned exact versions** (unpinned → `HSCC-BUILD-002`). Installed at image build, off the clock.
- **HF models via `models.txt`** (one repo id per line, e.g. `Qwen/Qwen2.5-1.5B-Instruct`): downloaded into the image cache at build time, `from_pretrained()` finds them offline. Other fitted artifacts (`.pt`, `.safetensors`, `.joblib`, …) must be bundled in the zip and loaded from a local path. FAQ: disclose external models/data used.
- `predict(frame, schema)` is called **once per instrument**, returns one probability vector per blank cell — rows top-to-bottom, items in `schema["items"]` key order (not `frame.columns` order), each vector finite, non-negative, sum > 0 (grader renormalizes+floors). Load weights at **module import**, not inside `predict()`.
- Network removed before import; no downloads at runtime (`HSCC-NETWORK-*` / `HSCC-HF-CACHE`).
- Compute: **1× H100, 16 GB RAM (hard limit), 8 CPUs. Phase 1: 900 s; Phase 2: 3600 s — the budget covers the whole run: import + model load + all three instruments together, NOT per instrument.** Same `predict()` must PASS all three schemas.
- Phase 1: 1 leaderboard submission/day, **max 20 total per participant** (confirmed in launch config.yml). Phase 2: single final submission + 4-page method description (`docs/method-4p.md`).
- Failures come back as sanitized `HSCC-*` codes only — no stdout, no tracebacks (exception *type* survives, message dropped). Debug locally; the platform will not tell you more.
- Data exfiltration / re-identification attempts = disqualification (contractual, third-party enforceable).

## Local pipeline (verified end-to-end)

```
# from external/starter-kit/
python make_sandbox.py --schema data/sample.json --out _sandbox/sample   # writes respondents.parquet + schema.json
python score.py --submission baseline/marginal_counts --data _sandbox/sample --schema data/sample.json --phase 1
python tools/check_submission_zip.py sub.zip                             # archive contract, says nothing about score
```

Fast iteration: `src/eval/runner.py` scores any `predict()` in-process on all four sandboxes with exact (un-noised) skill, using the kit's own scoring functions.

Sandbox has the real shape (same columns/options/skip logic/roles) but invented marginals: **a model tuned to sandbox content will not transfer; a pipeline debugged against it will.** Since launch, `sandbox.trait_scale` = 2.0 (was 0.6 in the draft) — respondent-level dependence is now strong enough locally to test conditional models, not just column-marginal ones. An LLM world-knowledge prior is *by construction* useless on the sandbox (answers are random) — don't read a sandbox non-gain as the prior failing (organizers' own warning in `baseline/external_model`).

## Key dates (2026)

- **Aug 17: public launch (done).** Registration open.
- Aug 17 – Oct 30: phase 1 (dev). Nov 1–14: phase 2 (final), single submission.
- Dec: NeurIPS Sydney session. Top-3 = proceedings co-authorship.

**Launch-day verification (2026-08-17):** kit re-cloned from the new `public` repo and diffed against the draft; all facts above re-verified against launch README/config.yml. Draft ambiguities resolved: submission cap **20** stands; contact is team@simulacrabench.org. Baselines now three: `marginal_counts` (unchanged), `bundled_artifact` (bundled-CSV prior — the shape to copy for offline-fitted artifacts), `external_model` (HF LLM prior via `models.txt` + gate recursion + Dirichlet backoff).

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

## Experiment tree (how approaches are recorded)

- **One experiment = one file** in `docs/experiments/E0XX-slug.md` (copy `TEMPLATE.md`): `parent:` header is the tree edge (which model it branches from), `status:` ∈ adopted / rejected / parked / superseded-by:E0YY. `docs/log.md` stays a daily journal and refers to experiments by ID.
- **Rejected model code is never deleted** — only its status changes. Approaches get revived and combined; deleting code falsifies the tree.
- **Commit messages carry the experiment ID** (`E003: given-stratum backoff`) so git history maps onto the tree.
- **Adoption threshold is fixed**: Δ(3-instrument mean, sample excluded) > +0.005 (~3σ of phase-sampling noise, measured 2026-08-12). The experiment file's Decision section is the only place verdicts are rendered.
- `python scripts/render_tree.py` regenerates `docs/tree.md` (mermaid) from the headers — run it whenever an experiment file is added or its status changes.
- Leaderboard submissions snapshot into `submissions/` with the experiment ID and expected-vs-actual score pair.
- **End of each working day: push to `origin` (private GitHub repo).**

## Rules for working here

- **All code, comments, and commit messages in English.**
- Never hardcode assumptions about the real data — develop only against the synthetic sandbox and published shard statistics.
- Local validation harness is the source of truth between daily submissions; don't waste the 1/day leaderboard submission on unverified changes.
- Log every experiment in `docs/log.md`; snapshot every submission in `submissions/`.
- Strategy priority: exact skip-logic handling → calibrated simple models (IRT + low-rank + smoothing) → hybrids. LLM persona-prompting is log-loss-unfavorable without calibration post-processing.
- `external/starter-kit/score.py` is the official grader — use it for final validation of any submission; keep `src/eval/` for fast in-process iteration and mirror its skill metric exactly.
