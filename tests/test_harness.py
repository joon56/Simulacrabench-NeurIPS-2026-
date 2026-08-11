import numpy as np
import pytest

from src.eval.logloss import (
    mean_log_loss,
    evaluate,
    floor_mix,
    uniform_reference,
    skill,
)
from src.eval.masking import mcar_mask, holdout_respondents, apply_mask
from src.eval.synthetic import generate
from src.models.marginal import MarginalBaseline


def test_perfect_prediction_is_near_zero():
    y = np.array([0, 1, 2])
    p = np.eye(3)
    assert mean_log_loss(y, p) < 1e-10


def test_uniform_prediction_equals_log_k():
    y = np.array([0, 1, 2, 3])
    p = np.full((4, 4), 0.25)
    assert mean_log_loss(y, p) == pytest.approx(np.log(4))


def test_zero_probability_is_clipped_not_inf():
    y = np.array([0])
    p = np.array([[0.0, 1.0]])
    loss = mean_log_loss(y, p)
    assert np.isfinite(loss) and loss > 30  # -log(1e-15) ~ 34.5


def test_evaluate_pools_cells_not_items():
    # Two items with different masked-cell counts: pooled mean must weight
    # by cell count, not average the per-item means.
    import pandas as pd

    truth = pd.DataFrame({"a": [0, 0, 0], "b": [1, 1, 1]})
    mask = pd.DataFrame({"a": [True, True, True], "b": [True, False, False]})
    proba = {
        "a": np.tile([0.5, 0.5], (3, 1)),   # loss log(2) per cell, 3 cells
        "b": np.tile([0.2, 0.8], (3, 1)),   # loss -log(0.8), 1 cell
    }
    overall, per_item = evaluate(truth, mask, proba)
    expected = (3 * np.log(2) + -np.log(0.8)) / 4
    assert overall == pytest.approx(expected)
    assert per_item["a"][1] == 3 and per_item["b"][1] == 1


def test_marginal_beats_uniform_on_synthetic_track_a():
    df, n_levels, _ = generate(n=2000, seed=1)
    rng = np.random.default_rng(2)
    mask = mcar_mask(df, frac=0.2, rng=rng)
    train = apply_mask(df, mask)

    model = MarginalBaseline().fit(train, n_levels)
    proba = model.predict_proba(len(df))
    marginal_loss, _ = evaluate(df, mask, proba)

    uniform = {
        item: np.full((len(df), k), 1.0 / k) for item, k in n_levels.items()
    }
    uniform_loss, _ = evaluate(df, mask, uniform)

    assert marginal_loss < uniform_loss


def test_track_b_mask_keeps_demographics_visible():
    df, n_levels, demo_cols = generate(n=500, seed=3)
    rng = np.random.default_rng(4)
    mask, holdout = holdout_respondents(df, demo_cols, frac=0.3, rng=rng)

    assert len(holdout) > 0
    assert not mask[demo_cols].to_numpy().any()
    non_demo = [c for c in df.columns if c not in demo_cols]
    assert mask.loc[holdout, non_demo].to_numpy().all()
    kept = df.index.difference(holdout)
    assert not mask.loc[kept].to_numpy().any()


def test_gated_item_not_shown_is_a_scored_level():
    df, n_levels, _ = generate(n=2000, seed=5)
    # "Not shown" level (3) must occur and be predictable mass.
    assert (df["q_child"] == 3).any()
    rng = np.random.default_rng(6)
    mask = mcar_mask(df, frac=0.2, rng=rng)
    train = apply_mask(df, mask)
    model = MarginalBaseline().fit(train, n_levels)
    p_child = model.probs_["q_child"]
    assert len(p_child) == 4 and p_child[3] > 0


def test_floor_mix_keeps_floor_and_sum():
    p = np.array([[1.0, 0.0, 0.0], [0.4, 0.35, 0.25]])
    out = floor_mix(p, floor=1e-3)
    assert (out >= 1e-3).all()
    assert np.allclose(out.sum(axis=1), 1.0)


def test_skill_scale_matches_official_definition():
    # Uniform guess scores 0, perfection scores 1.
    n_levels = {"a": 4, "b": 2}
    u = uniform_reference(n_levels, ["a", "b"])
    assert u == pytest.approx((np.log(4) + np.log(2)) / 2)
    uniform_loss = u  # pooled mean over one cell each is the same mean here
    assert skill(uniform_loss, u) == pytest.approx(0.0)
    assert skill(0.0, u) == pytest.approx(1.0)


def test_masking_is_deterministic_with_seed():
    df, _, _ = generate(n=300, seed=7)
    m1 = mcar_mask(df, 0.1, np.random.default_rng(8))
    m2 = mcar_mask(df, 0.1, np.random.default_rng(8))
    assert m1.equals(m2)
