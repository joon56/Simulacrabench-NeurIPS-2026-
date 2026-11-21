"""E075 expert r: neighbour trees fed by E041's supervised section retrieval (fabricated data only).

Usage: E075_BUILD=<build dir> python tmp/e075_selftest.py   (the model venv has no pytest)
"""
import importlib.util
import os
import sys
from pathlib import Path

import numpy as np

BUILD = os.environ.get("E075_BUILD")
_spec = importlib.util.spec_from_file_location("test_e074_base", Path(__file__).with_name("test_e074_twin.py"))
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)


def load():
    sys.path.insert(0, BUILD)
    spec = importlib.util.spec_from_file_location("e075_main", Path(BUILD) / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _mean_log(maps, y, heads, rows):
    return float(np.mean([np.log(maps[n][rows, y[n][rows]]) for n in heads]))


def test_retrieval_features_shapes_and_no_query_labels(m):
    f, truth, kind = base.frame()
    given, heads, options = m._layout(base.SCHEMA)
    visible, held = m._roles(f, heads)
    r = m._retrieval_features(f, base.SCHEMA, heads, options, visible, held)
    for n in heads:
        width = len(options[n])
        assert r["c"][n].shape == (len(visible), 2 * width + 6) and r["q"][n].shape == (len(held), 2 * width + 6)
        assert np.isfinite(r["c"][n]).all() and np.isfinite(r["q"][n]).all()
        assert np.allclose(r["q"][n][:, :width].sum(axis=1), 1.0) and len(r["cat"][n]) == 2 * width + 6
        assert r["cat"][n][-3:] == [True] * 3 and not any(r["cat"][n][:-3])
    y1 = np.array([options["y1"].index(t[0]) for t in truth])
    hit = r["q"]["y1"][np.arange(len(held)), y1]                  # learned-metric share on the truth
    assert hit[kind == 1].mean() > 0.85 and hit[kind == 0].mean() < 0.6


def test_r_expert_is_valid_and_copies_clusters(m):
    f, truth, kind = base.frame()
    given, heads, options = m._layout(base.SCHEMA)
    visible, held = m._roles(f, heads)
    y = {n: np.array([options[n].index(t[j]) for t in truth]) for j, n in enumerate(heads)}
    plain = m._fit_expert("g", f, base.SCHEMA, given, heads, options, visible, held)
    expert = m._fit_expert("r", f, base.SCHEMA, given, heads, options, visible, held)
    for n in heads:
        p = expert[n]
        assert p.shape == (len(held), len(options[n])) and np.isfinite(p).all() and (p > 0).all()
        assert np.allclose(p.sum(axis=1), 1.0)
    copies = np.flatnonzero(kind == 1)
    assert _mean_log(expert, y, heads, copies) > np.log(0.8)
    assert _mean_log(expert, y, heads, copies) > _mean_log(plain, y, heads, copies) + 0.02


def test_r_chain_grammar(m):
    assert m._split("rmix100") == ("r", "mix100") and m._split("rlpoolh") == ("r", "lpoolh")
    assert m._split("regate") == ("t", "regate")
    assert m._needs_expert("rlpool+cal") == {"r"} and m._needs_expert("regate") == set()
