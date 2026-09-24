"""A011 fixed paired replay audit; deliberately included labels are diagnostic only.

No new estimator, optimized lambda, source modification, or DEV label scoring.
Positive gradients mean pressure toward more evidence. At lambda zero and the
legacy clipping kink, report the right derivative. Official gradients include
normalization of the entire mixed vector. All evidence is frozen from honest
E041; missing evidence stays missing. Bootstrap intervals are descriptive,
conditional on these fits, without training variability or multiplicity control.
"""

import argparse
from copy import deepcopy
import gzip
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import pickle
import sys
import time

for variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[variable] = "2"
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import torch

from src.eval.recursive_candidates import cached_renderer, mask_query
from src.eval.logloss import floor_mix
from src.models import hh_cap, supervised_retrieval
from src.models.hier_backoff import _layout
from src.models.prob_link import EV_FLOOR

PROTOCOL = "A011-paired-400CAL-400CTRL-split5301-bootstrap5302-v1"
OUTPUT = ROOT / "docs/analysis/A011-outputs"
GROUP_SIZE = 400
BOOTSTRAPS = 1000


def digest(data):
    return hashlib.sha256(data).hexdigest()


def readonly(value):
    """Freeze owned array copies recursively, including captured evidence."""
    if isinstance(value, np.ndarray):
        result = value.copy()
        result.flags.writeable = False
        return result
    if isinstance(value, dict):
        return {k: readonly(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return type(value)(readonly(v) for v in value)
    return value


def partition_rows(frame, schema):
    predicted = [n for n, r in schema["items"].items() if r["class"] == "PREDICT"]
    missing = frame[predicted].isna().to_numpy()
    if np.any(missing.any(axis=1) != missing.all(axis=1)):
        raise ValueError("Require whole PREDICT blocks for original DEV")
    visible = np.flatnonzero(~missing.any(axis=1))
    if len(visible) <= 2 * GROUP_SIZE:
        raise ValueError("Need more than 800 fully visible TRAIN rows")
    order = np.random.default_rng(5301).permutation(visible)
    return {"CAL": order[:GROUP_SIZE], "CTRL": order[GROUP_SIZE:2*GROUP_SIZE],
            "FIT": order[2*GROUP_SIZE:], "DEV": np.flatnonzero(missing.any(axis=1))}


def paired_frames(frame, schema, partitions):
    honest = mask_query(frame, schema, np.r_[partitions["CAL"], partitions["CTRL"]])
    included = mask_query(frame, schema, partitions["CTRL"])
    return honest, included


def prepare_case(case):
    if case == "adult":
        from scripts.screen_e050_e051 import ADULT_SOURCE, adapt_adult
        from tests.e041_external import load_observed
        observed, source_ids, counts = load_observed(ADULT_SOURCE, 53, rows=5000)
        frame, schema = adapt_adult(observed)
        return frame, schema, {"adult_seed": 53, "source_ids": source_ids.tolist(),
                               "source_file_sha256": digest(ADULT_SOURCE.read_bytes()),
                               "counts": counts, "vocabulary": "full sampled 5000 rows",
                               "no_fabricated_gates": True}
    from scripts.check_daily_retrieval import get_case
    _, schema, frame, _, _, case_hash = get_case("unhcr", case)
    return frame, schema, {"case_sha256": case_hash,
                           "household_seed": 13 if case == "household" else None}


def provenance(frame, schema, partitions):
    paths = sorted((ROOT / "src").rglob("*.py")) + [
        Path(__file__), ROOT / "scripts/check_daily_retrieval.py",
        ROOT / "scripts/screen_e050_e051.py", ROOT / "tests/e041_external.py",
        ROOT / "tests/test_hh_sharp.py", ROOT / "external/starter-kit/score.py",
        ROOT / "external/starter-kit/make_sandbox.py",
        ROOT / "external/starter-kit/config.yml"]
    hashes = {p.relative_to(ROOT).as_posix(): digest(p.read_bytes()) for p in paths}
    return {"source_hashes": hashes,
            "source_sha256": digest(json.dumps(hashes, sort_keys=True).encode()),
            "frame_sha256": digest(pickle.dumps((schema, frame), protocol=5)),
            "partition_sha256": digest(pickle.dumps(partitions, protocol=5)),
            "versions": {n: version(n) for n in ("numpy", "pandas", "torch", "scipy", "scikit-learn")}}


def capture_fit(frame, schema, rows, honest):
    """One actual generic E041 render; private cache namespace per fitted arm."""
    captured = {}
    records, items, _ = _layout(frame, schema)
    predicted = [n for n in items if records[n]["class"] == "PREDICT"]
    query = np.flatnonzero(frame[predicted].isna().any(axis=1))

    def layer(f, s, model_dists):
        if captured:
            raise AssertionError("Unexpected second layer callback")
        captured["full_head"] = readonly({n: model_dists[n][rows] for n in predicted})
        evidence, lambdas = supervised_retrieval.supervised_layer(f, s, model_dists) if honest else ({}, {})
        captured["evidence_rows"] = readonly(evidence)
        captured["lambdas"] = deepcopy(lambdas)
        captured["layer_diagnostics"] = deepcopy(supervised_retrieval.LAST_DIAGNOSTICS) if honest else {}
        return evidence, lambdas

    # Generic rendering matters for Adult: ordinary predict dispatch uses E025.
    raw = cached_renderer()(frame, schema, layer_fn=layer, configs=hh_cap.CONFIGS)
    if len(raw) != len(query) * len(predicted):
        raise ValueError("Recursive outputs must cover every masked block")
    captured["recursive"] = {n: np.stack(raw[i::len(predicted)]) for i, n in enumerate(predicted)}
    captured["query"] = query
    return readonly(captured)


def check_probability(probability):
    if not np.isfinite(probability).all() or np.min(probability) < -1e-7:
        raise ValueError("Invalid probabilities")
    if not np.allclose(probability.sum(axis=1), 1., atol=2e-6, rtol=0):
        raise ValueError("Invalid probability normalization")


def reconstruct_base(final, evidence, effective_lambda):
    shares = np.asarray(effective_lambda)
    if np.any((shares < 0) | (shares >= 1)) or not np.isfinite(shares).all():
        raise ValueError("Cannot invert effective lambda outside [0,1)")
    result = np.array(final, dtype=float, copy=True)
    active = shares > 0
    result[active] = (final[active] - shares[active, None] * evidence[active]) / (1-shares[active, None])
    check_probability(result)
    rebuilt = result.copy()
    rebuilt[active] = (1-shares[active, None])*result[active] + shares[active, None]*evidence[active]
    if not np.allclose(rebuilt, final, atol=1e-12, rtol=0):
        raise ValueError("Own-evidence reconstruction failed")
    return result


def derive_honest(captured, rows):
    positions = {int(row): i for i, row in enumerate(captured["query"])}
    selected = np.array([positions[int(row)] for row in rows])
    result = {name: {} for name in ("final", "evidence", "concentration", "effective_lambda", "gate_base")}
    for item, full in captured["full_head"].items():
        check_probability(full)
        final = captured["recursive"][item][selected]
        check_probability(final)
        evidence = np.full_like(final, np.nan, dtype=float)
        concentration = np.full(len(rows), -1, dtype=int)
        effective = np.zeros(len(rows))
        for i, row in enumerate(rows):
            entry = captured["evidence_rows"].get(int(row))
            if entry is None or item not in entry[0]:
                continue
            evidence[i] = entry[0][item]
            concentration[i] = int(entry[1])
            pair = captured["lambdas"].get(item)
            if pair is not None and evidence[i].sum() > 0:
                effective[i] = max(0., pair[int(entry[1])])
        valid = np.isfinite(evidence).all(axis=1) & (evidence.sum(axis=1) > 0)
        if valid.any():
            check_probability(evidence[valid])
        result["final"][item] = final
        result["evidence"][item] = evidence
        result["concentration"][item] = concentration
        result["effective_lambda"][item] = effective
        result["gate_base"][item] = reconstruct_base(final, evidence, effective)
    return readonly(result)


def log_gradient(base, evidence, labels, shares, objective):
    """Per-cell log-score derivative; right derivative at clipping kinks."""
    rows = np.arange(len(labels))
    if objective == "legacy":
        model = np.maximum(base[rows, labels], EV_FLOOR)
        direction = evidence[rows, labels] - model
        mixture = model + shares * direction
        return np.where((mixture > EV_FLOOR) | ((mixture == EV_FLOOR) & (direction > 0)),
                        direction / np.maximum(mixture, EV_FLOOR), 0.)
    if objective != "official":
        raise ValueError(f"Unknown objective: {objective}")
    direction = evidence - base
    mixed = base + shares[:, None] * direction
    total, change = mixed.sum(axis=1), direction.sum(axis=1)
    probability = mixed[rows, labels] / total
    derivative = (direction[rows, labels] * total - mixed[rows, labels] * change) / total**2
    scale = 1 - EV_FLOOR * base.shape[1]
    return scale * derivative / (EV_FLOOR + scale * probability)


def bootstrap_indices(ncal, nctrl):
    rng = np.random.default_rng(5302)
    return (rng.integers(ncal, size=(BOOTSTRAPS, ncal)),
            rng.integers(nctrl, size=(BOOTSTRAPS, nctrl)))


def summarize(values, draws):
    values = np.asarray(values, dtype=float)
    if values.ndim == 1:
        values = values[:, None]
    finite = np.isfinite(values)
    row_sum = np.where(finite, values, 0.).sum(axis=1)
    row_count = finite.sum(axis=1)
    if row_count.sum() == 0:
        return {"rows": 0, "cells": 0, "mean": None, "interval95": None}, np.full(len(draws), np.nan)
    samples = row_sum[draws].sum(axis=1) / row_count[draws].sum(axis=1)
    return {"rows": int((row_count > 0).sum()), "cells": int(row_count.sum()),
            "mean": float(row_sum.sum()/row_count.sum()),
            "interval95": np.quantile(samples, [.025, .975]).tolist()}, samples


def paired_summary(cal, ctrl, draws=None):
    if draws is None:
        draws = bootstrap_indices(len(cal), len(ctrl))
    first, first_samples = summarize(cal, draws[0])
    second, second_samples = summarize(ctrl, draws[1])
    delta = None if first["mean"] is None or second["mean"] is None else first["mean"]-second["mean"]
    interval = None if delta is None else np.quantile(first_samples-second_samples, [.025, .975]).tolist()
    return {"CAL": first, "CTRL": second, "CAL_minus_CTRL": {"mean": delta, "interval95": interval}}


def score_capture(frozen, labels, schema):
    names = list(labels)
    derived = frozen["derived"]
    ncal = len(frozen["partitions"]["CAL"])
    nctrl = len(frozen["partitions"]["CTRL"])
    nrows = ncal+nctrl
    draws = bootstrap_indices(ncal, nctrl)
    gated = np.array([bool(schema["items"][n].get("gate")) for n in names])
    group_columns = {"all": np.arange(len(names)), "gated": np.flatnonzero(gated),
                     "ungated": np.flatnonzero(~gated)}
    membership, mismatch, probability_distance = [], [], []
    gradients = {objective: {arm: np.full((nrows, len(names)), np.nan) for arm in
                             ("honest_full", "included_full", "gate_base")}
                 for objective in ("legacy", "official")}
    for j, item in enumerate(names):
        honest = frozen["honest"]["full_head"][item]
        included = frozen["included"]["full_head"][item]
        base = derived["gate_base"][item]
        check_probability(included)
        logs = [np.log(floor_mix(p)[np.arange(nrows), labels[item]]) for p in (honest, included, base)]
        membership.append(logs[1]-logs[0])
        mismatch.append(logs[2]-logs[0])
        probability_distance.append(.5*np.abs(base-honest).sum(axis=1))
        ev = derived["evidence"][item]
        valid = np.isfinite(ev).all(axis=1) & (ev.sum(axis=1)>0)
        for objective, arms in gradients.items():
            for arm, probability in zip(arms, (honest, included, base)):
                if valid.any():
                    arms[arm][valid, j] = log_gradient(probability[valid], ev[valid], labels[item][valid],
                                                      derived["effective_lambda"][item][valid], objective)
    result = {"protocol": PROTOCOL, "case": frozen["case"], "scored_rows": nrows,
              "DEV_scored": False, "included_arm_is_out_of_sample": False,
              "bootstrap": {"draws": BOOTSTRAPS, "seed": 5302, "unit": "respondent",
                            "independent_CAL_CTRL": True, "conditional_on_fits": True},
              "membership": {}, "gate_mismatch": {}, "gate_probability_total_variation": {},
              "gradients": {}, "evidence_coverage": {}}
    for key, cells in (("membership", membership), ("gate_mismatch", mismatch),
                       ("gate_probability_total_variation", probability_distance)):
        matrix = np.column_stack(cells)
        for group, columns in group_columns.items():
            if len(columns):
                result[key][group] = paired_summary(matrix[:ncal, columns], matrix[ncal:, columns], draws)
        result[key]["per_item"] = {n: paired_summary(matrix[:ncal, j], matrix[ncal:, j], draws)
                                   for j, n in enumerate(names)}
    pooled_draws = np.concatenate((draws[0], draws[1]+ncal), axis=1)
    subsets = {"CAL": (np.arange(ncal), draws[0]), "CTRL": (np.arange(ncal, nrows), draws[1]),
               "pooled": (np.arange(nrows), pooled_draws)}
    for j, item in enumerate(names):
        valid = np.isfinite(gradients["official"]["honest_full"][:, j])
        result["evidence_coverage"][item] = {part: int(valid[rows].sum()) for part, (rows, _) in subsets.items()}
    for objective, arms in gradients.items():
        report = {"groups": {}, "item_buckets": []}
        for part, (rows, resamples) in subsets.items():
            report["groups"][part] = {}
            for group, columns in group_columns.items():
                if not len(columns):
                    continue
                selected = {arm: values[np.ix_(rows, columns)] for arm, values in arms.items()}
                if (np.isfinite(selected["honest_full"]).any(axis=1)).sum() < 30:
                    continue
                report["groups"][part][group] = {arm: summarize(values, resamples)[0]
                                                  for arm, values in selected.items()}
            for j, item in enumerate(names):
                for bucket in (0, 1):
                    valid = (derived["concentration"][item][rows] == bucket) & np.isfinite(arms["honest_full"][rows, j])
                    if valid.sum() < 30:
                        continue
                    summaries = {arm: summarize(np.where(valid, values[rows, j], np.nan), resamples)[0]
                                 for arm, values in arms.items()}
                    report["item_buckets"].append({"partition": part, "item": item, "bucket": bucket,
                        "rows": int(valid.sum()), "lambda": float(derived["effective_lambda"][item][rows[valid][0]]),
                        "slopes": summaries,
                        "membership_sign_flip": bool(summaries["honest_full"]["mean"]*summaries["included_full"]["mean"]<0),
                        "gate_sign_flip": bool(summaries["honest_full"]["mean"]*summaries["gate_base"]["mean"]<0)})
        result["gradients"][objective] = report
    result["limitations"] = [
        "Included fit has 400 additional labels; CAL-minus-CTRL is not a perfect causal adjustment.",
        "Gradient signs indicate local frozen-evidence pressure, not gains from a fitted policy.",
        "Intervals ignore training variability and multiple testing; no significance-driven follow-up.",
        "Respondent resampling does not model shared donor or household dependence.",
        "Gate-base gradients hold upstream beliefs fixed, not total derivatives through descendants.",
        "Absent captured evidence remains absent; Adult has no humanitarian gate semantics."]
    return result


def flatten_arrays(value, prefix=""):
    arrays = {}
    if isinstance(value, np.ndarray):
        arrays[prefix] = value
    elif isinstance(value, dict):
        for key, child in value.items():
            arrays.update(flatten_arrays(child, f"{prefix}/{key}".lstrip("/")))
    elif isinstance(value, (tuple, list)):
        for i, child in enumerate(value):
            arrays.update(flatten_arrays(child, f"{prefix}/{i}"))
    return arrays


def run(case="clean", output_dir=OUTPUT):
    output_dir = Path(output_dir)
    paths = {name: output_dir / f"{case}-{suffix}" for name, suffix in (
        ("capture", "capture.pkl.gz"), ("arrays", "arrays.npz"),
        ("manifest", "manifest.json"), ("results", "results.json"))}
    if any(p.exists() for p in paths.values()) or (output_dir / f"{case}-capture.pkl").exists():
        raise FileExistsError("Existing A011 artifact; refuse before loading or fitting")
    torch.set_num_threads(2)
    frame, schema, metadata = prepare_case(case)
    partitions = partition_rows(frame, schema)
    rows = np.r_[partitions["CAL"], partitions["CTRL"]]
    manifest = {"protocol": PROTOCOL, "case": case, **provenance(frame, schema, partitions), **metadata,
                "partition_rows": {n: p.tolist() for n, p in partitions.items()},
                "fit_counts": {"honest": len(partitions["FIT"]), "included": len(partitions["FIT"])+GROUP_SIZE},
                "derivative_convention": "log score; right derivative at lambda0/clipping kink",
                "official_floor": EV_FLOOR, "scored_partition": "CAL and CTRL only"}
    honest_frame, included_frame = paired_frames(frame, schema, partitions)
    frozen = {"case": case, "partitions": partitions, "schema": schema}
    manifest["seconds"] = {}
    for arm, fit_frame in (("honest", honest_frame), ("included", included_frame)):
        print(f"{case}: fitting {arm}", flush=True)
        start = time.perf_counter()
        frozen[arm] = capture_fit(fit_frame, schema, rows, honest=arm == "honest")
        manifest["seconds"][arm] = time.perf_counter()-start
    frozen["derived"] = derive_honest(frozen["honest"], rows)
    frozen = readonly(frozen)
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = pickle.dumps(frozen, protocol=5)
    compressed = gzip.compress(payload, mtime=0)
    with paths["capture"].open("xb") as file:
        file.write(compressed)
    # Complete row-wise evidence is retained in the compressed pickle. NPZ holds
    # dense diagnostic views, avoiding hundreds of thousands of tiny members.
    dense = {"partitions": partitions, "honest_full": frozen["honest"]["full_head"],
             "included_full": frozen["included"]["full_head"], "derived": frozen["derived"]}
    with paths["arrays"].open("xb") as file:
        np.savez_compressed(file, **flatten_arrays(dense))
    manifest.update(capture_sha256=digest(compressed), raw_capture_sha256=digest(payload),
                    capture_format="deterministic gzip-compressed protocol-5 pickle; complete capture",
                    arrays_contents="dense CAL/CTRL heads, honest derived views, and partitions",
                    arrays_sha256=digest(paths["arrays"].read_bytes()))
    with paths["manifest"].open("x", encoding="utf-8") as file:
        file.write(json.dumps(manifest, indent=2)+"\n")
    # Only CAL/CTRL labels are mapped, and only after all captures are persisted.
    _, _, options = _layout(frame, schema)
    labels = {n: frame.iloc[rows][n].map({v: i for i, v in enumerate(options[n])}).to_numpy(dtype=int)
              for n in frozen["honest"]["full_head"]}
    results = score_capture(frozen, labels, schema)
    results["capture_sha256"] = manifest["capture_sha256"]
    with paths["results"].open("x", encoding="utf-8") as file:
        file.write(json.dumps(results, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"case": case, "results": str(paths["results"]),
                      "membership": results.get("membership", {}).get("all")}), flush=True)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=("clean", "household", "adult"), default="clean")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    args = parser.parse_args()
    run(args.case, args.output_dir)


if __name__ == "__main__":
    main()
