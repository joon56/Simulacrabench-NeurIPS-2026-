"""Preregistered E045 distinct-union oracle; never a production estimator."""

import os

for _variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[_variable] = "2"

import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import numpy as np
from threadpoolctl import threadpool_limits

from e041_external import (GIVEN, TARGETS, SECTIONS, load_observed, encode,
                           baseline_probabilities, truth_probabilities)
from oracle_e043 import ITERATIONS, bounds, digest, summarize
from src.eval.retrieval_oracle import candidate_indices
from src.models.supervised_retrieval import fit_sections

OUTPUT = ROOT / "docs/analysis/E045-outputs"


def run(seed):
    started = time.perf_counter()
    source = ROOT / "tmp/e041/adult/adult.data"
    observed, source_ids, counts = load_observed(source, seed, rows=5000)
    frame, schema = encode(observed)
    bank, fit = np.arange(2000), np.arange(2000, 3000)
    selection, audit = np.arange(3000, 4000), np.arange(4000, 5000)
    partitions = (bank, fit, selection, audit)
    assert len(np.unique(np.concatenate(partitions))) == 5000
    assert len(set(source_ids)) == 5000
    codes = frame[GIVEN].to_numpy(dtype=int)
    labels = frame[TARGETS].to_numpy(dtype=int)
    groups = [[TARGETS.index(item) for item in items] for items in SECTIONS.values()]
    sizes = np.array([len(schema["items"][item]["options"]) for item in TARGETS])
    initial = []
    for j in range(len(GIVEN)):
        frequency = np.bincount(codes[bank, j]) / len(bank)
        initial.append(-np.log(np.clip(np.square(frequency).sum(), 1e-6, 1.)))
    initial = np.asarray(initial)
    learned, active, diagnostics = fit_sections(
        codes, labels, bank, fit, selection, initial, sizes, groups)

    masked_frame = frame.copy()
    masked_frame.loc[audit, TARGETS] = -1
    masked_codes = masked_frame[GIVEN].to_numpy(dtype=int)
    masked_labels = masked_frame[TARGETS].to_numpy(dtype=int)
    repeated, repeated_active, repeated_diagnostics = fit_sections(
        masked_codes, masked_labels, bank, fit, selection, initial, sizes, groups)
    assert all(np.array_equal(a, b) for a, b in zip(learned, repeated))
    assert active == repeated_active and diagnostics == repeated_diagnostics

    visible = np.concatenate((bank, fit))
    base = baseline_probabilities(frame, schema, visible, audit)
    masked_base = baseline_probabilities(masked_frame, schema, visible, audit)
    assert all(np.array_equal(base[item], masked_base[item]) for item in TARGETS)
    base_truth = truth_probabilities(base, frame, audit)
    original = candidate_indices(codes, initial, audit, bank, k=32)
    masked_original = candidate_indices(masked_codes, initial, audit, bank, k=32)
    assert np.array_equal(original, masked_original)

    u = float(np.log(sizes).mean())
    totals = {name: [np.zeros(len(audit)), np.zeros(len(audit))]
              for name in ("original32", "distinct_union_original32_learned32")}
    sections = {}
    for group_index, (section, indices) in enumerate(zip(SECTIONS, groups)):
        is_active = group_index in active
        if is_active:
            learned32 = candidate_indices(codes, learned[group_index], audit, bank, k=32)
            masked_learned32 = candidate_indices(
                masked_codes, repeated[group_index], audit, bank, k=32)
            assert np.array_equal(learned32, masked_learned32)
            union_rows = [np.union1d(a, b) for a, b in zip(original, learned32)]
            union_sizes = np.array([len(row) for row in union_rows])
            union = np.stack([np.pad(row, (0, union_sizes.max() - len(row)), mode="edge")
                              for row in union_rows])
            masked_union_rows = [np.union1d(a, b)
                                 for a, b in zip(masked_original, masked_learned32)]
            masked_union = np.stack([
                np.pad(row, (0, union_sizes.max() - len(row)), mode="edge")
                for row in masked_union_rows])
            assert np.array_equal(union, masked_union)
        else:
            learned32 = original
            union = original
            union_sizes = np.full(len(audit), 32)
        assert np.isin(original, bank).all() and np.isin(union, bank).all()
        original_bounds = bounds(original, indices, labels, audit, sizes, base_truth)
        if is_active:
            union_bounds = bounds(union, indices, labels, audit, sizes, base_truth)
            union_bounds = (np.maximum(union_bounds[0], original_bounds[0]), union_bounds[1])
            assert np.all(union_bounds[1] >= union_bounds[0] - 1e-10)
        else:
            union_bounds = original_bounds
            assert all(np.array_equal(a, b) for a, b in zip(original_bounds, union_bounds))
        family_bounds = {
            "original32": original_bounds,
            "distinct_union_original32_learned32": union_bounds,
        }
        overlap = 64 - union_sizes if is_active else np.full(len(audit), 32)
        sections[section] = {
            "items": list(SECTIONS[section]),
            "active": is_active,
            "candidate_overlap": {
                "mean_shared_donors": float(overlap.mean()),
                "min_shared_donors": int(overlap.min()),
                "max_shared_donors": int(overlap.max()),
                "mean_shared_fraction": float(overlap.mean() / 32),
                "mean_jaccard": float(np.mean(overlap / union_sizes)),
                "fraction_identical_sets": float(np.mean(overlap == 32)),
                "mean_union_size": float(union_sizes.mean()),
                "max_union_size": int(union_sizes.max()),
            },
            "candidate_sha256": {
                "original32": digest(original),
                "learned32": digest(learned32),
                "distinct_union_padded": digest(union),
            },
            "bounds": {name: summarize(*value, u) for name, value in family_bounds.items()},
        }
        for name, value in family_bounds.items():
            for bound_index in (0, 1):
                totals[name][bound_index] += len(indices) / len(TARGETS) * value[bound_index]

    delta_lower = float((totals["distinct_union_original32_learned32"][0] -
                         totals["original32"][1]).mean())
    delta_upper = float((totals["distinct_union_original32_learned32"][1] -
                         totals["original32"][0]).mean())
    threshold = .005 if seed == 43 else 0.
    return {
        "seed": seed,
        "source_counts": counts,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "source_line_ids_sha256": digest(source_ids),
        "encoded_given_sha256": digest(codes),
        "encoded_target_sha256": digest(labels),
        "schema": schema,
        "split": {"bank": 2000, "metric_fit": 1000, "selection": 1000,
                  "audit": 1000},
        "split_source_ids_sha256": {name: digest(source_ids[rows]) for name, rows in
                                    zip(("bank", "fit", "selection", "audit"), partitions)},
        "baseline_training_rows": 3000,
        "uniform_reference": u,
        "baseline_log_score": float(np.log(base_truth).mean()),
        "baseline_truth_sha256": digest(base_truth),
        "initial_given_weights": dict(zip(GIVEN, initial.tolist())),
        "learned_given_weights": {name: dict(zip(GIVEN, weights.tolist()))
                                  for name, weights in zip(SECTIONS, learned)},
        "active_sections": [list(SECTIONS)[i] for i in active],
        "core_selection_diagnostics": dict(zip(SECTIONS, diagnostics)),
        "bounds": {name: summarize(*value, u) for name, value in totals.items()},
        "union_minus_original": {
            "feasible_minus_upper_log": delta_lower,
            "upper_minus_feasible_log": delta_upper,
            "skill_lower": delta_lower / u,
            "skill_upper": delta_upper / u,
            "skill_div3_lower": delta_lower / u / 3,
            "skill_div3_upper": delta_upper / u / 3,
        },
        "gate_threshold_skill_div3_lower": threshold,
        "seed_gate_pass": delta_lower / u / 3 > threshold,
        "sections": sections,
        "leakage_checks": {
            "all_partitions_disjoint": True,
            "audit_excluded_from_reference_and_baseline_fit": True,
            "audit_label_mask_preserves_fitted_weights": True,
            "audit_label_mask_preserves_activation_and_diagnostics": True,
            "audit_label_mask_preserves_all_candidate_identities": True,
            "audit_label_mask_preserves_baseline_predictions": True,
            "inactive_sections_identical_between_arms": True,
            "modeled_full_row_duplicates_removed_before_split": True,
        },
        "elapsed_seconds": time.perf_counter() - started,
    }


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    runs = []
    with threadpool_limits(limits=2):
        for seed in (43, 44):
            result = run(seed)
            runs.append(result)
            (OUTPUT / f"oracle-seed{seed}.json").write_text(
                json.dumps(result, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({key: result[key] for key in
                              ("seed", "active_sections", "union_minus_original",
                               "seed_gate_pass", "elapsed_seconds")}), flush=True)
    gate_pass = all(result["seed_gate_pass"] for result in runs)
    source_files = ("scripts/oracle_e043.py", "src/models/supervised_retrieval.py",
                    "src/eval/retrieval_oracle.py", "tests/e041_external.py")
    report = {
        "experiment": "E045",
        "seeds": [43, 44],
        "candidate_k_each": 32,
        "oracle_iterations": ITERATIONS,
        "oracle_tolerance": 1e-7,
        "family": "Query-specific SECTION-shared convex weights over held-out logistic base "
                  "and officially floored donor one-hots; no independent per-cell oracle.",
        "candidate_comparison": "Original 32 versus distinct original32 plus learned32 union "
                                "only in active E041 sections; inactive sections identical.",
        "protocol": "Observed Adult, 5000 distinct profiles: bank 2000, metric fit 1000, "
                    "selection 1000, audit 1000. E041 fit_sections and honest logistic base.",
        "gate": "seed43 (union feasible - original upper) / U / 3 > .005 AND seed44 > 0",
        "gate_pass": gate_pass,
        "decision": ("proceed_to_production_evaluation" if gate_pass
                     else "park_E045_without_production_estimator"),
        "immutable_source_sha256": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in source_files
        },
        "interpretation": "Observed Adult candidate headroom only. Oracle reads audit answers; "
                          "not an estimator result, learnability claim, or HSCC forecast.",
        "runs": runs,
    }
    (OUTPUT / "oracle-summary.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("gate_pass", "decision")}), flush=True)


if __name__ == "__main__":
    main()
