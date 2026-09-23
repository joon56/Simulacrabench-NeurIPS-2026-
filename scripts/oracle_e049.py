"""E049 hash-bound frozen-library oracle, followed by preregistered selection."""

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "tests")]

import numpy as np
from e041_external import (TARGETS, SECTIONS, load_observed, encode,
                           truth_probabilities, metrics)
from src.models import adaptive_final_evidence as adaptive
from scripts.oracle_e046 import paired_gain

OUTPUT = ROOT / "docs/analysis/E049-outputs"


def frozen(seed):
    source = ROOT / f"docs/analysis/E048-outputs/oracle-seed{seed}.json"
    record = json.loads(source.read_text(encoding="utf-8"))
    path = ROOT / f"docs/analysis/E048-outputs/frozen-seed{seed}.npz"
    raw_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    assert raw_hash == record["frozen_predictions"]["sha256"]
    observed, ids, _ = load_observed(ROOT / "tmp/e041/adult/adult.data", seed, 3000)
    assert hashlib.sha256(ids.tobytes()).hexdigest() == record["source_line_ids_sha256"]
    frame, schema = encode(observed)
    arrays = np.load(path)
    base = {item: arrays[f"baseline__{item}"] for item in TARGETS}
    candidate = {item: arrays[f"tabpfn__{item}"] for item in TARGETS}
    query = np.arange(1800, 3000)
    labels = {item: frame.loc[query, item].to_numpy() for item in TARGETS}
    legacy_logs = np.log(np.stack([
        truth_probabilities({item: (1 - a) * base[item] + a * candidate[item]
                             for item in TARGETS}, frame, query)
        for a in (0., .25, .5)]))
    # Match E047's deployed family: normalize each endpoint before blending.
    # PFN float32 row-mass roundoff otherwise perturbs the effective alpha.
    normalized_base = {item: adaptive.e047_normalize(base[item]) for item in TARGETS}
    normalized_candidate = {item: adaptive.e047_normalize(candidate[item]) for item in TARGETS}
    logs = np.log(np.stack([
        truth_probabilities({item: (1 - a) * normalized_base[item] + a * normalized_candidate[item]
                             for item in TARGETS}, frame, query)
        for a in (0., .25, .5)]))
    vector_difference = max(
        float(np.max(np.abs((1 - .001 * base[item].shape[1]) * (
            adaptive.e047_normalize((1 - a) * base[item] + a * candidate[item]) -
            adaptive.e047_normalize((1 - a) * normalized_base[item] + a * normalized_candidate[item])))))
        for a in (0., .25, .5) for item in TARGETS)
    audit = logs[:, 800:]
    oracle = audit[0].copy()
    legacy_audit = legacy_logs[:, 800:]
    legacy_oracle = legacy_audit[0].copy()
    changed_choices = 0
    for names in SECTIONS.values():
        index = [TARGETS.index(name) for name in names]
        local = audit[:, :, index]
        best = local.mean(axis=2).argmax(axis=0)
        oracle[:, index] = local[best, np.arange(400)]
        legacy_local = legacy_audit[:, :, index]
        legacy_best = legacy_local.mean(axis=2).argmax(axis=0)
        legacy_oracle[:, index] = legacy_local[legacy_best, np.arange(400)]
        changed_choices += int(np.count_nonzero(best != legacy_best))
    baseline = metrics(np.exp(audit[0]), schema)
    upper = metrics(np.exp(oracle), schema)
    gain = (upper["skill"] - baseline["skill"]) / 3
    legacy_gain = (metrics(np.exp(legacy_oracle), schema)["skill"] -
                   metrics(np.exp(legacy_audit[0]), schema)["skill"]) / 3
    # Continuous alpha in [0,.5] contains the production sigmoid policy.
    # Log probability is concave in alpha; bracket its derivative to get a
    # feasible optimum and a tangent-based upper bound (numerical dual gap).
    first = truth_probabilities(base, frame, query)[800:]
    second = truth_probabilities(candidate, frame, query)[800:]
    continuous = first.copy()
    gaps = []
    for names in SECTIONS.values():
        index = [TARGETS.index(name) for name in names]
        p = first[:, index]
        difference = second[:, index] - p
        low, high = np.zeros(400), np.full(400, .5)
        for _ in range(48):
            middle = (low + high) / 2
            derivative = (difference / (p + middle[:, None] * difference)).mean(axis=1)
            low = np.where(derivative > 0, middle, low)
            high = np.where(derivative > 0, high, middle)
        alpha = (low + high) / 2
        probability = p + alpha[:, None] * difference
        derivative = (difference / probability).mean(axis=1)
        gap = np.maximum(-alpha * derivative, (.5 - alpha) * derivative)
        gaps.append(float(gap.max()))
        continuous[:, index] = probability
    continuous_metrics = metrics(continuous, schema)
    assert continuous_metrics["skill"] >= upper["skill"] - 1e-10
    assert max(gaps) < 1e-9
    report = {"seed": seed, "frozen_sha256": raw_hash, "oracle": upper,
              "baseline": baseline, "oracle_skill_div3": gain,
              "oracle_gate_pass": bool(gain > .005),
              "continuous_oracle": continuous_metrics,
              "continuous_oracle_skill_div3": (continuous_metrics["skill"] - baseline["skill"]) / 3,
              "continuous_max_tangent_gap_nats": max(gaps),
              "finite_grid_is_continuous_feasible_lower_bound": True,
              "endpoint_normalization_audit": {
                  "reason": "Normalize endpoints before mixing to match unchanged E047 policy; same alpha grid.",
                  "max_raw_endpoint_row_mass_error": max(
                      float(np.max(np.abs(values.sum(axis=1) - 1.)))
                      for endpoint in (base, candidate) for values in endpoint.values()),
                  "max_floored_probability_abs_change_all_vectors": vector_difference,
                  "max_truth_log_abs_change": float(np.max(np.abs(logs - legacy_logs))),
                  "legacy_finite_grid_skill_div3": legacy_gain,
                  "finite_grid_skill_div3_change": gain - legacy_gain,
                  "changed_audit_section_choices": changed_choices,
              },
              "oracle_paired": paired_gain(oracle, audit[0]),
              "audit_previously_screened": True}
    return report, base, candidate, labels, schema


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    runs = [frozen(seed) for seed in (49, 50)]
    passed = all(run[0]["oracle_gate_pass"] for run in runs)
    # The complete two-seed oracle gate is measured before any policy fit.
    (OUTPUT / "oracle-gate.json").write_text(json.dumps(
        {"passed": passed, "runs": [run[0] for run in runs],
         "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                           for name in ("scripts/oracle_e049.py",
                                        "src/models/adaptive_final_evidence.py",
                                        "docs/experiments/E049-adaptive-tabpfn-parents.md")}},
        indent=2) + "\n")
    print("ORACLE", json.dumps([run[0] for run in runs]), flush=True)
    if not passed:
        return
    for report, base, candidate, labels, schema in runs:
        policies, diagnostics = adaptive.e047_fit_policies(
            base, candidate, labels, list(SECTIONS.values()),
            np.arange(400), np.arange(400, 800), np.arange(800, 1200))
        audit_base = {name: p[800:] for name, p in base.items()}
        audit_candidate = {name: p[800:] for name, p in candidate.items()}
        selected = adaptive.e047_apply(audit_base, audit_candidate,
                                      list(SECTIONS.values()), policies)
        base_log = np.column_stack([
            adaptive.e047_log_truth(audit_base[n], labels[n][800:]) for n in TARGETS])
        final_log = np.column_stack([
            adaptive.e047_log_truth(selected[n], labels[n][800:]) for n in TARGETS])
        result = metrics(np.exp(final_log), schema)
        result["delta_skill"] = result["skill"] - report["baseline"]["skill"]
        result.update(paired_gain(final_log, base_log))
        report.update(learned=result, diagnostics=diagnostics, policies=policies,
                      interpretation="Exploratory reused Adult rows; not an HSCC forecast.")
        (OUTPUT / f"observed-seed{report['seed']}.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("LEARNED", json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
