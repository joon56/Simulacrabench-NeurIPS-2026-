# E054 independent design review

Reviewed 2026-09-24: E054 preregistration and A013 Task 1 as dispatched at
`a29fa9f`; current working-copy documents, CLAUDE.md, status, top three log
entries, existing probes, official score.py/config and public schemas.
No fits, hidden labels, noise recovery, or production edits. Git HEAD lookup
was blocked by repository ownership; no global Git setting was changed.

## Verdict

The preregistered algebra and noise-envelope design are sound under their
stated assumptions. An existential information-gate PASS is only permission
to prepare the registered measurement. It does not establish expected value
of a submission, probable informativeness, recoverable gain, or which gate
versus content mechanism should receive research effort. Numerical arm and
implementation review remains separate.

## Independent algebra and public constants

Write N for scored item count, U=mean(log K), s=N_G/N and
A=sum_G(log K)/(N U)=s(1-u). All PREDICT items are scored for every DEV row.
Replacing final gated vectors with uniform leaves uniform unchanged by the
official affine floor. Consequently P=H-s(skill_G-u), and

- L_G=s(1-skill_G)=A-H+P.
- L_C=(1-s)(1-skill_C)=1-A-P.
- L_G+L_C=1-H; D=L_G-L_C=2A-H+2P-1.
- D/3 is a Grand-equivalent difference in pooled loss, not an achievable gain.

The floor f gives per-item maximum correct probability 1-(K-1)f. Hence each
group's lower loss is sum_group[-log(1-(K-1)f)]/(N U); its upper loss is
group_share*(-log f)/U. Negative skill values remain physically possible.

Independent PowerShell UTF-8 schema computation (no project analysis import):

| Instrument | PREDICT / gated | U | Laplace scale b | t6 | t93 |
|---|---:|---:|---:|---:|---:|
| UNICEF | 12 / 7 | 1.562041821918335 | .000297194901576242 | .001422818137293181 | .002237381818439856 |
| World Bank | 76 / 30 | 2.018361563225098 | .000658164771332986 | .003150958408146703 | .004954882755753728 |
| UNHCR | 213 / 156 | 1.261752202679108 | .000881599371052733 | .004220649709356805 | .006636972550605420 |

UNHCR A=.7391182798263595; minimum L_G=.001700661446389479;
minimum L_C=.000615250988946145. These constants agree directly with the
official normalization and affine floor, not historical rounded probe values.

## Envelope and reporting conditions

Official public b=-log(f)/(n_DEV U epsilon), using respondent count, not scored
cell count. For Laplace noise, Pr(|noise|>t)=exp(-t/b), so choosing
t=b*log(m/.05) bounds the union event by .05 without independence assumptions.
The six-draw envelope covers a fixed baseline/probe pair. Selecting E041 as
the best among prior submissions invalidates interpreting that pairwise bound
as an unconditional post-selection 95% confidence guarantee.

The 93-draw sensitivity covers 30 prior submissions times three instruments
plus three probe draws, provided those counts and the public mechanism apply.
It protects selection among those readings through a simultaneous event; it
does not repair an unknown Grand mechanism, undocumented extra score noise,
different historical schemas, or changed true baseline/control predictions.
Adaptive submission choice does not by itself break the union bound when
each draw has the documented conditional tail bound.

Both Grand models must retain joint constraints from all baseline readings
.64/.52/.49/.92. Do not treat .52+.49+.92 as exact true control/baseline skills.
For averaging rounded instruments, keep cent-valued instrument readings
discrete and coupled to their true/noised values; a free continuous Grand
interval alone can admit impossible allocations. Closed rounding-bin bounds
are conservative at tie endpoints; report that convention. Avoid assuming
true skill lies in [0,1]: the floor permits negative skills.

Baseline/probe control true scores must be equal for the intended inversion.
This requires unchanged predictions, not merely unchanged source text if
training nondeterminism or environment differences change fitted outputs.
Release checks should establish local exactness; hosted reproducibility stays
an explicit assumption. Two Grand paths are sensitivity models, not an
exhaustive proof of the hosted reporting pipeline.

## Interpretation and recommendation risk

Use the same displayed Grand arm for the comparison across both reporting
orders, require feasibility in both, and require the same strict D>.015 or
D<-.015 conclusion under the complete 93-draw envelopes. An infeasible arm
must never pass vacuously. This is a defensible fixed test for the existence
of a resolvable arm; it is deliberately weaker than a guarantee of useful
information from the next slot.

Feasible passing arms may require almost all residual loss to sit in one
group, favorable control rounding, or extreme bounded noise. Counting
passing arms divided by feasible arms is not a probability. Optimistic
presentation of such arms can mislead even when the formal PASS is correct.
Report all unresolved arms, their loss intervals, and how restrictive the
passing arms are; do not invent a distribution over unknown true allocations.

Gated items include both sentinel outcomes and asked substantive answers.
Their pooled loss combines both; ungated items are only one part of content
prediction. Thus neither sign of D selects gate decoding versus answer-content
prediction. Prefer “gated-item loss” and “ungated-item loss”; calling L_C
“content loss” risks reviving the invalid E032 mechanism inference. Historical
E025 .079/.031 is not a prior constraint on E041. Even a large group loss is
not its reducible error, and item-group dominance does not identify a causal
repair, distinguish A011 replay mismatch, or resolve E053 transfer limits.

A useful follow-up would need a separately preregistered measurement that
isolates the targeted model operation, or a distinct coupled calibration
family with a valid held-out channel. E054 alone cannot supply that evidence.
