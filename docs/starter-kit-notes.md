# Starter kit notes (internal domain knowledge)

Distilled from `external/starter-kit/` — the **launch release** of
<https://github.com/SituatedEvals/public>, cloned and verified 2026-08-17
(the pre-launch `notebooks` draft clone has been deleted; its differences
are recorded here and in [[log]]). Literature backing the modelling
choices referenced here lives in [[domain]]; day-by-day findings in [[log]].

## The submission contract, exactly

- `predict(frame, schema)` — called **once per instrument**; pure, no I/O.
  `frame`: `respondent_id` + one column per non-EXCLUDE item; visible
  respondents complete, held-out respondents with every PREDICT cell NaN.
- Return one probability vector per NaN cell: rows top-to-bottom, items in
  `schema["items"]` key order (not frame column order).
- Vector length = `len(values)`, **plus one final sentinel slot
  (`schema["gated_value"]` = `NA_GATED`) only if the item is gated**
  (`options_for` in `make_sandbox.py` is the single definition of option
  order). Option order from the schema, never from observed data.
- Finite, non-negative, sum > 0 per vector; grader renormalizes and
  flat-mixes at floor 1e-3, so no self-flooring needed.
- Load fitted state at **module import** (runs once at container start,
  inside the wall-clock budget); `predict()` per-call work is ×3.

## Delivered data = one file with roles

`respondents.parquet` + `role` column, assigned once at dataset build
(`assign_roles`, schema `split` fractions), never redrawn:

| Role | Phase 1 | Phase 2 | split fraction (unicef/wb = .75/.075/.175, unhcr = .8/.06/.14) |
|---|---|---|---|
| `TRAIN` | visible | visible | `train_fraction` |
| `DEV` | masked, scored | visible with answers | `dev_fraction` |
| `FINAL` | **not shipped** | masked, scored | `final_fraction` |

Phase 1 `data_fraction` 0.30 thins the *visible* rows only — the scored
cells are identical for every submission in a phase, so leaderboard entries
are directly comparable. Whole respondents go one way (cell-splitting would
leak gated parents via visible children).

## Instrument shapes (launch schemas, v1.0)

| Schema | rows | items | GIVEN | PREDICT | EXCLUDE | gated |
|---|---|---|---|---|---|---|
| sample (v2.0) | 12,000 | 11 | 6 | 4 | 1 | 2 |
| unicef | 19,847 | 19 | 7 | 12 | 0 | 7 |
| world_bank | 6,927 | 106 | 9 | 76 | 21 | 19 |
| unhcr | 10,349 | 285 | 17 | 213 | 55 | 143 |

Changes vs the draft: sample grew 400 → 12,000 rows and 7 → 11 items (GIVEN
block now deliberately "the cheap half of a questionnaire" — frame/roster
variables); world_bank re-classed several cognitive items PREDICT↔EXCLUDE
and re-binned spans (76 scored now, was 73); unhcr unchanged in scored count
(213) but 143 gated (was 142); all numeric option values are now strings
("1"…"5"), and `split` gained `dev_fraction`/`final_fraction`.

## Skip logic is deterministic structure, not statistics

The gate rule: an item is asked iff its parent's answer is in
`gate.observed_if`. Consequences:

- Within a held-out respondent, predicted cells are **coupled**: coherent
  predictions satisfy P(child = NA_GATED) = 1 − P(parent ∈ observed_if).
  The marginal baseline ignores this; enforcing it is the first structural
  gain (an earlier tutorial draft measured the skip-logic step at
  log score 0.98 → 0.76, bigger than any modelling step after it).
- Gate chains exist (sample two deep; unhcr has 143 gated of 285).
  Chain-closure: parent NA_GATED ⇒ child NA_GATED.
- "A gated item's answer is determined whenever its parent is visible" — on
  visible rows the gate is data-consistent by construction.
- **Where the gain lives:** the per-respondent coupling beats the pooled
  marginal only when the parent is *visible* for held-out rows (parent GIVEN,
  or already predicted sharply). If the parent is itself a blanked PREDICT
  item, everyone gets the same parent belief and gate-aware ≈ plain marginal
  (measured 2026-08-17: unicef +0.18 skill, unhcr/sample ±0.000).

## Reference numbers (launch sandbox, seed 0, phase 1, local harness exact skill)

| Schema | marginal_counts | gated_marginal (ours) | bundled_artifact | cells |
|---|---|---|---|---|
| sample | 0.3198 | 0.3198 | 0.3195 | 3,628 |
| unicef | 0.1486 | 0.3267 | 0.1486 | 17,868 |
| world_bank | 0.2469 | 0.2568 | 0.2469 | 40,508 |
| unhcr | 0.2988 | 0.2988 | 0.2988 | 132,699 |
| **mean** | **0.2535** | **0.3005** | 0.2534 | |

Official `score.py` on sample, phase 1: `PASS 0.3200 (27 s)` — matches the
harness to noise. (Draft-era reference numbers are obsolete: sandbox
`trait_scale` went 0.6 → 2.0, so all draft scores moved.)

Sandbox marginals/dependencies are invented (Dirichlet α=0.9, one latent
trait per respondent, loading scale **2.0** since launch — strong enough to
test conditional models locally, which the 0.6 draft was not). Content still
does not transfer; structure and pipeline behaviour do. An LLM
world-knowledge prior is by construction uninformative on the sandbox
(organizers' warning in `baseline/external_model/main.py`).

## The hosted runtime

- 1× H100, 16 GB RAM (hard limit), 8 CPUs, Python 3.13, no network.
- Budget covers the **whole run** (import + model load + all three
  instruments): 900 s phase 1, 3600 s phase 2.
- Pre-installed: numpy pandas pyarrow scipy scikit-learn torch torchvision
  Pillow transformers sentence-transformers tokenizers sentencepiece
  tiktoken huggingface_hub accelerate safetensors bitsandbytes autoawq
  protobuf **torch_measure** (organizer latent-trait/IRT lib).
- `requirements.txt` optional, pinned-exact only, installed at image build
  (off the clock, own ceiling → `HSCC-BUILD-002`).
- `models.txt`: HF repo ids, `snapshot_download`ed into the image cache at
  build; `from_pretrained()` works offline at runtime.
- Zip ≤ 1 GB, `main.py` at archive root, no nested zip;
  `tools/check_submission_zip.py` mirrors hosted ingestion checks.
- Failures return sanitized `HSCC-*` codes only (families: ZIP, ARTIFACT,
  IMPORT/DEPS, HF-CACHE, BUILD, NETWORK, PREDICT, SCORING,
  TIMEOUT/CONTAINER, INFRA, UNKNOWN). Exception *type* survives, message and
  traceback do not. Debug locally.

## Modelling lessons recorded by the organizers

- Naive Bayes on the GIVEN block **underperformed** simpler conditioning in
  their runs: one latent trait drives many answers, so conditionally-
  independent evidence gets double-counted — overconfidence, which log score
  punishes. Shrink/temper any multi-feature conditioning.
- Conditioning on a GIVEN feature whose training support is empty must fall
  back to the crowd marginal.
- Hedging: floored log score means a confidently wrong cell costs log(1e-3)
  ≈ −6.9 vs ≈ −1.4 for an honest four-option hedge. Sharpness only after
  calibration.
- `baseline/external_model` shows the organizer-sanctioned LLM recipe: gate
  recursion first, then Dirichlet backoff (stratum counts → coarser counts →
  LLM next-token prior over option text), ALPHA in units of respondents so
  data drowns a bad prior.

## Draft-era open questions — resolved at launch

- Submission cap: **20 total** stands (config.yml); the "92 submissions"
  rules-doc number is gone.
- Contact: **team@simulacrabench.org** (both stanford.edu addresses gone).
- Site moved to **simulacrabench.org**; kit repo moved from `notebooks` to
  `public`. Leaderboard: codabench.org/competitions/17822.
- Schema key naming settled on `class` (`GIVEN`/`PREDICT`/`EXCLUDE`) and
  `role` (`TRAIN`/`DEV`/`FINAL`).
- Phase 1 window per site: Aug 17 – **Oct 30** (draft said Oct 31).
