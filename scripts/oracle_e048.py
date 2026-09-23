"""Preregistered E048 frozen TabPFN V2 Adult proxy oracle; no production fit."""

import os

for _variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[_variable] = "2"
os.environ["TABPFN_DISABLE_TELEMETRY"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "tmp/e048-vendor"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(VENDOR))

import numpy as np
import sklearn
import torch
from tabpfn import TabPFNClassifier
from tabpfn.base import ClassifierModelSpecs
from tabpfn.constants import ModelVersion
from tabpfn.model_loading import load_model_criterion_config
from threadpoolctl import threadpool_limits

from e041_external import (
    GIVEN, TARGETS, SECTIONS, SOURCE, load_observed, encode,
    baseline_probabilities, truth_probabilities, metrics,
)
from scripts.oracle_e046 import digest, paired_gain, choose_sections, section_policy

OUTPUT = ROOT / "docs/analysis/E048-outputs"
WEIGHTS = (0., .25, .5)
CHECKPOINT = ROOT / "tmp/e048-model/tabpfn-v2-classifier.ckpt"
EXPECTED_CHECKPOINT_SHA256 = (
    "f65a35685aeef42e31b796d9bfa34e68d6fc780bc98e7bff7763802964cf435f"
)
PARAMETERS = {
    "version": "v2", "n_estimators": 1, "device": "cpu",
    "fit_mode": "fit_preprocessors", "n_jobs": 1, "random_state": 0,
    "categorical_features_indices": list(range(len(GIVEN))),
    "reference_rows": 512, "torch_threads": 2, "threadpool_threads": 2,
}


def file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dependency_manifest():
    """Hash installed metadata and RECORD manifests, preserving resolved versions."""
    result = {}
    for distribution in sorted(VENDOR.glob("*.dist-info")):
        result[distribution.name] = {
            name: file_digest(distribution / name)
            for name in ("METADATA", "RECORD") if (distribution / name).exists()
        }
    assert result, "Missing isolated dependency installation"
    serialized = json.dumps(result, sort_keys=True).encode()
    versions = {
        distribution.metadata["Name"]: distribution.version
        for distribution in importlib.metadata.distributions(path=[str(VENDOR)])
    }
    return {"sha256": hashlib.sha256(serialized).hexdigest(),
            "versions": versions, "distributions": result}


# Loading occurs at module import, with downloads explicitly disabled.
assert importlib.metadata.version("tabpfn") == "8.0.8"
assert file_digest(CHECKPOINT) == EXPECTED_CHECKPOINT_SHA256
torch.set_num_threads(2)
_load_started = time.perf_counter()
_models, _criterion, _configs, _inference = load_model_criterion_config(
    model_path=CHECKPOINT,
    check_bar_distribution_criterion=False,
    cache_trainset_representation=False,
    which="classifier",
    version="v2",
    download_if_not_exists=False,
)
V2_SPEC = ClassifierModelSpecs(_models[0], _configs[0], _inference)
LOAD_SECONDS = time.perf_counter() - _load_started
DEPENDENCIES = dependency_manifest()


def tabpfn_probabilities(frame, schema, reference, query, base):
    """Each frozen forward sees reference labels and GIVEN-only query features."""
    assert len(reference) == 512 and not np.intersect1d(reference, query).size
    assert (frame.loc[query, TARGETS].to_numpy() == -1).all()
    x = frame.loc[reference, GIVEN].to_numpy(dtype=np.float64, copy=True)
    x_query = frame.loc[query, GIVEN].to_numpy(dtype=np.float64, copy=True)
    result, diagnostics = {}, {}
    for item in TARGETS:
        started = time.perf_counter()
        k = len(schema["items"][item]["options"])
        y = frame.loc[reference, item].to_numpy(dtype=np.int64, copy=True)
        classes = np.unique(y)
        if k > 10 or len(classes) < 2:
            result[item] = base[item].copy()
            diagnostics[item] = {
                "schema_classes": k, "reference_classes": classes.tolist(),
                "intervened": False,
                "fallback_reason": "schema_classes_gt_10" if k > 10 else "single_class",
            }
            continue
        model = TabPFNClassifier.create_default_for_version(
            ModelVersion.V2,
            model_path=V2_SPEC,
            n_estimators=1,
            device="cpu",
            fit_mode="fit_preprocessors",
            n_jobs=1,
            random_state=0,
            categorical_features_indices=list(range(len(GIVEN))),
        )
        model.fit(x, y)
        probabilities = np.zeros((len(query), k), dtype=np.float64)
        probabilities[:, np.asarray(model.classes_, dtype=int)] = model.predict_proba(x_query)
        assert np.isfinite(probabilities).all() and (probabilities >= 0).all()
        assert np.allclose(probabilities.sum(axis=1), 1.)
        result[item] = probabilities
        diagnostics[item] = {
            "schema_classes": k, "reference_classes": classes.tolist(),
            "intervened": True, "elapsed_seconds": time.perf_counter() - started,
            "probabilities_sha256": digest(probabilities),
        }
        print(json.dumps({"event": "frozen_forward", "item": item,
                          **diagnostics[item]}), flush=True)
    return result, diagnostics


def query_section_oracle(audit_logs):
    """Exact finite maximum: one weight per respondent and section, shared by items."""
    result = audit_logs[0].copy()
    diagnostics = {}
    for section, items in SECTIONS.items():
        indices = [TARGETS.index(item) for item in items]
        local = audit_logs[:, :, indices]
        choices = local.mean(axis=2).argmax(axis=0)
        selected = local[choices, np.arange(local.shape[1]), :]
        result[:, indices] = selected
        assert np.all(selected.mean(axis=1) >= local[0].mean(axis=1) - 1e-12)
        diagnostics[section] = {
            "items": items,
            "weight_counts": {str(weight): int((choices == index).sum())
                              for index, weight in enumerate(WEIGHTS)},
            **paired_gain(selected, local[0]),
        }
    return result, diagnostics


def run(seed):
    assert seed in (49, 50)
    started = time.perf_counter()
    source = ROOT / "tmp/e041/adult/adult.data"
    observed, source_ids, counts = load_observed(source, seed, rows=3000)
    frame, schema = encode(observed)
    fit = np.arange(1800)
    reference = fit[:512]
    selection = np.arange(1800, 2400)
    audit = np.arange(2400, 3000)
    query = np.concatenate((selection, audit))
    partitions = {"fit": fit, "selection": selection, "audit": audit}
    assert len(np.unique(np.concatenate(list(partitions.values())))) == 3000
    assert len(set(source_ids)) == 3000 and not set(GIVEN) & set(TARGETS)
    masked = frame.copy()
    masked.loc[query, TARGETS] = -1
    base = baseline_probabilities(masked, schema, fit, query)
    frozen, head_diagnostics = tabpfn_probabilities(masked, schema, reference, query, base)

    # Freeze all probabilities before using selection/audit truth for mixtures.
    frozen_path = OUTPUT / f"frozen-seed{seed}.npz"
    np.savez_compressed(frozen_path, **{
        f"{kind}__{item}": predictions[item]
        for kind, predictions in (("baseline", base), ("tabpfn", frozen))
        for item in TARGETS
    })
    frozen_sha256 = file_digest(frozen_path)
    logs = np.log(np.stack([
        truth_probabilities(
            {item: (1. - weight) * base[item] + weight * frozen[item]
             for item in TARGETS}, frame, query)
        for weight in WEIGHTS
    ]))
    assert logs.shape == (3, 1200, len(TARGETS))
    selection_logs, audit_logs = logs[:, :600], logs[:, 600:]
    choices, selection_diagnostics = choose_sections(selection_logs)
    honest_log = section_policy(audit_logs, choices)
    oracle_log, oracle_diagnostics = query_section_oracle(audit_logs)
    constant_choices = {
        section: int(audit_logs[:, :, [TARGETS.index(item) for item in items]]
                     .mean(axis=(1, 2)).argmax())
        for section, items in SECTIONS.items()
    }
    constant_log = section_policy(audit_logs, constant_choices)
    base_log = audit_logs[0]
    assert oracle_log.mean() >= constant_log.mean() - 1e-12
    assert constant_log.mean() >= honest_log.mean() - 1e-12
    evaluated = {
        "categorical_logistic": base_log,
        "tabpfn_supported_heads": np.log(truth_probabilities(frozen, frame, query)[600:]),
        "query_section_oracle": oracle_log,
        "constant_section_oracle": constant_log,
        "selection_only_section_policy": honest_log,
    }
    methods = {}
    baseline_metric = metrics(np.exp(base_log), schema)
    for name, method_log in evaluated.items():
        result = metrics(np.exp(method_log), schema)
        result.update(paired_gain(method_log, base_log))
        result["delta_skill_vs_baseline"] = result["skill"] - baseline_metric["skill"]
        result["delta_skill_div3_proxy"] = result["delta_skill_vs_baseline"] / 3.
        result["respondent_se_skill_div3_proxy"] = (
            result["respondent_se_nats"] / result["uniform_reference"] / 3.
        )
        methods[name] = result
    source_files = (
        "scripts/oracle_e048.py", "scripts/oracle_e046.py", "tests/e041_external.py",
        "src/eval/logloss.py", "docs/experiments/E048-tabpfn-gate-parents.md",
    )
    return {
        "experiment": "E048", "seed": seed,
        "source": {"url": SOURCE, "license": "CC BY 4.0", "sha256": file_digest(source)},
        "source_counts": counts, "source_line_ids_sha256": digest(source_ids),
        "split": {name: len(rows) for name, rows in partitions.items()},
        "split_source_ids_sha256": {
            name: digest(source_ids[rows]) for name, rows in partitions.items()},
        "reference_source_ids_sha256": digest(source_ids[reference]),
        "encoded_given_sha256": digest(frame[GIVEN].to_numpy(dtype=np.int64)),
        "encoded_target_sha256": digest(frame[TARGETS].to_numpy(dtype=np.int64)),
        "source_files_sha256": {name: file_digest(ROOT / name) for name in source_files},
        "runtime_versions": {"python": sys.version, "numpy": np.__version__,
                             "scikit_learn": sklearn.__version__, "torch": torch.__version__,
                             "tabpfn": importlib.metadata.version("tabpfn")},
        "dependencies": DEPENDENCIES,
        "checkpoint": {"file": CHECKPOINT.name, "sha256": EXPECTED_CHECKPOINT_SHA256,
                       "size_bytes": CHECKPOINT.stat().st_size,
                       "hf_revision": "f851f2a3c941544733b712d8c0f96dfae9b28862",
                       "import_load_seconds": LOAD_SECONDS},
        "schema": schema, "parameters": PARAMETERS, "weight_grid": WEIGHTS,
        "frozen_predictions": {"file": str(frozen_path.relative_to(ROOT)),
                               "sha256": frozen_sha256},
        "head_diagnostics": head_diagnostics, "methods": methods,
        "oracle": {
            "family": "One weight per audit respondent and section, shared across section items.",
            "optimization": "Exact separable maximum over three frozen mixtures.",
            "uses_audit_labels": True, "section_diagnostics": oracle_diagnostics,
            "constant_section_weights": {
                section: WEIGHTS[index] for section, index in constant_choices.items()},
            "bound_scope": "Finite frozen mixture library on Adult audit rows only.",
        },
        "honest_selection": selection_diagnostics,
        "gate_threshold_skill_div3_proxy": .005,
        "seed_gate_pass": bool(methods["query_section_oracle"]["delta_skill_div3_proxy"] > .005),
        "leakage_checks": {
            "fit_selection_audit_disjoint": True,
            "tabpfn_first_512_fit_rows_only": True,
            "baseline_all_1800_fit_rows_only": True,
            "all_query_targets_masked_in_actual_fit_path": True,
            "predictor_query_input_given_only": True,
            "section_selection_receives_selection_only": True,
            "full_profile_duplicates_removed_before_split": True,
            "frozen_predictions_saved_before_truth_based_mixture_scoring": True,
            "all_row_option_vocabulary_matches_existing_E041_protocol": True,
        },
        "interpretation": "Exploratory observed Adult bound. Audit truth screens a frozen "
                          "library, not an untouched confirmatory set, learnability claim, "
                          "survey gate replica, or HSCC ceiling/forecast.",
        "elapsed_seconds": time.perf_counter() - started,
    }


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    runs = []
    with threadpool_limits(limits=2):
        for seed in (49, 50):
            result = run(seed)
            runs.append(result)
            (OUTPUT / f"oracle-seed{seed}.json").write_text(
                json.dumps(result, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({key: result[key] for key in
                              ("seed", "methods", "seed_gate_pass", "elapsed_seconds")}),
                  flush=True)
    gate_pass = all(result["seed_gate_pass"] for result in runs)
    summary = {
        "joint_gate_pass": gate_pass,
        "decision": "proceed_to_production_evaluation" if gate_pass
                    else "park_E048_without_production_estimator",
        "interpretation": "Adult proxy-only screening; no HSCC forecast.",
    }
    (OUTPUT / "oracle-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
