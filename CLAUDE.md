# CLAUDE.md — SimulacraBench / HSCC (NeurIPS 2026 Competition)

Working folder for SimulacraBench, officially the Humanitarian Survey Completion Competition (HSCC). Original briefing: `SIMULACRABENCH.md` (Korean, partially outdated — this file wins on conflicts). Official site: <https://simulacrabench.org> · Starter kit: <https://github.com/SituatedEvals/public> (cloned at `external/starter-kit/`, gitignored) · Leaderboard: <https://www.codabench.org/competitions/17822/> · Terms/forum: Codabench org 4076 · Contact: team@simulacrabench.org. (Pre-launch URLs situatedevals.org and the `notebooks` repo are dead.)

## Task summary (per official starter kit README)

Three unpublished survey instruments (post-launch schema update 2026-08-19): UNICEF v1.1 "Faith & Immunisation" 19 items / 12 scored / 8 gated (19,846 rows, 10 countries); World Bank "Skills Assessment" 106 / 76 scored / 40 gated (6,927 rows, 3 countries, youth job-seekers); UNHCR ERPIS v1.3 285 / 213 scored / 156 gated (10,349 rows — Syrian refugees in Egypt/Iraq/Jordan/Lebanon, 2 CATI rounds treated as independent cross-sections). Schema `description` fields now carry real instrument metadata — read them, they are modelling input. Visible respondents arrive complete; **held-out respondents show only their `GIVEN` block — every `PREDICT` cell is blank and scored** (cross-respondent generalization; there are no separate Track A/B).

- Item classes: `GIVEN` (visible, never scored), `PREDICT` (held out, scored), `EXCLUDE` (never shown, stays in schema — filter on `class`, don't assume columns line up).
- **Respondent roles, fixed at dataset build:** one `respondents.parquet` with a `role` column ∈ {`TRAIN`, `DEV`, `TEST`} (renamed from FINAL), counts published in `schema["split"]`: unicef 14,885/1,488/3,473 · world_bank 5,195/520/1,212 · unhcr 8,279/621/1,449. **Nothing is subsampled** (`data_fraction` removed): phase 1 = all TRAIN visible, all DEV scored (exact scored cells: unicef 17,856 · wb 39,520 · unhcr 132,273); phase 2 = TRAIN+DEV visible, TEST scored. TEST rows not shipped in phase 1. Scored set fixed within a phase → leaderboard entries directly comparable.
- **Gates are approximate on real UNHCR data**: schema states gate-vs-data agreement has median 0.83, range 0.29–0.98; the three s3_11 return-intention branches overlap in the file; five multi-select families mark the sentinel in round 2 only; five gates approximate conditions the one-parent format can't express (the `GATE_CORRECTIONS.md` reference was removed from the schema 2026-09-01; organizer email 2026-09-02: "<5 gating changes" to unhcr still unshipped — re-run the full harness when a kit update lands). **Hard gate coupling (P=1) is unsafe on unhcr — soften toward observed sentinel rates.** Sandbox gates remain exact, so this failure mode is invisible locally.
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
- Phase 1: **1 leaderboard submission/day — the 20-total cap was removed 2026-08-18** (config.yml commit "Removed max per participant submission number"; Codabench shows 1/day only). Phase 2: single final submission + 4-page method description (`docs/method-4p.md`). Submissions stay disciplined regardless: local-harness verification first, expected-vs-actual logged.
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

- **Launched (Codabench live 2026-08-19, site says launch Aug 18). Registered — auto-approve.**
- Phase 1 (dev): now – **Oct 30 (site) / Oct 31 (Codabench phase config)** — treat Oct 30 as the safe deadline. Phase 2: Nov 1–14, single submission.
- Dec: NeurIPS Sydney session. Top-3 = proceedings co-authorship. New: **"Roots of the Data Prize"** for top teams based in the 14 data-collection countries (not us).
- Codabench leaderboard columns: Grand Prize (mean skill) + per-instrument UNICEF / World Bank / UNHCR.

**Verification history:** launch kit audited 2026-08-17; post-launch kit update pulled 2026-08-19 (8 commits: FINAL→TEST rename, split counts, cap removal, real instrument metadata in schema descriptions, unhcr/wb gating rework, disjunctional-gating documentation). Baselines three: `marginal_counts`, `bundled_artifact` (bundled-CSV prior shape), `external_model` (HF LLM prior via `models.txt` + gate recursion + Dirichlet backoff).

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
docs/analysis/   # A-series process records (EDA, domain research): append-only attempt logs, every method/version/dead end — see TEMPLATE.md there
```

## Operating discipline (how every modelling decision is made)

1. **No claim without a number.** Every modelling change is justified only by held-out skill on the local harness. No merge without measured improvement.
2. **Structure before parameters.** Exhaust deterministic structure (skip-logic gate coupling, chain closure) before adding learned components — the organizers measured gating alone at 0.98 → 0.76 log score.
3. **Overconfidence is the cardinal sin.** A confident wrong cell costs log(1e-3) ≈ −6.9 nats vs ≈ −1.4 for an honest hedge. When uncertain, shrink toward the marginal; check calibration before any submission.
4. **Submissions are ammunition** — 1/day (total cap removed 2026-08-18, but the noised leaderboard still can't rank close variants). Never spend a submission on unverified changes; record expected score before submitting, compare after.
5. **Complexity must pay rent.** A complex model is adopted only after beating the calibrated simple stack on the local harness, within the wall-clock budget (profile it).
6. **Everything is logged** — hypothesis → result → conclusion in docs/log.md. An unreproducible experiment didn't happen.
7. **Every empirical conclusion is validated against background domain.** Two domain types, tracked separately: *technical* (methods — which technique, how implemented) and *background* (what the data means — populations, instruments, humanitarian context; independent of AI/statistics). An EDA finding or measured gain becomes a claim only after checking consistency with background domain knowledge (docs/domain.md, published survey reports). A finding that contradicts domain expectations is flagged — neither auto-rejected nor built upon as-is. Domain surprise raises the evidence bar, it does not veto: check for artifacts (leakage, coding error, confound) and replicate (different seed/split/instrument slice) before adopting; if it survives, adopt it AND log it as a potential genuine discovery (surprising-but-real correlations exist — domain consensus can be wrong). Numbers-only correlation chains without this check produce contradictory hypotheses (lesson from prior work). Experiment files carry a "Domain check" section: expectation pre-registered before the run, verdict after.

## Experiment tree (how approaches are recorded)

- **One experiment = one file** in `docs/experiments/E0XX-slug.md` (copy `TEMPLATE.md`): `parent:` header is the tree edge (which model it branches from), `status:` ∈ adopted / rejected / parked / superseded-by:E0YY. `docs/log.md` stays a daily journal and refers to experiments by ID.
- **Rejected model code is never deleted** — only its status changes. Approaches get revived and combined; deleting code falsifies the tree.
- **Commit messages carry the experiment ID** (`E003: given-stratum backoff`) so git history maps onto the tree.
- **Adoption threshold is fixed**: Δ(3-instrument mean, sample excluded) > +0.005 (~3σ of phase-sampling noise, measured 2026-08-12). The experiment file's Decision section is the only place verdicts are rendered.
- `python scripts/render_tree.py` regenerates `docs/tree.md` (mermaid) from the headers — run it whenever an experiment file is added or its status changes.
- Leaderboard submissions snapshot into `submissions/` with the experiment ID and expected-vs-actual score pair.
- Submission ZIPs use `submissions/YYYY-MM-DD-E0XX.zip`; matching source and scorecards use `submissions/YYYY-MM-DD-E0XX/`. Keep future deliverables in this established layout, not `output/dev/` (user preference, 2026-09-19).
- **End of each working day: push to `origin` (private GitHub repo).**

## Study sessions

Domain study runs as one-paper-per-session via the `paper-session` skill (`.claude/skills/paper-session/`): reading map from the paper's own sections → 3 self-check questions → tier-bound deliverable ([구현] = running code, [설계] = design note, [스킴] = 3-line summary) → ✅ + summary recorded in `docs/domain-study-guide.ko.md` → `study:` commit. Tiers and deliverables are defined per entry in that guide.

## Rules for working here

- **All code, comments, and commit messages in English.**
- Never hardcode assumptions about the real data — develop only against the synthetic sandbox and published shard statistics.
- Local validation harness is the source of truth between daily submissions; don't waste the 1/day leaderboard submission on unverified changes.
- Log every experiment in `docs/log.md`; snapshot every submission in `submissions/`.
- Strategy priority: exact skip-logic handling → calibrated simple models (IRT + low-rank + smoothing) → hybrids. LLM persona-prompting is log-loss-unfavorable without calibration post-processing.
- `external/starter-kit/score.py` is the official grader — use it for final validation of any submission; keep `src/eval/` for fast in-process iteration and mirror its skill metric exactly.
