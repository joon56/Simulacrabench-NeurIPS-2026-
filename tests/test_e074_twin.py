"""E074 `twin` chain: honest copy share from the best-matching labelled rows (fabricated data only).

Usage: E074_BUILD=<build dir> python tmp/e074_selftest.py   (the model venv has no pytest)
"""
import importlib.util
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = os.environ.get("E074_BUILD")

SCHEMA = {
    "gated_value": "NA_GATED",
    "items": {
        "wave": {"class": "GIVEN", "values": ["1", "2"], "gate": None},
        **{c: {"class": "GIVEN", "values": [str(i) for i in range(6)], "gate": None} for c in "abcdefg"},
        "y1": {"class": "PREDICT", "values": ["u", "v", "w"], "gate": None},
        "y2": {"class": "PREDICT", "values": ["0", "1"], "gate": {"parent": "y1", "observed_if": ["u"]}},
    },
}
GIVEN = ["wave"] + list("abcdefg")
HEADS = ["y1", "y2"]


def load():
    sys.path.insert(0, BUILD)
    spec = importlib.util.spec_from_file_location("e074_main", Path(BUILD) / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def frame(clusters=300, singles=900, held_copies=150, held_fresh=150, noise=0.02, seed=0):
    """Clusters: three visible rows with one GIVEN block and (almost) the same answers; singles: one
    visible row each. Held rows either copy a cluster (answers follow it) or are fresh profiles."""
    rng = np.random.default_rng(seed)

    def profile():
        return dict({"wave": str(rng.integers(1, 3))}, **{c: str(rng.integers(6)) for c in "abcdefg"})

    def answers():
        y1 = str(rng.choice(["u", "v", "w"]))
        return y1, (str(rng.integers(2)) if y1 == "u" else "NA_GATED")

    def jitter(y1, y2):
        return answers() if rng.random() < noise else (y1, y2)

    rows, truth, kind = [], [], []
    cluster = []
    for _ in range(clusters):
        g, (y1, y2) = profile(), answers()
        cluster.append((g, y1, y2))
        for _ in range(3):
            a1, a2 = jitter(y1, y2)
            rows.append(dict(g, y1=a1, y2=a2))
    for _ in range(singles):
        y1, y2 = answers()
        rows.append(dict(profile(), y1=y1, y2=y2))
    for i in range(held_copies):
        g, y1, y2 = cluster[i]
        rows.append(dict(g, y1=None, y2=None))
        truth.append(jitter(y1, y2))
        kind.append(1)
    for _ in range(held_fresh):
        rows.append(dict(profile(), y1=None, y2=None))
        truth.append(answers())
        kind.append(0)
    return pd.DataFrame(rows), truth, np.array(kind)


def _setup(m, **kwargs):
    f, truth, kind = frame(**kwargs)
    given, heads, options = m._layout(SCHEMA)
    visible, held = m._roles(f, heads)
    twin = m._twin_evidence(f, given, heads, options, visible, held)
    y = {n: np.array([options[n].index(t[j]) for t in truth]) for j, n in enumerate(heads)}
    base = {n: np.full((len(held), len(options[n])), 1.0 / len(options[n])) for n in heads}
    return f, heads, options, twin, y, base, kind


def _mean_log(m, maps, y, heads, rows=None):
    total, cells = 0.0, 0
    for n in heads:
        p = m._floored(maps[n])
        idx = np.arange(len(p)) if rows is None else rows
        total += float(np.log(p[idx, y[n][idx]]).sum())
        cells += len(idx)
    return total / cells


def test_twin_evidence_and_features(m):
    f, heads, options, twin, y, base, kind = _setup(m)
    width = len(GIVEN) + 6
    assert twin["x"].shape == (len(kind), width) and np.isfinite(twin["x"]).all()
    for n in heads:
        ev = twin["ev"][n]
        assert ev.shape == base[n].shape and (ev >= 0).all() and np.allclose(ev.sum(axis=1), 1.0)
    copies = kind == 1
    assert (twin["x"][copies, :len(GIVEN)] == 0).all()             # best row agrees on every field
    assert (twin["x"][copies, len(GIVEN)] == 1).all()              # at least two exact rows
    assert twin["x"][copies, len(GIVEN) + 2].mean() > 0.9          # the two best rows answer alike
    hit = twin["ev"]["y1"][np.arange(len(kind)), y["y1"]]
    assert hit[copies].mean() > 0.9 and hit[~copies].mean() < 0.6


def test_twin_fit_trusts_clusters_and_not_lookalikes(m):
    f, heads, options, twin, y, base, kind = _setup(m)
    fit_rows = np.arange(0, len(kind), 2)
    test_rows = np.arange(1, len(kind), 2)
    truth = {n: y[n][fit_rows] for n in heads}
    for per_head in (False, True):
        params = m._twin_fit(base, twin, fit_rows, truth, heads, per_head)
        out = m._twin_apply(base, twin, params, heads)
        for n in heads:
            assert np.isfinite(out[n]).all() and (out[n] >= 0).all() and np.allclose(out[n].sum(axis=1), 1.0)
        share = m._twin_share(params["a"] + twin["x"] @ params["g"])
        assert share[kind == 1].mean() > 0.9 and share[kind == 0].mean() < 0.35
        gain = _mean_log(m, out, y, heads, test_rows) - _mean_log(m, base, y, heads, test_rows)
        assert gain > 0.25                                         # out of sample
        copies = test_rows[kind[test_rows] == 1]
        assert _mean_log(m, out, y, heads, copies) > np.log(0.85)


def test_twin_fit_is_inert_without_signal(m):
    f, heads, options, twin, y, base, kind = _setup(m, clusters=0, singles=1500, held_copies=0, held_fresh=300)
    rows = np.arange(len(kind))
    params = m._twin_fit(base, twin, rows[:150], {n: y[n][:150] for n in heads}, heads, False)
    out = m._twin_apply(base, twin, params, heads)
    assert abs(_mean_log(m, out, y, heads, rows[150:]) - _mean_log(m, base, y, heads, rows[150:])) < 0.02


def test_twin_fit_is_stationary(m):
    f, heads, options, twin, y, base, kind = _setup(m)
    rows = np.arange(len(kind))
    params = m._twin_fit(base, twin, rows, y, heads, False)

    def value(p):
        return _mean_log(m, m._twin_apply(base, twin, p, heads), y, heads) - m.TWIN_RIDGE * float(p["g"] @ p["g"])

    best = value(params)
    for step in (-0.2, 0.2):
        moved = dict(params, a=params["a"] + step)
        assert value(moved) <= best + 1e-6
        for j in range(len(params["g"])):
            g = params["g"].copy()
            g[j] = np.clip(g[j] + step, -12, 12)
            assert value(dict(params, g=g)) <= best + 1e-6


def test_twin_chain_through_apply_and_oof(m):
    f, heads, options, twin, y, base, kind = _setup(m)
    experts = {"w": twin}
    rows = np.arange(len(kind))
    assert m._is_fitted("twin") and m._is_fitted("twinh+cal") and m._needs_expert("twinh+cal") == {"w"}
    for chain in ("twin", "twinh", "twin+cal", "twinh+cal"):
        stack = {}
        out = m._apply(chain, f, SCHEMA, base, experts, heads, options, stack, fit=(rows, y))
        again = m._apply(chain, f, SCHEMA, base, experts, heads, options, stack)
        for n in heads:
            assert np.allclose(out[n], again[n]) and np.allclose(out[n].sum(axis=1), 1.0) and (out[n] >= 0).all()
        assert "twin@" + chain in stack and isinstance(m._stack_summary("twin@" + chain, stack["twin@" + chain]), dict)
        order = np.random.default_rng(1).permutation(rows)        # the guard's S rows are a random sample
        oof = m._chain_oof(chain, f, SCHEMA, base, experts, order, {n: y[n][order] for n in heads}, heads, options)
        assert oof > _mean_log(m, base, y, heads) + 0.2
