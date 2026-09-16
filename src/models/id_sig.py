"""E038 — respondent-id structure as matching signature, over E025.

The evidence layer matches held-out rows to visible rows on the GIVEN
block only. The frame also carries `respondent_id`, which the sandbox
generates as a plain sequence (R000001, …) but which a real survey
file may not: identifiers commonly embed a household key, a round tag
or a member suffix, and files are often ordered household by household.
This module derives candidate signature columns from the identifier —

  * string tokens (letter / digit / other runs, by position),
  * truncated digit runs (a fixed-width household key + member index
    shows up as a shared prefix),
  * block ids of the numeric rank at several granularities (rank // 2,
    // 3, // 5, // 10: contiguous household blocks agree within a block)

— and lets the E021 Fellegi–Sunter step decide their weight from the
data: provisional pairs come from the GIVEN-only rarity pass exactly as
in E025, the agreement rate m_j of every derived column is measured on
those pairs, and a column whose agreement among pairs is no higher than
chance (m_j ≈ u_j) gets weight 0. Sequential identifiers and random row
order therefore leave E025 bit-for-bit unchanged (the sandbox), while
a real household key or block structure arms with a large weight and
concentrates the posterior on true co-respondents. No identifier is
interpreted; nothing is hard-coded to any data set.
"""

import re

import numpy as np
import pandas as pd

from src.models.hier_backoff import _layout
from src.models.prob_link import EV_FLOOR, _evidence
from src.models import link_sharp
from src.models.link_sharp import _max_q, _best_lambda, CONC_SPLIT
from src.models.dup_link import (
    _sig_data_all, _topk_excl, CAL_QUERIES, CAL_SEED,
)
from src.models.hh_link import estimate_weights, PAIR_MASS
from src.models.hh_cap import CONFIGS

ID_COLUMN = "respondent_id"
MAX_TOKENS = 6
BLOCKS = (2, 3, 5, 10)
MIN_AGREE = 5      # observed agreements among provisional pairs
_RUN = re.compile(r"[A-Za-z]+|\d+|[^A-Za-z\d]+")


def id_columns(frame):
    """Derived identifier columns as an object DataFrame (may be empty)."""
    if ID_COLUMN not in frame.columns:
        return pd.DataFrame(index=frame.index)
    ids = frame[ID_COLUMN].astype(str).to_numpy()
    cols = {}
    tokens = [_RUN.findall(s) for s in ids]
    for j in range(MAX_TOKENS):
        col = [t[j] if j < len(t) else "__none__" for t in tokens]
        if len(set(col)) > 1:
            cols["id_tok_%d" % j] = col
    # truncated digit runs: prefixes of the first two digit runs
    for r in range(2):
        runs = [[t for t in ts if t.isdigit()] for ts in tokens]
        vals = [rs[r] if r < len(rs) else "" for rs in runs]
        if all(v == "" for v in vals):
            continue
        for cut in (1, 2):
            col = [v[:-cut] if len(v) > cut else "__none__" for v in vals]
            if len(set(col)) > 1:
                cols["id_num%d_cut%d" % (r, cut)] = col
    # numeric rank blocks (order by first digit run, then the string)
    first = []
    for ts in tokens:
        digs = [t for t in ts if t.isdigit()]
        first.append(int(digs[0]) if digs else -1)
    order = np.lexsort((ids, np.asarray(first)))
    rank = np.empty(len(ids), dtype=np.int64)
    rank[order] = np.arange(len(ids))
    for b in BLOCKS:
        cols["id_block_%d" % b] = (rank // b).astype(str).tolist()
    return pd.DataFrame(cols, index=frame.index, dtype=object)


def _sig_data_ext(frame, records, items):
    """(codes over GIVEN + derived id columns, rarity weights, n_given)."""
    codes_g, rarity_g = _sig_data_all(frame, records, items)
    if codes_g is None:
        return None, None, 0
    extra = id_columns(frame)
    if extra.shape[1] == 0:
        return codes_g, rarity_g, codes_g.shape[1]
    codes_e = np.empty((len(frame), extra.shape[1]), dtype=np.int32)
    rarity_e = np.empty(extra.shape[1])
    for j, col in enumerate(extra.columns):
        codes_e[:, j] = pd.factorize(extra[col].astype(object))[0]
        _, counts = np.unique(codes_e[:, j], return_counts=True)
        f = counts / counts.sum()
        rarity_e[j] = -np.log(np.clip((f ** 2).sum(), 1e-6, 1.0))
    return (np.concatenate([codes_g, codes_e], axis=1),
            np.concatenate([rarity_g, rarity_e]), codes_g.shape[1])


def _id_agree(posteriors, query_pos, codes, weights, n_given):
    """True where the top candidate agrees with the query on at least
    one derived id column that carries weight."""
    armed = np.flatnonzero(weights[n_given:] > 0) + n_given
    out = np.zeros(len(query_pos), dtype=bool)
    if len(armed) == 0:
        return out
    for i, (q, (cands, qw)) in enumerate(zip(query_pos, posteriors)):
        if len(qw):
            c = cands[np.argmax(qw)]
            out[i] = bool((codes[q, armed] == codes[c, armed]).any())
    return out


def id_sharp_layer(frame, schema, model_dists, return_weights=False):
    records, items, options = _layout(frame, schema)
    predict_cols = [n for n in items if records[n]["class"] == "PREDICT"]
    heldout = frame[predict_cols].isna().any(axis=1).to_numpy()
    codes, rarity_w, n_given = _sig_data_ext(frame, records, items)
    empty = ({}, {}, None) if return_weights else ({}, {})
    if codes is None:
        return empty
    vis_pos = np.flatnonzero(~heldout)
    held_pos = np.flatnonzero(heldout)
    if len(vis_pos) < 2 or len(held_pos) == 0:
        return empty

    cal_pos = vis_pos
    if len(cal_pos) > CAL_QUERIES:
        rng = np.random.default_rng(CAL_SEED)
        cal_pos = np.sort(rng.choice(cal_pos, CAL_QUERIES,
                                     replace=False))
    # pass 1 exactly as E025: GIVEN-only rarity match -> provisional pairs
    post0 = _topk_excl(codes[:, :n_given], rarity_w[:n_given], cal_pos,
                       vis_pos)
    # Fellegi-Sunter weights for ALL columns from those pairs; derived id
    # columns with chance-level agreement get 0 and drop out
    weights, _ = estimate_weights(codes, rarity_w, cal_pos, post0)
    # evidence guard: a derived column keeps weight only if it actually
    # agreed on >= MIN_AGREE provisional pairs (Laplace smoothing alone
    # gives near-unique columns a spurious positive weight)
    pairs = [(q, cands[np.argmax(qw)]) for q, (cands, qw)
             in zip(cal_pos, post0) if len(qw) and qw.max() >= PAIR_MASS]
    if pairs:
        a = codes[[p for p, _ in pairs]]
        b = codes[[c for _, c in pairs]]
        agree_n = (a == b).sum(axis=0)
        weights = weights.copy()
        weights[n_given:][agree_n[n_given:] < MIN_AGREE] = 0.0
    else:
        weights = weights.copy()
        weights[n_given:] = 0.0
    cal_post = _topk_excl(codes, weights, cal_pos, vis_pos)
    ev_cal = _evidence(frame, items, records, options, cal_post, cal_pos)
    conc_cal = _max_q(cal_post) >= CONC_SPLIT
    idag_cal = _id_agree(cal_post, cal_pos, codes, weights, n_given)
    bucket_cal = conc_cal.astype(int) + (conc_cal & idag_cal).astype(int)

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
        pair = [0.0, 0.0]
        for b, mask in enumerate((~conc, conc)):
            if mask.sum() >= 30:
                pair[b] = _best_lambda(p_model[mask], p_ev[mask])
        # bucket 2 (concentrated AND id agreement) calibrates its own λ,
        # falling back to the pooled concentrated λ when thin
        three = [pair[0], pair[1], pair[1]]
        mask = bucket == 2
        if mask.sum() >= 30:
            three[2] = _best_lambda(p_model[mask], p_ev[mask])
        if any(l > 0 for l in three):
            lam[item] = tuple(three)
    if not lam:
        return empty

    post = _topk_excl(codes, weights, held_pos, vis_pos)
    ev = _evidence(frame, items, records, options, post, held_pos)
    conc_held = _max_q(post) >= CONC_SPLIT
    idag_held = _id_agree(post, held_pos, codes, weights, n_given)
    bucket_held = conc_held.astype(int) + (conc_held & idag_held).astype(int)
    ev_rows = {}
    for row_i, pos in enumerate(held_pos):
        ev_rows[pos] = ({item: ev[item][row_i] for item in ev},
                        int(bucket_held[row_i]))
    if return_weights:
        return ev_rows, lam, (weights, n_given)
    return ev_rows, lam


def predict(frame, schema, cols=None, kappas=None):
    return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                              layer_fn=id_sharp_layer, configs=CONFIGS)
