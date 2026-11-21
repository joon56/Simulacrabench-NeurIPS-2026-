"""E063: one query-wave metric; original E041 fallback/base/policies preserved."""
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, softmax
from threadpoolctl import threadpool_limits

from src.models import supervised_retrieval as original
from src.models.supervised_retrieval import (
    hh_cap, link_sharp, hh_sharp_layer, estimate_weights, _layout,
    _sig_data_all, _topk_excl, CAL_QUERIES, CAL_SEED, _evidence, EV_FLOOR,
    _max_q, _best_lambda, CONC_SPLIT, candidate_indices, _groups, _retrieval_log,
    RETRIEVAL_K, FIT_QUERIES, SELECT_QUERIES, REPLAY_QUERIES,
    METRIC_ITERATIONS, METRIC_PENALTY, MIN_SECTION_GAIN,
)

LAST_DIAGNOSTICS = {}


def round_posterior(features, weights, waves):
    """Use declared raw-wave indices, never factorized GIVEN codes."""
    return softmax(np.einsum("qkd,qd->qk", features, weights[waves]), axis=1)


def metric_objective(params, features, matches, prior_truth, sizes, initial, waves):
    d = len(initial)
    weights, share = params[:-1].reshape(2, d), expit(params[-1])
    posterior = round_posterior(features, weights, waves)
    evidence = np.einsum("qk,qki->qi", posterior, matches)
    scale = 1.0 - EV_FLOOR * np.asarray(sizes)
    probability = EV_FLOOR + scale * ((1-share) * prior_truth + share * evidence)
    center = weights.mean(axis=0) - initial
    delta = weights[0] - weights[1]
    loss = -np.log(probability).mean() + METRIC_PENALTY * (np.mean(center**2) + np.mean(delta**2))
    derivative = -scale / probability / probability.size
    donor_gradient = np.einsum("qi,qki->qk", share * derivative, matches)
    score_gradient = posterior * (donor_gradient - (posterior * donor_gradient).sum(axis=1, keepdims=True))
    row_gradient = np.einsum("qk,qkd->qd", score_gradient, features)
    gradient = np.stack([row_gradient[waves == r].sum(axis=0) for r in (0, 1)])
    gradient += METRIC_PENALTY * center / d
    gradient[0] += 2 * METRIC_PENALTY * delta / d
    gradient[1] -= 2 * METRIC_PENALTY * delta / d
    eta = np.sum(derivative * (evidence-prior_truth)) * share * (1-share)
    return float(loss), np.r_[gradient.ravel(), eta]


def _round_retrieval_log(features, matches, prior, sizes, weights, share, waves):
    posterior = round_posterior(features, weights, waves)
    evidence = np.einsum("qk,qki->qi", posterior, matches)
    probability = (1-share) * prior + share * evidence
    return np.log(EV_FLOOR + (1-EV_FLOOR*np.asarray(sizes)) * probability)


def round_support(frame, schema):
    """GIVEN-only support gate; all fallback decisions precede base/H fitting."""
    records = schema["items"]
    predicted = [n for n, rec in records.items() if rec["class"] == "PREDICT"]
    hidden = frame[predicted].isna().any(axis=1).to_numpy()
    visible, held = np.flatnonzero(~hidden), np.flatnonzero(hidden)
    result = {"eligible": False, "visible": len(visible), "held": len(held)}
    if len(visible) < 500 or not len(held):
        return None, dict(result, reason="original small-input/no-query fallback")
    wave = records.get("wave", {})
    if wave.get("class") != "GIVEN" or wave.get("values") != ["1", "2"] or "wave" not in frame:
        return None, dict(result, reason="unsupported wave schema")
    if sum(rec["class"] == "GIVEN" for rec in records.values()) != 17:
        return None, dict(result, reason="unsupported GIVEN width")
    if not frame["wave"].isin(["1", "2"]).all():
        return None, dict(result, reason="unsupported/unknown wave")
    waves = frame["wave"].map({"1": 0, "2": 1}).to_numpy(dtype=int)
    shuffled = np.random.default_rng(4101).permutation(visible)
    nf = min(FIT_QUERIES, max(1, len(visible)//5))
    ns = min(SELECT_QUERIES, max(1, len(visible)//10))
    nr = min(REPLAY_QUERIES, max(1, len(visible)//10))
    fit, select = shuffled[:nf], shuffled[nf:nf+ns]
    counts = {"fit": np.bincount(waves[fit], minlength=2).tolist(),
              "select": np.bincount(waves[select], minlength=2).tolist()}
    width = min(RETRIEVAL_K, len(visible)-nf-ns-nr)
    result.update(wave_support=counts, fit_donor_width=width)
    if width != 32 or any(n < 30 for counts_for_role in counts.values() for n in counts_for_role):
        return waves, dict(result, reason="fixed round support/donor width")
    return waves, dict(result, eligible=True, reason="supported")


def fit_sections(codes, labels, bank, fit, select, initial, sizes, groups, waves,
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
            start = np.r_[np.tile(np.clip(initial, 0, 12), 2), 0.]
            fitted = minimize(metric_objective, start,
                              args=(features[:nf], matches[:nf], pr[:nf], dim, initial, waves[fit]),
                              jac=True, method="L-BFGS-B",
                              bounds=[(0., 12.)] * (2 * len(initial)) + [(-5., 5.)],
                              options={"maxiter": maxiter, "ftol": 1e-7})
            if not np.isfinite(fitted.x).all():
                learned.append(np.stack((initial.copy(), initial.copy())))
                diagnostics.append({"selected": False, "reason": "nonfinite fit"})
                continue
            weights, share = fitted.x[:-1].reshape(2, -1).copy(), float(expit(fitted.x[-1]))
            learned.append(weights)
            old = _retrieval_log(features[nf:, :old_k], matches[nf:, :old_k], pr[nf:], dim,
                                 initial, old_share).mean(axis=1)
            new = _round_retrieval_log(features[nf:], matches[nf:], pr[nf:], dim,
                                 weights, share, waves[select]).mean(axis=1)
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


def _replace_evidence(evidence, frame, records, items, options, codes,
                      query, bank, initial, predicted, groups, learned, active, waves):
    if not active:
        return evidence
    donors = candidate_indices(codes, initial, query, bank, k=RETRIEVAL_K)
    features = (codes[query, None, :] == codes[donors]).astype(float)
    for group_idx in active:
        posterior = round_posterior(features, learned[group_idx], waves[query])
        post = [(positions, weights) for positions, weights in zip(donors, posterior)]
        selected_items = [predicted[i] for i in groups[group_idx]]
        evidence.update(_evidence(frame, selected_items, records, options, post, query))
    return evidence


def round_layer(frame, schema, model_dists):
    records, items, options = _layout(frame, schema)
    waves = frame["wave"].map({"1": 0, "2": 1}).to_numpy(dtype=int)
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
                                                initial, sizes, groups, waves)
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
                               cal, visible, initial, predicted, groups, learned, active, waves)
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
                           held, visible, initial, predicted, groups, learned, active, waves)
    conc = _max_q(post) >= CONC_SPLIT
    rows = {position: ({item: ev[item][i] for item in ev}, bool(conc[i]))
            for i, position in enumerate(held)}
    return rows, lam



def predict(frame, schema, cols=None, kappas=None):
    LAST_DIAGNOSTICS.clear()
    if "s3_11_intent_return_12m_lbl" not in schema["items"]:
        LAST_DIAGNOSTICS.update(eligible=False, reason="exact E041 control")
        return original.predict(frame, schema, cols=cols, kappas=kappas)
    _, support = round_support(frame, schema)
    LAST_DIAGNOSTICS.update(support)
    if not support["eligible"]:
        return original.predict(frame, schema, cols=cols, kappas=kappas)
    return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                              layer_fn=round_layer, configs=hh_cap.CONFIGS)

