"""E039 — gradient-boosted trees as a second base model, blended into the
E025 stack on the outer holdout.

A005 showed the shared-trunk net sits at the GIVEN-only Bayes ceiling
of the sandbox, so no base-model change can be validated locally — but
on real data the ladder still earns a blend weight (w ≈ 0.6–0.9 vs 1.0
on the sandbox), i.e. the net leaves real GIVEN interactions on the
table. Per-item HistGradientBoosting classifiers on the integer-coded
GIVEN block (categorical splits) are the cheapest strong nonparametric
conditional. They are fitted ONCE on the fit split (no refit on all
rows — the runtime budget), mixed into the full-head distribution at a
per-instrument weight v chosen on the outer holdout (v = 0 ⇒ E025
exactly), and only where the instrument is large enough to matter
(MIN_ROWS). Gated items use the tree only through the soft (full-head)
part of the gate mixture; the asked-only conditional stays net/ladder.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

from src.models import link_sharp
from src.models.hier_backoff import (
    _layout, _complete_rows, _codes, build_ladder, ladder_lookup,
    HOLDOUT_SEED, HOLDOUT_FRAC,
)
from src.models.logit_blend import _floored
from src.models.shared_trunk import tune_and_train, _tensor, _proba_maps
from src.models.logit_blend import _given_matrix
from src.models.hh_sharp import hh_sharp_layer
from src.models.hh_cap import CONFIGS

V_GRID = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5)
MAX_ITER = 40
MAX_LEAF = 15
MIN_ROWS = 4000        # instruments smaller than this keep E025 (v = 0)
MIN_PREDICT = 150      # only the large instrument (unhcr) gets trees
CONTENT_ONLY = True    # E040: ungated PREDICT items only (runtime)
LAST_V = {}            # diagnostics: instrument size -> chosen v


def _given_codes(frame, records, items):
    given = [n for n in items if records[n]["class"] == "GIVEN"]
    X = np.empty((len(frame), len(given)), dtype=np.int64)
    for j, col in enumerate(given):
        opts = {o: i for i, o in enumerate(records[col]["values"])}
        X[:, j] = frame[col].map(opts).fillna(len(opts)).to_numpy(
            dtype=np.int64)
    return X


def _fit_trees(X, rows, predict_items, options, frame):
    trees = {}
    for item in predict_items:
        opts = options[item]
        idx = {o: i for i, o in enumerate(opts)}
        y = frame[item].iloc[rows].map(idx)
        ok = y.notna().to_numpy()
        yv = y[ok].to_numpy(dtype=np.int64)
        if len(yv) < 50 or len(np.unique(yv)) < 2:
            continue
        clf = HistGradientBoostingClassifier(
            max_iter=MAX_ITER, max_leaf_nodes=MAX_LEAF, learning_rate=0.1,
            categorical_features=list(range(X.shape[1])),
            early_stopping=False, random_state=0)
        clf.fit(X[rows][ok], yv)
        trees[item] = (clf, len(opts))
    return trees


def _tree_proba(trees, X, predict_items):
    out = {}
    for item in predict_items:
        if item not in trees:
            continue
        clf, k = trees[item]
        p = np.zeros((X.shape[0], k))
        p[:, clf.classes_] = clf.predict_proba(X)
        out[item] = p
    return out


def tune_and_train_trees(frame, schema, cols, kappas, configs=None,
                         extra=None):
    """Drop-in for shared_trunk.tune_and_train: returns (w, net wrapper,
    layout). The wrapper is the E025 net; the tree mixture is applied by
    `predict` below through the returned closure attributes."""
    w, net, layout = tune_and_train(frame, schema, cols, kappas,
                                    configs=configs, extra=extra)
    return w, net, layout


def predict(frame, schema, cols=None, kappas=None):
    frame = frame.reset_index(drop=True)
    records, items, options = _layout(frame, schema)
    predict_items = [n for n in items if records[n]["class"] == "PREDICT"]
    complete = _complete_rows(frame, items)
    if len(complete) < MIN_ROWS or len(predict_items) < MIN_PREDICT:
        return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                                  layer_fn=hh_sharp_layer, configs=CONFIGS)

    # the same outer split the net uses
    rng = np.random.default_rng(HOLDOUT_SEED)
    mask = rng.random(len(complete)) < HOLDOUT_FRAC
    fit_rows, eval_rows = complete[~mask], complete[mask]
    X = _given_codes(frame, records, items)
    fit_pos = frame.index.get_indexer(fit_rows.index)
    eval_pos = frame.index.get_indexer(eval_rows.index)
    tree_items = ([n for n in predict_items if not records[n].get("gate")]
                  if CONTENT_ONLY else predict_items)
    trees = _fit_trees(X, fit_pos, tree_items, options, frame)
    tree_eval = _tree_proba(trees, X[eval_pos], predict_items)

    # E025's own net + blend on the same split, to tune v against the
    # SAME base the final predict will use
    if cols is None:
        from src.models.hier_backoff import select_ladder
        cols, kappas, _ = select_ladder(frame, schema)
    w, net, (pi, gi) = tune_and_train(frame, schema, cols, kappas,
                                      configs=CONFIGS)
    if net is None or w <= 0:
        return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                                  layer_fn=hh_sharp_layer, configs=CONFIGS)
    X_ev = _tensor(_given_matrix(eval_rows, records, items, options))
    nn_full, _ = _proba_maps(net, X_ev, pi, gi)
    totals = {v: 0.0 for v in V_GRID}
    cells = 0
    for item in predict_items:
        opts = options[item]
        codes_eval, valid = _codes(eval_rows, item, opts)
        if len(codes_eval) == 0 or item not in tree_eval:
            continue
        valid = np.asarray(valid)
        p0, levels = build_ladder(fit_rows, item, opts, cols, kappas)
        keys = list(map(tuple, eval_rows.loc[valid, cols].to_numpy())) \
            if cols else [() for _ in codes_eval]
        ladder = np.stack([ladder_lookup(p0, levels, k) for k in keys])
        base = w * nn_full[item][valid] + (1.0 - w) * ladder
        tr = tree_eval[item][valid]
        rows_idx = np.arange(len(codes_eval))
        cells += len(codes_eval)
        for v in V_GRID:
            mix = _floored((1.0 - v) * base + v * tr)
            totals[v] += np.log(mix[rows_idx, codes_eval]).sum()
    v = max(totals, key=lambda x: totals[x] / max(cells, 1)) if cells else 0.0
    LAST_V[len(frame)] = (v, {k: round(t / max(cells, 1), 5) for k, t in totals.items()})
    if v <= 0:
        return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                                  layer_fn=hh_sharp_layer, configs=CONFIGS)

    tree_all = _tree_proba(trees, X, predict_items)

    def layer_fn(frame_, schema_, model_dists):
        return hh_sharp_layer(frame_, schema_, model_dists)

    # mix the trees into the full-head probabilities the stack consumes:
    # wrap tune_and_train so link_sharp.predict receives a net whose
    # full-head output already contains the tree share
    import torch
    from torch import nn as _nn

    class _Mixed(_nn.Module):
        def __init__(self, base):
            super().__init__()
            self.base = base

        def forward(self, x):
            fl, cl = self.base(x)
            n = x.shape[0]
            out = []
            for item, logits in zip(pi, fl):
                p = torch.softmax(logits, dim=1)
                if item in tree_all and n == tree_all[item].shape[0]:
                    t = torch.from_numpy(tree_all[item]).to(p.dtype).to(p.device)
                    p = (1.0 - v) * p + v * t
                out.append(torch.log(p + 1e-12))
            return out, cl

    def tune_fn(frame_, schema_, cols_, kappas_, configs=None, extra=None):
        return w, _Mixed(net), (pi, gi)

    return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                              layer_fn=layer_fn, configs=CONFIGS,
                              tune_fn=tune_fn)
