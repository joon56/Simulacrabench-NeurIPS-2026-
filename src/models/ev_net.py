"""E020 — twin evidence as network INPUT over the E012 stack.

E018 mixes posterior-weighted twin answers into the belief with a
per-item scalar λ (a copy model). Real twins are noisy, so instead the
evidence vectors of ALL PREDICT items become extra inputs to the
shared-trunk net, alongside the GIVEN one-hots: the network learns,
per item and across items, how much and in what shape to trust a
twin's answers. Replay-consistent by construction — visible rows train
on evidence built with self excluded from the pool, exactly as held-out
rows are scored. No λ layer. Ladder blend, gate recursion, conditional
agreement: E012/E010 unchanged.
"""

import numpy as np
import pandas as pd
import torch

from src.models.hier_backoff import (
    _layout, _complete_rows, build_ladder, ladder_lookup, select_ladder,
)
from src.models.logit_blend import _given_matrix
from src.models.cond_agree import conditional_agreement
from src.models.shared_trunk import tune_and_train, _tensor, _proba_maps
from src.models.prob_link import _evidence
from src.models.dup_link import _sig_data_all, _topk_excl


def evidence_block(frame, schema):
    """[len(frame), sum K_i] evidence matrix: every row's posterior-
    weighted candidate answers over the visible pool (self excluded);
    zeros when no pool exists."""
    records, items, options = _layout(frame, schema)
    predict_items = [n for n in items if records[n]["class"] == "PREDICT"]
    width = sum(len(options[n]) for n in predict_items)
    block = np.zeros((len(frame), width), dtype=np.float32)
    codes, weights = _sig_data_all(frame, records, items)
    if codes is None:
        return block, predict_items
    predict_cols = predict_items
    heldout = frame[predict_cols].isna().any(axis=1).to_numpy()
    vis_pos = np.flatnonzero(~heldout)
    if len(vis_pos) < 2:
        return block, predict_items
    all_pos = np.arange(len(frame))
    post = _topk_excl(codes, weights, all_pos, vis_pos)
    ev = _evidence(frame, items, records, options, post, all_pos)
    off = 0
    for item in predict_items:
        k = len(options[item])
        block[:, off:off + k] = ev[item]
        off += k
    return block, predict_items


def predict(frame, schema, cols=None, kappas=None):
    frame = frame.reset_index(drop=True)
    records, items, options = _layout(frame, schema)
    if cols is None:
        cols, kappas, _ = select_ladder(frame, schema)
    extra, _ = evidence_block(frame, schema)
    w, net, (predict_items, gated_items) = tune_and_train(
        frame, schema, cols, kappas, extra=extra)

    complete = _complete_rows(frame, items)
    if net is not None and w > 0:
        X_all = torch.cat([
            _tensor(_given_matrix(frame, records, items, options)),
            torch.from_numpy(extra)], dim=1)
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
