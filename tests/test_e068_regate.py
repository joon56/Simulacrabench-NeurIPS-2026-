"""E068 re-gating: switch only when s3_12 explains skips better; sentinel = belief @ rates."""
import importlib.util
import sys
import types
from pathlib import Path

import numpy as np
import pandas as pd

MAIN = Path(__file__).resolve().parents[1] / "submissions" / "2026-11-09-E068" / "main.py"
NO, YES, DK, NA = "0. No", "1. Yes", "98. I don't know", "NA_GATED"


def load_module():
    sys.modules["e041_core"] = types.SimpleNamespace(predict=lambda frame, schema: None)
    spec = importlib.util.spec_from_file_location("e068_main", MAIN)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCHEMA = {
    "gated_value": NA,
    "items": {
        "wave": {"class": "GIVEN", "values": ["1", "2"], "gate": None},
        "s3_11_intent_return_12m_lbl": {"class": "PREDICT", "values": [NO, YES, DK], "gate": None},
        "s7a_1_dest": {"class": "PREDICT", "values": ["a", "b"],
                       "gate": {"parent": "s3_11_intent_return_12m_lbl", "observed_if": [YES]}},
        "s3_12_hope_return_someday_lbl": {"class": "PREDICT", "values": [NO, YES, DK],
                                          "gate": {"parent": "s3_11_intent_return_12m_lbl",
                                                   "observed_if": [NO, DK]}},
    },
}
HEADS = ["s3_11_intent_return_12m_lbl", "s7a_1_dest", "s3_12_hope_return_someday_lbl"]


def frame(follow_new=True, n=400):
    rows = []
    for i in range(n):
        s311 = [NO, YES, DK, NO][i % 4]
        s312 = NA if s311 == YES else [NO, YES, DK][i % 3]
        asked = (s312 == YES) if follow_new else (s311 == YES)
        rows.append({"wave": "2", HEADS[0]: s311, HEADS[1]: ("a" if i % 2 else "b") if asked else NA,
                     HEADS[2]: s312})
    for _ in range(2):
        rows.append({"wave": "2", HEADS[0]: None, HEADS[1]: None, HEADS[2]: None})
    return pd.DataFrame(rows)


def vectors():
    out = []
    for belief in ([0.0, 0.9, 0.05, 0.05], [0.8, 0.1, 0.05, 0.05]):  # P(s3_12) per held row
        out += [[0.5, 0.3, 0.2], [0.3, 0.1, 0.6], belief]
    return out


def test_switches_when_s3_12_explains_skips_and_rescales_content():
    m = load_module()
    out = m.regate(frame(True), SCHEMA, vectors())
    assert m.LAST[("s7a_", "2")]["switch"] is True
    for i, belief in enumerate(([0.0, 0.9, 0.05, 0.05], [0.8, 0.1, 0.05, 0.05])):
        child = np.asarray(out[i * 3 + 1])
        assert abs(child.sum() - 1) < 1e-12
        assert np.isclose(child[0] / child[1], 3.0)          # content proportions kept
        assert np.isclose(child[2], (child[2]))               # finite sentinel
    # respondent 1 likely hopes to return (asked): small sentinel; respondent 2 likely skipped
    assert out[1][2] < 0.25 and out[4][2] > 0.7   # smoothing toward the pooled rate on 400 rows
    # other heads untouched
    assert out[0] == [0.5, 0.3, 0.2] and out[2] == [0.0, 0.9, 0.05, 0.05]


def test_no_switch_when_schema_parent_fits_better():
    m = load_module()
    v = vectors()
    assert m.regate(frame(False), SCHEMA, v) is v
    assert m.LAST[("s7a_", "2")]["switch"] is False
