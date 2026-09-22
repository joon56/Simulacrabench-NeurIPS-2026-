"""E047: guarded, respondent-adaptive evidence after the complete E041 stack.

Correction fit, selection and audit rows are hidden before the shadow first
stage. Accepted scaling and coefficients are frozen for the final E041 refit.
The final mixture does not re-enter gate propagation. Returned vectors are
not floored: the grader applies its floor once, as reproduced during fitting.
"""

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit

from src.models import supervised_retrieval as parent
from src.models import hh_cap, link_sharp
from src.models.hier_backoff import _layout

E047_FLOOR = .001
E047_PENALTY = .01
E047_SEED = 4701
E047_MARKER = "s3_11_intent_return_12m_lbl"
E047_LAST_DIAGNOSTICS = {}
LAST_DIAGNOSTICS = E047_LAST_DIAGNOSTICS


def e047_normalize(probability):
    probability = np.asarray(probability, dtype=float)
    return probability / probability.sum(axis=-1, keepdims=True)


def e047_features(base, evidence, names):
    """Seven label-free section features; absent evidence equals the base."""
    features = []
    for name in names:
        p = e047_normalize(base[name])
        q = e047_normalize(evidence.get(name, base[name]))
        k = p.shape[1]
        entropy_p = -(p * np.log(np.maximum(p, 1e-300))).sum(axis=1)
        entropy_q = -(q * np.log(np.maximum(q, 1e-300))).sum(axis=1)
        if k > 1:
            entropy_p /= np.log(k)
            entropy_q /= np.log(k)
        features.append(np.column_stack((entropy_p, entropy_q, p.max(axis=1),
                                         q.max(axis=1), (p * q).sum(axis=1),
                                         p.argmax(axis=1) == q.argmax(axis=1))))
    values = np.mean(features, axis=0)
    return np.column_stack((np.ones(len(values)), values))


def e047_objective(beta, features, p_base_truth, p_ev_truth, sizes):
    """Officially floored final-mixture loss and analytic coefficient gradient."""
    beta = np.asarray(beta, dtype=float)
    sigmoid = expit(features @ beta)
    alpha = .5 * sigmoid
    difference = p_ev_truth - p_base_truth
    scale = 1 - E047_FLOOR * np.asarray(sizes)
    probability = E047_FLOOR + scale * (p_base_truth + alpha[:, None] * difference)
    loss = -np.log(probability).mean() + E047_PENALTY * np.mean(beta[1:] ** 2)
    derivative = -(scale * difference / probability).sum(axis=1) / probability.size
    gradient = features.T @ (derivative * .5 * sigmoid * (1 - sigmoid))
    gradient[1:] += 2 * E047_PENALTY * beta[1:] / len(beta[1:])
    return float(loss), gradient


def e047_fit_section(features, p_base_truth, p_ev_truth, sizes):
    """Fit scaling and coefficients using correction-fit rows only."""
    features = np.asarray(features, dtype=float)
    center = features.mean(axis=0)
    scale = np.maximum(features.std(axis=0), .001)
    center[0], scale[0] = 0., 1.
    standardized = (features - center) / scale
    initial = np.zeros(features.shape[1])
    initial[0] = -2.
    fitted = minimize(e047_objective, initial,
                      args=(standardized, np.asarray(p_base_truth),
                            np.asarray(p_ev_truth), sizes),
                      jac=True, method="L-BFGS-B", bounds=[(-6., 6.)] * len(initial),
                      options={"maxiter": 50})
    beta = fitted.x if np.isfinite(fitted.x).all() else initial
    return {"center": center.tolist(), "scale": scale.tolist(), "beta": beta.tolist()}


def e047_alpha(policy, features):
    standardized = (np.asarray(features) - np.asarray(policy["center"])) / np.asarray(policy["scale"])
    return .5 * expit(standardized @ np.asarray(policy["beta"]))


def e047_apply(base, evidence, groups, policies):
    """Normalize active mixtures; preserve inactive raw probabilities exactly."""
    result = {name: values.copy() for name, values in base.items()}
    for section, policy in policies.items():
        names = groups[int(section)]
        alpha = e047_alpha(policy, e047_features(base, evidence, names))[:, None]
        for name in names:
            if name not in evidence:
                continue
            result[name] = e047_normalize((1 - alpha) * e047_normalize(base[name]) +
                                          alpha * e047_normalize(evidence[name]))
    return result


def e047_log_truth(probability, labels):
    probability = e047_normalize(probability)
    truth = probability[np.arange(len(probability)), labels]
    return np.log(E047_FLOOR + (1 - E047_FLOOR * probability.shape[1]) * truth)


def e047_gain_summary(delta, minimum, multiplier):
    gain = float(np.mean(delta))
    se = float(np.std(delta, ddof=1) / np.sqrt(len(delta))) if len(delta) > 1 else float("inf")
    threshold = max(minimum, multiplier * se)
    return {"gain_log": gain, "standard_error": se, "threshold": threshold,
            "accepted": bool(gain > threshold)}


def e047_fit_policies(base, evidence, labels, groups, fit, select, audit):
    """Fit per section, select honestly, then accept or reject the whole policy."""
    fit, select, audit = (np.asarray(rows, dtype=int) for rows in (fit, select, audit))
    if any(len(np.intersect1d(a, b)) for a, b in ((fit, select), (fit, audit), (select, audit))):
        raise ValueError("Correction fit, selection and audit rows must be disjoint")
    if min(len(fit), len(select), len(audit)) == 0:
        raise ValueError("Correction fit, selection and audit partitions must be nonempty")
    policies, sections = {}, []
    for section, names in enumerate(groups):
        if not any(name in evidence for name in names):
            sections.append({"selected": False, "reason": "no evidence"})
            continue
        features = e047_features(base, evidence, names)
        normalized_base = {name: e047_normalize(base[name]) for name in names}
        normalized_evidence = {name: e047_normalize(evidence.get(name, base[name])) for name in names}
        p_base = np.column_stack([normalized_base[name][fit, labels[name][fit]] for name in names])
        p_ev = np.column_stack([normalized_evidence[name][fit, labels[name][fit]] for name in names])
        policy = e047_fit_section(features[fit], p_base, p_ev, [base[name].shape[1] for name in names])
        # Selection labels are read only after coefficients/scaling have frozen.
        selection_base = {name: base[name][select] for name in names}
        selection_ev = {name: evidence[name][select] for name in names if name in evidence}
        candidate = e047_apply(selection_base, selection_ev, [names], {0: policy})
        delta = np.column_stack([
            e047_log_truth(candidate[name], labels[name][select]) -
            e047_log_truth(selection_base[name], labels[name][select]) for name in names]).mean(axis=1)
        summary = e047_gain_summary(delta, .001, 2.)
        sections.append({"selected": summary["accepted"], **summary})
        if summary["accepted"]:
            policies[section] = policy
    # Overall audit pools all predicted items, including unchanged sections.
    audit_base = {name: values[audit] for name, values in base.items()}
    audit_ev = {name: values[audit] for name, values in evidence.items()}
    candidate = e047_apply(audit_base, audit_ev, groups, policies)
    delta = np.column_stack([
        e047_log_truth(candidate[name], labels[name][audit]) -
        e047_log_truth(audit_base[name], labels[name][audit]) for name in base]).mean(axis=1)
    audit_summary = e047_gain_summary(delta, 0., 1.)
    diagnostics = {"sections": sections, "selected": list(policies), "audit": audit_summary,
                   "fit_rows": len(fit), "selection_rows": len(select), "audit_rows": len(audit)}
    return (policies if audit_summary["accepted"] else {}), diagnostics


def e047_shadow_split(frame, schema):
    """Remove original held rows, then hide all outer labels before any fit."""
    predicted = [name for name, record in schema["items"].items() if record["class"] == "PREDICT"]
    visible = np.flatnonzero(~frame[predicted].isna().any(axis=1).to_numpy())
    shadow = frame.iloc[visible].copy().reset_index(drop=True)
    shuffled = np.random.default_rng(E047_SEED).permutation(len(visible))
    nfit, nselect, naudit = (min(cap, len(visible) // 10) for cap in (1000, 600, 400))
    fit = shuffled[:nfit]
    select = shuffled[nfit:nfit + nselect]
    audit = shuffled[nfit + nselect:nfit + nselect + naudit]
    shadow.loc[np.concatenate((fit, select, audit)), predicted] = np.nan
    return shadow, visible, fit, select, audit


def e047_capture(frame, schema, cols=None, kappas=None):
    """Capture immutable E041 evidence while preserving its own renderer."""
    records, items, options = _layout(frame, schema)
    predicted = [name for name in items if records[name]["class"] == "PREDICT"]
    held = np.flatnonzero(frame[predicted].isna().any(axis=1).to_numpy())
    captured = {}

    def e047_layer(f, s, model_dists):
        rows, shares = parent.supervised_layer(f, s, model_dists)
        captured.update(rows)
        return rows, shares

    output = link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                                layer_fn=e047_layer, configs=hh_cap.CONFIGS)
    # All query PREDICT cells are blank (checked at the public entry point).
    base = {name: np.empty((len(held), len(options[name]))) for name in predicted}
    cursor = 0
    for row in range(len(held)):
        for name in predicted:
            base[name][row] = output[cursor]
            cursor += 1
    evidence = {}
    for row, position in enumerate(held):
        entry = captured.get(position)
        if entry is None:
            continue
        for name, values in entry[0].items():
            if name in base and np.asarray(values).sum() > 0:
                if name not in evidence:
                    evidence[name] = base[name].copy()
                evidence[name][row] = values
    return output, base, evidence, held


def predict(frame, schema, cols=None, kappas=None):
    E047_LAST_DIAGNOSTICS.clear()
    if E047_MARKER not in schema["items"]:
        return parent.predict(frame, schema, cols=cols, kappas=kappas)
    predicted = [name for name, record in schema["items"].items() if record["class"] == "PREDICT"]
    blank = frame[predicted].isna().to_numpy()
    held = blank.any(axis=1)
    if (~held).sum() < 4000 or not held.any() or not blank[held].all():
        return parent.predict(frame, schema, cols=cols, kappas=kappas)
    groups = [[predicted[i] for i in group] for group in parent._groups(predicted)]
    shadow, visible, fit, select, audit = e047_shadow_split(frame, schema)
    _, base, evidence, query = e047_capture(shadow, schema, cols=cols, kappas=kappas)
    if not evidence:
        E047_LAST_DIAGNOSTICS.update({"reason": "no shadow evidence"})
        return parent.predict(frame, schema, cols=cols, kappas=kappas)
    _, _, options = _layout(frame, schema)
    labels = {name: frame.iloc[visible[query]][name].map(
        {value: index for index, value in enumerate(options[name])}).to_numpy(dtype=int)
        for name in predicted}
    lookup = np.full(len(shadow), -1, dtype=int)
    lookup[query] = np.arange(len(query))
    policies, diagnostics = e047_fit_policies(base, evidence, labels, groups,
                                              lookup[fit], lookup[select], lookup[audit])
    E047_LAST_DIAGNOSTICS.update(diagnostics)
    if not policies:
        return parent.predict(frame, schema, cols=cols, kappas=kappas)
    output, base, evidence, query = e047_capture(frame, schema, cols=cols, kappas=kappas)
    if not evidence:
        E047_LAST_DIAGNOSTICS["reason"] = "no final evidence"
        return output
    mixed = e047_apply(base, evidence, groups, policies)
    active = {name for section in policies for name in groups[section] if name in evidence}
    result = list(output)
    for row in range(len(query)):
        for col, name in enumerate(predicted):
            if name in active:
                result[row * len(predicted) + col] = mixed[name][row]
    return result
