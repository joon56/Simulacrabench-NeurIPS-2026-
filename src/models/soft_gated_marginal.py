"""E003 — soft (agreement-weighted) gate coupling on top of E002.

Real unhcr gates are approximate (schema: agreement median 0.83, range
0.29-0.98). Hard coupling wins where the gate holds and pays log(1e-3)
where it does not. Per gated item, the agreement rate is estimated from
the visible rows and shrunk with a beta-binomial prior toward the
instrument median:

    n_i = visible rows where parent and child are both non-NaN
    k_i = rows where (child == NA_GATED) == (parent not in observed_if)
    a_i = (k_i + ALPHA * m) / (n_i + ALPHA),   m = median of k_i/n_i

Prediction mixes E002's hard-coupled vector with the observed full
marginal (sentinel included):  pred = a_i * hard + (1 - a_i) * soft.
On a sandbox with exact gates a_i ~= 1 and this reduces to E002; the gain
exists only on gate-violating data (measured by the violation simulation
in tests/test_soft_gating.py — the sandbox cannot show it).

ALPHA is fixed at 20 (cannot be tuned locally: the sandbox has no
violations to fit against; 20 keeps a_i near the raw rate once a few
dozen rows are visible while pulling tiny-n items to the median).
"""

import numpy as np
import pandas as pd

ALPHA = 20.0


def agreement_weights(frame, schema):
    """Per-gated-item shrunk agreement rate a_i, from visible rows."""
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
        return {}, 1.0
    m = float(np.median(list(raw.values())))
    weights = {item: (k + ALPHA * m) / (n + ALPHA)
               for item, (k, n) in counts.items()}
    return weights, m


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

    weights, _ = agreement_weights(frame, schema)

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
                hard = np.append(p_asked * conditional[item], 1.0 - p_asked)
                a = weights.get(item, 1.0)
                belief[item] = a * hard + (1.0 - a) * marginal[item]
            out.append(belief[item])
    return out
