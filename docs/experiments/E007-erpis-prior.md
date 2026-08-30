# E007 — eRPIS published-marginal prior blend (unhcr)
parent: E006
status: parked
date: 2026-08-30

## Hypothesis

Blending the A003 CSV (`data/priors/erpis_2025.csv`, eRPIS Sep-2025
published marginals mapped onto unhcr item names) into the E006 tables as
Dirichlet base measures improves unhcr skill, because the report covers
the same population and fieldwork window as both competition rounds
(A002 finding 1).

## Why parked (quantitative, 2026-08-30, before any implementation)

The prior enters as W pseudo-counts against the empirical count n of the
same cell. Phase 1 exposes ALL 8,279 unhcr TRAIN rows complete — the
country×wave cells the CSV addresses hold n ≈ 1,000–2,000 real answers
each. The posterior shift is ‖shift‖ ≈ W/(n+W)·‖prior − empirical‖:

- Even at an aggressive W = 200, W/(n+W) ≤ 0.17.
- TRAIN and DEV roles are assigned from one deterministic build of the
  same survey — same distribution, so the empirical table is already an
  unbiased estimate of the DEV target and ‖prior − empirical‖ has no
  systematic sign. Expected skill gain ≈ 0; risk is symmetric noise plus
  transcription/mapping error (14 of 49 rows are derived or mapped-medium).
- The one place a prior beats data is empty/thin cells — but the ladder's
  κ-backoff (E006) already fills those from the parent level, which is
  itself estimated from thousands of real rows rather than a PDF table.

This is the mirror image of the `bundled_artifact` baseline situation:
bundled priors pay when visible data are scarce; phase 1 is data-rich.

## Revive conditions

- Leaderboard evidence of unhcr country-cell miscalibration that the
  visible rows cannot explain, or
- any future phase/rule change that shrinks the visible unhcr rows, or
- microdata-scale priors (WGM 2018 for unicef — free CC-BY microdata,
  A001) where the prior is per-respondent conditional, not marginal —
  that variant would be a NEW experiment (logistic prior features), not
  this pseudo-count blend.

## Decision

**Parked without implementation.** Expected Δ ≈ 0 by the argument above;
rule 5 (complexity must pay rent) blocks spending model complexity and a
leaderboard slot on it. The A003 CSV keeps its value as a validation
anchor: E008+ models should reproduce s3_11 per-country tables within
sampling error — a standing sanity check, not a model input.
