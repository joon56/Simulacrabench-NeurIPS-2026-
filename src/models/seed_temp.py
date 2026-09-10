"""E029 — net seed ensemble + per-instrument output temperature over E025.

Two calibration refinements to the shared-trunk stage, both decided on
the same outer holdout split that already picks the architecture and
the blend weight w:

  1. Seed ensemble: the selected architecture is trained N_SEEDS times
     (different torch seeds), and the net's distribution is the mean of
     the members' softmax outputs. Averaging removes the seed-specific
     part of an early-stopped full-batch net's error; on the hosted
     H100 the extra trainings are nearly free.
  2. Output temperature: the member logits are divided by T, chosen
     jointly with w from T_GRID x W_GRID by pooled log score on the
     outer split. Early stopping leaves the net's sharpness at whatever
     epoch the inner split picked; T lets the holdout correct it in
     either direction (T < 1 sharpens, T > 1 flattens).

Both reduce to E025 exactly at N_SEEDS = 1, T_GRID = (1.0,). Ladder,
gate recursion, E010 agreement and the E022/E025 evidence layer are
untouched — the ensemble is wrapped so downstream code sees one net.
"""

import numpy as np
import torch
from torch import nn

from src.models import link_sharp
from src.models import shared_trunk as st
from src.models.hier_backoff import (
    _layout, _complete_rows, _codes, build_ladder, ladder_lookup,
    HOLDOUT_SEED, HOLDOUT_FRAC,
)
from src.models.logit_blend import _given_matrix, _floored, W_GRID
from src.models.shared_trunk import (
    _targets, _pooled_ce, _train, _net_device, _tensor, DEFAULT_CONFIG,
)
from src.models.hh_cap import CONFIGS
from src.models.hh_sharp import hh_sharp_layer

N_SEEDS = 3
T_GRID = (0.8, 0.9, 1.0, 1.1, 1.25, 1.5)


class _Ensemble(nn.Module):
    """Averages member softmax outputs at temperature T; returns log-mean
    probabilities so shared_trunk._proba_maps (which softmaxes the
    output) yields exactly the averaged distribution."""

    def __init__(self, members, temperature=1.0):
        super().__init__()
        self.members = nn.ModuleList(members)
        self.temperature = float(temperature)

    def forward(self, x):
        fulls, conds = None, None
        for m in self.members:
            fl, cl = m(x)
            fl = [torch.softmax(l / self.temperature, dim=1) for l in fl]
            cl = [torch.softmax(l / self.temperature, dim=1) for l in cl]
            if fulls is None:
                fulls, conds = fl, cl
            else:
                fulls = [a + b for a, b in zip(fulls, fl)]
                conds = [a + b for a, b in zip(conds, cl)]
        n = len(self.members)
        return ([torch.log(f / n) for f in fulls],
                [torch.log(c / n) for c in conds])


def _train_seed(seed, *args, **kwargs):
    """shared_trunk._train with a different torch seed (its seed is a
    module constant; set-and-restore keeps every other caller bit-exact)."""
    prev = st.TORCH_SEED
    st.TORCH_SEED = seed
    try:
        return _train(*args, **kwargs)
    finally:
        st.TORCH_SEED = prev


def _member_probas(members, X, predict_items, T):
    """Mean over members of softmax(logits / T) on the full heads."""
    acc = None
    with torch.no_grad():
        for m in members:
            fl, _ = m(X.to(_net_device(m)))
            ps = [torch.softmax(l / T, dim=1).cpu().numpy() for l in fl]
            acc = ps if acc is None else [a + b for a, b in zip(acc, ps)]
    return {item: p / len(members) for item, p in zip(predict_items, acc)}


def tune_and_train(frame, schema, cols, kappas, configs=None, extra=None,
                   n_seeds=N_SEEDS, t_grid=T_GRID):
    """Drop-in for shared_trunk.tune_and_train: returns (w, ensemble net,
    layout helpers). Architecture selection is unchanged (seed 0 member);
    (T, w) are then tuned jointly on the outer split with all members."""
    records, items, options = _layout(frame, schema)
    predict_items = [n for n in items if records[n]["class"] == "PREDICT"]
    gated_items = [n for n in predict_items if records[n].get("gate")]
    full_dims = [len(options[n]) for n in predict_items]
    cond_dims = [len(records[n]["values"]) for n in gated_items]
    gated_value = schema["gated_value"]

    complete = _complete_rows(frame, items)
    rng = np.random.default_rng(HOLDOUT_SEED)
    mask = rng.random(len(complete)) < HOLDOUT_FRAC
    fit_rows, eval_rows = complete[~mask], complete[mask]
    if len(fit_rows) < 10 or len(eval_rows) == 0:
        return 0.0, None, (predict_items, gated_items)

    rng2 = np.random.default_rng(HOLDOUT_SEED + 1)
    inner = rng2.random(len(fit_rows)) < 0.2
    train_rows, val_rows = fit_rows[~inner], fit_rows[inner]

    def prep(rows):
        X = _tensor(_given_matrix(rows, records, items, options))
        if extra is not None:
            pos = frame.index.get_indexer(rows.index)
            X = torch.cat([X, torch.from_numpy(
                np.asarray(extra[pos], dtype=np.float32))], dim=1)
        f, c = _targets(rows, predict_items, options, records, gated_value)
        return X, torch.from_numpy(f), torch.from_numpy(c)

    X_tr, f_tr, c_tr = prep(train_rows)
    X_va, f_va, c_va = prep(val_rows)
    X_ev, f_ev, c_ev = prep(eval_rows)
    if configs is None:
        configs = (DEFAULT_CONFIG,)
    net, best_epoch, config = None, 0, DEFAULT_CONFIG
    best_ce = np.inf
    for cand in configs:
        cand_net, cand_epoch = _train(X_tr, f_tr, c_tr, X_va, f_va,
                                      c_va, full_dims, cond_dims,
                                      config=cand)
        with torch.no_grad():
            dev = _net_device(cand_net)
            fl, cl = cand_net(X_ev.to(dev))
            ce = float(_pooled_ce(fl, cl, f_ev.to(dev), c_ev.to(dev)))
        if ce < best_ce:
            best_ce, net, best_epoch, config = ce, cand_net, \
                cand_epoch, cand

    # further members of the selected architecture, on the same split
    seeds = [st.TORCH_SEED + i for i in range(n_seeds)]
    members, epochs = [net], [best_epoch]
    for seed in seeds[1:]:
        m, ep = _train_seed(seed, X_tr, f_tr, c_tr, X_va, f_va, c_va,
                            full_dims, cond_dims, config=config)
        members.append(m)
        epochs.append(ep)

    # (T, w) jointly on the outer eval split
    ladders, codes_by_item = {}, {}
    for item in predict_items:
        opts = options[item]
        codes_eval, valid = _codes(eval_rows, item, opts)
        if len(codes_eval) == 0:
            continue
        p0, levels = build_ladder(fit_rows, item, opts, cols, kappas)
        keys = list(map(tuple, eval_rows.loc[valid, cols].to_numpy())) \
            if cols else [() for _ in codes_eval]
        ladders[item] = np.stack([ladder_lookup(p0, levels, k)
                                  for k in keys])
        codes_by_item[item] = (codes_eval, np.asarray(valid))
    cells = sum(len(c) for c, _ in codes_by_item.values())
    if cells == 0:
        return 0.0, None, (predict_items, gated_items)
    best = (-np.inf, 1.0, 0.0)
    for T in t_grid:
        nn_full = _member_probas(members, X_ev, predict_items, T)
        totals = {w: 0.0 for w in W_GRID}
        for item, (codes_eval, valid) in codes_by_item.items():
            proba = nn_full[item][valid]
            rows_idx = np.arange(len(codes_eval))
            for w in W_GRID:
                mix = _floored(w * proba + (1.0 - w) * ladders[item])
                totals[w] += np.log(mix[rows_idx, codes_eval]).sum()
        for w in W_GRID:
            s = totals[w] / cells
            if s > best[0] + 1e-12:
                best = (s, T, w)
    _, T, w = best

    # final members: all complete rows, each member's own epoch budget
    X_all_fit, f_all, c_all = prep(complete)
    finals = []
    for seed, ep in zip(seeds, epochs):
        m, _ = _train_seed(seed, X_all_fit, f_all, c_all, None, None,
                           None, full_dims, cond_dims,
                           max_epochs=max(ep, 1), config=config)
        finals.append(m)
    return w, _Ensemble(finals, T), (predict_items, gated_items)


def predict(frame, schema, cols=None, kappas=None, n_seeds=N_SEEDS,
            t_grid=T_GRID):
    def tune_fn(frame, schema, cols, kappas, configs=None, extra=None):
        return tune_and_train(frame, schema, cols, kappas, configs=configs,
                              extra=extra, n_seeds=n_seeds, t_grid=t_grid)
    return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                              layer_fn=hh_sharp_layer, configs=CONFIGS,
                              tune_fn=tune_fn)


def predict_seeds_only(frame, schema, cols=None, kappas=None):
    return predict(frame, schema, cols, kappas, n_seeds=N_SEEDS,
                   t_grid=(1.0,))


def predict_temp_only(frame, schema, cols=None, kappas=None):
    return predict(frame, schema, cols, kappas, n_seeds=1, t_grid=T_GRID)
