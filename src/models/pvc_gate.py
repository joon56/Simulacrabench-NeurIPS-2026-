"""E028 — parent-value-conditional gate decoding over E025.

For a gated child with parent p, every parent value v gets its own
table T_v = (1 - r_v) * A_v + r_v * sentinel, where
  r_v  = sentinel rate among visible rows with parent = v, shrunk
         (alpha) toward the hard-gate prior and optionally split by
         E010's selected conditioning column (shrunk toward r_v);
  A_v  = the answer distribution given parent = v: for asked values the
         GIVEN-conditioned cond blend (net cond head + cond ladder), for
         non-asked values the empirical answer table among the
         overlap rows (kappa-smoothed toward the asked-row marginal).
The child belief is sum_v b_parent[v] * T_v — the three E003/E010 pieces
(hard, soft, agreement) collapse into one data-estimated table per
parent value; exact gates reproduce the hard gate.
"""

import numpy as np
import pandas as pd

from src.models.hier_backoff import (
    _layout, _complete_rows, build_ladder, ladder_lookup, select_ladder,
    ALPHA,
)
from src.models.logit_blend import _given_matrix
from src.models.cond_agree import conditional_agreement
from src.models.shared_trunk import tune_and_train, _tensor, _proba_maps
from src.models.hh_sharp import hh_sharp_layer
from src.models.hh_cap import CONFIGS

PVC_KAPPA = 10.0


def build_pvc(frame, schema, complete, sel_cols):
    """{item: (parent, child values, {v: (r_v, {colval: r_vc}, A_v)},
    sel_col)}; A_v is None for asked values (blend at predict time)."""
    records, items, options = _layout(frame, schema)
    gated_value = schema["gated_value"]
    out = {}
    for item in items:
        gate = records[item].get("gate")
        if not gate or records[item]["class"] != "PREDICT":
            continue
        parent = gate["parent"]
        values = list(records[item]["values"])
        vidx = {o: i for i, o in enumerate(values)}
        child = complete[item].to_numpy(dtype=object)
        par = complete[parent].to_numpy(dtype=object)
        is_sent = child == gated_value
        asked_mask = np.isin(par, gate["observed_if"]) & ~is_sent
        marg = np.full(len(values), 0.5)
        for val in child[asked_mask]:
            j = vidx.get(val)
            if j is not None:
                marg[j] += 1
        marg /= marg.sum()
        sel_col = sel_cols.get(item)
        colvals = complete[sel_col].to_numpy(dtype=object) \
            if sel_col else None
        per_v = {}
        for v in options[parent]:
            m = par == v
            n = int(m.sum())
            k = int(is_sent[m].sum())
            # shrink toward the hard-gate prior (0 asked / 1 not asked):
            # exact gates leak nothing, overlap counts dominate quickly
            prior = 0.0 if v in gate["observed_if"] else 1.0
            r_v = (k + ALPHA * prior) / (n + ALPHA)
            r_vc = {}
            if colvals is not None and n:
                for c in pd.unique(colvals[m]):
                    mc = m & (colvals == c)
                    r_vc[c] = (is_sent[mc].sum() + ALPHA * r_v) / \
                        (mc.sum() + ALPHA)
            if v in gate["observed_if"]:
                A_v = None
            else:
                cnt = np.zeros(len(values))
                for val in child[m & ~is_sent]:
                    j = vidx.get(val)
                    if j is not None:
                        cnt[j] += 1
                A_v = (cnt + PVC_KAPPA * marg) / (cnt.sum() + PVC_KAPPA)
            per_v[v] = (r_v, r_vc, A_v)
        out[item] = (parent, values, per_v, sel_col)
    return out


def predict(frame, schema, cols=None, kappas=None, configs=CONFIGS,
            layer_fn=hh_sharp_layer):
    frame = frame.reset_index(drop=True)
    records, items, options = _layout(frame, schema)
    if cols is None:
        cols, kappas, _ = select_ladder(frame, schema)
    w, net, (predict_items, gated_items) = tune_and_train(
        frame, schema, cols, kappas, configs=configs)

    complete = _complete_rows(frame, items)
    if net is not None and w > 0:
        X_all = _tensor(_given_matrix(frame, records, items, options))
        full_proba, cond_proba = _proba_maps(net, X_all, predict_items,
                                             gated_items)
    else:
        w = 0.0
        full_proba = {n: np.zeros((len(frame), len(options[n])))
                      for n in predict_items}
        cond_proba = {n: np.zeros((len(frame),
                                   len(records[n]["values"])))
                      for n in gated_items}

    full_tables, cond_tables = {}, {}
    for item in predict_items:
        full_tables[item] = build_ladder(complete, item, options[item],
                                         cols, kappas)
        if records[item].get("gate"):
            cond_tables[item] = build_ladder(
                complete, item, list(records[item]["values"]),
                cols, kappas)

    agreement = conditional_agreement(frame, schema)
    sel_cols = {item: entry[1] for item, entry in agreement.items()}
    pvc = build_pvc(frame, schema, complete, sel_cols)
    item_index = {item: i for i, item in enumerate(items)}

    values = frame[items].to_numpy(dtype=object)
    col_idx = [items.index(c) for c in cols]
    keys_all = [tuple(values[r, i] for i in col_idx)
                for r in range(len(frame))]

    def blended(tables, probas, item, key, row):
        p0, levels = tables[item]
        ladder = ladder_lookup(p0, levels, key)
        logit = probas[item][row]
        if logit.sum() <= 0:
            return ladder
        return w * logit + (1.0 - w) * ladder

    def model_dist_matrix(item):
        p0, levels = full_tables[item]
        base = np.stack([ladder_lookup(p0, levels, k) for k in keys_all])
        logit = full_proba[item]
        if logit.sum() <= 0:
            return base
        return w * logit + (1.0 - w) * base

    model_dists = {item: model_dist_matrix(item)
                   for item in predict_items}
    ev_rows, lam = layer_fn(frame, schema, model_dists)

    out = []
    for row in range(values.shape[0]):
        key = keys_all[row]
        entry_row = ev_rows.get(row)
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
                base = blended(full_tables, full_proba, item, key, row)
            else:
                parent, cvals, per_v, sel_col = pvc[item]
                pb = belief[parent]
                cond = blended(cond_tables, cond_proba, item, key, row)
                colval = values[row, item_index[sel_col]] \
                    if sel_col else None
                base = np.zeros(len(cvals) + 1)
                for pv_i, pv in enumerate(options[parent]):
                    b = pb[pv_i]
                    if b <= 0:
                        continue
                    r_v, r_vc, A_v = per_v[pv]
                    r = r_vc.get(colval, r_v) if colval is not None \
                        else r_v
                    A = cond if A_v is None else A_v
                    base[:-1] += b * (1.0 - r) * A
                    base[-1] += b * r
            if entry_row is not None:
                ev, conc = entry_row
                pair = lam.get(item)
                e = ev.get(item)
                if pair is not None and e is not None and e.sum() > 0:
                    l = pair[1] if conc else pair[0]
                    if l > 0:
                        base = (1.0 - l) * base + l * e
            belief[item] = base
            out.append(belief[item])
    return out
