"""Fixed-split observed Adult audit of E045; no audit-driven tuning."""

import os

for variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[variable] = "2"

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
                           baseline_probabilities, truth_probabilities, metrics)
from e041_external_learned import evidence, select_blend, paired_delta
from src.models import union_retrieval as model

OUTPUT = ROOT / "docs/analysis/E045-outputs"


def evidence_pair(frame, schema, codes, query, bank, initial, groups, plans, active):
    weights = [plan["original"] if g in active else initial
               for g, plan in enumerate(plans)]
    original = evidence(frame, schema, codes, bank, query, initial, weights, groups)
    options = {item: list(range(len(schema["items"][item]["options"]))) for item in TARGETS}
    expanded = model.union_evidence(
        dict(original), frame, schema["items"], TARGETS, options, codes, query,
        bank, initial, TARGETS, groups, plans, active)
    return original, expanded


def run(seed):
    start = time.perf_counter()
    source = ROOT / "tmp/e041/adult/adult.data"
    observed, source_ids, counts = load_observed(source, seed, rows=5000)
    frame, schema = encode(observed)
    bank, fit = np.arange(2000), np.arange(2000, 3000)
    selection, audit = np.arange(3000, 4000), np.arange(4000, 5000)
    query = np.concatenate((selection, audit))
    codes, labels = frame[GIVEN].to_numpy(dtype=int), frame[TARGETS].to_numpy(dtype=int)
    groups = [[TARGETS.index(item) for item in items] for items in SECTIONS.values()]
    sizes = [len(schema["items"][item]["options"]) for item in TARGETS]
    initial = []
    for j in range(len(GIVEN)):
        frequency = np.bincount(codes[bank, j]) / len(bank)
        initial.append(-np.log(np.clip(np.square(frequency).sum(), 1e-6, 1.)))
    initial = np.asarray(initial)
    plans, active, diagnostics = model.fit_union_sections(
        codes, labels, bank, fit, selection, initial, sizes, groups)
    masked_labels = labels.copy()
    masked_labels[audit] = -1
    repeated, repeated_active, repeated_diagnostics = model.fit_union_sections(
        codes, masked_labels, bank, fit, selection, initial, sizes, groups)
    assert active == repeated_active and diagnostics == repeated_diagnostics
    for first, second in zip(plans, repeated):
        assert first["use_union"] == second["use_union"]
        for key in ("original", "expanded"):
            np.testing.assert_array_equal(first[key], second[key])
    base = baseline_probabilities(frame, schema, np.arange(3000), query)
    original, expanded = evidence_pair(frame, schema, codes, query, bank,
                                       initial, groups, plans, active)
    masked_frame = frame.copy()
    masked_frame.loc[query, TARGETS] = -1
    masked_base = baseline_probabilities(masked_frame, schema, np.arange(3000), query)
    masked_original, masked_expanded = evidence_pair(
        masked_frame, schema, codes, query, bank, initial, groups, plans, active)
    for item in TARGETS:
        np.testing.assert_array_equal(base[item], masked_base[item])
        np.testing.assert_array_equal(original[item], masked_original[item])
        np.testing.assert_array_equal(expanded[item], masked_expanded[item])
        np.testing.assert_allclose(expanded[item].sum(axis=1), 1., atol=1e-12)
    base_truth = truth_probabilities(base, frame, query)
    old_mix, old_share = select_blend(
        base_truth, truth_probabilities(original, frame, query), groups, len(selection))
    new_mix, new_share = select_blend(
        base_truth, truth_probabilities(expanded, frame, query), groups, len(selection))
    old, new = old_mix[len(selection):], new_mix[len(selection):]
    uniform = float(np.log(sizes).mean())
    names = list(SECTIONS)
    return {
        "seed": seed, "source_counts": counts,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "source_ids_sha256": hashlib.sha256(source_ids.tobytes()).hexdigest(),
        "split": {"bank": 2000, "metric_fit": 1000, "selection": 1000, "audit": 1000},
        "active_E041_sections": [names[g] for g in active],
        "union_sections": [names[g] for g in active if plans[g]["use_union"]],
        "selection_diagnostics": dict(zip(names, diagnostics)),
        "retrieval_shares_E041": dict(zip(names, old_share)),
        "retrieval_shares_E045": dict(zip(names, new_share)),
        "audit_E041": metrics(old, schema), "audit_E045": metrics(new, schema),
        "audit_delta": paired_delta(new, old, uniform),
        "audit_probability_max_abs": float(np.max(np.abs(new - old))),
        "leakage_checks": {"audit_mask_preserves_fit_and_selection": True,
                           "masked_query_labels_preserve_base_and_evidence": True},
        "elapsed_seconds": time.perf_counter() - start,
    }


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    results = []
    with threadpool_limits(limits=2):
        for seed in (43, 44):
            result = run(seed)
            results.append(result)
            (OUTPUT / f"observed-seed{seed}.json").write_text(
                json.dumps(result, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({key: result[key] for key in
                              ("seed", "union_sections", "audit_delta", "elapsed_seconds")}), flush=True)
    report = {
        "experiment": "E045", "runs": results,
        "model_sha256": hashlib.sha256((ROOT / "src/models/union_retrieval.py").read_bytes()).hexdigest(),
        "protocol": "Fixed seeds43/44; production union selector; separate audit; same honest "
                    "logistic base with section blends selected on selection only. No audit tuning.",
        "limitations": "Observed Adult, not HSCC. Inactive comparator sections retain the existing "
                       "external protocol's initial-metric top32. Production retains legacy E025 "
                       "inactive evidence and in-sample base replay; this audit does not validate "
                       "those. Oracle headroom is distinct from learned performance.",
    }
    (OUTPUT / "observed-summary.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
