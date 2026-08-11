"""Gate-aware marginal baseline.

The crowd marginal ignores skip logic: it predicts the pooled frequency of
NA_GATED like any other level. But gating is deterministic — a child item
is asked iff the parent's answer is in gate.observed_if. So for each
respondent:

    P(child = NA_GATED) = 1 - P(parent answer in observed_if)
    P(child = v)        = P(asked) * P(v | asked)      for substantive v

where P(parent ...) uses that respondent's own belief about the parent —
a one-hot vector if the parent is visible, else the parent's predicted
distribution (computed first; schema order lists parents before children,
which also closes gate chains: a parent's NA_GATED mass is never in
observed_if, so it propagates into the child's NA_GATED mass).

P(v | asked) is the smoothed crowd distribution among respondents who were
actually asked. Everything else is identical to the plain marginal.
"""

import numpy as np
import pandas as pd


def predict(frame, schema):
    gated_value = schema["gated_value"]
    records = schema["items"]
    items = [name for name, r in records.items()
             if r["class"] in ("GIVEN", "PREDICT")]

    options = {}
    for item in items:
        r = records[item]
        options[item] = list(r["values"]) + (
            [gated_value] if r.get("gate") else [])

    # Crowd tables from visible cells: full marginal for ungated items,
    # asked-only conditional for gated ones. Half a count per option so
    # nothing is impossible.
    marginal = {}
    conditional = {}
    for item in items:
        counts = frame[item].value_counts()
        full = np.array([counts.get(o, 0) + 0.5 for o in options[item]], float)
        marginal[item] = full / full.sum()
        if records[item].get("gate"):
            asked = np.array([counts.get(o, 0) + 0.5
                              for o in records[item]["values"]], float)
            conditional[item] = asked / asked.sum()

    out = []
    values = frame[items].to_numpy(dtype=object)
    for row in range(values.shape[0]):
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
                belief[item] = marginal[item]
            else:
                parent_belief = belief[gate["parent"]]
                asked_idx = [options[gate["parent"]].index(o)
                             for o in gate["observed_if"]]
                p_asked = float(parent_belief[asked_idx].sum())
                belief[item] = np.append(p_asked * conditional[item],
                                         1.0 - p_asked)
            out.append(belief[item])
    return out
