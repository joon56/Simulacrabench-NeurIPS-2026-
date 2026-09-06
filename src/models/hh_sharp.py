"""E022 — composition: household-aware weights (E021) feeding the
sharpened λ layer (E019). Learned column weights concentrate the
posterior on true co-respondents; the concentration bucket then
calibrates its own λ (up to 0.98) for exactly those rows. Both parts
stay replay-calibrated; inertness on duplicate-free data inherited.
"""

import numpy as np

from src.models.hier_backoff import _layout
from src.models.prob_link import EV_FLOOR, _evidence
from src.models import link_sharp
from src.models.link_sharp import (
    _max_q, _best_lambda, CONC_SPLIT,
)
from src.models.dup_link import (
    _sig_data_all, _topk_excl, CAL_QUERIES, CAL_SEED,
)
from src.models.hh_link import estimate_weights


def hh_sharp_layer(frame, schema, model_dists):
    records, items, options = _layout(frame, schema)
    predict_cols = [n for n in items if records[n]["class"] == "PREDICT"]
    heldout = frame[predict_cols].isna().any(axis=1).to_numpy()
    codes, rarity_w = _sig_data_all(frame, records, items)
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
    # E021: rarity pass -> learned household weights
    post0 = _topk_excl(codes, rarity_w, cal_pos, vis_pos)
    weights, _ = estimate_weights(codes, rarity_w, cal_pos, post0)
    # E019: replay with concentration buckets under the learned weights
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


def predict(frame, schema, cols=None, kappas=None):
    return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                              layer_fn=hh_sharp_layer)
