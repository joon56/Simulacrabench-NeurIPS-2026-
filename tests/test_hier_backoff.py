import numpy as np
import pytest

from src.models import hier_backoff
from tests.test_stratum_backoff import load_sample


def test_vectors_valid():
    frame, schema = load_sample()
    out = hier_backoff.predict(frame, schema)
    assert len(out) > 0
    for vec in out:
        assert np.all(np.isfinite(vec))
        assert np.all(vec >= 0)
        assert vec.sum() == pytest.approx(1.0, abs=1e-6)


def test_empty_ladder_is_marginal_plus_gates():
    """cols=[] must reduce to the global-marginal gate-coupled model."""
    frame, schema = load_sample()
    from src.models import gated_marginal
    ours = hier_backoff.predict(frame, schema, cols=[], kappas=[])
    e002 = gated_marginal.predict(frame, schema)
    # smoothing differs slightly (0.5-count marginal is shared), gate math
    # identical: vectors must be close, not bit-equal
    for a, b in zip(ours, e002):
        assert np.allclose(a, b, atol=5e-3)


def test_ladder_lookup_falls_back():
    p0 = np.array([0.5, 0.5])
    l1 = {("a",): np.array([0.9, 0.1])}
    l2 = {("a", "x"): np.array([0.8, 0.2])}
    assert np.allclose(
        hier_backoff.ladder_lookup(p0, [l1, l2], ("a", "x")), [0.8, 0.2])
    assert np.allclose(
        hier_backoff.ladder_lookup(p0, [l1, l2], ("a", "y")), [0.9, 0.1])
    assert np.allclose(
        hier_backoff.ladder_lookup(p0, [l1, l2], ("b", "y")), [0.5, 0.5])


def test_deeper_level_shrinks_toward_parent_when_thin():
    frame, schema = load_sample()
    items = [n for n, r in schema["items"].items()
             if r["class"] in ("GIVEN", "PREDICT")]
    complete = hier_backoff._complete_rows(frame, items)
    item = next(n for n, r in schema["items"].items()
                if r["class"] == "PREDICT" and not r.get("gate"))
    opts = list(schema["items"][item]["values"])
    p0, levels = hier_backoff.build_ladder(
        complete, item, opts, ["region", "age_band"], [1e9, 1e9])
    # with huge kappa every level collapses onto its parent
    for table in levels:
        for vec in table.values():
            assert np.allclose(vec, p0, atol=1e-3)
