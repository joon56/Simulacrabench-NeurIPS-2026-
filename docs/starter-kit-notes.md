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

`respondents.parquet` + `role` column, assigned once at dataset build,
never redrawn. Since the 2026-08-19 kit update roles are **counts, not
fractions** (`n_train`/`n_dev`/`n_test`, summing to `n_rows`; sandbox
assigns them deterministically: first `n_train` rows TRAIN, etc.), the
`FINAL` role is renamed **`TEST`**, and **nothing is subsampled** —
`data_fraction` is gone; a phase takes every row of every role it is
entitled to.

| Role | Phase 1 | Phase 2 |
|---|---|---|
| `TRAIN` | visible, answers included | visible, answers included |
| `DEV` | GIVEN only, PREDICT scored | visible, answers included |
| `TEST` | **not shipped** | GIVEN only, PREDICT scored |

Whole respondents go one way (cell-splitting would leak gated parents via
visible children).

## Instrument shapes (schemas as of 2026-08-19)

| Schema | rows | items | GIVEN | PREDICT | EXCLUDE | gated | n_train/n_dev/n_test | phase-1 cells |
|---|---|---|---|---|---|---|---|---|
| sample (v2.0) | 12,000 | 11 | 6 | 4 | 1 | 2 | 8,000/1,900/2,100 | 7,600 |
| unicef (v1.1) | 19,846 | 19 | 7 | 12 | 0 | 8 | 14,885/1,488/3,473 | 17,856 |
| world_bank (v1.0) | 6,927 | 106 | 9 | 76 | 21 | 40 | 5,195/520/1,212 | 39,520 |
| unhcr (v1.3) | 10,349 | 285 | 17 | 213 | 55 | 156 | 8,279/621/1,449 | 132,273 |

Phase-1 scored cell counts are now exact (`n_dev` × PREDICT items). Phase 2:
`n_test` × PREDICT = 41,676 / 92,112 / 308,637.

**Schema `description` fields now carry real instrument metadata** (added
2026-08-19 — read them as modelling input): unicef = Faith & Immunisation
COVID/childhood-vaccination survey, 10 named countries, Q01 age gated on
country (not fielded in Egypt); unhcr = ERPIS, Syrian refugee households in
Egypt/Iraq/Jordan/Lebanon (46 governorates, origins in 15 Syrian
governorates), two CATI rounds (6,316 + 4,033 rows) treated as independent
cross-sections, fieldwork May–June 2025, ages/counts/years cut into closed
bands; world_bank = youth job-seeker skills assessment, 3 countries.

## Real-data gating is APPROXIMATE (unhcr) — the big modelling warning

From the unhcr v1.3 description, verbatim facts:

- "Gates state the instrument's routing… They are **not a constraint the
  delivered rows satisfy**: agreement between a gate and who actually holds
  a value has a **median of 0.83 and ranges from 0.29 to 0.98**."
- The three return-intention branches off `s3_11` (return / not-return /
  undecided, s7a/s7b/s7c) are mutually exclusive in the instrument but
  **overlap in the file**.
- Five gates approximate conditions the one-parent `{parent, observed_if}`
  format cannot express (disjunctions); one is inferred from skip rates.
  All six are "set out in `GATE_CORRECTIONS.md`" — **file not present in
  the kit** (forum question).
- Five multi-select families (6.4, 6.6, 6.11, 7A.7, 7B.1 — 59 items):
  round 1 wrote `0` for skipped respondents, so the sentinel appears on
  round-2 rows only → sentinel rate is confounded with round membership.
- 156 of 230 GIVEN+PREDICT items carry the sentinel somewhere; the rest
  never do.

Consequence: **hard gate coupling (P(child=NA_GATED) = 1 − P(parent asked),
enforced with probability 1) is unsafe on real unhcr** — a gate-violating
cell costs log(1e-3). The coupling must be softened toward observed
per-item sentinel rates (e.g. mixture weight = per-item gate agreement
estimated from visible rows). The sandbox generator still enforces gates
exactly, so the local harness CANNOT measure this failure mode — sandbox
gate gains are an upper bound for unhcr.

unicef/world_bank descriptions state routing without an agreement caveat —
treat their gates as clean until visible real data says otherwise.

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

## Reference numbers (2026-08-19 kit, seed 0, phase 1, local harness exact skill)

| Schema | marginal_counts | gated_marginal (ours) | cells |
|---|---|---|---|
| sample | 0.3210 | 0.3210 | 7,600 |
| unicef | 0.1623 | 0.3232 | 17,856 |
| world_bank | 0.2387 | 0.2909 | 39,520 |
| unhcr | 0.4287 | 0.4297 | 132,273 |
| **mean** | **0.2877** | **0.3412** | |

Gate-gain pattern on the updated schemas: unicef +0.161, world_bank +0.052
(gated items went 19 → 40, more with GIVEN parents), unhcr +0.001 (gates
sit on PREDICT parents → falls back to crowd → nearly identical). All
numbers moved vs 08-17 (roles now deterministic counts, schemas updated) —
earlier tables are obsolete. Official `score.py` cross-check on the 08-17
kit gave `PASS 0.3200` vs harness 0.3198 on sample; harness mirrors the
kit's own functions, so no re-check needed per kit pull.

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

## Open/resolved questions ledger

- Submission cap: launch config said 20 total; **removed 2026-08-18** —
  now 1/day only (Codabench phase config agrees).
- Contact: **team@simulacrabench.org** (both stanford.edu addresses gone).
- Site moved to **simulacrabench.org**; kit repo moved from `notebooks` to
  `public`. Leaderboard: codabench.org/competitions/17822 (registration
  auto-approve; columns: Grand Prize + per-instrument skills).
- Schema key naming settled on `class` (`GIVEN`/`PREDICT`/`EXCLUDE`) and
  `role` (`TRAIN`/`DEV`/`TEST` — `FINAL` renamed 08-19).
- Phase 1 end: site says **Oct 30**, Codabench phase config **Oct 31** —
  treat Oct 30 as the deadline.
- Codabench API lists `docker_image: python:3.12-slim` vs kit config
  `python:3.13-slim` — likely a stale Codabench field; kit README says the
  hosted image is Python 3.13. Watch for a `HSCC-BUILD-*` surprise.
- **`GATE_CORRECTIONS.md` referenced by unhcr v1.3 but absent from the
  kit** — forum question before building unhcr gate softening.
