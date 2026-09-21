"""E045: preserve E041 donors and selectively add learned-search donors.

E041 still determines section activation. Expanded metrics use fit labels only;
selection labels only decide whether each active section uses its fixed union.
"""

from types import FunctionType

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, logit
from threadpoolctl import threadpool_limits

from src.models import supervised_retrieval as parent


RETRIEVAL_K = parent.RETRIEVAL_K
METRIC_ITERATIONS = parent.METRIC_ITERATIONS
METRIC_PENALTY = parent.METRIC_PENALTY
MIN_SECTION_GAIN = parent.MIN_SECTION_GAIN
LAST_DIAGNOSTICS = {}


def candidate_union(codes, initial, search_weights, query, bank, k=RETRIEVAL_K):
    """Original K donors followed by distinct learned-search donors."""
    query, bank = np.asarray(query, dtype=int), np.asarray(bank, dtype=int)
    original = parent.candidate_indices(codes, initial, query, bank, k=k)
    searched = parent.candidate_indices(codes, search_weights, query, bank, k=k)
    width = min(2 * k, len(bank))
    donors = np.zeros((len(query), width), dtype=int)
    valid = np.zeros_like(donors, dtype=bool)
    for row, position in enumerate(query):
        ordered = []
        seen = {int(position)}
        for donor in np.concatenate((original[row], searched[row])):
            donor = int(donor)
            if donor not in seen:
                ordered.append(donor)
                seen.add(donor)
        count = min(width, len(ordered))
        if count:
            donors[row, :count] = ordered[:count]
            donors[row, count:] = ordered[0]
            valid[row, :count] = True
        elif width:
            donors[row] = int(bank[0])
    return donors, valid


def _masked_posterior(features, weights, valid):
    """Softmax with exact zero probability on padding positions."""
    scores = np.einsum("qkd,d->qk", features, weights)
    valid = np.asarray(valid, dtype=bool)
    peak = np.max(np.where(valid, scores, -np.inf), axis=1, keepdims=True)
    shifted = np.where(valid, scores - peak, -np.inf)
    mass = np.where(valid, np.exp(shifted), 0.)
    return np.divide(mass, mass.sum(axis=1, keepdims=True),
                     out=np.zeros_like(mass), where=mass.sum(axis=1, keepdims=True) > 0)


def union_objective(params, features, matches, prior_truth, sizes, initial, valid):
    """Floored union log loss and analytic diagonal-metric gradient."""
    sizes, initial = np.asarray(sizes), np.asarray(initial, dtype=float)
    weights, share = params[:-1], expit(params[-1])
    posterior = _masked_posterior(features, weights, valid)
    evidence = np.einsum("qk,qki->qi", posterior, matches)
    scale = 1.0 - parent.EV_FLOOR * sizes
    probability = parent.EV_FLOOR + scale * (
        (1 - share) * prior_truth + share * evidence)
    residual = weights - initial
    loss = -np.log(probability).mean() + METRIC_PENALTY * np.mean(residual ** 2)
    derivative = -scale / probability / probability.size
    donor_gradient = np.einsum("qi,qki->qk", share * derivative, matches)
    score_gradient = posterior * (
        donor_gradient - (posterior * donor_gradient).sum(axis=1, keepdims=True))
    gradient_w = np.einsum("qk,qkd->d", score_gradient, features)
    gradient_w += 2 * METRIC_PENALTY * residual / len(weights)
    gradient_share = np.sum(derivative * (evidence - prior_truth)) * share * (1 - share)
    return float(loss), np.append(gradient_w, gradient_share)


def _union_log(features, matches, prior, sizes, weights, share, valid):
    posterior = _masked_posterior(features, weights, valid)
    evidence = np.einsum("qk,qki->qi", posterior, matches)
    probability = (1 - share) * prior + share * evidence
    return np.log(parent.EV_FLOOR +
                  (1 - parent.EV_FLOOR * np.asarray(sizes)) * probability)


def fit_union_sections(codes, labels, bank, fit, select, initial, sizes, groups,
                       k=RETRIEVAL_K, maxiter=METRIC_ITERATIONS,
                       min_gain=MIN_SECTION_GAIN):
    """Retain E041 activation, fit unions on fit rows, select on held-out rows."""
    originals, active, base_diagnostics = parent.fit_sections(
        codes, labels, bank, fit, select, initial, sizes, groups,
        k=k, maxiter=maxiter, min_gain=min_gain)
    plans = [{"original": np.asarray(weight).copy(),
              "expanded": np.asarray(weight).copy(), "use_union": False}
             for weight in originals]
    diagnostics = [dict(entry) for entry in base_diagnostics]
    if not active:
        return plans, active, diagnostics

    bank, fit, select = (np.asarray(x, dtype=int) for x in (bank, fit, select))
    query = np.concatenate((fit, select))
    nf = len(fit)
    sizes = np.asarray(sizes)
    initial = np.maximum(np.asarray(initial, dtype=float), 0)
    priors = []
    for column, size in enumerate(sizes):
        counts = np.bincount(labels[bank, column], minlength=int(size)) + .5
        priors.append(counts / counts.sum())
    prior_truth = np.stack(
        [prior[labels[query, column]] for column, prior in enumerate(priors)], axis=1)

    with threadpool_limits(limits=2):
        for group_idx in active:
            indices = np.asarray(groups[group_idx], dtype=int)
            original = plans[group_idx]["original"]
            donors, valid = candidate_union(
                codes, initial, original, query, bank, k=k)
            features = (codes[query, None, :] == codes[donors]).astype(float)
            matches = (labels[donors][:, :, indices] ==
                       labels[query][:, None, indices]).astype(float)
            prior = prior_truth[:, indices]
            dimensions = sizes[indices]
            original_share = float(base_diagnostics[group_idx]["new_share"])
            start = np.append(np.clip(original, 0, 12),
                              logit(np.clip(original_share, 1e-6, 1 - 1e-6)))
            fitted = minimize(
                union_objective, start,
                args=(features[:nf], matches[:nf], prior[:nf], dimensions,
                      original, valid[:nf]),
                jac=True, method="L-BFGS-B",
                bounds=[(0., 12.)] * len(initial) + [(-5., 5.)],
                options={"maxiter": maxiter, "ftol": 1e-7})
            diagnostic = diagnostics[group_idx]
            if not np.isfinite(fitted.x).all() or not np.isfinite(fitted.fun):
                diagnostic.update({"use_union": False, "union_reason": "nonfinite fit",
                                   "original_share": original_share})
                continue

            expanded = fitted.x[:-1].copy()
            share = float(expit(fitted.x[-1]))
            plans[group_idx]["expanded"] = expanded
            old_donors = parent.candidate_indices(
                codes, initial, query, bank, k=k)
            old_features = (codes[query, None, :] == codes[old_donors]).astype(float)
            old_matches = (labels[old_donors][:, :, indices] ==
                           labels[query][:, None, indices]).astype(float)
            old = parent._retrieval_log(
                old_features[nf:], old_matches[nf:], prior[nf:], dimensions,
                original, original_share).mean(axis=1)
            new = _union_log(
                features[nf:], matches[nf:], prior[nf:], dimensions,
                expanded, share, valid[nf:]).mean(axis=1)
            delta = new - old
            standard_error = (float(delta.std(ddof=1) / np.sqrt(len(delta)))
                              if len(delta) > 1 else np.inf)
            gain = float(delta.mean())
            use_union = bool(gain > max(min_gain, 2 * standard_error))
            plans[group_idx]["use_union"] = use_union
            diagnostic.update({"use_union": use_union, "union_gain_log": gain,
                               "union_standard_error": standard_error,
                               "original_share": original_share, "new_share": share,
                               "union_iterations": int(fitted.nit)})
    return plans, active, diagnostics


def union_evidence(evidence, frame, records, items, options, codes,
                   query, bank, initial, predicted, groups, plans, active):
    """Build exact E041 evidence first, then replace selected sections by union."""
    originals = [plan["original"] for plan in plans]
    evidence = parent._replace_evidence(
        evidence, frame, records, items, options, codes, query, bank, initial,
        predicted, groups, originals, active)
    for group_idx in active:
        plan = plans[group_idx]
        if not plan["use_union"]:
            continue
        donors, valid = candidate_union(
            codes, initial, plan["original"], query, bank, k=RETRIEVAL_K)
        features = (codes[query, None, :] == codes[donors]).astype(float)
        posterior = _masked_posterior(features, plan["expanded"], valid)
        posteriors = [(row[mask], probability[mask])
                      for row, probability, mask in zip(donors, posterior, valid)]
        selected_items = [predicted[index] for index in groups[group_idx]]
        evidence.update(parent._evidence(
            frame, selected_items, records, options, posteriors, query))
    return evidence


# Names expected by the inherited E041 layer.
fit_sections = fit_union_sections
_replace_evidence = union_evidence

union_layer = FunctionType(
    parent.supervised_layer.__code__,
    dict(parent.supervised_layer.__globals__, fit_sections=fit_union_sections,
         _replace_evidence=union_evidence, LAST_DIAGNOSTICS=LAST_DIAGNOSTICS),
    name="union_layer", argdefs=parent.supervised_layer.__defaults__,
    closure=parent.supervised_layer.__closure__)


def predict(frame, schema, cols=None, kappas=None):
    if "s3_11_intent_return_12m_lbl" not in schema["items"]:
        return parent.predict(frame, schema, cols=cols, kappas=kappas)
    return parent.link_sharp.predict(
        frame, schema, cols=cols, kappas=kappas,
        layer_fn=union_layer, configs=parent.hh_cap.CONFIGS)
