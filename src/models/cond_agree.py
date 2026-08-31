"""E010 — conditional gate-agreement softening over the E008 model.

E003/E008 soften each gated item's hard gate coupling by a SCALAR
beta-binomial-shrunk agreement rate ã_i. Real unhcr agreement is
heterogeneous across rows (five multi-select families mark the sentinel
in round 2 only — schema's own statement), so here ã becomes conditional:

    per gated item, choose at most ONE GIVEN column (cardinality <= 12)
    by held-out Bernoulli log-likelihood of the agree indicator on a 20%
    split of the rows where parent and child are both visible; if no
    column beats the scalar baseline, keep the scalar.
    ã_i(v) = (k_v + ALPHA * ã_i) / (n_v + ALPHA)   [shrunk to the scalar]

Everything else — ladder, full-GIVEN logistic blend, per-instrument w,
gate recursion, guards — is E008 unchanged. On exact-gate data every
agreement is ~1, no column is selected, and the model degenerates to E008.
"""

import numpy as np
import pandas as pd

from src.models.hier_backoff import (
    _layout, _complete_rows, _codes, build_ladder, ladder_lookup,
    select_ladder, ALPHA, HOLDOUT_SEED,
)
from src.models.logit_blend import (
    _given_matrix, _fit_model, _proba, tune_weight,
)

COND_MAX_CARD = 12
COND_HOLDOUT_FRAC = 0.2


def _bernoulli_ll(y, p):
    p = np.clip(p, 1e-6, 1.0 - 1e-6)
    return float(np.sum(y * np.log(p) + (1 - y) * np.log(1.0 - p)))


def _value_table(values, y, shrink_to):
    table = {}
    for val in pd.unique(values):
        sel = values == val
        k, n = y[sel].sum(), sel.sum()
        table[val] = (k + ALPHA * shrink_to) / (n + ALPHA)
    return table


def conditional_agreement(frame, schema):
    """Per gated item: (scalar ã, selected column or None, {value: ã_v})."""
    records = schema["items"]
    gated_value = schema["gated_value"]
    items = [n for n, r in records.items()
             if r["class"] in ("GIVEN", "PREDICT")]
    candidates = [n for n in items
                  if records[n]["class"] == "GIVEN"
                  and len(records[n]["values"]) <= COND_MAX_CARD]

    raw = {}
    for item in items:
        gate = records[item].get("gate")
        if not gate or gate["parent"] not in frame.columns:
            continue
        parent, child = frame[gate["parent"]], frame[item]
        both = parent.notna() & child.notna()
        if not both.any():
            continue
        asked = parent[both].isin(gate["observed_if"])
        agree = ((child[both] == gated_value) == ~asked).to_numpy()
        raw[item] = (agree, frame.index[both])
    if not raw:
        return {}

    m = float(np.median([agree.mean() for agree, _ in raw.values()]))
    rng = np.random.default_rng(HOLDOUT_SEED)
    out = {}
    for item, (y, idx) in raw.items():
        k, n = y.sum(), len(y)
        scalar = (k + ALPHA * m) / (n + ALPHA)
        mask = rng.random(n) < COND_HOLDOUT_FRAC
        if mask.sum() == 0 or (~mask).sum() == 0:
            out[item] = (scalar, None, {})
            continue
        y_fit, y_eval = y[~mask], y[mask]
        scalar_fit = (y_fit.sum() + ALPHA * m) / (len(y_fit) + ALPHA)
        best_col, best_ll = None, _bernoulli_ll(
            y_eval, np.full(len(y_eval), scalar_fit))
        sub = frame.loc[idx]
        for col in candidates:
            v = sub[col].to_numpy(dtype=object)
            table = _value_table(v[~mask], y_fit, scalar_fit)
            p_eval = np.array([table.get(val, scalar_fit)
                               for val in v[mask]])
            ll = _bernoulli_ll(y_eval, p_eval)
            if ll > best_ll:
                best_col, best_ll = col, ll
        if best_col is None:
            out[item] = (scalar, None, {})
        else:
            v = sub[best_col].to_numpy(dtype=object)
            out[item] = (scalar, best_col, _value_table(v, y, scalar))
    return out


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

    agreement = conditional_agreement(frame, schema)
    item_index = {item: i for i, item in enumerate(items)}

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
