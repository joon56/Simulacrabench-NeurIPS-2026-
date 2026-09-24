# E050 design review

Read-only source review, 2026-09-24. No training, model edits, or commits.
Read CLAUDE.md, status, latest log entries, A009, E041 renderer/layer, E042/E047 oracles, and E049 cache implementation.

## Recommended bounded family

Root's proposed five arms are scientifically distinct from E042/E047:
identity; lambda=0; lambda=0.5*legacy_lambda; lambda=legacy_lambda+0.5*(1-legacy_lambda); lambda=1.
Apply each inside unchanged `link_sharp.predict` recursion, preserving donor vectors, learned metric, candidate ordering, concentration flags, base model, conditional agreement, and gate definitions. Score final vectors with actual official normalization/floor exactly once. This repairs selection's comparison target without claiming to replace every part of inherited inner replay.

Use connected components of the graph restricted to PREDICT-to-PREDICT gate edges. GIVEN parents are fixed boundaries. Each component contains all its PREDICT descendants; no edge crosses components. Choose one constant arm per component, initially without concentration-specific or respondent-feature selectors. Global arm renders can then be composed exactly by component. Do not use schema section labels as a substitute: a gate may cross sections.

Pre-estimator oracle: cache the five complete recursive predictions on frozen held-out rows; for each component, select the single arm maximizing its pooled final log score across all rows/cells. Sum component maxima and subtract identity total; normalize by all scored-cell count, schema U, and three instruments. This is the exact finite-family oracle over all componentwise fixed arm assignments, not merely a maximum of five global scores. Include identity in every component, making oracle gain nonnegative. It does not bound continuous lambdas, respondent-specific policies, new donors, or real HSCC headroom. Preserve registered >.005 three-instrument-equivalent screen; do not substitute E042's historical .005 log threshold.

## Honest calibration and validation

One shadow frame: hide the whole PREDICT block of calibration-fit, selection, and audit rows before *every* first-stage fit, metric activation, donor-label pool, replay, and conditional-agreement calculation. Freeze candidate outputs before looking at oracle answers. Use separate selection to choose component arms and audit to measure composed policy; if audit is used as a guard, call it acceptance data. If oracle uses the same audit answers, its later performance is exploratory, not untouched validation. Prefer a separate, preregistered oracle-screen partition when affordable.

After selection, freeze arm IDs before full visible refit. Legacy lambdas, evidence strength, metric activation, and concentration can shift at refit; frozen IDs are not frozen final mixture probabilities. Report this shift and changed-vector fraction. Actual learned held-out gain matters more than permissive oracle clearance. Clean/household channels remain simulations; household structure is injected. Adult's existing targets have no HSCC gates: actual E041 rendering on a flat converted schema checks learning and engineering only. Do not invent gate semantics to call it evidence for humanitarian recursion.

## Source findings and exact fallback

- `supervised_retrieval.py` tunes legacy lambda against full-head `model_dists` on rows included in base refit. Deployment blends evidence after conditional/full gate mixing; changed parent beliefs affect descendants. Neither E047's final-output blend nor its Adult oracle models this recursion.
- `_best_lambda` clips truth probabilities with `EV_FLOOR`; official scoring instead normalizes and mixes a flat floor. Use official final scoring for new selection. Do not double-floor cached vectors.
- Missing lambda pairs mean zero, but donor evidence may still exist. New positive arms can activate those items only when corresponding evidence is available. When **all** legacy lambdas are zero, E041 returns `({}, {})` before generating held-out evidence. Exposing dormant evidence requires an explicit new capture path and provenance tests; a plain layer wrapper cannot recover it. Preserve identical donor indices, tie handling, learned activation, and legacy concentration calculation.
- Cache identity output and return its original arrays for total rejection and unchanged components. Do not recompute nominal identity using an algebraically equivalent expression. Controls bypass candidate machinery through unchanged E041 dispatch.
- Verify component-composed outputs against an actual renderer run with the selected lambda map. This catches hidden dependencies and provides stronger evidence than graph inspection alone. Also verify masking invariance, all-zero legacy evidence, empty donors, complete-block checks, and forced nonidentity source/archive parity.

## Cost boundary

Use E049's **pattern**, without importing its PFN-heavy module: a private copy of renderer globals, cached `select_ladder`, `tune_and_train`, `_proba_maps`, `conditional_agreement`, and item/options-keyed ladders. Capture the supervised evidence layer once. Scope caches to one immutable frame/schema/configuration; recreate between shadow and final frame. No global monkeypatch, no cross-frame cache reuse. `tune_fn` overrides bypass the existing default memoization unless explicitly handled.

Budget: one shadow fit and one full visible fit; five cheap recursion passes per frame, no arm-specific base refits. Release shadow fitted products before full refit. Existing E049 demonstrated this caching architecture, not E050's runtime. Profile full three-instrument import+prediction and active path against shared 900s limit before packaging. Avoid multi-fold ensembles today.

E051 direct all-head HistGBM is independent content evidence but much broader computationally (up to 213 classifiers plus calibration/refit). Keep it separate from E050, preserve sentinel class coverage, measure fit/runtime before committing to all heads, and screen its exact finite component-mixture family. No score expectation follows from either design.
