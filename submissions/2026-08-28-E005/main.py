"""E005 — GIVEN-stratum backoff with soft (agreement-weighted) gate coupling.

Self-contained submission build of src/models/soft_stratum.py (which composes
src/models/stratum_backoff.py [E004] and src/models/soft_gated_marginal.py
[E003]). See docs/experiments/E003..E005 for the measurements behind it.

Per item, the answer distribution is conditioned on a data-selected GIVEN
stratum and interpolated with the crowd marginal (Jelinek-Mercer,
lambda = n/(n+kappa)); stratum and kappa are chosen at run time on an
internal 20% holdout of the complete visible rows. Gate coupling follows
the respondent's own parent belief (E002 recursion); because real gates can
be approximate, each gated item's hard-coupled vector is mixed with the
stratum full marginal by its beta-binomial-shrunk gate-agreement rate
estimated from visible rows.
"""

import numpy as np
import pandas as pd

MAX_CARD = 12
KAPPA_GRID = (1.0, 3.0, 10.0, 30.0, 100.0)
HOLDOUT_FRAC = 0.2
HOLDOUT_SEED = 0
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


def _count_tables(rows, item, options, strat_cols):
    opt_index = {o: i for i, o in enumerate(options)}
    k = len(options)
    global_counts = np.full(k, 0.5)
    strat_counts = {}
    codes = rows[item].map(opt_index)
    valid = codes.notna()
    codes = codes[valid].astype(int).to_numpy()
    np.add.at(global_counts, codes, 1.0)
    if strat_cols:
        keys = list(map(tuple, rows.loc[valid, strat_cols].to_numpy()))
        for key, code in zip(keys, codes):
            vec = strat_counts.get(key)
            if vec is None:
                vec = np.zeros(k)
                strat_counts[key] = vec
            vec[code] += 1.0
    return global_counts, strat_counts


def _mixed(global_counts, strat_counts, kappa):
    marginal = global_counts / global_counts.sum()
    mixed = {}
    for key, counts in strat_counts.items():
        n = counts.sum()
        lam = n / (n + kappa)
        p_s = (counts + 0.5) / (n + 0.5 * len(counts))
        mixed[key] = lam * p_s + (1.0 - lam) * marginal
    return marginal, mixed


def _holdout_score(fit_rows, eval_rows, predict_items, options, strat_cols,
                   kappa_grid):
    totals = {kappa: 0.0 for kappa in kappa_grid}
    cells = 0
    for item in predict_items:
        opts = options[item]
        opt_index = {o: i for i, o in enumerate(opts)}
        gc, sc = _count_tables(fit_rows, item, opts, strat_cols)
        eval_codes = eval_rows[item].map(opt_index)
        valid = eval_codes.notna()
        codes = eval_codes[valid].astype(int).to_numpy()
        keys = list(map(tuple, eval_rows.loc[valid, strat_cols].to_numpy()))
        cells += len(codes)
        for kappa in kappa_grid:
            marginal, mixed = _mixed(gc, sc, kappa)
            logp = 0.0
            for key, code in zip(keys, codes):
                vec = mixed.get(key)
                p = (vec if vec is not None else marginal)[code]
                logp += np.log(max(p, 1e-12))
            totals[kappa] += logp
    return {kappa: totals[kappa] / max(cells, 1) for kappa in kappa_grid}


def select_stratum(frame, schema, kappa_grid=KAPPA_GRID):
    records, items, options = _layout(frame, schema)
    predict_items = [n for n in items if records[n]["class"] == "PREDICT"]
    candidates = [n for n in items
                  if records[n]["class"] == "GIVEN"
                  and len(records[n]["values"]) <= MAX_CARD]
    complete = _complete_rows(frame, items)
    rng = np.random.default_rng(HOLDOUT_SEED)
    mask = rng.random(len(complete)) < HOLDOUT_FRAC
    fit_rows, eval_rows = complete[~mask], complete[mask]

    def best(strat_cols):
        scores = _holdout_score(fit_rows, eval_rows, predict_items, options,
                                strat_cols, kappa_grid)
        kappa = max(scores, key=scores.get)
        return scores[kappa], kappa

    base_score, _ = best([])
    best_single, best_single_score, best_single_kappa = None, base_score, None
    for cand in candidates:
        score, kappa = best([cand])
        if score > best_single_score:
            best_single, best_single_score, best_single_kappa = \
                cand, score, kappa

    chosen, chosen_kappa, chosen_score = [], None, base_score
    if best_single is not None:
        chosen = [best_single]
        chosen_kappa, chosen_score = best_single_kappa, best_single_score
        for cand in candidates:
            if cand == best_single:
                continue
            score, kappa = best([best_single, cand])
            if score > chosen_score:
                chosen = [best_single, cand]
                chosen_kappa, chosen_score = kappa, score
    return chosen, chosen_kappa


def agreement_weights(frame, schema):
    records = schema["items"]
    gated_value = schema["gated_value"]
    items = [n for n, r in records.items()
             if r["class"] in ("GIVEN", "PREDICT")]
    raw = {}
    counts = {}
    for item in items:
        gate = records[item].get("gate")
        if not gate or gate["parent"] not in frame.columns:
            continue
        parent = frame[gate["parent"]]
        child = frame[item]
        both = parent.notna() & child.notna()
        if not both.any():
            continue
        asked = parent[both].isin(gate["observed_if"])
        is_sentinel = child[both] == gated_value
        agree = (is_sentinel == ~asked).sum()
        raw[item] = agree / both.sum()
        counts[item] = (int(agree), int(both.sum()))
    if not raw:
        return {}
    m = float(np.median(list(raw.values())))
    return {item: (k + ALPHA * m) / (n + ALPHA)
            for item, (k, n) in counts.items()}


def predict(frame, schema):
    records, items, options = _layout(frame, schema)
    strat_cols, kappa = select_stratum(frame, schema)
    if not strat_cols:
        kappa = kappa or KAPPA_GRID[0]

    complete = _complete_rows(frame, items)

    marginal, mixed = {}, {}
    conditional, cond_mixed = {}, {}
    for item in items:
        gc, sc = _count_tables(complete, item, options[item], strat_cols)
        marginal[item], mixed[item] = _mixed(gc, sc, kappa)
        if records[item].get("gate"):
            asked_opts = list(records[item]["values"])
            gc_a, sc_a = _count_tables(complete, item, asked_opts, strat_cols)
            conditional[item], cond_mixed[item] = _mixed(gc_a, sc_a, kappa)

    weights = agreement_weights(frame, schema)

    def table(item, key):
        vec = mixed[item].get(key) if strat_cols else None
        return vec if vec is not None else marginal[item]

    def cond_table(item, key):
        vec = cond_mixed[item].get(key) if strat_cols else None
        return vec if vec is not None else conditional[item]

    out = []
    values = frame[items].to_numpy(dtype=object)
    strat_idx = [items.index(c) for c in strat_cols]
    for row in range(values.shape[0]):
        key = tuple(values[row, i] for i in strat_idx)
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
                belief[item] = table(item, key)
            else:
                parent_belief = belief[gate["parent"]]
                asked_idx = [options[gate["parent"]].index(o)
                             for o in gate["observed_if"]]
                p_asked = float(parent_belief[asked_idx].sum())
                hard = np.append(p_asked * cond_table(item, key),
                                 1.0 - p_asked)
                a = weights.get(item, 1.0)
                belief[item] = a * hard + (1.0 - a) * table(item, key)
            out.append(belief[item])
    return out
