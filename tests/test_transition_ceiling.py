"""E035 — recorded null: evidence transition tables (H2) ceiling.

Structured-disagreement household sim: when a twin does not copy an
answer it maps to a fixed item-specific alternative with prob s. The
oracle per-item transition T (from the KNOWN sim pairs, both directions)
replaces the one-hot evidence (ev -> ev @ T) inside the E025 layer.
Measured 2026-09-16: s = 0.7 -> +0.0032 log over E025; s = 0 -> -0.0013.
The gain assertion is kept as a strict xfail (the recorded null)."""

import numpy as np
import pandas as pd
import pytest

from src.models import hier_backoff, link_sharp, hh_sharp
from src.models.hh_cap import CONFIGS
from tests.test_soft_gating import KIT, load
from tests.test_hh_link import ROSTER_PREFIXES

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def inject_structured(frame, schema, frac, seed, lo, hi, s_struct):
    """hh_inject_rho with structured disagreement: a non-copied twin
    answer maps to one fixed other value of the item with prob s_struct,
    else to a random value. `_src` holds the original respondent_id."""
    rng = np.random.default_rng(seed)
    records = schema["items"]
    gv = schema["gated_value"]
    given = [n for n, r in records.items()
             if r["class"] == "GIVEN" and n != "wave"]
    roster = [n for n in given if n.startswith(ROSTER_PREFIXES)]
    person = [n for n in given if n not in roster]
    base = frame.copy()
    take = base[base["wave"] == "1"].sample(frac=frac, random_state=seed)
    twins = take.copy()
    twins["respondent_id"] = ["hh_%d" % i for i in range(len(twins))]
    twins["role"] = rng.choice(["TRAIN", "DEV"], size=len(twins),
                               p=[0.8, 0.2])
    twins["_src"] = take["respondent_id"].to_numpy()
    for col in person:
        vals = list(records[col]["values"])
        twins[col] = [vals[rng.integers(len(vals))]
                      for _ in range(len(twins))]
    for item, r in records.items():
        if r["class"] != "PREDICT" or item not in twins.columns:
            continue
        rho = rng.uniform(lo, hi)
        vals = list(r["values"])
        if len(vals) < 2:
            perm = {v: v for v in vals}
        else:
            perm = {v: vals[(i + 1 + rng.integers(len(vals) - 1)) % len(vals)]
                    for i, v in enumerate(vals)}
        cur = twins[item].to_numpy(dtype=object)
        keep = rng.random(len(twins)) < rho
        for i in np.flatnonzero(~keep):
            if pd.isna(cur[i]) or cur[i] == gv:
                continue
            cur[i] = (perm[cur[i]] if rng.random() < s_struct
                      else vals[rng.integers(len(vals))])
        twins[item] = cur
    base["_src"] = None
    return pd.concat([base, twins], ignore_index=True)


def true_transition(merged, src_id, records, items, options):
    """Per-item T[candidate value -> query value] from visible known
    pairs (both directions), Laplace-smoothed."""
    predict = [n for n in items if records[n]["class"] == "PREDICT"]
    vis = ~merged[predict].isna().any(axis=1).to_numpy()
    pos = {rid: i for i, rid in enumerate(merged["respondent_id"])}
    pairs = [(i, pos[s]) for i, s in enumerate(src_id)
             if s is not None and s in pos and vis[i] and vis[pos[s]]]
    T = {}
    for item in predict:
        opts = options[item]
        idx = {o: k for k, o in enumerate(opts)}
        M = np.ones((len(opts), len(opts)))
        vals = merged[item].to_numpy(dtype=object)
        for a, b in pairs:
            for x, y in ((a, b), (b, a)):
                if vals[x] in idx and vals[y] in idx:
                    M[idx[vals[x]], idx[vals[y]]] += 1
        T[item] = M / M.sum(1, keepdims=True)
    return T, len(pairs)


def layer_with_transition(T):
    """E022 layer with evidence post-multiplied by T (oracle H2)."""
    def layer(frame, schema, model_dists):
        orig = hh_sharp._evidence

        def ev_T(frame_, items, records, options, posteriors, query_pos):
            ev = orig(frame_, items, records, options, posteriors,
                      query_pos)
            return {it: (m @ T[it]) if it in T else m
                    for it, m in ev.items()}
        hh_sharp._evidence = ev_T
        try:
            return hh_sharp.hh_sharp_layer(frame, schema, model_dists)
        finally:
            hh_sharp._evidence = orig
    return layer


def _ceiling(s_struct):
    frame, schema = load("unhcr")
    config = load_config(str(KIT / "config.yml"))
    sim = inject_structured(frame, schema, 0.3, 13, 0.2, 0.8, s_struct)
    src_of = dict(zip(sim["respondent_id"], sim["_src"]))
    merged, cells, truth = sample_rows(schema, sim.drop(columns="_src"), 1)
    src_id = [src_of[r] for r in merged["respondent_id"]]
    records, items, options = hier_backoff._layout(merged, schema)
    T, _ = true_transition(merged, src_id, records, items, options)
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)
    out = {}
    for name, layer in (("E025", hh_sharp.hh_sharp_layer),
                        ("T", layer_with_transition(T))):
        v = link_sharp.predict(merged, schema, cols=cols, kappas=kappas,
                               layer_fn=layer, configs=CONFIGS)
        v = floored(v, schema, cells, config["scoring"]["floor"])
        out[name] = grade(schema, config, v, truth, cells)["log_score"]
    delta = out["T"] - out["E025"]
    print(f"\nstructured sim s={s_struct}: E025 {out['E025']:.4f} "
          f"oracle-T {delta:+.4f}")
    return delta


@pytest.mark.xfail(strict=True, reason="E035 recorded null: oracle "
                   "transition tables +0.0032 at s=0.7 (bar +0.005)")
def test_oracle_transition_clears_bar_on_structured_sim():
    assert _ceiling(0.7) > 0.005
