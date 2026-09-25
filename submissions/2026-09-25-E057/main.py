"""HSCC submission — E025: household-aware full-pool evidence layer
(E022) over the shared-trunk model with the trunk architecture selected
per instrument from {64x2, 128x2+dropout} on the internal holdout (E017).

Self-contained merge of src/models/{hier_backoff, logit_blend (helpers),
cond_agree, shared_trunk, prob_link + dup_link (evidence utilities),
link_sharp, hh_link, hh_sharp}.py + the E025 configuration (submission
snapshot 2026-09-09). Runtime pass included (vectorized ladder
selection / evidence accumulation; training on CUDA when available with
CPU fallback). No bundled artifacts; torch and scikit-learn are
pre-installed in the hosted image.

Evidence layer (organizer-permitted 2026-09-02: matching rows within the
dataset is allowed): candidates for every held-out row are ALL visible
rows (self excluded); signature column weights are estimated from the
data (Fellegi-Sunter one iteration) so household-defining columns keep
weight while person-level columns lose it; softmax posterior over the
top-10; posterior-mixed candidate answers enter the belief at
per-(item, posterior-concentration) weights calibrated by replaying the
construction on visible rows. No signal tunes every weight to zero.
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
                    prev_ladders, prefix_cols, cand, kappa_grid,
                    code_cache=None):
    """Held-out log score per kappa for extending the ladder by `cand`.

    prev_ladders: {item: (p0, levels)} for the fixed prefix — built once
    per depth, reused across candidates and kappas.

    Vectorized (2026-09-07, hosted-timeout response): cells are
    factorized once per candidate, per-item counts become a
    [cells, K] matrix, and every kappa is scored with numpy on the
    truth column. Same numbers as the original row loop — an unseen
    eval cell (or a cell with no valid fit answers, whose smoothed
    vector equals its parent) falls back to the prefix ladder exactly
    as before.
    """
    cols = prefix_cols + [cand]
    fit_keys = list(map(tuple, fit_rows[cols].to_numpy()))
    eval_keys = list(map(tuple, eval_rows[cols].to_numpy()))
    cell_id = {}
    fit_cell = np.empty(len(fit_keys), dtype=np.int64)
    for i, key in enumerate(fit_keys):
        fit_cell[i] = cell_id.setdefault(key, len(cell_id))
    eval_cell = np.array([cell_id.get(key, -1) for key in eval_keys],
                         dtype=np.int64)
    cell_keys = list(cell_id)
    n_cells = len(cell_keys)

    if code_cache is None:
        code_cache = {item: (_codes(fit_rows, item, options[item]),
                             _codes(eval_rows, item, options[item]))
                      for item in predict_items}
    totals = {kappa: 0.0 for kappa in kappa_grid}
    cells = 0
    for item in predict_items:
        opts = options[item]
        k = len(opts)
        p0, prev_levels = prev_ladders[item]
        (codes_fit, valid_fit), (codes, valid) = code_cache[item]
        M = np.zeros((n_cells, k))
        np.add.at(M, (fit_cell[np.asarray(valid_fit)], codes_fit), 1.0)
        n_cell = M.sum(axis=1)
        Pm = np.stack([ladder_lookup(p0, prev_levels, key[:-1])
                       for key in cell_keys]) if n_cells else \
            np.zeros((0, k))

        ce = eval_cell[np.asarray(valid)]
        cells += len(codes)
        seen = ce >= 0
        c_t = M[ce[seen], codes[seen]]
        n_t = n_cell[ce[seen]]
        p_t = Pm[ce[seen], codes[seen]]
        valid_keys = [key for key, ok in zip(eval_keys, np.asarray(valid))
                      if ok]
        fb_keys = [key[:-1] for key, s in zip(valid_keys, seen) if not s]
        fb_codes = codes[~seen]
        fb = np.array([ladder_lookup(p0, prev_levels, fk)[c]
                       for fk, c in zip(fb_keys, fb_codes)])
        fb_log = np.log(np.maximum(fb, 1e-12)).sum() if len(fb) else 0.0
        for kappa in kappa_grid:
            p = (c_t + kappa * p_t) / (n_t + kappa)
            totals[kappa] += np.log(np.maximum(p, 1e-12)).sum() + fb_log
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

    code_cache = {item: (_codes(fit_rows, item, options[item]),
                         _codes(eval_rows, item, options[item]))
                  for item in predict_items}
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
                                     KAPPA_GRID, code_cache=code_cache)
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


DEFAULT_CONFIG = (HIDDEN, 2, 0.0)  # (width, depth, dropout) == E012


class _Net(nn.Module):
    def __init__(self, d_in, full_dims, cond_dims, config=DEFAULT_CONFIG):
        super().__init__()
        width, depth, dropout = config
        layers, d = [], d_in
        for _ in range(depth):
            layers += [nn.Linear(d, width), nn.ReLU()]
            if dropout > 0:
                layers.append(nn.Dropout(dropout))
            d = width
        self.trunk = nn.Sequential(*layers)
        self.full_heads = nn.ModuleList(
            [nn.Linear(width, k) for k in full_dims])
        self.cond_heads = nn.ModuleList(
            [nn.Linear(width, k) for k in cond_dims])

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


def _device():
    """Hosted runner has an H100; locally this is the CPU. The CPU path is
    unchanged bit-for-bit (all .to() calls are no-ops there)."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _train(X_fit, full_fit, cond_fit, X_val, full_val, cond_val,
           full_dims, cond_dims, max_epochs=MAX_EPOCHS,
           config=DEFAULT_CONFIG):
    dev = _device()
    try:
        return _train_on(dev, X_fit, full_fit, cond_fit, X_val, full_val,
                         cond_val, full_dims, cond_dims, max_epochs, config)
    except Exception:
        if dev.type != "cuda":
            raise
        # any GPU-side trouble (driver, memory, dtype) -> retrain on CPU
        return _train_on(torch.device("cpu"), X_fit, full_fit, cond_fit,
                         X_val, full_val, cond_val, full_dims, cond_dims,
                         max_epochs, config)


def _train_on(dev, X_fit, full_fit, cond_fit, X_val, full_val, cond_val,
              full_dims, cond_dims, max_epochs, config):
    torch.manual_seed(TORCH_SEED)
    net = _Net(X_fit.shape[1], full_dims, cond_dims, config).to(dev)
    X_fit, full_fit, cond_fit = (X_fit.to(dev), full_fit.to(dev),
                                 cond_fit.to(dev))
    if X_val is not None:
        X_val, full_val, cond_val = (X_val.to(dev), full_val.to(dev),
                                     cond_val.to(dev))
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


def _net_device(net):
    return next(net.parameters()).device


def _proba_maps(net, X_all, predict_items, gated_items):
    with torch.no_grad():
        fl, cl = net(X_all.to(_net_device(net)))
    full = {item: torch.softmax(logits, dim=1).cpu().numpy()
            for item, logits in zip(predict_items, fl)}
    cond = {item: torch.softmax(logits, dim=1).cpu().numpy()
            for item, logits in zip(gated_items, cl)}
    return full, cond


def _tensor(X):
    return torch.from_numpy(np.asarray(X.todense(), dtype=np.float32))


def tune_and_train(frame, schema, cols, kappas, configs=None, extra=None):
    """Returns (w, net trained on all complete rows, layout helpers).

    configs: optional tuple of (width, depth, dropout) architectures —
    each is trained on the inner split and the one with the best pooled
    CE on the OUTER eval split wins before w tuning. None keeps the
    single DEFAULT_CONFIG (bit-identical to E012)."""
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
        if extra is not None:  # extra: [len(frame), D] aligned to frame
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

    # blend weight on the outer eval split, net fit on the fit portion
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
                          max_epochs=max(best_epoch, 1), config=config)
    return w, final_net, (predict_items, gated_items)

TOP_K = 10

LAMBDA_GRID = tuple(round(0.1 * i, 1) for i in range(10))  # 0 .. 0.9

EV_FLOOR = 1e-3

def _evidence(frame, items, records, options, posteriors, query_pos):
    """{item: dist matrix aligned to query_pos} from candidate answers.

    Vectorized (2026-09-07, hosted-timeout response): candidates and
    posterior weights are packed into [n_query, K] matrices once, each
    item's answer column is coded once, and the weighted accumulation
    is a single np.add.at per item. Same numbers as the row loop."""
    predict_items = [n for n in items if records[n]["class"] == "PREDICT"]
    n_q = len(query_pos)
    k_max = max((len(c) for c, _ in posteriors), default=0)
    cand_mat = np.full((n_q, k_max), -1, dtype=np.int64)
    q_mat = np.zeros((n_q, k_max))
    for i, (cands, q) in enumerate(posteriors):
        cand_mat[i, :len(cands)] = cands
        q_mat[i, :len(q)] = q
    row_idx = np.repeat(np.arange(n_q), k_max)
    cand_flat = cand_mat.ravel()
    q_flat = q_mat.ravel()
    live = cand_flat >= 0

    ev = {}
    for item in predict_items:
        opt_index = {o: i for i, o in enumerate(options[item])}
        code_col = frame[item].map(opt_index).fillna(-1) \
            .to_numpy(dtype=np.int64)
        codes = np.full(len(cand_flat), -1, dtype=np.int64)
        codes[live] = code_col[cand_flat[live]]
        ok = codes >= 0
        mat = np.zeros((n_q, len(options[item])))
        np.add.at(mat, (row_idx[ok], codes[ok]), q_flat[ok])
        ev[item] = mat
    return ev

CAL_QUERIES = 6000   # cap on calibration replay queries (runtime guard;

CAL_SEED = 0         # lambda on 6k rows/item is plenty)

def _sig_data_all(frame, records, items):
    """Codes + rarity weights over the FULL GIVEN block (no exclusion)."""
    given = [n for n in items if records[n]["class"] == "GIVEN"]
    if not given:
        return None, None
    codes = np.empty((len(frame), len(given)), dtype=np.int32)
    weights = np.empty(len(given))
    for j, col in enumerate(given):
        vals = frame[col].astype(object).where(frame[col].notna(),
                                               "__NA__")
        codes[:, j] = pd.factorize(vals)[0]
        _, counts = np.unique(codes[:, j], return_counts=True)
        f = counts / counts.sum()
        weights[j] = -np.log(np.clip((f ** 2).sum(), 1e-6, 1.0))
    return codes, weights

def _topk_excl(codes, weights, query_pos, cand_pos, k=TOP_K, chunk=256):
    """Top-k posteriors with self-exclusion: a query row present in the
    candidate pool never matches itself."""
    cand = codes[cand_pos]
    cand_index = {pos: i for i, pos in enumerate(cand_pos)}
    w = weights[None, None, :]
    out = []
    for start in range(0, len(query_pos), chunk):
        block_pos = query_pos[start:start + chunk]
        block = codes[block_pos]
        score = ((block[:, None, :] == cand[None, :, :]) * w).sum(axis=2)
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

LAMBDA_GRID_X = tuple(round(0.1 * i, 1) for i in range(10)) + (0.95, 0.98)
CONC_SPLIT = 0.5   # max posterior weight >= this -> "concentrated" bucket


def _max_q(posteriors):
    return np.array([q.max() if len(q) else 0.0 for _, q in posteriors])


def _best_lambda(p_model, p_ev):
    best_l, best_s = 0.0, np.log(p_model).mean()
    for l in LAMBDA_GRID_X[1:]:
        s = np.log(np.maximum(
            (1 - l) * p_model + l * p_ev, EV_FLOOR)).mean()
        if s > best_s:
            best_l, best_s = l, s
    return best_l


def sharp_layer(frame, schema, model_dists):
    """(evidence for held-out rows incl. concentration flag,
    per-item (λ_diffuse, λ_concentrated))."""
    records, items, options = _layout(frame, schema)
    predict_cols = [n for n in items if records[n]["class"] == "PREDICT"]
    heldout = frame[predict_cols].isna().any(axis=1).to_numpy()
    codes, weights = _sig_data_all(frame, records, items)
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


def predict(frame, schema, cols=None, kappas=None, layer_fn=None,
            extra_fn=None, configs=None):
    if layer_fn is None:
        layer_fn = sharp_layer
    frame = frame.reset_index(drop=True)
    records, items, options = _layout(frame, schema)
    if cols is None:
        cols, kappas, _ = select_ladder(frame, schema)
    extra = extra_fn(frame, schema) if extra_fn is not None else None
    w, net, (predict_items, gated_items) = tune_and_train(
        frame, schema, cols, kappas, configs=configs, extra=extra)

    complete = _complete_rows(frame, items)
    if net is not None and w > 0:
        X_all = _tensor(_given_matrix(frame, records, items, options))
        if extra is not None:
            X_all = torch.cat([X_all, torch.from_numpy(
                np.asarray(extra, dtype=np.float32))], dim=1)
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

    values = frame[items].to_numpy(dtype=object)
    col_idx = [items.index(c) for c in cols]
    keys_all = [tuple(values[r, i] for i in col_idx)
                for r in range(len(frame))]

    def blended(tables, probas, item, key, row):
        p0, levels = tables[item]
        ladder = ladder_lookup(p0, levels, key)
        logit = probas[item][row]
        if logit.sum() <= 0:
            return ladder
        return w * logit + (1.0 - w) * ladder

    def model_dist_matrix(item):
        p0, levels = full_tables[item]
        base = np.stack([ladder_lookup(p0, levels, k) for k in keys_all])
        logit = full_proba[item]
        if logit.sum() <= 0:
            return base
        return w * logit + (1.0 - w) * base

    model_dists = {item: model_dist_matrix(item)
                   for item in predict_items}
    ev_rows, lam = layer_fn(frame, schema, model_dists)

    out = []
    for row in range(values.shape[0]):
        key = keys_all[row]
        entry_row = ev_rows.get(row)
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
            if entry_row is not None:
                ev, conc = entry_row
                pair = lam.get(item)
                e = ev.get(item)
                if pair is not None and e is not None and e.sum() > 0:
                    l = pair[1] if conc else pair[0]
                    if l > 0:
                        base = (1.0 - l) * base + l * e
            belief[item] = base
            out.append(belief[item])
    return out

PAIR_MASS = 0.5     # top-1 posterior mass needed for a provisional pair

MIN_PAIRS = 30

def estimate_weights(codes, rarity_w, vis_pos, posteriors):
    """Household-aware column weights from provisional pairs.
    Returns (weights, n_pairs); falls back to rarity when too few
    concentrated pairs exist."""
    pairs = []
    for q, (cands, q_w) in zip(vis_pos, posteriors):
        if len(q_w) and q_w.max() >= PAIR_MASS:
            pairs.append((q, cands[np.argmax(q_w)]))
    if len(pairs) < MIN_PAIRS:
        return rarity_w, len(pairs)
    a = codes[[p for p, _ in pairs]]
    b = codes[[c for _, c in pairs]]
    agree = (a == b).mean(axis=0)
    m = (agree * len(pairs) + 1.0) / (len(pairs) + 2.0)
    u = np.exp(-rarity_w)                     # rarity_w = -log u_j
    m = np.clip(m, 1e-4, 1.0 - 1e-4)
    u = np.clip(u, 1e-4, 1.0 - 1e-4)
    w = np.log(m / u) - np.log((1.0 - m) / (1.0 - u))
    return np.maximum(w, 0.0), len(pairs)

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

# ---------------------------------------------------- E025 entry point

_SHARP_PREDICT = predict
CONFIGS = (
    (64, 2, 0.0),    # E012 baseline
    (128, 2, 0.1),   # E017's per-instrument winner on wb and unhcr
)


def predict(frame, schema, cols=None, kappas=None):
    return _SHARP_PREDICT(frame, schema, cols=cols, kappas=kappas,
                          layer_fn=hh_sharp_layer, configs=CONFIGS)

# E041: supervised section retrieval; E025 remains the fallback.
_E025_PREDICT = predict

def candidate_indices(codes, weights, query, bank, k=32, chunk=128):
    """Return frame positions of GIVEN-only nearest donors, excluding queries."""
    query, bank = (np.asarray(query, dtype=int), np.sort(np.asarray(bank, dtype=int)))
    overlap = np.isin(query, bank).any()
    width = max(0, min(k, len(bank) - int(overlap)))
    result = np.empty((len(query), width), dtype=int)
    if width == 0:
        return result
    bank_codes = codes[bank]
    for start in range(0, len(query), chunk):
        rows = query[start:start + chunk]
        scores = np.zeros((len(rows), len(bank)), dtype=np.float64)
        for j, weight in enumerate(weights):
            scores += weight * (codes[rows, j, None] == bank_codes[None, :, j])
        scores[rows[:, None] == bank[None, :]] = -np.inf
        idx = np.argpartition(scores, -width, axis=1)[:, -width:]
        for row in range(len(rows)):
            order = np.lexsort((bank[idx[row]], -scores[row, idx[row]]))
            result[start + row] = bank[idx[row, order]]
    return result

"""E041: supervised section-specific metrics over the E025 evidence pool.

Reference, fitting-query, selection and new-metric replay labels are disjoint.
The selector is a marginal/retrieval proxy: its section mixture shares are not
the deployed E025 per-item shares, and tied donors can differ from E025's old
sort policy. Full-stack outer evaluation is required. The retained E025 base
is still in-sample during lambda replay; this limitation is not repaired by
the new metric. No source module or incumbent snapshot is modified.
"""
import re
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit, softmax
from threadpoolctl import threadpool_limits
RETRIEVAL_K = 32
FIT_QUERIES = 1200
SELECT_QUERIES = 800
REPLAY_QUERIES = 800
METRIC_ITERATIONS = 50
METRIC_PENALTY = 0.001
MIN_SECTION_GAIN = 0.003
LAST_DIAGNOSTICS = {}

def metric_objective(params, features, matches, prior_truth, sizes, initial):
    """Officially floored section log loss and analytic metric gradient."""
    sizes, initial = (np.asarray(sizes), np.asarray(initial))
    weights, share = (params[:-1], expit(params[-1]))
    posterior = softmax(np.einsum('qkd,d->qk', features, weights), axis=1)
    evidence = np.einsum('qk,qki->qi', posterior, matches)
    scale = 1.0 - EV_FLOOR * sizes
    probability = EV_FLOOR + scale * ((1 - share) * prior_truth + share * evidence)
    residual = weights - initial
    loss = -np.log(probability).mean() + METRIC_PENALTY * np.mean(residual ** 2)
    derivative = -scale / probability / probability.size
    donor_gradient = np.einsum('qi,qki->qk', share * derivative, matches)
    score_gradient = posterior * (donor_gradient - (posterior * donor_gradient).sum(axis=1, keepdims=True))
    gradient_w = np.einsum('qk,qkd->d', score_gradient, features)
    gradient_w += 2 * METRIC_PENALTY * residual / len(weights)
    gradient_share = np.sum(derivative * (evidence - prior_truth)) * share * (1 - share)
    return (float(loss), np.append(gradient_w, gradient_share))

def _retrieval_log(features, matches, prior, sizes, weights, share):
    posterior = softmax(np.einsum('qkd,d->qk', features, weights), axis=1)
    evidence = np.einsum('qk,qki->qi', posterior, matches)
    probability = (1 - share) * prior + share * evidence
    return np.log(EV_FLOOR + (1 - EV_FLOOR * np.asarray(sizes)) * probability)

def fit_sections(codes, labels, bank, fit, select, initial, sizes, groups, k=RETRIEVAL_K, maxiter=METRIC_ITERATIONS, min_gain=MIN_SECTION_GAIN):
    """Fit metric weights without selector labels; select on separate rows."""
    bank, fit, select = (np.asarray(x, dtype=int) for x in (bank, fit, select))
    if any((len(np.intersect1d(a, b)) for a, b in ((bank, fit), (bank, select), (fit, select)))):
        raise ValueError('Reference, fit and selection rows must be disjoint')
    if min(len(bank), len(fit), len(select)) == 0:
        raise ValueError('Reference, fit and selection partitions must be nonempty')
    sizes = np.asarray(sizes)
    initial = np.maximum(np.asarray(initial, dtype=float), 0)
    query = np.concatenate((fit, select))
    donors = candidate_indices(codes, initial, query, bank, k=k)
    features = (codes[query, None, :] == codes[donors]).astype(float)
    nf = len(fit)
    priors = []
    for j, size in enumerate(sizes):
        counts = np.bincount(labels[bank, j], minlength=int(size)) + 0.5
        priors.append(counts / counts.sum())
    prior_truth = np.stack([p[labels[query, j]] for j, p in enumerate(priors)], axis=1)
    learned, active, diagnostics = ([], [], [])
    with threadpool_limits(limits=2):
        for group_idx, indices in enumerate(groups):
            ix = np.asarray(indices, dtype=int)
            matches = (labels[donors][:, :, ix] == labels[query][:, None, ix]).astype(float)
            pr = prior_truth[:, ix]
            dim = sizes[ix]
            grid = (0.0, 0.25, 0.5, 0.75, 0.9, 0.98)
            old_k = min(10, donors.shape[1])
            old_share = max(grid, key=lambda v: _retrieval_log(features[:nf, :old_k], matches[:nf, :old_k], pr[:nf], dim, initial, v).mean())
            start = np.append(np.clip(initial, 0, 12), 0.0)
            fitted = minimize(metric_objective, start, args=(features[:nf], matches[:nf], pr[:nf], dim, initial), jac=True, method='L-BFGS-B', bounds=[(0.0, 12.0)] * len(initial) + [(-5.0, 5.0)], options={'maxiter': maxiter, 'ftol': 1e-07})
            if not np.isfinite(fitted.x).all():
                learned.append(initial.copy())
                diagnostics.append({'selected': False, 'reason': 'nonfinite fit'})
                continue
            weights, share = (fitted.x[:-1].copy(), float(expit(fitted.x[-1])))
            learned.append(weights)
            old = _retrieval_log(features[nf:, :old_k], matches[nf:, :old_k], pr[nf:], dim, initial, old_share).mean(axis=1)
            new = _retrieval_log(features[nf:], matches[nf:], pr[nf:], dim, weights, share).mean(axis=1)
            delta = new - old
            se = float(delta.std(ddof=1) / np.sqrt(len(delta))) if len(delta) > 1 else np.inf
            gain = float(delta.mean())
            selected = bool(gain > max(min_gain, 2 * se))
            if selected:
                active.append(group_idx)
            diagnostics.append({'selected': selected, 'gain_log': gain, 'standard_error': se, 'old_share': float(old_share), 'new_share': share, 'iterations': int(fitted.nit)})
    return (learned, active, diagnostics)

def _groups(predicted):
    groups = {}
    for index, item in enumerate(predicted):
        match = re.match('s(\\d+[a-z]?)_', item)
        groups.setdefault(match.group(1) if match else 'other', []).append(index)
    return list(groups.values())

def _replace_evidence(evidence, frame, records, items, options, codes, query, bank, initial, predicted, groups, learned, active):
    if not active:
        return evidence
    donors = candidate_indices(codes, initial, query, bank, k=RETRIEVAL_K)
    features = (codes[query, None, :] == codes[donors]).astype(float)
    for group_idx in active:
        posterior = softmax(np.einsum('qkd,d->qk', features, learned[group_idx]), axis=1)
        post = [(positions, weights) for positions, weights in zip(donors, posterior)]
        selected_items = [predicted[i] for i in groups[group_idx]]
        evidence.update(_evidence(frame, selected_items, records, options, post, query))
    return evidence

def supervised_layer(frame, schema, model_dists):
    records, items, options = _layout(frame, schema)
    predicted = [n for n in items if records[n]['class'] == 'PREDICT']
    hidden = frame[predicted].isna().any(axis=1).to_numpy()
    visible, held = (np.flatnonzero(~hidden), np.flatnonzero(hidden))
    if len(visible) < 500 or len(held) == 0:
        return hh_sharp_layer(frame, schema, model_dists)
    codes, rarity = _sig_data_all(frame, records, items)
    if codes is None:
        return ({}, {})
    cal = visible
    if len(cal) > CAL_QUERIES:
        cal = np.sort(np.random.default_rng(CAL_SEED).choice(cal, CAL_QUERIES, replace=False))
    preliminary = _topk_excl(codes, rarity, cal, visible)
    initial, _ = estimate_weights(codes, rarity, cal, preliminary)
    labels = np.stack([frame[n].map({v: i for i, v in enumerate(options[n])}).fillna(-1).to_numpy(dtype=int) for n in predicted], axis=1)
    shuffled = np.random.default_rng(4101).permutation(visible)
    nfit = min(FIT_QUERIES, max(1, len(visible) // 5))
    nselect = min(SELECT_QUERIES, max(1, len(visible) // 10))
    nreplay = min(REPLAY_QUERIES, max(1, len(visible) // 10))
    fit, select = (shuffled[:nfit], shuffled[nfit:nfit + nselect])
    replay = shuffled[nfit + nselect:nfit + nselect + nreplay]
    bank = shuffled[nfit + nselect + nreplay:]
    groups = _groups(predicted)
    sizes = [len(options[n]) for n in predicted]
    learned, active, diagnostics = fit_sections(codes, labels, bank, fit, select, initial, sizes, groups)
    LAST_DIAGNOSTICS.clear()
    LAST_DIAGNOSTICS.update({'sections': diagnostics, 'active': active, 'fit_rows': len(fit), 'selection_rows': len(select), 'reference_rows': len(bank), 'replay_rows': len(replay)})
    original_cal = cal
    if active:
        cal = np.union1d(cal, replay)
    active_items = {predicted[i] for g in active for i in groups[g]}
    cal_post = _topk_excl(codes, initial, cal, visible)
    ev_cal = _evidence(frame, items, records, options, cal_post, cal)
    ev_cal = _replace_evidence(ev_cal, frame, records, items, options, codes, cal, visible, initial, predicted, groups, learned, active)
    conc_cal = _max_q(cal_post) >= CONC_SPLIT
    lam = {}
    for j, item in enumerate(predicted):
        truth = labels[cal, j]
        eligible = replay if item in active_items else original_cal
        ok = (truth >= 0) & np.isin(cal, eligible)
        if not ok.any():
            continue
        rows = np.arange(ok.sum())
        p_model = np.maximum(model_dists[item][cal[ok]][rows, truth[ok]], EV_FLOOR)
        p_ev = ev_cal[item][ok][rows, truth[ok]]
        pair = [0.0, 0.0]
        for bucket, mask in enumerate((~conc_cal[ok], conc_cal[ok])):
            if mask.sum() >= 30:
                pair[bucket] = _best_lambda(p_model[mask], p_ev[mask])
        if pair[0] > 0 or pair[1] > 0:
            lam[item] = tuple(pair)
    if not lam:
        return ({}, {})
    post = _topk_excl(codes, initial, held, visible)
    ev = _evidence(frame, items, records, options, post, held)
    ev = _replace_evidence(ev, frame, records, items, options, codes, held, visible, initial, predicted, groups, learned, active)
    conc = _max_q(post) >= CONC_SPLIT
    rows = {position: ({item: ev[item][i] for item in ev}, bool(conc[i])) for i, position in enumerate(held)}
    return (rows, lam)

def predict(frame, schema, cols=None, kappas=None):
    if 's3_11_intent_return_12m_lbl' not in schema['items']:
        return _E025_PREDICT(frame, schema, cols=cols, kappas=kappas)
    return _SHARP_PREDICT(frame, schema, cols=cols, kappas=kappas, layer_fn=supervised_layer, configs=CONFIGS)

# E057: names isolated to preserve immutable E041 globals.
_e057_incumbent_predict = predict
def _e057_floor_mix(proba, floor=0.001):
    """Official flooring: renormalize, then mix with a flat vector so every
    entry is at least `floor` and the vector still sums to 1 (score.py's
    `floored`). Clip-then-renormalize would not keep both properties."""
    proba = _e057_np.asarray(proba, dtype=float)
    p = proba / proba.sum(axis=-1, keepdims=True)
    k = p.shape[-1]
    return floor + (1.0 - k * floor) * p
'E057: honest visible-row selection and refit of UNHCR leaf content.\n\nOnly GIVEN features enter trees. Diagnostics are optional local callbacks;\nthe normal predict contract returns probability vectors only.\n'
from time import perf_counter as _e057_perf_counter
import numpy as _e057_np
from sklearn.ensemble import HistGradientBoostingClassifier as _e057_HistGradientBoostingClassifier
from threadpoolctl import threadpool_limits as _e057_threadpool_limits
_e057_MARKER = 's3_11_intent_return_12m_lbl'
_e057_SHARES = (0.0, 0.25, 0.5)
_e057_SPLIT_SEED = 5701
_e057_TREE_PARAMETERS = dict(max_iter=40, max_leaf_nodes=15, learning_rate=0.1, l2_regularization=1.0, early_stopping=False, random_state=0, max_bins=255)

def _e057_layout(schema):
    records = schema['items']
    predicted = [n for n, r in records.items() if r['class'] == 'PREDICT']
    parents = {r['gate']['parent'] for r in records.values() if r.get('gate')}
    leaves = [n for n in predicted if records[n].get('gate') and n not in parents]
    given = [n for n, r in records.items() if r['class'] == 'GIVEN']
    return (predicted, leaves, given)

def _e057_split_visible(visible):
    shuffled = _e057_np.random.default_rng(_e057_SPLIT_SEED).permutation(visible)
    count = min(1200, len(visible) // 5)
    return (_e057_np.sort(shuffled[2 * count:]), _e057_np.sort(shuffled[:count]), _e057_np.sort(shuffled[count:2 * count]))

def _e057_features(frame, schema, given):
    if not given or any((len(schema['items'][n]['values']) > 255 for n in given)):
        return None
    values = _e057_np.column_stack([frame[n].map({v: i for i, v in enumerate(schema['items'][n]['values'])}).to_numpy(dtype=float) for n in given])
    return values if _e057_np.isfinite(values).all() else None

def _e057_fit_trees(masked, schema, query, leaves):
    predicted, _, given = _e057_layout(schema)
    missing = masked[predicted].isna().to_numpy()
    if not _e057_np.array_equal(_e057_np.flatnonzero(missing.any(1)), query) or not missing[query].all():
        raise ValueError('Whole non-fit target block masking required')
    visible = _e057_np.flatnonzero(~missing.any(1))
    x = _e057_features(masked, schema, given)
    if x is None:
        raise ValueError('Unsupported GIVEN vocabulary')
    result, details = ({}, {})
    with _e057_threadpool_limits(limits=2):
        for name in leaves:
            options = schema['items'][name]['values']
            asked = visible[masked.iloc[visible][name].ne(schema['gated_value']).to_numpy()]
            encoded = masked.iloc[asked][name].map({v: i for i, v in enumerate(options)})
            if encoded.isna().any():
                raise ValueError(f'Invalid answer code: {name}')
            labels = encoded.to_numpy(dtype=int)
            counts = _e057_np.bincount(labels, minlength=len(options))
            trained = len(asked) >= 100 and _e057_np.count_nonzero(counts) >= 2
            details[name] = {'asked_rows': len(asked), 'observed_classes': int(_e057_np.count_nonzero(counts)), 'trained': bool(trained)}
            if not trained:
                result[name] = None
                continue
            tree = _e057_HistGradientBoostingClassifier(**_e057_TREE_PARAMETERS, categorical_features=[True] * len(given))
            tree.fit(x[asked], labels)
            probability = _e057_np.zeros((len(query), len(options)))
            probability[:, _e057_np.asarray(tree.classes_, dtype=int)] = tree.predict_proba(x[query])
            result[name] = 0.99 * probability + 0.01 * (counts + 1) / (counts.sum() + len(options))
    return (result, details)

def _e057_mix_content(p, q, alpha):
    if alpha == 0 or q is None:
        return p
    mass = p[:, :-1].sum(1)
    changed = p.copy()
    rows = mass > 0
    changed[rows, :-1] = (1 - alpha) * p[rows, :-1] + alpha * mass[rows, None] * q[rows]
    return changed

def _e057_validate_vectors(raw, predicted, query, records):
    if len(raw) != len(predicted) * len(query):
        raise ValueError('Output length or schema order contract failed')
    for j, name in enumerate(predicted):
        width = len(records[name]['values']) + bool(records[name].get('gate'))
        p = _e057_np.asarray(raw[j::len(predicted)], dtype=float)
        if p.shape != (len(query), width) or not _e057_np.isfinite(p).all() or (p < 0).any() or (p.sum(1) <= 0).any():
            raise ValueError(f'Invalid probability vectors: {name}')

def _e057_apply_policy(raw, predicted, query, trees, shares):
    if not any((a and trees.get(n) is not None for n, a in shares.items())):
        return raw
    output = list(raw)
    for name, alpha in shares.items():
        q = trees.get(name)
        if alpha == 0 or q is None:
            continue
        j = predicted.index(name)
        p = _e057_np.stack(raw[j::len(predicted)])
        changed = _e057_mix_content(p, q, alpha)
        _e057_np.testing.assert_array_equal(p[:, -1], changed[:, -1])
        _e057_np.testing.assert_allclose(p.sum(1), changed.sum(1), atol=1e-12, rtol=0)
        for i in _e057_np.flatnonzero(p[:, :-1].sum(1) > 0):
            output[int(i) * len(predicted) + j] = changed[i]
    return output

def _e057_mean_se(difference):
    return (float(_e057_np.mean(difference)), float(_e057_np.std(difference, ddof=1) / _e057_np.sqrt(len(difference))))

def _e057_choose_shares(base, trees, frame, schema, positions, query_index, leaves):
    shares, diagnostics = ({}, {})
    at = query_index[positions]
    for name in leaves:
        q = trees[name]
        if q is None:
            shares[name] = 0.0
            diagnostics[name] = {'reason': 'sparse_or_constant'}
            continue
        options = list(schema['items'][name]['values']) + [schema['gated_value']]
        labels = frame.iloc[positions][name].map({v: i for i, v in enumerate(options)}).to_numpy(dtype=int)
        p = base[name][at]
        logs = [_e057_np.log(_e057_floor_mix(_e057_mix_content(p, q[at], a))[_e057_np.arange(len(at)), labels]) for a in _e057_SHARES]
        choice = int(_e057_np.argmax([v.mean() for v in logs]))
        gain, se = _e057_mean_se(logs[choice] - logs[0])
        shares[name] = _e057_SHARES[choice] if gain > 0 and gain > 2 * se else 0.0
        diagnostics[name] = {'proposed': _e057_SHARES[choice], 'gain_log': gain, 'se': se}
    return (shares, diagnostics)

def _e057_validate_policy(base, trees, shares, frame, schema, positions, query_index, predicted):
    at = query_index[positions]
    difference = _e057_np.zeros(len(at))
    for name, alpha in shares.items():
        if alpha == 0:
            continue
        options = list(schema['items'][name]['values']) + [schema['gated_value']]
        labels = frame.iloc[positions][name].map({v: i for i, v in enumerate(options)}).to_numpy(dtype=int)
        p = base[name][at]
        before = _e057_floor_mix(p)
        after = _e057_floor_mix(_e057_mix_content(p, trees[name][at], alpha))
        difference += _e057_np.log(after[_e057_np.arange(len(at)), labels]) - _e057_np.log(before[_e057_np.arange(len(at)), labels])
    u = _e057_np.mean([_e057_np.log(len(schema['items'][n]['values']) + bool(schema['items'][n].get('gate'))) for n in predicted])
    difference /= len(predicted) * u
    gain, se = _e057_mean_se(difference)
    return {'gain_skill': gain, 'se_skill': se, 'accepted': bool(gain > 0 and gain > 2 * se), 'rows': len(positions), 'paired_difference': difference}

def _e057_predict(frame, schema, *, base_predict=None, observer=None):
    base_predict = _e057_incumbent_predict if base_predict is None else base_predict

    def emit(event, payload):
        if observer is not None:
            observer(event, payload)

    def fit_call(stage, function, *args):
        started = _e057_perf_counter()
        emit('fit_start', {'stage': stage})
        try:
            return function(*args)
        finally:
            emit('fit_end', {'stage': stage, 'seconds': _e057_perf_counter() - started})

    def fallback(reason):
        emit('fallback', {'reason': reason})
        return fit_call('final_base', base_predict, frame, schema)
    predicted, leaves, given = _e057_layout(schema)
    if _e057_MARKER not in schema['items']:
        return fallback('other_instrument')
    if not leaves:
        return fallback('no_gated_leaf')
    work = frame.reset_index(drop=True).copy()
    missing = work[predicted].isna().to_numpy()
    query = _e057_np.flatnonzero(missing.any(1))
    visible = _e057_np.flatnonzero(~missing.any(1))
    if not len(query) or not missing[query].all():
        return fallback('unsupported_missingness')
    if _e057_features(work, schema, given) is None:
        return fallback('unsupported_given')
    fit, selection, validation = _e057_split_visible(visible)
    if len(visible) < 2000 or min(len(selection), len(validation)) < 200:
        return fallback('small_visible_sample')
    shadow = work.copy()
    shadow_query = _e057_np.setdiff1d(_e057_np.arange(len(work)), fit)
    shadow.loc[shadow_query, predicted] = _e057_np.nan
    emit('split', {'fit': fit, 'selection': selection, 'validation': validation, 'query': query, 'shadow_query': shadow_query, 'masked_frame': shadow})
    raw_shadow = fit_call('shadow_base', base_predict, shadow, schema)
    _e057_validate_vectors(raw_shadow, predicted, shadow_query, schema['items'])
    trees, shadow_details = fit_call('shadow_trees', _e057_fit_trees, shadow, schema, shadow_query, leaves)
    base = {name: _e057_np.stack(raw_shadow[j::len(predicted)]) for j, name in enumerate(predicted)}
    emit('shadow_frozen', {'base': base, 'trees': trees, 'query': shadow_query, 'details': shadow_details})
    query_index = _e057_np.full(len(work), -1, dtype=int)
    query_index[shadow_query] = _e057_np.arange(len(shadow_query))
    shares, selection_details = _e057_choose_shares(base, trees, work, schema, selection, query_index, leaves)
    emit('selection_frozen', {'shares': shares.copy(), 'details': selection_details})
    if any(shares.values()):
        validation_result = _e057_validate_policy(base, trees, shares, work, schema, validation, query_index, predicted)
        emit('validation_scored', validation_result)
        if not validation_result['accepted']:
            shares = dict.fromkeys(leaves, 0.0)
    emit('policy_frozen', {'shares': shares.copy()})
    raw_full = fit_call('final_base', base_predict, work, schema)
    _e057_validate_vectors(raw_full, predicted, query, schema['items'])
    full_trees, full_details = fit_call('refit_trees', _e057_fit_trees, work, schema, query, leaves)
    emit('refit_frozen', {'base': raw_full, 'trees': full_trees, 'query': query, 'details': full_details, 'shadow_query_index': query_index[query]})
    output = _e057_apply_policy(raw_full, predicted, query, full_trees, shares)
    _e057_validate_vectors(output, predicted, query, schema['items'])
    emit('final', {'base': raw_full, 'output': output, 'shares': shares.copy()})
    return output
predict = _e057_predict
