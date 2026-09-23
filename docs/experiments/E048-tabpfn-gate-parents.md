# E048 — TabPFN gate-parent challenger
parent: E041
status: parked
date: 2026-09-23

## Hypothesis

A frozen TabPFN-v2 classifier can capture GIVEN interactions missed by E041;
mixing its predictions into high-fanout gate parents, when independently
validated on final descendant predictions, improves UNHCR completion.

## Domain check

Preregistered before model downloads, forward passes or estimator construction.
Technical: this introduces an independent pretrained predictor, not another
retrieval coefficient, candidate-count or tree-depth sweep. Schema-only scope:
the four PREDICT parents with most direct PREDICT children, ties in schema order,
provided the complete output has at most ten classes. Their effects must be
propagated through the existing soft gates and evidence mixture. Keep E041's
learned retrieval. Selection must see final output, not an in-sample base head.

Background: the published ERPIS metadata describes return intentions, social
networks and economic conditions of Syrian refugees across four host countries
and two CATI rounds; these domains need not share one demographic response
function. Approximate gates require preserving learned soft routing rather
than imposing deterministic sentinel rules (CLAUDE.md; docs/domain.md section9;
external/starter-kit/data/unhcr.json). A better parent can help descendants,
but gate disagreement can nullify that benefit. Historical E025 decomposition
(.79 base + .10 evidence, .079 gated residual) motivates the target, not a
measured E041 decomposition or a claim that all gated loss is recoverable.

Ceiling channel: freeze TabPFN-v2 outputs before any new mixture estimator.
Observed, deduplicated UCI Adult profiles, existing GIVEN/target protocol,
seeds49/50, 3000 rows: fit first1800, selection next600, audit last600.
TabPFN uses first512 fit rows, one estimator, categorical GIVEN indices,
random_state0, CPU; logistic comparator uses all1800 fit rows. Exclude targets
with more than ten schema classes from interventions, retain them in scoring.
Candidate mixtures alpha in {0,.25,.5}; query/section oracle selects among
these frozen mixtures using audit truth, with alpha shared within a section.
It is a permissive upper bound for this finite library, not learnability or
the HSCC ceiling. Require oracle skill gain/3 >.005 on both fixed splits;
otherwise stop before a production estimator. Also report honest section
selection on separate selection rows and audit score without changing settings.
Audit is used for screening: exploratory, not untouched confirmatory evidence.
No assumed household/gate structure is injected into this channel.

Feasibility gate: public locally bundled V2 weights, exact pinned compatible
package, offline import-time load, one CPU estimator, <=512 reference rows,
no new dependency changes to the baseline environment. Stop if incompatible
or if the measured full pipeline cannot pass the 900-second total budget.

## Change

Implementation plan: docs/plans/2026-09-23-E048.md. No old model or snapshot
will be edited. Production construction is conditional on the oracle gate.

Production details frozen before the oracle reading: select a single common
alpha from {0,.25,.5} for all four eligible parents, on the pooled final output
including every PREDICT item. Visible rows are shuffled with seed4801; first
min(600,n//10) selection and next min(400,n//10) audit rows are removed from
all shadow E041 fits and PFN references. Reference subset: first512 remaining
rows of that fixed shuffle, same budget after the final visible-data refit.
Selection requires paired respondent mean log gain >max(.001,2*SE), separate
audit >max(0,SE); otherwise exact E041. Alpha freezes before the final refit.
No threshold changes in response to clean/sim/observed outcomes. UNICEF/WB
call the immutable E041 path. All external weights load once at module import;
sequential item estimators reuse a preloaded spec. Fit intermediates may be
cached locally when replaying the same shadow gate renderer at three alphas.
Changing a parent mixes PFN with its complete E041 parent belief (including
retrieval); soft routing and descendant evidence remain E041. Do not blend
PFN into an intermediate base and claim selection/deployment parity.

## Result

Compatible isolated package: tabpfn8.0.8/common-utils0.2.23; original V2
checkpoint 29,016,968 bytes, SHA256
f65a35685aeef42e31b796d9bfa34e68d6fc780bc98e7bff7763802964cf435f.
Socket-blocked import succeeds; import5.62s, weight load.107s; synthetic
512-reference/512-query/17-feature smoke6.91s on CPU2 threads. These establish
feasibility only. Full baseline environment unchanged.

Observed Adult seeds49/50, fixed frozen library:
- Query/section oracle skill/3 +.008285992/+.007461967: permissive gate passes.
- Tighter constant-section oracle skill/3 +.001362032/+.001414845: both <.005.
- Honest constant-section selection audit skill +.001156298/+.002285258.
- Standalone supported-head PFN skill -.009697424/-.008079412 vs logistic.

Raw arrays and outputs: docs/analysis/E048-outputs/. The tighter oracle also
contains the proposed common-alpha policy, so the larger permissive bound
cannot justify constructing that estimator. These are Adult-family readings,
not a UNHCR or foundation-model universal ceiling. Source/license/API evidence
is preserved separately with the analysis outputs.
The historical oracle-summary.json reports only the permissive script gate;
decision.json explicitly supersedes its proceed decision with the tighter
constant-policy stop, preserving original measured hashes and provenance.

## Decision

Parked at the tighter constant-mixture ceiling; no E048 production estimator
or submission ZIP. Do not silently replace its registered common-alpha
policy after reading outcomes. A separately registered E049 may test a
respondent-dependent policy within the broader query/section family. Both
the reuse of exploratory rows and the negative standalone PFN readings must
remain disclosed. No .65 forecast follows from this screen.
