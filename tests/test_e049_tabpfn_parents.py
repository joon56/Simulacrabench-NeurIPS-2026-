"""E049 masking, frozen renderer reuse, root interventions and exact fallbacks."""

from collections import Counter
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


def _model():
    assert importlib.util.find_spec("src.models.adaptive_tabpfn_parents") is not None
    from src.models import adaptive_tabpfn_parents
    return adaptive_tabpfn_parents


def _case(n=8000, held=2):
    roots = ["s3_11_intent_return_12m_lbl", "root_b", "root_c", "root_d"]
    records = {"given": {"class": "GIVEN", "values": ["x", "y"]}}
    for root in roots:
        records[root] = {"class": "PREDICT", "values": ["0", "1", "2"]}
        records[root + "_child"] = {
            "class": "PREDICT", "values": ["0", "1"],
            "gate": {"parent": root, "observed_if": ["1"]}}
        records[root + "_grandchild"] = {
            "class": "PREDICT", "values": ["0", "1"],
            "gate": {"parent": root + "_child", "observed_if": ["1"]}}
    records["other"] = {"class": "PREDICT", "values": ["0", "1"]}
    schema = {"gated_value": "NA_GATED", "items": records}
    frame = pd.DataFrame({name: np.where(np.arange(n + held) % 2, "1", "0")
                          for name in records})
    frame["given"] = np.where(np.arange(n + held) % 2, "y", "x")
    frame.loc[n:, list(records)[1:]] = np.nan
    return frame, schema, roots


def test_shadow_masks_all_outer_labels_and_keeps_reference_shuffle_order():
    model = _model()
    frame, schema, _ = _case()
    before = frame.copy(deep=True)
    shadow, visible, fit, select, audit, reference = model.e049_shadow_split(frame, schema)
    expected = np.random.default_rng(4901).permutation(8000)
    outer = np.concatenate((fit, select, audit))
    assert [len(x) for x in (fit, select, audit)] == [800, 600, 400]
    np.testing.assert_array_equal(outer, expected[:1800])
    np.testing.assert_array_equal(reference, expected[1800:2312])
    np.testing.assert_array_equal(visible, np.arange(8000))
    assert not np.intersect1d(reference, outer).size
    assert shadow.iloc[outer, 1:].isna().all().all()
    assert shadow.iloc[reference, 1:].notna().all().all()
    assert len(shadow) == 8000
    pd.testing.assert_frame_equal(before, frame)


def test_roots_rank_direct_children_schema_ties_and_require_disjoint_closures():
    model = _model()
    frame, schema, roots = _case(10)
    # Parent/child ties would select overlapping closures in this fixture.
    assert model.e049_groups(frame, schema) == ([], [])
    for root in roots:
        schema["items"][root + "_extra"] = {
            "class": "PREDICT", "values": ["0", "1"],
            "gate": {"parent": root, "observed_if": ["1"]}}
    chosen, groups = model.e049_groups(frame, schema)
    assert chosen == roots
    assert groups[0] == [roots[0], roots[0] + "_child", roots[0] + "_grandchild",
                         roots[0] + "_extra"]
    schema["items"][roots[0]]["values"] = list(map(str, range(11)))
    chosen, _ = model.e049_groups(frame, schema)
    assert roots[0] not in chosen


def _disjoint_case(n=8000, held=2):
    frame, schema, roots = _case(n, held)
    for root in roots:
        # Make the four top direct-child counts strictly beat their children.
        name = root + "_extra"
        schema["items"][name] = {"class": "PREDICT", "values": ["0", "1"],
                                  "gate": {"parent": root, "observed_if": ["1"]}}
        frame[name] = frame[root + "_child"]
    return frame, schema, roots


def test_gated_root_schema_limit_counts_sentinel():
    model = _model()
    frame, schema, roots = _disjoint_case(10)
    root = roots[0]
    schema["items"][root]["gate"] = {"parent": "given", "observed_if": ["x"]}
    schema["items"][root]["values"] = list(map(str, range(10)))
    chosen, _ = model.e049_groups(frame, schema)
    assert root not in chosen
    schema["items"][root]["values"] = list(map(str, range(9)))
    chosen, _ = model.e049_groups(frame, schema)
    assert root in chosen


def test_root_ranking_counts_only_predicted_children():
    model = _model()
    frame, schema, roots = _disjoint_case(10)
    for index in range(3):
        schema["items"][f"given_child_{index}"] = {
            "class": "GIVEN", "values": ["0", "1"],
            "gate": {"parent": roots[0] + "_child", "observed_if": ["1"]}}
    chosen, _ = model.e049_groups(frame, schema)
    assert chosen == roots


@pytest.mark.parametrize("kind", ["control", "small", "partial", "overlap", "noheld"])
def test_fallback_calls_exact_parent_with_original_arguments(monkeypatch, kind):
    model = _model()
    frame, schema, roots = _disjoint_case(600 if kind == "small" else 8000,
                                          0 if kind == "noheld" else 2)
    if kind == "control":
        schema["items"].pop(roots[0])
    if kind == "partial":
        frame.loc[len(frame) - 1, "other"] = "0"
    if kind == "overlap":
        frame, schema, roots = _case()
    sentinel = object()
    calls = []
    monkeypatch.setattr(model.parent, "predict", lambda *a, **kw: calls.append((a, kw)) or sentinel)
    assert model.predict(frame, schema, cols=["given"], kappas=[3]) is sentinel
    assert len(calls) == 1 and calls[0][0][0] is frame and calls[0][0][1] is schema
    assert calls[0][1] == {"cols": ["given"], "kappas": [3]}


def test_pfn_uses_only_given_maps_missing_classes_and_skips_single_class(monkeypatch):
    model = _model()
    frame, schema, roots = _disjoint_case(512)
    frame.loc[:511, roots[1:]] = "0"
    reference, query = np.arange(512), np.arange(512, 514)
    fits = []

    class Classifier:
        classes_ = np.array([1, 0])

        def fit(self, x, y):
            fits.append((x.copy(), y.copy()))

        def predict_proba(self, x):
            assert x.shape == (2, 1)
            return np.tile([.7, .3], (len(x), 1))

    def create(version, **kwargs):
        assert kwargs["model_path"] is model.E049_V2_SPEC
        assert kwargs["categorical_features_indices"] == [0]
        assert (kwargs["n_estimators"], kwargs["n_jobs"], kwargs["random_state"], kwargs["device"]) == (1, 1, 0, "cpu")
        return Classifier()

    monkeypatch.setattr(model.TabPFNClassifier, "create_default_for_version", create)
    result = model.e049_tabpfn(frame, schema, roots, reference, query)
    assert list(result) == roots[:1]
    np.testing.assert_array_equal(result[roots[0]], [[.3, .7, 0], [.3, .7, 0]])
    assert fits[0][0].shape == (512, 1)
    np.testing.assert_array_equal(fits[0][0][:, 0], np.arange(512) % 2)
    with pytest.raises(ValueError, match="reference"):
        model.e049_tabpfn(frame, schema, roots, np.arange(1, 513), query)


def _cheap_renderer(monkeypatch, model):
    calls = Counter()
    original_build = model.link_sharp.build_ladder

    def select(*args):
        calls["select"] += 1
        return [], [], 0

    def tune(frame, schema, *args, **kwargs):
        calls["train"] += 1
        predicted = [n for n, r in schema["items"].items() if r["class"] == "PREDICT"]
        return .2, object(), (predicted, [n for n in predicted if schema["items"][n].get("gate")])

    def maps(net, x, predicted, gated):
        calls["maps"] += 1
        return ({n: np.tile([.1, .6, .3] if n != "other" else [.8, .2], (len(x), 1)) for n in predicted},
                {n: np.tile([.2, .8], (len(x), 1)) for n in gated})

    def build(*args, **kwargs):
        calls[("build", args[1], tuple(args[2]))] += 1
        return original_build(*args, **kwargs)

    def agreement(frame, schema):
        calls["agreement"] += 1
        return {n: (.65, None, {}) for n, r in schema["items"].items() if r.get("gate")}

    def layer(frame, schema, dists):
        calls["evidence"] += 1
        predicted = [n for n, r in schema["items"].items() if r["class"] == "PREDICT"]
        held = np.flatnonzero(frame[predicted].isna().any(axis=1))
        # Second held row has no E041 evidence at all.
        ev = {n: np.array([.6, .2, .2] if n != "other" else [.3, .7]) for n in predicted}
        return {held[0]: (ev, True)}, {n: (.1, .35) for n in predicted}

    for name, value in (("select_ladder", select), ("tune_and_train", tune),
                        ("_proba_maps", maps), ("build_ladder", build),
                        ("conditional_agreement", agreement)):
        monkeypatch.setattr(model.link_sharp, name, value)
    monkeypatch.setattr(model.parent, "supervised_layer", layer)
    return calls


def test_cached_renderer_trains_once_without_module_mutation_and_is_linear(monkeypatch):
    model = _model()
    frame, schema, roots = _disjoint_case(12)
    calls = _cheap_renderer(monkeypatch, model)
    before = dict(vars(model.link_sharp))
    render = model.e049_cached_renderer()
    output = render(frame, schema, layer_fn=model.parent.supervised_layer, configs=model.hh_cap.CONFIGS)
    predicted = [n for n, r in schema["items"].items() if r["class"] == "PREDICT"]
    base = {n: np.stack(output[j::len(predicted)]) for j, n in enumerate(predicted)}
    query = np.array([12, 13])
    ev_rows, shares = model.parent.supervised_layer(frame, schema, {})
    candidate_roots = {n: np.tile([.8, .1, .1], (2, 1)) for n in roots}
    candidate_layer = model.e049_root_layer(ev_rows, shares, candidate_roots, query)
    candidate = render(frame, schema, layer_fn=lambda *a: candidate_layer, configs=model.hh_cap.CONFIGS)
    # Distinct per-root, per-query alpha tests independent descendant closures.
    alphas = {n: np.array([.15 + j * .05, .45 - j * .05])[:, None] for j, n in enumerate(roots)}
    mixed_roots = {n: (1 - alphas[n]) * base[n] + alphas[n] * candidate_roots[n] for n in roots}
    direct_layer = model.e049_root_layer(ev_rows, shares, mixed_roots, query)
    direct = render(frame, schema, layer_fn=lambda *a: direct_layer, configs=model.hh_cap.CONFIGS)
    _, groups = model.e049_groups(frame, schema)
    for row in range(2):
        for col, name in enumerate(predicted):
            index = row * len(predicted) + col
            root = next((root for root, group in zip(roots, groups) if name in group), None)
            alpha = alphas[root][row, 0] if root else 0
            np.testing.assert_allclose(direct[index], (1 - alpha) * output[index] + alpha * candidate[index], atol=1e-12)
    for key, count in calls.items():
        assert count == (2 if key == "evidence" else 1)
    assert vars(model.link_sharp).keys() == before.keys()
    assert all(vars(model.link_sharp)[key] is value for key, value in before.items())
    assert roots[0] not in ev_rows.get(13, ({}, False))[0]
    assert shares[roots[0]] == (.1, .35)


def test_capture_exact_e041_base_and_one_evidence_fit(monkeypatch):
    model = _model()
    frame, schema, roots = _disjoint_case(512)
    calls = _cheap_renderer(monkeypatch, model)
    expected = model.parent.predict(frame, schema)
    calls.clear()
    monkeypatch.setattr(model, "e049_tabpfn", lambda *a: {roots[0]: np.tile([.8, .1, .1], (2, 1))})
    output, base, candidate, query = model.e049_capture(frame, schema, roots, np.arange(512))
    assert calls["train"] == calls["evidence"] == calls["maps"] == 1
    assert set(base) == set(candidate)
    np.testing.assert_array_equal(query, [512, 513])
    for actual, previous in zip(output, expected):
        np.testing.assert_array_equal(actual, previous)
    np.testing.assert_array_equal(candidate[roots[0]], [[.8, .1, .1]] * 2)
    np.testing.assert_array_equal(candidate[roots[1]], base[roots[1]])


def test_public_active_path_hides_outer_labels_freezes_policies_then_refits(monkeypatch):
    model = _model()
    frame, schema, roots = _disjoint_case(8000)
    captures = []
    policy = {"center": [0.] * 7, "scale": [1.] * 7, "beta": [0.] * 7}

    def capture(f, s, selected, reference, **kwargs):
        captures.append((f.copy(deep=True), reference.copy()))
        predicted = [n for n, r in s["items"].items() if r["class"] == "PREDICT"]
        query = np.flatnonzero(f[predicted].isna().any(axis=1))
        assert not np.intersect1d(reference, query).size
        base = {n: np.tile([.4, .6] if n == "other" else [.1, .2, .7], (len(query), 1)) for n in predicted}
        candidate = {n: np.tile([.4, .6] if n == "other" else [.7, .2, .1], (len(query), 1)) for n in predicted}
        return [base[n][i] for i in range(len(query)) for n in predicted], base, candidate, query

    def fit(base, candidate, labels, groups, correction, selection, audit):
        assert len(captures) == 1
        assert len(captures[0][0]) == 8000
        assert captures[0][0].iloc[:, 1:].isna().any(axis=1).sum() == 1800
        assert [len(part) for part in (correction, selection, audit)] == [800, 600, 400]
        assert labels[roots[0]].shape == (1800,)
        return {0: policy}, {"accepted_test": True}

    monkeypatch.setattr(model, "e049_capture", capture)
    monkeypatch.setattr(model, "e047_fit_policies", fit)
    actual = model.predict(frame, schema)
    assert len(captures) == 2
    pd.testing.assert_frame_equal(captures[1][0], frame)
    np.testing.assert_array_equal(captures[1][1], np.random.default_rng(4901).permutation(8000)[:512])
    predicted = [n for n, r in schema["items"].items() if r["class"] == "PREDICT"]
    assert len(actual) == 2 * len(predicted)
    _, groups = model.e049_groups(frame, schema)
    for i, values in enumerate(actual):
        name = predicted[i % len(predicted)]
        expected = [.25, .2, .55] if name in groups[0] else ([.4, .6] if name == "other" else [.1, .2, .7])
        np.testing.assert_allclose(values, expected, atol=1e-15)
    assert np.all(model.e047_alpha(policy, np.ones((2, 7))) <= .5)


def test_rejected_policy_returns_exact_parent(monkeypatch):
    model = _model()
    frame, schema, roots = _disjoint_case(800)
    predicted = [n for n, r in schema["items"].items() if r["class"] == "PREDICT"]

    def capture(f, *args, **kwargs):
        query = np.flatnonzero(f[predicted].isna().any(axis=1))
        base = {n: np.tile([.4, .6] if n == "other" else [.1, .2, .7], (len(query), 1)) for n in predicted}
        return [], base, base, query

    sentinel = object()
    monkeypatch.setattr(model, "e049_capture", capture)
    monkeypatch.setattr(model, "e047_fit_policies", lambda *args: ({}, {"rejected": True}))
    monkeypatch.setattr(model.parent, "predict", lambda *args, **kwargs: sentinel)
    assert model.predict(frame, schema) is sentinel


def test_singleton_final_root_keeps_exact_raw_base_even_with_frozen_policy(monkeypatch):
    model = _model()
    frame, schema, roots = _disjoint_case(800)
    predicted = [n for n, r in schema["items"].items() if r["class"] == "PREDICT"]
    policy = {"center": [0.] * 7, "scale": [1.] * 7, "beta": [0.] * 7}
    outputs = []

    def capture(f, *args, **kwargs):
        query = np.flatnonzero(f[predicted].isna().any(axis=1))
        base = {n: np.tile([.4, .6] if n == "other" else [.1, .2, .7000001], (len(query), 1)) for n in predicted}
        output = [base[n][i] for i in range(len(query)) for n in predicted]
        outputs.append(output)
        # Other roots can have PFN predictions while selected root has a singleton.
        candidate = {n: values.copy() for n, values in base.items()}
        candidate[roots[1]][:] = [.8, .1, .1]
        return output, base, candidate, query

    monkeypatch.setattr(model, "e049_capture", capture)
    monkeypatch.setattr(model, "e047_fit_policies", lambda *args: ({0: policy}, {}))
    actual = model.predict(frame, schema)
    for values, expected in zip(actual, outputs[-1]):
        np.testing.assert_array_equal(values, expected)
