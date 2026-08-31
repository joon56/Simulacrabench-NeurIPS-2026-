# 2026-09-01-E010 — conditional gate-agreement softening over E008

Experiment: E010 (adopted, real-data motivated per E003 precedent;
parent E008). Code: E008 submission main.py with `agreement_weights`
replaced by `conditional_agreement` (per gated item, agreement
conditioned on one data-selected GIVEN column, beta-binomial-shrunk to
the item scalar). No bundled artifacts, no requirements.txt. Zip:
`submissions/2026-09-01-E010.zip`, check_submission_zip OK.

## Local scores (2026-09-01, seed 0, phase 1)

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact (runner) | 0.4418 | 0.4994 | 0.4447 | 0.5532 | 0.4991 |
| E008 (LB 0.58) | 0.4418 | 0.4994 | 0.4447 | 0.5532 | 0.4991 |

**Identical to E008 by design** — sandbox gates are exact, so ã ≈ 1 and
conditioning never engages. Adoption evidence is the violation-sim pair
(E010 experiment file): group-dependent flips +0.0352 log over scalar ã
(sim group column = wave), uniform flips ±0.0000 (shrinkage no-loss).
Official score.py PASS ×3: 0.5000 / 0.4500 / 0.5500 (noised sandbox,
identical to E008 as designed). Tests 35/35.

## Leaderboard expectation (real data)

Reference: E008 LB = 0.58 (unicef 0.51 / wb 0.49 / unhcr 0.74).
Pre-registered 2026-09-01 BEFORE submission:

- **unicef and world_bank must stay flat** (0.51 / 0.49 ± noise): their
  gates are near-exact on real data; the change only engages where
  agreement is heterogeneous. A move > 0.02 on either ⇒ something
  unintended engaged — diagnose before trusting.
- **unhcr is the entire bet**: schema states agreement 0.29–0.98 with 59
  multi-select items sentinel-marked in round 2 only and wave GIVEN.
  If the mechanism is real, expected unhcr +0.01–0.03 (sim says +0.028
  skill under strong heterogeneity; real heterogeneity is strong for
  ~28% of cells, weaker elsewhere) → Grand ≈ 0.58–0.59.
- **unhcr flat (±0.01) does NOT falsify the mechanism** — it would mean
  E008's logistic soft path already absorbed most of the wave-dependent
  sentinel signal (wave is a logistic feature); in that case the scalar-ã
  headroom was already spent and E010 keeps it as insurance. unhcr DOWN
  > 0.02 ⇒ the conditional estimator overfit visible-row agreement —
  raise ALPHA for the conditional layer / revert to E008.
- No wall-clock concern: ~270 s local ≪ 900 s.

## Actual leaderboard result (2026-09-01)

**Grand 0.59 — unicef 0.51 / world_bank 0.49 / unhcr 0.77**
(E008: 0.51 / 0.49 / 0.74). Scorecard vs pre-registration — 4/4:

- unicef flat ✓ (0.51, unchanged) — no unintended engagement.
- world_bank flat ✓ (0.49, unchanged) — same.
- unhcr +0.03 ✓ — at the TOP of the pre-registered +0.01–0.03 band.
  The wave-heterogeneity thesis is confirmed on real data: the
  conditional-ã layer found real agreement structure the scalar pooled
  away, and E008's logistic soft path had NOT already absorbed it.
- Grand in the 0.58–0.59 band ✓.

Interpretation: a locally-invisible structural change (clean sandbox
identical to E008) moved the leaderboard +0.01 Grand purely on
domain-anchored evidence — the E003-precedent adoption path is now
validated twice. unhcr 0.77 with U = 1.2618: remaining unhcr headroom is
thinner; unicef (0.51, U 1.5620) and wb (0.49, U 2.0184, 39.5k cells)
are now the widest gaps to perfect.
