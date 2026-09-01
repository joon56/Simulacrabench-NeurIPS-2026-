"""HSCC submission — E012: shared-trunk multi-head network + backoff
ladder + conditional gate-agreement softening.

Self-contained merge of src/models/{hier_backoff, logit_blend (helpers),
cond_agree, shared_trunk}.py (submission snapshot 2026-09-02). No bundled
artifacts; torch and scikit-learn are pre-installed in the hosted image.

Per instrument: one-hot GIVEN block -> shared Linear-ReLU-Linear-ReLU
trunk -> per-PREDICT-item softmax heads (full distributions incl. the
gate sentinel) + asked-only conditional heads, trained jointly with
early stopping on an internal split; blended in probability space with a
greedy-selected hierarchical count-backoff ladder (blend weight per
instrument from the internal holdout). Gates: hard coupling through the
respondent's own parent belief, softened by a beta-binomial-shrunk
agreement rate optionally conditioned on one data-selected GIVEN column.
"""

import numpy as np
import pandas as pd
import torch
from torch import nn
from sklearn.preprocessing import OneHotEncoder

MAX_CARD = 12
KAPPA_GRID = (1.0, 3.0, 10.0, 30.0, 100.0)
MAX_DEPTH = 3
HOLDOUT_FRAC = 0.2
HOLDOUT_SEED = 0
EVAL_CAP = 3000  # cap on holdout eval rows, keeps selection under budget
ALPHA = 20.0


def _layout(frame, schema):
    gated_value = schema["gated_value"]
    records = schema["items"]
    items = [n for n, r in records.items()
             if r["class"] in ("GIVEN", "PREDICT")]
    options = {}
    for item in items:
        r = records[item]
        options[item] = list(r["values"]) + (
            [gated_value] if r.get("gate") else [])
    return records, items, options


def _complete_rows(frame, items):
    return frame[frame[items].notna().all(axis=1)]


def _codes(rows, item, options):
    opt_index = {o: i for i, o in enumerate(options)}
    codes = rows[item].map(opt_index)
    valid = codes.notna()
    return codes[valid].astype(int).to_numpy(), valid


def _level_counts(rows, item, options, cols):
    """dict cell_tuple -> count vector over options (raw counts)."""
    opt_index = {o: i for i, o in enumerate(options)}
    k = len(options)
    counted = (rows.groupby(cols, sort=False, observed=True)[item]
               .value_counts())
    out = {}
    for idx, n in counted.items():
        *cell, value = idx if isinstance(idx, tuple) else (idx,)
        code = opt_index.get(value)
        if code is None:
            continue
        key = tuple(cell)
        vec = out.get(key)
        if vec is None:
            vec = np.zeros(k)
            out[key] = vec
        vec[code] += n
    return out


def build_ladder(rows, item, options, cols, kappas):
    """Return (p0, [level-1 dict, level-2 dict, ...]) of distributions."""
    codes, _ = _codes(rows, item, options)
    k = len(options)
    global_counts = np.full(k, 0.5)
    np.add.at(global_counts, codes, 1.0)
    p0 = global_counts / global_counts.sum()

    levels = []
    prev = None  # dict at L-1 (None means p0 for every parent)
    for depth in range(1, len(cols) + 1):
        counts = _level_counts(rows, item, options, cols[:depth])
        kappa = kappas[depth - 1]
        table = {}
        for key, vec in counts.items():
            parent = p0 if prev is None else prev.get(key[:-1], p0)
            n = vec.sum()
            table[key] = (vec + kappa * parent) / (n + kappa)
        levels.append(table)
        prev = table
    return p0, levels


def ladder_lookup(p0, levels, key):
    for depth in range(len(levels), 0, -1):
        vec = levels[depth - 1].get(key[:depth])
        if vec is not None:
            return vec
    return p0


def _eval_candidate(fit_rows, eval_rows, predict_items, options,
                    prev_ladders, prefix_cols, cand, kappa_grid):
    """Held-out log score per kappa for extending the ladder by `cand`.

    prev_ladders: {item: (p0, levels)} for the fixed prefix — built once
    per depth, reused across candidates and kappas.
    """
    cols = prefix_cols + [cand]
    eval_keys = list(map(tuple, eval_rows[cols].to_numpy()))
    totals = {kappa: 0.0 for kappa in kappa_grid}
    cells = 0
    for item in predict_items:
        opts = options[item]
        p0, prev_levels = prev_ladders[item]
        counts = _level_counts(fit_rows, item, opts, cols)
        codes, valid = _codes(eval_rows, item, opts)
        keys = [k for k, ok in zip(eval_keys, valid) if ok]
        cells += len(codes)
        parent_of = {key: ladder_lookup(p0, prev_levels, key[:-1])
                     for key in counts}
        for kappa in kappa_grid:
            table = {key: (vec + kappa * parent_of[key]) /
                     (vec.sum() + kappa)
                     for key, vec in counts.items()}
            logp = 0.0
            for key, code in zip(keys, codes):
                vec = table.get(key)
                if vec is None:
                    vec = ladder_lookup(p0, prev_levels, key[:-1])
                logp += np.log(max(vec[code], 1e-12))
            totals[kappa] += logp
    return {kappa: totals[kappa] / max(cells, 1) for kappa in kappa_grid}


def select_ladder(frame, schema):
    """Greedy (columns, kappas) selection on an internal holdout."""
    records, items, options = _layout(frame, schema)
    predict_items = [n for n in items if records[n]["class"] == "PREDICT"]
    candidates = [n for n in items
                  if records[n]["class"] == "GIVEN"
                  and len(records[n]["values"]) <= MAX_CARD]
    complete = _complete_rows(frame, items)
    rng = np.random.default_rng(HOLDOUT_SEED)
    mask = rng.random(len(complete)) < HOLDOUT_FRAC
    fit_rows, eval_rows = complete[~mask], complete[mask]
    if len(eval_rows) > EVAL_CAP:
        eval_rows = eval_rows.sample(EVAL_CAP, random_state=HOLDOUT_SEED)

    # depth-0 baseline: global marginal only
    base_total, base_cells = 0.0, 0
    marginals = {}
    for item in predict_items:
        opts = options[item]
        codes_fit, _ = _codes(fit_rows, item, opts)
        gc = np.full(len(opts), 0.5)
        np.add.at(gc, codes_fit, 1.0)
        marginals[item] = gc / gc.sum()
        codes, _ = _codes(eval_rows, item, opts)
        base_total += np.log(np.maximum(marginals[item][codes], 1e-12)).sum()
        base_cells += len(codes)
    best_score = base_total / max(base_cells, 1)

    cols, kappas = [], []
    history = [(list(cols), list(kappas), best_score)]
    while len(cols) < MAX_DEPTH:
        prev_ladders = {item: build_ladder(fit_rows, item, options[item],
                                           cols, kappas)
                        for item in predict_items}
        best_step = None
        for cand in candidates:
            if cand in cols:
                continue
            scores = _eval_candidate(fit_rows, eval_rows, predict_items,
                                     options, prev_ladders, cols, cand,
                                     KAPPA_GRID)
            kappa = max(scores, key=scores.get)
            if scores[kappa] > best_score and (
                    best_step is None or scores[kappa] > best_step[2]):
                best_step = (cand, kappa, scores[kappa])
        if best_step is None:
            break
        cols.append(best_step[0])
        kappas.append(best_step[1])
        best_score = best_step[2]
        history.append((list(cols), list(kappas), best_score))
    return cols, kappas, history


def agreement_weights(frame, schema):
    records = schema["items"]
    gated_value = schema["gated_value"]
    items = [n for n, r in records.items()
             if r["class"] in ("GIVEN", "PREDICT")]
    raw, counts = {}, {}
    for item in items:
        gate = records[item].get("gate")
        if not gate or gate["parent"] not in frame.columns:
            continue
        parent, child = frame[gate["parent"]], frame[item]
        both = parent.notna() & child.notna()
        if not both.any():
            continue
        asked = parent[both].isin(gate["observed_if"])
        agree = ((child[both] == gated_value) == ~asked).sum()
        raw[item] = agree / both.sum()
        counts[item] = (int(agree), int(both.sum()))
    if not raw:
        return {}
    m = float(np.median(list(raw.values())))
    return {item: (k + ALPHA * m) / (n + ALPHA)
            for item, (k, n) in counts.items()}


W_GRID = tuple(round(0.1 * i, 1) for i in range(11))

C_REG = 1.0

MAX_ITER = 200

FLOOR = 1e-3

def _given_matrix(frame, records, items, options):
    """One-hot encode the GIVEN block for every row of frame (sparse)."""
    given = [n for n in items if records[n]["class"] == "GIVEN"]
    enc = OneHotEncoder(categories=[options[g] for g in given],
                        handle_unknown="ignore", sparse_output=True)
    block = frame[given].astype(object).where(
        frame[given].notna(), "__NA__")
    return enc.fit_transform(block)

def _floored(p):
    """Approximate the grader's flat-mix floor for holdout scoring."""
    k = p.shape[-1]
    eps = min(1.0, FLOOR * k)
    return (1.0 - eps) * p + eps / k

COND_MAX_CARD = 12
COND_HOLDOUT_FRAC = 0.2


def _bernoulli_ll(y, p):
    p = np.clip(p, 1e-6, 1.0 - 1e-6)
    return float(np.sum(y * np.log(p) + (1 - y) * np.log(1.0 - p)))


def _value_table(values, y, shrink_to):
    table = {}
    for val in pd.unique(values):
        sel = values == val
        k, n = y[sel].sum(), sel.sum()
        table[val] = (k + ALPHA * shrink_to) / (n + ALPHA)
    return table


def conditional_agreement(frame, schema):
    """Per gated item: (scalar ã, selected column or None, {value: ã_v})."""
    records = schema["items"]
    gated_value = schema["gated_value"]
    items = [n for n, r in records.items()
             if r["class"] in ("GIVEN", "PREDICT")]
    candidates = [n for n in items
                  if records[n]["class"] == "GIVEN"
                  and len(records[n]["values"]) <= COND_MAX_CARD]

    raw = {}
    for item in items:
        gate = records[item].get("gate")
        if not gate or gate["parent"] not in frame.columns:
            continue
        parent, child = frame[gate["parent"]], frame[item]
        both = parent.notna() & child.notna()
        if not both.any():
            continue
        asked = parent[both].isin(gate["observed_if"])
        agree = ((child[both] == gated_value) == ~asked).to_numpy()
        raw[item] = (agree, frame.index[both])
    if not raw:
        return {}

    m = float(np.median([agree.mean() for agree, _ in raw.values()]))
    rng = np.random.default_rng(HOLDOUT_SEED)
    out = {}
    for item, (y, idx) in raw.items():
        k, n = y.sum(), len(y)
        scalar = (k + ALPHA * m) / (n + ALPHA)
        mask = rng.random(n) < COND_HOLDOUT_FRAC
        if mask.sum() == 0 or (~mask).sum() == 0:
            out[item] = (scalar, None, {})
            continue
        y_fit, y_eval = y[~mask], y[mask]
        scalar_fit = (y_fit.sum() + ALPHA * m) / (len(y_fit) + ALPHA)
        best_col, best_ll = None, _bernoulli_ll(
            y_eval, np.full(len(y_eval), scalar_fit))
        sub = frame.loc[idx]
        for col in candidates:
            v = sub[col].to_numpy(dtype=object)
            table = _value_table(v[~mask], y_fit, scalar_fit)
            p_eval = np.array([table.get(val, scalar_fit)
                               for val in v[mask]])
            ll = _bernoulli_ll(y_eval, p_eval)
            if ll > best_ll:
                best_col, best_ll = col, ll
        if best_col is None:
            out[item] = (scalar, None, {})
        else:
            v = sub[best_col].to_numpy(dtype=object)
            out[item] = (scalar, best_col, _value_table(v, y, scalar))
    return out

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
