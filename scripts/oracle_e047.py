"""E047 preregistered feasible final-evidence oracle, not an estimator score."""

import os

for _variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[_variable] = "2"

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "tests")]
from e041_external import (GIVEN, TARGETS, SECTIONS, SOURCE, DOWNLOAD,
                           load_observed, encode, baseline_probabilities,
                           truth_probabilities, metrics)
from e041_external_learned import ALPHAS, evidence, select_blend, paired_delta
from src.models.supervised_retrieval import fit_sections

SHARES = (0., .25, .5)
PARTITIONS = {"bank": (0, 2000), "metric_fit": (2000, 3000),
              "metric_selection": (3000, 3800), "correction_fit": (3800, 4800),
              "correction_selection": (4800, 5400), "audit": (5400, 6000)}


def section_features(initial, donor, items):
    """Observable features only; scaling belongs to the later correction fit."""
    columns = []
    for item in items:
        first, second = initial[item], donor[item]
        entropy = lambda p: -(p * np.log(np.maximum(p, 1e-300))).sum(axis=1) / np.log(p.shape[1])
        columns.append(np.column_stack((entropy(first), entropy(second),
            first.max(axis=1), second.max(axis=1), (first * second).sum(axis=1),
            (first.argmax(axis=1) == second.argmax(axis=1)).astype(float))))
    mean = np.mean(columns, axis=0)
    return np.column_stack((np.ones(len(mean)), mean))


def run(seed, cache_dir):
    started = time.perf_counter()
    source_path = ROOT / "tmp/e041/adult/adult.data"
    observed, source_ids, counts = load_observed(source_path, seed, rows=6000)
    frame, schema = encode(observed)
    partitions = {name: np.arange(start, stop) for name, (start, stop) in PARTITIONS.items()}
    assert len(np.unique(np.concatenate(list(partitions.values())))) == 6000
    assert len(np.unique(source_ids)) == 6000
    bank, fit, selection = (partitions[name] for name in
                             ("bank", "metric_fit", "metric_selection"))
    visible, query = np.arange(3800), np.arange(3000, 6000)
    correction_rows = np.arange(3800, 6000)
    audit_slice = slice(2400, 3000)
    codes, labels = frame[GIVEN].to_numpy(int), frame[TARGETS].to_numpy(int)
    groups = [[TARGETS.index(item) for item in items] for items in SECTIONS.values()]
    sizes = [len(schema["items"][item]["options"]) for item in TARGETS]
    rarity = np.asarray([-np.log(np.clip(np.square(
        np.bincount(codes[bank, j]) / len(bank)).sum(), 1e-6, 1.))
        for j in range(len(GIVEN))])
    learned, active, diagnostics = fit_sections(codes, labels, bank, fit, selection,
                                                rarity, sizes, groups)
    masked_labels = labels.copy()
    masked_labels[correction_rows] = -1
    repeated, repeated_active, repeated_diagnostics = fit_sections(
        codes, masked_labels, bank, fit, selection, rarity, sizes, groups)
    assert all(np.array_equal(a, b) for a, b in zip(learned, repeated))
    assert active == repeated_active and diagnostics == repeated_diagnostics
    deployed = [metric if group in active else rarity
                for group, metric in enumerate(learned)]
    base = baseline_probabilities(frame, schema, visible, query)
    donor = evidence(frame, schema, codes, bank, query, rarity, deployed, groups)
    masked_frame = frame.copy()
    masked_frame.loc[correction_rows, TARGETS] = -1
    masked_base = baseline_probabilities(masked_frame, schema, visible, query)
    masked_donor = evidence(masked_frame, schema, codes, bank, query, rarity, deployed, groups)
    assert all(np.array_equal(base[item], masked_base[item]) for item in TARGETS)
    assert all(np.array_equal(donor[item], masked_donor[item]) for item in TARGETS)
    base_truth = truth_probabilities(base, frame, query)
    donor_truth = truth_probabilities(donor, frame, query)
    initial_truth, alphas = select_blend(base_truth, donor_truth, groups, len(selection))
    initial = {}
    for items, alpha in zip(SECTIONS.values(), alphas):
        initial.update({item: (1 - alpha) * base[item] + alpha * donor[item] for item in items})
    assert np.allclose(initial_truth, truth_probabilities(initial, frame, query), atol=1e-14)
    # Recompute selection with masked correction labels: only selection labels enter.
    masked_truth, masked_alphas = select_blend(
        truth_probabilities(masked_base, masked_frame, query),
        truth_probabilities(masked_donor, masked_frame, query), groups, len(selection))
    assert alphas == masked_alphas
    for items, alpha in zip(SECTIONS.values(), masked_alphas):
        for item in items:
            assert np.array_equal(initial[item],
                (1 - alpha) * masked_base[item] + alpha * masked_donor[item])
    initial_audit, donor_audit = initial_truth[audit_slice], donor_truth[audit_slice]
    oracle = np.empty_like(initial_audit)
    sections = {}
    for section, group in zip(SECTIONS, groups):
        candidates = np.stack([(1 - a) * initial_audit[:, group] + a * donor_audit[:, group]
                               for a in SHARES], axis=1)
        choice = np.log(candidates).mean(axis=2).argmax(axis=1)
        oracle[:, group] = candidates[np.arange(600), choice]
        sections[section] = {
            "initial_alpha": alphas[list(SECTIONS).index(section)],
            "oracle_share_counts": {str(a): int((choice == j).sum()) for j, a in enumerate(SHARES)},
            "delta_log": float((np.log(oracle[:, group]) - np.log(initial_audit[:, group])).mean())}
    assert np.all(np.log(oracle).mean(axis=1) >= np.log(initial_audit).mean(axis=1) - 1e-14)
    scores = {"initial": metrics(initial_audit, schema), "feasible_oracle": metrics(oracle, schema)}
    delta = paired_delta(oracle, initial_audit, scores["initial"]["uniform_reference"])
    # Cache raw probabilities, not floored values: later fitting must floor once.
    arrays = {"query_rows": query, "labels": labels[query], "source_ids": source_ids,
              "sizes": np.asarray(sizes), "targets": np.asarray(TARGETS),
              "sections": np.asarray(list(SECTIONS)), "initial_alphas": np.asarray(alphas)}
    for item in TARGETS:
        arrays["initial__" + item] = initial[item]
        arrays["evidence__" + item] = donor[item]
    for section, items in SECTIONS.items():
        arrays["features__" + section] = section_features(initial, donor, items)
    for name, rows in partitions.items():
        arrays["partition__" + name] = rows
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"oracle-seed{seed}.npz"
    np.savez_compressed(cache_path, **arrays)
    return {"seed": seed, "rows": 6000, "source_counts": counts,
        "source_line_ids_sha256": hashlib.sha256(source_ids.tobytes()).hexdigest(),
        "split": {name: len(rows) for name, rows in partitions.items()},
        "baseline_fit_rows": len(visible), "initial_mixture_grid": ALPHAS,
        "active_sections": [list(SECTIONS)[i] for i in active],
        "core_selection_diagnostics": dict(zip(SECTIONS, diagnostics)),
        "initial_given_weights": dict(zip(GIVEN, rarity.tolist())),
        "learned_given_weights": {s: dict(zip(GIVEN, w.tolist())) for s, w in zip(SECTIONS, learned)},
        "sections": sections, "audit_methods": scores, "oracle_vs_initial": delta,
        "gate_threshold_skill_div3": .005 if seed == 47 else 0.,
        "gate_passed": bool(delta["delta_skill_div3_proxy"] > (.005 if seed == 47 else 0.)),
        "leakage_checks": {"all_partitions_disjoint": True,
            "correction_rows_excluded_from_every_first_stage_fit_and_selection": True,
            "correction_label_mask_preserves_metrics_activation_base_evidence_initial_mixture": True,
            "distinct_modeled_profiles_before_split": True,
            "audit_labels_used_only_for_oracle_scoring": True},
        "cache_path": str(cache_path.relative_to(ROOT)) if cache_path.is_relative_to(ROOT) else str(cache_path),
        "cache_sha256": hashlib.sha256(cache_path.read_bytes()).hexdigest(),
        "elapsed_seconds": time.perf_counter() - started}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=ROOT / "docs/analysis/A008-outputs/e047-final-evidence-oracle.json")
    parser.add_argument("--cache-dir", type=Path, default=ROOT / "tmp/e047")
    args = parser.parse_args()
    with threadpool_limits(limits=2):
        runs = [run(seed, args.cache_dir) for seed in (47, 48)]
    result = {"experiment": "E047", "oracle_shares": SHARES,
        "protocol": "docs/experiments/E047-adaptive-final-evidence.md",
        "interpretation": "Feasible per-query section-shared extra-evidence headroom, not learnability, "
            "not a continuous optimum and not an HSCC forecast. Oracle sees audit answers.",
        "limitations": "Initial logistic base fits 3800 rows, including metric-selection rows; "
            "initial alpha selection is therefore in-sample for that base, mirroring inherited "
            "E041 replay limitation. Correction-fit, correction-selection and audit remain excluded "
            "from all first-stage fits and initial mixture selection. Adult proxy lacks HSCC gates.",
        "source": {"url": SOURCE, "download_url": DOWNLOAD, "license": "CC BY 4.0",
            "sha256": hashlib.sha256((ROOT / "tmp/e041/adult/adult.data").read_bytes()).hexdigest()},
        "code_sha256": {str(path): hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            for path in ("scripts/oracle_e047.py", "tests/e041_external.py",
                         "tests/e041_external_learned.py", "src/models/supervised_retrieval.py")},
        "runs": runs, "proceed_to_estimator": all(run["gate_passed"] for run in runs)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"proceed_to_estimator": result["proceed_to_estimator"],
        "runs": [{key: run[key] for key in ("seed", "oracle_vs_initial", "gate_passed", "elapsed_seconds")}
                 for run in runs]}, indent=2))


if __name__ == "__main__":
    main()
