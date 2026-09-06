# E022 — composition: household weights ∘ sharpened λ (E021 ∘ E019)
parent: E021
status: adopted
date: 2026-09-07

## Hypothesis

E019 (λ ceiling 0.98 + posterior-concentration buckets) and E021
(data-estimated household-aware signature weights) each measure
+0.005–0.010 log on the household sim across perturbation regimes —
real, but below what the phase-1 leaderboard can resolve (0.01
rounding + ±0.01–0.02 noise), which is why E019 read as "flat".
Composed, they should exceed the resolution floor: learned weights
concentrate the posterior on true co-respondents, which is exactly
the regime the concentration bucket then rewards with a high λ.

## Domain check

Pre-registered 2026-09-07 BEFORE implementation.

- (a) Technical: the two changes touch different stages (matching
  weights vs mixing weights) and are individually replay-calibrated;
  composition risk is the interaction "sharper posteriors ⇒ more rows
  in the concentrated bucket ⇒ λ up to 0.98 on household matches whose
  per-item copy rate is < 1" — but λ per (item, bucket) is still chosen
  by the replay on visible rows, so a bucket that over-trusts would be
  measured and tuned down. Inertness on duplicate-free data is
  inherited from both parents.
- (b) Background: as E021 — household composition is the shared block,
  person-level fields differ; per-item copy rates vary (facts high,
  attitudes low).
- (c) Local evidence plan: household sim, ρ ∈ [0.2, 0.8] (the harder
  regime): E022 > max(E019, E021) by ≥ +0.003 and > E018 by ≥ +0.010
  log; clean runner within ±0.002 of E018; runtime ≤ ~150 s local.
  Leaderboard readings: unhcr ≥ +0.02 ⇒ the tuning family is real and
  stackable, keep composing; +0.01 ⇒ consistent with sims, one repeat
  before more slots; flat ⇒ the layer-tuning line is closed for phase
  1 (below resolution) and effort moves to structural axes.

## Change

`src/models/hh_sharp.py` (planned): link_sharp's layer with E021's
weight-estimation pass inserted between the rarity pass and the
calibration replay; link_sharp.predict gains a `layer_fn` hook.

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

Hard household sim (ρ ~ U(0.2, 0.8)): E018 −0.5750 | E019 +0.0053 |
E021 +0.0068 | **E022 +0.0116** — near-additive, > both parents by
≈ +0.005 and > E018 by > +0.010 as pre-registered. Clean sandbox:
0.4429 / 0.5006 / 0.4549 / 0.5627 (unhcr +0.0001 vs E018, in bound).
Runtime 154 s local after the perf pass (worst-case ~620 s hosted at
4×). Tests: composition test 1/1 (+ E021's 3/3).

## Decision

**Adopted (E003 route on the household sim).** Submission
`submissions/2026-09-08-E022/`. Readings pre-registered in SCORES.md;
the family's next step depends on whether the composition clears the
leaderboard's resolution floor.
