"""E041: supervised section-specific metrics over the E025 evidence pool.

Reference, fitting-query, selection and new-metric replay labels are disjoint.
The selector is a marginal/retrieval proxy: its section mixture shares are not
the deployed E025 per-item shares, and tied donors can differ from E025's old
sort policy. Full-stack outer evaluation is required. The retained E025 base
is still in-sample during lambda replay; this limitation is not repaired by
the new metric. No source module or incumbent snapshot is modified.
"""

import re
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, softmax
from threadpoolctl import threadpool_limits

from src.models import hh_cap, link_sharp
from src.models.hh_sharp import hh_sharp_layer
from src.models.hh_link import estimate_weights
from src.models.hier_backoff import _layout
from src.models.dup_link import _sig_data_all, _topk_excl, CAL_QUERIES, CAL_SEED
from src.models.prob_link import _evidence, EV_FLOOR
from src.models.link_sharp import _max_q, _best_lambda, CONC_SPLIT
from src.eval.retrieval_oracle import candidate_indices

RETRIEVAL_K = 32
FIT_QUERIES = 1200
SELECT_QUERIES = 800
REPLAY_QUERIES = 800
METRIC_ITERATIONS = 50
METRIC_PENALTY = .001
MIN_SECTION_GAIN = .003
LAST_DIAGNOSTICS = {}


def metric_objective(params, features, matches, prior_truth, sizes, initial):
    """Officially floored section log loss and analytic metric gradient."""
    sizes, initial = np.asarray(sizes), np.asarray(initial)
    weights, share = params[:-1], expit(params[-1])
    posterior = softmax(np.einsum("qkd,d->qk", features, weights), axis=1)
    evidence = np.einsum("qk,qki->qi", posterior, matches)
    scale = 1.0 - EV_FLOOR * sizes
    probability = EV_FLOOR + scale * ((1 - share) * prior_truth + share * evidence)
    residual = weights - initial
    loss = -np.log(probability).mean() + METRIC_PENALTY * np.mean(residual ** 2)
    derivative = -scale / probability / probability.size
    donor_gradient = np.einsum("qi,qki->qk", share * derivative, matches)
    score_gradient = posterior * (donor_gradient -
                                  (posterior * donor_gradient).sum(axis=1, keepdims=True))
    gradient_w = np.einsum("qk,qkd->d", score_gradient, features)
    gradient_w += 2 * METRIC_PENALTY * residual / len(weights)
    gradient_share = np.sum(derivative * (evidence - prior_truth)) * share * (1 - share)
    return float(loss), np.append(gradient_w, gradient_share)


def _retrieval_log(features, matches, prior, sizes, weights, share):
    posterior = softmax(np.einsum("qkd,d->qk", features, weights), axis=1)
    evidence = np.einsum("qk,qki->qi", posterior, matches)
    probability = (1 - share) * prior + share * evidence
    return np.log(EV_FLOOR + (1 - EV_FLOOR * np.asarray(sizes)) * probability)


def fit_sections(codes, labels, bank, fit, select, initial, sizes, groups,
                 k=RETRIEVAL_K, maxiter=METRIC_ITERATIONS,
                 min_gain=MIN_SECTION_GAIN):
    """Fit metric weights without selector labels; select on separate rows."""
    bank, fit, select = (np.asarray(x, dtype=int) for x in (bank, fit, select))
    if any(len(np.intersect1d(a, b)) for a, b in
           ((bank, fit), (bank, select), (fit, select))):
        raise ValueError("Reference, fit and selection rows must be disjoint")
    if min(len(bank), len(fit), len(select)) == 0:
        raise ValueError("Reference, fit and selection partitions must be nonempty")
    sizes = np.asarray(sizes)
    initial = np.maximum(np.asarray(initial, dtype=float), 0)
    query = np.concatenate((fit, select))
    donors = candidate_indices(codes, initial, query, bank, k=k)
    features = (codes[query, None, :] == codes[donors]).astype(float)
    nf = len(fit)
    priors = []
    for j, size in enumerate(sizes):
        counts = np.bincount(labels[bank, j], minlength=int(size)) + .5
        priors.append(counts / counts.sum())
    prior_truth = np.stack([p[labels[query, j]] for j, p in enumerate(priors)], axis=1)
    learned, active, diagnostics = [], [], []
    with threadpool_limits(limits=2):
        for group_idx, indices in enumerate(groups):
            ix = np.asarray(indices, dtype=int)
            matches = (labels[donors][:, :, ix] == labels[query][:, None, ix]).astype(float)
            pr = prior_truth[:, ix]
            dim = sizes[ix]
            # Both compared mixture shares are fitted without selection labels.
            grid = (0., .25, .5, .75, .9, .98)
            old_k = min(10, donors.shape[1])
            old_share = max(grid, key=lambda v: _retrieval_log(
                features[:nf, :old_k], matches[:nf, :old_k], pr[:nf], dim, initial, v).mean())
            start = np.append(np.clip(initial, 0, 12), 0.)
            fitted = minimize(metric_objective, start,
                              args=(features[:nf], matches[:nf], pr[:nf], dim, initial),
                              jac=True, method="L-BFGS-B",
                              bounds=[(0., 12.)] * len(initial) + [(-5., 5.)],
                              options={"maxiter": maxiter, "ftol": 1e-7})
            if not np.isfinite(fitted.x).all():
                learned.append(initial.copy())
                diagnostics.append({"selected": False, "reason": "nonfinite fit"})
                continue
            weights, share = fitted.x[:-1].copy(), float(expit(fitted.x[-1]))
            learned.append(weights)
            old = _retrieval_log(features[nf:, :old_k], matches[nf:, :old_k], pr[nf:], dim,
                                 initial, old_share).mean(axis=1)
            new = _retrieval_log(features[nf:], matches[nf:], pr[nf:], dim,
                                 weights, share).mean(axis=1)
            delta = new - old
            se = float(delta.std(ddof=1) / np.sqrt(len(delta))) if len(delta) > 1 else np.inf
            gain = float(delta.mean())
            selected = bool(gain > max(min_gain, 2 * se))
            if selected:
                active.append(group_idx)
            diagnostics.append({"selected": selected, "gain_log": gain,
                                "standard_error": se, "old_share": float(old_share),
                                "new_share": share, "iterations": int(fitted.nit)})
    return learned, active, diagnostics


def _groups(predicted):
    groups = {}
    for index, item in enumerate(predicted):
        match = re.match(r"s(\d+[a-z]?)_", item)
        groups.setdefault(match.group(1) if match else "other", []).append(index)
    return list(groups.values())


def _replace_evidence(evidence, frame, records, items, options, codes,
                      query, bank, initial, predicted, groups, learned, active):
    if not active:
        return evidence
    donors = candidate_indices(codes, initial, query, bank, k=RETRIEVAL_K)
    features = (codes[query, None, :] == codes[donors]).astype(float)
    for group_idx in active:
        posterior = softmax(np.einsum("qkd,d->qk", features, learned[group_idx]), axis=1)
        post = [(positions, weights) for positions, weights in zip(donors, posterior)]
        selected_items = [predicted[i] for i in groups[group_idx]]
        evidence.update(_evidence(frame, selected_items, records, options, post, query))
    return evidence


def supervised_layer(frame, schema, model_dists):
    records, items, options = _layout(frame, schema)
    predicted = [n for n in items if records[n]["class"] == "PREDICT"]
    hidden = frame[predicted].isna().any(axis=1).to_numpy()
    visible, held = np.flatnonzero(~hidden), np.flatnonzero(hidden)
    if len(visible) < 500 or len(held) == 0:
        return hh_sharp_layer(frame, schema, model_dists)
    codes, rarity = _sig_data_all(frame, records, items)
    if codes is None:
        return {}, {}
    cal = visible
    if len(cal) > CAL_QUERIES:
        cal = np.sort(np.random.default_rng(CAL_SEED).choice(cal, CAL_QUERIES, replace=False))
    preliminary = _topk_excl(codes, rarity, cal, visible)
    initial, _ = estimate_weights(codes, rarity, cal, preliminary)
    labels = np.stack([frame[n].map({v: i for i, v in enumerate(options[n])})
                       .fillna(-1).to_numpy(dtype=int) for n in predicted], axis=1)
    shuffled = np.random.default_rng(4101).permutation(visible)
    nfit = min(FIT_QUERIES, max(1, len(visible) // 5))
    nselect = min(SELECT_QUERIES, max(1, len(visible) // 10))
    nreplay = min(REPLAY_QUERIES, max(1, len(visible) // 10))
    fit, select = shuffled[:nfit], shuffled[nfit:nfit + nselect]
    replay = shuffled[nfit + nselect:nfit + nselect + nreplay]
    bank = shuffled[nfit + nselect + nreplay:]
    groups = _groups(predicted)
    sizes = [len(options[n]) for n in predicted]
    learned, active, diagnostics = fit_sections(codes, labels, bank, fit, select,
                                                initial, sizes, groups)
    LAST_DIAGNOSTICS.clear()
    LAST_DIAGNOSTICS.update({"sections": diagnostics, "active": active,
                             "fit_rows": len(fit), "selection_rows": len(select),
                             "reference_rows": len(bank), "replay_rows": len(replay)})
    original_cal = cal
    if active:
        cal = np.union1d(cal, replay)
    active_items = {predicted[i] for g in active for i in groups[g]}
    cal_post = _topk_excl(codes, initial, cal, visible)
    ev_cal = _evidence(frame, items, records, options, cal_post, cal)
    ev_cal = _replace_evidence(ev_cal, frame, records, items, options, codes,
                               cal, visible, initial, predicted, groups, learned, active)
    conc_cal = _max_q(cal_post) >= CONC_SPLIT
    lam = {}
    for j, item in enumerate(predicted):
        truth = labels[cal, j]
        eligible = replay if item in active_items else original_cal
        ok = (truth >= 0) & np.isin(cal, eligible)
        if not ok.any():
            continue
        rows = np.arange(ok.sum())
        p_model = np.maximum(model_dists[item][cal[ok]][rows, truth[ok]], EV_FLOOR)
        p_ev = ev_cal[item][ok][rows, truth[ok]]
        pair = [0., 0.]
        for bucket, mask in enumerate((~conc_cal[ok], conc_cal[ok])):
            if mask.sum() >= 30:
                pair[bucket] = _best_lambda(p_model[mask], p_ev[mask])
        if pair[0] > 0 or pair[1] > 0:
            lam[item] = tuple(pair)
    if not lam:
        return {}, {}
    post = _topk_excl(codes, initial, held, visible)
    ev = _evidence(frame, items, records, options, post, held)
    ev = _replace_evidence(ev, frame, records, items, options, codes,
                           held, visible, initial, predicted, groups, learned, active)
    conc = _max_q(post) >= CONC_SPLIT
    rows = {position: ({item: ev[item][i] for item in ev}, bool(conc[i]))
            for i, position in enumerate(held)}
    return rows, lam


def predict(frame, schema, cols=None, kappas=None):
    if "s3_11_intent_return_12m_lbl" not in schema["items"]:
        return hh_cap.predict(frame, schema, cols=cols, kappas=kappas)
    return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                              layer_fn=supervised_layer, configs=hh_cap.CONFIGS)
