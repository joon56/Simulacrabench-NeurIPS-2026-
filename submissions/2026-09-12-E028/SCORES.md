# 2026-09-12-E028 — parent-value-conditional gate decoding over E025

Experiment: E028 (adopted, E003 route; parent E025). Code: E025
assembly with the gated-child decode replaced by
Σ_v b_parent[v]·[(1−r_v)·A_v + r_v·sentinel] (per-parent-value tables
from visible rows; r_v split by E010's selected column). Zip:
`submissions/2026-09-12-E028.zip`, check_submission_zip OK.

## Local scores (2026-09-10, seed 0, phase 1)

| | sample | unicef | world_bank | unhcr | 3-inst mean |
|---|---|---|---|---|---|
| exact (runner) | 0.4432 | 0.5006 | 0.4548 | 0.5629 | 0.5061 |
| E025 (LB 0.63 / unhcr 0.89) | 0.4436 | 0.5006 | 0.4548 | 0.5629 | 0.5061 |

Identical on the exact-gate sandbox by construction. Branch-overlap
sim: +0.0017 (light) / **+0.0121 log** (heavy, schema-documented
range). Official score.py PASS ×3: 0.5000 / 0.4500 / 0.5600 (parity exact). Runtime ≈ E025.

## Leaderboard expectation (real data)

Reference: E025 LB = 0.63 (0.52 / 0.49 / 0.89). Pre-registered
2026-09-10 BEFORE submission (submit after E027 so each change reads
alone):

- **unhcr 0.90+** ⇒ real branch overlap is heavy and the No/DK-branch
  answer distributions carry signal E010's agreement mixing did not;
  next: condition A_v on wave / country too.
- **unhcr 0.89** ⇒ overlap light or already captured by E010's
  column-conditioned agreement; gate math complete.
- **≤ 0.88** ⇒ per-parent-value tables too thin somewhere (raise
  PVC_KAPPA / ALPHA) — revert to E025.
- unicef/wb: identical math on near-exact gates ⇒ flat.
