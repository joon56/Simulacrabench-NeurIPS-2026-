"""HSCC submission — E008: full-GIVEN logistic conditionals blended with
the E006 hierarchical backoff ladder (MRP-lite) and E003 soft gating.

Self-contained copy of src/models/hier_backoff.py + src/models/logit_blend.py
(submission snapshot 2026-08-30). No bundled artifacts; scikit-learn is
pre-installed in the hosted image.

Per PREDICT item: a multinomial logistic regression on the one-hot-encoded
full GIVEN block, mixed in probability space with a greedy-selected
hierarchical count-backoff ladder (<= 3 GIVEN columns, per-level kappa),
one blend weight per instrument tuned on an internal 20% holdout.
Gates: hard coupling through the respondent's own parent belief, softened
per gated item by its beta-binomial-shrunk gate-agreement rate.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

# ---------------------------------------------------------------- ladder

MAX_CARD = 12
KAPPA_GRID = (1.0, 3.0, 10.0, 30.0, 100.0)
MAX_DEPTH = 3
HOLDOUT_FRAC = 0.2
HOLDOUT_SEED = 0
EVAL_CAP = 3000
ALPHA = 20.0


def _layout(frame, schema):
    gated_value = schema["gated_value"]
    records = schema["items"]
    items = [n for n, r in records.items()
             if r["class"] in ("GIVEN", "PREDICT")]
    options = {}
    for item in items:
        r = records[item]
        options[item] = list(r["values"]) + (
            [gated_value] if r.get("gate") else [])
    return records, items, options


def _complete_rows(frame, items):
    return frame[frame[items].notna().all(axis=1)]


def _codes(rows, item, options):
    opt_index = {o: i for i, o in enumerate(options)}
    codes = rows[item].map(opt_index)
    valid = codes.notna()
    return codes[valid].astype(int).to_numpy(), valid


def _level_counts(rows, item, options, cols):
    opt_index = {o: i for i, o in enumerate(options)}
    k = len(options)
    counted = (rows.groupby(cols, sort=False, observed=True)[item]
               .value_counts())
    out = {}
    for idx, n in counted.items():
        *cell, value = idx if isinstance(idx, tuple) else (idx,)
        code = opt_index.get(value)
        if code is None:
            continue
        key = tuple(cell)
        vec = out.get(key)
        if vec is None:
            vec = np.zeros(k)
            out[key] = vec
        vec[code] += n
    return out


def build_ladder(rows, item, options, cols, kappas):
    codes, _ = _codes(rows, item, options)
    k = len(options)
    global_counts = np.full(k, 0.5)
    np.add.at(global_counts, codes, 1.0)
    p0 = global_counts / global_counts.sum()

    levels = []
    prev = None
    for depth in range(1, len(cols) + 1):
        counts = _level_counts(rows, item, options, cols[:depth])
        kappa = kappas[depth - 1]
        table = {}
        for key, vec in counts.items():
            parent = p0 if prev is None else prev.get(key[:-1], p0)
            n = vec.sum()
            table[key] = (vec + kappa * parent) / (n + kappa)
        levels.append(table)
        prev = table
    return p0, levels


def ladder_lookup(p0, levels, key):
    for depth in range(len(levels), 0, -1):
        vec = levels[depth - 1].get(key[:depth])
        if vec is not None:
            return vec
    return p0


def _eval_candidate(fit_rows, eval_rows, predict_items, options,
                    prev_ladders, prefix_cols, cand, kappa_grid):
    cols = prefix_cols + [cand]
    eval_keys = list(map(tuple, eval_rows[cols].to_numpy()))
    totals = {kappa: 0.0 for kappa in kappa_grid}
    cells = 0
    for item in predict_items:
        opts = options[item]
        p0, prev_levels = prev_ladders[item]
        counts = _level_counts(fit_rows, item, opts, cols)
        codes, valid = _codes(eval_rows, item, opts)
        keys = [k for k, ok in zip(eval_keys, valid) if ok]
        cells += len(codes)
        parent_of = {key: ladder_lookup(p0, prev_levels, key[:-1])
                     for key in counts}
        for kappa in kappa_grid:
            table = {key: (vec + kappa * parent_of[key]) /
                     (vec.sum() + kappa)
                     for key, vec in counts.items()}
            logp = 0.0
            for key, code in zip(keys, codes):
                vec = table.get(key)
                if vec is None:
                    vec = ladder_lookup(p0, prev_levels, key[:-1])
                logp += np.log(max(vec[code], 1e-12))
            totals[kappa] += logp
    return {kappa: totals[kappa] / max(cells, 1) for kappa in kappa_grid}


def select_ladder(frame, schema):
    records, items, options = _layout(frame, schema)
    predict_items = [n for n in items if records[n]["class"] == "PREDICT"]
    candidates = [n for n in items
                  if records[n]["class"] == "GIVEN"
                  and len(records[n]["values"]) <= MAX_CARD]
    complete = _complete_rows(frame, items)
    rng = np.random.default_rng(HOLDOUT_SEED)
    mask = rng.random(len(complete)) < HOLDOUT_FRAC
    fit_rows, eval_rows = complete[~mask], complete[mask]
    if len(eval_rows) > EVAL_CAP:
        eval_rows = eval_rows.sample(EVAL_CAP, random_state=HOLDOUT_SEED)

    base_total, base_cells = 0.0, 0
    marginals = {}
    for item in predict_items:
        opts = options[item]
        codes_fit, _ = _codes(fit_rows, item, opts)
        gc = np.full(len(opts), 0.5)
        np.add.at(gc, codes_fit, 1.0)
        marginals[item] = gc / gc.sum()
        codes, _ = _codes(eval_rows, item, opts)
        base_total += np.log(np.maximum(marginals[item][codes], 1e-12)).sum()
        base_cells += len(codes)
    best_score = base_total / max(base_cells, 1)

    cols, kappas = [], []
    history = [(list(cols), list(kappas), best_score)]
    while len(cols) < MAX_DEPTH:
        prev_ladders = {item: build_ladder(fit_rows, item, options[item],
                                           cols, kappas)
                        for item in predict_items}
        best_step = None
        for cand in candidates:
            if cand in cols:
                continue
            scores = _eval_candidate(fit_rows, eval_rows, predict_items,
                                     options, prev_ladders, cols, cand,
                                     KAPPA_GRID)
            kappa = max(scores, key=scores.get)
            if scores[kappa] > best_score and (
                    best_step is None or scores[kappa] > best_step[2]):
                best_step = (cand, kappa, scores[kappa])
        if best_step is None:
            break
        cols.append(best_step[0])
        kappas.append(best_step[1])
        best_score = best_step[2]
        history.append((list(cols), list(kappas), best_score))
    return cols, kappas, history


def agreement_weights(frame, schema):
    records = schema["items"]
    gated_value = schema["gated_value"]
    items = [n for n, r in records.items()
             if r["class"] in ("GIVEN", "PREDICT")]
    raw, counts = {}, {}
    for item in items:
        gate = records[item].get("gate")
        if not gate or gate["parent"] not in frame.columns:
            continue
        parent, child = frame[gate["parent"]], frame[item]
        both = parent.notna() & child.notna()
        if not both.any():
            continue
        asked = parent[both].isin(gate["observed_if"])
        agree = ((child[both] == gated_value) == ~asked).sum()
        raw[item] = agree / both.sum()
        counts[item] = (int(agree), int(both.sum()))
    if not raw:
        return {}
    m = float(np.median(list(raw.values())))
    return {item: (k + ALPHA * m) / (n + ALPHA)
            for item, (k, n) in counts.items()}


# ------------------------------------------------------- logistic blend

W_GRID = tuple(round(0.1 * i, 1) for i in range(11))
C_REG = 1.0
MAX_ITER = 200
FLOOR = 1e-3


def _given_matrix(frame, records, items, options):
    given = [n for n in items if records[n]["class"] == "GIVEN"]
    enc = OneHotEncoder(categories=[options[g] for g in given],
                        handle_unknown="ignore", sparse_output=True)
    block = frame[given].astype(object).where(
        frame[given].notna(), "__NA__")
    return enc.fit_transform(block)


def _fit_model(X, codes, k):
    if len(np.unique(codes)) < 2:
        return None
    model = LogisticRegression(C=C_REG, max_iter=MAX_ITER)
    model.fit(X, codes)
    return model


def _proba(model, X, k):
    out = np.zeros((X.shape[0], k))
    if model is None:
        return out
    out[:, model.classes_] = model.predict_proba(X)
    return out


def _floored(p):
    k = p.shape[-1]
    eps = min(1.0, FLOOR * k)
    return (1.0 - eps) * p + eps / k


def tune_weight(frame, schema, cols, kappas):
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
        if logit.sum() <= 0:
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
