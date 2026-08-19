# E001 — marginal_counts (kit baseline, reference root)
parent: —
status: adopted
date: 2026-08-17

## Hypothesis

None — this is the reference point. The kit's crowd-marginal baseline
(`external/starter-kit/baseline/marginal_counts/main.py`): each item's
smoothed visible distribution, identical for every held-out respondent.
Everything else in the tree is measured against a chain that starts here.

## Change

No code of ours. Scored the kit baseline through the local harness on the
launch kit (trait_scale 2.0 sandboxes — all draft-era numbers obsolete).

## Result (seed 0, phase 1, exact skill via src/eval/runner.py)

| | sample | unicef | world_bank | unhcr | mean | Δ vs parent |
|---|---|---|---|---|---|---|
| 08-17 kit | 0.3198 | 0.1486 | 0.2469 | 0.2988 | 0.2535 | — |
| 08-19 kit (schemas v1.1/v1.3, count roles) | 0.3210 | 0.1623 | 0.2387 | 0.4287 | 0.2877 | — |

Official grader cross-check (08-17 kit): `score.py` on sample, phase 1 → `PASS 0.3200 (27 s)`.
Reproduce: `.venv/Scripts/python src/eval/runner.py external/starter-kit/baseline/marginal_counts/main.py`

## Decision

Adopted as the root reference. This is "the thing to beat" (kit README).
`bundled_artifact` scores identically (0.2534 mean) — same model, different
artifact plumbing; not tracked as a separate experiment.
