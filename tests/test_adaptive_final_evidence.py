"""E047 final-mixture objective, honest partitions and source integration."""

import json

import numpy as np
import pandas as pd
import pytest
from scipy.optimize._numdiff import approx_derivative

from src.models import adaptive_final_evidence as model


def test_gradient_matches_finite_differences_and_official_floor():
    rng = np.random.default_rng(47)
    features = np.column_stack((np.ones(13), rng.normal(size=(13, 6))))
    beta = rng.normal(size=7)
    base, evidence = rng.uniform(.02, .8, (2, 13, 3))
    sizes = np.array([2, 3, 5])
    loss, gradient = model.e047_objective(beta, features, base, evidence, sizes)
    numeric = approx_derivative(
        lambda b: model.e047_objective(b, features, base, evidence, sizes)[0], beta)
    np.testing.assert_allclose(gradient, numeric.ravel(), atol=1e-7, rtol=1e-5)
    alpha = .5 / (1 + np.exp(-features @ beta))
    expected = -np.log(.001 + (1 - .001 * sizes) * (
        (1 - alpha[:, None]) * base + alpha[:, None] * evidence)).mean()
    expected += .01 * np.mean(beta[1:] ** 2)
    assert loss == pytest.approx(expected, abs=1e-12)


def test_features_normalize_raw_vectors_and_missing_evidence():
    base = {"a": np.array([[2., 0.], [1., 1.]]),
            "b": np.array([[0., 3.], [0., 2.]])}
    evidence = {"a": np.array([[0., 4.], [1., 1.]])}
    features = model.e047_features(base, evidence, ["a", "b"])
    np.testing.assert_allclose(features, [[1, 0, 0, 1, 1, .5, .5],
                                         [1, .5, .5, .75, .75, .75, 1]])


def test_constant_features_stable_fit_and_serializable_policy():
    features = np.ones((40, 7))
    policy = model.e047_fit_section(features, np.full((40, 1), .2),
                                   np.full((40, 1), .9), [2])
    json.dumps(policy, allow_nan=False)
    np.testing.assert_array_equal(policy["center"], [0, 1, 1, 1, 1, 1, 1])
    np.testing.assert_array_equal(policy["scale"], [1, .001, .001, .001, .001, .001, .001])
    alpha = model.e047_alpha(policy, features)
    assert np.isfinite(alpha).all()
    assert np.all((alpha > .45) & (alpha < .5))


def _policy_case():
    base = {"a": np.tile([.2, .8], (90, 1)),
            "b": np.tile([.5, .5], (90, 1))}
    evidence = {"a": np.tile([.9, .1], (90, 1))}
    labels = {"a": np.zeros(90, dtype=int), "b": np.zeros(90, dtype=int)}
    return base, evidence, labels, [["a"], ["b"]], np.arange(30), np.arange(30, 60), np.arange(60, 90)


def test_selection_and_audit_labels_never_enter_fit(monkeypatch):
    args = _policy_case()
    fitted = []
    original = model.e047_fit_section

    def capture(*values):
        result = original(*values)
        fitted.append(result)
        return result

    monkeypatch.setattr(model, "e047_fit_section", capture)
    policies, first = model.e047_fit_policies(*args)
    assert list(policies) == [0]
    fit_before = fitted.copy()
    fitted.clear()
    changed = {name: labels.copy() for name, labels in args[2].items()}
    changed["a"][args[6]] = 1
    rejected, second = model.e047_fit_policies(args[0], args[1], changed, *args[3:])
    assert not rejected
    assert fitted == fit_before
    assert first["sections"] == second["sections"]
    assert first["audit"]["accepted"]
    assert not second["audit"]["accepted"]
    assert second["audit"]["gain_log"] < 0
    fitted.clear()
    changed["a"][args[5]] = 1
    selected, _ = model.e047_fit_policies(args[0], args[1], changed, *args[3:])
    assert not selected
    assert fitted == fit_before


def test_disjoint_nonempty_partitions_required():
    args = _policy_case()
    with pytest.raises(ValueError, match="disjoint"):
        model.e047_fit_policies(*args[:4], [0, 1], [1, 2], [3, 4])
    with pytest.raises(ValueError, match="nonempty"):
        model.e047_fit_policies(*args[:4], [], [1, 2], [3, 4])


def test_apply_preserves_raw_inactive_vectors_and_normalizes_active_once():
    base = {"a": np.array([[2., 0.]]), "b": np.array([[2., 3.]])}
    evidence = {"a": np.array([[0., 4.]])}
    policy = {"center": [0.] * 7, "scale": [1.] * 7, "beta": [0.] * 7}
    changed = model.e047_apply(base, evidence, [["a"], ["b"]], {0: policy})
    np.testing.assert_array_equal(changed["a"], [[.75, .25]])
    np.testing.assert_array_equal(changed["b"], base["b"])
    assert not np.shares_memory(changed["b"], base["b"])
    for actual in (model.e047_apply(base, evidence, [["a"]], {}),
                   model.e047_apply(base, {}, [["a"]], {0: policy})):
        for item in base:
            np.testing.assert_array_equal(actual[item], base[item])


def _frame_case(visible=4000, partial=False):
    item = "s3_11_intent_return_12m_lbl"
    frame = pd.DataFrame({"given": np.arange(visible + 2).astype(str),
                          "s4_item": "0", item: "0"})
    frame.loc[visible:, ["s4_item", item]] = np.nan
    if partial:
        frame.loc[visible, "s4_item"] = "0"
    schema = {"gated_value": "NA_GATED", "items": {
        "given": {"class": "GIVEN", "values": frame["given"].tolist()},
        item: {"class": "PREDICT", "values": ["0", "1"]},
        "s4_item": {"class": "PREDICT", "values": ["0", "1"]}}}
    return frame, schema, item


def test_shadow_masks_every_correction_row_and_excludes_original_held():
    frame, schema, item = _frame_case(8000)
    before = frame.copy(deep=True)
    shadow, visible, fit, select, audit = model.e047_shadow_split(frame, schema)
    assert len(shadow) == 8000
    np.testing.assert_array_equal(visible, np.arange(8000))
    assert [len(part) for part in (fit, select, audit)] == [800, 600, 400]
    correction = np.concatenate((fit, select, audit))
    assert len(np.unique(correction)) == len(correction)
    assert shadow.loc[correction, [item, "s4_item"]].isna().all().all()
    retained = np.setdiff1d(np.arange(8000), correction)
    assert shadow.loc[retained, [item, "s4_item"]].notna().all().all()
    np.testing.assert_array_equal(correction, np.random.default_rng(4701).permutation(8000)[:1800])
    pd.testing.assert_frame_equal(frame, before)


@pytest.mark.parametrize("kind", ["control", "small", "partial"])
def test_controls_small_and_partial_held_use_exact_parent(monkeypatch, kind):
    frame, schema, item = _frame_case(3999 if kind == "small" else 4000, kind == "partial")
    if kind == "control":
        schema["items"]["control"] = schema["items"].pop(item)
    sentinel = object()
    calls = []
    monkeypatch.setattr(model.parent, "predict", lambda *a, **kw: calls.append(kw) or sentinel)
    assert model.predict(frame, schema, cols=["given"], kappas=[3]) is sentinel
    assert calls == [{"cols": ["given"], "kappas": [3]}]


def test_capture_uses_parent_layer_and_schema_output_order(monkeypatch):
    frame, schema, item = _frame_case(2)
    sentinel = [np.array([2., 3.]), np.array([4., 1.]),
                np.array([1., 4.]), np.array([3., 2.])]
    calls = []

    def layer(f, s, d):
        calls.append("layer")
        return {2: ({item: np.array([.9, .1])}, False)}, {item: (.1, .2)}

    def first_stage(f, s, **kw):
        assert kw["configs"] is model.hh_cap.CONFIGS
        assert kw["layer_fn"](f, s, {})[1] == {item: (.1, .2)}
        return sentinel

    monkeypatch.setattr(model.parent, "supervised_layer", layer)
    monkeypatch.setattr(model.link_sharp, "predict", first_stage)
    output, base, evidence, held = model.e047_capture(frame, schema)
    assert output is sentinel
    assert calls == ["layer"]
    np.testing.assert_array_equal(held, [2, 3])
    np.testing.assert_array_equal(base[item], [[2, 3], [1, 4]])
    np.testing.assert_array_equal(base["s4_item"], [[4, 1], [3, 2]])
    np.testing.assert_array_equal(evidence[item], [[.9, .1], [1, 4]])
    assert "s4_item" not in evidence


def test_predict_masks_shadow_before_fit_then_applies_after_final_parent(monkeypatch):
    frame, schema, item = _frame_case()
    captures = []
    policy = {"center": [0.] * 7, "scale": [1.] * 7, "beta": [0.] * 7}

    def capture(f, s, **kw):
        captures.append(f.copy(deep=True))
        held = np.flatnonzero(f[item].isna().to_numpy())
        base = {name: np.tile([2., 0.], (len(held), 1)) for name in (item, "s4_item")}
        evidence = {item: np.tile([0., 1.], (len(held), 1))}
        output = [base[name][row] for row in range(len(held)) for name in (item, "s4_item")]
        return output, base, evidence, held

    def policies(base, evidence, labels, groups, fit, select, audit):
        assert len(captures) == 1
        assert len(captures[0]) == 4000
        assert captures[0][item].isna().sum() == 1200
        assert [len(part) for part in (fit, select, audit)] == [400, 400, 400]
        assert len(set(np.concatenate((fit, select, audit)))) == 1200
        assert len(labels[item]) == 1200 and np.all(labels[item] == 0)
        return {0: policy}, {"test": True}

    monkeypatch.setattr(model, "e047_capture", capture)
    monkeypatch.setattr(model, "e047_fit_policies", policies)
    actual = model.predict(frame, schema)
    assert len(captures) == 2
    pd.testing.assert_frame_equal(captures[1], frame)
    for row in range(2):
        np.testing.assert_array_equal(actual[2 * row], [.75, .25])
        np.testing.assert_array_equal(actual[2 * row + 1], [2., 0.])


@pytest.mark.parametrize("has_evidence", [False, True])
def test_source_rejection_or_missing_evidence_returns_parent_object(monkeypatch, has_evidence):
    frame, schema, item = _frame_case()
    calls = []
    sentinel = object()

    def capture(f, s, **kw):
        calls.append("shadow")
        held = np.flatnonzero(f[item].isna().to_numpy())
        base = {name: np.tile([.5, .5], (len(held), 1)) for name in (item, "s4_item")}
        return [], base, {item: base[item]} if has_evidence else {}, held

    monkeypatch.setattr(model, "e047_capture", capture)
    monkeypatch.setattr(model, "e047_fit_policies", lambda *a: ({}, {"rejected": True}))
    monkeypatch.setattr(model.parent, "predict", lambda *a, **kw: calls.append("parent") or sentinel)
    assert model.predict(frame, schema) is sentinel
    assert calls == ["shadow", "parent"]
