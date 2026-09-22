"""Preregistered E046 finite Adult tree-mixture oracle, not an HSCC forecast.

Run directly with the repository Python environment. Both seeds and every
hyperparameter are fixed before execution; no download or production fit.
"""

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
import sklearn
from sklearn.ensemble import HistGradientBoostingClassifier
from threadpoolctl import threadpool_limits

from e041_external import (
    GIVEN, TARGETS, SECTIONS, SOURCE, load_observed, encode,
    baseline_probabilities, truth_probabilities, metrics,
)

OUTPUT = ROOT / "docs/analysis/E046-outputs"
WEIGHTS = (0., .25, .5)
TREE_PARAMETERS = {
    "max_iter": 40,
    "max_leaf_nodes": 15,
    "learning_rate": .1,
    "early_stopping": False,
    "random_state": 0,
    "categorical_features": GIVEN,
}


def digest(array):
    return hashlib.sha256(np.ascontiguousarray(array).tobytes()).hexdigest()


def tree_probabilities(frame, schema, fit, query):
    """Fit uses only fit labels; prediction receives only GIVEN columns."""
    x = frame.loc[fit, GIVEN]
    x_query = frame.loc[query, GIVEN]
    result = {}
    for item in TARGETS:
        model = HistGradientBoostingClassifier(**TREE_PARAMETERS)
        model.fit(x, frame.loc[fit, item])
        k = len(schema["items"][item]["options"])
        p = np.zeros((len(query), k))
        p[:, model.classes_] = model.predict_proba(x_query)
        assert np.isfinite(p).all() and (p >= 0).all()
        assert np.allclose(p.sum(axis=1), 1.)
        result[item] = p
    return result


def paired_gain(candidate_log, base_log):
    """Cluster uncertainty by respondent, preserving target dependence."""
    row_gain = (candidate_log - base_log).mean(axis=1)
    return {
        "mean_log_gain_nats": float(row_gain.mean()),
        "respondent_se_nats": float(row_gain.std(ddof=1) / np.sqrt(len(row_gain))),
        "respondents": len(row_gain),
    }


def choose_sections(selection_logs):
    """Selection input excludes audit entirely; smallest weight breaks ties."""
    choices, diagnostics = {}, {}
    for section, items in SECTIONS.items():
        indices = [TARGETS.index(item) for item in items]
        local = selection_logs[:, :, indices]
        best = int(local.mean(axis=(1, 2)).argmax())
        gain = paired_gain(local[best], local[0])
        threshold = max(.001, 2. * gain["respondent_se_nats"])
        accepted = gain["mean_log_gain_nats"] > threshold
        choices[section] = best if accepted else 0
        diagnostics[section] = {
            "items": items,
            "best_weight": WEIGHTS[best],
            "selected_weight": WEIGHTS[choices[section]],
            "selection_log_scores": dict(zip(
                map(str, WEIGHTS), local.mean(axis=(1, 2)).tolist())),
            **gain,
            "acceptance_threshold_nats": threshold,
            "selection_accepted": accepted,
        }
    return choices, diagnostics


def section_policy(logs, choices):
    result = logs[0].copy()
    for section, index in choices.items():
        indices = [TARGETS.index(item) for item in SECTIONS[section]]
        result[:, indices] = logs[index][:, indices]
    return result


def run(seed):
    assert seed in (45, 46)
    started = time.perf_counter()
    source = ROOT / "tmp/e041/adult/adult.data"
    observed, source_ids, counts = load_observed(source, seed, rows=5000)
    frame, schema = encode(observed)
    fit = np.arange(3000)
    selection = np.arange(3000, 4000)
    audit = np.arange(4000, 5000)
    query = np.concatenate((selection, audit))
    partitions = {"fit": fit, "selection": selection, "audit": audit}
    assert len(np.unique(np.concatenate(list(partitions.values())))) == 5000
    assert len(set(source_ids)) == 5000
    assert not set(GIVEN) & set(TARGETS)

    # The actual fit/prediction path sees no selection or audit target values.
    masked = frame.copy()
    masked.loc[query, TARGETS] = -1
    base = baseline_probabilities(masked, schema, fit, query)
    tree = tree_probabilities(masked, schema, fit, query)

    # Verify invariance, including refitting, against the original query labels.
    unmasked_base = baseline_probabilities(frame, schema, fit, query)
    unmasked_tree = tree_probabilities(frame, schema, fit, query)
    assert all(np.array_equal(base[item], unmasked_base[item]) for item in TARGETS)
    assert all(np.array_equal(tree[item], unmasked_tree[item]) for item in TARGETS)
    del unmasked_base, unmasked_tree

    # Enumerate the complete finite family. Floor each final vector once.
    truths = []
    for weight in WEIGHTS:
        mixture = {item: (1. - weight) * base[item] + weight * tree[item]
                   for item in TARGETS}
        truths.append(truth_probabilities(mixture, frame, query))
    logs = np.log(np.stack(truths))
    assert logs.shape == (3, 2000, len(TARGETS))
    selection_logs, audit_logs = logs[:, :1000], logs[:, 1000:]
    choices, selection_diagnostics = choose_sections(selection_logs)

    # One weight per head, constant across all audit respondents. Separability
    # makes these three comparisons per head exact enumeration of 3**8 policies.
    head_choices = audit_logs.mean(axis=1).argmax(axis=0)
    oracle_log = np.column_stack([
        audit_logs[head_choices[j], :, j] for j in range(len(TARGETS))])
    honest_log = section_policy(audit_logs, choices)
    base_log = audit_logs[0]
    assert oracle_log.mean() >= honest_log.mean() - 1e-12
    assert oracle_log.mean() >= base_log.mean() - 1e-12

    # Audit only accepts/rejects the frozen selection policy; no audit retuning.
    audit_gain = paired_gain(honest_log, base_log)
    audit_threshold = max(0., audit_gain["respondent_se_nats"])
    audit_pass = audit_gain["mean_log_gain_nats"] > audit_threshold
    accepted_log = honest_log if audit_pass else base_log
    methods = {
        "categorical_logistic": metrics(np.exp(base_log), schema),
        "categorical_tree": metrics(truth_probabilities(tree, frame, query)[1000:], schema),
        "constant_headwise_oracle": metrics(np.exp(oracle_log), schema),
        "selection_only_section_policy": metrics(np.exp(honest_log), schema),
        "audit_guarded_section_policy": metrics(np.exp(accepted_log), schema),
    }
    reference = methods["categorical_logistic"]
    for result in methods.values():
        result["delta_log_vs_baseline"] = result["log_score"] - reference["log_score"]
        result["delta_skill_vs_baseline"] = result["skill"] - reference["skill"]
        result["delta_skill_div3_proxy"] = result["delta_skill_vs_baseline"] / 3.
    oracle_gain = methods["constant_headwise_oracle"]["delta_skill_div3_proxy"]
    threshold = .005 if seed == 45 else 0.
    source_files = ("scripts/oracle_e046.py", "tests/e041_external.py",
                    "src/eval/logloss.py", "docs/experiments/E046-honest-tree-selector.md")
    return {
        "experiment": "E046",
        "seed": seed,
        "source": {"url": SOURCE, "license": "CC BY 4.0",
                   "sha256": hashlib.sha256(source.read_bytes()).hexdigest()},
        "source_counts": counts,
        "source_line_ids_sha256": digest(source_ids),
        "split": {name: len(rows) for name, rows in partitions.items()},
        "split_source_ids_sha256": {
            name: digest(source_ids[rows]) for name, rows in partitions.items()},
        "encoded_given_sha256": digest(frame[GIVEN].to_numpy(dtype=np.int64)),
        "encoded_target_sha256": digest(frame[TARGETS].to_numpy(dtype=np.int64)),
        "source_files_sha256": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in source_files},
        "runtime_versions": {"python": sys.version, "numpy": np.__version__,
                             "scikit_learn": sklearn.__version__},
        "schema": schema,
        "tree_parameters": TREE_PARAMETERS,
        "baseline": "Unchanged e041_external.baseline_probabilities, fit rows only.",
        "weight_grid": WEIGHTS,
        "threshold_units": "Paired respondent mean log-score gain, nats per scored cell.",
        "methods": methods,
        "oracle": {
            "family": "One constant weight per head across every audit respondent.",
            "finite_policy_count": len(WEIGHTS) ** len(TARGETS),
            "optimization": "Exact separable enumeration; no numerical optimization gap.",
            "uses_audit_labels": True,
            "per_respondent_or_cell_choices": False,
            "head_weights": dict(zip(TARGETS, [WEIGHTS[i] for i in head_choices])),
            "head_audit_log_scores": {
                item: dict(zip(map(str, WEIGHTS), audit_logs[:, :, j].mean(axis=1).tolist()))
                for j, item in enumerate(TARGETS)},
            "bound_scope": "Upper bound on the finite section-shared mixture family "
                           "on these Adult audit rows only.",
        },
        "honest_selection": selection_diagnostics,
        "honest_audit": {
            **audit_gain,
            "acceptance_threshold_nats": audit_threshold,
            "audit_guard_pass": audit_pass,
            "fallback_to_baseline": not audit_pass,
            "audit_retuning": False,
            "section_diagnostics": {
                section: paired_gain(
                    honest_log[:, [TARGETS.index(item) for item in items]],
                    base_log[:, [TARGETS.index(item) for item in items]])
                for section, items in SECTIONS.items()},
        },
        "gate_threshold_skill_div3_proxy": threshold,
        "seed_gate_pass": bool(oracle_gain > threshold),
        "leakage_checks": {
            "fit_selection_audit_disjoint": True,
            "identical_3000_fit_rows_for_both_models": True,
            "all_query_targets_masked_in_actual_fit_path": True,
            "query_label_mask_preserves_baseline_predictions_after_refit": True,
            "query_label_mask_preserves_tree_predictions_after_refit": True,
            "model_predict_inputs_contain_given_only": True,
            "section_choice_function_receives_selection_only": True,
            "modeled_full_row_duplicates_removed_before_split": True,
            "raw_target_fields_absent_from_given": True,
            "schema_option_vocabulary_only_uses_all_rows_as_in_E041": True,
        },
        "interpretation": "Observed Adult proxy bound only. Oracle reads audit labels; "
                          "not a learnability claim, survey-gating replica, or HSCC forecast. "
                          "The all-row option vocabulary follows the unchanged E041 schema proxy.",
        "elapsed_seconds": time.perf_counter() - started,
    }


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    runs = []
    with threadpool_limits(limits=2):
        for seed in (45, 46):
            result = run(seed)
            runs.append(result)
            (OUTPUT / f"oracle-seed{seed}.json").write_text(
                json.dumps(result, indent=2) + "\n", encoding="utf-8")
            print(json.dumps({key: result[key] for key in
                              ("seed", "methods", "honest_audit", "seed_gate_pass",
                               "elapsed_seconds")}), flush=True)
    gate_pass = all(result["seed_gate_pass"] for result in runs)
    print(json.dumps({
        "joint_gate_pass": gate_pass,
        "decision": "proceed_to_production_evaluation" if gate_pass
                    else "park_E046_without_production_estimator",
        "interpretation": "Adult proxy-only bound; no HSCC forecast.",
    }), flush=True)


if __name__ == "__main__":
    main()
