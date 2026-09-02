"""E013 — cross-round respondent linkage over E012.

Organizer ruling 2026-09-02: matching rows WITHIN the dataset is
permitted. The real unhcr design is a panel flattened into two CATI
rounds inside one fieldwork window, so a held-out respondent's twin row
in the other round — when it is visible — nearly answers the sheet.

Layer mechanics (all runtime-estimated, nothing hardcoded to real data):
- round column: the 2-valued GIVEN item named like wave/round; absent
  (unicef, world_bank, sample) -> layer inert.
- signature: the full GIVEN block minus the round column; fuzzy 1:1
  matching — the best cross-round candidate is accepted only when it
  agrees on all but <= MAX_MISMATCH columns (with a 90% relative floor,
  so low-dimensional signatures stay exact), beats the runner-up by
  >= MIN_MARGIN columns, and no other held-out row claims it more
  closely. Fuzziness covers real panels where a household's roster
  shifts slightly between rounds.
- per-item stability s_i: share of visible-visible twin pairs giving
  the same answer, beta-shrunk (alpha=20) to the item median; with no
  visible-visible pairs the layer stays off.
- prediction for a matched held-out row: belief = s_i * ((1-eps) *
  onehot(twin answer) + eps * model) + (1 - s_i) * model, applied
  BEFORE children consume the parent belief, so the gate cascade
  sharpens too. Unmatched rows fall through to E012 unchanged.

On the sandbox rows are independent, signature groups of size 2 across
rounds are vanishing-rare, and no visible-visible pairs support the
stability estimate -> degenerates to E012 (pre-registered evidence 1).
"""

import numpy as np
import pandas as pd

from src.models.hier_backoff import (
    _layout, _complete_rows, _codes, build_ladder, ladder_lookup,
    select_ladder,
)
from src.models.logit_blend import _given_matrix
from src.models.cond_agree import conditional_agreement
from src.models.shared_trunk import tune_and_train, _tensor, _proba_maps

LINK_ALPHA = 20.0
TWIN_EPS = 0.02
ROUND_TOKENS = ("wave", "round")
MIN_PAIRS = 30  # visible-visible pairs needed before the layer engages


def find_round_col(records, items):
    for n in items:
        r = records[n]
        if r["class"] != "GIVEN" or len(r["values"]) != 2:
            continue
        low = n.lower()
        if any(tok in low for tok in ROUND_TOKENS):
            return n
    return None


MAX_MISMATCH = 2   # fuzzy: allow up to this many differing GIVEN columns
MIN_MARGIN = 2     # best match must beat the runner-up by this many cols


def _sig_codes(frame, records, items, round_col):
    given = [n for n in items
             if records[n]["class"] == "GIVEN" and n != round_col]
    codes = np.empty((len(frame), len(given)), dtype=np.int32)
    for j, col in enumerate(given):
        vals = frame[col].astype(object).where(frame[col].notna(),
                                               "__NA__")
        codes[:, j] = pd.factorize(vals)[0]
    return codes


def _best_matches(codes, query_pos, cand_pos, chunk=256):
    """For each query row: (best candidate pos, agree count, margin)."""
    n_cols = codes.shape[1]
    out = []
    cand = codes[cand_pos]
    for start in range(0, len(query_pos), chunk):
        block = codes[query_pos[start:start + chunk]]
        agree = (block[:, None, :] == cand[None, :, :]).sum(axis=2)
        order = np.argsort(agree, axis=1)
        best = order[:, -1]
        second = agree[np.arange(len(block)), order[:, -2]] \
            if agree.shape[1] > 1 else np.zeros(len(block))
        for i in range(len(block)):
            out.append((cand_pos[best[i]],
                        int(agree[i, best[i]]),
                        int(agree[i, best[i]] - second[i])))
    return out, n_cols


def build_links(frame, records, items, round_col):
    """Returns (twin_of: {heldout row pos: visible row pos},
    vis_pairs: [(pos_a, pos_b)]). Fuzzy 1:1 matching: accept the best
    cross-round candidate when it agrees on all but <= MAX_MISMATCH
    signature columns AND beats the runner-up by >= MIN_MARGIN columns;
    a visible row claimed by two held-out rows keeps only the closer
    one."""
    predict_cols = [n for n in items if records[n]["class"] == "PREDICT"]
    heldout = frame[predict_cols].isna().any(axis=1).to_numpy()
    rounds = frame[round_col].to_numpy(dtype=object)
    codes = _sig_codes(frame, records, items, round_col)
    round_vals = pd.unique(rounds)
    if len(round_vals) != 2:
        return {}, []
    r_a = rounds == round_vals[0]

    def accept(matches, n_cols):
        # relative floor keeps low-dimensional signatures effectively
        # exact (2 cols -> exact) while 71 cols tolerate MAX_MISMATCH
        need = max(n_cols - MAX_MISMATCH,
                   int(np.ceil(0.9 * n_cols)))
        return [(q, c, agree) for (q, (c, agree, margin)) in matches
                if agree >= need and margin >= MIN_MARGIN]

    twin_of = {}
    claimed = {}
    for q_mask, c_mask in ((r_a, ~r_a), (~r_a, r_a)):
        q_pos = np.flatnonzero(q_mask & heldout)
        c_pos = np.flatnonzero(c_mask & ~heldout)
        if len(q_pos) == 0 or len(c_pos) == 0:
            continue
        found, n_cols = _best_matches(codes, q_pos, c_pos)
        for q, cand, agree in accept(zip(q_pos, found), n_cols):
            prev = claimed.get(cand)
            if prev is None or agree > prev[1]:
                if prev is not None:
                    twin_of.pop(prev[0], None)
                claimed[cand] = (q, agree)
                twin_of[q] = cand

    vis_pairs, used = [], set()
    q_pos = np.flatnonzero(r_a & ~heldout)
    c_pos = np.flatnonzero(~r_a & ~heldout)
    if len(q_pos) and len(c_pos):
        found, n_cols = _best_matches(codes, q_pos, c_pos)
        for q, cand, agree in accept(zip(q_pos, found), n_cols):
            if cand not in used:
                used.add(cand)
                vis_pairs.append((q, cand))
    return twin_of, vis_pairs


def stability(frame, records, items, vis_pairs):
    """Per-PREDICT-item shrunk cross-round answer-stability. Empty when
    fewer than MIN_PAIRS visible-visible pairs support it — a handful of
    signature collisions on truly independent rows must not arm the
    layer."""
    if len(vis_pairs) < MIN_PAIRS:
        return {}
    predict_cols = [n for n in items if records[n]["class"] == "PREDICT"]
    a_idx = [a for a, _ in vis_pairs]
    b_idx = [b for _, b in vis_pairs]
    raw, counts = {}, {}
    for item in predict_cols:
        va = frame[item].to_numpy(dtype=object)[a_idx]
        vb = frame[item].to_numpy(dtype=object)[b_idx]
        ok = pd.notna(va) & pd.notna(vb)
        n = int(ok.sum())
        if n == 0:
            continue
        k = int((va[ok] == vb[ok]).sum())
        raw[item] = k / n
        counts[item] = (k, n)
    if not raw:
        return {}
    m = float(np.median(list(raw.values())))
    return {item: (k + LINK_ALPHA * m) / (n + LINK_ALPHA)
            for item, (k, n) in counts.items()}


def predict(frame, schema, cols=None, kappas=None, link_fn=None):
    if link_fn is None:
        link_fn = build_links
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

    round_col = find_round_col(records, items)
    if round_col is not None:
        twin_of, vis_pairs = link_fn(frame, records, items, round_col)
        stab = stability(frame, records, items, vis_pairs)
        if not stab:
            twin_of = {}
    else:
        twin_of, stab = {}, {}

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
        twin = twin_of.get(row)
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
            if twin is not None:
                s = stab.get(item, 0.0)
                tv = values[twin, col]
                if s > 0.0 and not pd.isna(tv) and tv in options[item]:
                    onehot = np.zeros(len(options[item]))
                    onehot[options[item].index(tv)] = 1.0
                    base = s * ((1.0 - TWIN_EPS) * onehot
                                + TWIN_EPS * base) + (1.0 - s) * base
            belief[item] = base
            out.append(belief[item])
    return out
