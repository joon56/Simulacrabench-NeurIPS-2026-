"""E068: E041 plus data-checked re-gating of the s3_11 return branches (UNHCR).

The UNHCR schema (kit 30dd72d, 2026-10-25) states that the return branch (s7a) and the
do-not-return branch (s7b) "follow s3_12 more closely than s3_11", while the schema
gates them on s3_11. E041 couples their skip probability to s3_11. Here, per branch
family and survey wave, the visible rows decide: if s3_12 explains who was skipped
clearly better than s3_11 (smoothed per-value skip rates, log-likelihood), the
sentinel mass of each held-out cell is re-estimated as sum_v P(s3_12 = v) * rate_v,
using E041's own predicted s3_12 distribution for that respondent; content mass keeps
E041's proportions. Otherwise the cell is unchanged. The E066 wave-coded transfer is
applied afterwards for (item, wave) cells with no visible sentinel. e041_core.py is a
byte copy of submissions/2026-09-19-E041/main.py.
"""
import os

import numpy as np

import e041_core

UNHCR_MARKER = "s3_11_intent_return_12m_lbl"
PARENT_OLD = "s3_11_intent_return_12m_lbl"
PARENT_NEW = "s3_12_hope_return_someday_lbl"
BRANCHES = ("s7a_", "s7b_", "s7c_")
MIN_WAVE_ROWS = 300
SMOOTH = 20.0
LL_MARGIN = 0.01
FAMILIES = ("s6_4_", "s6_6_", "s6_11_", "s7a_7_", "s7b_1_")
LAST = {}


def _options(items, gated, name):
    return list(items[name]["values"]) + ([gated] if items[name].get("gate") else [])


def _rates(parent_values, skip, levels):
    """Smoothed per-parent-value skip rate pooled over children, and its log-likelihood."""
    overall = skip.mean()
    rates, ll = {}, 0.0
    for level in levels:
        sel = parent_values == level
        n = int(sel.sum()) * skip.shape[1]
        k = float(skip[sel].sum())
        r = (k + SMOOTH * overall) / (n + SMOOTH)
        r = min(max(r, 1e-6), 1 - 1e-6)
        rates[level] = r
        ll += k * np.log(r) + (n - k) * np.log(1 - r)
    return rates, ll


def regate(frame, schema, vectors, force=False):
    items = schema["items"]
    gated = schema["gated_value"]
    heads = [n for n, r in items.items() if r["class"] == "PREDICT"]
    if PARENT_NEW not in heads or PARENT_OLD not in heads or "wave" not in frame:
        return vectors
    block = frame[heads]
    held = block.isna().all(axis=1).to_numpy().nonzero()[0]
    visible = block.notna().all(axis=1).to_numpy().nonzero()[0]
    width = len(heads)
    if len(held) + len(visible) != len(frame) or len(vectors) != len(held) * width:
        return vectors
    waves_all = frame["wave"].astype(str).to_numpy()
    vis = frame.iloc[visible]
    vis_wave = waves_all[visible]
    new_levels = _options(items, gated, PARENT_NEW)
    old_levels = _options(items, gated, PARENT_OLD)
    j_new = heads.index(PARENT_NEW)
    belief = np.array([vectors[i * width + j_new] for i in range(len(held))], dtype=np.float64)
    belief = belief / belief.sum(axis=1, keepdims=True)
    out = None
    LAST.clear()
    for branch in BRANCHES:
        children = [n for n in heads if n.startswith(branch) and items[n].get("gate")
                    and items[n]["gate"]["parent"] == PARENT_OLD]
        for wave in ("1", "2"):
            in_w = vis_wave == wave
            if int(in_w.sum()) < MIN_WAVE_ROWS:
                continue
            active = [c for c in children if (vis[c].to_numpy()[in_w] == gated).any()]
            if not active:
                continue
            skip = np.stack([(vis[c].to_numpy()[in_w] == gated) for c in active], axis=1).astype(float)
            rates_new, ll_new = _rates(vis[PARENT_NEW].to_numpy()[in_w], skip, new_levels)
            _, ll_old = _rates(vis[PARENT_OLD].to_numpy()[in_w], skip, old_levels)
            switch = bool(force or ll_new > ll_old + LL_MARGIN * abs(ll_old))
            LAST[(branch, wave)] = dict(children=len(active), ll_new=float(ll_new), ll_old=float(ll_old),
                                        switch=switch)
            if not switch:
                continue
            r = np.array([rates_new[level] for level in new_levels])
            if out is None:
                out = [list(v) for v in vectors]
            rows = [i for i, row in enumerate(held) if waves_all[row] == wave]
            for c in active:
                j = heads.index(c)
                for i in rows:
                    v = np.asarray(out[i * width + j], dtype=np.float64)
                    v = v / v.sum()
                    content = v[:-1]
                    total = content.sum()
                    content = content / total if total > 0 else np.full(len(content), 1.0 / len(content))
                    s_new = float(belief[i] @ r)
                    out[i * width + j] = list(np.append((1.0 - s_new) * content, s_new))
    return vectors if out is None else out


def flagged_cells(frame, schema, heads, visible):
    """E066: (item, wave) cells where the visible rows show the round-specific coding."""
    items = schema["items"]
    gated = schema["gated_value"]
    wave = frame["wave"].astype(str).iloc[visible]
    flags = set()
    for name in heads:
        rec = items[name]
        if not name.startswith(FAMILIES) or not rec.get("gate") or "0" not in rec["values"]:
            continue
        values = frame[name].iloc[visible]
        for this, other in (("1", "2"), ("2", "1")):
            in_this = wave == this
            if int(in_this.sum()) < MIN_WAVE_ROWS:
                continue
            sentinel_this = int(((values == gated) & in_this).sum())
            sentinel_other = int(((values == gated) & (wave == other)).sum())
            if sentinel_this == 0 and sentinel_other > 0:
                flags.add((name, this))
    return flags


def transfer(frame, schema, vectors):
    """E066: move wave-coded sentinel mass to "0" where the visible rows confirm the coding."""
    items = schema["items"]
    heads = [n for n, r in items.items() if r["class"] == "PREDICT"]
    block = frame[heads]
    held = block.isna().all(axis=1).to_numpy().nonzero()[0]
    visible = block.notna().all(axis=1).to_numpy().nonzero()[0]
    if len(held) + len(visible) != len(frame) or len(vectors) != len(held) * len(heads):
        return vectors
    flags = flagged_cells(frame, schema, heads, visible)
    if not flags:
        return vectors
    out = [list(v) for v in vectors]
    waves = frame["wave"].astype(str).to_numpy()
    width = len(heads)
    for j, name in enumerate(heads):
        for this in ("1", "2"):
            if (name, this) not in flags:
                continue
            zero = items[name]["values"].index("0")
            sentinel = len(items[name]["values"])
            for i, row in enumerate(held):
                if waves[row] == this:
                    vector = out[i * width + j]
                    vector[zero] += vector[sentinel]
                    vector[sentinel] = 0.0
    return out


def predict(frame, schema):
    vectors = e041_core.predict(frame, schema)
    items = schema["items"]
    if UNHCR_MARKER not in items or "wave" not in items or "wave" not in frame:
        return vectors
    vectors = regate(frame, schema, vectors, force=bool(os.environ.get("E068_FORCE")))
    return transfer(frame, schema, vectors)
