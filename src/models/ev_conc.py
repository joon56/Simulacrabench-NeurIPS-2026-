"""E027 — concentrated-row evidence as net input, stacked on E025.

E024 fed the posterior-weighted co-respondent answers of EVERY row into
the shared-trunk net and paid ~0.001 skill per instrument on
duplicate-free data (noise feature). Here only rows whose top candidate
holds max posterior weight >= CONC_SPLIT — the bucket the mixture layer
already trusts — carry the block; all other rows get zeros, so the
extra inputs are inert wherever there is no household match. The
E022 mixture layer and E025's architecture selection are unchanged.
"""

import numpy as np

from src.models.hier_backoff import _layout
from src.models.prob_link import _evidence
from src.models.dup_link import _sig_data_all, _topk_excl
from src.models.hh_link import estimate_weights
from src.models.link_sharp import CONC_SPLIT, _max_q
from src.models import link_sharp
from src.models.hh_sharp import hh_sharp_layer
from src.models.hh_cap import CONFIGS


def concentrated_evidence_block(frame, schema):
    """[len(frame), sum K_i]: evidence under learned household weights
    for rows with a concentrated posterior, zeros elsewhere."""
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
    conc = _max_q(post) >= CONC_SPLIT
    if not conc.any():
        return block
    ev = _evidence(frame, items, records, options, post, all_pos)
    off = 0
    for item in predict_items:
        k = len(options[item])
        block[conc, off:off + k] = ev[item][conc]
        off += k
    return block


def predict(frame, schema, cols=None, kappas=None):
    return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                              layer_fn=hh_sharp_layer,
                              extra_fn=concentrated_evidence_block,
                              configs=CONFIGS)
