# A042 S1 — query-round conditional retrieval contract

2026-10-09 KST. **CONTRACT_READY_FOR_S0_REVIEW** — information/design only.
One prospective UNHCR candidate, no implementation or execution authorization.
Role/read receipt, source identities and preservation evidence: [verification.json](verification.json).

## 1. Decision and evidence boundary

The proposed family can change donor rankings that E041's section-constant
metric cannot change. Keep the original K32 construction, all-cell objective,
section selector, lambda algorithm and global recursive renderer. Add only
query-wave-dependent metric weights with an explicit common-weight penalty.
Its useful complementarity, learnability, actual activation and complete runtime
are **unmeasured**. No numerical oracle, fresh labels or model outputs exist here.

Public `unhcr.json` v1.3 declares GIVEN `wave` with string levels `1`,`2`, 17 GIVEN
columns, 213 PREDICT items and eight source-regex groups, in encounter order:
2:6, 3:61, 7a:24, 7b:39, 7c:11, 4:12, 5:10, 6:50. All groups remain eligible;
no favorable head subset. There are 156 gated PREDICT items. Their declared
substantive options total678; appending sentinels gives834 full output columns
(maximum15); gated conditional heads total456 columns. These are schema counts,
not observed fitting/support counts.

The public description reports round-specific coding differences, including
59 multi-select items with round-2-only sentinels. This motivates a question,
not an observed predictive advantage. Both rounds are within May–June2025;
the description treats them as independent cross-sections without a usable
cross-round respondent link. No panel, duplicate-household, drift, exact-gate,
or causal-round assumption. E041 already uses wave in its neural/GIVEN inputs,
conditional gate agreement when selected, and donor exact-match features.

E062 ID969351 remains published tie/UNRESOLVED, not exact effect0. E041 remains
incumbent. Historical E041 hosted improvement concerns its whole procedure;
E043/E045 pool and E047 correction oracles do not bound this family's gain.
E058 active0 STOP, E059 STOP_SELECTION and E060 tie remain counterevidence
against assuming that greater flexibility produces useful learned evidence.

## 2. Exactly one parameterization

For section s, fixed query q and original ordered donors d in D(q), let
`x_qdj = 1[GIVEN_qj = GIVEN_dj]`, D=17, and r(q) be the query's own wave.
All donor identities/order are produced by original initial metric v0; the
conditional weights never participate in shortlist search.

Fit `w_s1,w_s2 in [0,12]^17` and one shared `eta_s in [-5,5]`:

\[
z_{qd}=x_{qd}^{T}w_{s,r(q)},\quad
\pi_{qd}=\operatorname{softmax}_{d\in D(q)}z_{qd},\quad a_s=\sigma(\eta_s).
\]

For item i, bank marginal `m_i` is the original count+.5 prior (including
sentinel); `e_qi(y)=sum_d pi_qd 1[y_di=y]`. Fit on F only, all section cells:

\[
L_s=-\frac{1}{|F||I_s|}\sum_{q\in F,i\in I_s}
\log\{.001+(1-.001K_i)[(1-a_s)m_i(y_{qi})+a_se_{qi}(y_{qi})]\}
+\frac{.001}{17}\|\mu_s-v_0\|^2
+\frac{.001}{17}\|\Delta_s\|^2,
\quad\mu_s=(w_{s1}+w_{s2})/2,\quad\Delta_s=w_{s1}-w_{s2}.
\]

This is one fixed coupling coefficient .001, not a searched grid or separately
selected penalty. The first penalty retains the original E041 common-metric
anchor; the second shrinks the round difference to zero. In expanded form the
penalty couples the two round vectors; it is not two independent round fits.
The equal-weight arithmetic center is fixed; no inverse-frequency balancing,
round-specific share, label smoothing or sentinel deletion. Actual F cell
frequencies retain their original weighting.

Start both w at `clip(v0,0,12)`, eta=0. Preserve the source's nonnegative,
otherwise **unclipped** v0 as penalty anchor; it can exceed12. One L-BFGS-B
start, analytic gradient, maxiter50, ftol1e-7, same bounds and numerical
environment. 35 coordinates replace18; eight optimizations remain eight.
No common-fit warm start, second optimizer, alternating fit, coefficient search
or post-selection metric refit. Penalty gradients are
`g_w1=.001*(mu-v0)/17 + .002*Delta/17` and
`g_w2=.001*(mu-v0)/17 - .002*Delta/17`, plus their wave-masked data gradients;
eta receives the pooled original share gradient. These are algebraic derivations,
not executed gradient checks. No convexity, unique optimum or convergence claim.

### Reduction, identifiability and hand calculation

At w1=w2=w the loss is exactly the original common objective. However, solving
the duplicated parameterization at equality need not reproduce the original
optimizer's floating-point trajectory. **Exact common endpoint C therefore calls
the original18-coordinate E041 path**, including its selector and renderer.
Do not describe merely small Delta, an infinite-penalty limit, or manually zeroed
Delta with a different mu/share/activity as exact E041.

For two different-round queries, suppose each has two same-round donors with
other matches A=(1,0), B=(0,1), and all remaining matches identical. A common
w ranks A/B identically for both queries. Fixed match-pair terms x_j*x_k do
too: their complete match vectors repeat. Conditional w1=(2,1), w2=(1,2)
gives score differences +1 and -1, reversing the ranking. All weights satisfy
bounds. This is a hand-written representational witness, not a fixture run or
evidence that the actual K32 libraries contain those patterns or useful labels.

A query-only intercept `b(r(q))` is donor-constant and cancels in softmax;
it is not added. More generally any weight change whose score increment is
constant over all donors for every relevant q cannot change those posteriors.
Collinear match features and absent donor alternatives also limit identification.
The penalty chooses among weakly informed weights but supplies no empirical signal.

Wave agreement already exists. For binary z_q,z_d in {+1,-1},
`x_wave=(1+z_q*z_d)/2` and `z_q*x_wave=(z_q+z_d)/2`.
Thus the difference component on the wave-match coefficient is, after removing
the query constant, a donor-wave preference. It is not an entirely new source
of query information. Differences on other GIVEN matches can still express
the reversal above. Where every donor has the same wave relationship to q,
the wave-match coefficient itself cancels. Bounds preserve nonnegative match
weights in both rounds; this is not an unrestricted interaction network.

| Prior mechanism | Difference retained here |
| --- | --- |
| E036 | Splits final lambda by top-donor same/cross relation; this changes within-K32 posterior by query wave, without splitting lambda. Its historical panel interpretation is not adopted. |
| E043/E045 | Replace/expand donor pools; this retains original initial-search K32. No claim to recover donors outside it. |
| E047 | Extra final-output mixture after rendering; this replaces section evidence inside original recursion. |
| E058/E059 | Match×match terms, with their original fixed activity/lambda scopes; this uses query-wave×match and retains E041's activity/replay algorithm, so resulting activity/lambda may differ. |
| E060 | Removes sentinel fit cells; this keeps every original fit cell and prior. |
| A021/A023 | Controlled marginal/deployed selector study; this changes neither selector objective nor role allocation. It is not P/D or D-P/D-R validation. |

### Fixed support and failure policy

Prospective, GIVEN-only eligibility is fixed now: require the declared wave
column/levels; every row supplied to this invocation must have a supported
wave; original F and S must each contain **at least30 rows per wave**, and
the fit donor width must be32. Otherwise route the entire instrument through
original E041 before candidate metric optimization. One-wave, unknown/missing
wave and sparse-wave cases thereby have an exact common fallback. Do not coerce
unknown tokens or mix a common per-query weight with candidate-trained lambdas
and call that exact R. The30 support minimum is an additional engineering
eligibility choice, **not** a precision guarantee or the lambda bucket rule;
it is not tuned, and does not alter the .003/2SE selector. A bank containing
only one round need not prohibit other-feature reranking when F/S qualify;
its donor-constant wave component remains uninformative as above.

Preserve original `visible<500`/no held rows dispatch and all ordinary E041
fallbacks. A finite maxiter result follows original handling and is disclosed;
nonfinite metric coordinates retain the original section-inactive/initial
fallback, without refitting. An unexpected numerical/probability/leakage/parity
defect is technical STOP, not an opportunity to change policy or claim a PASS
because a fallback emitted predictions. Zero active sections gives original
legacy evidence policy; it need not equal R, which can activate other sections.

## 3. Comparators and unchanged selection rule

Names: R is exact E041; C is the restricted common-metric arm; H is the one
conditional arm. For this minimal contract **C is R by construction**: reuse
the original fit, roles, initial weights, optimizer, activity, lambda and final
rendering. There is no altered-role common arm, common-only penalty, extra
training budget or new selector. Treat C and R as one baseline invocation,
not two independent controls or two claims of success. Future source/assembled
parity must establish that the designated C entry actually uses the original path.

For each arm and each section preserve E041's old comparator O: the first10
of initial-search K32 with original v0 and a share picked on F from
{0,.25,.5,.75,.9,.98}, first maximum on ties. This is **not** deployment's
legacy `_topk_excl` top10. The learned arm has K32 and its fitted shared a.
On S compute per-row mean section log difference versus O; activate iff
`mean(delta) > max(.003, 2*sample_sd(delta,ddof=1)/sqrt(nS))`.
Strict comparison, nS<=1 infinite SE, no cluster substitution or extra round guard.
The same S is reused across eight sections and across R/H engineering comparison.
This is an algorithmic selector, not a multiplicity-adjusted efficacy test.

There is **no S argmax choosing H versus C**, no new H-C acceptance threshold,
no S-based shrinkage choice, and no winner-conditioned refit. Such a selector
would change the preserved policy and needs a different S0 decision. C/H's
S diagnostics answer a reused proxy comparison only. A future full-output
H-C contrast asks whether extra conditional flexibility and its induced
share/activity/replay choices help this procedure. H-R asks the same complete
procedure question because C=R; neither isolates a fixed-weight direct effect
nor provides an independent audit. Reusing those contrasts cannot create two
independent replications. If S0 needs objective-only or independently honest
selection evidence, this contract cannot provide it; A023/A024 HOLD remains.

## 4. Information and state flow from actual source

V denotes complete visible TRAIN, Q wholly masked queries; B/F/S/L denote the
metric bank, fit, selection and replay rows within V. L is called `replay` in
source, not an independent outer evaluation. These are future algorithm roles,
not assignments or permissions to access any present dataset.

| Stage | Response access and fixed state | Interpretation |
| --- | --- | --- |
| Input | Mask every Q PREDICT cell before any base/ladder/gate/retrieval helper; EXCLUDE never features. GIVEN kept. Same frame/order/mask for R,H. | Partial target masking would let visible query targets affect recursive beliefs; it is prohibited in this proposed evaluation. |
| Base | Original ladder holdout seed0/.2; neural inner seed1/.2, two configs and final refit on all V; gate agreement trained on available V. | Base final replay already sees F/S/L answers. Neural config/epoch/blend policy unchanged. |
| Common preprocessing | `_sig_data_all` uses GIVEN from the entire supplied frame, including Q, for coding/rarity. Preliminary legacy K10 and `estimate_weights` use GIVEN, cal capped6000 seed0. | Transductive GIVEN access is retained, not called fit-only. No Q responses. |
| Metric roles | Same seed4101 permutation; F=min(1200,max(1,N//5)), S=min(800,max(1,N//10)), L=min(800,max(1,N//10)); B is remainder. | B/F/S/L row-disjoint at this metric stage; no new household audit or seed. Public counts alone do not reveal wave support. |
| Metric fit | B responses build priors/donor matches; F responses optimize weights/share and old-share grid. S labels form selection comparisons, never optimizer inputs. | Existing `fit_sections` materializes F+S truth/match arrays before slicing F. Future tracing must verify actual optimizer slices; do not falsely claim S labels never enter the combined function. |
| Section choice | S against O independently in each section, as above. Freeze weights, shares and activity afterward; no metric refit. | This freezes metric choices, not yet lambda or whole-output candidates. |
| Replay | Original_cal=V or sample6000; if any active, cal=union(original_cal,L). Deployment evidence bank becomes **all V**, excluding each replay query itself. | Not the smaller B used for metric fit. Other F/S/L responses can now be donors. |
| Lambda | Active items use L only; inactive use original_cal. Legacy K10 max posterior>=.5 defines the two buckets. Each needs30; else0. Original grid0,.1,...,.9,.95,.98 and strict tie retention. | Base full marginal probabilities are in-sample. Original_cal can overlap S/F/B/L. No wave split or learned-posterior rebucketing. |
| Final Q | GIVEN-only initial K32 and legacy K10 against V; learned section weights follow query wave. No Q response in any state. Freeze lambda before Q scoring. | Same V as replay, larger than metric B; no second whole-model refit. |
| Render/evaluate | Original all213 schema-order recursion; final parent beliefs include evidence before children use them. Only an external evaluator may compare frozen Q outputs with authorized truth. | All UNHCR outputs/sentinel mass can change through parents, even inactive heads. UNICEF/WB must remain exact E041. |

Source's `model_dists` is the full ladder/neural marginal distribution before
gate/evidence recursion. Learned proxy share a is discarded after section
selection. Actual donor evidence has no bank+.5 mixture. Lambda uses clipped
truth probabilities and `log(max(mixture,.001))`, not the selector's distribution
or the final recursive output. Preserve these known mismatches; do not add a
second floor to emitted raw vectors. Evaluation normalizes the final vector
then applies `.001+(1-.001*K)*p`, as `logloss.floor_mix` records.

Although F/S/L are metric-disjoint, full-stack validation is not honest outer
cross-fitting: final base sees them all, legacy lambda can reuse S, and replay
donors include other replay rows. H can change activity, the cal union, which
rows fit each lambda, the lambda values, and descendant outputs. Hold the
**algorithms**, not those resulting values, equal. No new outer refit policy.

Original K32 sorts bank positions, excludes self, uses `argpartition` for
membership, then score-descending/ID-ascending `lexsort` within the selected
subset. Ties at the K boundary are not globally ID-stable. Preserve exact
source, NumPy version, input row order and selected IDs/order. Legacy K10 uses
default `argsort` and its last10 order; never substitute first10-of-K32 for it.

## 5. Complete source-derived cost contract — not timing evidence

Call chain: `supervised_retrieval.predict` dispatches UNICEF/WB to
`hh_cap.predict`, UNHCR to `link_sharp.predict(...supervised_layer,hh_cap.CONFIGS)`.
`link_sharp` selects ladder, calls `shared_trunk.tune_and_train`, builds full/
conditional ladders, conditional agreement, marginal maps, retrieval layer and
global recursion. `tune_and_train` performs two config `_train` calls plus one
all-V final `_train`, even if selected neural blend is0. Each `_train` calls
`_train_on`; GPU exception can add a CPU retry in existing source. The minimum
future local scope must enforce CPU selection before numerical imports and
verify it in the worker (CPU2/GPU0); the GPU retry branch is outside that scope.

| Normal scope, no cache reuse | Base pipelines | Neural `_train` calls | Metric optimizer calls | Additional post-selection refit |
| --- | ---: | ---: | ---: | ---: |
| R=C, UNHCR | 1 | 3 | 8 at18 coordinates | 0 |
| H, UNHCR | 1 | 3 | 8 at35 coordinates | 0 |
| One all3 R or H | 3 | 9 | 8 | 0 |
| Fresh all3 R and H, sequential | 6 | 18 | 16 | 0 |
| Also fresh all3 E025, if later required | +3 | +9 | +0 | 0 |

The final neural refit is already counted in each three calls; “no additional
refit” does not mean there is no refit. H adds no base pipeline or optimizer
invocation relative to R, but each objective/gradient has different work and
may require different line-search evaluations. Maxiter50 is not50 function calls.
Eight active sections are not required for eight fits: all sections fit before
activity is known. Small/invalid input or failure can reduce completed calls;
record starts, failures and completions separately. No new loop repairs a failed
scientific run. Eligibility fallback calls R once, not H then a second R stack.

Other work per normal UNHCR invocation, unchanged algorithm:

- One greedy ladder search; 15 public GIVEN columns have cardinality<=12,
  max depth3, five kappa values. At most15+14+13=42 candidate extensions,
  each pooling all213 heads over five kappas, plus prefix ladders/marginals.
  Neural blend tuning builds213 ladders; final full/conditional tables369.
- Neural configs64x2 and128x2/dropout.1, seed0, max500 epochs/early-stop30;
  two config evaluations and original blend grid. Conditional agreement is
  one loop over gated items/GIVEN candidates, not another neural fit.
- Legacy K10 construction: preliminary cal, post-weight cal, and final Q
  if any lambda is nonzero. K32 construction: F+S once, cal once if any
  section active, Q once if active and lambda permits final evidence.
- Six old-share evaluations per section (48 total); one learned optimizer
  per section; two proxy distributions per section on S. Active section
  posterior/evidence replacement once on cal and once on Q when reached.
- Up to426 item/bucket lambda searches, each baseline plus11 nonzero grid
  scores; no extra lambda variants. Full recursive output serialization,
  imports, input adaptation, hashing/monitoring and cleanup must also be timed.

Static tensor sizes explain what to measure; they do not certify peak RSS.
With F+S<=2000, K32, D17, float64 features occupy8,704,000 bytes; donor int64
indices512,000 bytes. Largest section61 gives31,232,000-byte float64 match
tensor. Current `labels[donors]` first materializes **all213 heads**, a
109,056,000-byte int64 temporary at Q=2000, before section slicing; account for
slice, Boolean and conversion temporaries too. Reuse the same feature tensor,
index one [Q,17] row-weight matrix (272,000 bytes at2000), and do not duplicate
full features for two rounds. This is a future implementation requirement,
not an implemented optimization.

At cal<=6800, the equivalent K32 feature tensor alone is29,593,600 bytes.
K32 search has chunk128×bank float64 scores plus partition indices/temporaries.
Legacy K10 broadcasts chunk256×Nvisible×17 and creates weighted float64
temporaries, potentially much larger than the conditional parameters. Full
neural outputs include834+456 columns per row, GIVEN dense width159; targets,
autograd activations, best-state copies, retained config/final nets, ladder
tables, marginal maps, evidence and Python output objects also coexist.
The schema's total10349 rows does not fix actual Nvisible/Nquery or fit support.
No numeric process-memory upper bound follows from adding just these arrays.

Future minimum technical measurement, only if separately authorized: existing
CPU environment, two numerical threads, one worker, GPU0; one fresh R=C all3
and one H all3 in separate sequential processes, each shared900s including
imports and all instruments; aggregate computational1800s ceiling and owned
process-tree RSS/private commitment8GiB ceiling. These are proposed STOP caps,
not expected times. An outside monitor starts before imports, samples both
memory measures at<=1s, records per-phase/total wall and call counters, and
kills only its owned tree on time/memory/monitor failure. Registration must
also bound total session/focused-check wall before starting. No new cloud,
dependency installation or model acquisition is needed by the mathematical
contract; actual environment sufficiency is not tested here.

A matching existing R/E025 engineering cache may later replace a baseline
fit only with source/dependency/options/schema/frame/order/mask/split identity
and valid complete-output provenance. This session opens/hashes no cache.
Without matching E025 evidence, an extra fresh E025 all3 would add900s and
the +3/+9 row above, requiring that larger scope before execution. Assembly,
ZIP checker and official all3 are additional S2 work, not hidden in1800s.
Do not extrapolate SIPP tree times, partial heads, E060/E062 historical runtimes
or coordinate ratios into measured candidate all3 time.

## 6. Future gates and useful observation channel

This list is a design deliverable, not commands or an activated experiment.

1. Freeze this family/support rule, schema group order, source/options/seeds,
   original selection/lambda policy, input roles and aggregate resource caps
   before any future response access. No new threshold/head/context search.
2. Cheapest authorized engineering checks first: analytic-gradient comparison;
   donor-constant invariance; common objective reduction; exact original-C path;
   bounds/finite distributions/final floor and schema ordering. Preserve K32
   membership/order and legacy top10 separately. Check every fallback.
3. Trace actual label access: Q fully masked before all helpers, F-only optimizer;
   within the metric stage S changes activity, not fitted weights/share. Freeze
   metric before replay; no Q truth callback. Test that L/S can affect the base
   and replay states they historically control;
   do not demand false independence from in-sample base refit. Confirm UNICEF/WB
   exact parity, global ancestor/descendant propagation, unchanged lambda
   minimum30/zero fallback and two legacy concentration buckets. A deliberately
   active tiny fixture is engineering only, separate from learned activation.
4. Only after those checks and authorization, run the complete fixed engineering
   comparison, all213 UNHCR outputs and both exact controls, with source-derived
   counters above. Freeze outputs before scoring; no test-label model choices.
   All-equal final outputs stop that unchanged engineering candidate before any
   release preparation; they do not establish hidden-UNHCR impossibility. Do not
   force sections to activate. A later qualified adverse full-policy reading is
   evidence against that fixed candidate, not a refutation of every conditional
   metric; an inconclusive reading permits no same-policy/seed/threshold rescue.

| Observation | Allowed reading / action |
| --- | --- |
| Static representational and flow contract coherent | Current CONTRACT_READY_FOR_S0_REVIEW only. |
| Leakage, wrong common endpoint, invalid probability, changed controls or resource failure | Future technical STOP; preserve failure, repair only authorized ordinary implementation errors under fixed aggregate budgets. No scientific policy rescue. |
| Synthetic active/fallback paths valid, complete costs within caps | Local engineering evidence only; S0 may review a separate next scope. |
| Synthetic gain, loss or all-equal output | Descriptive engineering result; no true UNHCR benefit/refutation, no fresh audit. No favorable seed search. |
| Future independently permitted observed comparison absent | Empirical effect remains unresolved; do not appropriate Adult/SIPP roles or assume VAF semantics. |
| Future hosted higher/tie/lower/error | Must preregister favorable/unresolved/adverse/technical and source-comparability arms before a separately authorized release. No current slot or upload permission. |

No valid numerical oracle now: no new frozen H/C output library and authorized
evaluation labels. Earlier Adult donor oracles concern different data/policies;
SIPP roles remain protected and lack this CATI round interpretation. Existing
synthetic is exposed engineering material; injecting the hypothesized round
mechanism cannot establish its natural occurrence. No universal +.005 hurdle
is imposed or used to reopen prior STOPs.

Specific next decisions: S0/user owns authorization for one bounded technical
implementation under this prospective UNHCR scope; the implementing S1 owns
source isolation, fixed registration and complete measurement. An independent
observed study would additionally require a named legally permitted channel,
its owner-provided coding/round/unit/exposure metadata, authorized roles and
pre-label precision/claim design. None is silently supplied by A022 counts or
this document. Actual competition TRAIN selection would run inside hosted
execution only; no detailed diagnostic extraction/score encoding is proposed.

For any later S2, still required: clean E025 absolute .002 per-instrument check,
full E041 comparison and fixed exact controls, source/assembly parity, ZIP
checker, official all3/shared900s and memory qualification, plus a prospective
SCORES interpretation table. No release or TEST claim follows from this contract.

## 7. Source anchors and preserved state

Static anchors (current hashes in verification):
[supervised retrieval](../../../../src/models/supervised_retrieval.py),
[K32 construction](../../../../src/eval/retrieval_oracle.py),
[legacy retrieval](../../../../src/models/dup_link.py),
[initial weights](../../../../src/models/hh_link.py),
[lambda/rendering](../../../../src/models/link_sharp.py),
[evidence](../../../../src/models/prob_link.py),
[shared trunk](../../../../src/models/shared_trunk.py),
[base configs](../../../../src/models/hh_cap.py),
[ladder](../../../../src/models/hier_backoff.py),
[GIVEN encoding](../../../../src/models/logit_blend.py),
[conditional gates](../../../../src/models/cond_agree.py),
[final floor](../../../../src/eval/logloss.py).
The four directly connected additional source files were named with reading
purposes before access; none was imported. E041 snapshot identity was hashed,
not executed or independently reassembled.

E041 incumbent/E025 fallback; E057/E060/E061/E062 parked. E058 STOP,
E059 STOP_SELECTION, A023/A024 empirical HOLD, A039/A040/all STOP/HOLD unchanged.
17999people/12339SSUID and aggregate exposure/A022 original roles retained;
E059 consumed oracle1918/1124 and selection2007/1130; protected audit2074/1177
and calibration1866 untouched. A_half unpromoted, A018 user-unconfirmed,
S3 stopped, no new S2 candidate. Return to S0; no automatic implementation.
