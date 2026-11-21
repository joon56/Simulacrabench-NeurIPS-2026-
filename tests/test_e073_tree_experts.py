"""E073 tree-expert plumbing on fabricated frames (run inside the model venv with a built package).

Usage: E073_BUILD=<build dir> python -m pytest -q tests/test_e073_tree_experts.py
The build dir must hold main.py, e041_core.py, vendor/ and weights/ (see scripts/build_e070.py).
"""
import importlib.util
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

BUILD = os.environ.get("E073_BUILD")
pytestmark = pytest.mark.skipif(not BUILD, reason="E073_BUILD not set")


@pytest.fixture(scope="module")
def m():
    sys.path.insert(0, BUILD)
    spec = importlib.util.spec_from_file_location("e073_main", Path(BUILD) / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCHEMA = {
    "gated_value": "NA_GATED",
    "items": {
        "wave": {"class": "GIVEN", "values": ["1", "2"], "gate": None},
        "s2_3_boys_0_5": {"class": "GIVEN", "values": ["0", "1", "2", "6-10", "11+"], "gate": None},
        "s2_3_girls_0_5": {"class": "GIVEN", "values": ["0", "1", "2", "6-10", "11+"], "gate": None},
        "s2_3_men_18_59": {"class": "GIVEN", "values": ["0", "1", "2", "6-10", "11+"], "gate": None},
        "s2_3_women_18_59": {"class": "GIVEN", "values": ["0", "1", "2", "6-10", "11+"], "gate": None},
        "region": {"class": "GIVEN", "values": ["a", "b", "c", "d"], "gate": None},
        "y_copy": {"class": "PREDICT", "values": ["u", "v", "w"], "gate": None},
        "y_gated": {"class": "PREDICT", "values": ["0", "1"],
                    "gate": {"parent": "y_copy", "observed_if": ["u"]}},
    },
}
GIVEN = ["wave", "s2_3_boys_0_5", "s2_3_girls_0_5", "s2_3_men_18_59", "s2_3_women_18_59", "region"]
HEADS = ["y_copy", "y_gated"]


def frame(n_pairs=400, n_held=40, seed=0):
    """Twin pairs share GIVEN and (mostly) answers; answers are otherwise unpredictable from GIVEN."""
    rng = np.random.default_rng(seed)
    rows = []
    levels = ["0", "1", "2", "6-10", "11+"]
    for _ in range(n_pairs + n_held):
        g = {"wave": rng.choice(["1", "2"]), "region": rng.choice(["a", "b", "c", "d"])}
        for c in GIVEN[1:5]:
            g[c] = rng.choice(levels)
        y = rng.choice(["u", "v", "w"])
        yg = rng.choice(["0", "1"]) if y == "u" else "NA_GATED"
        rows.append((g, y, yg))
    data = []
    for g, y, yg in rows[:n_pairs]:            # visible twins: two rows each
        data.append(dict(g, y_copy=y, y_gated=yg))
        data.append(dict(g, y_copy=y, y_gated=yg))
    for g, y, yg in rows[n_pairs:]:            # one visible twin + one held-out row
        data.append(dict(g, y_copy=y, y_gated=yg))
    truth = []
    for g, y, yg in rows[n_pairs:]:
        data.append(dict(g, y_copy=None, y_gated=None))
        truth.append((y, yg))
    return pd.DataFrame(data), truth


def test_given_codes_and_roster_totals(m):
    f, _ = frame(5, 2)
    coded = m._given_codes(f, SCHEMA, GIVEN)
    assert coded.shape == (len(f), 6) and np.isfinite(coded).all()
    extra = m._derived(f, SCHEMA, GIVEN)
    assert extra is not None and extra.shape == (len(f), 2)       # roster total and children total
    row = f.iloc[0]
    value = {"0": 0, "1": 1, "2": 2, "6-10": 8, "11+": 12}
    assert extra[0, 0] == sum(value[row[c]] for c in GIVEN[1:5])
    assert extra[0, 1] == value[row["s2_3_boys_0_5"]] + value[row["s2_3_girls_0_5"]]


def test_neighbors_exclude_self_and_find_twin(m):
    f, _ = frame(50, 5)
    codes, weights = m._signature(f, GIVEN)
    visible = np.arange(105)
    index, score, count = m._top_neighbors(codes, weights, visible, visible)
    assert (index[:, 0] != visible).all()                          # never itself
    twins = np.arange(100)
    assert (index[twins, 0] == (twins ^ 1)).mean() > 0.9           # the duplicated row is the top match
    assert (count[twins, 0] == len(GIVEN)).mean() > 0.9
    held = np.arange(105, 110)
    index_q, _, count_q = m._top_neighbors(codes, weights, held, visible)
    assert set(index_q[:, 0]) <= set(range(100, 105)) or (count_q[:, 0] == len(GIVEN)).all()


def test_neighbor_trees_learn_to_copy_and_plain_trees_cannot(m):
    f, truth = frame()
    given, heads, options = m._layout(SCHEMA)
    visible, held = m._roles(f, heads)
    plain = m._expert_hgb(f, SCHEMA, given, heads, options, visible, held, neighbors=False)
    near = m._expert_hgb(f, SCHEMA, given, heads, options, visible, held, neighbors=True)
    for maps in (plain, near):
        for name in heads:
            p = maps[name]
            assert p.shape == (len(held), len(options[name])) and np.isfinite(p).all()
            assert (p > 0).all() and np.allclose(p.sum(axis=1), 1.0)

    def mean_log(maps):
        total = 0.0
        for i, (y, yg) in enumerate(truth):
            total += np.log(maps["y_copy"][i, options["y_copy"].index(y)])
            total += np.log(maps["y_gated"][i, options["y_gated"].index(yg)])
        return total / (2 * len(truth))

    assert mean_log(near) > mean_log(plain) + 0.3                  # twin answers are informative here
    assert mean_log(near) > np.log(0.6)


def _noisy_models(seed=0, rows=1500, width=3):
    """Two imperfect, partly independent probabilistic views of the same latent truth."""
    rng = np.random.default_rng(seed)
    y = rng.integers(0, width, size=rows)
    out = []
    for strength in (2.0, 1.6):
        logits = rng.normal(size=(rows, width))
        logits[np.arange(rows), y] += strength
        p = np.exp(logits)
        out.append(p / p.sum(axis=1, keepdims=True))
    return y, out[0], out[1]


def test_log_pool_gradient_and_gain(m):
    y, p1, p2 = _noisy_models()
    logs = [m._clog(p1), m._clog(p2)]
    rows = np.arange(len(y))

    def mean_log(weights):
        return float(np.log(m._pool(logs, np.asarray(weights))[rows, y]).mean())

    fitted = m._pool_fit([logs], [y], [1.0, 0.0])
    assert (fitted > 0.2).all() and (fitted <= 3.0).all()            # both views get weight
    assert mean_log(fitted) > max(mean_log([1.0, 0.0]), mean_log([0.0, 1.0])) + 0.02
    for j in range(2):                                               # optimum: zero gradient inside bounds
        step = np.zeros(2)
        step[j] = 1e-4
        assert mean_log(fitted) >= mean_log(fitted + step) - 1e-9
        assert mean_log(fitted) >= mean_log(fitted - step) - 1e-9


def test_pool_chain_through_apply_keeps_valid_distributions(m):
    y, p1, p2 = _noisy_models(seed=1, rows=600)
    heads = ["h"]
    base, experts = {"h": p1}, {"n": {"h": p2}}
    idx = np.arange(400)
    params = m._pool_params("nlpoolh", base, experts, idx, {"h": y[idx]}, heads)
    assert params["kinds"] == ["n"] and set(params["heads"]) == {"h"}
    pooled = m._apply("nlpoolh", None, {"items": {}}, base, experts, heads, {"h": [0, 1, 2]}, {"nlpoolh": params})
    p = pooled["h"]
    assert p.shape == p1.shape and np.isfinite(p).all() and np.allclose(p.sum(axis=1), 1.0)
    held = np.arange(400, 600)
    gain = np.log(p[held, y[held]]).mean() - np.log(p1[held, y[held]]).mean()
    assert gain > 0.02                                               # out-of-sample gain on the fabricated data
    assert m._needs_expert("nlpoolh") == {"n"} and m._needs_expert("xlpool") == set(m.XSTACK_KINDS)


def _underconfident(seed=0, rows=4000):
    """A binary model that is right 99% of the time on its confident cells but only says ~.93."""
    rng = np.random.default_rng(seed)
    y = rng.integers(0, 2, size=rows)
    easy = rng.random(rows) < 0.8
    correct = np.where(easy, rng.random(rows) < 0.99, rng.random(rows) < 0.65)
    guess = np.where(correct, y, 1 - y)
    stated = np.where(easy, rng.uniform(0.90, 0.96, rows), rng.uniform(0.55, 0.75, rows))
    p = np.empty((rows, 2))
    p[np.arange(rows), guess] = stated
    p[np.arange(rows), 1 - guess] = 1 - stated
    return y, p


def test_reliability_calibration_sharpens_underconfident_cells(m):
    y, p = _underconfident()
    heads = ["h"]
    fit, held = np.arange(2000), np.arange(2000, 4000)
    params = m._cal_fit({"h": p}, fit, {"h": y[fit]}, heads)
    xs, ys = params
    assert xs[0] == 0.5 and ys[0] == 0.5 and (np.diff(ys) >= 0).all() and ys.max() <= m.CAL_CAP
    q = m._cal_apply({"h": p}, params, heads)["h"]
    assert np.isfinite(q).all() and (q > 0).all() and np.allclose(q.sum(axis=1), 1.0)
    assert (q.argmax(axis=1) == p.argmax(axis=1)).all()                 # top class preserved
    before = np.log(m._floored(p)[held, y[held]]).mean()
    after = np.log(m._floored(q)[held, y[held]]).mean()
    assert after > before + 0.02                                        # held-out gain from sharpening
    low = p.max(axis=1) < 0.5
    assert np.allclose(q[low], p[low])


def test_cal_chain_fits_then_reuses_parameters(m):
    y, p = _underconfident(seed=3, rows=1200)
    heads, stack = ["h"], {}
    idx = np.arange(600)
    first = m._apply("cal", None, {"items": {}}, {"h": p}, {}, heads, {"h": [0, 1]}, stack,
                     fit=(idx, {"h": y[idx]}))
    assert "cal@cal" in stack
    again = m._apply("cal", None, {"items": {}}, {"h": p}, {}, heads, {"h": [0, 1]}, stack)
    assert np.allclose(first["h"], again["h"]) and m._needs_expert("cal") == set()
    assert isinstance(m._stack_summary("cal@cal", stack["cal@cal"]), list)


def test_per_head_temperature_pool_needs_no_expert_and_sharpens(m):
    y, p = _underconfident(seed=5, rows=3000)
    heads = ["h"]
    fit, held = np.arange(1500), np.arange(1500, 3000)
    params = m._pool_params("tpoolh", {"h": p}, {}, fit, {"h": y[fit]}, heads)
    assert params["kinds"] == [] and params["global"][0] > 1.05        # learned exponent sharpens
    q = m._apply("tpoolh", None, {"items": {}}, {"h": p}, {}, heads, {"h": [0, 1]}, {"tpoolh": params})["h"]
    assert np.allclose(q.sum(axis=1), 1.0) and np.isfinite(q).all()
    assert np.log(m._floored(q)[held, y[held]]).mean() > np.log(m._floored(p)[held, y[held]]).mean() + 0.01
    assert m._needs_expert("tpoolh") == set() and m._needs_expert("tpoolh+cal") == set()
    assert np.isfinite(m._pool_oof("tpoolh", {"h": p}, {}, fit, {"h": y[fit]}, heads))


def test_vote_features_and_m_expert(m):
    answers = np.array([0, 1, 1, 2, -1])
    near = np.array([[0, 1, 2], [3, 0, 1]])
    score = np.array([[5.0, 5.0, 5.0], [9.0, 1.0, 1.0]])
    shares = m._votes(answers, near, score, 3)
    assert np.allclose(shares.sum(axis=1), 1.0)
    assert np.allclose(shares[0], [1 / 3, 2 / 3, 0.0]) and shares[1, 2] > 0.99
    f, truth = frame(300, 40, seed=2)
    given, heads, options = m._layout(SCHEMA)
    visible, held = m._roles(f, heads)
    plain = m._fit_expert("g", f, SCHEMA, given, heads, options, visible, held)
    voted = m._fit_expert("m", f, SCHEMA, given, heads, options, visible, held)
    for name in heads:
        p = voted[name]
        assert p.shape == (len(held), len(options[name])) and (p > 0).all() and np.allclose(p.sum(axis=1), 1.0)

    def mean_log(maps):
        return float(np.mean([np.log(maps["y_copy"][i, options["y_copy"].index(y)])
                              for i, (y, _) in enumerate(truth)]))

    assert mean_log(voted) > mean_log(plain) + 0.3
    assert m._split("mlpoolh") == ("m", "lpoolh") and m._split("mix50") == ("t", "mix50")
    assert m._needs_expert("mlpool+cal") == {"m"}


def test_chain_oof_is_honest_for_fitted_chains(m):
    """Noise experts must not look useful: the out-of-fold score of a fitted chain stays at or
    below the base on pure-noise experts, while an informative expert scores above it."""
    rng = np.random.default_rng(7)
    rows, heads = 800, ["a", "b"]
    y = {n: rng.integers(0, 2, size=rows) for n in heads}

    def noisy(strength):
        maps = {}
        for n in heads:
            logits = rng.normal(size=(rows, 2))
            logits[np.arange(rows), y[n]] += strength
            p = np.exp(logits)
            maps[n] = p / p.sum(axis=1, keepdims=True)
        return maps

    base, good, junk = noisy(1.5), noisy(1.5), noisy(0.0)
    idx = np.arange(rows)
    schema, options = {"items": {}}, {n: [0, 1] for n in heads}
    reference = float(np.mean([np.log(m._floored(base[n])[idx, y[n]]).mean() for n in heads]))
    assert m._is_fitted("nlpoolh+cal") and m._is_fitted("cal") and not m._is_fitted("mix50")
    # the fabricated base is itself miscalibrated, so pools may gain from its exponent alone:
    # compare pooled chains with the base-only temperature pool, the linear stack with the raw base
    recalibrated = m._chain_oof("tpool", None, schema, base, {}, idx, y, heads, options)
    assert recalibrated >= reference - 0.005
    for chain, anchor in (("nlpool", recalibrated), ("nlpoolh", recalibrated), ("nstack", reference)):
        useful = m._chain_oof(chain, None, schema, base, {"n": good}, idx, y, heads, options)
        useless = m._chain_oof(chain, None, schema, base, {"n": junk}, idx, y, heads, options)
        assert useful > anchor + 0.02, (chain, useful, anchor)
        assert useless < anchor + 0.01, (chain, useless, anchor)
    junk_weight = m._pool_params("nlpool", base, {"n": junk}, idx, y, heads)["global"][1]
    good_weight = m._pool_params("nlpool", base, {"n": good}, idx, y, heads)["global"][1]
    assert junk_weight < 0.1 < good_weight
    assert np.isfinite(m._chain_oof("nlpoolh+cal", None, schema, base, {"n": good}, idx, y, heads, options))
