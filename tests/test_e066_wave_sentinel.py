"""E066 wave-coded sentinel transfer: flagging and mass movement on fabricated frames."""
import importlib.util
import sys
import types
from pathlib import Path

import numpy as np
import pandas as pd

MAIN = Path(__file__).resolve().parents[1] / "submissions" / "2026-11-08-E066" / "main.py"


def load_module():
    sys.modules["e041_core"] = types.SimpleNamespace(predict=lambda frame, schema: None)
    spec = importlib.util.spec_from_file_location("e066_main", MAIN)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCHEMA = {
    "gated_value": "NA_GATED",
    "items": {
        "wave": {"class": "GIVEN", "values": ["1", "2"], "gate": None},
        "s3_11_intent_return_12m_lbl": {"class": "PREDICT", "values": ["0. No", "1. Yes"], "gate": None},
        "s6_6_food": {"class": "PREDICT", "values": ["0", "1"],
                      "gate": {"parent": "s6_5_assistance_received_lbl", "observed_if": ["1. Yes"]}},
        "s9_other": {"class": "PREDICT", "values": ["0", "1"],
                     "gate": {"parent": "s3_11_intent_return_12m_lbl", "observed_if": ["1. Yes"]}},
    },
}
HEADS = ["s3_11_intent_return_12m_lbl", "s6_6_food", "s9_other"]


def frame(n1=400, n2=400, sentinel_in_wave1=False):
    rows = []
    for w, n in (("1", n1), ("2", n2)):
        for i in range(n):
            food = "NA_GATED" if (w == "2" and i % 4 == 0) else ("1" if i % 3 == 0 else "0")
            if sentinel_in_wave1 and w == "1" and i == 7:
                food = "NA_GATED"
            other = "NA_GATED" if i % 5 == 0 else "0"
            rows.append({"wave": w, "s3_11_intent_return_12m_lbl": "1. Yes", "s6_6_food": food, "s9_other": other})
    for w in ("1", "2", "1"):
        rows.append({"wave": w, "s3_11_intent_return_12m_lbl": None, "s6_6_food": None, "s9_other": None})
    return pd.DataFrame(rows)


def vectors(n_held):
    out = []
    for _ in range(n_held):
        out += [[0.5, 0.5], [0.6, 0.1, 0.3], [0.5, 0.2, 0.3]]
    return out


def test_flags_only_the_documented_wave():
    m = load_module()
    f = frame()
    visible = np.flatnonzero(f[HEADS].notna().all(axis=1).to_numpy())
    assert m.flagged_cells(f, SCHEMA, HEADS, visible) == {("s6_6_food", "1")}


def test_no_flag_when_wave1_has_a_sentinel_or_too_few_rows():
    m = load_module()
    for f in (frame(sentinel_in_wave1=True), frame(n1=299)):
        visible = np.flatnonzero(f[HEADS].notna().all(axis=1).to_numpy())
        assert m.flagged_cells(f, SCHEMA, HEADS, visible) == set()


def test_transfer_moves_sentinel_mass_to_zero_for_wave1_rows_only():
    m = load_module()
    f = frame()
    v = vectors(3)
    out = m.transfer(f, SCHEMA, v)
    assert len(out) == len(v)
    # held rows are waves 1, 2, 1; family item is head index 1
    assert np.allclose(out[1], [0.9, 0.1, 0.0], rtol=0, atol=1e-12)
    assert out[4] == [0.6, 0.1, 0.3]
    assert np.allclose(out[7], [0.9, 0.1, 0.0], rtol=0, atol=1e-12)
    # non-family and ungated heads untouched; input not mutated
    for i in (0, 2, 3, 5, 6, 8):
        assert out[i] == v[i]
    assert v[1] == [0.6, 0.1, 0.3]


def test_no_change_when_nothing_flagged():
    m = load_module()
    f = frame(sentinel_in_wave1=True)
    v = vectors(3)
    assert m.transfer(f, SCHEMA, v) is v
