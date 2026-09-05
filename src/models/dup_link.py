"""E018 — full-pool visible-row evidence over E012.

Generalizes E014's cross-round evidence layer: the candidate pool for
every query row is ALL visible rows (self excluded), so within-round
near-duplicates — household co-respondents, re-dials, double entries —
are visible to the matcher, and the k-NN residual draws on the full
dataset. No round column is required; every instrument gets the layer.

Scoring, posterior, evidence and the per-item λ replay calibration are
E014's (rarity-weighted agreement = log-likelihood ratio; softmax over
the top-K candidates; λ per item from replaying the construction on
visible rows against realized answers; λ→0 ⇒ inert). The one new
correctness requirement is SELF-EXCLUSION in the calibration replay —
a visible query must never see itself among its candidates.
"""

import numpy as np
import pandas as pd

from src.models.hier_backoff import (
    _layout, _complete_rows, build_ladder, ladder_lookup, select_ladder,
)
from src.models.logit_blend import _given_matrix
from src.models.cond_agree import conditional_agreement
from src.models.shared_trunk import tune_and_train, _tensor, _proba_maps
from src.models.prob_link import (
    TOP_K, LAMBDA_GRID, EV_FLOOR, _evidence,
)

CAL_QUERIES = 6000   # cap on calibration replay queries (runtime guard;
CAL_SEED = 0         # lambda on 6k rows/item is plenty)


def _sig_data_all(frame, records, items):
    """Codes + rarity weights over the FULL GIVEN block (no exclusion)."""
    given = [n for n in items if records[n]["class"] == "GIVEN"]
    if not given:
        return None, None
    codes = np.empty((len(frame), len(given)), dtype=np.int32)
    weights = np.empty(len(given))
    for j, col in enumerate(given):
        vals = frame[col].astype(object).where(frame[col].notna(),
                                               "__NA__")
        codes[:, j] = pd.factorize(vals)[0]
        _, counts = np.unique(codes[:, j], return_counts=True)
        f = counts / counts.sum()
        weights[j] = -np.log(np.clip((f ** 2).sum(), 1e-6, 1.0))
    return codes, weights


def _topk_excl(codes, weights, query_pos, cand_pos, k=TOP_K, chunk=256):
    """Top-k posteriors with self-exclusion: a query row present in the
    candidate pool never matches itself."""
    cand = codes[cand_pos]
    cand_index = {pos: i for i, pos in enumerate(cand_pos)}
    w = weights[None, None, :]
    out = []
    for start in range(0, len(query_pos), chunk):
        block_pos = query_pos[start:start + chunk]
        block = codes[block_pos]
        score = ((block[:, None, :] == cand[None, :, :]) * w).sum(axis=2)
        for i, qpos in enumerate(block_pos):
            self_i = cand_index.get(qpos)
            if self_i is not None:
                score[i, self_i] = -np.inf
        top = np.argsort(score, axis=1)[:, -k:]
        for i in range(len(block)):
            s = score[i, top[i]]
            ok = np.isfinite(s)
            s, t = s[ok], top[i][ok]
            q = np.exp(s - s.max())
            q /= q.sum()
            out.append((cand_pos[t], q))
    return out


def full_pool_layer(frame, schema, model_dists):
    """(evidence dists for held-out rows, per-item λ) over the full
    visible pool. ({}, {}) when nothing calibrates above zero."""
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

    # ---- calibration replay: visible queries vs the pool, self excluded
    cal_pos = vis_pos
    if len(cal_pos) > CAL_QUERIES:
        rng = np.random.default_rng(CAL_SEED)
        cal_pos = np.sort(rng.choice(cal_pos, CAL_QUERIES,
                                     replace=False))
    cal_post = _topk_excl(codes, weights, cal_pos, vis_pos)
    ev_cal = _evidence(frame, items, records, options, cal_post, cal_pos)

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
        best_l, best_s = 0.0, np.log(p_model).mean()
        for l in LAMBDA_GRID[1:]:
            s = np.log(np.maximum(
                (1 - l) * p_model + l * p_ev, EV_FLOOR)).mean()
            if s > best_s:
                best_l, best_s = l, s
        if best_l > 0:
            lam[item] = best_l
    if not lam:
        return {}, {}

    # ---- evidence for held-out rows (self can't be in the pool)
    post = _topk_excl(codes, weights, held_pos, vis_pos)
    ev = _evidence(frame, items, records, options, post, held_pos)
    ev_rows = {}
    for row_i, pos in enumerate(held_pos):
        ev_rows[pos] = {item: ev[item][row_i] for item in ev}
    return ev_rows, lam


def predict(frame, schema, cols=None, kappas=None):
    records, items, options = _layout(frame, schema)
    if cols is None:
        cols, kappas, _ = select_ladder(frame, schema)
    w, net, (predict_items, gated_items) = tune_and_train(
        frame, schema, cols, kappas)

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
    ev_rows, lam = full_pool_layer(frame, schema, model_dists)

    out = []
    for row in range(values.shape[0]):
        key = keys_all[row]
        ev = ev_rows.get(row)
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
            if ev is not None:
                l = lam.get(item, 0.0)
                e = ev.get(item)
                if l > 0 and e is not None and e.sum() > 0:
                    base = (1.0 - l) * base + l * e
            belief[item] = base
            out.append(belief[item])
    return out
