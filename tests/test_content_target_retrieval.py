"""Content-target retrieval contracts; tiny fixtures, no survey responses."""
import numpy as np
import pytest
from scipy.optimize._numdiff import approx_derivative

from src.models import content_target_retrieval as model
from src.models import supervised_retrieval as original


def objective_case():
    rng = np.random.default_rng(4)
    features = rng.integers(0, 2, (9, 5, 3)).astype(float)
    matches = rng.integers(0, 2, (9, 5, 4)).astype(float)
    args = (features, matches, np.full((9, 4), .3),
            np.array([3, 3, 4, 5]), np.array([1., 2., 3.]))
    return np.array([1.2, .7, 2.2, -.3]), args


def test_content_gradient_matches_finite_differences():
    params, args = objective_case()
    mask = np.ones((9, 4), dtype=bool)
    mask[::2, 1:3] = False
    loss, gradient = model.metric_objective(params, *args, cell_mask=mask)
    numerical = approx_derivative(
        lambda x: model.metric_objective(x, *args, cell_mask=mask)[0], params)
    assert np.isfinite(loss)
    np.testing.assert_allclose(gradient, numerical.ravel(), atol=1e-6, rtol=1e-5)


@pytest.mark.parametrize('value', [True, False])
def test_all_cells_or_empty_content_falls_back_exactly(value):
    params, args = objective_case()
    expected = original.metric_objective(params, *args)
    actual = model.metric_objective(params, *args, cell_mask=np.full((9, 4), value))
    assert actual[0] == expected[0]
    np.testing.assert_array_equal(actual[1], expected[1])


def test_excluded_cells_do_not_affect_fitting_objective():
    params, args = objective_case()
    mask = np.ones((9, 4), dtype=bool)
    mask[:, 2] = False
    expected = model.metric_objective(params, *args, cell_mask=mask)
    changed = list(args)
    changed[1] = args[1].copy()
    changed[1][:, :, 2] = 1 - changed[1][:, :, 2]
    changed[2] = args[2].copy()
    changed[2][:, 2] = .8
    actual = model.metric_objective(params, *changed, cell_mask=mask)
    assert actual[0] == expected[0]
    np.testing.assert_array_equal(actual[1], expected[1])


def test_selector_truth_cannot_change_metric_fitting():
    rng = np.random.default_rng(12)
    codes = rng.integers(0, 3, (100, 3))
    labels = np.column_stack([codes[:, 0], codes[:, 1]])
    bank, fit, select = np.arange(50), np.arange(50, 80), np.arange(80, 100)
    extra = dict(k=8, maxiter=15, sentinel_codes=[-1, 2])
    first = model.fit_sections(codes, labels, bank, fit, select,
                               np.ones(3), [3, 3], [[0, 1]], **extra)
    changed = labels.copy()
    changed[select] = (changed[select] + 1) % 3
    second = model.fit_sections(codes, changed, bank, fit, select,
                                np.ones(3), [3, 3], [[0, 1]], **extra)
    np.testing.assert_array_equal(first[0][0], second[0][0])


def test_no_sentinel_fixture_matches_original_fitter():
    rng = np.random.default_rng(12)
    codes = rng.integers(0, 3, (100, 3))
    labels = np.column_stack([codes[:, 0], codes[:, 1]])
    args = (codes, labels, np.arange(50), np.arange(50, 80), np.arange(80, 100),
            np.ones(3), [3, 3], [[0, 1]])
    expected = original.fit_sections(*args, k=8, maxiter=15)
    actual = model.fit_sections(*args, k=8, maxiter=15, sentinel_codes=[-1, -1])
    np.testing.assert_array_equal(actual[0][0], expected[0][0])
    assert actual[1] == expected[1]
    assert actual[2] == expected[2]


def test_non_unhcr_delegates_unchanged(monkeypatch):
    output = object()
    monkeypatch.setattr(model.hh_cap, 'predict', lambda *a, **k: output)
    assert model.predict('unused', {'items': {}}) is output
