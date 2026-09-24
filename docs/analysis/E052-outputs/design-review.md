# E052 mechanism review

2026-09-24; read-only review. No code changes or training. Checked E028, E036, E037, E042, E050 and E041 renderer/layer source.

**Verdict:** distinct, bounded structural ablation. Register as an exploratory fixed endpoint, not as a successful repair or a new estimator after failed E050/E051 screens. Existing local outcomes provide no expected hosted gain.

## Exact intervention

Let G_i(p) be unchanged E041 soft-gate/base decoder with parent belief p, e_i unchanged donor evidence, and l_i unchanged effective legacy lambda for the query's concentration bucket. Effective lambda is zero when evidence is absent or unusable.

- E041: F_i = (1-l_i) G_i(F_parent) + l_i e_i.
- Evidence-free recursive base: B_i = G_i(B_parent).
- E052: Q_i = (1-l_i) B_i + l_i e_i, applied once after B recursion finishes.

For a gated child, with agreement a_i and conditional answer vector c_i:

`Q_i - F_i = (1-l_i) * a_i * (asked(B_parent)-asked(F_parent)) * concat(c_i,-1)`.

This preserves own-item donor evidence and changes parent-route contribution only. Because c_i is unchanged and normalized, half the L1 vector difference is `(1-l_i)*a_i*abs(delta_asked)` (up to floating-point error). At deeper levels it removes all upstream evidence effects, not merely immediate parent's direct donor mixture.

Nongated heads, heads gated on observed GIVEN parents, a_i=0, l_i=1, and unchanged parent asked probability are identity cases. Flat Adult is identity and cannot measure efficacy. No evidence means exact E041 fallback. Retain original vectors directly for guaranteed identity cases; never floor intermediate beliefs.

## Historical scope and attribution

E028 replaced gate decoding with parent-value-conditioned sentinel/content tables; its renderer still propagated final parent beliefs. E036 partitioned lambda by same/cross-round relation, using the same recursion. Neither tests E052. E042/E047 blend additional evidence with already recursive final outputs; they cannot generally reconstruct evidence-free parent routes. E050 changes both own-item evidence and its propagation together; E052 separates those effects.

E037's cross-fitted isotonic sentinel recalibration is also different. Its historical negative readings do not upper-bound every gate intervention or this fixed endpoint; a truth-trained cross-fitted estimator is not a mathematical oracle over all models.

Related donor information may make parent-route and child evidence errors correlated. E041's construction is a mixture, so 'double-counting' is only a proposed explanation, not a proven probabilistic defect. E052 can also remove useful household/parent information. Approximate UNHCR gates motivate testing but do not predict direction. Historical .079 gated residual includes content errors and does not measure recoverable E052 headroom. Keeping legacy lambda intentionally leaves A006 in-sample replay and objective mismatch unchanged.

## Guard and measurement requirements

1. Fit/capture exact E041 once; render no-evidence endpoint with identical cached net/maps/ladders/agreement. Reuse original evidence rows/lambda without dormant evidence extraction, donor recomputation, recalibration, or changed sorting. Return controls through unchanged E041 dispatch.
2. Check algebra on a multi-level gate example, identity cases, missing evidence, normalization and sentinel order. Verify no-evidence rendering actually suppresses evidence at every ancestor. Confirm no in-place mutation of captured vectors or model globals.
3. Before packaging, report fixed endpoint pooled log/skill versus E041 on unchanged clean and household seed13; changed-vector fraction, effect by gate depth/section, and both helpful/harmful slices. These diagnostics are descriptive, not selection rules. No favourable simulator added after results.
4. Optional exact two-endpoint component oracle may select E041/E052 once per closed PREDICT dependency component. Report bound for that finite family only. Failed bound forbids that learned selector; it does not make fixed endpoint beneficial or justify a relaxed selector. Keep E050/E051 stops unchanged and their audit labels unopened.
5. A fixed exploratory submission can remain a diagnostic candidate if preregistered clean no-regression, controls, archive parity, official all-three checks, and combined 900s budget pass. It is not local adoption. State why submitting it despite weak or negative efficacy evidence is exploratory under the standing daily-artifact preference.
6. Predefine adverse/flat/favourable hosted readings without attributing exact hidden instrument scores or causal certainty to rounded/noised Grand. Flat does not establish no propagation value; favourable shows only endpoint association at available resolution. Do not forecast .65.

Compute is bounded: one fitted E041 stack plus one extra recursive rendering and final vector mixtures; no new learner or shadow training. Profile rather than assume the cached path's speed. Unchanged-root and forced changed-descendant source/archive parity are particularly useful attribution checks.
