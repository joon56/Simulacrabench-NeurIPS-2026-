import numpy as np
import pytest

from src.models import hier_backoff, item_blend
from tests.test_stratum_backoff import load_sample


def test_vectors_valid():
    frame, schema = load_sample()
    out = item_blend.predict(frame, schema)
    assert len(out) > 0
    for vec in out:
        assert np.all(np.isfinite(vec))
        assert np.all(vec >= 0)
        assert vec.sum() == pytest.approx(1.0, abs=1e-6)


def test_all_w_zero_equals_e006():
    """Every item at w=0 must reduce exactly to the E006 ladder."""
    frame, schema = load_sample()
    cols, kappas, _ = hier_backoff.select_ladder(frame, schema)
    predict_items = [n for n, r in schema["items"].items()
                     if r["class"] == "PREDICT"]
    params = {item: (1.0, 0.0) for item in predict_items}
    ours = item_blend.predict(frame, schema, cols=cols, kappas=kappas,
                              params=params)
    e006 = hier_backoff.predict(frame, schema, cols=cols, kappas=kappas)
    assert len(ours) == len(e006)
    for a, b in zip(ours, e006):
        assert np.allclose(a, b, atol=1e-12)


def test_tuning_deterministic_and_uses_logit():
    frame, schema = load_sample()
    cols, kappas, _ = hier_backoff.select_ladder(frame, schema)
    p1, s1 = item_blend.tune_item_params(frame, schema, cols, kappas)
    p2, s2 = item_blend.tune_item_params(frame, schema, cols, kappas)
    assert p1 == p2 and s1 == s2
    # sandbox trait_scale=2.0 gives real GIVEN signal: at least one item
    # must pick a positive blend weight
    assert any(w > 0 for _, w in p1.values())


def test_params_shapes():
    frame, schema = load_sample()
    cols, kappas, _ = hier_backoff.select_ladder(frame, schema)
    params, _ = item_blend.tune_item_params(frame, schema, cols, kappas)
    predict_items = [n for n, r in schema["items"].items()
                     if r["class"] == "PREDICT"]
    assert set(params) == set(predict_items)
    for c_reg, w in params.values():
        assert c_reg in item_blend.C_GRID
        assert 0.0 <= w <= 1.0
