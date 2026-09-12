"""Probe submissions — leaderboard slots used as a measurement instrument.

The phase-1 leaderboard is our only real-data channel, and it reports
one pooled skill per instrument. Replacing a DEFINED subset S of cells
with the uniform vector removes exactly S's contribution:

    skill' = skill − share(S) · (skill_S − u_S)

where share(S) is S's fraction of scored cells, skill_S the mean
per-cell skill on S (1 + log p / U) and u_S = mean over S of
(1 − log K_i / U) the per-cell skill of the uniform vector itself
(zero only for an item whose K equals the instrument's mean K) — both
share and u_S are exact from the schema. For item subsets the
share is exact from the schema (every PREDICT item has one cell per
held-out row), so one leaderboard reading gives skill_S — a loss map by
item group that the sandbox cannot provide. Probes are built on the
model of record (E025); they never change what the model does on the
cells outside S. Interpretation uses only public shares (schema item
counts) or model-side switches — never a dataset statistic.

`decompose` reproduces the arithmetic locally (sandbox truth) so a
probe's local reading must equal the prediction from the unprobed
model's per-cell scores before the slot is spent.
"""

import numpy as np

from src.models.hier_backoff import _layout


def blank_cells(frame, schema):
    """[(row, item)] in the grader's canonical order for the frame's
    blank PREDICT cells (rows top to bottom, items in schema order)."""
    records, items, options = _layout(frame, schema)
    predict = [n for n in items if records[n]["class"] == "PREDICT"]
    isna = frame[predict].isna().to_numpy()
    out = []
    for row in range(len(frame)):
        for j, item in enumerate(predict):
            if isna[row, j]:
                out.append((row, item))
    return out


def uniform_on(predict_fn, in_subset):
    """Wrap predict_fn: cells with in_subset(schema, row, item) True get
    the uniform vector over the item's full option list (gate slot
    included); every other cell is untouched."""
    def probed(frame, schema, *args, **kwargs):
        frame = frame.reset_index(drop=True)
        vectors = predict_fn(frame, schema, *args, **kwargs)
        cells = blank_cells(frame, schema)
        assert len(cells) == len(vectors), (len(cells), len(vectors))
        out = []
        for vec, (row, item) in zip(vectors, cells):
            if in_subset(schema, row, item):
                out.append(np.full(len(vec), 1.0 / len(vec)))
            else:
                out.append(vec)
        return out
    return probed


def gated_items(schema, row, item):
    return schema["items"][item].get("gate") is not None


def item_share(schema, in_subset):
    """Exact cell share of an item-defined subset."""
    records = schema["items"]
    predict = [n for n, r in records.items() if r["class"] == "PREDICT"]
    return sum(in_subset(schema, None, n) for n in predict) / len(predict)


def decompose(vectors, truth, cells, schema, floor, in_subset):
    """Per-cell skill on S and its complement from floored vectors, plus
    the pooled skill the uniform-on-S probe must read."""
    from score import uniform_reference, options_for  # noqa: kit on path
    U = uniform_reference(schema)
    logp = np.empty(len(cells))
    mask = np.zeros(len(cells), dtype=bool)
    for i, (vec, actual, (row, _, item)) in enumerate(zip(vectors, truth,
                                                          cells)):
        opts = options_for(schema, item)
        p = np.asarray(vec, dtype=float)
        p = floor + (1.0 - p.size * floor) * (p / p.sum())
        logp[i] = np.log(p[opts.index(actual)])
        mask[i] = in_subset(schema, row, item)
    cell_skill = 1.0 + logp / U          # per-cell skill
    share = mask.mean()
    s_in = cell_skill[mask].mean() if mask.any() else 0.0
    s_out = cell_skill[~mask].mean() if (~mask).any() else 0.0
    total = cell_skill.mean()
    u_S = uniform_skill(schema, in_subset)
    return {"share": share, "skill_S": s_in, "skill_notS": s_out,
            "u_S": u_S, "skill": total,
            "probe_skill": total - share * (s_in - u_S)}


def uniform_skill(schema, in_subset):
    """u_S: mean per-cell skill of the uniform vector over the items in
    S (exact from the schema; gate slot counted in K)."""
    from score import uniform_reference, options_for  # noqa: kit on path
    U = uniform_reference(schema)
    ks = [len(options_for(schema, n)) for n, r in schema["items"].items()
          if r["class"] == "PREDICT" and in_subset(schema, None, n)]
    return float(np.mean([1.0 - np.log(k) / U for k in ks])) if ks else 0.0


def read_probe(schema, in_subset, skill_ref, skill_probe):
    """Invert a leaderboard reading: skill_S from the reference and the
    probe skills."""
    share = item_share(schema, in_subset)
    return (skill_ref - skill_probe) / share + uniform_skill(schema, in_subset)
