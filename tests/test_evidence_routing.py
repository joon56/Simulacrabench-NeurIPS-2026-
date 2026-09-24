"""E052 routing semantics against an independently modified recursive renderer."""

import ast
from collections import Counter
import importlib
import inspect

import numpy as np
import pandas as pd
import pytest


def routing():
    return importlib.import_module("src.eval.evidence_routing")


@pytest.fixture
def stack(monkeypatch):
    from src.models import link_sharp, supervised_retrieval
    from src.models.hier_backoff import _layout
    schema = {"gated_value": "NA_GATED", "items": {
        "given": {"class": "GIVEN", "values": ["yes", "no"]},
        "root": {"class": "PREDICT", "values": ["yes", "no"]},
        "child": {"class": "PREDICT", "values": ["yes", "no"],
                  "gate": {"parent": "root", "observed_if": ["yes"]}},
        "leaf": {"class": "PREDICT", "values": ["yes", "no"],
                 "gate": {"parent": "child", "observed_if": ["yes"]}},
        "boundary": {"class": "PREDICT", "values": ["yes", "no"],
                     "gate": {"parent": "given", "observed_if": ["yes"]}},
        "zero_agreement": {"class": "PREDICT", "values": ["yes", "no"],
                     "gate": {"parent": "root", "observed_if": ["yes"]}},
        "full_evidence": {"class": "PREDICT", "values": ["yes", "no"],
                     "gate": {"parent": "root", "observed_if": ["yes"]}},
    }}
    frame = pd.DataFrame({n: ["yes", "no"] * 30 for n in schema["items"]})
    predicted = list(schema["items"])[1:]
    frame.loc[[58, 59], predicted] = np.nan
    _, _, options = _layout(frame, schema)
    gated = predicted[1:]
    calls = Counter()

    def counted(name, fn):
        def wrapper(*a, **kw):
            calls[name] += 1
            return fn(*a, **kw)
        return wrapper

    def proba(*a):
        return ({n: np.full((len(frame), len(options[n])), 1 / len(options[n])) for n in predicted},
                {n: np.full((len(frame), 2), .5) for n in gated})

    evidence = {r: ({n: np.eye(len(options[n]))[0] for n in predicted}, r == 59)
                for r in [58, 59]}
    lambdas = {n: (.2, .8) for n in predicted}
    lambdas["full_evidence"] = (1., 1.)
    agreements = {n: (.8, None, {}) for n in gated}
    agreements["zero_agreement"] = (0., None, {})
    monkeypatch.setattr(link_sharp, "select_ladder", counted("select", lambda *a: ([], [], 0)))
    monkeypatch.setattr(link_sharp, "tune_and_train", counted("fit", lambda *a, **k: (.3, object(), (predicted, gated))))
    monkeypatch.setattr(link_sharp, "_proba_maps", counted("proba", proba))
    monkeypatch.setattr(link_sharp, "conditional_agreement", counted("agreement", lambda *a: agreements))
    monkeypatch.setattr(supervised_retrieval, "supervised_layer", counted("layer", lambda *a: (evidence, lambdas)))
    return frame[list(reversed(frame.columns))], schema, evidence, lambdas, calls


def direct_without_evidence_in_beliefs(frame, schema, evidence, lambdas):
    """Independent reference: route the original renderer's pre-evidence base."""
    from src.models import link_sharp, hh_cap
    tree = ast.parse(inspect.getsource(link_sharp.predict))
    loop = next(n for n in ast.walk(tree) if isinstance(n, ast.For)
                and isinstance(n.target, ast.Tuple) and ast.unparse(n.target) == '(col, item)')
    index = next(i for i, n in enumerate(loop.body) if isinstance(n, ast.If)
                 and ast.unparse(n.test) == 'entry_row is not None')
    loop.body.insert(index, ast.parse("routing_base = base").body[0])
    loop.body[-2:] = ast.parse("belief[item] = routing_base\nout.append(base)").body
    namespace = link_sharp.predict.__globals__.copy()
    exec(compile(ast.fix_missing_locations(tree), "<reference-renderer>", "exec"), namespace)
    return namespace["predict"](frame, schema, configs=hh_cap.CONFIGS,
                                layer_fn=lambda *a: (evidence, lambdas))


def test_multilevel_endpoint_matches_direct_recursion_and_fits_once(stack):
    frame, schema, evidence, lambdas, calls = stack
    result = routing().routing_library(frame, schema)
    assert calls == Counter(select=1, fit=1, proba=1, agreement=1, layer=1)
    direct = direct_without_evidence_in_beliefs(frame, schema, evidence, lambdas)
    for actual, expected in zip(result["arms_raw"]["after_gates"], direct):
        np.testing.assert_allclose(actual, expected, rtol=0, atol=1e-15)
    assert result["evidence_rows"] is evidence
    assert result["lambdas"] is lambdas
    for item in ("child", "leaf"):
        assert not np.array_equal(result["arms"]["after_gates"][item], result["base"][item])
    assert result["diagnostics"]["changed_vectors"] == 4


def test_identity_boundaries_keep_original_raw_objects(stack):
    result = routing().routing_library(*stack[:2])
    for i, item in enumerate(result["predicted"]):
        if item in ("root", "boundary", "zero_agreement", "full_evidence"):
            for j in range(i, len(result["base_raw"]), len(result["predicted"])):
                assert result["arms_raw"]["after_gates"][j] is result["base_raw"][j]


def test_no_evidence_and_zero_evidence_are_exact(stack, monkeypatch):
    from src.models import supervised_retrieval
    for layer in (({}, {}), (stack[2], {n: (0., 0.) for n in stack[3]})):
        monkeypatch.setattr(supervised_retrieval, "supervised_layer", lambda *a: layer)
        result = routing().routing_library(*stack[:2])
        assert result["diagnostics"]["changed_vectors"] == 0
        assert all(a is b for a, b in zip(result["base_raw"], result["arms_raw"]["after_gates"]))


def test_partial_query_rejected_before_fitting(stack):
    frame, schema, _, _, calls = stack
    frame.loc[58, "root"] = "yes"
    with pytest.raises(ValueError, match="whole PREDICT"):
        routing().routing_library(frame, schema)
    assert not calls


def test_screen_freezes_endpoints_and_rejects_wrong_baseline(stack, tmp_path, monkeypatch):
    import hashlib
    import json
    import pickle
    screen = importlib.import_module("scripts.screen_e052")
    frame, schema = stack[:2]
    frozen = routing().routing_library(frame, schema)
    cells = [(int(r), f"respondent-{r}", n) for r in frozen["query"] for n in frozen["predicted"]]
    truth = ["yes"] * len(cells)
    baseline = {"frame_sha256": "test-frame", "source_sha256": screen.BASELINE_HASHES["E041"],
                "vectors": frozen["base_raw"]}
    cache = tmp_path / "cache"
    cache.mkdir()
    baseline_path = cache / "clean-unhcr-E041.pkl"
    baseline_path.write_bytes(pickle.dumps(baseline, protocol=5))
    monkeypatch.setattr(screen, "CACHE", cache)
    monkeypatch.setattr(screen, "get_case", lambda *a: ({"scoring": {"bootstrap_draws": 20}}, schema,
                                                       frame, cells, truth, "test-frame"))
    monkeypatch.setattr(screen, "routing_library", lambda *a: frozen)
    oracle = screen.component_oracle
    output = tmp_path / "outputs"

    def frozen_before_score(*args):
        payload = (output / "clean-endpoints.pkl").read_bytes()
        manifest = json.loads((output / "clean-manifest.json").read_text())
        assert hashlib.sha256(payload).hexdigest() == manifest["library_sha256"]
        return oracle(*args)

    monkeypatch.setattr(screen, "component_oracle", frozen_before_score)
    result = screen.run("clean", output)
    assert result["baseline_probability_max_abs"] == 0
    assert result["changed_vectors"] == 4
    assert sum(r["cells"] for r in result["by_depth"].values()) == len(cells)
    assert sum(r["cells"] for r in result["by_section"].values()) == len(cells)
    baseline["frame_sha256"] = "wrong-frame"
    baseline_path.write_bytes(pickle.dumps(baseline))
    monkeypatch.setattr(screen, "routing_library", lambda *a: pytest.fail("fit before baseline validation"))
    with pytest.raises(AssertionError, match="frame"):
        screen.run("clean", tmp_path / "new-output")


@pytest.mark.parametrize("suffix", ["endpoints.pkl", "arrays.npz", "manifest.json", "screen.json"])
def test_screen_refuses_any_existing_case_artifact_before_loading_or_fitting(tmp_path, monkeypatch, suffix):
    screen = importlib.import_module("scripts.screen_e052")
    artifact = tmp_path / f"clean-{suffix}"
    artifact.write_bytes(b"frozen-proof")
    monkeypatch.setattr(screen, "get_case", lambda *a: pytest.fail("case loaded before overwrite guard"))
    monkeypatch.setattr(screen, "routing_library", lambda *a: pytest.fail("fit before overwrite guard"))
    with pytest.raises(FileExistsError, match="Preserve frozen E052"):
        screen.run("clean", tmp_path)
    assert artifact.read_bytes() == b"frozen-proof"
