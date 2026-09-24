"""Freeze actual E041/E050/E051 arrays, then score ONLY the oracle partition.

No selector or production model is implemented. Adult uses 2600 visible fit,
800 oracle, 800 selection and 800 untouched audit rows, in that order. All
2400 query PREDICT blocks are hidden before fitting either library. Later
selection/audit work must load the saved arrays without tuning this library.
"""

import argparse
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
from src.eval.recursive_candidates import (e050_library, e051_library, mask_query,
                                           component_oracle)
from src.models.hier_backoff import _layout
from tests.e041_external import encode, load_observed, GIVEN, TARGETS

OUTPUT = ROOT / "docs/analysis/E050-outputs"
ADULT_SOURCE = ROOT / "tmp/e041/adult/adult.data"
PROTOCOL = "E050-E051-2600fit-800oracle-800selection-800audit-v1"


def adapt_adult(observed):
    """Public full-sample vocabulary, original strings, no fabricated gates."""
    _, public = encode(observed)
    schema = {"name": public["name"], "scoring": public["scoring"],
              "gated_value": "NA_GATED", "sections": public["sections"],
              "excluded_raw_fields": public["excluded_raw_fields"], "items": {}}
    for name, record in public["items"].items():
        schema["items"][name] = {"class": record["class"], "values": list(record["options"])}
    return observed.copy(), schema


def digest(data):
    return hashlib.sha256(data).hexdigest()


def provenance(frame, schema, case, seed):
    paths = sorted((ROOT / "src").rglob("*.py")) + [Path(__file__), ROOT / "tests/e041_external.py"]
    hashes = {p.relative_to(ROOT).as_posix(): digest(p.read_bytes()) for p in paths}
    return {"protocol": PROTOCOL, "case": case, "seed": seed,
            "source_hashes": hashes, "source_sha256": digest(json.dumps(hashes, sort_keys=True).encode()),
            "frame_sha256": digest(pickle.dumps((schema, frame), protocol=5)),
            "versions": {name: version(name) for name in ("numpy", "pandas", "torch", "scikit-learn")}}


def prepare_case(case, seed):
    if case == "adult":
        observed, source_ids, counts = load_observed(ADULT_SOURCE, seed, rows=5000)
        frame, schema = adapt_adult(observed)
        query = np.arange(2600, 5000)
        oracle_rows = np.arange(800)
        _, _, options = _layout(frame, schema)
        # Only oracle labels leave preparation; selection/audit stay unscored.
        labels = {n: observed.iloc[2600:3400][n].map(
            {v: i for i, v in enumerate(options[n])}).to_numpy(dtype=int) for n in TARGETS}
        masked = mask_query(frame, schema, query)
        metadata = {"source_file_sha256": digest(ADULT_SOURCE.read_bytes()),
                    "source_ids": source_ids.tolist(), "counts": counts,
                    "partitions": {"fit": [0, 2600], "oracle": [2600, 3400],
                                   "selection": [3400, 4200], "audit": [4200, 5000]},
                    "vocabulary": "full sampled 5000 rows, schema metadata only",
                    "given": GIVEN, "predictors_exclude_source_ids": True}
    else:
        from scripts.check_daily_retrieval import get_case
        _, schema, masked, cells, truth, case_hash = get_case("unhcr", case)
        predicted = [n for n, r in schema["items"].items() if r["class"] == "PREDICT"]
        query = np.flatnonzero(masked[predicted].isna().any(axis=1))
        masked = mask_query(masked, schema, query)
        oracle_rows = np.arange(len(query))
        _, _, options = _layout(masked, schema)
        labels = {n: np.array([options[n].index(y) for cell, y in zip(cells, truth)
                               if cell[2] == n], dtype=int) for n in predicted}
        metadata = {"case_sha256": case_hash, "diagnostic_only": True,
                    "household_seed": 13 if case == "household" else None,
                    "partitions": {"oracle_diagnostic_query_rows": len(query)}}
    return masked, schema, labels, oracle_rows, metadata


def run(case="adult", seed=51, output_dir=OUTPUT):
    torch.set_num_threads(2)
    frame, schema, labels, oracle_rows, metadata = prepare_case(case, seed)
    provenance_record = provenance(frame, schema, case, seed)
    provenance_record.update(metadata)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{case}-seed{seed}"
    cache_path = output_dir / f"{stem}-libraries.pkl"
    manifest_path = output_dir / f"{stem}-manifest.json"
    if cache_path.exists() or manifest_path.exists():
        if not (cache_path.exists() and manifest_path.exists()):
            raise ValueError("Incomplete frozen library; use a fresh output directory")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for key in ("protocol", "source_sha256", "frame_sha256"):
            if manifest[key] != provenance_record[key]:
                raise ValueError(f"Frozen library provenance differs: {key}; use a fresh output directory")
        frozen = cache_path.read_bytes()
        if digest(frozen) != manifest["library_sha256"]:
            raise ValueError("Frozen library hash mismatch")
        libraries = pickle.loads(frozen)
    else:
        start = time.perf_counter()
        e050 = e050_library(frame, schema)
        e050_seconds = time.perf_counter() - start
        start = time.perf_counter()
        e051 = e051_library(frame, schema, e050)
        libraries = {"E050": e050, "E051": e051}
        frozen = pickle.dumps(libraries, protocol=5)
        # Persist and hash all query predictions BEFORE oracle label scoring.
        cache_path.write_bytes(frozen)
        arrays = {f"{family}/{arm}/{item}": p for family, lib in libraries.items()
                  for arm, heads in lib["arms"].items() for item, p in heads.items()}
        arrays_path = output_dir / f"{stem}-arrays.npz"
        np.savez_compressed(arrays_path, **arrays)
        manifest = dict(provenance_record, library_sha256=digest(frozen),
                        arrays_sha256=digest(arrays_path.read_bytes()),
                        seconds={"E050": e050_seconds, "E051": time.perf_counter() - start},
                        diagnostics={family: lib["diagnostics"] for family, lib in libraries.items()})
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    results = {"protocol": PROTOCOL, "case": case, "seed": seed,
               "library_sha256": manifest["library_sha256"],
               "scored_partition": "oracle" if case == "adult" else "diagnostic_query",
               "selection_or_audit_evaluated": False, "families": {}}
    for family, lib in libraries.items():
        restricted = {a: {n: p[oracle_rows] for n, p in heads.items()} for a, heads in lib["arms"].items()}
        results["families"][family] = component_oracle(restricted, labels, lib["components"])
    (output_dir / f"{stem}-oracle.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results), flush=True)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=("adult", "clean", "household"), default="adult")
    parser.add_argument("--seed", type=int, choices=(51, 52), default=51)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    args = parser.parse_args()
    run(args.case, args.seed, args.output_dir)


if __name__ == "__main__":
    main()
