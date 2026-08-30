import numpy as np
import pytest

from src.models import hier_backoff, logit_blend
from tests.test_stratum_backoff import load_sample


def test_vectors_valid():
    frame, schema = load_sample()
    out = logit_blend.predict(frame, schema)
    assert len(out) > 0
    for vec in out:
        assert np.all(np.isfinite(vec))
        assert np.all(vec >= 0)
        assert vec.sum() == pytest.approx(1.0, abs=1e-6)


def test_w_zero_equals_e006():
    """w=0 must reduce exactly to the E006 ladder (same cols/kappas)."""
    frame, schema = load_sample()
    cols, kappas, _ = hier_backoff.select_ladder(frame, schema)
    ours = logit_blend.predict(frame, schema, cols=cols, kappas=kappas,
                               w=0.0)
    e006 = hier_backoff.predict(frame, schema, cols=cols, kappas=kappas)
    assert len(ours) == len(e006)
    for a, b in zip(ours, e006):
        assert np.allclose(a, b, atol=1e-12)


def test_tuned_weight_in_range():
    frame, schema = load_sample()
    cols, kappas, _ = hier_backoff.select_ladder(frame, schema)
    w, scores = logit_blend.tune_weight(frame, schema, cols, kappas)
    assert 0.0 <= w <= 1.0
    # tuned w can never score worse than the pure ladder on the holdout
    assert scores[w] >= scores[0.0]


def test_single_class_model_is_none():
    X = np.zeros((10, 3))
    codes = np.zeros(10, dtype=int)
    assert logit_blend._fit_model(X, codes, 4) is None
    proba = logit_blend._proba(None, X, 4)
    assert proba.shape == (10, 4)
    assert np.all(proba == 0)
