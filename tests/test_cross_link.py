"""E013 tests: linkage detector correctness; inertness on the clean
sandbox (independent rows -> no twins); large gain on a synthetic panel
sim where round-2 rows are perturbed copies of round-1 rows."""

import numpy as np
import pandas as pd
import pytest

from src.models import cross_link, hier_backoff, shared_trunk
from tests.test_soft_gating import KIT, load

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def toy():
    frame = pd.DataFrame({
        "wave": ["1", "2", "1", "2", "1", "2", "2"],
        "g1":   ["a", "a", "b", "b", "c", "c", "c"],
        "g2":   ["x", "x", "y", "y", "z", "z", "z"],
        "p1":   ["u", "v", np.nan, "v", "u", "u", "v"],
    })
    records = {
        "wave": {"class": "GIVEN", "values": ["1", "2"]},
        "g1": {"class": "GIVEN", "values": ["a", "b", "c"]},
        "g2": {"class": "GIVEN", "values": ["x", "y", "z"]},
        "p1": {"class": "PREDICT", "values": ["u", "v"]},
    }
    return frame, records, list(records)


def test_build_links_unit():
    frame, records, items = toy()
    twin_of, vis_pairs = cross_link.build_links(frame, records, items,
                                                "wave")
    # rows 0-1: both visible, cross-round, unique -> vis pair
    assert (0, 1) in vis_pairs or (1, 0) in vis_pairs
    # rows 2-3: row 2 held out, unique cross-round -> twin
    assert twin_of.get(2) == 3
    # rows 4-5-6: signature collision (3 rows) -> rejected entirely
    assert 4 not in twin_of and 5 not in twin_of and 6 not in twin_of
    assert all(a not in (4, 5, 6) and b not in (4, 5, 6)
               for a, b in vis_pairs)


def test_stability_shrinks(monkeypatch):
    monkeypatch.setattr(cross_link, "MIN_PAIRS", 1)
    frame, records, items = toy()
    stab = cross_link.stability(frame, records, items, [(0, 1), (4, 5)])
    # pairs disagree once (u!=v) and agree once (u==u): raw 0.5,
    # shrunk to the median (0.5) stays 0.5
    assert stab["p1"] == pytest.approx(0.5, abs=1e-9)


def test_clean_unhcr_inert():
    """Independent sandbox rows: the 72-column signature never repeats
    1:1 across rounds -> no twins, no stability set, layer off."""
    frame, schema = load("unhcr")
    merged, _, _ = sample_rows(schema, frame, 1)
    records = schema["items"]
    items = [n for n, r in records.items()
             if r["class"] in ("GIVEN", "PREDICT")]
    round_col = cross_link.find_round_col(records, items)
    assert round_col is not None
    twin_of, vis_pairs = cross_link.build_links(merged, records, items,
                                                round_col)
    # a handful of signature collisions can slip through on independent
    # rows (observed: 1); the MIN_PAIRS guard must keep the layer off
    assert len(twin_of) < 5
    assert len(vis_pairs) < cross_link.MIN_PAIRS
    assert cross_link.stability(merged, records, items, vis_pairs) == {}


def test_no_round_col_is_inert():
    frame, schema = load("sample")
    records = schema["items"]
    items = [n for n, r in records.items()
             if r["class"] in ("GIVEN", "PREDICT")]
    assert cross_link.find_round_col(records, items) is None


def panel_sim(frame, schema, link_frac, perturb, seed,
              given_perturb=0.3, drift_lambda=None):
    """Round-2 rows replaced by perturbed copies of sampled round-1
    rows; twin roles drawn TRAIN(0.8)/DEV(0.2) so pairs straddle the
    visible/held-out boundary. `given_perturb` of twins get ONE GIVEN
    column changed — real panel drift; only the fuzzy matcher finds
    these."""
    rng = np.random.default_rng(seed)
    records = schema["items"]
    gated_value = schema["gated_value"]
    r1 = frame[frame["wave"] == "1"].copy()
    take = r1.sample(frac=link_frac, random_state=seed)
    twins = take.copy()
    twins["wave"] = "2"
    twins["respondent_id"] = ["twin_%d" % i for i in range(len(twins))]
    twins["role"] = rng.choice(["TRAIN", "DEV"], size=len(twins),
                               p=[0.8, 0.2])
    given_cols = [n for n, r in records.items()
                  if r["class"] == "GIVEN" and n != "wave"
                  and n in twins.columns]
    if drift_lambda is None:
        n_drift = (rng.random(len(twins)) < given_perturb).astype(int)
    else:
        n_drift = rng.poisson(drift_lambda, len(twins))
    for i in np.flatnonzero(n_drift):
        picks = rng.choice(len(given_cols),
                           size=min(n_drift[i], len(given_cols)),
                           replace=False)
        for p in picks:
            col = given_cols[p]
            vals = list(records[col]["values"])
            twins.iloc[i, twins.columns.get_loc(col)] = \
                vals[rng.integers(len(vals))]
    for item, r in records.items():
        if r["class"] != "PREDICT" or item not in twins.columns:
            continue
        values = list(r["values"])
        flip = rng.random(len(twins)) < perturb
        cur = twins[item].to_numpy(dtype=object)
        for i in np.flatnonzero(flip):
            if pd.isna(cur[i]) or cur[i] == gated_value:
                continue
            cur[i] = values[rng.integers(len(values))]
        twins[item] = cur
    return pd.concat([r1, twins], ignore_index=True)


def test_panel_sim_gain_unhcr():
    frame, schema = load("unhcr")
    sim = panel_sim(frame, schema, link_frac=0.6, perturb=0.1, seed=3)
    config = load_config(str(KIT / "config.yml"))
    merged, cells, truth = sample_rows(schema, sim, 1)

    records = schema["items"]
    items = [n for n, r in records.items()
             if r["class"] in ("GIVEN", "PREDICT")]
    twin_of, vis_pairs = cross_link.build_links(
        merged, records, items, "wave")
    assert len(vis_pairs) > 100 and len(twin_of) > 50

    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)

    def scored(model):
        vectors = model.predict(merged, schema, cols=cols, kappas=kappas)
        vectors = floored(vectors, schema, cells,
                          config["scoring"]["floor"])
        return grade(schema, config, vectors, truth, cells)["log_score"]

    e012 = scored(shared_trunk)
    e013 = scored(cross_link)
    print(f"\npanel sim unhcr (twins={len(twin_of)} heldout, "
          f"{len(vis_pairs)} visible pairs): E012 {e012:.4f} "
          f"E013 {e013:.4f} delta {e013 - e012:+.4f}")
    assert e013 > e012 + 0.05, (e012, e013)
