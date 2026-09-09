# E028 — parent-value-conditional gate decoding (joint branches)
parent: E025
status: adopted
date: 2026-09-10

## Hypothesis

The gate math since E003/E010 is
  belief = a·[P(asked)·cond + (1−P(asked))·sentinel] + (1−a)·soft,
with a single softening weight a per item (optionally per one GIVEN
column). It never looks at WHICH parent value the respondent holds
beyond asked/not-asked. On unhcr the s3_11 return-intention parent has
three single-value branches (Yes 21 / No 40 / DK 11 children) that
"overlap in the file": some No-respondents answer Yes-branch items, and
their answers need not look like the Yes-respondents'. Decoding each
gated child as
  belief = Σ_v b_parent[v] · T_v,   T_v = (1−r_v)·A_v + r_v·sentinel,
with r_v = sentinel rate given parent=v (shrunk; further conditioned on
E010's selected column, e.g. wave) and A_v = the answer distribution
given parent=v (GIVEN-conditioned net/ladder blend for asked values;
empirical κ-smoothed table for non-asked values) replaces the three
ad-hoc pieces (hard/soft/agreement) with one data-estimated table per
parent value. On exact gates it reduces to the hard gate exactly.

## Domain check

Pre-registered 2026-09-10 BEFORE implementation. (a) all quantities are
count tables over visible rows with κ/α shrinkage; per-(item, parent
value, column value) cells hold hundreds to thousands of rows on unhcr.
Exact gates ⇒ r_v ∈ {0, 1} ⇒ identical to the current hard gate (the
sandbox no-regression channel). (b) branch overlap is documented by the
organizers (schema note); CATI practice — interviewers ask return
questions regardless of the stated 12-month intention in some scripts —
makes the No→Yes-branch overlap the expected direction, with answers
that differ from committed returnees'. (c) local: (1) clean runner
within ±0.002 of E025; (2) branch-overlap sim — a fraction of
round-2 No/DK respondents answer Yes-branch children from a distinct
skewed distribution — E028 > E025 by > +0.005 log; E003-route
adoption. Leaderboard readings: unhcr up ⇒ overlap structure real;
flat ⇒ E010's conditional agreement already captured it.

## Change

`src/models/pvc_gate.py`: copy of the link_sharp pipeline with the
gated branch replaced by the parent-value-conditional decode; tables
built per gated item from complete visible rows.

## Result

Attempt log: v1 shrank r_v toward the item's pooled sentinel rate —
clean sandbox leaked ~0.5% sentinel mass on asked rows (wb −0.0010).
v2 shrinks toward the hard-gate prior (0 asked / 1 not asked): clean
sandbox **identical to E025** (0.5006 / 0.4548 / 0.5629), exact gates
reproduce the hard gate (unit-tested: r ≈ 0 asked, ≈ 1 not asked).

Branch-overlap sims (Yes-branch children of s3_11 answered by
non-Yes respondents from a skewed distribution): light regime (30% of
round-2 No) **+0.0017**; heavy regime (70% of No+DK, both waves —
inside the schema's documented agreement range 0.29–0.98)
**+0.0121 log** over E025. The gain scales with overlap magnitude;
the real magnitude is what the leaderboard reads. Tests 2/2.

## Decision

**Adopted (E003 route).** Exact no-regression + a schema-anchored sim
gain above threshold in the documented overlap regime. Submission
`submissions/2026-09-12-E028/` (queued after E027 for attribution).
Readings: unhcr up ⇒ real overlap is heavy and E010's scalar/column
agreement was leaving the No/DK-branch answer distributions on the
table; flat ⇒ real overlap is light or E010 already captured it.
