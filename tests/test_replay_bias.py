"""A011 protocol checks without expensive model fitting."""

import importlib
import gzip
import json
import pickle

import numpy as np
import pandas as pd
import pytest


def audit():
    return importlib.import_module("scripts.audit_replay_bias")


@pytest.fixture
def case():
    schema = {"gated_value": "NA_GATED", "items": {
        "given": {"class": "GIVEN", "values": ["x", "y"]},
        "answer": {"class": "PREDICT", "values": ["a", "b"]}}}
    frame = pd.DataFrame({"given": ["x", "y"] * 451,
                          "answer": ["a", "b"] * 450 + [np.nan, np.nan]})
    return frame, schema


def test_fixed_partitions_hide_whole_blocks_keep_original_dev(case):
    frame, schema = case
    part = audit().partition_rows(frame, schema)
    assert len(part["CAL"]) == len(part["CTRL"]) == 400
    assert not set(part["CAL"]) & set(part["CTRL"])
    assert set(part["DEV"]) == {900, 901}
    honest, included = audit().paired_frames(frame, schema, part)
    assert honest.answer.isna().sum() == 802
    assert included.answer.isna().sum() == 402
    pd.testing.assert_series_equal(included.loc[part["CAL"], "answer"],
                                   frame.loc[part["CAL"], "answer"])
    pd.testing.assert_series_equal(honest.given, frame.given)
    changed = frame.copy()
    changed.loc[np.r_[part["CAL"], part["CTRL"]], "answer"] = "b"
    hidden, _ = audit().paired_frames(changed, schema, part)
    pd.testing.assert_frame_equal(honest, hidden)
    for name, rows in audit().partition_rows(frame, schema).items():
        np.testing.assert_array_equal(rows, part[name])


def test_capture_uses_actual_renderer_namespace_and_empty_included_layer(case, monkeypatch):
    from src.models import link_sharp, supervised_retrieval
    frame, schema = case
    part = audit().partition_rows(frame, schema)
    honest, included = audit().paired_frames(frame, schema, part)
    rows = np.r_[part["CAL"], part["CTRL"]]
    calls = []
    monkeypatch.setattr(link_sharp, "select_ladder", lambda *a: ([], [], 0))
    monkeypatch.setattr(link_sharp, "tune_and_train", lambda *a, **k: (0., None, (["answer"], [])))
    monkeypatch.setattr(link_sharp, "conditional_agreement", lambda *a: {})

    def layer(f, s, full):
        calls.append(f.answer.isna().sum())
        return {int(r): ({"answer": np.array([.9, .1])}, False) for r in rows}, {"answer": (.4, .8)}

    monkeypatch.setattr(supervised_retrieval, "supervised_layer", layer)
    one = audit().capture_fit(honest, schema, rows, honest=True)
    two = audit().capture_fit(included, schema, rows, honest=False)
    assert calls == [802]
    assert two["evidence_rows"] == two["lambdas"] == {}
    assert len(one["recursive"]["answer"]) == 802
    assert len(two["recursive"]["answer"]) == 402
    assert one["full_head"]["answer"].shape == two["full_head"]["answer"].shape == (800, 2)
    assert not one["full_head"]["answer"].flags.writeable
    frozen = one["full_head"]["answer"].copy()
    prepared = audit().derive_honest(one, rows)
    np.testing.assert_allclose(prepared["gate_base"]["answer"], frozen, atol=1e-12)
    np.testing.assert_allclose(prepared["final"]["answer"], .6 * frozen + .4 * np.array([.9, .1]))


def test_inversion_missing_evidence_and_lambda_one_rejection():
    module = audit()
    base = np.array([[.2, .8], [.6, .4], [.1, .9]])
    evidence = np.array([[.8, .2], [np.nan, np.nan], [.7, .3]])
    shares = np.array([.98, 0., 0.])
    final = base.copy()
    final[0] = .02 * base[0] + .98 * evidence[0]
    actual = module.reconstruct_base(final, evidence, shares)
    np.testing.assert_allclose(actual, base, atol=1e-12)
    assert np.isnan(evidence[1]).all()
    with pytest.raises(ValueError, match="lambda"):
        module.reconstruct_base(final[:1], evidence[:1], np.array([1.]))
    with pytest.raises(ValueError, match="probabilit"):
        module.reconstruct_base(np.array([[.99, .01]]), evidence[:1], np.array([.98]))


@pytest.mark.parametrize("objective", ["legacy", "official"])
def test_analytic_gradient_matches_independent_finite_difference(objective):
    from src.eval.logloss import floor_mix
    from src.models.prob_link import EV_FLOOR
    base = np.array([[.03, .97], [.6, .4], [0., 1.]])
    evidence = np.array([[.8, .2], [.1, .9], [.5, .5]])
    truth = np.array([0, 1, 0])
    shares = np.array([.2, .98, .1])
    rows = np.arange(3)

    def objective_values(weight):
        if objective == "legacy":
            return np.log(np.maximum((1-weight) * np.maximum(base[rows, truth], EV_FLOOR)
                                     + weight * evidence[rows, truth], EV_FLOOR))
        return np.log(floor_mix((1-weight[:, None])*base + weight[:, None]*evidence)[rows, truth])

    numerical = (objective_values(shares+1e-6)-objective_values(shares-1e-6))/2e-6
    np.testing.assert_allclose(audit().log_gradient(base, evidence, truth, shares, objective),
                               numerical, rtol=1e-7)


def test_legacy_right_derivative_at_floor_zero_lambda():
    from src.models.prob_link import EV_FLOOR
    base = np.array([[0., 1.], [0., 1.]])
    evidence = np.array([[.3, .7], [0., 1.]])
    result = audit().log_gradient(base, evidence, np.array([0, 0]), np.zeros(2), "legacy")
    np.testing.assert_allclose(result, [(.3-EV_FLOOR)/EV_FLOOR, 0.])


def test_official_gradient_preserves_full_vector_normalization_derivative():
    from src.eval.logloss import floor_mix
    base = np.array([[.2, .7], [.6, .45]])
    evidence = np.array([[.85, .25], [.1, .8]])
    labels, shares = np.array([0, 1]), np.array([.3, .8])
    def scores(weight):
        return np.log(floor_mix((1-weight[:, None])*base+weight[:, None]*evidence)[np.arange(2), labels])
    numerical = (scores(shares+1e-6)-scores(shares-1e-6))/2e-6
    np.testing.assert_allclose(audit().log_gradient(base, evidence, labels, shares, "official"), numerical, rtol=1e-7)


def test_paired_bootstrap_constant_contrast():
    result = audit().paired_summary(np.full((400, 2), .3), np.full((400, 2), -.2))
    assert result["CAL"]["mean"] == pytest.approx(.3)
    assert result["CTRL"]["mean"] == pytest.approx(-.2)
    assert result["CAL_minus_CTRL"]["interval95"] == pytest.approx([.5, .5])
    assert result["CAL_minus_CTRL"]["mean"] == pytest.approx(.5)


def test_existing_artifact_refused_before_loading_or_fitting(tmp_path, monkeypatch):
    module = audit()
    (tmp_path / "clean-manifest.json").write_text("{}")
    monkeypatch.setattr(module, "prepare_case", lambda *a: pytest.fail("loaded despite existing artifact"))
    with pytest.raises(FileExistsError):
        module.run("clean", tmp_path)


def test_score_membership_gate_mismatch_and_minimum_bucket_count():
    module = audit()
    count = 800
    schema = {"items": {"answer": {"gate": {"parent": "given"}}}}
    honest = np.tile([.5, .5], (count, 1))
    included = np.tile([.7, .3], (count, 1))
    included[400:] = [.6, .4]
    gate = np.tile([.4, .6], (count, 1))
    evidence = np.tile([.9, .1], (count, 1))
    concentration = np.zeros(count, dtype=int)
    concentration[:29] = 1
    frozen = {"case": "fixture", "partitions": {"CAL": np.arange(400), "CTRL": np.arange(400, 800)},
              "honest": {"full_head": {"answer": honest}},
              "included": {"full_head": {"answer": included}},
              "derived": {"gate_base": {"answer": gate}, "evidence": {"answer": evidence},
                          "concentration": {"answer": concentration},
                          "effective_lambda": {"answer": np.full(count, .4)}}}
    result = module.score_capture(frozen, {"answer": np.zeros(count, dtype=int)}, schema)
    expected = np.log((.001+.998*.7)/(.001+.998*.6))
    assert result["membership"]["gated"]["CAL_minus_CTRL"]["mean"] == pytest.approx(expected)
    assert result["membership"]["gated"]["CAL_minus_CTRL"]["interval95"] == pytest.approx([expected]*2)
    assert result["gate_mismatch"]["all"]["CAL"]["mean"] < 0
    assert result["gate_probability_total_variation"]["all"]["CAL"]["mean"] == pytest.approx(.1)
    assert "ungated" not in result["membership"]
    for objective in ("legacy", "official"):
        buckets = result["gradients"][objective]["item_buckets"]
        assert all(row["bucket"] == 0 and row["rows"] >= 30 for row in buckets)
        assert all(row["slopes"]["honest_full"]["mean"] > 0 for row in buckets)
    evidence[:] = np.nan
    no_evidence = module.score_capture(frozen, {"answer": np.zeros(count, dtype=int)}, schema)
    assert no_evidence["evidence_coverage"]["answer"] == {"CAL": 0, "CTRL": 0, "pooled": 0}
    assert no_evidence["gradients"]["official"]["item_buckets"] == []
    json.dumps(no_evidence, allow_nan=False)


def test_freeze_precedes_any_label_scoring(tmp_path, case, monkeypatch):
    module = audit()
    frame, schema = case
    monkeypatch.setattr(module, "prepare_case", lambda *a: (frame, schema, {}))
    monkeypatch.setattr(module, "provenance", lambda *a: {})
    rows = np.r_[module.partition_rows(frame, schema)["CAL"], module.partition_rows(frame, schema)["CTRL"]]

    def capture(f, s, selected, honest):
        hidden = np.flatnonzero(f.answer.isna())
        return {"full_head": {"answer": np.tile([.5, .5], (800, 1))},
                "recursive": {"answer": np.tile([.5, .5], (len(hidden), 1))},
                "query": hidden, "evidence_rows": {}, "lambdas": {}}

    def score(frozen, labels, s):
        assert set(tmp_path.iterdir()) == {tmp_path / f"clean-{suffix}" for suffix in
                                            ("capture.pkl.gz", "arrays.npz", "manifest.json")}
        manifest = json.loads((tmp_path / "clean-manifest.json").read_text())
        assert "capture_sha256" in manifest and "arrays_sha256" in manifest
        compressed = (tmp_path / "clean-capture.pkl.gz").read_bytes()
        assert module.digest(compressed) == manifest["capture_sha256"]
        assert module.digest(gzip.decompress(compressed)) == manifest["raw_capture_sha256"]
        assert pickle.loads(gzip.decompress(compressed))["case"] == "clean"
        with np.load(tmp_path / "clean-arrays.npz") as arrays:
            assert "honest_full/answer" in arrays
            assert not any("evidence_rows" in key for key in arrays.files)
        assert len(labels["answer"]) == len(rows) == 800
        assert not frozen["honest"]["full_head"]["answer"].flags.writeable
        return {"checked": True}

    monkeypatch.setattr(module, "capture_fit", capture)
    monkeypatch.setattr(module, "score_capture", score)
    assert module.run("clean", tmp_path)["checked"]
