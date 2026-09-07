"""E023 — evidence layer stack 2 over E022.

Two replay-measured refinements on top of household-aware weights and
the sharpened λ layer:

  (1) K chosen by the replay from K_GRID: the K=10 posterior is computed
      once and restricted to its top-k masses (renormalized) for each
      candidate k; the k whose per-(item, bucket) λ calibration gives the
      best pooled replay log score wins, and held-out evidence is built
      at that k.
  (2) EM_ITERS weight-estimation passes: provisional pairs from the
      learned weights are purer than the rarity pass's, so a second
      estimate of the column agreement rates is cleaner.

Everything else — pool, self-exclusion, caps, λ ceiling 0.98,
concentration buckets, E012 stack — is E022's.
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

K_GRID = (3, 5, 10)
EM_ITERS = 2


def _restrict(posteriors, k):
    """Restrict top-K posteriors to their k largest masses."""
    if k >= max(len(q) for _, q in posteriors):
        return posteriors
    out = []
    for cands, q in posteriors:
        if len(q) > k:
            keep = np.argsort(q)[-k:]
            qq = q[keep]
            out.append((cands[keep], qq / qq.sum()))
        else:
            out.append((cands, q))
    return out


def _calibrate(frame, items, records, options, cal_post, cal_pos,
               model_dists):
    """Per-(item, bucket) λ and the pooled replay log score achieved."""
    ev_cal = _evidence(frame, items, records, options, cal_post, cal_pos)
    conc_cal = _max_q(cal_post) >= CONC_SPLIT
    values = frame[items].to_numpy(dtype=object)
    col_of = {n: i for i, n in enumerate(items)}
    lam, total, cells = {}, 0.0, 0
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
            l = pair[b]
            if mask.any():
                total += np.log(np.maximum(
                    (1 - l) * p_model[mask] + l * p_ev[mask],
                    EV_FLOOR)).sum()
                cells += int(mask.sum())
        if pair[0] > 0 or pair[1] > 0:
            lam[item] = tuple(pair)
    return lam, (total / cells if cells else -np.inf)


def make_layer(k_grid=K_GRID, em_iters=EM_ITERS):
    def layer(frame, schema, model_dists):
        records, items, options = _layout(frame, schema)
        predict_cols = [n for n in items
                        if records[n]["class"] == "PREDICT"]
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
        k_max = max(k_grid)

        # weights: rarity -> EM iterations
        weights = rarity_w
        for _ in range(em_iters):
            post = _topk_excl(codes, weights, cal_pos, vis_pos, k=k_max)
            weights, _ = estimate_weights(codes, rarity_w, cal_pos, post)

        # K selection on the replay
        post_max = _topk_excl(codes, weights, cal_pos, vis_pos, k=k_max)
        best = None
        for k in k_grid:
            lam_k, score_k = _calibrate(
                frame, items, records, options, _restrict(post_max, k),
                cal_pos, model_dists)
            if best is None or score_k > best[1]:
                best = (k, score_k, lam_k)
        k_star, _, lam = best
        if not lam:
            return {}, {}

        post = _restrict(_topk_excl(codes, weights, held_pos, vis_pos,
                                    k=k_max), k_star)
        ev = _evidence(frame, items, records, options, post, held_pos)
        conc_held = _max_q(post) >= CONC_SPLIT
        ev_rows = {}
        for row_i, pos in enumerate(held_pos):
            ev_rows[pos] = ({item: ev[item][row_i] for item in ev},
                            bool(conc_held[row_i]))
        return ev_rows, lam
    return layer


def predict(frame, schema, cols=None, kappas=None, k_grid=K_GRID,
            em_iters=EM_ITERS):
    return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                              layer_fn=make_layer(k_grid, em_iters))
