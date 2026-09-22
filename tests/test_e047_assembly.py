"""Exercise the active E047 policy in source and frozen single-file assembly."""

from pathlib import Path
import sys
import types

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from assemble_e047 import build_source
from src.models import adaptive_final_evidence as source


def snapshot():
    module = types.ModuleType("e047_test_snapshot")
    exec(compile(build_source(), "e047_test_snapshot", "exec"), module.__dict__)
    return module


def test_active_fit_apply_matches_assembled_helpers():
    assembled = snapshot()
    names = ["s3_a", "s4_b"]
    base = {name: np.tile([.6, .4], (120, 1)) for name in names}
    evidence = {name: np.tile([.2, .8], (120, 1)) for name in names}
    labels = {name: np.ones(120, dtype=int) for name in names}
    groups = [[name] for name in names]
    parts = (np.arange(40), np.arange(40, 80), np.arange(80, 120))
    policies, diagnostics = source.e047_fit_policies(base, evidence, labels, groups, *parts)
    frozen_policies, frozen_diagnostics = assembled.e047_fit_policies(
        base, evidence, labels, groups, *parts)
    assert policies, "This test must exercise a nonzero correction"
    assert policies == frozen_policies
    assert diagnostics == frozen_diagnostics
    first = source.e047_apply(base, evidence, groups, policies)
    second = assembled.e047_apply(base, evidence, groups, frozen_policies)
    for name in names:
        assert np.array_equal(first[name], second[name])
        assert np.all(first[name][:, 1] > base[name][:, 1])


def test_active_predict_matches_assembly_with_identical_first_stage(monkeypatch):
    assembled = snapshot()
    target = "s3_11_intent_return_12m_lbl"
    names = [target, "s4_test"]
    schema = {"gated_value": "NA_GATED", "scoring": {"floor": .001}, "items": {
        "given": {"class": "GIVEN", "values": ["a", "b"]},
        **{name: {"class": "PREDICT", "values": ["no", "yes"]} for name in names},
    }}
    frame = pd.DataFrame({"given": ["a", "b"] * 2001,
                          **{name: ["yes"] * 4000 + [np.nan, np.nan] for name in names}})

    def capture(data, specification, **kwargs):
        held = np.flatnonzero(data[names].isna().all(axis=1).to_numpy())
        base = {name: np.tile([.6, .4], (len(held), 1)) for name in names}
        evidence = {name: np.tile([.2, .8], (len(held), 1)) for name in names}
        raw = [base[name][row].copy() for row in range(len(held)) for name in names]
        return raw, base, evidence, held

    monkeypatch.setattr(source, "e047_capture", capture)
    monkeypatch.setattr(assembled, "e047_capture", capture)
    expected = source.predict(frame, schema)
    actual = assembled.predict(frame, schema)
    assert len(expected) == 4
    for a, b in zip(expected, actual):
        assert np.array_equal(a, b)
        assert a[1] > .4, "Active correction must survive the full predict path"
