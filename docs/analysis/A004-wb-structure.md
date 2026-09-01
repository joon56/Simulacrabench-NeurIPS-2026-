# A004 — world_bank structural pass (schema-level, locally readable)
date-started: 2026-09-02
status: done (v1)
relates-to: A002, E011 (planned ordinal smoothing)

## Goal

wb is the lowest instrument (LB 0.49, four submissions with zero
wb-specific work) with the highest U (2.0184 = most skill per log-point).
Read everything real the kit exposes locally about wb — the schema
(shapes, gates, descriptions are real; only the sandbox DATA is
invented) — and find the structural lever.

## Attempt log (chronological, append-only)

### v1 — 2026-09-02: full schema inventory

- **Class counts correct our notes**: 106 items = 76 PREDICT + 9 GIVEN +
  21 EXCLUDE. Earlier "30 GIVEN" was wrong — 21 of the non-PREDICT items
  are EXCLUDE (raw duplicates of banded scores, tracer pay details).
  The wb logistic sees only 9 GIVEN columns (group, age, gender,
  country, educationLevel, hadJob, employmentStatus,
  wageOfSimilarEmployees, lowestAcceptablePay) — the "many weak
  predictors" story from E008's open claim was mis-premised: wb's GIVEN
  block is SMALL, not wide. (unicef 7, unhcr 72.)
- **Gates are near-exhausted as a lever**: 30 gated non-EXCLUDE items =
  27 GIVEN-parented (19 on `group` — the tracer/feedback arms — all
  deterministic for held-out rows) + only 3 PREDICT-parented
  (tr_job_number & tr_feel_work ← tr_job_full; howManyHoursToUpskill ←
  accessedLearningLinks). No unhcr-style cascade to unlock.
- **The real wb lever is the option axis**: 24 PREDICT items have
  fully-numeric option sets — digit-span/Corsi raw spans (K=15,
  values '0','2'..'15'), search-hours / applications counts (K=12–13,
  '0'..'11'), a numeric feel-work scale (K=12, '2.125'..'). High K +
  thin conditional cells + nothing in the current stack pools strength
  across ADJACENT options: the ladder pools across cells, the logistic
  across respondents, but a count of 7 says nothing about 6 or 8 in any
  current component. K=24/25 sector items are nominal, not ordinal —
  excluded from this lever.
- **Sandbox cannot show ordinal gains BY CONSTRUCTION**:
  make_sandbox.py couples trait to options via
  `np.outer(trait, rng.normal(size=K))` — random per-option loadings,
  no order structure. Same situation as E010's exact gates → same
  adoption route (runtime data-driven engagement + degeneration
  guarantee + synthetic-structure sim as the positive evidence).
- Tracer subsample numbers in the real description (1,229 feedback arm,
  471 tracer) match the `group` gate structure — background-consistent.

## Findings

1. wb-specific headroom is concentrated in ordinal-option items
   (24/76 PREDICT), not in gating (exhausted) or GIVEN width (only 9).
   [consistent — STEP-style batteries are count/span/Likert-heavy]
2. Digit-span norms (Woods 2011), Corsi norms (Kessels 2000), and count
   data generally are unimodal/decaying — adjacent-category mass
   borrowing is domain-grounded, not just a smoothing trick. [A001]
3. Strict-numeric option detection is the safe flag: unhcr/unicef
   '98. I don't know' style coded labels fail float-parse, so
   non-response codes (98/99) can never be pulled adjacent to substantive
   values by a rank kernel. Likert items with worded labels are left out
   in v1 (conservative; revisit only with a labeled-ordinal map).

## Feeds into

- E011 (ordinal kernel smoothing, per-item bandwidth from the internal
  holdout, off-by-default).
