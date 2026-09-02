"""E014 v2 — soft posterior cross-round evidence mixing.

E013 (hard 1:1 fuzzy matching) armed nothing on real unhcr data, and
A005-level diagnosis showed why hard matching is fragile there: the
signature is only ~16 GIVEN columns (the "72" in earlier notes counted
EXCLUDE), so concentrated real populations collide — the uniqueness
margin then rejects everything — while drifted twins sink into the
random-score zone. This layer needs neither uniqueness nor certainty:

  score    W(q, c) = sum over agreeing signature columns of
           c_j = -log u_j  (u_j = random-agreement probability from
           value frequencies): rare coincidences weigh heavily. W is a
           log-likelihood ratio, so
  posterior q(c) = softmax over the top-K other-round visible
           candidates — collisions just share the mass.
  evidence ev_i(row) = sum_c q(c) * onehot(candidate c's answer to i).
  mixing   belief_i = (1 - lambda_i) * model_i + lambda_i * ev_i, with
           lambda_i CALIBRATED per item by replaying the identical
           construction on visible rows against their realized answers
           (grid argmax of held-in log score). No cross-round signal ->
           every lambda_i tunes to 0 -> bit-inert. Applied at the
           belief level, before gated children consume parent beliefs.

Everything else (net, ladder, conditional agreement, gate math) is
E012/E010 unchanged.
"""

import numpy as np
import pandas as pd

from src.models.hier_backoff import (
    _layout, _complete_rows, build_ladder, ladder_lookup, select_ladder,
)
from src.models.logit_blend import _given_matrix
from src.models.cond_agree import conditional_agreement
from src.models.cross_link import find_round_col
from src.models.shared_trunk import tune_and_train, _tensor, _proba_maps

TOP_K = 10
LAMBDA_GRID = tuple(round(0.1 * i, 1) for i in range(10))  # 0 .. 0.9
EV_FLOOR = 1e-3


def _sig_data(frame, records, items, round_col):
    given = [n for n in items
             if records[n]["class"] == "GIVEN" and n != round_col]
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


def _topk_posteriors(codes, weights, query_pos, cand_pos, k=TOP_K,
                     chunk=256):
    """Per query row: (top-k candidate positions, posterior weights)."""
    cand = codes[cand_pos]
    w = weights[None, None, :]
    out = []
    for start in range(0, len(query_pos), chunk):
        block = codes[query_pos[start:start + chunk]]
        score = ((block[:, None, :] == cand[None, :, :]) * w).sum(axis=2)
        top = np.argsort(score, axis=1)[:, -k:]
        for i in range(len(block)):
            s = score[i, top[i]]
            q = np.exp(s - s.max())
            q /= q.sum()
            out.append((cand_pos[top[i]], q))
    return out


def _evidence(frame, items, records, options, posteriors, query_pos):
    """{item: dist matrix aligned to query_pos} from candidate answers."""
    predict_items = [n for n in items if records[n]["class"] == "PREDICT"]
    values = frame[items].to_numpy(dtype=object)
    col_of = {n: i for i, n in enumerate(items)}
    ev = {item: np.zeros((len(query_pos), len(options[item])))
          for item in predict_items}
    opt_index = {item: {o: i for i, o in enumerate(options[item])}
                 for item in predict_items}
    for row_i, (cands, q) in enumerate(posteriors):
        for item in predict_items:
            col = col_of[item]
            idx = opt_index[item]
            vec = ev[item][row_i]
            for c, qc in zip(cands, q):
                code = idx.get(values[c, col])
                if code is not None:
                    vec[code] += qc
    return ev


def cross_round_layer(frame, schema, model_dists):
    """Build (evidence dists for held-out rows, per-item lambda).

    model_dists: {item: [n_rows, K] model distributions} used for the
    calibration replay. Returns ({}, {}) when no round column exists or
    nothing calibrates above zero."""
    records, items, options = _layout(frame, schema)
    round_col = find_round_col(records, items)
    if round_col is None:
        return {}, {}
    predict_cols = [n for n in items if records[n]["class"] == "PREDICT"]
    heldout = frame[predict_cols].isna().any(axis=1).to_numpy()
    rounds = frame[round_col].to_numpy(dtype=object)
    round_vals = pd.unique(rounds)
    if len(round_vals) != 2:
        return {}, {}
    r_a = rounds == round_vals[0]

    codes, weights = _sig_data(frame, records, items, round_col)

    # ---- calibration replay on visible rows
    lam = {}
    cal_pos, cal_post = [], []
    for q_mask, c_mask in ((r_a, ~r_a), (~r_a, r_a)):
        qq = np.flatnonzero(q_mask & ~heldout)
        cc = np.flatnonzero(c_mask & ~heldout)
        if len(qq) == 0 or len(cc) == 0:
            continue
        cal_pos.append(qq)
        cal_post += _topk_posteriors(codes, weights, qq, cc)
    if not cal_pos:
        return {}, {}
    cal_pos = np.concatenate(cal_pos)
    ev_cal = _evidence(frame, items, records, options, cal_post, cal_pos)

    values = frame[items].to_numpy(dtype=object)
    col_of = {n: i for i, n in enumerate(items)}
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

    # ---- evidence for held-out rows
    ev_rows = {}
    for q_mask, c_mask in ((r_a, ~r_a), (~r_a, r_a)):
        qq = np.flatnonzero(q_mask & heldout)
        cc = np.flatnonzero(c_mask & ~heldout)
        if len(qq) == 0 or len(cc) == 0:
            continue
        post = _topk_posteriors(codes, weights, qq, cc)
        ev = _evidence(frame, items, records, options, post, qq)
        for row_i, pos in enumerate(qq):
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

    def blended(tables, probas, item, key, row):
        p0, levels = tables[item]
        ladder = ladder_lookup(p0, levels, key)
        logit = probas[item][row]
        if logit.sum() <= 0:
            return ladder
        return w * logit + (1.0 - w) * ladder

    # model dists for the calibration replay: the blended full-table
    # distribution per row (soft path — same family the E008 w-tuning
    # used), computed lazily per item over all rows
    keys_all = [tuple(values[r, i] for i in col_idx)
                for r in range(len(frame))]

    def model_dist_matrix(item):
        p0, levels = full_tables[item]
        base = np.stack([ladder_lookup(p0, levels, k) for k in keys_all])
        logit = full_proba[item]
        if logit.sum() <= 0:
            return base
        return w * logit + (1.0 - w) * base

    model_dists = {item: model_dist_matrix(item)
                   for item in predict_items}
    ev_rows, lam = cross_round_layer(frame, schema, model_dists)

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
