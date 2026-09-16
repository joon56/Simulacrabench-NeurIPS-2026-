# 2026-09-19-E038 — respondent-id structure as matching signature, over E025

Experiment: E038 (adopted, E003 route; parent E025). Code: the E025
assembly with signature columns derived from `respondent_id` (string
tokens, truncated digit runs, numeric-rank blocks), weighted by the
Fellegi–Sunter step from the GIVEN-only provisional pairs, with an
evidence guard (≥ 5 observed agreements) and a separate λ bucket for
matches confirmed by an armed id column. Zip:
`submissions/2026-09-19-E038.zip`, check_submission_zip OK.

## Local scores (2026-09-19, seed 0, phase 1)

| | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|
| exact (runner) | 0.5006 | 0.4548 | 0.5630 | 0.5061 |
| E025 (LB 0.63 / unhcr 0.89) | 0.5006 | 0.4548 | 0.5629 | 0.5061 |

Sequential ids (sandbox): derived-column weights ≤ 0.37 (GIVEN max
4.84), household sim −0.0004 vs E025. **Keyed-id recall sim** (twin id =
source id + "-2", half the twins' household columns scrambled so GIVEN
alone cannot find them): key column weight 7.87 > GIVEN max 4.56,
**+0.0108 log** over E025. Parity assembled vs src exact (unhcr 0.562963 both).
Official score.py PASS ×3: 0.5000 / 0.4600 / 0.5600 (= E025 within grader
noise). Runtime ≈ E025 (+ ~10 signature columns in the
kernel). Phase-2 hardening done in advance: `score.py --phase 2` PASS ×3
= 0.4902 / 0.4620 / 0.5652 (= E025; sandbox ids are sequential).

## Leaderboard expectation (real data)

Reference: E025 LB = 0.63 (0.52 / 0.49 / 0.89). Pre-registered
2026-09-19 BEFORE submission. Five teams sit at unhcr 0.93 with
identical unicef/wb; our map puts E025 at base 0.79 + evidence 0.10, so
their +0.04 is most plausibly twin recall — and the identifier is the
one column the evidence layer never used.

- **Grand ≥ 0.64 (unhcr ≥ 0.91, best updates, per-instrument visible)**
  ⇒ the real identifier / row order carries household structure; the
  missing recall is found. Next: retune MIN_AGREE / blocks, add the
  E029 ensemble as ride-along, and write the disclosure paragraph.
- **Grand 0.63, no update** ⇒ identifiers are opaque (or roles were
  assigned so that twins are not visible); the 0.93 cluster comes from
  something else. Park; remaining levers are unknown to us.
- **Grand ≤ 0.62** ⇒ a derived column armed on a spurious regularity
  (e.g. id order correlated with interview batch) and hurt the
  concentrated bucket — raise MIN_AGREE, drop the block columns, retest.
- unicef / wb: identifiers sequential there too ⇒ flat.

## Actual leaderboard result

(pending)
