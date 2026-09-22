"""Apply the frozen E047 estimator to its preregistered observed-data screen."""

import os

for variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[variable] = "2"

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "tests")]

import numpy as np
from e041_external import SECTIONS
from e041_external_learned import paired_delta
from src.models import adaptive_final_evidence as model


def truth_probability(predictions, labels, names):
    columns = []
    for name in names:
        p = predictions[name]
        p = .001 + (1. - p.shape[1] * .001) * p / p.sum(axis=1, keepdims=True)
        columns.append(p[np.arange(len(p)), labels[name]])
    return np.column_stack(columns)


def run(seed, expected):
    path = ROOT / expected["cache_path"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected["cache_sha256"]
    cache = np.load(path, allow_pickle=False)
    names = cache["targets"].tolist()
    base = {name: cache["initial__" + name][800:] for name in names}
    evidence = {name: cache["evidence__" + name][800:] for name in names}
    labels = {name: cache["labels"][800:, j] for j, name in enumerate(names)}
    fit, select, audit = np.arange(1000), np.arange(1000, 1600), np.arange(1600, 2200)
    groups = list(SECTIONS.values())
    policies, diagnostics = model.e047_fit_policies(
        base, evidence, labels, groups, fit, select, audit)
    prediction = model.e047_apply(base, evidence, groups, policies)
    original = truth_probability(base, labels, names)[audit]
    corrected = truth_probability(prediction, labels, names)[audit]
    u = float(np.log(cache["sizes"]).mean())
    return {"seed": seed, "diagnostics": diagnostics, "policies": policies,
            "audit_guarded_delta": paired_delta(corrected, original, u),
            "interpretation": "Audit-guarded result includes acceptance selection; "
                              "pre-guard audit diagnostics must be read alongside it. "
                              "The same audit labels previously screened the family oracle, "
                              "so this is not an untouched end-to-end research holdout. "
                              "Intervals are descriptive and do not adjust for that selection. "
                              "Observed Adult proxy, not an HSCC forecast."}


def main():
    oracle_path = ROOT / "docs/analysis/A008-outputs/e047-final-evidence-oracle.json"
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    assert oracle["proceed_to_estimator"]
    result = {
        "experiment": "E047",
        "model_sha256": hashlib.sha256(Path(model.__file__).read_bytes()).hexdigest(),
        "oracle_report_sha256": hashlib.sha256(oracle_path.read_bytes()).hexdigest(),
        "runs": [run(item["seed"], item) for item in oracle["runs"]],
        "audit_retuning": False,
    }
    output = ROOT / "docs/analysis/E047-outputs/observed-estimator.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
