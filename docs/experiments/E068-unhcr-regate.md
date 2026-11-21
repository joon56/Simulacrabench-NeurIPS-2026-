# E068 — UNHCR return-branch re-gating on s3_12
parent: E066
status: parked
date: 2026-11-08

## Registration (before any hosted run)

Organizer hint (kit 30dd72d, 2026-10-25, unhcr.json dataset description): "The three
branches off s3_11 ... partially overlap in the file, and the return branch (s7a) and
do-not-return branch (s7b) follow s3_12 more closely than s3_11." The schema still gates
s7a (21 items, observed_if s3_11 = Yes), s7b (40, No) and s7c (11, Don't know) on s3_11;
E041 couples their skip probability to s3_11 (hard path weighted by gate agreement).
In the delivered schema order s3_12 comes after s7a/s7b, so E041 cannot be re-parented
internally; E068 post-processes E041's output instead.

Rule, per branch family (s7a_/s7b_/s7c_) and wave, on visible rows only: pool the skip
indicators of the family's s3_11-gated children that show the sentinel in that wave;
fit smoothed per-value skip rates (prior strength 20) given s3_12 (4 levels incl.
NA_GATED, which encodes s3_11 = Yes) and given s3_11; switch only if the s3_12
log-likelihood beats s3_11 by more than 1% relative. For each held-out cell of a switched
family/wave: sentinel = sum_v P_E041(s3_12 = v) * rate_v; content keeps E041's proportions.
Then the E066 transfer. Children with no visible sentinel in that wave are left to E066.

Local: unit tests 2/2 (switch and no-switch cases) plus E066 4/4; ZIP checker OK; official
scorer PASS all three; outputs identical to E041 on exact-gate synthetic data (no switch);
a forced switch changes 44091 UNHCR vectors, all valid, and lowers synthetic log score
(-.551737 to -.565692), as expected when s3_11 is the true synthetic gate.
Package submissions/2026-11-09-E068.zip, 16877 bytes, SHA256
97a22a86e43ebcd3cf4e02852b140c97d3004e81e9cb2fc9a8b664ffd74cdf6d.

Hosted arms (UNHCR versus the day-1 E041-code UNHCR .8457264165, same scale; UNICEF/WB
must equal .3499339289/.2335276584):
- Favorable: UNHCR higher. Re-gating helps on real data; extend (s7c, content, combine).
- Unresolved: equal. Effect below resolution or no switch fired.
- Adverse: lower. The s3_12-based skip estimate is worse than E041's own handling; drop.
- Technical: Failed.

## Results

(appended after runs)
