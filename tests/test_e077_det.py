"""E077 `det` chain part: routing exclusions on gated heads read off the labelled rows
(fabricated data only).

Usage: E077_BUILD=<build dir> python tmp/e077_selftest.py   (the model venv has no pytest)
"""
import importlib.util
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = os.environ.get("E077_BUILD")
SCHEMA = {
    "gated_value": "NA_GATED",
    "items": {
        "a": {"class": "GIVEN", "values": ["0", "1", "2"], "gate": None},
        "b": {"class": "GIVEN", "values": ["0", "1", "2", "3"], "gate": None},
        "y1": {"class": "PREDICT", "values": ["u", "v", "w"], "gate": None},
        "y2": {"class": "PREDICT", "values": ["0", "1"], "gate": {"parent": "y1", "observed_if": ["u"]}},
    },
}


def load():
    sys.path.insert(0, BUILD)
    spec = importlib.util.spec_from_file_location("e077_main", Path(BUILD) / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def frame(rows=4200, held_share=0.15, structure=True, seed=0):
    """y2 is asked only after y1 == "u". With structure, y1 is never "u" when a == "0" (y2 never
    asked), always "u" when a == "1" (y2 always asked) and never "u" when (a, b) == ("2", "3").
    Held rows are scattered through the table, not appended at its end."""
    rng = np.random.default_rng(seed)
    a = rng.integers(3, size=rows).astype(str)
    b = rng.integers(4, size=rows).astype(str)
    y1 = rng.choice(["u", "v", "w"], size=rows).astype(object)
    if structure:
        never = (a == "0") | ((a == "2") & (b == "3"))
        y1[never] = rng.choice(["v", "w"], size=int(never.sum()))
        y1[a == "1"] = "u"
    y2 = np.where(y1 == "u", rng.integers(2, size=rows).astype(str), "NA_GATED").astype(object)
    held = rng.random(rows) < held_share
    truth = {"y1": y1[held].copy(), "y2": y2[held].copy()}
    y1[held] = None
    y2[held] = None
    return pd.DataFrame({"a": a, "b": b, "y1": y1, "y2": y2}), truth


def _setup(m, f):
    given, heads, options = m._layout(SCHEMA)
    visible, held = m._roles(f, heads)
    rng = np.random.default_rng(1)
    maps = {n: rng.dirichlet(np.ones(len(options[n])) * 4.0, size=len(held)) for n in heads}
    return heads, options, visible, held, maps


def test_det_moves_the_gate_value_inside_its_bounds(m):
    m._DET_CACHE.clear()
    f, truth = frame()
    heads, options, visible, held, maps = _setup(m, f)
    out = m._det_apply(f, SCHEMA, maps, heads, options)
    assert out["y1"] is maps["y1"]                             # ungated heads are never touched
    a, b = f["a"].to_numpy()[held], f["b"].to_numpy()[held]
    va = f["a"].to_numpy()[visible]
    p, q = maps["y2"], out["y2"]
    assert np.allclose(q.sum(axis=1), 1.0) and (q >= 0).all()
    never = a == "0"
    n0 = int((va == "0").sum())
    assert never.sum() > 100 and np.allclose(q[never, 2], np.maximum(p[never, 2], 1.0 - 3.0 / (n0 + 2)))
    assert np.allclose(q[never, 0] / q[never, 1], p[never, 0] / p[never, 1])   # asked answers keep their ratio
    always = a == "1"
    n1 = int((va == "1").sum())
    assert always.sum() > 100 and np.allclose(q[always, 2], np.minimum(p[always, 2], 3.0 / (n1 + 2)))
    assert np.allclose(q[always, 0] / q[always, 1], p[always, 0] / p[always, 1])
    pair = (a == "2") & (b == "3")
    assert pair.sum() > 20 and (q[pair, 2] > 0.98).all()
    rest = (a == "2") & (b != "3")
    assert np.array_equal(q[rest], p[rest])                    # bit for bit outside the bounded strata
    code = {v: i for i, v in enumerate(options["y2"])}
    y = np.array([code[v] for v in truth["y2"]])
    rows = np.arange(len(held))
    assert np.log(q[rows, y]).mean() > np.log(p[rows, y]).mean() + 0.3


def test_det_is_inert_without_structure_and_ignores_small_strata(m):
    m._DET_CACHE.clear()
    f, _ = frame(structure=False)
    heads, options, visible, held, maps = _setup(m, f)
    out = m._det_apply(f, SCHEMA, maps, heads, options)
    assert all(out[n] is maps[n] for n in heads)               # same objects: an inert chain scores the same
    m._DET_CACHE.clear()
    small, _ = frame(rows=900)                                 # the (a, b) strata hold about 64 labelled rows
    heads, options, visible, held, maps = _setup(m, small)
    out = m._det_apply(small, SCHEMA, maps, heads, options)
    a, b = small["a"].to_numpy()[held], small["b"].to_numpy()[held]
    pair = (a == "2") & (b == "3")
    assert pair.sum() > 3 and np.array_equal(out["y2"][pair], maps["y2"][pair])
    assert (out["y2"][a == "0", 2] > 0.98).all()               # the single-field stratum is still large enough


def test_det_runs_as_a_chain_part_and_caches_its_bounds(m):
    m._DET_CACHE.clear()
    f, _ = frame()
    heads, options, visible, held, maps = _setup(m, f)
    direct = m._det_apply(f, SCHEMA, maps, heads, options)
    m._DET_CACHE.clear()
    chained = m._apply("det", f, SCHEMA, maps, {}, heads, options)
    assert all(np.array_equal(direct[n], chained[n]) for n in heads)
    assert m._needs_expert("xlpool+det") == set(m.XSTACK_KINDS) and m._needs_expert("det") == set()
    assert not m._is_fitted("det") and m._is_fitted("cal+det")
    m._DET_CACHE.clear()
    bounds = m._det_bounds(f, SCHEMA, heads, options)
    assert m._det_bounds(f, SCHEMA, heads, options) is bounds and set(bounds) == {"y2"}
    lower, upper = bounds["y2"]
    assert lower.shape == (len(held),) and upper.shape == (len(held),) and (lower <= upper).all()
