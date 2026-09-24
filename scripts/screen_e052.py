"""Freeze and score the two registered E052 endpoints; never fit a selector."""

import argparse
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
from scripts.check_daily_retrieval import (
    BASELINE_HASHES, CACHE, digest, difference, floored, get_case, grade,
)
from src.eval.evidence_routing import routing_library
from src.eval.logloss import floor_mix
from src.eval.recursive_candidates import component_oracle

OUTPUT = ROOT / "docs/analysis/E052-outputs"
SNAPSHOT = ROOT / "submissions/2026-09-19-E041/main.py"


def grouped_effects(groups, delta, changed):
    """Descriptive effects only; no group choices or learned guard."""
    result = {}
    for group in dict.fromkeys(groups):
        selected = np.asarray([g == group for g in groups])
        values = delta[:, selected]
        result[str(group)] = {"cells": int(values.size),
                              "changed_vectors": int(changed[:, selected].sum()),
                              "mean_delta_log": float(values.mean()),
                              "helpful_cells": int((values > 0).sum()),
                              "harmful_cells": int((values < 0).sum())}
    return result


def run(case, output_dir=OUTPUT):
    torch.set_num_threads(2)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for suffix in ("endpoints.pkl", "arrays.npz", "manifest.json", "screen.json"):
        artifact = output_dir / f"{case}-{suffix}"
        if artifact.exists():
            raise FileExistsError(f"Preserve frozen E052 artifact: {artifact}")
    config, schema, frame, cells, truth, frame_hash = get_case("unhcr", case)
    baseline_path = CACHE / f"{case}-unhcr-E041.pkl"
    baseline = pickle.loads(baseline_path.read_bytes())
    assert baseline["frame_sha256"] == frame_hash, "Frozen E041 frame mismatch"
    assert baseline["source_sha256"] == BASELINE_HASHES["E041"], "Frozen E041 cache code mismatch"
    assert digest(SNAPSHOT) == BASELINE_HASHES["E041"], "Frozen E041 snapshot changed"
    start = time.perf_counter()
    library = routing_library(frame, schema)
    seconds = time.perf_counter() - start
    parity = difference(library["base_raw"], baseline["vectors"])
    assert parity == 0, f"E041 endpoint is not raw-exact: {parity}"

    # Freeze every endpoint and its provenance BEFORE any truth-dependent score.
    payload = output_dir / f"{case}-endpoints.pkl"
    payload.write_bytes(pickle.dumps(library, protocol=5))
    arrays_path = output_dir / f"{case}-arrays.npz"
    np.savez_compressed(arrays_path, **{
        f"{arm}__{item}": values for arm, heads in library["arms"].items()
        for item, values in heads.items()})
    sources = sorted((ROOT / "src").rglob("*.py")) + [
        Path(__file__), ROOT / "scripts/check_daily_retrieval.py",
        ROOT / "tests/test_hh_sharp.py"]
    manifest = {"case": case, "seed": 13, "frame_sha256": frame_hash,
                "baseline_snapshot_sha256": digest(SNAPSHOT),
                "baseline_cache_sha256": digest(baseline_path),
                "source_sha256": {p.relative_to(ROOT).as_posix(): digest(p) for p in sources},
                "library_sha256": digest(payload), "arrays_sha256": digest(arrays_path),
                "endpoint_seconds": seconds}
    (output_dir / f"{case}-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    predicted, options, query = library["predicted"], library["options"], library["query"]
    assert [(int(r), n) for r in query for n in predicted] == [(r, n) for r, _, n in cells]
    truth_matrix = np.asarray(truth, dtype=object).reshape(len(query), len(predicted))
    labels = {n: np.asarray([options[n].index(v) for v in truth_matrix[:, i]], dtype=int)
              for i, n in enumerate(predicted)}
    oracle = component_oracle(library["arms"], labels, library["components"])
    scores = {}
    for arm, raw in library["arms_raw"].items():
        measured = grade(schema, config, floored(raw, schema, cells, .001), truth, cells)
        scores[arm] = {k: v for k, v in measured.items() if k != "by_item"}
    log_scores = {arm: np.column_stack([
        np.log(floor_mix(heads[n], .001)[np.arange(len(query)), labels[n]])
        for n in predicted]) for arm, heads in library["arms"].items()}
    delta = log_scores["after_gates"] - log_scores["identity"]
    changed = np.column_stack([np.any(library["arms"]["identity"][n]
                                      != library["arms"]["after_gates"][n], axis=1)
                               for n in predicted])
    depths = {}
    for name, record in schema["items"].items():
        gate = record.get("gate")
        depths[name] = depths[gate["parent"]] + 1 if gate else 0
    result = {"experiment": "E052", "case": case, "seed": 13,
              "frame_sha256": frame_hash, "library_sha256": manifest["library_sha256"],
              "baseline_probability_max_abs": parity, "endpoint_seconds": seconds,
              "scores": scores, "delta_skill": scores["after_gates"]["skill"] - scores["identity"]["skill"],
              "changed_vectors": int(changed.sum()), "changed_fraction": float(changed.mean()),
              "probability_max_abs": difference(library["base_raw"], library["arms_raw"]["after_gates"]),
              "by_item": grouped_effects(predicted, delta, changed),
              "by_depth": grouped_effects([depths[n] for n in predicted], delta, changed),
              "by_section": grouped_effects([n.split("_")[0] for n in predicted], delta, changed),
              "oracle": oracle, "selector_built": False,
              "diagnostics": library["diagnostics"]}
    (output_dir / f"{case}-screen.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("case", "delta_skill", "changed_vectors", "changed_fraction", "endpoint_seconds")}), flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("clean", "household"), required=True)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    args = parser.parse_args()
    run(args.case, args.output_dir)
