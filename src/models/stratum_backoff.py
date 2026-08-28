"""E004 — GIVEN-stratum backoff with interpolated smoothing, on top of
E002's gate coupling.

Each item's distribution is conditioned on a low-cardinality GIVEN stratum
and interpolated with the crowd marginal via a count-dependent weight
(Jelinek-Mercer): with n_s visible rows in stratum cell s,

    lambda_s = n_s / (n_s + kappa)
    p(v | s) = lambda_s * p_stratum(v | s) + (1 - lambda_s) * p_marginal(v)

Stratum selection rule (never hardcoded to an instrument): candidates are
GIVEN items with cardinality <= MAX_CARD. On an internal 20% holdout of
the complete visible rows, every single candidate is scored (best kappa on
a fixed grid); the best single is then tried in a pair with every other
candidate, and the pair is kept only if it beats the single. Selection
maximizes held-out log score of the interpolated full-marginal tables
(gate sentinel included as an ordinary level, so sentinel-predictive
strata like a survey round are visible to the rule).

Gate coupling is exactly E002's: per respondent, P(child = NA_GATED) =
1 - P(parent in observed_if) under the respondent's own parent belief,
with the asked-only conditional now stratum-conditioned as well. Because
parent beliefs become respondent-specific, gate chains on PREDICT parents
propagate stratum information downstream.
"""

import numpy as np
import pandas as pd

MAX_CARD = 12
KAPPA_GRID = (1.0, 3.0, 10.0, 30.0, 100.0)
HOLDOUT_FRAC = 0.2
HOLDOUT_SEED = 0


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
    """Per-stratum and global counts of `item` over the option list."""
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
    """dict stratum -> interpolated vector, plus the global marginal."""
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
    """Held-out log score (per kappa) of interpolated full-marginal tables."""
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


def select_stratum(frame, schema, kappa_grid=KAPPA_GRID, verbose=False):
    """Choose (strat_cols, kappa) on an internal holdout of visible rows."""
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
        return scores[kappa], kappa, scores

    results = {}
    base_score, _, _ = best([])  # no stratum = pure marginal baseline
    best_single, best_single_score, best_single_kappa = None, base_score, None
    for cand in candidates:
        score, kappa, scores = best([cand])
        results[cand] = (score, kappa, scores)
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
            score, kappa, _ = best([best_single, cand])
            if score > chosen_score:
                chosen = [best_single, cand]
                chosen_kappa, chosen_score = kappa, score
    if verbose:
        print(f"stratum selection: baseline {base_score:.4f}; chosen "
              f"{chosen} kappa={chosen_kappa} score {chosen_score:.4f}")
        for cand, (score, kappa, _) in sorted(results.items(),
                                              key=lambda t: -t[1][0]):
            print(f"  single {cand}: {score:.4f} (kappa {kappa})")
    return chosen, chosen_kappa


def predict(frame, schema, strat_cols=None, kappa=None):
    records, items, options = _layout(frame, schema)
    gated_value = schema["gated_value"]
    if strat_cols is None:
        strat_cols, kappa = select_stratum(frame, schema)
    if not strat_cols:
        kappa = kappa or KAPPA_GRID[0]

    complete = _complete_rows(frame, items)

    # Per-item tables: full marginal (sentinel incl.) for ungated use and
    # parent beliefs; asked-only conditional for gated items.
    marginal, mixed = {}, {}
    conditional, cond_mixed = {}, {}
    for item in items:
        gc, sc = _count_tables(complete, item, options[item], strat_cols)
        marginal[item], mixed[item] = _mixed(gc, sc, kappa)
        if records[item].get("gate"):
            asked_opts = list(records[item]["values"])
            gc_a, sc_a = _count_tables(complete, item, asked_opts, strat_cols)
            conditional[item], cond_mixed[item] = _mixed(gc_a, sc_a, kappa)

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
                belief[item] = np.append(p_asked * cond_table(item, key),
                                         1.0 - p_asked)
            out.append(belief[item])
    return out
