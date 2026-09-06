"""E021 — household-aware signature weights over E018.

E018 weights every GIVEN column by rarity (-log u_j). If the real
near-duplicates are household co-respondents, the person-level columns
(age, education, marital status, relationship) legitimately differ
between a row and its best match, and rarity weighting punishes exactly
those disagreements. One Fellegi-Sunter iteration fixes that from the
data: rarity match -> provisional top-1 pairs with concentrated
posterior -> per-column agreement m_j among them -> weights
log(m_j/u_j) - log((1-m_j)/(1-u_j)) clipped at 0 -> re-match. Columns
that define a household keep their weight; columns that vary within it
lose it. No duplicate structure -> m_j ~ u_j -> weights ~ 0 -> flat
posteriors -> lambda calibrates to 0 (E018's inertness kept).
"""

import numpy as np

from src.models.hier_backoff import _layout
from src.models.prob_link import EV_FLOOR, LAMBDA_GRID, _evidence
from src.models import dup_link
from src.models.dup_link import (
    _sig_data_all, _topk_excl, CAL_QUERIES, CAL_SEED,
)

PAIR_MASS = 0.5     # top-1 posterior mass needed for a provisional pair
MIN_PAIRS = 30


def estimate_weights(codes, rarity_w, vis_pos, posteriors):
    """Household-aware column weights from provisional pairs.
    Returns (weights, n_pairs); falls back to rarity when too few
    concentrated pairs exist."""
    pairs = []
    for q, (cands, q_w) in zip(vis_pos, posteriors):
        if len(q_w) and q_w.max() >= PAIR_MASS:
            pairs.append((q, cands[np.argmax(q_w)]))
    if len(pairs) < MIN_PAIRS:
        return rarity_w, len(pairs)
    a = codes[[p for p, _ in pairs]]
    b = codes[[c for _, c in pairs]]
    agree = (a == b).mean(axis=0)
    m = (agree * len(pairs) + 1.0) / (len(pairs) + 2.0)
    u = np.exp(-rarity_w)                     # rarity_w = -log u_j
    m = np.clip(m, 1e-4, 1.0 - 1e-4)
    u = np.clip(u, 1e-4, 1.0 - 1e-4)
    w = np.log(m / u) - np.log((1.0 - m) / (1.0 - u))
    return np.maximum(w, 0.0), len(pairs)


def household_layer(frame, schema, model_dists, return_weights=False):
    records, items, options = _layout(frame, schema)
    predict_cols = [n for n in items if records[n]["class"] == "PREDICT"]
    heldout = frame[predict_cols].isna().any(axis=1).to_numpy()
    codes, rarity_w = _sig_data_all(frame, records, items)
    if codes is None:
        return ({}, {}, None) if return_weights else ({}, {})
    vis_pos = np.flatnonzero(~heldout)
    held_pos = np.flatnonzero(heldout)
    if len(vis_pos) < 2 or len(held_pos) == 0:
        return ({}, {}, None) if return_weights else ({}, {})

    cal_pos = vis_pos
    if len(cal_pos) > CAL_QUERIES:
        rng = np.random.default_rng(CAL_SEED)
        cal_pos = np.sort(rng.choice(cal_pos, CAL_QUERIES,
                                     replace=False))
    # pass 1: rarity weights -> provisional pairs -> learned weights
    post0 = _topk_excl(codes, rarity_w, cal_pos, vis_pos)
    weights, _ = estimate_weights(codes, rarity_w, cal_pos, post0)
    # pass 2: calibration replay with the learned weights
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
        return ({}, {}, weights) if return_weights else ({}, {})

    post = _topk_excl(codes, weights, held_pos, vis_pos)
    ev = _evidence(frame, items, records, options, post, held_pos)
    ev_rows = {pos: {item: ev[item][i] for item in ev}
               for i, pos in enumerate(held_pos)}
    return (ev_rows, lam, weights) if return_weights else (ev_rows, lam)


def predict(frame, schema, cols=None, kappas=None):
    return dup_link.predict(frame, schema, cols=cols, kappas=kappas,
                            layer_fn=household_layer)
