"""E012 — shared-trunk multi-head network replacing the per-item logistic.

One network per instrument: one-hot GIVEN block -> Linear-ReLU-Linear-ReLU
trunk -> per-item softmax heads (full distributions incl. the gate
sentinel) + asked-only conditional heads for gated items (masked CE).
Marginalizing a latent respondent factor makes P(item | GIVEN) nonlinear
in the one-hots, and the shared trunk pools information across all items
— both things the independent main-effects logistics cannot do.

Training: pooled cross-entropy (sum over heads / total cells), Adam,
full-batch, early stopping on an inner validation split; the final net
retrains on all complete rows for the selected epoch count. The blend
weight w per instrument (same grid, same holdout) stays as the
calibration guard. Ladder, gate recursion, and E010's conditional
agreement are unchanged.
"""

import numpy as np
import pandas as pd
import torch
from torch import nn

from src.models.hier_backoff import (
    _layout, _complete_rows, _codes, build_ladder, ladder_lookup,
    select_ladder, HOLDOUT_SEED, HOLDOUT_FRAC,
)
from src.models.logit_blend import _given_matrix, _floored, W_GRID
from src.models.cond_agree import conditional_agreement

HIDDEN = 64
LR = 3e-3
WEIGHT_DECAY = 1e-4
MAX_EPOCHS = 500
PATIENCE = 30
TORCH_SEED = 0


class _Net(nn.Module):
    def __init__(self, d_in, full_dims, cond_dims):
        super().__init__()
        self.trunk = nn.Sequential(
            nn.Linear(d_in, HIDDEN), nn.ReLU(),
            nn.Linear(HIDDEN, HIDDEN), nn.ReLU())
        self.full_heads = nn.ModuleList(
            [nn.Linear(HIDDEN, k) for k in full_dims])
        self.cond_heads = nn.ModuleList(
            [nn.Linear(HIDDEN, k) for k in cond_dims])

    def forward(self, x):
        z = self.trunk(x)
        return ([h(z) for h in self.full_heads],
                [h(z) for h in self.cond_heads])


def _targets(rows, predict_items, options, records, gated_value):
    """(full targets [n, I], cond targets [n, G] with -1 = not asked)."""
    full, cond = [], []
    for item in predict_items:
        opt_index = {o: i for i, o in enumerate(options[item])}
        full.append(rows[item].map(opt_index).to_numpy(dtype=np.int64))
        if records[item].get("gate"):
            values = {o: i for i, o in
                      enumerate(records[item]["values"])}
            cond.append(rows[item].map(values).fillna(-1)
                        .to_numpy(dtype=np.int64))
    full = np.stack(full, axis=1)
    cond = (np.stack(cond, axis=1) if cond
            else np.zeros((len(rows), 0), dtype=np.int64))
    return full, cond


def _pooled_ce(full_logits, cond_logits, full_t, cond_t):
    loss, count = 0.0, 0
    for j, logits in enumerate(full_logits):
        t = full_t[:, j]
        loss = loss + nn.functional.cross_entropy(logits, t,
                                                  reduction="sum")
        count += len(t)
    for j, logits in enumerate(cond_logits):
        t = cond_t[:, j]
        mask = t >= 0
        if mask.any():
            loss = loss + nn.functional.cross_entropy(
                logits[mask], t[mask], reduction="sum")
            count += int(mask.sum())
    return loss / max(count, 1)


def _train(X_fit, full_fit, cond_fit, X_val, full_val, cond_val,
           full_dims, cond_dims, max_epochs=MAX_EPOCHS):
    torch.manual_seed(TORCH_SEED)
    net = _Net(X_fit.shape[1], full_dims, cond_dims)
    opt = torch.optim.Adam(net.parameters(), lr=LR,
                           weight_decay=WEIGHT_DECAY)
    best_val, best_epoch, best_state = np.inf, 0, None
    for epoch in range(1, max_epochs + 1):
        net.train()
        opt.zero_grad()
        fl, cl = net(X_fit)
        loss = _pooled_ce(fl, cl, full_fit, cond_fit)
        loss.backward()
        opt.step()
        if X_val is None:
            continue
        net.eval()
        with torch.no_grad():
            fl, cl = net(X_val)
            val = float(_pooled_ce(fl, cl, full_val, cond_val))
        if val < best_val - 1e-5:
            best_val, best_epoch = val, epoch
            best_state = {k: v.clone()
                          for k, v in net.state_dict().items()}
        elif epoch - best_epoch >= PATIENCE:
            break
    if best_state is not None:
        net.load_state_dict(best_state)
    net.eval()
    return net, (best_epoch if X_val is not None else max_epochs)


def _proba_maps(net, X_all, predict_items, gated_items):
    with torch.no_grad():
        fl, cl = net(X_all)
    full = {item: torch.softmax(logits, dim=1).numpy()
            for item, logits in zip(predict_items, fl)}
    cond = {item: torch.softmax(logits, dim=1).numpy()
            for item, logits in zip(gated_items, cl)}
    return full, cond


def _tensor(X):
    return torch.from_numpy(np.asarray(X.todense(), dtype=np.float32))


def tune_and_train(frame, schema, cols, kappas):
    """Returns (w, net trained on all complete rows, layout helpers)."""
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

    # inner early-stop split inside the fit portion
    rng2 = np.random.default_rng(HOLDOUT_SEED + 1)
    inner = rng2.random(len(fit_rows)) < 0.2
    train_rows, val_rows = fit_rows[~inner], fit_rows[inner]

    def prep(rows):
        X = _tensor(_given_matrix(rows, records, items, options))
        f, c = _targets(rows, predict_items, options, records, gated_value)
        return X, torch.from_numpy(f), torch.from_numpy(c)

    X_tr, f_tr, c_tr = prep(train_rows)
    X_va, f_va, c_va = prep(val_rows)
    net, best_epoch = _train(X_tr, f_tr, c_tr, X_va, f_va, c_va,
                             full_dims, cond_dims)

    # blend weight on the outer eval split, net fit on the fit portion
    X_ev = _tensor(_given_matrix(eval_rows, records, items, options))
    nn_full, _ = _proba_maps(net, X_ev, predict_items, gated_items)
    totals = {w: 0.0 for w in W_GRID}
    cells = 0
    for item in predict_items:
        opts = options[item]
        codes_eval, valid = _codes(eval_rows, item, opts)
        if len(codes_eval) == 0:
            continue
        proba = nn_full[item][np.asarray(valid)]
        p0, levels = build_ladder(fit_rows, item, opts, cols, kappas)
        keys = list(map(tuple, eval_rows.loc[valid, cols].to_numpy())) \
            if cols else [() for _ in codes_eval]
        ladder = np.stack([ladder_lookup(p0, levels, key) for key in keys])
        rows_idx = np.arange(len(codes_eval))
        cells += len(codes_eval)
        for w in W_GRID:
            mix = _floored(w * proba + (1.0 - w) * ladder)
            totals[w] += np.log(mix[rows_idx, codes_eval]).sum()
    if cells == 0:
        return 0.0, None, (predict_items, gated_items)
    w = max(totals, key=lambda x: totals[x] / cells)

    # final net: all complete rows, the selected epoch budget, no val
    X_all_fit, f_all, c_all = prep(complete)
    final_net, _ = _train(X_all_fit, f_all, c_all, None, None, None,
                          full_dims, cond_dims,
                          max_epochs=max(best_epoch, 1))
    return w, final_net, (predict_items, gated_items)


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
                belief[item] = blended(full_tables, full_proba,
                                       item, key, row)
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
                belief[item] = a * hard + (1.0 - a) * soft
            out.append(belief[item])
    return out
