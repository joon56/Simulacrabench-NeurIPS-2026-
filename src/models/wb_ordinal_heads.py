"""E062: one WB16 conditional-logit head, retaining E041 pipeline policies."""
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

from src.models import shared_trunk, hh_cap, link_sharp, supervised_retrieval
from src.models.hh_sharp import hh_sharp_layer
from src.models.hier_backoff import (
    _layout, _complete_rows, _codes, build_ladder, ladder_lookup,
    HOLDOUT_SEED, HOLDOUT_FRAC,
)
from src.models.logit_blend import _given_matrix, _floored, W_GRID
from src.models.shared_trunk import (
    _targets, _pooled_ce, _device, _net_device, _proba_maps, _tensor,
    DEFAULT_CONFIG, LR, WEIGHT_DECAY, MAX_EPOCHS, PATIENCE, TORCH_SEED,
)

TARGETS=tuple('sc_nstd_'+suffix for suffix in (
    'extra','agree','consc','stability','open','gm','pp','s_aware',
    's_manage','soc_aware','realistic','invest','artistic','social','enterp','convent'))
LABELS=('<2.5','2.5-3.0','3.0-3.5','3.5-4.0','4.0-4.5','4.5-5.0','Not answered')


def ordinal_log_probs(logits):
    """Return six substantive log probabilities and separate nonresponse logp."""
    t, g=logits[..., :5], logits[..., 5:6]
    log_continue=F.logsigmoid(t)
    cumulative=log_continue.cumsum(dim=-1)
    prefix=torch.cat((torch.zeros_like(g), cumulative[..., :-1]), dim=-1)
    content=torch.cat((prefix+F.logsigmoid(-t), cumulative[..., -1:]), dim=-1)
    return torch.cat((F.logsigmoid(-g)+content, F.logsigmoid(g)), dim=-1)


def ordinal_indices(predict_items, records, options):
    """Reject any partial or altered WB16 contract before a model fit."""
    for item in TARGETS:
        rec=records.get(item)
        if (rec is None or rec.get('class')!='PREDICT' or rec.get('gate') is not None
                or tuple(rec.get('values',()))!=LABELS or tuple(options.get(item,()))!=LABELS
                or item not in predict_items):
            raise ValueError('WB16 ordinal schema contract mismatch: '+item)
    return tuple(i for i,item in enumerate(predict_items) if item in TARGETS)


class OrdinalHead(nn.Module):
    def __init__(self, nominal):
        super().__init__()
        if nominal.out_features!=7:
            raise ValueError('Ordinal head requires seven original classes')
        rows=[0,1,2,3,4,6]
        self.weight=nn.Parameter(nominal.weight.detach()[rows].clone())
        self.bias=nn.Parameter(nominal.bias.detach()[rows].clone())

    def forward(self, z):
        return ordinal_log_probs(F.linear(z,self.weight,self.bias))


class OrdinalNet(shared_trunk._Net):
    def __init__(self,d_in,full_dims,cond_dims,config,ordinal_map):
        # Construct all nominal parameters first, preserving every original draw.
        super().__init__(d_in,full_dims,cond_dims,config)
        for index in ordinal_map:
            self.full_heads[index]=OrdinalHead(self.full_heads[index])


def _train(X_fit, full_fit, cond_fit, X_val, full_val, cond_val,
           full_dims, cond_dims, max_epochs=MAX_EPOCHS,
           config=DEFAULT_CONFIG, ordinal_map=()):
    dev = _device()
    try:
        return _train_on(dev, X_fit, full_fit, cond_fit, X_val, full_val,
                         cond_val, full_dims, cond_dims, max_epochs, config,
                         ordinal_map)
    except Exception:
        if dev.type != 'cuda':
            raise
        return _train_on(torch.device('cpu'), X_fit, full_fit, cond_fit,
                         X_val, full_val, cond_val, full_dims, cond_dims,
                         max_epochs, config, ordinal_map)


def _train_on(dev, X_fit, full_fit, cond_fit, X_val, full_val, cond_val,
              full_dims, cond_dims, max_epochs, config, ordinal_map):
    torch.manual_seed(TORCH_SEED)
    net = OrdinalNet(X_fit.shape[1], full_dims, cond_dims, config, ordinal_map).to(dev)
    X_fit, full_fit, cond_fit = (X_fit.to(dev), full_fit.to(dev), cond_fit.to(dev))
    if X_val is not None:
        X_val, full_val, cond_val = (X_val.to(dev), full_val.to(dev), cond_val.to(dev))
    opt = torch.optim.Adam(net.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
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
            best_state = {k: v.clone() for k, v in net.state_dict().items()}
        elif epoch - best_epoch >= PATIENCE:
            break
    if best_state is not None:
        net.load_state_dict(best_state)
    net.eval()
    return net, (best_epoch if X_val is not None else max_epochs)


def tune_and_train(frame, schema, cols, kappas, configs=None, extra=None):
    """Original shared-trunk selection/refit; only the network factory differs."""
    records, items, options = _layout(frame, schema)
    predict_items = [n for n in items if records[n]['class'] == 'PREDICT']
    gated_items = [n for n in predict_items if records[n].get('gate')]
    full_dims = [len(options[n]) for n in predict_items]
    cond_dims = [len(records[n]['values']) for n in gated_items]
    gated_value = schema['gated_value']
    mapping = ordinal_indices(predict_items, records, options)
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
            X = torch.cat([X, torch.from_numpy(np.asarray(extra[pos], dtype=np.float32))], dim=1)
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
        cand_net, cand_epoch = _train(X_tr, f_tr, c_tr, X_va, f_va, c_va,
                                      full_dims, cond_dims, config=cand, ordinal_map=mapping)
        with torch.no_grad():
            dev = _net_device(cand_net)
            fl, cl = cand_net(X_ev.to(dev))
            ce = float(_pooled_ce(fl, cl, f_ev.to(dev), c_ev.to(dev)))
        if ce < best_ce:
            best_ce, net, best_epoch, config = ce, cand_net, cand_epoch, cand
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
        keys = list(map(tuple, eval_rows.loc[valid, cols].to_numpy())) if cols else [() for _ in codes_eval]
        ladder = np.stack([ladder_lookup(p0, levels, key) for key in keys])
        rows_idx = np.arange(len(codes_eval))
        cells += len(codes_eval)
        for w in W_GRID:
            mix = _floored(w * proba + (1.0 - w) * ladder)
            totals[w] += np.log(mix[rows_idx, codes_eval]).sum()
    if cells == 0:
        return 0.0, None, (predict_items, gated_items)
    w = max(totals, key=lambda x: totals[x] / cells)
    X_all_fit, f_all, c_all = prep(complete)
    final_net, _ = _train(X_all_fit, f_all, c_all, None, None, None,
                          full_dims, cond_dims, max_epochs=max(best_epoch, 1),
                          config=config, ordinal_map=mapping)
    return w, final_net, (predict_items, gated_items)


def predict(frame, schema, cols=None, kappas=None):
    items=schema['items']
    is_wb=('participant_id' in items and 'group' in items) or any(name in items for name in TARGETS)
    if not is_wb:
        return supervised_retrieval.predict(frame,schema,cols=cols,kappas=kappas)
    return link_sharp.predict(frame,schema,cols=cols,kappas=kappas,
                              layer_fn=hh_sharp_layer,configs=hh_cap.CONFIGS,
                              tune_fn=tune_and_train)
