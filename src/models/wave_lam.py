"""E036 — evidence weight per twin RELATION: λ per (item, concentration
bucket, same-round vs cross-round top candidate), over E025.

E022 calibrates λ per (item, concentration bucket). On unhcr the best
candidate for a held-out row is either the same household in the OTHER
CATI round (the panel recurrence: same person a year later, or another
member) or a co-respondent in the SAME round. The two relations
disagree for different reasons — panel drift on volatile items
(intentions, needs, coping) vs person-level differences between
co-respondents on personal items — so one λ per item pools two
different agreement rates. Here the replay calibrates λ separately for
the two relations (bucket = conc + 2·cross, four per item) and falls
back to the E022 pooled bucket wherever a refined bucket has fewer than
MIN_BUCKET calibration rows. No round column (unicef, wb) ⇒ bit-identical
to E022/E025; twins only in one round (the household sim) ⇒ the
cross-round buckets are empty and fall back ⇒ identical as well.
"""

import numpy as np

from src.models.hier_backoff import _layout
from src.models.prob_link import EV_FLOOR, _evidence
from src.models import link_sharp
from src.models.link_sharp import _max_q, _best_lambda, CONC_SPLIT
from src.models.dup_link import (
    _sig_data_all, _topk_excl, CAL_QUERIES, CAL_SEED,
)
from src.models.hh_link import estimate_weights
from src.models.hh_cap import CONFIGS
from src.models.cross_link import find_round_col

MIN_BUCKET = 30


def _top_cross(posteriors, query_pos, rounds):
    """True where the top candidate sits in a different round than the
    query (False when no candidates or no round column)."""
    out = np.zeros(len(query_pos), dtype=bool)
    if rounds is None:
        return out
    for i, (q, (cands, w)) in enumerate(zip(query_pos, posteriors)):
        if len(w):
            out[i] = rounds[cands[np.argmax(w)]] != rounds[q]
    return out


def wave_lam_layer(frame, schema, model_dists):
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
    round_col = find_round_col(records, items)
    rounds = (frame[round_col].to_numpy(dtype=object)
              if round_col is not None else None)

    cal_pos = vis_pos
    if len(cal_pos) > CAL_QUERIES:
        rng = np.random.default_rng(CAL_SEED)
        cal_pos = np.sort(rng.choice(cal_pos, CAL_QUERIES,
                                     replace=False))
    post0 = _topk_excl(codes, rarity_w, cal_pos, vis_pos)
    weights, _ = estimate_weights(codes, rarity_w, cal_pos, post0)
    cal_post = _topk_excl(codes, weights, cal_pos, vis_pos)
    ev_cal = _evidence(frame, items, records, options, cal_post, cal_pos)
    conc_cal = _max_q(cal_post) >= CONC_SPLIT
    cross_cal = _top_cross(cal_post, cal_pos, rounds)
    bucket_cal = conc_cal.astype(int) + 2 * cross_cal.astype(int)

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
        bucket = bucket_cal[ok]
        # E022 pooled buckets first (the fallback)
        pooled = [0.0, 0.0]
        for b, mask in enumerate((~conc, conc)):
            if mask.sum() >= MIN_BUCKET:
                pooled[b] = _best_lambda(p_model[mask], p_ev[mask])
        four = [pooled[0], pooled[1], pooled[0], pooled[1]]
        if rounds is not None:
            for b in range(4):
                mask = bucket == b
                if mask.sum() >= MIN_BUCKET:
                    four[b] = _best_lambda(p_model[mask], p_ev[mask])
        if any(l > 0 for l in four):
            lam[item] = tuple(four)
    if not lam:
        return {}, {}

    post = _topk_excl(codes, weights, held_pos, vis_pos)
    ev = _evidence(frame, items, records, options, post, held_pos)
    conc_held = _max_q(post) >= CONC_SPLIT
    cross_held = _top_cross(post, held_pos, rounds)
    bucket_held = conc_held.astype(int) + 2 * cross_held.astype(int)
    ev_rows = {}
    for row_i, pos in enumerate(held_pos):
        ev_rows[pos] = ({item: ev[item][row_i] for item in ev},
                        int(bucket_held[row_i]))
    return ev_rows, lam


def predict(frame, schema, cols=None, kappas=None):
    return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                              layer_fn=wave_lam_layer, configs=CONFIGS)
