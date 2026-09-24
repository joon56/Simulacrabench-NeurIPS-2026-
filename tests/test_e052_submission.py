"""E052 dispatch, pre-fit boundaries, and immutable standalone packaging."""

import ast
import hashlib
import importlib
from pathlib import Path
import types
import zipfile

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
MARKER = "s3_11_intent_return_12m_lbl"


def source():
    assert (ROOT / "src/models/evidence_after_gates.py").exists(), "E052 wrapper missing"
    return importlib.import_module("src.models.evidence_after_gates")


def assembler():
    assert (ROOT / "scripts/assemble_e052.py").exists(), "E052 assembler missing"
    return importlib.import_module("scripts.assemble_e052")


@pytest.fixture
def case():
    schema = {"gated_value": "NA_GATED", "items": {
        "given": {"class": "GIVEN", "values": ["yes", "no"]},
        MARKER: {"class": "PREDICT", "values": ["yes", "no"]},
        "child": {"class": "PREDICT", "values": ["yes", "no"],
                  "gate": {"parent": MARKER, "observed_if": ["yes"]}},
    }}
    frame = pd.DataFrame({"given": ["yes", "no"], MARKER: ["yes", np.nan],
                          "child": ["no", np.nan]})
    return frame, schema


@pytest.mark.parametrize("name", ["unicef", "wb", "ordinary"])
def test_non_unhcr_returns_exact_e041_result_and_arguments(case, monkeypatch, name):
    model = source()
    frame, schema = case
    schema["items"][name] = schema["items"].pop(MARKER)
    original = [np.array([2., 3.])]
    cols, kappas = ["given"], [3.]
    calls = []

    def incumbent(f, s, **kwargs):
        calls.append((f is frame, s is schema, kwargs))
        return original

    monkeypatch.setattr(model.supervised_retrieval, "predict", incumbent)
    monkeypatch.setattr(model, "routing_library", lambda *a: pytest.fail("non-UNHCR routing"))
    assert model.predict(frame, schema, cols=cols, kappas=kappas) is original
    assert calls == [(True, True, {"cols": cols, "kappas": kappas})]
    assert model.LAST_DIAGNOSTICS["mode"] == "e041"


@pytest.mark.parametrize("kind", ["partial", "no_query", "given_missing", "missing_column"])
def test_invalid_partition_falls_back_before_any_routing_fit(case, monkeypatch, kind):
    model = source()
    frame, schema = case
    if kind == "partial":
        frame.loc[1, "child"] = "yes"
    elif kind == "no_query":
        frame = frame.fillna("yes")
    elif kind == "given_missing":
        frame.loc[1, "given"] = np.nan
    else:
        frame = frame.drop(columns="child")
    original = [np.array([4., 7.])]
    monkeypatch.setattr(model.supervised_retrieval, "predict", lambda *a, **k: original)
    monkeypatch.setattr(model, "routing_library", lambda *a: pytest.fail("fit before validation"))
    assert model.predict(frame, schema) is original
    assert model.LAST_DIAGNOSTICS["mode"] == "e041"
    assert model.LAST_DIAGNOSTICS["fallback_reason"]


def test_active_dispatch_returns_frozen_endpoint_without_normalizing(case, monkeypatch):
    model = source()
    endpoint = [np.array([2., 1.]), np.array([1., 3., 2.])]
    diagnostics = {"changed_vectors": 1, "legacy_lambdas": {"child": (.2, .8)}}
    monkeypatch.setattr(model, "routing_library", lambda *a: {
        "arms_raw": {"after_gates": endpoint}, "diagnostics": diagnostics})
    monkeypatch.setattr(model.supervised_retrieval, "predict", lambda *a, **k: pytest.fail("active fallback"))
    assert model.predict(*case) is endpoint
    assert model.LAST_DIAGNOSTICS["changed_vectors"] == 1
    assert model.LAST_DIAGNOSTICS["mode"] == "after_gates"
    model.LAST_DIAGNOSTICS["legacy_lambdas"].clear()
    assert diagnostics["legacy_lambdas"], "reported diagnostics must not mutate cached library"


def test_valid_path_does_not_hide_routing_errors(case, monkeypatch):
    model = source()

    def broken(*args):
        raise ValueError("routing defect")

    monkeypatch.setattr(model, "routing_library", broken)
    with pytest.raises(ValueError, match="routing defect"):
        model.predict(*case)


def test_custom_base_options_remain_exact_e041(case, monkeypatch):
    model = source()
    original = [np.array([3., 8.])]
    monkeypatch.setattr(model.supervised_retrieval, "predict", lambda *a, **k: original)
    monkeypatch.setattr(model, "routing_library", lambda *a: pytest.fail("custom options discarded"))
    assert model.predict(*case, cols=["given"], kappas=[3.]) is original


def snapshot():
    module = types.ModuleType("e052_test_snapshot")
    exec(compile(assembler().build_source(), "e052_test_snapshot", "exec"), module.__dict__)
    return module


def test_assembly_preserves_exact_parent_and_excludes_unneeded_helpers():
    build = assembler()
    raw = build.build_source()
    parent = (ROOT / "submissions/2026-09-19-E041/main.py").read_bytes()
    assert hashlib.sha256(parent).hexdigest() == build.PARENT_HASH
    assert raw[:len(parent)] == parent
    tree = ast.parse(raw)
    assert not any(isinstance(n, ast.ImportFrom) and (n.module or "").startswith("src")
                   for n in ast.walk(tree))
    assert not any(isinstance(n, ast.Name) and n.id in {
        "link_sharp", "hh_cap", "supervised_retrieval"} for n in ast.walk(tree))
    names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert {"routing_library", "cached_renderer", "_partition", "_mapped", "predict_components"} <= names
    assert not {"e050_library", "e051_library", "direct_tree", "component_oracle"} & names


def test_assembled_aliases_and_diagnostics_have_separate_namespaces(case, monkeypatch):
    module = snapshot()
    assert module._E041_SUPERVISED_LAYER is module.supervised_layer
    assert module._E041_PREDICT is not module.predict
    assert module.cached_renderer().__code__ is module._SHARP_PREDICT.__code__
    assert module._E052_DIAGNOSTICS is not module.LAST_DIAGNOSTICS
    module.LAST_DIAGNOSTICS["incumbent"] = "preserve"
    endpoint = [np.array([1., 2.]), np.array([4., 2., 1.])]
    monkeypatch.setattr(module, "routing_library", lambda *a: {
        "arms_raw": {"after_gates": endpoint}, "diagnostics": {"changed_vectors": 1}})
    assert module.predict(*case) is endpoint
    assert module.LAST_DIAGNOSTICS == {"incumbent": "preserve"}
    assert module._E052_DIAGNOSTICS["changed_vectors"] == 1
    case[0].loc[1, "child"] = "yes"
    monkeypatch.setattr(module, "_E041_PREDICT", lambda *a, **k: endpoint)
    assert module.predict(*case) is endpoint
    assert module._E052_DIAGNOSTICS["mode"] == "e041"
    assert "changed_vectors" not in module._E052_DIAGNOSTICS


def test_actual_helper_and_recursive_endpoint_match_source_and_assembly(case, monkeypatch):
    from src.models import link_sharp, supervised_retrieval
    model, module = source(), snapshot()
    frame, schema = case
    evidence = {1: ({MARKER: np.array([1., 0.]), "child": np.array([0., 1., 0.])}, False)}
    lambdas = {MARKER: (.8, .8), "child": (.2, .2)}
    calls = {"source": 0, "assembly": 0}

    # Stub only expensive fitted inputs; use real ladders, cached renderer,
    # original gate recursion, routing helper, wrapper, and assembly bindings.
    for namespace in (link_sharp, module):
        monkeypatch.setattr(namespace, "select_ladder", lambda *a: ([], [], 0))
        monkeypatch.setattr(namespace, "tune_and_train", lambda *a, **k:
                            (0., None, ([MARKER, "child"], ["child"])))
        monkeypatch.setattr(namespace, "conditional_agreement", lambda *a:
                            {"child": (.8, None, {})})

    def layer(name, diagnostics):
        def capture(*args):
            calls[name] += 1
            diagnostics.clear()
            diagnostics.update(active={"s3": True})
            return evidence, lambdas
        return capture

    monkeypatch.setattr(supervised_retrieval, "supervised_layer",
                        layer("source", supervised_retrieval.LAST_DIAGNOSTICS))
    monkeypatch.setattr(module, "_E041_SUPERVISED_LAYER",
                        layer("assembly", module.LAST_DIAGNOSTICS))
    expected = model.predict(frame, schema)
    actual = module.predict(frame, schema)
    assert calls == {"source": 1, "assembly": 1}
    assert model.LAST_DIAGNOSTICS["changed_vectors"] == 1
    assert module._E052_DIAGNOSTICS == model.LAST_DIAGNOSTICS
    assert module.LAST_DIAGNOSTICS == {"active": {"s3": True}}
    assert all(np.array_equal(a, b) for a, b in zip(actual, expected))
    incumbent = module._SHARP_PREDICT(frame, schema, layer_fn=lambda *a: (evidence, lambdas),
                                     configs=module.CONFIGS)
    np.testing.assert_array_equal(actual[0], incumbent[0])
    assert not np.array_equal(actual[1], incumbent[1]), "active child must differ from E041"


def test_zip_is_reproducible_main_only_and_matches_snapshot(tmp_path, monkeypatch):
    build = assembler()
    source_bytes = build.build_source()
    monkeypatch.setattr(build, "ROOT", tmp_path)
    monkeypatch.setattr(build, "build_source", lambda: source_bytes)
    build.main()
    archive = tmp_path / "submissions/2026-09-24-E052.zip"
    first = archive.read_bytes()
    build.main()
    assert archive.read_bytes() == first
    assert (archive.with_suffix("") / "main.py").read_bytes() == source_bytes
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.namelist() == ["main.py"]
        assert bundle.read("main.py") == source_bytes
        assert bundle.getinfo("main.py").date_time == (2026, 9, 24, 0, 0, 0)
