"""E009 — per-item blend weight + regularization grid over the E008 model.

E008 blends a full-GIVEN logistic with the E006 backoff ladder using one
weight per instrument and a fixed C=1.0. Here every PREDICT item gets its
own (C, w) pair, chosen jointly on the internal 20% holdout:

    for each C in C_GRID: fit the item's logistic on the 80% split
    score p = w * p_logit + (1 - w) * p_ladder on the 20% split
    (C_item, w_item) = argmax over the C x W grid

The chosen C refits on all complete rows; the chosen w applies to both
the item's full-table and asked-only conditional distributions, exactly
where E008's single w applied. Ladder, gate recursion, E003 softening,
and the E008 edge guards are unchanged.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from src.models.hier_backoff import (
    _layout, _complete_rows, _codes, build_ladder, ladder_lookup,
    select_ladder, agreement_weights, HOLDOUT_FRAC, HOLDOUT_SEED,
)
from src.models.logit_blend import (
    _given_matrix, _proba, _floored, W_GRID, MAX_ITER,
)

C_GRID = (0.3, 1.0, 3.0)


def _fit_model(X, codes, c_reg):
    if len(np.unique(codes)) < 2:
        return None
    model = LogisticRegression(C=c_reg, max_iter=MAX_ITER)
    model.fit(X, codes)
    return model


def tune_item_params(frame, schema, cols, kappas):
    """Per-item (C, w) from the internal holdout. Returns
    ({item: (C, w)}, {item: holdout score at the chosen pair})."""
    records, items, options = _layout(frame, schema)
    predict_items = [n for n in items if records[n]["class"] == "PREDICT"]
    complete = _complete_rows(frame, items)
    rng = np.random.default_rng(HOLDOUT_SEED)
    mask = rng.random(len(complete)) < HOLDOUT_FRAC
    fit_rows, eval_rows = complete[~mask], complete[mask]
    if len(fit_rows) == 0 or len(eval_rows) == 0:
        return ({item: (C_GRID[1], 0.0) for item in predict_items}, {})

    X_fit = _given_matrix(fit_rows, records, items, options)
    X_eval = _given_matrix(eval_rows, records, items, options)

    params, scores_at = {}, {}
    for item in predict_items:
        opts = options[item]
        k = len(opts)
        codes_fit, _ = _codes(fit_rows, item, opts)
        codes_eval, valid = _codes(eval_rows, item, opts)
        if len(codes_eval) == 0 or len(np.unique(codes_fit)) < 2:
            params[item] = (C_GRID[1], 0.0)
            continue

        p0, levels = build_ladder(fit_rows, item, opts, cols, kappas)
        keys = list(map(tuple, eval_rows.loc[valid, cols].to_numpy())) \
            if cols else [() for _ in codes_eval]
        ladder = np.stack([ladder_lookup(p0, levels, key) for key in keys])
        rows = np.arange(len(codes_eval))

        best = (None, -np.inf)
        for c_reg in C_GRID:
            model = _fit_model(X_fit, codes_fit, c_reg)
            proba = _proba(model, X_eval, k)[np.asarray(valid)]
            for w in W_GRID:
                mix = _floored(w * proba + (1.0 - w) * ladder)
                score = np.log(mix[rows, codes_eval]).mean()
                if score > best[1]:
                    best = ((c_reg, w), score)
        params[item] = best[0]
        scores_at[item] = best[1]
    return params, scores_at


def predict(frame, schema, cols=None, kappas=None, params=None):
    records, items, options = _layout(frame, schema)
    if cols is None:
        cols, kappas, _ = select_ladder(frame, schema)
    if params is None:
        params, _ = tune_item_params(frame, schema, cols, kappas)

    complete = _complete_rows(frame, items)
    any_logit = any(w > 0 for _, w in params.values())
    if any_logit:
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
        c_reg, w = params.get(item, (C_GRID[1], 0.0))
        full_tables[item] = build_ladder(complete, item, opts, cols, kappas)
        codes, _ = _codes(complete, item, opts)
        full_proba[item] = _proba(_fit_model(X_complete, codes, c_reg),
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
                    _fit_model(X_asked, codes_a, c_reg),
                    X_all, len(values))
            else:
                cond_proba[item] = np.zeros((X_all.shape[0], len(values)))

    weights = agreement_weights(frame, schema)

    def blended(tables, probas, item, key, row):
        p0, levels = tables[item]
        ladder = ladder_lookup(p0, levels, key)
        logit = probas[item][row]
        if logit.sum() <= 0:
            return ladder
        w = params[item][1]
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
