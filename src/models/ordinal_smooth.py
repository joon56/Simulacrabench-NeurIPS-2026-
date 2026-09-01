"""E011 — ordinal kernel smoothing along the option axis, over E010.

Every current component pools across cells (ladder) or respondents
(logistic); nothing pools across ADJACENT OPTIONS. For items whose
options strict-parse as numbers (spans, counts, numeric scales), a
discrete Gaussian kernel over option RANKS redistributes mass among
numeric neighbours:

    M_h[i, j] ∝ exp(-(rank_i - rank_j)^2 / (2 h^2))   (numeric block)

Non-numeric options (worded levels, coded labels like '98. I don't
know', the gate sentinel) stay identity — mass never crosses between the
numeric block and anything else. Bandwidth h is selected PER ITEM on the
internal holdout from {off, 0.5, 1.0, 2.0}; off wins ties, so on data
with no ordinal structure (the sandbox couples trait to options with
random loadings — A004) the model degenerates to E010.

Detection rule (pre-registered in E011): >= K-1 options parse as float
and K >= 4 for the option list at hand.
"""

import numpy as np
import pandas as pd

from src.models.hier_backoff import (
    _layout, _complete_rows, _codes, build_ladder, ladder_lookup,
    select_ladder, HOLDOUT_SEED, HOLDOUT_FRAC,
)
from src.models.logit_blend import (
    _given_matrix, _fit_model, _proba, _floored, W_GRID,
)
from src.models.cond_agree import conditional_agreement

H_GRID = (0.5, 1.0, 2.0)  # 'off' (identity) is always in the running


def _numeric_ranks(options):
    """{option index: rank} over numerically-parsing options, or None
    if the list fails the detection rule (>= K-1 numeric, K >= 4)."""
    parsed = {}
    for i, v in enumerate(options):
        try:
            parsed[i] = float(str(v).strip())
        except ValueError:
            continue
    if len(options) < 4 or len(parsed) < len(options) - 1:
        return None
    order = sorted(parsed, key=parsed.get)
    return {idx: rank for rank, idx in enumerate(order)}


def kernel_matrix(options, h):
    """K x K row-stochastic matrix: Gaussian over ranks in the numeric
    block, identity elsewhere. None if the item is not ordinal."""
    ranks = _numeric_ranks(options)
    if ranks is None:
        return None
    k = len(options)
    M = np.eye(k)
    idx = np.array(sorted(ranks))
    r = np.array([ranks[i] for i in idx], dtype=float)
    block = np.exp(-((r[:, None] - r[None, :]) ** 2) / (2.0 * h * h))
    block /= block.sum(axis=1, keepdims=True)
    M[np.ix_(idx, idx)] = block
    return M


def tune_weight_and_bandwidth(frame, schema, cols, kappas):
    """One fitting pass on the internal holdout: instrument-level blend
    weight w (as E008), then per-item kernel bandwidth h given w.
    Returns (w, {item: h}) — items absent from the dict are 'off'."""
    records, items, options = _layout(frame, schema)
    predict_items = [n for n in items if records[n]["class"] == "PREDICT"]
    complete = _complete_rows(frame, items)
    rng = np.random.default_rng(HOLDOUT_SEED)
    mask = rng.random(len(complete)) < HOLDOUT_FRAC
    fit_rows, eval_rows = complete[~mask], complete[mask]
    if len(fit_rows) == 0 or len(eval_rows) == 0:
        return 0.0, {}

    X_fit = _given_matrix(fit_rows, records, items, options)
    X_eval = _given_matrix(eval_rows, records, items, options)

    per_item = {}
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
        per_item[item] = (model is not None, proba, ladder, codes_eval)

        cells += len(codes_eval)
        rows = np.arange(len(codes_eval))
        for w in W_GRID:
            mix = ladder if (model is None and w > 0) else \
                w * proba + (1.0 - w) * ladder
            totals[w] += np.log(_floored(mix)[rows, codes_eval]).sum()
    if cells == 0:
        return 0.0, {}
    w = max(totals, key=lambda x: totals[x] / cells)

    bandwidths = {}
    for item, (has_model, proba, ladder, codes_eval) in per_item.items():
        opts = options[item]
        if _numeric_ranks(opts) is None:
            continue
        mix = ladder if (not has_model and w > 0) else \
            w * proba + (1.0 - w) * ladder
        rows = np.arange(len(codes_eval))
        base = np.log(_floored(mix)[rows, codes_eval]).sum()
        best_h, best_score = None, base
        for h in H_GRID:
            M = kernel_matrix(opts, h)
            smoothed = mix @ M  # p' = p @ M, matching predict's M.T @ vec
            score = np.log(_floored(smoothed)[rows, codes_eval]).sum()
            if score > best_score:
                best_h, best_score = h, score
        if best_h is not None:
            bandwidths[item] = best_h
    return w, bandwidths


def predict(frame, schema, cols=None, kappas=None, w=None,
            bandwidths=None):
    records, items, options = _layout(frame, schema)
    if cols is None:
        cols, kappas, _ = select_ladder(frame, schema)
    if w is None or bandwidths is None:
        w, bandwidths = tune_weight_and_bandwidth(frame, schema,
                                                  cols, kappas)

    complete = _complete_rows(frame, items)
    if w > 0:
        X_complete = _given_matrix(complete, records, items, options)
        X_all = _given_matrix(frame, records, items, options)
    else:
        X_all = np.zeros((len(frame), 0))

    full_tables, cond_tables = {}, {}
    full_proba, cond_proba = {}, {}
    full_kernel, cond_kernel = {}, {}
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
        h = bandwidths.get(item)
        if h is not None:
            full_kernel[item] = kernel_matrix(opts, h)
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
            if h is not None:
                cond_kernel[item] = kernel_matrix(values, h)

    agreement = conditional_agreement(frame, schema)
    item_index = {item: i for i, item in enumerate(items)}

    def blended(tables, probas, kernels, item, key, row):
        p0, levels = tables[item]
        ladder = ladder_lookup(p0, levels, key)
        logit = probas[item][row]
        vec = ladder if logit.sum() <= 0 else \
            w * logit + (1.0 - w) * ladder
        M = kernels.get(item)
        return vec if M is None else M.T @ vec

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
                                       full_kernel, item, key, row)
            else:
                parent_belief = belief[gate["parent"]]
                asked_idx = [options[gate["parent"]].index(o)
                             for o in gate["observed_if"]]
                p_asked = float(parent_belief[asked_idx].sum())
                hard = np.append(
                    p_asked * blended(cond_tables, cond_proba,
                                      cond_kernel, item, key, row),
                    1.0 - p_asked)
                soft = blended(full_tables, full_proba, full_kernel,
                               item, key, row)
                entry = agreement.get(item)
                if entry is None:
                    a = 1.0
                else:
                    scalar, sel_col, table = entry
                    if sel_col is None:
                        a = scalar
                    else:
                        a = table.get(values[row, item_index[sel_col]],
                                      scalar)
                belief[item] = a * hard + (1.0 - a) * soft
            out.append(belief[item])
    return out
