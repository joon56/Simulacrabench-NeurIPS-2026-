"""E066: E041 plus wave-coded sentinel transfer for five UNHCR multi-select families.

The UNHCR schema documents that in families 6.4, 6.6, 6.11, 7A.7 and 7B.1 round 1
wrote "0" for respondents the routing skipped, so the gate sentinel appears on
round-2 rows only. For held-out rows of such a (item, wave) cell, E041's sentinel
mass is moved to "0". The rule is re-checked on the delivered visible rows at run
time: a cell is changed only if that wave has >= 300 visible rows, none of them
carries the sentinel, and the other wave does. Everything else is E041 unchanged
(e041_core.py is a byte copy of submissions/2026-09-19-E041/main.py).
"""
import e041_core

FAMILIES = ("s6_4_", "s6_6_", "s6_11_", "s7a_7_", "s7b_1_")
MIN_ROWS = 300
UNHCR_MARKER = "s3_11_intent_return_12m_lbl"


def flagged_cells(frame, schema, heads, visible):
    """(item, wave) cells where the visible rows show the round-specific coding."""
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
            if int(in_this.sum()) < MIN_ROWS:
                continue
            sentinel_this = int(((values == gated) & in_this).sum())
            sentinel_other = int(((values == gated) & (wave == other)).sum())
            if sentinel_this == 0 and sentinel_other > 0:
                flags.add((name, this))
    return flags


def transfer(frame, schema, vectors):
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
    return transfer(frame, schema, vectors)
