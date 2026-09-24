# E052 - Fixed evidence-routing interaction control
parent: E041
status: parked
date: 2026-09-24

## Hypothesis

Applying unchanged E041 donor evidence once to each fully base-routed answer,
instead of also propagating evidence-updated parent beliefs through downstream
gates, can reduce harmful routing interactions on approximate UNHCR gates.

## Domain check

Registered after E050/E051 oracle failures and BEFORE E052 library execution.
Those failures remain stops, not changed gates. E052 is a fixed structural
intervention with no newly fitted selector, weights, threshold or donor bank.
It is eligible only as explicitly labeled exploration under the user's daily
slot preference, not an adopted model or a purported oracle-qualified learner.

Loss-map fit: historical E025 .79 base + .10 evidence shows both sources matter;
.079 gated residual locates the interaction, including asked-answer content.
These do not decompose E041's .92. ERPIS gates are approximate, median agreement
.83 and range .29-.98 (CLAUDE.md and docs/domain.md section9). The same donor
information can enter a child's answer through a predicted parent and through
the child's own evidence mixture. Removing the former may help or hurt; this
is not a mathematical claim that the original convex mixture double-counts
probability. Exact gates may benefit from parent evidence.

Keep all E041 base fits, retrieval metrics, donor sets/ties, per-item bucket
lambdas, gate agreement and conditional heads. E041 output is
F_i=(1-lambda_i)*G_i(F_parent)+lambda_i*e_i. E052 first renders
B_i=G_i(B_parent) with no evidence in any PREDICT belief, then returns
Q_i=(1-lambda_i)*B_i+lambda_i*e_i using the ORIGINAL E041 lambdas/evidence.
For a child, the difference is (1-lambda_i)*a_i times the difference between
base-parent and E041-parent asked probability, multiplied by concat(cond_i,-1).
This excludes all ancestor evidence from routing, not only the immediate edge.
No hard-gate change or recalibration occurs. Own-item evidence is preserved.

Ungated heads and heads with GIVEN parents must remain raw-exact E041; so must
an entire component whose PREDICT ancestors have no effective evidence.
Child lambda1 or gate agreement0 implies algebraic equality. Return original
raw vectors where structurally unchanged to avoid normalization-only changes.
UNICEF/WB delegate to frozen E041 exactly. Reject malformed partial-block cases
to E041 rather than inventing an ordering. All-zero evidence gives exact E041.

Pre-production channel: construct and freeze the TWO fixed endpoints, no fitted
estimator, on official clean UNHCR and unchanged household seed13. Check exact
E041 snapshot parity, score actual fixed intervention, changed-vector scope,
and exact constant-component two-arm oracle (same PREDICT components as E050).
This oracle bounds only an optional component selector on these simulations.
If skill/3 <=.005, do not build such a selector. A fixed diagnostic intervention
does not acquire adoption status from that bound. Flat observed Adult must be
identical by construction and is not an efficacy channel for this mechanism;
do not invent gates or substitute another favorable observed dataset.

E028 changed parent-value conditional decoding; E036 changed relation-specific
lambdas; E042/E047 added final evidence mass. None isolates the routing of
existing parent evidence while keeping own-item evidence and lambdas fixed.
This intervention does not repair A006's replay fitting procedure.

## Change

First build diagnostic endpoint helper/tests and screen. After results and
review, a separate new src/models wrapper may expose the SAME fixed endpoint
for exploration if clean <=.002 vs E041/E025, actual active parity, ZIP checker,
official all3 and combined runtime<900s pass. No post-result intensity grid.
If technical or no-regression checks fail, stop this configuration.

## Hosted reading arms (registered before upload)

Planning anchor Grand .64; .65+ favorable scenario, not a calibrated forecast.
Grand>=.65 with best update: retain winning bytes; reduced upstream evidence
routing improved the complete pipeline, not proof of the specific cause.
Grand .64 with best update: preserve bytes; inspect newly available scores.
Grand .64 without update: unresolved at display/noise resolution; keep E041,
park E052, no blind routing-intensity grid. Grand<=.63: adverse intervention,
retain upstream routing. Failed build/runtime is a technical result, not skill.
UNHCR-only approximate translation3*Grand delta, resolution about.015-.03;
never fabricate hidden instrument values or activation from a flat reading.

## Result

Not run at registration. Static algebra/history review found no blocker for
this scoped exploratory control; no measured improvement or hosted forecast.

## Decision

Parked, not adopted. No estimator is authorized by a failed oracle. Fixed
exploratory packaging remains conditional on all required technical checks.
