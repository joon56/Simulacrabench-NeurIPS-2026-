# Starter kit notes (internal domain knowledge)

Distilled from `external/starter-kit/` (pre-launch draft, pushed 2026-08-10) —
README, tutorial.ipynb, score.py, config.yml, and repo commit history.
Re-verify after the Aug 17 launch pull.

## The submission contract, exactly

- `predict(frame, schema)` — pure function, no I/O. `frame`: `respondent_id`
  + one column per non-EXCLUDE item; training respondents complete on top,
  held-out respondents below with every PREDICT cell NaN.
- Return one probability vector per NaN cell: rows top-to-bottom, items in
  `schema["items"]` key order (not frame column order).
- Vector length = `len(values)` + 1 extra final slot for `schema["gated_value"]`
  (`NA_GATED`) if the item is gated. Option order from the schema, never from
  observed data.
- No zeros, no negatives, sum to 1. Grader floors at 1e-3 by flat-mixing anyway.

## Skip logic is deterministic structure, not statistics

The gate rule: an item is asked iff its parent's answer is in
`gate.observed_if`. Consequences:

- Within a held-out respondent, predicted cells are **coupled**: coherent
  predictions satisfy P(child = NA_GATED) = 1 − P(parent ∈ observed_if).
  The marginal baseline ignores this; enforcing it is the first and largest
  gain (an earlier tutorial draft measured the skip-logic step at
  log score 0.98 → 0.76, bigger than any modelling step after it).
- Gate chains exist (sample: would_return ← clinic_wait ← visited_clinic,
  two deep; unhcr has 142 gated items of 230). Chain-closure: parent
  NA_GATED ⇒ child NA_GATED.
- Tutorial wording: "a gated item's answer is determined whenever its parent
  is visible" — on training rows the gate is data-consistent by construction.

## Reference numbers (sandbox, seed 0, phase 1)

| Schema | crowd-marginal skill | notes |
|---|---|---|
| sample | 0.4709 exact (0.45 noised) | U = 1.3144 nats, 144 cells |
| unicef | 0.19 noised | 18,348 cells, 12 scored items |
| world_bank | 0.25 noised | 36,208 cells, 73 scored items |
| unhcr | 0.32 noised | 132,060 cells, 213 scored items |

Sandbox marginals/dependencies are invented (Dirichlet α=0.9, one latent trait
per respondent, loading scale 0.6 — see `config.yml sandbox:`). Model tuned on
sandbox will not transfer; only pipeline behaviour and structural handling do.

## Modelling lessons recorded by the organizers (commit history, 8/5 draft)

- Naive Bayes on the GIVEN block **underperformed** simpler conditioning in
  their runs: one latent trait drives many answers, so conditionally-
  independent evidence gets double-counted — overconfidence, which log score
  punishes. Shrink/temper any multi-feature conditioning.
- Conditioning on a GIVEN feature whose training support is empty must fall
  back to the crowd marginal (their M3 = M2 to four decimals when the
  conditioning cells contributed no data).
- Hedging: floored log score means a confidently wrong cell costs log(1e-3)
  ≈ −6.9 vs ≈ −1.4 for an honest four-option hedge. Sharpness only after
  calibration.

## Draft-status warnings

- Rules v0.8 (not in repo, referenced in commits): dev phase "92 submissions"
  vs `config.yml max_submissions_per_participant: 20` — unresolved.
- Contact address inconsistency: neurips-un-benchmark@stanford.edu vs
  h4upt@stanford.edu.
- Commit history shows schema key naming drift (`role` vs `class`) across
  drafts — pin to whatever ships on Aug 17.
