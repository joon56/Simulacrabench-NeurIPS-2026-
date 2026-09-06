"""E006 — hierarchical backoff ladder (MRP-lite) with soft gate coupling.

Partial pooling approximated by count smoothing: with an ordered list of
GIVEN columns c1..cD, level L conditions on (c1..cL) and uses the level
above as its prior,

    p_0 = smoothed global marginal
    p_L(v | cell) = (count_L(v) + kappa_L * p_{L-1}(v | parent)) / (n_L + kappa_L)

Column order and depth are selected greedily at run time (never hardcoded):
candidates are GIVEN items with cardinality <= MAX_CARD; at each depth the
column (and its kappa from KAPPA_GRID) that most improves held-out log
score on an internal 20% split of the complete visible rows is appended;
selection stops when no candidate improves, or at depth 3.

Gate handling is E005's: hard coupling through the respondent's own parent
belief, softened per gated item by its beta-binomial-shrunk gate-agreement
rate (ALPHA = 20); asked-only conditionals ride the same ladder.
"""

import numpy as np
import pandas as pd

MAX_CARD = 12
KAPPA_GRID = (1.0, 3.0, 10.0, 30.0, 100.0)
MAX_DEPTH = 3
HOLDOUT_FRAC = 0.2
HOLDOUT_SEED = 0
EVAL_CAP = 3000  # cap on holdout eval rows, keeps selection under budget
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
    """dict cell_tuple -> count vector over options (raw counts)."""
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
    """Return (p0, [level-1 dict, level-2 dict, ...]) of distributions."""
    codes, _ = _codes(rows, item, options)
    k = len(options)
    global_counts = np.full(k, 0.5)
    np.add.at(global_counts, codes, 1.0)
    p0 = global_counts / global_counts.sum()

    levels = []
    prev = None  # dict at L-1 (None means p0 for every parent)
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
                    prev_ladders, prefix_cols, cand, kappa_grid,
                    code_cache=None):
    """Held-out log score per kappa for extending the ladder by `cand`.

    prev_ladders: {item: (p0, levels)} for the fixed prefix — built once
    per depth, reused across candidates and kappas.

    Vectorized (2026-09-07, hosted-timeout response): cells are
    factorized once per candidate, per-item counts become a
    [cells, K] matrix, and every kappa is scored with numpy on the
    truth column. Same numbers as the original row loop — an unseen
    eval cell (or a cell with no valid fit answers, whose smoothed
    vector equals its parent) falls back to the prefix ladder exactly
    as before.
    """
    cols = prefix_cols + [cand]
    fit_keys = list(map(tuple, fit_rows[cols].to_numpy()))
    eval_keys = list(map(tuple, eval_rows[cols].to_numpy()))
    cell_id = {}
    fit_cell = np.empty(len(fit_keys), dtype=np.int64)
    for i, key in enumerate(fit_keys):
        fit_cell[i] = cell_id.setdefault(key, len(cell_id))
    eval_cell = np.array([cell_id.get(key, -1) for key in eval_keys],
                         dtype=np.int64)
    cell_keys = list(cell_id)
    n_cells = len(cell_keys)

    if code_cache is None:
        code_cache = {item: (_codes(fit_rows, item, options[item]),
                             _codes(eval_rows, item, options[item]))
                      for item in predict_items}
    totals = {kappa: 0.0 for kappa in kappa_grid}
    cells = 0
    for item in predict_items:
        opts = options[item]
        k = len(opts)
        p0, prev_levels = prev_ladders[item]
        (codes_fit, valid_fit), (codes, valid) = code_cache[item]
        M = np.zeros((n_cells, k))
        np.add.at(M, (fit_cell[np.asarray(valid_fit)], codes_fit), 1.0)
        n_cell = M.sum(axis=1)
        Pm = np.stack([ladder_lookup(p0, prev_levels, key[:-1])
                       for key in cell_keys]) if n_cells else \
            np.zeros((0, k))

        ce = eval_cell[np.asarray(valid)]
        cells += len(codes)
        seen = ce >= 0
        c_t = M[ce[seen], codes[seen]]
        n_t = n_cell[ce[seen]]
        p_t = Pm[ce[seen], codes[seen]]
        valid_keys = [key for key, ok in zip(eval_keys, np.asarray(valid))
                      if ok]
        fb_keys = [key[:-1] for key, s in zip(valid_keys, seen) if not s]
        fb_codes = codes[~seen]
        fb = np.array([ladder_lookup(p0, prev_levels, fk)[c]
                       for fk, c in zip(fb_keys, fb_codes)])
        fb_log = np.log(np.maximum(fb, 1e-12)).sum() if len(fb) else 0.0
        for kappa in kappa_grid:
            p = (c_t + kappa * p_t) / (n_t + kappa)
            totals[kappa] += np.log(np.maximum(p, 1e-12)).sum() + fb_log
    return {kappa: totals[kappa] / max(cells, 1) for kappa in kappa_grid}


def select_ladder(frame, schema):
    """Greedy (columns, kappas) selection on an internal holdout."""
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

    # depth-0 baseline: global marginal only
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

    code_cache = {item: (_codes(fit_rows, item, options[item]),
                         _codes(eval_rows, item, options[item]))
                  for item in predict_items}
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
                                     KAPPA_GRID, code_cache=code_cache)
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


def predict(frame, schema, cols=None, kappas=None):
    records, items, options = _layout(frame, schema)
    if cols is None:
        cols, kappas, _ = select_ladder(frame, schema)

    complete = _complete_rows(frame, items)
    full_tables, cond_tables = {}, {}
    for item in items:
        full_tables[item] = build_ladder(complete, item, options[item],
                                         cols, kappas)
        if records[item].get("gate"):
            cond_tables[item] = build_ladder(complete, item,
                                             list(records[item]["values"]),
                                             cols, kappas)

    weights = agreement_weights(frame, schema)

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
                p0, levels = full_tables[item]
                belief[item] = ladder_lookup(p0, levels, key)
            else:
                parent_belief = belief[gate["parent"]]
                asked_idx = [options[gate["parent"]].index(o)
                             for o in gate["observed_if"]]
                p_asked = float(parent_belief[asked_idx].sum())
                c0, clevels = cond_tables[item]
                hard = np.append(
                    p_asked * ladder_lookup(c0, clevels, key), 1.0 - p_asked)
                f0, flevels = full_tables[item]
                soft = ladder_lookup(f0, flevels, key)
                a = weights.get(item, 1.0)
                belief[item] = a * hard + (1.0 - a) * soft
            out.append(belief[item])
    return out
