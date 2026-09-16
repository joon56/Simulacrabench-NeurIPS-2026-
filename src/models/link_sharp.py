"""E019 — sharpened evidence layer over E018.

Two calibration refinements, both still chosen by the visible-row
replay (degenerate data tunes everything to zero):

  1. λ grid extended past 0.9 to {0.95, 0.98} — a near-exact twin puts
     ~1.0 on the truth and the old ceiling forced 10% model mass onto
     every matched cell.
  2. λ per (item × posterior-concentration bucket): rows whose top
     candidate holds max posterior weight >= CONC_SPLIT are the
     exact-twin regime (want λ near 1); diffuse rows are the k-NN
     regime (want λ low). One λ per item averaged the two; now each
     bucket calibrates its own. False matches are diffuse by
     construction, so they land in the low-λ bucket — the bucket IS
     the guard for the higher ceiling.

Pool, scoring, self-exclusion, runtime caps and the E012 stack are
E018's, unchanged.
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
from src.models.prob_link import EV_FLOOR, _evidence
from src.models.dup_link import (
    _sig_data_all, _topk_excl, CAL_QUERIES, CAL_SEED,
)

LAMBDA_GRID_X = tuple(round(0.1 * i, 1) for i in range(10)) + (0.95, 0.98)
CONC_SPLIT = 0.5   # max posterior weight >= this -> "concentrated" bucket


def _max_q(posteriors):
    return np.array([q.max() if len(q) else 0.0 for _, q in posteriors])


def _best_lambda(p_model, p_ev):
    best_l, best_s = 0.0, np.log(p_model).mean()
    for l in LAMBDA_GRID_X[1:]:
        s = np.log(np.maximum(
            (1 - l) * p_model + l * p_ev, EV_FLOOR)).mean()
        if s > best_s:
            best_l, best_s = l, s
    return best_l


def sharp_layer(frame, schema, model_dists):
    """(evidence for held-out rows incl. concentration flag,
    per-item (λ_diffuse, λ_concentrated))."""
    records, items, options = _layout(frame, schema)
    predict_cols = [n for n in items if records[n]["class"] == "PREDICT"]
    heldout = frame[predict_cols].isna().any(axis=1).to_numpy()
    codes, weights = _sig_data_all(frame, records, items)
    if codes is None:
        return {}, {}
    vis_pos = np.flatnonzero(~heldout)
    held_pos = np.flatnonzero(heldout)
    if len(vis_pos) < 2 or len(held_pos) == 0:
        return {}, {}

    cal_pos = vis_pos
    if len(cal_pos) > CAL_QUERIES:
        rng = np.random.default_rng(CAL_SEED)
        cal_pos = np.sort(rng.choice(cal_pos, CAL_QUERIES,
                                     replace=False))
    cal_post = _topk_excl(codes, weights, cal_pos, vis_pos)
    ev_cal = _evidence(frame, items, records, options, cal_post, cal_pos)
    conc_cal = _max_q(cal_post) >= CONC_SPLIT

    values = frame[items].to_numpy(dtype=object)
    col_of = {n: i for i, n in enumerate(items)}
    lam = {}
    for item in ev_cal:
        idx = {o: i for i, o in enumerate(options[item])}
        truth = np.array([idx.get(values[p, col_of[item]], -1)
                          for p in cal_pos])
        ok = truth >= 0
        if ok.sum() == 0:
            continue
        model = model_dists[item][cal_pos[ok]]
        ev = ev_cal[item][ok]
        t = truth[ok]
        rows = np.arange(len(t))
        p_model = np.maximum(model[rows, t], EV_FLOOR)
        p_ev = ev[rows, t]
        conc = conc_cal[ok]
        pair = [0.0, 0.0]
        for b, mask in enumerate((~conc, conc)):
            if mask.sum() >= 30:
                pair[b] = _best_lambda(p_model[mask], p_ev[mask])
        if pair[0] > 0 or pair[1] > 0:
            lam[item] = tuple(pair)
    if not lam:
        return {}, {}

    post = _topk_excl(codes, weights, held_pos, vis_pos)
    ev = _evidence(frame, items, records, options, post, held_pos)
    conc_held = _max_q(post) >= CONC_SPLIT
    ev_rows = {}
    for row_i, pos in enumerate(held_pos):
        ev_rows[pos] = ({item: ev[item][row_i] for item in ev},
                        bool(conc_held[row_i]))
    return ev_rows, lam


def predict(frame, schema, cols=None, kappas=None, layer_fn=None,
            extra_fn=None, configs=None, tune_fn=None):
    if layer_fn is None:
        layer_fn = sharp_layer
    if tune_fn is None:
        tune_fn = tune_and_train
    frame = frame.reset_index(drop=True)
    records, items, options = _layout(frame, schema)
    if cols is None:
        cols, kappas, _ = select_ladder(frame, schema)
    extra = extra_fn(frame, schema) if extra_fn is not None else None
    w, net, (predict_items, gated_items) = tune_fn(
        frame, schema, cols, kappas, configs=configs, extra=extra)

    complete = _complete_rows(frame, items)
    if net is not None and w > 0:
        X_all = _tensor(_given_matrix(frame, records, items, options))
        if extra is not None:
            X_all = torch.cat([X_all, torch.from_numpy(
                np.asarray(extra, dtype=np.float32))], dim=1)
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
                base = a * hard + (1.0 - a) * soft
            if entry_row is not None:
                ev, conc = entry_row
                pair = lam.get(item)
                e = ev.get(item)
                if pair is not None and e is not None and e.sum() > 0:
                    l = pair[int(conc)]   # bool -> 0/1; int buckets (E036)
                    if l > 0:
                        base = (1.0 - l) * base + l * e
            belief[item] = base
            out.append(belief[item])
    return out
