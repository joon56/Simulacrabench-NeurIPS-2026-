"""E005 — soft (agreement-weighted) gating on stratum-backoff tables.

E004's stratum conditioning makes gate parents respondent-specific, which
activates the gate cascade — including on instruments whose real gates are
approximate (unhcr: agreement median 0.83). E003's agreement weighting is
therefore mandatory here: per gated item,

    pred = a_i * hard_stratum + (1 - a_i) * soft_stratum

where hard_stratum is E004's gate-coupled vector, soft_stratum is the
stratum-conditioned full marginal (sentinel included), and a_i is the
beta-binomial-shrunk gate-agreement rate estimated from visible rows
(E003, ALPHA = 20). On exact-gate data a_i ~= 1 and this is E004.
"""

import numpy as np
import pandas as pd

from src.models.soft_gated_marginal import agreement_weights
from src.models.stratum_backoff import (
    KAPPA_GRID,
    _complete_rows,
    _count_tables,
    _layout,
    _mixed,
    select_stratum,
)


def predict(frame, schema, strat_cols=None, kappa=None):
    records, items, options = _layout(frame, schema)
    if strat_cols is None:
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

    weights, _ = agreement_weights(frame, schema)

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
