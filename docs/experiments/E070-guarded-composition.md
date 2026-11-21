# E070 — Internally validated composition (Final candidate structure)
parent: E067
status: parked
date: 2026-11-09

## Why (registered before any E070 run)

Day-2 hosted readings showed byte-identical E041 UNHCR code (E067ws) reading old-scale .91
while the same code read .92 on day 1; with ~16 near-E041 UNHCR readings (13 x .92, 3 x .91)
and DEV Laplace noise of ~.00088 scale, E041's UNHCR appears to sit just above the .915
rounding boundary. Single DEV readings cannot decide small effects. The run itself sees
the real visible rows, so decisions move inside the submission: a held-out internal
comparison on real data is exact and unrounded.

## Procedure

Per instrument: final base = cellwise mean of E041 over SEEDS (Jensen: cannot lower the
expected log score of a single seed). If CANDIDATES lists chains for the instrument and at
least 2001 visible rows exist: fixed PCG64(4501) permutation -> S1000 / E1000 / F rest;
shadow frame masks S and E; shadow E041 (seed 0) and, if needed, a TabICLv2 expert fitted on
F predict S and E. Each chain (transforms joined by "+": mixNN / confNN expert mixing,
sent = E069 sentinel replacement on gates with visible agreement < .95, regate = E068,
transfer = E066) is applied to the shadow base; the best chain by pooled floored log score
on S is kept only if it beats the shadow base on S and the one-sided E lower bound
mean(d) - 1.645 sd(d)/sqrt(1000) > 0 (d = per-respondent mean log difference). The accepted
chain is then applied to the final base with rules recomputed on all visible rows (expert
refit on all visible rows). Otherwise output = final base. Non-strict builds fall back to
the final base on any error and respect BUDGET_SECONDS.

DEV build dev1: SEEDS (0,); WB sent / mix25 / mix50 / mix50+sent; UNICEF mix25 / mix50;
UNHCR regate / transfer / regate+transfer (no UNHCR expert, to fit 900 s). Final build:
more seeds, UNHCR conf/mix chains, non-strict with a budget guard; phase-2 local PASS required.

Limits: S selection among <= 4 chains plus the E check is not an independent audit; the
shadow base is single-seed while the final base is a seed mean; internal decisions are not
observable from hosted scores (no encoding of statistics into outputs, by project rule).

Hosted arms for dev1 (versus same-scale E041-code values; UNHCR near-boundary noise noted):
Favorable = any instrument higher with others unchanged; Unresolved = all equal; Adverse =
an instrument lower (UNHCR .91 alone is weak evidence); Technical = Failed / timeout.
Main purpose: hosted rehearsal of the Final code path.

## Results

(appended after runs)

**Local dev1, 2026-11-09 (kit aa03186, synthetic, phase 1; engineering only).** ZIP checker OK;
PASS on all three. UNICEF: best mix25 on S (-.793928 vs -.794147) but E lower -2.1e-5 ->
rejected, output E041 (82 s). WB: best mix50 (S -1.094319 vs -1.096213), E lower +.00130 ->
accepted, final log delta +.002852 (246 s). UNHCR: regate/transfer did not fire on exact-gate
synthetic data, all chains equal the reference -> not applied (299 s; shadow E041 129 s).
~627 s for all three. Package submissions/2026-11-10-E070dev1.zip, 103060948 bytes, SHA256
06a361c05a98d33ee779d193e00f092f1abdbf07f0cc06839f60364184d90b31.

**Local final1, phase 2, 2026-11-09 (kit aa03186, synthetic, TRAIN+DEV visible, TEST scored).**
Build tmp/e070/2026-11-10-E070final1.zip (SHA256 74ad34b9...86e4): SEEDS (0,1,2,3), non-strict,
BUDGET 3300; UNICEF mix25/mix50; WB sent/mix25/mix50/mix50+sent; UNHCR regate/transfer/
regate+transfer/conf25/conf50/conf50+regate+transfer. PASS on all three.
- UNICEF: seed mean + accepted mix25 (E lower +5.4e-5): log +.000662 vs E041; 187 s.
- WB: seed mean + accepted mix50 (+.00122): +.001639; 433 s.
- UNHCR: 4 seeds 663 s, shadow E041 154 s, shadow expert 341 s, final expert 433 s; accepted
  conf50 (S -.546132 vs -.547210; E lower +.00087); regate/transfer inert on synthetic; +.001430;
  1620 s.
Sum of separate processes ~2240 s against 3600 s. Engineering evidence only; on real data the
guards decide independently.
