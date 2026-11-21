# E073 — Boosted-tree experts (GIVEN-only and neighbour-answer features)
parent: E072
status: parked
date: 2026-11-12

## Registration (before any hosted run)

Motivation (full review 2026-11-12, see log): fifteen sprint uploads gave no readable gain;
E041's UNHCR sits on a rounding boundary (old-scale ~.9155); the gap to the leaders is
structural (UNHCR old .94 means ~23% lower log loss; WB .50 vs .49). A categorical boosted-
tree model has never been evaluated properly on real data in this project (E040's blend
weight was selected against an in-sample net, A006; E046/E051 stopped at an Adult-proxy
gate). The leaderboard's clusters of identical rounded scores fit a common tabular solution.
E034's loss map (base .79 + evidence) implies most remaining UNHCR loss sits on rows where
neighbour evidence is weak, i.e. where base quality decides.

Experts (per PREDICT head, all option classes incl. the sentinel, scikit-learn
HistGradientBoostingClassifier: lr .1, <=120 iterations with internal early stopping
(15% validation, patience 6), 15 leaves, min leaf 10, L2 1; classes with < 8 rows disable
early stopping (40 iterations); output mixed with 2% of the smoothed context marginal):
- g: GIVEN columns as native categorical features plus totals of count-banded roster columns.
- n: g plus, from the three nearest labelled context rows by rarity-weighted GIVEN agreement
  (self excluded, so context rows are leave-one-out): their match scores, agreement counts,
  per-column agreement flags of the nearest row, and their answers to the target item. The
  trees learn when to copy a neighbour, replacing fixed per-item lambda buckets.
No labels of held-out or S/E rows are used; neighbours come from the fitting rows only.

Chains: gmixNN/nmixNN, gconfNN/nconfNN, gstack/nstack(c) (per-head weight on S), and
xstack/xstackc (per head the best expert kind and weight on S; two-fold out-of-fold S score
for ranking). Same S/E guard as E071; DIRECT and NO_E_CHECK probe switches from E072.

Probe uploads (each instrument is an independent reading):
- E073g: every instrument = g alone (gmix100). Diagnostic of plain tabular-model strength.
- E073n: every instrument = n alone (nmix100). Diagnostic of the neighbour-tree model.
- E073s: per instrument the best S chain among xstack/xstackc/nstack(c)/gstack(c) applied
  without the E test (applied only if it beats the shadow E041 on S).

Reading (old-scale bins; new-scale values): UNHCR .92=.8457, .93=.8650, .94=.8843, .91=.8264,
.90=.8071, .85=.7107, .80=.6143; WB .49=.2335, .50=.2486, .48=.2185; UNICEF .52=.3499,
.53=.3635, .51=.3364.
- g/n alone at or above E041's bin on an instrument: the expert alone matches the whole E041
  stack there -> stack is expected to gain; prioritise that expert in the Final.
- g/n alone far below E041 (UNHCR <= .85): tabular/neighbour trees do not explain the
  leaders' edge; keep only guarded stacking.
- E073s above E041's bin: readable gain from stacking -> Final candidate after phase-2 PASS.
  Equal: unresolved. Below: S-only selection overfits; keep the E test in the Final.
- Technical: Failed (not counted).
Local synthetic data cannot show real twin/neighbour structure; local runs check validity,
runtime and plumbing only.

## Design revision before any upload (2026-11-12, same day)

User reminder: few uploads remain; every upload must carry a real chance to beat E041, not
only a diagnostic. Self-review of the first trio (g alone, n alone, S-stack) found:
- two of three were pure diagnostics; g alone is dropped (kept as a reserve build);
- the most direct route was missing: trees as E041's own base. E034's loss map says rows with
  weak neighbour evidence carry most remaining UNHCR loss, where base quality decides;
- the 2% marginal smoothing of tree outputs was too heavy for near-deterministic UNHCR cells
  (about -.008 nats/cell on confident correct cells); reduced to 0.2% (grader floor is .001);
- neighbour ranking now uses Fellegi-Sunter agreement weights estimated from provisional
  top-1 pairs (the E021 rule already deployed in E025/E041), rarity weights as fallback.

Added `BASE_TREES` (instrument -> weight v): GIVEN-only tree distributions for every row
(5-fold out-of-fold for visible rows, all-visible fit for held rows) replace E041's network
probabilities by (1 - v) * network + v * trees inside E041 (hook on `_proba_maps` for the
full-frame call only; the holdout call that tunes the network/ladder weight is untouched).
Conditional heads use the trees' non-sentinel mass renormalized. The ladder mix, gate
coupling, donor-evidence replay (now against honest out-of-fold tree predictions) and
rendering are E041's own code. v = 0 must reproduce E041 exactly (plumbing check).

Revised upload trio: E073n (n alone), E073s (S-selected stack of E041 with g/n), E073b
(E041 with tree base, v = .5, all three instruments). Arms for E073b: any instrument above
its E041 bin = the base was a bottleneck there -> guarded choice of v in the Final; equal =
unresolved; below = trees weaker than the network as a base on that instrument.

## Results

**Local engineering, 2026-11-12 (synthetic sandbox, kit aa03186 scorer; not efficacy evidence).**
Self-tests on fabricated twin data (tmp/e073_selftest.py running tests/test_e073_tree_experts.py
in the model venv): roster totals, self-excluded neighbour search finding the duplicated row,
neighbour trees learning to copy while plain trees cannot — PASS x3. Tree-base weight 0
reproduces E041 exactly (UNICEF 17856 vectors, hook applied once). Uploads E073n / E073s /
E073b: ZIP checker OK, official phase 1 PASS on all instruments, vectors valid; wall 330 /
571 / 571 s. Tree fitting cost: UNHCR 213 heads 25 s (g) / 38 s (n) per pass, WB 15-22 s,
UNICEF 3-10 s; out-of-fold base trees UNHCR 154 s, WB 117 s, UNICEF 18 s.
Synthetic log deltas vs E041: n alone -.0147 / -.0494 / -.0149; tree base v=.5 -.0025 / -.0097 /
-.0033; S-stack 0 / 0 / +.0002. Identities in ../../submissions/2026-11-13-E073/SCORES.md.

**Phase-2 dry run, 2026-11-12 (synthetic, TRAIN+DEV visible, TEST scored; engineering only).**
E073b PASS on all three, 560 s (UNICEF 46, WB 166, UNHCR 348); E073n PASS, 359 s. No
phase-2-specific failure of the tree code paths (larger visible set, 1449/1212/3473 queries).

**Hosted, 2026-11-12 (user-pasted API fragment; owner and team fields of a second Codabench account (identifiers withheld),
not the team's usual `minjoonyoo` / "Odyssey" account — legitimacy unverified, raised with the
user; see the scorecard).** E073n ID 1049629: old-scale UNICEF .51 / WB .48 / UNHCR .91, each
one bin below E041 (.52 / .49 / .92; E041's UNHCR reads .91 about two times in five).
E073s ID 1049646: equal to E041 on all four values (**Unresolved**). E073b: Failed, timeout.
Reading: an untuned single neighbour-tree model is within about one bin of the whole E041
stack on every instrument; per-head linear stacking of the two gained less than one bin.
Hosted CPU-bound tree fitting ran roughly 2x slower than local (E073b 571 s local timed out;
E073s 571 s local with fewer tree passes finished).

## Registration of the pooled stack (2026-11-12, before any upload of it)

Two near-equal models built on different principles call for a stronger combiner than a
per-head linear weight. Added learned log-linear pooling: p proportional to
p_E041^a * prod_k p_k^(b_k), exponents in [0, 3] fitted by L-BFGS on the S rows (concave
multinomial-logistic problem on log-probabilities clipped at 1e-6; start (1, 0) = E041 itself).
`nlpool` = global exponents (2 parameters per instrument); `nlpoolh` = per-head exponents
shrunk toward the global ones (ridge .02); `xlpool(h)` = all XSTACK_KINDS experts. Ranking on
S uses two-fold out-of-fold scores; the E test or NO_E_CHECK applies as before. Agreement of
the two models sharpens the pooled distribution, disagreement hedges; the fitted exponents
also absorb temperature calibration of E041.
Build E073p: every instrument, chains nlpool / nlpoolh / nstack / nstackc with expert n only,
best-on-S applied (no E test). Arms versus E041's bins: above = readable gain from pooling ->
Final uses the guarded pool; equal = unresolved; below = pooling overfits S, keep the E test.
Self-tests (fabricated data): pool fit reaches a stationary point with weight on both views and
gains out of sample; chain application keeps valid distributions — PASS.

**Hosted, 2026-11-12, E073b2 (ID 1049751, same second account; see scorecard).** UNHCR
old-scale .91 with UNICEF/WB unchanged. A model better than E041 by +.002 would read .91 with
probability about .03, so the tree-base route gives no meaningful gain; dropped from the Final.

## Registration of reliability calibration (2026-11-12, before any upload of it)

Two structurally different models (E041; neighbour trees alone) stall within one bin of each
other while leaders sit about .02 higher. Hypothesis: sharpness, not information. Most UNHCR
cells are near-deterministic; E041's final probability on a perfectly matched donor is capped
near lambda + (1 - lambda) * base with lambda <= .98 chosen per item for a whole bucket that
mixes perfect and mediocre matches, so the best-matched cells may be systematically
under-confident. Stated .97 versus true .995 on a majority of cells is worth about .01-.015
skill; this has never been measured on real data (all earlier calibration studies used
synthetic or proxy data, and E071 offered only two global temperatures).

`cal`: on the S rows of the shadow run, bin the top-class probability above .5 at
(.5, .7, .8, .9, .95, .98, .99, .995, .999), take per bin the smoothed observed accuracy (50
pseudo-cells toward the stated confidence), make it monotone, cap at 1 - 1e-4, and move each
cell's top-class probability onto the interpolated curve; other classes keep their
proportions; cells below .5 are unchanged. Usable after any chain ("nlpool+cal"). The curve is
fitted on S; the E rows decide (one-sided lower bound > 0). Cells of one respondent are
correlated, so bin accuracies are less precise than cell counts suggest; the E test covers it.
Limit: the curve comes from the shadow fit (F rows) and is applied to the all-visible fit.

Builds: E073c = `cal` alone on every instrument (no expert; cheapest hosted run); E073pc =
UNHCR/WB with cal / nlpool / nlpool+cal / nlpoolh+cal / nstackc, best two on S E-tested.
Arms versus E041's bins: above = readable gain (E041 was under-confident at the top) -> Final
keeps the guarded calibration; equal = unresolved or rejected internally; below = adverse
(shadow-to-final transfer failed) -> drop. Self-tests on fabricated under-confident data PASS.

**Final local validation of the calibration / pool packages, 2026-11-13 (synthetic; engineering
only).** After patch 10 (two-fold out-of-fold S ranking of every fitted chain; refit on S+E
after acceptance; ten self-tests PASS): E073c 524 s, E073pc 489 s, E073x 474 s, official phase
1 PASS on all three instruments, vectors valid, every chain rejected on the synthetic data
(outputs equal E041). Identities and arms: second set in
../../submissions/2026-11-13-E073/SCORES.md. A third soft-vote expert `m` (n plus the weighted
class shares of the ten nearest rows) is available to the pools (E073x).

**Review note 2026-11-13.** Row order as a hidden channel was checked and excluded (kit README:
rows permuted before ids were assigned). The hosted history shows that only the donor-evidence
axis moved real UNHCR (E018, E022, E041); the follow-up that targets how E041 uses its donors
is registered separately as [E074](E074-twin-copy-share.md).

**E073xm (replaces E073x before upload), 2026-11-13.** Single expert m, UNHCR guard over
`mlpool, mlpoolh, mlpool+cal, mlpoolh+cal, tpoolh, cal`, BUDGET_SECONDS 880: E073x could time
out exactly when a two-expert pool is accepted (final refits of n and m at 1.9-2.7x hosted CPU
slowdown). Clean synthetic: PASS x3, 452 s, rejected, vectors equal E041. Two-fidelity
duplicate simulation (synthetic): `mlpool+cal` accepted, +.0346 log / +.0488 old-scale skill
over E041 (E074's twin +.0100 there), 536 s; acceptance and final refit ran end to end.

**Hosted, 2026-11-13 (user-pasted API fragment, owner `minjoonyoo`).** E073c ID 1050766 and
E073xm ID 1050762: both equal E041 on all four values. Arms: **Unresolved** x2. Neither output
calibration nor the single-expert log-linear pool gives a readable gain on real data.
