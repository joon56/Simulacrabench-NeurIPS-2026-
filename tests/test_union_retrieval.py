"""E045 union retrieval objective, leakage, and inheritance invariants."""

import numpy as np
import pandas as pd
from scipy.optimize._numdiff import approx_derivative

from src.models import supervised_retrieval as parent
from src.models import union_retrieval as model


def test_union_gradient_is_finite_with_padded_duplicates():
    rng = np.random.default_rng(45)
    features = rng.integers(0, 2, (7, 6, 3)).astype(float)
    matches = rng.integers(0, 2, (7, 6, 2)).astype(float)
    prior = np.full((7, 2), .3)
    valid = np.ones((7, 6), dtype=bool)
    valid[:, 4:] = False
    features[:, 4:] = features[:, :2]
    matches[:, 4:] = matches[:, :2]
    x = np.array([1.2, .7, 2.2, -.3])
    args = (features, matches, prior, [3, 4], [1., 2., 3.], valid)
    loss, gradient = model.union_objective(x, *args)
    numerical = approx_derivative(lambda z: model.union_objective(z, *args)[0], x)
    assert np.isfinite(loss)
    np.testing.assert_allclose(gradient, numerical.ravel(), atol=1e-6, rtol=1e-5)


def test_union_retains_original_candidates_and_excludes_self_with_unique_mass():
    codes = np.array([[0, 0], [0, 1], [1, 0], [1, 1], [0, 0], [1, 1]])
    query, bank = np.array([0, 5]), np.arange(6)
    initial, learned = np.array([4., 0.]), np.array([0., 4.])
    original = parent.candidate_indices(codes, initial, query, bank, k=2)
    donors, valid = model.candidate_union(codes, initial, learned, query, bank, k=2)
    assert donors.shape == valid.shape
    assert donors.shape[1] <= 4
    for row, position in enumerate(query):
        live = donors[row, valid[row]]
        assert set(original[row]).issubset(set(live))
        assert position not in live
        assert len(live) == len(np.unique(live))
    posterior = model._masked_posterior(
        (codes[query, None] == codes[donors]).astype(float), learned, valid)
    np.testing.assert_array_equal(posterior[~valid], 0.)
    np.testing.assert_allclose(posterior.sum(axis=1), 1.)


def _evidence_case():
    frame = pd.DataFrame({
        "a": ["x", "y", "x", None],
        "b": ["y", "x", "y", None],
    })
    records = {name: {"class": "PREDICT", "values": ["x", "y"]}
               for name in frame}
    options = {name: ["x", "y"] for name in frame}
    codes = np.array([[1, 0], [0, 1], [1, 1], [1, 1]])
    query, bank = np.array([3]), np.array([0, 1, 2])
    initial = np.array([3., 0.])
    groups, active = [[0], [1]], [0]
    originals = [np.array([0., 3.]), np.ones(2)]
    args = (frame, records, ["a", "b"], options, codes, query, bank,
            initial, ["a", "b"], groups)
    return args, originals, active


def test_unselected_union_and_inactive_items_equal_parent_evidence():
    args, originals, active = _evidence_case()
    plans = [{"original": weight, "expanded": np.array([12., 0.]),
              "use_union": False} for weight in originals]
    seed = {"b": np.array([[.2, .8]])}
    expected = parent._replace_evidence(dict(seed), *args, originals, active)
    actual = model.union_evidence(dict(seed), *args, plans, active)
    assert actual.keys() == expected.keys()
    for item in actual:
        np.testing.assert_array_equal(actual[item], expected[item])


def test_selected_union_evidence_is_normalized_and_leaves_inactive_item_exact():
    args, originals, active = _evidence_case()
    plans = [{"original": weight, "expanded": np.array([12., 0.]),
              "use_union": index == 0}
             for index, weight in enumerate(originals)]
    seed = {"b": np.array([[.2, .8]])}
    actual = model.union_evidence(dict(seed), *args, plans, active)
    np.testing.assert_allclose(actual["a"].sum(axis=1), 1.)
    np.testing.assert_array_equal(actual["b"], seed["b"])


def _fit_case():
    rng = np.random.default_rng(8)
    codes = rng.integers(0, 3, (90, 3))
    labels = np.column_stack((codes[:, 0], codes[:, 1]))
    return (codes, labels, np.arange(45), np.arange(45, 65),
            np.arange(65, 80), np.ones(3), [3, 3], [[0, 1]])


def test_expanded_metric_ignores_selection_and_audit_labels(monkeypatch):
    args = _fit_case()
    fixed_weights = np.array([1.5, .5, 2.])
    fixed_diag = [{"selected": True, "new_share": .6}]
    monkeypatch.setattr(parent, "fit_sections",
                        lambda *a, **k: ([fixed_weights.copy()], [0], fixed_diag))
    first = model.fit_union_sections(*args, k=5, maxiter=12, min_gain=-1)
    changed = args[1].copy()
    changed[args[4]] = (changed[args[4]] + 1) % 3
    changed[80:] = (changed[80:] + 2) % 3
    second_args = (args[0], changed, *args[2:])
    second = model.fit_union_sections(*second_args, k=5, maxiter=12, min_gain=-1)
    np.testing.assert_array_equal(first[0][0]["expanded"], second[0][0]["expanded"])
    assert first[1] == second[1] == [0]


def test_union_layer_inherits_parent_replay_and_uses_isolated_globals():
    assert model.union_layer.__code__ is parent.supervised_layer.__code__
    assert model.union_layer.__globals__["fit_sections"] is model.fit_union_sections
    assert model.union_layer.__globals__["_replace_evidence"] is model.union_evidence
    assert model.union_layer.__globals__["LAST_DIAGNOSTICS"] is model.LAST_DIAGNOSTICS
    assert parent.supervised_layer.__globals__["fit_sections"] is parent.fit_sections
    assert parent.supervised_layer.__globals__["LAST_DIAGNOSTICS"] is parent.LAST_DIAGNOSTICS


def _layer_case():
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


def test_replay_labels_are_separate_from_union_fit_and_selection(monkeypatch):
    frame, schema, item = _layer_case()
    correct = .12 + np.arange(len(frame)) * .0001
    base_probability = np.repeat(((1 - correct) / 4)[:, None], 5, axis=1)
    base_probability[np.arange(len(frame)), np.arange(len(frame)) % 5] = correct
    base = {item: base_probability}
    probability_row = {float(value): row for row, vector in enumerate(base_probability)
                       for value in vector}
    fits, calibration_rows = [], []
    original_fit = model.fit_union_sections
    original_lambda = model.union_layer.__globals__["_best_lambda"]

    def capture_fit(codes, labels, bank, fit, select, *args, **kwargs):
        result = original_fit(codes, labels, bank, fit, select, *args, **kwargs)
        fits.append((bank.copy(), fit.copy(), select.copy(), result))
        return result

    def capture_lambda(p_model, p_evidence):
        calibration_rows.extend(probability_row[float(value)] for value in p_model)
        return original_lambda(p_model, p_evidence)

    monkeypatch.setitem(model.union_layer.__globals__, "fit_sections", capture_fit)
    monkeypatch.setitem(model.union_layer.__globals__, "_best_lambda", capture_lambda)
    model.union_layer(frame, schema, base)
    bank, fit, select, first = fits[0]
    assert first[1] == [0]
    visible = np.flatnonzero(frame[item].notna().to_numpy())
    replay = np.setdiff1d(visible, np.concatenate((bank, fit, select)))
    assert set(calibration_rows) == set(replay)

    changed = frame.copy()
    changed.loc[replay, item] = ((changed.loc[replay, item].astype(int) + 1) % 5).astype(str)
    calibration_rows.clear()
    model.union_layer(changed, schema, base)
    second = fits[1][3]
    for before, after in zip(first[0], second[0]):
        np.testing.assert_array_equal(before["original"], after["original"])
        np.testing.assert_array_equal(before["expanded"], after["expanded"])
        assert before["use_union"] == after["use_union"]
    assert first[1:] == second[1:]
    assert set(calibration_rows) == set(replay)


def test_non_unhcr_uses_exact_parent(monkeypatch):
    sentinel = object()
    calls = []
    monkeypatch.setattr(parent, "predict",
                        lambda *args, **kwargs: calls.append((args, kwargs)) or sentinel)
    assert model.predict("frame", {"items": {}}) is sentinel
    assert len(calls) == 1
