"""E076 expert q: retrieval trees with label-informed donor pairing (fabricated data only).

Usage: E076_BUILD=<build dir> python tmp/e076_selftest.py   (the model venv has no pytest)
"""
import importlib.util
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BUILD = os.environ.get("E076_BUILD")
HOUSE = ["h1", "h2", "h3", "h4"]          # household-level fields: shared by both records of a household
PERSON = ["p1", "p2", "p3"]               # respondent-level fields: redrawn for every record
HEADS = ["y%d" % i for i in range(1, 37)]      # enough answers for a sharp agreement score
SCHEMA = {
    "gated_value": "NA_GATED",
    "items": {
        "wave": {"class": "GIVEN", "values": ["1", "2"], "gate": None},
        **{c: {"class": "GIVEN", "values": [str(i) for i in range(4)], "gate": None} for c in HOUSE},
        **{c: {"class": "GIVEN", "values": [str(i) for i in range(2)], "gate": None} for c in PERSON},
        **{c: {"class": "PREDICT", "values": ["u", "v", "w"], "gate": None} for c in HEADS},
    },
}


def load():
    sys.path.insert(0, BUILD)
    spec = importlib.util.spec_from_file_location("e076_main", Path(BUILD) / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def frame(pairs=1100, singles=150, held_share=0.15, noise=0.03, seed=0):
    """Pair households contribute two records with the same household fields and (almost) the
    same answers; single households one record. Several households share each household
    signature, so a held record's twin competes with impostors that mostly have their own
    twin among the visible rows. Returns the frame, the truth of held rows and a flag marking
    held rows whose twin is visible."""
    rng = np.random.default_rng(seed)
    records = []
    for house in range(pairs + singles):
        sig = {c: str(rng.integers(4)) for c in HOUSE}
        answers = [str(rng.choice(["u", "v", "w"])) for _ in HEADS]
        for _ in range(2 if house < pairs else 1):
            mine = [str(rng.choice(["u", "v", "w"])) if rng.random() < noise else a for a in answers]
            records.append((house, dict(sig, wave=str(rng.integers(1, 3)),
                                        **{c: str(rng.integers(2)) for c in PERSON}), mine))
    order = rng.permutation(len(records))
    held = set(order[:int(held_share * len(records))].tolist())
    visible_houses = {}
    for i, (house, _, _) in enumerate(records):
        if i not in held:
            visible_houses[house] = visible_houses.get(house, 0) + 1
    rows, truth, twin_visible = [], [], []
    for i, (house, given, mine) in enumerate(records):
        if i in held:
            rows.append(dict(given, **{c: None for c in HEADS}))
            truth.append(mine)
            twin_visible.append(visible_houses.get(house, 0) > 0)
        else:
            rows.append(dict(given, **dict(zip(HEADS, mine))))
    columns = ["wave"] + HOUSE + PERSON + HEADS
    return pd.DataFrame(rows)[columns], truth, np.array(twin_visible)


def _mean_log(maps, y, heads, rows):
    return float(np.mean([np.log(maps[n][rows, y[n][rows]]) for n in heads]))


def test_pair_scores_flag_completed_pairs(m):
    f, truth, twin_visible = frame()
    given, heads, options = m._layout(SCHEMA)
    visible, held = m._roles(f, heads)
    codes, rarity = m.e041_core._sig_data_all(f, *m.e041_core._layout(f, SCHEMA)[:2])
    labels = np.full((len(f), len(heads)), -1, dtype=np.int64)
    for j, n in enumerate(heads):
        labels[visible, j] = m._labels(f, visible, n, options)
    bank, best, second, partner = m._pair_scores(codes, rarity, labels, visible)
    assert len(bank) == len(visible) and np.isfinite(best).all() and (best >= second).all()
    strong = best >= m.PAIR_STRONG
    assert 0.45 < strong.mean() < 0.95                       # most visible rows have their twin visible
    answers = f[heads].to_numpy(dtype=object)
    same = (answers[bank[strong]] == answers[partner[strong]]).mean()
    assert same > 0.9 and second[strong].mean() < m.PAIR_WEAK  # the partner is the twin; no second twin


def test_q_features_shape_and_twin_share(m):
    f, truth, twin_visible = frame()
    given, heads, options = m._layout(SCHEMA)
    visible, held = m._roles(f, heads)
    plain = m._retrieval_features(f, SCHEMA, heads, options, visible, held)
    paired = m._retrieval_features(f, SCHEMA, heads, options, visible, held, pairing=True)
    y = {n: np.array([options[n].index(t[j]) for t in truth]) for j, n in enumerate(heads)}
    rows = np.arange(len(held))
    gain = []
    for n in heads:
        width = len(options[n])
        assert paired["c"][n].shape == (len(visible), 2 * width + 9)
        assert paired["q"][n].shape == (len(held), 2 * width + 9) and np.isfinite(paired["q"][n]).all()
        assert paired["cat"][n][-3:] == [True] * 3 and not any(paired["cat"][n][:-3])
        assert np.allclose(paired["q"][n][:, :width].sum(axis=1), 1.0)
        gain.append(paired["q"][n][rows, y[n]][twin_visible].mean() - plain["q"][n][rows, y[n]][twin_visible].mean())
    assert np.mean(gain) > 0.08, np.mean(gain)               # more learned-metric mass on the twin's answer


def test_q_expert_beats_r_when_twins_compete_with_impostors(m):
    f, truth, twin_visible = frame()
    given, heads, options = m._layout(SCHEMA)
    visible, held = m._roles(f, heads)
    y = {n: np.array([options[n].index(t[j]) for t in truth]) for j, n in enumerate(heads)}
    r = m._fit_expert("r", f, SCHEMA, given, heads, options, visible, held)
    q = m._fit_expert("q", f, SCHEMA, given, heads, options, visible, held)
    for n in heads:
        assert q[n].shape == (len(held), len(options[n])) and np.isfinite(q[n]).all() and (q[n] > 0).all()
        assert np.allclose(q[n].sum(axis=1), 1.0)
    twins = np.flatnonzero(twin_visible)
    everyone = np.arange(len(held))
    assert _mean_log(q, y, heads, twins) > _mean_log(r, y, heads, twins) + 0.05
    # rows without a visible twin pay for the sharper match (measured -.07), the average must gain
    assert _mean_log(q, y, heads, everyone) > _mean_log(r, y, heads, everyone) + 0.03


def test_q_without_pairs_stays_close_to_r(m):
    f, truth, _ = frame(pairs=0, singles=1800)
    given, heads, options = m._layout(SCHEMA)
    visible, held = m._roles(f, heads)
    y = {n: np.array([options[n].index(t[j]) for t in truth]) for j, n in enumerate(heads)}
    r = m._fit_expert("r", f, SCHEMA, given, heads, options, visible, held)
    q = m._fit_expert("q", f, SCHEMA, given, heads, options, visible, held)
    rows = np.arange(len(held))
    assert abs(_mean_log(q, y, heads, rows) - _mean_log(r, y, heads, rows)) < 0.03


def test_q_chain_grammar_and_build_constants(m):
    assert m._split("qmix100") == ("q", "mix100") and m._split("qlpoolh") == ("q", "lpoolh")
    assert m._needs_expert("qlpool+cal") == {"q"} and m._needs_expert("rlpool") == {"r"}
    assert isinstance(m.E_Z, float) and isinstance(m.XSTACK_BY, dict)
    import inspect
    assert "E_Z * sd" in inspect.getsource(m._guard) and "1.645" not in inspect.getsource(m._guard)
