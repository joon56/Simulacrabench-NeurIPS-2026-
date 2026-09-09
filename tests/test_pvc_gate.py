"""E028 tests: exact gates reproduce E025 (clean); a branch-overlap sim
(round-2 No-respondents answering Yes-branch children from a skewed
distribution) is captured by parent-value-conditional decoding."""

import numpy as np
import pandas as pd
import pytest

from src.models import hh_cap, hier_backoff, pvc_gate
from tests.test_soft_gating import KIT, load

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402

PARENT = "s3_11_intent_return_12m_lbl"


def overlap_inject(frame, schema, frac, seed,
                   parents=("0. No", "98. I don't know"),
                   waves=("1", "2")):
    """Respondents with parent in `parents` (and wave in `waves`) answer
    the Yes-branch children with probability `frac`, drawing from a
    skewed distribution (weights 0.6**k over the child's values). The
    default is the HEAVY regime: schema-documented agreement ranges
    down to 0.29, so a 30%-of-round-2-No light regime (which gave
    +0.0017) under-represents the real overlap."""
    rng = np.random.default_rng(seed)
    records = schema["items"]
    gated_value = schema["gated_value"]
    out = frame.copy()
    yes_children = [n for n, r in records.items()
                    if r["class"] == "PREDICT" and r.get("gate")
                    and r["gate"]["parent"] == PARENT
                    and r["gate"]["observed_if"] == ["1. Yes"]]
    target = out[PARENT].isin(parents) & out["wave"].isin(waves)
    idx = out.index[target]
    for item in yes_children:
        vals = list(records[item]["values"])
        wts = 0.6 ** np.arange(len(vals))
        wts /= wts.sum()
        hit = idx[rng.random(len(idx)) < frac]
        draws = rng.choice(len(vals), size=len(hit), p=wts)
        cur = out[item].to_numpy(dtype=object)
        pos = out.index.get_indexer(hit)
        for p, d in zip(pos, draws):
            if cur[p] == gated_value:
                cur[p] = vals[d]
        out[item] = cur
    return out, yes_children


def test_pvc_tables_exact_gates():
    frame, schema = load("unhcr")
    merged, _, _ = sample_rows(schema, frame, 1)
    merged = merged.reset_index(drop=True)
    records, items, options = hier_backoff._layout(merged, schema)
    complete = hier_backoff._complete_rows(merged, items)
    pvc = pvc_gate.build_pvc(merged, schema, complete, {})
    parent, cvals, per_v, _ = pvc[next(
        n for n in pvc if pvc[n][0] == PARENT)]
    # exact sandbox gates: asked value ~0 sentinel, others ~1
    for v, (r_v, _, A_v) in per_v.items():
        if v == "1. Yes":
            assert r_v < 0.02 and A_v is None
        else:
            assert r_v > 0.98 and A_v is not None


def test_overlap_sim_gain():
    frame, schema = load("unhcr")
    sim, yes_children = overlap_inject(frame, schema, frac=0.7, seed=23)
    assert len(yes_children) > 10
    merged, cells, truth = sample_rows(schema, sim, 1)
    config = load_config(str(KIT / "config.yml"))
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)

    def scored(model):
        v = model.predict(merged, schema, cols=cols, kappas=kappas)
        v = floored(v, schema, cells, config["scoring"]["floor"])
        return grade(schema, config, v, truth, cells)["log_score"]

    e025 = scored(hh_cap)
    e028 = scored(pvc_gate)
    print(f"\nbranch-overlap sim: E025 {e025:.4f} E028 {e028:.4f} "
          f"delta {e028 - e025:+.4f}")
    assert e028 > e025 + 0.005, (e025, e028)
