"""Fixed-protocol Adult test of E041 fit_sections; no oracle evaluation fitting."""

import os

for _variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[_variable] = "2"

import hashlib
import json
import time

import numpy as np
from scipy.special import softmax
from threadpoolctl import threadpool_limits

from e041_external import (ROOT, GIVEN, TARGETS, SECTIONS, load_observed, encode,
                           baseline_probabilities, truth_probabilities, metrics)
from src.eval.retrieval_oracle import candidate_indices
from src.models.supervised_retrieval import fit_sections

ALPHAS = (0., .1, .25, .5, .75, 1.)


def evidence(frame, schema, codes, bank, query, initial, weights, groups):
    donors = candidate_indices(codes, initial, query, bank, k=32)
    assert not np.isin(donors, query).any()
    features = (codes[query, None, :] == codes[donors]).astype(float)
    result = {}
    for group, metric in zip(groups, weights):
        posterior = softmax(np.einsum("qkd,d->qk", features, metric), axis=1)
        for index in group:
            item = TARGETS[index]
            size = len(schema["items"][item]["options"])
            labels = frame[item].to_numpy()[donors]
            result[item] = (posterior[:, :, None] *
                           (labels[:, :, None] == np.arange(size))).sum(axis=1)
            assert np.allclose(result[item].sum(axis=1), 1.)
    return result


def select_blend(base_truth, retrieval_truth, groups, n_selection):
    """Choose section-shared alpha on selection, then freeze for audit."""
    result, shares = np.empty_like(base_truth), []
    for group in groups:
        candidates = np.stack([(1. - a) * base_truth[:, group] +
                               a * retrieval_truth[:, group] for a in ALPHAS], axis=1)
        score = np.log(candidates[:n_selection]).mean(axis=(0, 2))
        chosen = int(score.argmax())
        result[:, group] = candidates[:, chosen]
        shares.append(ALPHAS[chosen])
    return result, shares


def paired_delta(first, second, u):
    per_respondent = (np.log(first) - np.log(second)).mean(axis=1)
    mean = float(per_respondent.mean())
    se = float(per_respondent.std(ddof=1) / np.sqrt(len(per_respondent)))
    return {"delta_log": mean, "delta_skill": mean / u,
            "delta_skill_div3_proxy": mean / u / 3., "paired_log_standard_error": se,
            "skill_95pct_normal_interval": [(mean - 1.96 * se) / u,
                                             (mean + 1.96 * se) / u]}


def run(seed):
    start = time.perf_counter()
    observed, source_ids, counts = load_observed(ROOT / "tmp/e041/adult/adult.data", seed)
    frame, schema = encode(observed)
    bank, fit = np.arange(2000), np.arange(2000, 3000)
    selection, audit = np.arange(3000, 4000), np.arange(4000, 5000)
    visible, query = np.arange(3000), np.arange(3000, 5000)
    assert len(set(source_ids)) == 5000
    for a in (bank, fit, selection, audit):
        for b in (bank, fit, selection, audit):
            assert a is b or not np.intersect1d(a, b).size
    codes = frame[GIVEN].to_numpy(dtype=int)
    labels = frame[TARGETS].to_numpy(dtype=int)
    groups = [[TARGETS.index(item) for item in items] for items in SECTIONS.values()]
    sizes = [len(schema["items"][item]["options"]) for item in TARGETS]
    initial = []
    for j in range(len(GIVEN)):
        frequency = np.bincount(codes[bank, j]) / len(bank)
        initial.append(-np.log(np.clip(np.square(frequency).sum(), 1e-6, 1.)))
    initial = np.asarray(initial)
    learned, active, diagnostics = fit_sections(codes, labels, bank, fit, selection,
                                                initial, sizes, groups)
    # Audit labels must have no effect on training, selection, or predictions.
    masked_labels = labels.copy()
    masked_labels[audit] = -1
    repeated, repeated_active, repeated_diagnostics = fit_sections(
        codes, masked_labels, bank, fit, selection, initial, sizes, groups)
    assert all(np.array_equal(a, b) for a, b in zip(learned, repeated))
    assert active == repeated_active and diagnostics == repeated_diagnostics
    # Selector answers may choose sections, but cannot change learned weights.
    changed_selection = labels.copy()
    changed_selection[selection] = 0
    refitted, _, _ = fit_sections(codes, changed_selection, bank, fit, selection,
                                  initial, sizes, groups)
    assert all(np.array_equal(a, b) for a, b in zip(learned, refitted))
    deployed = [metric if group in active else initial
                for group, metric in enumerate(learned)]
    base = baseline_probabilities(frame, schema, visible, query)
    fixed = evidence(frame, schema, codes, bank, query, initial,
                     [initial] * len(groups), groups)
    supervised = evidence(frame, schema, codes, bank, query, initial, deployed, groups)
    masked_frame = frame.copy()
    masked_frame.loc[query, TARGETS] = -1
    masked_base = baseline_probabilities(masked_frame, schema, visible, query)
    masked_supervised = evidence(masked_frame, schema, codes, bank, query,
                                initial, deployed, groups)
    assert all(np.array_equal(base[i], masked_base[i]) for i in TARGETS)
    assert all(np.array_equal(supervised[i], masked_supervised[i]) for i in TARGETS)
    base_truth = truth_probabilities(base, frame, query)
    fixed_truth = truth_probabilities(fixed, frame, query)
    learned_truth = truth_probabilities(supervised, frame, query)
    fixed_mix, fixed_alpha = select_blend(base_truth, fixed_truth, groups, 1000)
    learned_mix, learned_alpha = select_blend(base_truth, learned_truth, groups, 1000)
    predictions = {"categorical_logistic": base_truth[1000:],
                   "fixed_retrieval_base": fixed_mix[1000:],
                   "supervised_section_retrieval_base": learned_mix[1000:]}
    result = {"seed": seed, "source_counts": counts,
              "source_line_ids_sha256": hashlib.sha256(source_ids.tobytes()).hexdigest(),
              "split": {"bank": 2000, "metric_fit": 1000, "selection": 1000, "audit": 1000},
              "initial_given_weights": dict(zip(GIVEN, initial.tolist())),
              "learned_given_weights": {s: dict(zip(GIVEN, w.tolist()))
                                        for s, w in zip(SECTIONS, learned)},
              "active_sections": [list(SECTIONS)[i] for i in active],
              "core_selection_diagnostics": dict(zip(SECTIONS, diagnostics)),
              "fixed_retrieval_alpha": dict(zip(SECTIONS, fixed_alpha)),
              "supervised_retrieval_alpha": dict(zip(SECTIONS, learned_alpha)),
              "audit_methods": {name: metrics(p, schema) for name, p in predictions.items()},
              "audit_deltas": {}, "sections": {},
              "leakage_checks": {"all_partitions_disjoint": True,
                  "audit_label_mask_preserves_metric_and_active_sections": True,
                  "selection_label_change_preserves_fitted_metric": True,
                  "query_label_mask_preserves_base_and_evidence_predictions": True},
              "elapsed_seconds": time.perf_counter() - start}
    u = result["audit_methods"]["categorical_logistic"]["uniform_reference"]
    for name, prediction in predictions.items():
        result["audit_deltas"][name + "_vs_base"] = paired_delta(
            prediction, predictions["categorical_logistic"], u)
    result["audit_deltas"]["supervised_vs_fixed"] = paired_delta(
        predictions["supervised_section_retrieval_base"], predictions["fixed_retrieval_base"], u)
    for name, indices in zip(SECTIONS, groups):
        result["sections"][name] = {method: float(np.log(p[:, indices]).mean())
                                    for method, p in predictions.items()}
    return result


if __name__ == "__main__":
    with threadpool_limits(limits=2):
        result = {
            "revision": "v2: reviewed core selector compares incumbent top10 to new top32; "
                "external protocol unchanged, including its fixed top32 comparator. "
                "v1 outputs preserved. Correction was not audit-driven tuning.",
            "protocol": "Fixed before audit: top32 bank-only collision rarity; production "
                "fit_sections defaults and active section selection; same honest logistic base "
                "for both retrieval arms; per-section alpha in [0,.1,.25,.5,.75,1] chosen on "
                "selection only. No audit-driven parameter changes.",
            "limitations": "External distinct Adult profiles, not HSCC forecast. This tests "
                "fit_sections with honest held-out logistic probabilities. Production retains "
                "E025 legacy lambda replay; that separate limitation is not exercised here.",
            "model_sha256": hashlib.sha256(
                (ROOT / "src/models/supervised_retrieval.py").read_bytes()).hexdigest(),
            "runs": [run(41), run(42)],
        }
    output = ROOT / "docs/analysis/A008-outputs/e041-external-learned.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for run_result in result["runs"]:
        print(json.dumps({k: run_result[k] for k in ("seed", "active_sections",
            "fixed_retrieval_alpha", "supervised_retrieval_alpha", "audit_methods",
            "audit_deltas", "elapsed_seconds")}, indent=2))
