"""E008 — full-GIVEN logistic conditionals blended with the E006 ladder.

The E006 hierarchical backoff ladder conditions on at most 3 GIVEN
columns. This model adds, per PREDICT item, a multinomial logistic
regression on the one-hot-encoded FULL GIVEN block (fit on complete
visible rows) and mixes the two in probability space,

    p = w * p_logit + (1 - w) * p_ladder,

with a single blend weight w per instrument tuned on the same internal
20% holdout the ladder selection uses (fit on 80%, floored log score of
the blended full-table distributions, grid search). Gate handling is
E006's, applied to the blended beliefs: hard coupling through the
respondent's own parent belief, softened by beta-binomial-shrunk gate
agreement; gated items get an asked-only conditional logistic as well.

Items whose training target is single-class keep w = 0 (ladder only).
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

from src.models.hier_backoff import (
    _layout, _complete_rows, _codes, build_ladder, ladder_lookup,
    select_ladder, agreement_weights, HOLDOUT_FRAC, HOLDOUT_SEED,
)

W_GRID = tuple(round(0.1 * i, 1) for i in range(11))
C_REG = 1.0
MAX_ITER = 200
FLOOR = 1e-3


def _given_matrix(frame, records, items, options):
    """One-hot encode the GIVEN block for every row of frame (sparse)."""
    given = [n for n in items if records[n]["class"] == "GIVEN"]
    enc = OneHotEncoder(categories=[options[g] for g in given],
                        handle_unknown="ignore", sparse_output=True)
    block = frame[given].astype(object).where(
        frame[given].notna(), "__NA__")
    return enc.fit_transform(block)


def _fit_model(X, codes, k):
    """Fit one multinomial logistic; None if the target is single-class."""
    if len(np.unique(codes)) < 2:
        return None
    model = LogisticRegression(C=C_REG, max_iter=MAX_ITER)
    model.fit(X, codes)
    return model


def _proba(model, X, k):
    """predict_proba expanded to the full option vector (absent classes 0)."""
    out = np.zeros((X.shape[0], k))
    if model is None:
        return out
    out[:, model.classes_] = model.predict_proba(X)
    return out


def _floored(p):
    """Approximate the grader's flat-mix floor for holdout scoring."""
    k = p.shape[-1]
    eps = min(1.0, FLOOR * k)
    return (1.0 - eps) * p + eps / k


def tune_weight(frame, schema, cols, kappas):
    """Grid-search the blend weight on the internal holdout.

    Fit logistic full-table models on the 80% split, score
    w*logit + (1-w)*ladder on the 20% split (floored log score, pooled
    over PREDICT cells). Returns (w, per-w mean log scores).
    """
    records, items, options = _layout(frame, schema)
    predict_items = [n for n in items if records[n]["class"] == "PREDICT"]
    complete = _complete_rows(frame, items)
    rng = np.random.default_rng(HOLDOUT_SEED)
    mask = rng.random(len(complete)) < HOLDOUT_FRAC
    fit_rows, eval_rows = complete[~mask], complete[mask]
    if len(fit_rows) == 0 or len(eval_rows) == 0:
        return 0.0, {w: 0.0 for w in W_GRID}  # too little data to tune

    X_fit = _given_matrix(fit_rows, records, items, options)
    X_eval = _given_matrix(eval_rows, records, items, options)

    totals = {w: 0.0 for w in W_GRID}
    cells = 0
    for item in predict_items:
        opts = options[item]
        k = len(opts)
        codes_fit, _ = _codes(fit_rows, item, opts)
        codes_eval, valid = _codes(eval_rows, item, opts)
        if len(codes_eval) == 0:
            continue
        model = _fit_model(X_fit, codes_fit, k)
        proba = _proba(model, X_eval, k)[np.asarray(valid)]

        p0, levels = build_ladder(fit_rows, item, opts, cols, kappas)
        keys = list(map(tuple, eval_rows.loc[valid, cols].to_numpy())) \
            if cols else [() for _ in codes_eval]
        ladder = np.stack([ladder_lookup(p0, levels, key) for key in keys])

        cells += len(codes_eval)
        rows = np.arange(len(codes_eval))
        for w in W_GRID:
            if model is None and w > 0:
                totals[w] += np.log(
                    _floored(ladder)[rows, codes_eval]).sum()
                continue
            mix = _floored(w * proba + (1.0 - w) * ladder)
            totals[w] += np.log(mix[rows, codes_eval]).sum()
    scores = {w: totals[w] / max(cells, 1) for w in W_GRID}
    best = max(scores, key=scores.get)
    return best, scores


def predict(frame, schema, cols=None, kappas=None, w=None):
    records, items, options = _layout(frame, schema)
    if cols is None:
        cols, kappas, _ = select_ladder(frame, schema)
    if w is None:
        w, _ = tune_weight(frame, schema, cols, kappas)

    complete = _complete_rows(frame, items)
    if w > 0:
        X_complete = _given_matrix(complete, records, items, options)
        X_all = _given_matrix(frame, records, items, options)
    else:
        X_all = np.zeros((len(frame), 0))

    full_tables, cond_tables = {}, {}
    full_proba, cond_proba = {}, {}
    for item in items:
        if records[item]["class"] != "PREDICT":
            continue
        opts = options[item]
        k = len(opts)
        full_tables[item] = build_ladder(complete, item, opts, cols, kappas)
        codes, _ = _codes(complete, item, opts)
        full_proba[item] = _proba(_fit_model(X_complete, codes, k),
                                  X_all, k) if w > 0 else np.zeros(
                                      (X_all.shape[0], k))
        if records[item].get("gate"):
            values = list(records[item]["values"])
            cond_tables[item] = build_ladder(complete, item, values,
                                             cols, kappas)
            asked = complete[complete[item] != schema["gated_value"]]
            if w > 0 and len(asked) > 0:
                codes_a, _ = _codes(asked, item, values)
                X_asked = _given_matrix(asked, records, items, options)
                cond_proba[item] = _proba(
                    _fit_model(X_asked, codes_a, len(values)),
                    X_all, len(values))
            else:
                cond_proba[item] = np.zeros((X_all.shape[0], len(values)))

    weights = agreement_weights(frame, schema)

    def blended(tables, probas, item, key, row):
        p0, levels = tables[item]
        ladder = ladder_lookup(p0, levels, key)
        logit = probas[item][row]
        if logit.sum() <= 0:  # single-class fallback
            return ladder
        return w * logit + (1.0 - w) * ladder

    out = []
    values = frame[items].to_numpy(dtype=object)
    col_idx = [items.index(c) for c in cols]
    for row in range(values.shape[0]):
        key = tuple(values[row, i] for i in col_idx)
        belief = {}
        for col, item in enumerate(items):
            v = values[row, col]
            if not pd.isna(v):
                vec = np.zeros(len(options[item]))
                vec[options[item].index(v)] = 1.0
                belief[item] = vec
                continue
            gate = records[item].get("gate")
            if gate is None:
                belief[item] = blended(full_tables, full_proba,
                                       item, key, row)
            else:
                parent_belief = belief[gate["parent"]]
                asked_idx = [options[gate["parent"]].index(o)
                             for o in gate["observed_if"]]
                p_asked = float(parent_belief[asked_idx].sum())
                hard = np.append(
                    p_asked * blended(cond_tables, cond_proba,
                                      item, key, row),
                    1.0 - p_asked)
                soft = blended(full_tables, full_proba, item, key, row)
                a = weights.get(item, 1.0)
                belief[item] = a * hard + (1.0 - a) * soft
            out.append(belief[item])
    return out
