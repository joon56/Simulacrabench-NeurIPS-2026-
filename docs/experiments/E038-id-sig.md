# E038 — respondent-id structure as matching signature
parent: E025
status: adopted
date: 2026-09-18

## Hypothesis

Five teams sit at unhcr 0.93 with identical unicef/wb scores; our
probe map puts E025 at base 0.79 + evidence 0.10, so the +0.04 gap is
most plausibly evidence recall. The one column the evidence layer never
looked at is `respondent_id`: the sandbox generates a plain sequence,
but a real survey file commonly embeds a household key, a round tag or
a member suffix in the identifier and is ordered household by household.
Deriving signature columns from the identifier (string tokens,
truncated digit runs, numeric-rank blocks) and letting the E021
Fellegi–Sunter step weight them from the GIVEN-only provisional pairs
turns any such structure into near-deterministic twin recall; with no
structure every derived column gets weight 0 and E025 is unchanged.

## Domain check

Pre-registered 2026-09-18 BEFORE the runs. (a) technical: derived
columns enter only after the E025 pass-1 pairs exist; their weight is
log(m/u) − log((1−m)/(1−u)) clipped at 0, so chance-level agreement
(m ≈ u) is inert; the sandbox (R000001…, roles in id order) must give
E025 exactly. (b) background: organizer ruling 2026-09-02 permits
matching rows within a dataset; this uses no external data and
re-identifies nobody — but identifier structure is a data-collection
artifact, not survey content, so the result is filed as "matching
recall via identifiers", disclosed in the method description. ERPIS
CATI files are built from household rosters (one household id, member
lines) — a key in the identifier is the norm for such files. (c)
readings: clean sandbox and plain household sim within ±0.002 of E025;
keyed-id sim (twin id = source id + suffix) > +0.01 and the key column
outweighs every GIVEN column. Leaderboard: unhcr ≥ 0.92 (Grand 0.64+)
⇒ the identifier carries household structure — the missing recall;
0.63 flat ⇒ identifiers are opaque on the real file; the 0.93 cluster
comes from something else.

## Change

`src/models/id_sig.py` (`id_columns`, `_sig_data_ext`, `id_sharp_layer`,
`predict`); `tests/test_id_sig.py` (derivation, sequential-id parity,
keyed-id gain).

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

Attempt log.
- v1: derived columns weighted by the plain E021 estimator — Laplace
  smoothing gave near-unique columns (id_tok_1, rank//2) spurious
  weights of 1.2–2.8 on the sandbox (zero observed agreements, smoothed
  m > u). Clean sandbox still within ±0.0001, but the mechanism was
  wrong. v2 adds an evidence guard: a derived column keeps weight only
  with ≥ 5 observed agreements among the provisional pairs.
- v2 on the keyed-id sim (all twins keyed, GIVEN intact): key armed
  (8.68) but **−0.0044** — the sim had no recall problem (E025 already
  finds twins by roster + governorate), and keyed matches pushed the
  pooled concentrated-bucket λ up for GIVEN-only matches too.
- v3: a third λ bucket for "concentrated AND top candidate agrees on an
  armed id column"; keyed sim redesigned as a recall problem (half the
  twins' household columns scrambled, the other half discoverable so
  the key can be learned): key weight 7.87 > GIVEN max 4.56,
  **+0.0108 log** over E025. Sequential-id sim (plain household sim)
  −0.0004; derived weights ≤ 0.37.

Clean sandbox and assembled-file parity: SCORES.md.

## Decision

**Adopted (E003 route)** — inert on sequential identifiers (clean
sandbox, household sim), +0.0108 where the identifier carries the
household key that GIVEN cannot recover. Real-data A/B:
`submissions/2026-09-19-E038/`; readings pre-registered there (≥ 0.64
⇒ identifier structure real; 0.63 ⇒ opaque, park; ≤ 0.62 ⇒ spurious
regularity, raise the guard). Disclosure: identifier-derived matching
is listed in the method description as "within-dataset row matching
using the record identifier" (organizer-permitted 2026-09-02).
