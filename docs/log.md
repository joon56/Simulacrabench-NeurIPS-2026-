# Experiment log

Daily record. Domain literature: [[domain]] · kit mechanics: [[starter-kit-notes]].

## 2026-08-29 — E006 hierarchical backoff; submission #3 packaged

- **E006 (MRP-lite ladder) implemented and adopted**: greedy forward
  selection of ≤ 3 GIVEN columns, per-level κ, each level's prior = level
  above (p_L = (count + κ_L·p_{L-1})/(n + κ_L)); E003 softening and gate
  recursion unchanged. Runner: 3-inst mean 0.4682 → 0.4783 (Δ +0.0101).
  Depth 3 selected on all four schemas with shrinking gains and rising κ —
  the MRP empty-cell prediction measured (pre-registered watch point).
  Selection vectorized (groupby + κ batching + prefix caching): unhcr
  selection 75 s, total ~95 s.
- **Submission #3 packaged** (`submissions/2026-08-29-E006/`, zip OK,
  score.py PASS 0.48/0.42/0.54, 23/23 tests). LB expectations
  pre-registered in SCORES.md (modest gain; unicef largest; flat result
  not falsifying at ±0.01–0.02 noise; >0.02 drop ⇒ greedy instability
  diagnostic).
- Next in queue: eRPIS published-marginal priors as bundled CSV (A001
  transcriptions), T1 temperature scaling as calibration guard, A001 v3
  (unicef exact source study with the named 10-country list).
- **A003 done (same day): eRPIS Sep-2025 tables → `data/priors/erpis_2025.csv`**
  (49 rows, basis-tagged verbatim/derived/mapped-medium, mapped onto real
  item names; intention chain s3_11→s3_12→s3_13 matches published
  conditionals 1:1 including gate directions). Flash Jan-2025 excluded
  (wrong time point per A002 finding 1). Feeds E007.
- **E006 submitted; result: Grand 0.55 — unicef 0.50 / wb 0.48 /
  unhcr 0.66** (E005: 0.49/0.48/0.63). Pre-registration scorecard:
  across-board gain ✓, no >0.02 drops ✓, wb flat (explicitly allowed).
  One miss: unhcr gained most (+0.03, above noise), not unicef —
  consistent with country_asylum/wave entering the real-data ladder
  (the A001/A002 domain prediction); sandbox magnitude ordering again
  didn't transfer. unhcr remains the paying vein → E007 (eRPIS prior
  blend) is the right next spend.

## 2026-08-28 — E003/E004/E005 implemented; submission #2 packaged

- **E004 (stratum backoff) implemented and adopted**: data-driven stratum
  selection (GIVEN card ≤ 12; best single by 20%-holdout log score, then
  best pair; κ ∈ {1,3,10,30,100} joint) — deviation from the T3
  smallest-cardinality rule, justified by A002 finding 5 (wb country only
  38.8% recorded). Runner: mean 0.3412 → 0.4595, **unhcr moved for the
  first time** (0.4297 → 0.5347) — gate cascade over 155 PREDICT parents
  confirmed as the multiplier E001/E002 predicted. 3-inst Δ +0.1202.
- **E003 (soft gating) implemented and adopted (real-data motivated)**:
  ã_i beta-binomial-shrunk gate agreement (α=20 fixed — untunable locally),
  pred = ã·hard + (1−ã)·marginal. Clean sandbox bit-identical to E002
  (pre-registered: sandbox gates exact). Violation sim (17% flipped):
  unhcr +0.0289 log over hard; on stratum tables +0.0422 log — insurance
  grows exactly when E004 activates the cascade.
- **E005 = E003∘E004 composed, adopted, packaged as submission #2**
  (`submissions/2026-08-28-E005/`, self-contained main.py, zip OK,
  score.py PASS ×3, ~101 s total, 19/19 tests). Clean sandbox ≡ E004.
  LB expectations pre-registered in SCORES.md (unhcr largest gain; unhcr
  below 0.41 ⇒ softening insufficient → raise α / cap ã on the 59
  round-2-only multi-select items).
- Process note: Domain check sections pre-registered in E003/E004 BEFORE
  implementation (first full use of rule 7 + A-series flow: A001 → A002 →
  experiment design).
- **Submitted; result: Grand Prize 0.53 — unicef 0.49 / wb 0.48 /
  unhcr 0.63** (E002 was 0.43 — 0.45/0.43/0.41). All three pre-registered
  expectations hit: every instrument up, unhcr largest (+0.22, the
  country×wave + cascade fingerprint), no softening-failure signal.
  unhcr's real gain (+0.22) doubles the sandbox prediction (+0.105):
  real GIVEN-answer coupling is stronger than the sandbox trait — supports
  investing next in richer conditioning (hierarchical backoff T4) and the
  eRPIS published-marginal priors (A001) rather than exotic models.

## 2026-08-27 — first submission packaged (E002)

- **Submission #1 packaged: `submissions/2026-08-27-E002/`** (exact copy of
  `src/models/gated_marginal.py` as `main.py`, no requirements.txt). Zip passes
  `check_submission_zip.py`; official `score.py` PASS on all three real schemas
  (unicef 0.3200 / wb 0.2900 / unhcr 0.4300 noised, ~15 s total ≪ 900 s).
  Runner exact skills reproduce the 08-19 numbers bit-for-bit (mean 0.3412 incl
  sample, 0.3479 excl) — no drift since the kit update.
- Purpose: pipeline validation + first REAL-data baseline; sandbox skills are
  not LB predictions (see SCORES.md for qualitative expectations). Reported LB
  triple becomes the reference for all future local-vs-LB gap tracking.
- Submission cadence decided: submit only changes that clear +0.005 locally;
  E004 (stratum backoff) next but **never alone** — must ship together with
  E003 soft gating, since predictable unhcr parents + hard coupling + approximate
  gates (agreement 0.29–0.98) = invisible-on-sandbox log(1e-3) risk.
- Still open: GATE_CORRECTIONS.md forum question not yet posted.
- **Process discipline upgrades (user-driven, same day):** rule 7 added to
  CLAUDE.md — every empirical conclusion validated against BACKGROUND domain
  (vs technical domain); domain surprise raises the evidence bar (artifact
  check + replication) but never auto-rejects — survivors are adopted and
  logged as potential discoveries. Experiment TEMPLATE gains a pre-registered
  "Domain check" section. New A-series (`docs/analysis/A0XX`) records every
  analysis attempt/method/version append-only, dead ends included, so the
  full process is reconstructible for the method description and talks.
- **A001 (background domain packet) v1 done** — delegated primary-source
  research, findings in `docs/analysis/A001-sources/findings.md`. Headlines:
  unhcr = real eRPIS (wave 1 = exactly 6,316 CATI, May–Jul 2025; real design
  is a PANEL, competition flattens to cross-sections); **the Assad-fall
  return-intention discontinuity (1.7%→27%) predates the competition window —
  between-round movement is a decay (Jordan 40%→22%), not a jump** — a wrong
  jump-prior averted purely by domain check; per-country marginals for the
  gated Q1→Q2→Q3 chain transcribed from PDFs (no microdata exists); unicef ≈
  WGM 2018 item content (free CC-BY microdata = best machine-readable prior;
  importance>effectiveness>safety ordering universal); world_bank = STEP-shaped
  composite, digit-span/Corsi from impact-evaluation batteries (Laajaj &
  Macours), country triple unverifiable. 15 pre-registrable expectations
  catalogued → A002 EDA lens + E004 Domain check.
- **A002 (schema EDA) v1–v3 done** — `docs/analysis/A002-schema-eda.md`,
  report in `A002-outputs/`. Headlines: (1) **both unhcr rounds sit inside
  the single May–June 2025 eRPIS wave-1 window** (round 2 ≠ Oct–Nov wave 2)
  → A001's between-round-decay expectation WITHDRAWN, replaced with
  "rounds near-identical; eRPIS Sept-2025 tables are direct priors for
  both"; (2) s3_11 = eRPIS Q1 verbatim, ungated root with 73 direct
  children, 155/156 unhcr gate parents PREDICT → E004's target is
  literally "predict s3_11 per country×wave"; (3) unicef gating nearly
  deterministic (6/8 GIVEN parents) — explains its LB lead; COVID-era
  faith survey, 10 countries named, WGM demoted to wording ancestor;
  (4) wb country recorded for only 38.8% → stratum = employmentStatus /
  RCT arm / hadJob, NOT country; full psychometric battery as banded
  scores, EXCLUDE = raw duplicates (leak prevention); (5) sandbox gates
  verified EXACT (0 violations / 2.57M pairs) — unhcr approximate-gate
  risk invisible locally, E003 violation sim is the only probe;
  (6) U: unicef 1.5620 / wb 2.0184 / unhcr 1.2618 — unhcr cheapest-U +
  132k cells + 144 binaries = calibration leverage concentrated there.
- **Submitted; result same day: Grand Prize 0.43 — unicef 0.45 / wb 0.43 /
  unhcr 0.41.** Pipeline validated end-to-end on the hosted stack. Readings:
  (1) unhcr 0.41 is the real-data crowd-marginal skill itself (E002 ≡ marginal
  there) — largest instrument sits fully unconditioned, biggest headroom;
  (2) real-data skills ≫ sandbox skills (real marginals much sharper than
  invented ones) — sandbox-vs-LB comparisons are meaningless, gap tracking is
  LB-vs-LB from here; (3) all numbers ±0.01–0.02 (Laplace ε=10, rounded).

## 2026-08-21 — trip pack (4 days away)

- Built `trip/` pack for a 4-day trip: `trip/README.ko.md` (day plan: AM paper via `/paper-session`, PM implementation), `trip/tasks/T1–T4` (temperature scaling, E003 soft gating, E004 stratum backoff, hierarchical backoff / first-submission prep), skeleton experiment files E003/E004 (status parked, hypotheses fixed), open-access PDFs under `trip/papers/` (gitignored, zip only). Zip includes the working copy with `.git` and `external/starter-kit/` (+ sandboxes) so the runner works offline after `pip install -r requirements.txt`.
- Nothing measured today; expectations written into E003/E004 Decision sections before any code exists.

## 2026-08-19 — Codabench live, registered; kit update audit

- **Codabench competition 17822 is live; user registered (auto-approve).** Leaderboard columns: Grand Prize + per-instrument skills. Phase config: Dev to Oct 31 / 1 per day, Test Nov 1–14 / 1 total. Site says launch Aug 18, dev ends Oct 30 → treat Oct 30 as deadline. New site item: "Roots of the Data Prize" (teams based in the 14 data-collection countries).
- **Kit: 8 new commits pulled.** The big ones:
  - **Submission cap removed** — `max_submissions_per_participant: 20` deleted from config.yml; 1/day is the only limit (~70+ possible submissions). Discipline unchanged: local harness decides, leaderboard validates.
  - **`FINAL` → `TEST` rename; split now exact counts** (`n_train/n_dev/n_test`), roles assigned deterministically, **`data_fraction` removed** — phase 1 shows ALL TRAIN rows. Exact phase-1 scored cells: unicef 17,856 / wb 39,520 / unhcr 132,273. `sample_rows` signature changed again → runner.py updated, sandboxes regenerated, 11 tests pass.
  - **Real instrument metadata published in schema descriptions**: unicef v1.1 = Faith & Immunisation, 10 named countries, Q01 gated on country; unhcr v1.3 = Syrian refugees in Egypt/Iraq/Jordan/Lebanon, 2 CATI rounds (6,316+4,033) as independent cross-sections; wb = youth job-seekers, 3 countries. Gated counts: unicef 8, wb 19→40, unhcr 143→156.
  - **unhcr gates are approximate on real data** (agreement median 0.83, range 0.29–0.98; s3_11 branches overlap; 59 multi-select items sentinel-marked in round 2 only; `GATE_CORRECTIONS.md` referenced but missing from kit → forum question). Hard gate coupling unsafe on unhcr; sandbox can't show it. E002 caveat recorded; softened gating is the successor experiment.
- **Re-measured on updated kit** (seed 0, exact): marginal mean 0.2877; gated_marginal 0.3412 (Δ +0.0535; unicef +0.161, wb +0.052, unhcr +0.001). E001/E002 files updated.
- Minor: Codabench API reports docker python:3.12-slim vs kit 3.13-slim — flagged in notes, likely stale platform field.
- Next: E003 = soft/agreement-weighted gate coupling design (needs a way to estimate per-item gate agreement from visible rows); first leaderboard submission once E002 zip passes check_submission_zip + all three schemas.
- **Domain-study update (same day, later):** [[domain]] §9 added for the substantive (not just factual) shifts: (1) gates as estimated structure — empirical-Bayes agreement weighting as the E003 design note; (2) **UNHCR instrument identified as Enhanced RPIS** — the published RPIS series (rounds since 2017, 9th 2024, flash Feb 2025, ERPIS report Sept 2025 with matching fieldwork window) gives partner-published aggregate marginals for near-identical items = strongest offline prior for the largest instrument; must be disclosed as external data (FAQ 8); (3) `wave` is GIVEN → round-confounded sentinel rates are directly conditionable; (4) cap removal recalibrates the reusable-holdout budget note (~70 queries, noise floor binds). UNICEF exact source study and World Bank countries still to identify. Reading order extended (items 16–17).
- **Full repo re-audit against the 08-19 kit as standard (same day, later):** verified gate format uniform across all four schemas ({parent, observed_if}, single string parent, parents always precede children — gated_marginal structurally compatible); kit `score()` metric unchanged (skill formula identical; new `item_normalized`/`brier` outputs are diagnostics only); baselines and runtime section untouched by the kit update; `check_submission_zip` smoke schema moved to count-splits (no contract change). Fixed stale internals on our side: submissions/README (20-cap), E001 (08-19 numbers row), logloss.py verification note, domain.md (61k×150 briefing-era scale, "Rule 9/declared before phase 2" → models.txt/FAQ disclosure), method-4p.md ("Rule 7" numbering, hard-gate wording → softened-gate wording, unverified license claim → verify-against-terms). Official grader re-cross-checked on the updated kit: sample `PASS 0.3200` vs harness exact 0.3210 (noise-consistent). 11 tests pass. SIMULACRABENCH.md left as-is (historical briefing, marked outdated).

## 2026-08-17 — public launch, kit migration

- **Competition launched.** Old URLs dead (situatedevals.org/simulacrabench, `SituatedEvals/notebooks` both 404). New: site **simulacrabench.org**, kit repo **SituatedEvals/public**, leaderboard **codabench.org/competitions/17822**, contact **team@simulacrabench.org**. Cloned the new kit to `external/starter-kit/`; draft archived at `external/starter-kit-notebooks-archived/`.
- **Full diff draft → launch kit.** Structural change: no more `train/test.parquet` — one `respondents.parquet` with `role` ∈ TRAIN/DEV/FINAL assigned at build; phase 1 scores DEV, phase 2 scores FINAL with DEV turned visible; FINAL rows not shipped in phase 1. `load_frames`/`sample_rows` signatures changed accordingly.
- **Fact corrections vs our notes (CLAUDE.md + starter-kit-notes updated):**
  - Wall-clock budget is for the **whole run, all three instruments together** (900 s / 3600 s) — not per instrument.
  - Runtime: +8 CPUs, Python 3.13, `requirements.txt` now optional (large pre-install list incl. torch, transformers, and organizer lib `torch_measure`); HF models via `models.txt` fetched at image build.
  - Schemas: world_bank now 106 items/76 scored (was 82/73, cognitive items re-classed, numeric options now strings); unhcr 285/213/143 gated; sample rebuilt (12,000 rows, 11 items). Splits now train/dev/final fractions.
  - Submission cap 20 confirmed; phase 1 ends **Oct 30** (site); zip ≤ 1 GB; failures return sanitized `HSCC-*` codes only.
  - Sandbox `trait_scale` 0.6 → **2.0**: conditional models are now testable locally. All draft-era reference scores obsolete.
- New kit pieces: `FAQ.md`, `tools/check_submission_zip.py` (mirrors hosted ingestion), baselines `bundled_artifact` (bundled-CSV prior) and `external_model` (LLM prior + gate recursion + Dirichlet backoff; organizers warn it cannot beat marginal on the sandbox by construction), 6-language tutorials.
- **Harness re-verified on launch kit** (`runner.py` updated to the role API; 11 tests pass). Exact skills, seed 0, phase 1: marginal 0.3198/0.1486/0.2469/0.2988 (mean 0.2535); gated_marginal 0.3198/0.3267/0.2568/0.2988 (mean **0.3005**). Official `score.py` on sample: `PASS 0.3200 (27 s)` — matches. Gate-gain pattern shifted with the new sandbox: unicef +0.178, world_bank +0.010, sample/unhcr ±0 (parents PREDICT → falls back to marginal, consistent with the 08-12 structural conclusion).
- Next: register on Codabench (user action — site may go live with the Aug 17 UTC day), then first leaderboard submission = gated_marginal as pipeline validation candidate; start GIVEN-conditioning to unlock unhcr's 143 gates.
- **Workflow decided (same day, later):** experiment-tree recording adopted — one file per experiment in `docs/experiments/` with `parent:`/`status:` headers forming the tree, IDs in commit messages, fixed +0.005 adoption threshold, `scripts/render_tree.py` → `docs/tree.md` (mermaid). E001 (kit marginal, root) and E002 (gated marginal, +0.047, adopted) written retroactively. Daily push to private GitHub repo (`joon56/Simulacrabench-NeurIPS-2026-`).
- **Cleanup + domain refresh (same day, later):** deleted the archived pre-launch clone (`external/starter-kit-notebooks-archived/` — differences fully recorded in starter-kit-notes and this log). Added [[domain]] §8, the areas the launch kit made load-bearing: (1) prediction-powered inference — tutorial part 2 builds the PPI estimator explicitly, GIVEN block reframed as sampling-frame variables; (2) reusable-holdout/Ladder theory for the noised fixed-DEV leaderboard → submission-spending policy; (3) cognitive-test norm priors (Woods 2011 digit span, Kessels 2000 Corsi) for world_bank's re-classed raw-span items — real-world priors the sandbox cannot measure; (4) the `external_model` LLM-prior + Dirichlet-backoff recipe as the sanctioned LLM pattern (base measure worth ALPHA pseudo-respondents, not persona simulation); (5) `torch_measure` = Stanford AIMS PyTorch IRT lib (Rasch/2PL/3PL, GPU) pre-installed in the image — public docs suggest binary-only, verify polytomous support before designing around it.

## 2026-08-12

- **Experiment runner** (`src/eval/runner.py`): scores any `predict(frame, schema)` in-process with the kit's own modules — exact un-noised skill + wall-clock, all four schemas. Kit marginal baseline reproduces the noised scores exactly (0.1902/0.2468/0.3208).
- **Metric noise baseline** (10 phase-sampling seeds, crowd marginal): per-instrument skill std 0.002–0.004; 3-instrument-mean std **0.0016**. Decision rule: an improvement is real only if > +0.005 on the 3-instrument mean (~3σ). `sample` is ±0.06 (144 cells) — debugging only, never for judging.
- **Gate-aware marginal** (`src/models/gated_marginal.py`): per respondent, P(child=NA_GATED) = 1 − P(parent ∈ observed_if) using the respondent's own parent belief (one-hot if visible, predicted otherwise); substantive mass = P(asked) × asked-only conditional. Chain closure automatic (NA never in observed_if).
- Results vs plain marginal (seed 0, phase 1, exact skill):

  | Schema | marginal | gated | Δ | why |
  |---|---|---|---|---|
  | unicef | 0.1902 | 0.3653 | **+0.1751** | 5/7 gates have GIVEN parents → deterministic for test rows |
  | world_bank | 0.2468 | 0.2516 | +0.0048 (~3σ, borderline) | only 6/19 gates on GIVEN parents |
  | unhcr | 0.3208 | 0.3208 | +0.0000 | all 143 gates on PREDICT parents → parent belief falls back to crowd → algebraically identical to marginal |
  | 3-inst mean | 0.2526 | 0.3126 | **+0.0600** | |

- **Structural conclusion:** gate coupling is a *multiplier on parent predictability*. unhcr's 143 gates yield nothing until a model predicts parents respondent-specifically — which is exactly what GIVEN-conditioning (MRP-lite) and latent-factor models add. Their value estimates should include the unlocked gate cascade, not just their direct item gains.
- Caveat: sandbox gains transfer qualitatively (the gate mechanism is identical on real data), magnitudes don't (invented marginals; unicef's +0.175 depends on how often invented parents fall outside observed_if).

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
