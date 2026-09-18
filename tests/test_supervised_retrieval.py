"""E041 leakage, objective and fallback invariants."""

import numpy as np
import pandas as pd
from scipy.optimize._numdiff import approx_derivative

from src.models import supervised_retrieval as model


def test_metric_gradient_matches_finite_differences():
    rng = np.random.default_rng(4)
    features = rng.integers(0, 2, (9, 5, 3)).astype(float)
    matches = rng.integers(0, 2, (9, 5, 4)).astype(float)
    prior = np.full((9, 4), .3)
    sizes = np.array([3, 3, 4, 5])
    initial = np.array([1., 2., 3.])
    x = np.array([1.2, .7, 2.2, -.3])
    args = (features, matches, prior, sizes, initial)
    loss, gradient = model.metric_objective(x, *args)
    numerical = approx_derivative(lambda z: model.metric_objective(z, *args)[0], x)
    assert np.isfinite(loss)
    np.testing.assert_allclose(gradient, numerical.ravel(), atol=1e-6, rtol=1e-5)


def test_selector_labels_cannot_enter_metric_training():
    rng = np.random.default_rng(12)
    codes = rng.integers(0, 3, (100, 3))
    labels = np.column_stack([codes[:, 0], codes[:, 1]])
    bank, fit, select = np.arange(50), np.arange(50, 80), np.arange(80, 100)
    args = (codes, labels, bank, fit, select, np.ones(3), [3, 3], [[0, 1]])
    first = model.fit_sections(*args, k=8, maxiter=15, min_gain=0)
    changed = labels.copy()
    changed[select] = (changed[select] + 1) % 3
    second = model.fit_sections(codes, changed, bank, fit, select,
                                np.ones(3), [3, 3], [[0, 1]],
                                k=8, maxiter=15, min_gain=0)
    np.testing.assert_array_equal(first[0][0], second[0][0])


def test_overlapping_label_partitions_are_rejected():
    codes = np.zeros((9, 2), dtype=int)
    labels = np.zeros((9, 1), dtype=int)
    import pytest
    with pytest.raises(ValueError, match="disjoint"):
        model.fit_sections(codes, labels, [0, 1, 2], [2, 3, 4], [6, 7, 8],
                           np.ones(2), [2], [[0]])


def test_non_unhcr_routes_to_unchanged_incumbent(monkeypatch):
    sentinel = object()
    calls = []
    monkeypatch.setattr(model.hh_cap, "predict",
                        lambda *args, **kwargs: calls.append((args, kwargs)) or sentinel)
    assert model.predict("frame", {"items": {}}) is sentinel
    assert len(calls) == 1


def test_official_floor_is_used_in_the_optimization():
    features = np.zeros((1, 2, 1))
    matches = np.array([[[1.], [0.]]])
    prior = np.array([[.25]])
    params = np.array([0., 0.])  # mixture share .5, evidence probability .5
    loss, _ = model.metric_objective(params, features, matches, prior, [4], [0.])
    expected = -np.log(.001 + .996 * .375)
    assert abs(loss - expected) < 1e-12


def _layer_case():
    """Exact GIVEN/answer relation makes retrieval useful against a weak base."""
    item = "s3_11_intent_return_12m_lbl"
    options = [str(i) for i in range(5)]
    answers = np.asarray(options)[np.arange(521) % len(options)]
    frame = pd.DataFrame({"given": answers, item: answers})
    frame.loc[500:, item] = np.nan
    schema = {
        "gated_value": "NA_GATED",
        "items": {
            "given": {"class": "GIVEN", "values": options},
            item: {"class": "PREDICT", "values": options},
        },
    }
    return frame, schema, item


def test_no_active_unhcr_layer_matches_incumbent_with_nonzero_lambda(monkeypatch):
    frame, schema, item = _layer_case()
    base = {item: np.full((len(frame), 5), .2)}
    monkeypatch.setattr(model, "fit_sections",
                        lambda *args, **kwargs: ([np.ones(1)], [], []))

    actual_rows, actual_lambda = model.supervised_layer(frame, schema, base)
    expected_rows, expected_lambda = model.hh_sharp_layer(frame, schema, base)

    assert expected_rows
    assert any(value > 0 for pair in expected_lambda.values() for value in pair)
    assert actual_lambda == expected_lambda
    assert actual_rows.keys() == expected_rows.keys()
    for row in expected_rows:
        actual_evidence, actual_bucket = actual_rows[row]
        expected_evidence, expected_bucket = expected_rows[row]
        assert actual_bucket == expected_bucket
        assert actual_evidence.keys() == expected_evidence.keys()
        for name in expected_evidence:
            np.testing.assert_array_equal(actual_evidence[name], expected_evidence[name])


def test_replay_labels_are_isolated_from_metric_fit_and_section_selection(monkeypatch):
    frame, schema, item = _layer_case()
    # Distinct row probabilities let the lambda spy identify actual calibration
    # rows while leaving fitting, retrieval, and lambda optimization unchanged.
    correct_probability = .12 + np.arange(len(frame)) * .0001
    base_probability = np.repeat(((1 - correct_probability) / 4)[:, None], 5, axis=1)
    base_probability[np.arange(len(frame)), np.arange(len(frame)) % 5] = correct_probability
    base = {item: base_probability}
    probability_row = {float(value): row for row, vector in enumerate(base_probability)
                       for value in vector}
    fits, calibration_rows = [], []
    original_fit, original_lambda = model.fit_sections, model._best_lambda

    def capture_fit(codes, labels, bank, fit, select, *args, **kwargs):
        result = original_fit(codes, labels, bank, fit, select, *args, **kwargs)
        fits.append((bank.copy(), fit.copy(), select.copy(), result))
        return result

    def capture_lambda(p_model, p_ev):
        calibration_rows.extend(probability_row[float(value)] for value in p_model)
        return original_lambda(p_model, p_ev)

    monkeypatch.setattr(model, "fit_sections", capture_fit)
    monkeypatch.setattr(model, "_best_lambda", capture_lambda)
    model.supervised_layer(frame, schema, base)
    bank, fit, select, first = fits[0]
    assert first[1] == [0], "Synthetic section must activate to exercise replay calibration"
    visible = np.flatnonzero(frame[item].notna().to_numpy())
    replay = np.setdiff1d(visible, np.concatenate((bank, fit, select)))
    partitions = (bank, fit, select, replay)
    assert all(len(partition) for partition in partitions)
    for i, partition in enumerate(partitions):
        for other in partitions[i + 1:]:
            assert not np.intersect1d(partition, other).size
    assert set(calibration_rows) == set(replay)

    changed = frame.copy()
    changed.loc[replay, item] = ((changed.loc[replay, item].astype(int) + 1) % 5).astype(str)
    calibration_rows.clear()
    model.supervised_layer(changed, schema, base)
    second = fits[1][3]
    for before, after in zip(first[0], second[0]):
        np.testing.assert_array_equal(before, after)
    assert first[1:] == second[1:]
    assert set(calibration_rows) == set(replay)
