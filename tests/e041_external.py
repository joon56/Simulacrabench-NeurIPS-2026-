"""Observed UCI Adult multioutput retrieval screen; run directly, not with pytest.

Oracle weights see query answers, so oracle scores are NOT estimator scores.
Every oracle shares donor weights across a section, never across one cell only.
"""

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
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.eval.logloss import floor_mix

COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education-num",
    "marital-status", "occupation", "relationship", "race", "sex",
    "capital-gain", "capital-loss", "hours-per-week", "native-country", "income",
]
GIVEN = ["age_band", "education", "race", "sex", "native-country"]
SECTIONS = {
    "family": ["marital-status", "relationship"],
    "employment": ["workclass", "occupation", "hours_band"],
    "finances": ["income", "capital_gain_positive", "capital_loss_positive"],
}
TARGETS = sum(SECTIONS.values(), [])
SOURCE = "https://archive.ics.uci.edu/dataset/2/adult"
DOWNLOAD = "https://archive.ics.uci.edu/static/public/2/adult.zip"


def load_observed(path, seed=41, rows=5000):
    """Binning uses fixed thresholds; no fitted transform sees held-out labels."""
    raw = pd.read_csv(path, names=COLUMNS, skipinitialspace=True)
    frame = raw[GIVEN[1:] + [x for x in TARGETS if x in raw]].copy()
    frame["age_band"] = pd.cut(raw.age, [0, 24, 34, 44, 54, 64, 100],
                               labels=False).astype(str)
    frame["hours_band"] = pd.cut(raw["hours-per-week"], [0, 34, 40, 49, 100],
                                 labels=False).astype(str)
    frame["capital_gain_positive"] = (raw["capital-gain"] > 0).astype(str)
    frame["capital_loss_positive"] = (raw["capital-loss"] > 0).astype(str)
    # Remove repeated modeled profiles to avoid cross-split duplicate shortcuts.
    frame = frame.drop_duplicates(GIVEN + TARGETS)
    unique_rows = len(frame)
    assert len(frame) >= rows
    frame = frame.sample(n=rows, random_state=seed)
    # Preserve original source line as identity, never as a predictor.
    source_ids = frame.index.to_numpy(copy=True)
    frame = frame.reset_index(drop=True)
    assert not frame[GIVEN + TARGETS].duplicated().any()
    assert not set(GIVEN) & set(TARGETS)
    return frame, source_ids, {"source_rows": len(raw), "unique_modeled_rows": unique_rows}


def encode(frame):
    """Option vocabulary is schema metadata; no frequencies fitted here."""
    schema = {"name": "observed_adult_external", "scoring": {"floor": .001},
              "items": {}, "sections": SECTIONS}
    encoded = {}
    for col in GIVEN + TARGETS:
        levels = sorted(frame[col].unique())
        encoded[col] = pd.Categorical(frame[col], categories=levels).codes
        schema["items"][col] = {
            "class": "GIVEN" if col in GIVEN else "PREDICT", "options": levels,
        }
    schema["excluded_raw_fields"] = ["age", "education-num", "fnlwgt",
                                     "hours-per-week", "capital-gain", "capital-loss"]
    return pd.DataFrame(encoded), schema


def baseline_probabilities(frame, schema, train, query):
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
    x = encoder.fit_transform(frame.loc[train, GIVEN])
    xq = encoder.transform(frame.loc[query, GIVEN])
    result = {}
    for item in TARGETS:
        model = LogisticRegression(C=1., max_iter=400)
        model.fit(x, frame.loc[train, item])
        k = len(schema["items"][item]["options"])
        p = np.zeros((len(query), k))
        p[:, model.classes_] = model.predict_proba(xq)
        # Weak marginal smoothing covers any schema option absent from TRAIN.
        marginal = np.bincount(frame.loc[train, item], minlength=k) + 1.
        marginal /= marginal.sum()
        result[item] = .99 * p + .01 * marginal
    return result


def retrieve(frame, train, query, bank_size=64):
    """Only GIVEN values and TRAIN frequencies define candidate identities."""
    assert not set(train) & set(query)
    scores = np.zeros((len(query), len(train)))
    for item in GIVEN:
        r = frame.loc[train, item].to_numpy()
        q = frame.loc[query, item].to_numpy()
        frequency = np.bincount(r, minlength=int(frame[item].max()) + 1)
        rarity = -np.log((frequency + 1.) / (len(train) + len(frequency)))
        scores += (q[:, None] == r[None, :]) * rarity[q, None]
    # Stable deterministic tie-break: TRAIN order, fixed before label access.
    top = np.argsort(-scores, axis=1, kind="stable")[:, :bank_size]
    donors = train[top]
    assert not np.isin(donors, query).any()
    return donors, np.take_along_axis(scores, top, axis=1)


def retrieval_probabilities(frame, schema, donors, scores, k, temperature):
    weights = np.exp((scores[:, :k] - scores[:, :1]) / temperature)
    weights /= weights.sum(axis=1, keepdims=True)
    result = {}
    for item in TARGETS:
        labels = frame[item].to_numpy()[donors[:, :k]]
        levels = len(schema["items"][item]["options"])
        result[item] = (weights[:, :, None] *
                        (labels[:, :, None] == np.arange(levels))).sum(axis=1)
    return result


def truth_probabilities(predictions, frame, query):
    return np.column_stack([
        floor_mix(predictions[item])[np.arange(len(query)), frame.loc[query, item]]
        for item in TARGETS
    ])


def metrics(true_p, schema):
    u = np.mean([np.log(len(schema["items"][i]["options"])) for i in TARGETS])
    log_score = float(np.log(true_p).mean())
    return {"log_score": log_score, "skill": 1. + log_score / u,
            "uniform_reference": float(u)}


def convex_oracle(atom_truth, max_iter=2000, tolerance=1e-6):
    """Optimize section-shared simplex weights by monotonic mixture EM.

    atom_truth shape: query x candidate/base atom x section item.
    Concavity gives optimal log-score <= achieved + Frank-Wolfe dual gap.
    The gap is a per-query, section-mean nats bound, not a statistical CI.
    """
    n, atoms, _ = atom_truth.shape
    weights = np.full((n, atoms), 1. / atoms)
    for iteration in range(max_iter):
        probability = np.einsum("na,nam->nm", weights, atom_truth)
        gradient = (atom_truth / probability[:, None, :]).mean(axis=2)
        gap = np.maximum(gradient.max(axis=1) - 1., 0.)
        if gap.max() < tolerance:
            break
        weights *= gradient
        weights /= weights.sum(axis=1, keepdims=True)
    probability = np.einsum("na,nam->nm", weights, atom_truth)
    gradient = (atom_truth / probability[:, None, :]).mean(axis=2)
    gap = np.maximum(gradient.max(axis=1) - 1., 0.)
    assert np.allclose(weights.sum(axis=1), 1.)
    assert np.all(probability >= .001 - 1e-12)
    return probability, gap, iteration + 1


def run(seed=41, rows=5000, candidate_k=32):
    start = time.perf_counter()
    path = ROOT / "tmp/e041/adult/adult.data"
    observed, source_ids, counts = load_observed(path, seed, rows)
    frame, schema = encode(observed)
    n_train, n_selection = int(rows * .6), int(rows * .2)
    train = np.arange(n_train)
    selection = np.arange(n_train, n_train + n_selection)
    evaluation = np.arange(n_train + n_selection, rows)
    query = np.concatenate([selection, evaluation])
    assert len(set(source_ids)) == rows
    base = baseline_probabilities(frame, schema, train, query)
    donors, scores = retrieve(frame, train, query, candidate_k)
    masked = frame.copy()
    masked.loc[query, TARGETS] = -1
    masked_donors, masked_scores = retrieve(masked, train, query, candidate_k)
    masked_base = baseline_probabilities(masked, schema, train, query)
    assert np.array_equal(donors, masked_donors)
    assert np.array_equal(scores, masked_scores)
    assert all(np.array_equal(base[item], masked_base[item]) for item in TARGETS)
    base_truth = truth_probabilities(base, frame, query)
    # Tune only one global retrieval policy and one global blend on selection.
    policies, configs = [], []
    for k in sorted(set((8, 16, candidate_k))):
        for temperature in (.5, 2., 8.):
            retrieval = retrieval_probabilities(frame, schema, donors, scores, k, temperature)
            retrieval_truth = truth_probabilities(retrieval, frame, query)
            for alpha in (0., .25, .5, .75, 1.):
                policies.append((1. - alpha) * base_truth + alpha * retrieval_truth)
                configs.append({"k": k, "temperature": temperature, "retrieval_weight": alpha})
    policies = np.stack(policies, axis=1)
    selection_scores = np.log(policies[:n_selection]).mean(axis=(0, 2))
    selected = int(selection_scores.argmax())
    pure_options = [i for i, config in enumerate(configs) if config["retrieval_weight"] == 1.]
    pure_selected = max(pure_options, key=lambda i: selection_scores[i])
    fixed = policies[n_selection:, selected]
    # Oracle I: one entire policy/alpha per query section, shared across items.
    policy_oracle = np.empty_like(fixed)
    convex = np.empty_like(fixed)
    sections = {}
    for section, items in SECTIONS.items():
        indices = [TARGETS.index(item) for item in items]
        local = policies[n_selection:][:, :, indices]
        assert local.shape == (len(evaluation), len(configs), len(items))
        choice = np.log(local).mean(axis=2).argmax(axis=1)
        policy_oracle[:, indices] = local[np.arange(len(evaluation)), choice]
        # Oracle II: convex combination of the same GIVEN-only donors + base.
        atom_truth = np.empty((len(evaluation), donors.shape[1] + 1, len(items)))
        for j, item in enumerate(items):
            k = len(schema["items"][item]["options"])
            labels = frame[item].to_numpy()[donors[n_selection:]]
            match = labels == frame.loc[evaluation, item].to_numpy()[:, None]
            atom_truth[:, :-1, j] = .001 + (1. - k * .001) * match
            atom_truth[:, -1, j] = base_truth[n_selection:, TARGETS.index(item)]
        probability, gaps, iterations = convex_oracle(atom_truth)
        convex[:, indices] = probability
        sections[section] = {
            "items": items, "mean_convex_dual_gap_nats": float(gaps.mean()),
            "max_convex_dual_gap_nats": float(gaps.max()), "iterations": iterations,
            "base_log_score": float(np.log(base_truth[n_selection:, indices]).mean()),
            "fixed_log_score": float(np.log(fixed[:, indices]).mean()),
            "policy_oracle_log_score": float(np.log(policy_oracle[:, indices]).mean()),
            "convex_oracle_log_score": float(np.log(probability).mean()),
        }
    # Every policy is admissible in the convex family; optimizer gap bounds residual.
    assert np.log(policy_oracle).mean() >= np.log(fixed).mean() - 1e-12
    weighted_gap = sum(len(SECTIONS[s]) * sections[s]["mean_convex_dual_gap_nats"]
                       for s in SECTIONS) / len(TARGETS)
    assert np.log(convex).mean() + weighted_gap >= np.log(policy_oracle).mean() - 1e-9
    report = {
        "source": {"url": SOURCE, "download_url": DOWNLOAD, "license": "CC BY 4.0",
                   "citation": "Becker, B. & Kohavi, R. (1996). Adult. doi:10.24432/C5XW20",
                   "sha256": hashlib.sha256(path.read_bytes()).hexdigest()},
        "seed": seed, "rows": rows, "candidate_k": candidate_k, "source_counts": counts,
        "split": {"train_reference": n_train,
            "selection": n_selection, "evaluation": len(evaluation)},
        "source_line_ids_sha256": hashlib.sha256(source_ids.tobytes()).hexdigest(),
        "schema": schema, "selected_global_policy": configs[selected],
        "selected_pure_retrieval_policy": configs[pure_selected],
        "selection_global_log_score": float(selection_scores[selected]),
        "methods": {"categorical_logistic": metrics(base_truth[n_selection:], schema),
                    "fixed_global_retrieval": metrics(policies[n_selection:, pure_selected], schema),
                    "fixed_global_retrieval_blend": metrics(fixed, schema),
                    "section_policy_oracle": metrics(policy_oracle, schema),
                    "section_convex_oracle": metrics(convex, schema)},
        "sections": sections, "convex_mean_dual_gap_nats": weighted_gap,
        "oracle_labels_used": True, "per_cell_oracle": False,
        "leakage_checks": {"train_selection_evaluation_disjoint": True,
            "all_query_rows_excluded_from_reference_bank": True,
            "all_query_rows_excluded_from_baseline_fit": True,
            "modeled_full_row_duplicates_removed_before_split": True,
            "raw_target_fields_absent_from_given": True,
            "candidate_rarity_fitted_on_train_only": True,
            "query_target_masking_preserves_candidates_scores_and_baseline": True,
            "global_policy_selected_on_selection_only": True},
        "interpretation": "External observed-data candidate-family headroom, not HSCC forecast. "
            "Oracle reads evaluation answers; no claim those choices are learnable from GIVEN.",
        "elapsed_seconds": time.perf_counter() - start,
    }
    reference = report["methods"]["fixed_global_retrieval_blend"]
    for name, result in report["methods"].items():
        result["delta_log_vs_fixed"] = result["log_score"] - reference["log_score"]
        result["delta_skill_vs_fixed"] = result["skill"] - reference["skill"]
        result["delta_skill_div3_proxy"] = result["delta_skill_vs_fixed"] / 3.
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=41)
    parser.add_argument("--rows", type=int, default=5000)
    parser.add_argument("--candidate-k", type=int, default=32)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "docs/analysis/A008-outputs/e041-external-oracle.json")
    args = parser.parse_args()
    with threadpool_limits(limits=2):
        result = run(args.seed, args.rows, args.candidate_k)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("split", "selected_global_policy", "methods",
                                           "convex_mean_dual_gap_nats", "elapsed_seconds")}, indent=2))
