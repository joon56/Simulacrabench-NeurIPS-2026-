"""Bounded E050/E051 libraries; expensive E041 fits use fixed test products."""

from collections import Counter
import importlib

import numpy as np
import pandas as pd
import pytest


def library():
    return importlib.import_module("src.eval.recursive_candidates")


@pytest.fixture
def case():
    schema = {"gated_value": "NA_GATED", "items": {
        "given": {"class": "GIVEN", "values": ["yes", "no"]},
        "s1_parent": {"class": "PREDICT", "values": ["yes", "no"]},
        "s2_child": {"class": "PREDICT", "values": ["a", "b"],
                     "gate": {"parent": "s1_parent", "observed_if": ["yes"]}},
        "independent": {"class": "PREDICT", "values": ["a", "b"],
                        "gate": {"parent": "given", "observed_if": ["yes"]}},
        "separate": {"class": "PREDICT", "values": ["a", "b"],
                     "gate": {"parent": "given", "observed_if": ["yes"]}},
    }}
    frame = pd.DataFrame({"given": ["yes", "no"] * 30,
                          "s1_parent": ["yes", "no"] * 30,
                          "s2_child": ["a", "NA_GATED"] * 30,
                          "independent": ["b", "NA_GATED"] * 30,
                          "separate": ["a", "NA_GATED"] * 30})
    frame.loc[[58, 59], list(schema["items"])[1:]] = np.nan
    # Deliberately differ from schema order.
    return frame[list(reversed(frame.columns))], schema


@pytest.fixture
def fixed_stack(monkeypatch, case):
    from src.models import link_sharp, supervised_retrieval
    from src.models.hier_backoff import _layout
    frame, schema = case
    records, items, options = _layout(frame, schema)
    predicted = [n for n in items if records[n]["class"] == "PREDICT"]
    gated = [n for n in predicted if records[n].get("gate")]
    calls = Counter()

    def counted(name, function):
        def wrapper(*args, **kwargs):
            calls[name] += 1
            return function(*args, **kwargs)
        return wrapper

    def proba(*args):
        return ({n: np.full((len(frame), len(options[n])), 1 / len(options[n]))
                 for n in predicted},
                {n: np.full((len(frame), len(records[n]["values"])),
                            1 / len(records[n]["values"])) for n in gated})

    def layer(f, s, model_dists):
        assert f[predicted].iloc[58:].isna().all().all()
        rows = {}
        for row in [58, 59]:
            evidence = {}
            for n in predicted:
                p = np.arange(1, len(options[n]) + 1, dtype=float)
                evidence[n] = p / p.sum()
            rows[row] = (evidence, row == 59)
        return rows, {"s1_parent": (.2, .8), "s2_child": (.4, .7)}

    monkeypatch.setattr(link_sharp, "select_ladder", counted("select_ladder", lambda *a: ([], [], 0)))
    monkeypatch.setattr(link_sharp, "tune_and_train", counted("tune_and_train", lambda *a, **k: (.3, object(), (predicted, gated))))
    monkeypatch.setattr(link_sharp, "_proba_maps", counted("_proba_maps", proba))
    for name in ["build_ladder", "conditional_agreement"]:
        monkeypatch.setattr(link_sharp, name, counted(name, getattr(link_sharp, name)))
    monkeypatch.setattr(supervised_retrieval, "supervised_layer", counted("evidence", layer))
    return calls, layer


def test_predict_components_cross_sections_but_not_given_boundary(case):
    _, schema = case
    assert library().predict_components(schema) == [
        ["s1_parent", "s2_child"], ["independent"], ["separate"]]


def test_identity_exact_and_private_fits_cached_once(case, fixed_stack):
    from src.models import link_sharp, hh_cap, supervised_retrieval
    frame, schema = case
    calls, layer = fixed_stack
    original_functions = {n: getattr(link_sharp, n) for n in (
        "select_ladder", "tune_and_train", "_proba_maps", "build_ladder", "conditional_agreement")}
    result = library().e050_library(frame, schema)
    assert calls == Counter(select_ladder=1, tune_and_train=1, _proba_maps=1,
                            build_ladder=7, conditional_agreement=1, evidence=1)
    assert all(getattr(link_sharp, n) is f for n, f in original_functions.items())
    expected = link_sharp.predict(frame, schema, layer_fn=layer, configs=hh_cap.CONFIGS)
    for actual, direct in zip(result["base_raw"], expected):
        np.testing.assert_array_equal(actual, direct)
    assert result["arms_raw"]["identity"] is result["base_raw"]
    assert list(result["arms"]) == ["identity", "zero", "half", "toward_one", "one"]
    np.testing.assert_array_equal(result["query"], [58, 59])
    # A second frame gets fresh private caches.
    calls.clear()
    library().e050_library(frame.copy(), schema)
    assert calls["tune_and_train"] == calls["evidence"] == 1


def test_component_composition_matches_full_mixed_recursive_render(case, fixed_stack):
    from src.models import hh_cap
    frame, schema = case
    _, layer = fixed_stack
    lib = library()
    result = lib.e050_library(frame, schema)
    choices = {"s1_parent": "one", "s2_child": "one",
               "independent": "zero", "separate": "half"}
    evidence, shares = layer(frame, schema, {})
    mixed = lib.transform_lambdas(evidence, shares, choices)
    direct = lib.cached_renderer()(frame, schema,
        layer_fn=lambda *a: (evidence, mixed), configs=hh_cap.CONFIGS)
    for i, item in enumerate(result["predicted"]):
        np.testing.assert_array_equal(np.stack(direct[i::4]), result["arms"][choices[item]][item])
    # Parent intervention really propagated into a differently named section.
    assert not np.array_equal(result["arms"]["zero"]["s2_child"], result["arms"]["one"]["s2_child"])


def test_missing_lambda_both_buckets_and_no_dormant_evidence():
    lib = library()
    rows = {3: ({"present": np.array([1., 0.]), "missing": np.array([0., 1.])}, False)}
    shares = {"present": (.2, .8), "dormant": (.5, .5)}
    assert lib.transform_lambdas(rows, shares, "half") == {"present": (.1, .4), "missing": (0., 0.)}
    increased = lib.transform_lambdas(rows, shares, "toward_one")
    assert increased["present"] == pytest.approx((.6, .9))
    assert increased["missing"] == (.5, .5)
    assert lib.transform_lambdas({}, shares, "one") == {}


def test_absent_evidence_keeps_every_arm_exact(case, fixed_stack, monkeypatch):
    from src.models import supervised_retrieval
    monkeypatch.setattr(supervised_retrieval, "supervised_layer", lambda *a: ({}, {}))
    result = library().e050_library(*case)
    for arm in result["arms_raw"].values():
        for actual, base in zip(arm, result["base_raw"]):
            np.testing.assert_array_equal(actual, base)


def test_whole_block_masking_is_label_blind(case, fixed_stack):
    frame, schema = case
    lib = library()
    one, two = frame.copy(), frame.copy()
    one.loc[[58, 59], "s1_parent"] = "yes"
    two.loc[[58, 59], "s1_parent"] = "no"
    one = lib.mask_query(one, schema, [58, 59])
    two = lib.mask_query(two, schema, [58, 59])
    pd.testing.assert_frame_equal(one, two)
    first, second = lib.e050_library(one, schema), lib.e050_library(two, schema)
    for name in first["arms"]:
        for item in first["predicted"]:
            np.testing.assert_array_equal(first["arms"][name][item], second["arms"][name][item])
    partially_visible = frame.copy()
    partially_visible.loc[58, "s1_parent"] = "yes"
    with pytest.raises(ValueError, match="whole PREDICT"):
        lib.e050_library(partially_visible, schema)


def test_direct_tree_complete_class_mapping_singleton_and_marginal_floor():
    lib = library()
    schema = {"gated_value": "NA_GATED", "items": {
        "given": {"class": "GIVEN", "values": ["x", "y"]},
        "binary": {"class": "PREDICT", "values": ["unseen", "left", "right"]},
        "singleton": {"class": "PREDICT", "values": ["unseen", "only"]},
    }}
    frame = pd.DataFrame({"given": ["x", "y"] * 60 + ["x", "y"],
                          "binary": ["left", "right"] * 60 + [np.nan] * 2,
                          "singleton": ["only"] * 120 + [np.nan] * 2})
    tree, diagnostics = lib.direct_tree(frame, schema)
    np.testing.assert_allclose(tree["singleton"], np.tile([.01 / 122, .99 + .01 * 121 / 122], (2, 1)))
    np.testing.assert_allclose(tree["binary"][:, 0], .01 / 123)
    assert tree["binary"][0, 1] > tree["binary"][0, 2]
    assert tree["binary"][1, 2] > tree["binary"][1, 1]
    assert diagnostics["fit_rows"] == 120
    assert diagnostics["categorical_features"] == [True]
    assert diagnostics["ordinal_features"] == []
    base = {"binary": np.full((2, 3), 1 / 3), "singleton": np.full((2, 2), .5)}
    raw = [base[n][r] for r in range(2) for n in base]
    frozen = {"base": base, "base_raw": raw, "query": np.array([120, 121]),
              "predicted": list(base), "components": [[n] for n in base]}
    result = lib.e051_library(frame, schema, frozen)
    assert result["arms_raw"]["tree_0"] is raw
    np.testing.assert_allclose(result["arms"]["tree_0.5"]["binary"], .5 * base["binary"] + .5 * tree["binary"])


def test_oracle_pools_component_and_rows_not_query_hindsight():
    lib = library()
    identity = {"a": np.array([[.9, .1], [.1, .9]]), "b": np.array([[.9, .1], [.1, .9]])}
    other = {"a": identity["a"][::-1], "b": identity["b"][::-1]}
    labels = {"a": np.array([0, 0]), "b": np.array([0, 0])}
    result = lib.component_oracle({"identity": identity, "other": other}, labels, [["a", "b"]])
    assert result["delta_skill"] == pytest.approx(0)
    assert result["choices"] == ["identity"]
    assert result["base_log_score"] == pytest.approx(np.log([.001 + .998 * .9, .001 + .998 * .1]).mean())


def test_adult_adapter_strings_public_values_and_no_gates():
    screen = importlib.import_module("scripts.screen_e050_e051")
    from tests.e041_external import GIVEN, TARGETS
    observed = pd.DataFrame({n: ["alpha", "beta"] for n in GIVEN + TARGETS})
    frame, schema = screen.adapt_adult(observed)
    pd.testing.assert_frame_equal(frame, observed)
    assert schema["gated_value"] == "NA_GATED"
    assert all(r["values"] == ["alpha", "beta"] and "gate" not in r and "options" not in r
               for r in schema["items"].values())


def test_oracle_screen_freezes_all_queries_before_scoring_only_oracle(tmp_path, monkeypatch):
    import hashlib
    import json
    import pickle
    screen = importlib.import_module("scripts.screen_e050_e051")
    schema = {"gated_value": "NA_GATED", "items": {
        "given": {"class": "GIVEN", "values": ["x"]},
        "answer": {"class": "PREDICT", "values": ["a", "b"]}}}
    frame = pd.DataFrame({"given": ["x"] * 2401, "answer": ["a"] + [np.nan] * 2400})
    base = np.tile([.6, .4], (2400, 1))
    # Deliberately extreme non-oracle predictions must never affect the bound.
    alternate = base.copy()
    alternate[800:] = [0., 1.]
    frozen = {"arms": {"identity": {"answer": base}, "other": {"answer": alternate}},
              "components": [["answer"]], "diagnostics": {}}
    labels = {"answer": np.zeros(800, dtype=int)}
    monkeypatch.setattr(screen, "prepare_case", lambda *a: (frame, schema, labels, np.arange(800), {}))
    monkeypatch.setattr(screen, "e050_library", lambda *a: frozen)
    monkeypatch.setattr(screen, "e051_library", lambda *a: frozen)
    original = screen.component_oracle
    calls = []

    def inspect_oracle(arms, supplied_labels, components):
        assert supplied_labels is labels
        assert all(len(p) == 800 for heads in arms.values() for p in heads.values())
        payload = (tmp_path / "adult-seed51-libraries.pkl").read_bytes()
        manifest = json.loads((tmp_path / "adult-seed51-manifest.json").read_text())
        assert hashlib.sha256(payload).hexdigest() == manifest["library_sha256"]
        assert len(pickle.loads(payload)["E050"]["arms"]["identity"]["answer"]) == 2400
        calls.append(True)
        return original(arms, supplied_labels, components)

    monkeypatch.setattr(screen, "component_oracle", inspect_oracle)
    result = screen.run(output_dir=tmp_path)
    assert len(calls) == 2
    assert not result["selection_or_audit_evaluated"]
    assert all(r["delta_skill"] == 0 for r in result["families"].values())
    # A matching frozen artifact is reused without refitting.
    monkeypatch.setattr(screen, "e050_library", lambda *a: pytest.fail("refit on cache hit"))
    assert screen.run(output_dir=tmp_path) == result


def test_oversized_given_vocabulary_is_explicit_ordinal():
    lib = library()
    schema = {"gated_value": "NA_GATED", "items": {
        "large": {"class": "GIVEN", "values": [str(i) for i in range(256)]},
        "answer": {"class": "PREDICT", "values": ["a", "b"]}}}
    frame = pd.DataFrame({"large": ["1", "255"], "answer": ["a", np.nan]})
    _, diagnostics = lib.direct_tree(frame, schema)
    assert diagnostics["categorical_features"] == [False]
    assert diagnostics["ordinal_features"] == ["large"]
