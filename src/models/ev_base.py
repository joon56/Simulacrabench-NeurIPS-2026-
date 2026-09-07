"""E024 — evidence-input net as the BASE inside E022's mixture layer.

E020 put posterior-weighted co-respondent answers into the net and
replaced the mixture; on the copy sim the mixture won. Here both are
kept: the net gets the evidence block (built with the household-aware
weights, self excluded for visible rows) as extra input so it can learn
cross-item household structure the per-item mixture cannot express
(a co-respondent's answer to A informing B), and E022's replay-
calibrated λ layer still mixes the direct per-item evidence on top.
If the net ignores its extra inputs the model is E022; overfitting is
bounded by the inner early-stopping split, which sees evidence built
identically.
"""

import numpy as np

from src.models.hier_backoff import _layout
from src.models.prob_link import _evidence
from src.models.dup_link import _sig_data_all, _topk_excl
from src.models.hh_link import estimate_weights
from src.models import link_sharp
from src.models.hh_sharp import hh_sharp_layer


def household_evidence_block(frame, schema):
    """[len(frame), sum K_i] evidence under learned household weights."""
    records, items, options = _layout(frame, schema)
    predict_items = [n for n in items if records[n]["class"] == "PREDICT"]
    width = sum(len(options[n]) for n in predict_items)
    block = np.zeros((len(frame), width), dtype=np.float32)
    codes, rarity_w = _sig_data_all(frame, records, items)
    if codes is None:
        return block
    heldout = frame[predict_items].isna().any(axis=1).to_numpy()
    vis_pos = np.flatnonzero(~heldout)
    if len(vis_pos) < 2:
        return block
    post0 = _topk_excl(codes, rarity_w, vis_pos, vis_pos)
    weights, _ = estimate_weights(codes, rarity_w, vis_pos, post0)
    all_pos = np.arange(len(frame))
    post = _topk_excl(codes, weights, all_pos, vis_pos)
    ev = _evidence(frame, items, records, options, post, all_pos)
    off = 0
    for item in predict_items:
        k = len(options[item])
        block[:, off:off + k] = ev[item]
        off += k
    return block


def predict(frame, schema, cols=None, kappas=None):
    return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                              layer_fn=hh_sharp_layer,
                              extra_fn=household_evidence_block)
