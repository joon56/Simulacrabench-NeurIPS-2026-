"""Preregistered E043 candidate-pool oracle; never a production estimator."""

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
from src.eval.retrieval_oracle import candidate_indices, mixture_oracle
from src.models.supervised_retrieval import fit_sections

OUTPUT = ROOT / "docs/analysis/E043-outputs"
ITERATIONS = 2000


def digest(array):
    return hashlib.sha256(np.asarray(array).tobytes()).hexdigest()


def bounds(candidates, indices, labels, audit, sizes, base_truth):
    """One simplex per respondent and section, over base plus donor one-hots."""
    matches = (labels[candidates][:, :, indices] ==
               labels[audit][:, None, indices]).transpose(0, 2, 1)
    atoms = .001 + (1. - .001 * sizes[indices][None, :, None]) * matches
    atoms = np.concatenate((base_truth[:, indices, None], atoms), axis=2)
    lower, upper = mixture_oracle(atoms, iterations=ITERATIONS, tolerance=1e-7)
    assert np.all(lower <= upper + 1e-12)
    assert np.all(lower >= np.log(base_truth[:, indices]).mean(axis=1) - 1e-12)
    return lower, upper


def summarize(lower, upper, u):
    lo, hi = float(lower.mean()), float(upper.mean())
    return {"feasible_log_score": lo, "upper_log_score": hi,
            "feasible_skill": 1. + lo / u, "upper_skill": 1. + hi / u,
            "mean_bound_gap_nats": hi - lo,
            "max_query_bound_gap_nats": float(np.max(upper - lower))}


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
    codes, labels = frame[GIVEN].to_numpy(dtype=int), frame[TARGETS].to_numpy(dtype=int)
    groups = [[TARGETS.index(item) for item in items] for items in SECTIONS.values()]
    sizes = np.array([len(schema["items"][item]["options"]) for item in TARGETS])
    initial = []
    for j in range(len(GIVEN)):
        frequency = np.bincount(codes[bank, j]) / len(bank)
        initial.append(-np.log(np.clip(np.square(frequency).sum(), 1e-6, 1.)))
    initial = np.asarray(initial)
    learned, active, diagnostics = fit_sections(codes, labels, bank, fit, selection,
                                                initial, sizes, groups)
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
    old = candidate_indices(codes, initial, audit, bank, k=32)
    assert np.array_equal(old, candidate_indices(masked_codes, initial, audit, bank, k=32))
    u = float(np.log(sizes).mean())
    totals = {name: [np.zeros(len(audit)), np.zeros(len(audit))]
              for name in ("old_pool", "new_pool", "union_larger_family")}
    sections = {}
    for group_index, (section, indices) in enumerate(zip(SECTIONS, groups)):
        new = (candidate_indices(codes, learned[group_index], audit, bank, k=32)
               if group_index in active else old.copy())
        masked_new = (candidate_indices(masked_codes, repeated[group_index], audit, bank, k=32)
                      if group_index in repeated_active else old.copy())
        assert np.array_equal(new, masked_new)
        assert np.isin(old, bank).all() and np.isin(new, bank).all()
        unions = [np.union1d(a, b) for a, b in zip(old, new)]
        union_sizes = np.array([len(row) for row in unions])
        # Duplicate padding changes neither the convex hull nor its optimum.
        union = np.stack([np.pad(row, (0, union_sizes.max() - len(row)), mode="edge")
                          for row in unions])
        old_bounds = bounds(old, indices, labels, audit, sizes, base_truth)
        new_bounds = (bounds(new, indices, labels, audit, sizes, base_truth)
                      if group_index in active else old_bounds)
        union_bounds = bounds(union, indices, labels, audit, sizes, base_truth)
        # Union contains both pools: their feasible points are union-feasible.
        union_bounds = (np.maximum.reduce([union_bounds[0], old_bounds[0], new_bounds[0]]),
                        union_bounds[1])
        assert np.all(union_bounds[1] >= union_bounds[0] - 1e-10)
        family_bounds = dict(zip(totals, (old_bounds, new_bounds, union_bounds)))
        overlap = 64 - union_sizes
        sections[section] = {
            "items": list(SECTIONS[section]), "active": group_index in active,
            "candidate_overlap": {"mean_shared_donors": float(overlap.mean()),
                "min_shared_donors": int(overlap.min()), "max_shared_donors": int(overlap.max()),
                "mean_shared_fraction": float(overlap.mean() / 32),
                "mean_jaccard": float(np.mean(overlap / union_sizes)),
                "fraction_identical_sets": float(np.mean(overlap == 32)),
                "mean_union_size": float(union_sizes.mean()),
                "max_union_size": int(union_sizes.max())},
            "candidate_sha256": {"old": digest(old), "new": digest(new), "union_padded": digest(union)},
            "bounds": {name: summarize(*value, u) for name, value in family_bounds.items()},
        }
        for name, value in family_bounds.items():
            for i in (0, 1):
                totals[name][i] += len(indices) / len(TARGETS) * value[i]
    delta_lower = float((totals["new_pool"][0] - totals["old_pool"][1]).mean())
    delta_upper = float((totals["new_pool"][1] - totals["old_pool"][0]).mean())
    return {"seed": seed, "source_counts": counts, "source_sha256": digest(source.read_bytes()),
        "source_line_ids_sha256": digest(source_ids), "schema": schema,
        "split": {"bank": 2000, "metric_fit": 1000, "selection": 1000, "audit": 1000},
        "split_source_ids_sha256": {name: digest(source_ids[rows]) for name, rows in
                                   zip(("bank", "fit", "selection", "audit"), partitions)},
        "baseline_training_rows": 3000, "uniform_reference": u,
        "baseline_log_score": float(np.log(base_truth).mean()),
        "initial_given_weights": dict(zip(GIVEN, initial.tolist())),
        "learned_given_weights": {name: dict(zip(GIVEN, weights.tolist()))
                                  for name, weights in zip(SECTIONS, learned)},
        "active_sections": [list(SECTIONS)[i] for i in active],
        "core_selection_diagnostics": dict(zip(SECTIONS, diagnostics)),
        "bounds": {name: summarize(*value, u) for name, value in totals.items()},
        "new_minus_old": {"feasible_minus_upper_log": delta_lower,
            "upper_minus_feasible_log": delta_upper, "skill_lower": delta_lower / u,
            "skill_upper": delta_upper / u, "skill_div3_lower": delta_lower / u / 3,
            "skill_div3_upper": delta_upper / u / 3},
        "seed_gate_pass": delta_lower / u / 3 > (.005 if seed == 41 else 0.),
        "sections": sections, "leakage_checks": {
            "all_partitions_disjoint": True, "audit_excluded_from_reference_and_baseline_fit": True,
            "audit_label_mask_preserves_fitted_weights": True,
            "audit_label_mask_preserves_activation_and_diagnostics": True,
            "audit_label_mask_preserves_all_candidate_identities": True,
            "audit_label_mask_preserves_baseline_predictions": True,
            "modeled_full_row_duplicates_removed_before_split": True},
        "elapsed_seconds": time.perf_counter() - started}


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    runs = []
    with threadpool_limits(limits=2):
        for seed in (41, 42):
            result = run(seed)
            runs.append(result)
            (OUTPUT / f"oracle-seed{seed}.json").write_text(
                json.dumps(result, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({key: result[key] for key in
                              ("seed", "active_sections", "new_minus_old", "seed_gate_pass",
                               "elapsed_seconds")}), flush=True)
    report = {"experiment": "E043", "seeds": [41, 42], "candidate_k": 32,
        "oracle_iterations": ITERATIONS, "oracle_tolerance": 1e-7,
        "family": "Query-specific SECTION-shared convex weights over held-out logistic base "
                  "and officially floored donor one-hots; no independent per-cell oracle.",
        "union_family": "Diagnostic larger family over distinct old/new donor union plus base; "
                        "not the proposed 32-candidate implementation or the gate.",
        "protocol": "Unchanged E041 fit_sections defaults and activation. New search uses learned "
                    "weights only for active sections; inactive sections retain old candidates.",
        "gate": "seed41 (new feasible - old upper) / U / 3 > .005 AND seed42 > 0",
        "gate_pass": all(result["seed_gate_pass"] for result in runs),
        "decision": "proceed_to_production_evaluation" if all(r["seed_gate_pass"] for r in runs)
                    else "park_E043_prepare_preregistered_metric_removal_control",
        "immutable_source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ("src/models/supervised_retrieval.py", "src/eval/retrieval_oracle.py",
                         "tests/e041_external.py", "tests/e041_external_learned.py")},
        "interpretation": "Observed Adult candidate headroom only. Oracle reads audit answers; "
                          "not an estimator result, learnability claim, or HSCC forecast.",
        "runs": runs}
    (OUTPUT / "oracle-summary.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("gate_pass", "decision")}), flush=True)


if __name__ == "__main__":
    main()
