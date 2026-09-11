"""E030 — ordinal near-agreement in the matching signature, over E025.

E021/E022 score a candidate by Σ_j w_j · [value_j agrees exactly]. For
ordinal signature columns — roster counts (0, 1, 2, …, 6-10, 11+), age
bands, pay bands — a near-duplicate that moved ONE level (a child born
between CATI rounds, a birthday crossing a band boundary, a member who
left) loses that column's whole weight, which on the household-defining
roster columns is several nats: the true match sinks in the ranking or
lands in the diffuse bucket. Here each ordinal column also gets an
ADJACENCY weight v_j for |rank difference| = 1, estimated from the same
provisional pairs as the exact weights (Fellegi–Sunter form, clipped at
0):

    v_j = clip( log(m_adj / u_adj) − log(m_oth / u_oth),  0,  w_j )

with m_o / u_o the pair / random probabilities of the three outcomes
exact / adjacent / other (Dirichlet-1 smoothed; ≥ 5 adjacent pairs
required). The exact weight keeps E021's binary form.

Ordinality is read from the schema: a column is ordinal when ≥ 3 of its
values parse to a leading number and those numbers increase in schema
order ('0', '1', '6-10', '11+', '18-24', '45 and above'). Non-parsing
levels ('Not answered', '[generalised:s2]', NA) never count as adjacent.
Data whose near-duplicates agree exactly (or that has none) gives
m_adj ≤ u_adj ⇒ v_j = 0 ⇒ bit-identical to E025. The rarity pass, the
concentration-bucket λ replay, and the whole E025 stack are unchanged.
"""

import re

import numpy as np

from src.models.hier_backoff import _layout
from src.models.prob_link import EV_FLOOR, _evidence
from src.models import link_sharp
from src.models.link_sharp import _max_q, _best_lambda, CONC_SPLIT
from src.models.dup_link import (
    _sig_data_all, _topk_excl, CAL_QUERIES, CAL_SEED,
)
from src.models.hh_link import PAIR_MASS, MIN_PAIRS
from src.models.hh_cap import CONFIGS
from src.models.prob_link import TOP_K

_LEAD_NUM = re.compile(r"^\s*(\d+(?:\.\d+)?)")
_LABEL_PREFIX = re.compile(r"^\s*\d+\.\s")     # '1. Head of household'


def _leading_number(value):
    s = str(value)
    if _LABEL_PREFIX.match(s):
        return None
    m = _LEAD_NUM.match(s)
    return float(m.group(1)) if m else None


def ordinal_ranks(values):
    """{value: rank} for a schema value list if it is ordinal, else None."""
    parsed = [(v, _leading_number(v)) for v in values]
    nums = [n for _, n in parsed if n is not None]
    if len(nums) < 3 or any(b <= a for a, b in zip(nums, nums[1:])):
        return None
    rank, out = 0, {}
    for v, n in parsed:
        if n is not None:
            out[v] = rank
            rank += 1
    return out


def _rank_data(frame, records, items):
    """ranks [n, G] aligned to _sig_data_all's columns; -1 = no rank."""
    given = [n for n in items if records[n]["class"] == "GIVEN"]
    ranks = np.full((len(frame), len(given)), -1, dtype=np.int32)
    for j, col in enumerate(given):
        table = ordinal_ranks(list(records[col]["values"]))
        if table is None:
            continue
        ranks[:, j] = frame[col].map(table).fillna(-1).to_numpy(
            dtype=np.int32)
    return ranks


def _adjacent(a, b):
    """Broadcastable |rank diff| == 1 with both ranks defined."""
    return (np.abs(a - b) == 1) & (a >= 0) & (b >= 0)


def estimate_weights_ord(codes, ranks, rarity_w, vis_pos, posteriors):
    """(exact weights, adjacency weights, n_pairs) from provisional
    pairs — E021's estimator plus the adjacency channel."""
    pairs = []
    for q, (cands, q_w) in zip(vis_pos, posteriors):
        if len(q_w) and q_w.max() >= PAIR_MASS:
            pairs.append((q, cands[np.argmax(q_w)]))
    n_cols = codes.shape[1]
    if len(pairs) < MIN_PAIRS:
        return rarity_w, np.zeros(n_cols), len(pairs)
    a_idx = [p for p, _ in pairs]
    b_idx = [c for _, c in pairs]
    a, b = codes[a_idx], codes[b_idx]
    agree = (a == b).mean(axis=0)
    m = (agree * len(pairs) + 1.0) / (len(pairs) + 2.0)
    u = np.exp(-rarity_w)
    m = np.clip(m, 1e-4, 1.0 - 1e-4)
    u = np.clip(u, 1e-4, 1.0 - 1e-4)
    w = np.maximum(np.log(m / u) - np.log((1.0 - m) / (1.0 - u)), 0.0)

    # adjacency as the third Fellegi-Sunter outcome (exact / adjacent /
    # other), weighted RELATIVE to "other": a one-level difference is
    # evidence for a pair exactly insofar as true pairs, when they
    # differ, differ by one level more often than random pairs do.
    # Capped at the exact weight so adjacency never outranks agreement.
    ra, rb = ranks[a_idx], ranks[b_idx]
    nonexact = a != b
    adj = _adjacent(ra, rb) & nonexact
    oth = nonexact & ~adj
    n_p = len(pairs)
    m_adj = (adj.sum(axis=0) + 1.0) / (n_p + 3.0)
    m_oth = (oth.sum(axis=0) + 1.0) / (n_p + 3.0)
    u_adj = np.zeros(n_cols)
    u_oth = np.ones(n_cols)
    for j in range(n_cols):
        r = ranks[vis_pos, j]
        r = r[r >= 0]
        if len(r) == 0:
            continue
        f = np.bincount(r) / len(ranks[vis_pos, j])
        u_adj[j] = float((f[:-1] * f[1:]).sum() * 2.0)
        u_oth[j] = max(1.0 - float((f ** 2).sum()) - u_adj[j], 1e-6)
    u_adj = np.clip(u_adj, 1e-6, 1.0)
    v = np.log(m_adj / u_adj) - np.log(m_oth / u_oth)
    v = np.minimum(np.maximum(v, 0.0), w)
    v[(ranks[vis_pos] >= 0).sum(axis=0) == 0] = 0.0
    v[adj.sum(axis=0) < 5] = 0.0
    return w, v, len(pairs)


def _topk_excl_ord(codes, ranks, weights, adj_w, query_pos, cand_pos,
                   k=TOP_K, chunk=256):
    """dup_link._topk_excl with the adjacency term; falls back to the
    exact-only kernel when every adjacency weight is zero."""
    if not np.any(adj_w > 0):
        return _topk_excl(codes, weights, query_pos, cand_pos, k=k,
                          chunk=chunk)
    cand = codes[cand_pos]
    cand_r = ranks[cand_pos]
    cand_index = {pos: i for i, pos in enumerate(cand_pos)}
    w = weights[None, None, :]
    v = adj_w[None, None, :]
    out = []
    for start in range(0, len(query_pos), chunk):
        block_pos = query_pos[start:start + chunk]
        block = codes[block_pos]
        block_r = ranks[block_pos]
        score = ((block[:, None, :] == cand[None, :, :]) * w).sum(axis=2)
        score += (_adjacent(block_r[:, None, :], cand_r[None, :, :])
                  * v).sum(axis=2)
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


def ord_sharp_layer(frame, schema, model_dists, return_weights=False):
    records, items, options = _layout(frame, schema)
    predict_cols = [n for n in items if records[n]["class"] == "PREDICT"]
    heldout = frame[predict_cols].isna().any(axis=1).to_numpy()
    codes, rarity_w = _sig_data_all(frame, records, items)
    empty = ({}, {}, None) if return_weights else ({}, {})
    if codes is None:
        return empty
    vis_pos = np.flatnonzero(~heldout)
    held_pos = np.flatnonzero(heldout)
    if len(vis_pos) < 2 or len(held_pos) == 0:
        return empty
    ranks = _rank_data(frame, records, items)

    cal_pos = vis_pos
    if len(cal_pos) > CAL_QUERIES:
        rng = np.random.default_rng(CAL_SEED)
        cal_pos = np.sort(rng.choice(cal_pos, CAL_QUERIES,
                                     replace=False))
    # E021 rarity pass -> provisional pairs -> exact + adjacency weights
    post0 = _topk_excl(codes, rarity_w, cal_pos, vis_pos)
    weights, adj_w, _ = estimate_weights_ord(codes, ranks, rarity_w,
                                             cal_pos, post0)
    # E019 replay with concentration buckets under the learned weights
    cal_post = _topk_excl_ord(codes, ranks, weights, adj_w, cal_pos,
                              vis_pos)
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
        return empty

    post = _topk_excl_ord(codes, ranks, weights, adj_w, held_pos, vis_pos)
    ev = _evidence(frame, items, records, options, post, held_pos)
    conc_held = _max_q(post) >= CONC_SPLIT
    ev_rows = {}
    for row_i, pos in enumerate(held_pos):
        ev_rows[pos] = ({item: ev[item][row_i] for item in ev},
                        bool(conc_held[row_i]))
    if return_weights:
        return ev_rows, lam, (weights, adj_w)
    return ev_rows, lam


def predict(frame, schema, cols=None, kappas=None):
    return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                              layer_fn=ord_sharp_layer, configs=CONFIGS)
