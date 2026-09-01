import numpy as np
import pytest

from src.models import shared_trunk
from tests.test_soft_gating import load
from score import sample_rows  # noqa: E402 (KIT on sys.path via import)


def test_vectors_valid_sample():
    frame, schema = load("sample")
    merged, _, _ = sample_rows(schema, frame, 1)
    out = shared_trunk.predict(merged, schema)
    assert len(out) > 0
    for vec in out:
        assert np.all(np.isfinite(vec))
        assert np.all(vec >= 0)
        assert vec.sum() == pytest.approx(1.0, abs=1e-6)


def test_deterministic():
    frame, schema = load("sample")
    merged, _, _ = sample_rows(schema, frame, 1)
    a = shared_trunk.predict(merged, schema)
    b = shared_trunk.predict(merged, schema)
    assert len(a) == len(b)
    for x, y in zip(a, b):
        assert np.allclose(x, y, atol=1e-7)


def test_cond_targets_masked():
    frame, schema = load("sample")
    merged, _, _ = sample_rows(schema, frame, 1)
    records = schema["items"]
    items = [n for n, r in records.items()
             if r["class"] in ("GIVEN", "PREDICT")]
    from src.models.hier_backoff import _complete_rows, _layout
    records, items, options = _layout(merged, schema)
    complete = _complete_rows(merged, items)
    predict_items = [n for n in items if records[n]["class"] == "PREDICT"]
    gated = [n for n in predict_items if records[n].get("gate")]
    full, cond = shared_trunk._targets(complete, predict_items, options,
                                       records, schema["gated_value"])
    assert full.shape == (len(complete), len(predict_items))
    assert cond.shape == (len(complete), len(gated))
    assert (full >= 0).all()  # complete rows: every full target valid
    for j, item in enumerate(gated):
        sentinel = complete[item] == schema["gated_value"]
        # sentinel rows must be masked out of the conditional head
        assert (cond[sentinel.to_numpy(), j] == -1).all()
        assert (cond[~sentinel.to_numpy(), j] >= 0).all()
