"""Score a frozen snapshot or new source, caching only matching frame/code hashes."""

import argparse
import hashlib
import importlib
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
from src.eval.runner import KIT, ensure_sandbox, load_predict
from make_sandbox import load_config
from score import load_frames, sample_rows, floored, score as grade

CACHE = ROOT / "tmp/e043-eval"
OUTPUT = ROOT / "docs/analysis/E043-outputs"
BASELINE_HASHES = {
    "E041": "22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073",
    "E025": "00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9",
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_digest(path):
    """Bind source predictions to the complete local model dependency tree."""
    h = hashlib.sha256(Path(path).read_bytes())
    if ROOT / "src" in Path(path).parents:
        for dependency in sorted((ROOT / "src").rglob("*.py")):
            h.update(dependency.relative_to(ROOT).as_posix().encode())
            h.update(dependency.read_bytes())
    return h.hexdigest()


def get_case(name, case):
    config = load_config(str(KIT / "config.yml"))
    schema, data_path = ensure_sandbox(name, config)
    data = load_frames(str(data_path), schema)
    if case == "household":
        from tests.test_hh_sharp import hh_inject_rho
        data = hh_inject_rho(data, schema, .3, 13, .2, .8)
    frame, cells, truth = sample_rows(schema, data, 1)
    raw = pickle.dumps((schema, config, frame, cells, truth), protocol=5)
    return config, schema, frame, cells, truth, hashlib.sha256(raw).hexdigest()


def difference(first, second):
    if len(first) != len(second):
        raise AssertionError("Canonical output count differs")
    return max(float(np.max(np.abs(np.asarray(a) - b))) for a, b in zip(first, second))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    model = parser.add_mutually_exclusive_group(required=True)
    model.add_argument("--snapshot", type=Path)
    model.add_argument("--module")
    parser.add_argument("--case", choices=("clean", "household"), default="clean")
    parser.add_argument("--schemas", default="unicef,world_bank,unhcr")
    parser.add_argument("--compare", default="")
    args = parser.parse_args()
    torch.set_num_threads(2)
    CACHE.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    module = importlib.import_module(args.module) if args.module else None
    path = Path(module.__file__) if module else args.snapshot.resolve()
    predict = module.predict if module else load_predict(path)
    code_hash = source_digest(path)
    if args.label in BASELINE_HASHES:
        assert code_hash == BASELINE_HASHES[args.label], "Frozen baseline changed"
    result = {"label": args.label, "case": args.case, "seed": 13,
              "source": str(path.relative_to(ROOT)), "source_sha256": code_hash,
              "instruments": {}}
    for name in args.schemas.split(","):
        config, schema, frame, cells, truth, frame_hash = get_case(name, args.case)
        cache_path = CACHE / f"{args.case}-{name}-{args.label}.pkl"
        cached = pickle.loads(cache_path.read_bytes()) if cache_path.exists() else None
        if cached is None or (cached["source_sha256"], cached["frame_sha256"]) != (code_hash, frame_hash):
            start = time.perf_counter()
            vectors = predict(frame, schema)
            seconds = time.perf_counter() - start
            measured = grade(schema, config, floored(vectors, schema, cells, .001), truth, cells)
            cached = {"source_sha256": code_hash, "frame_sha256": frame_hash,
                      "vectors": vectors, "seconds": seconds,
                      "skill": measured["skill"], "log_score": measured["log_score"]}
            cache_path.write_bytes(pickle.dumps(cached, protocol=5))
        row = {k: v for k, v in cached.items() if k != "vectors"}
        row["cells"] = len(cells)
        row["comparisons"] = {}
        for label in filter(None, args.compare.split(",")):
            other = pickle.loads((CACHE / f"{args.case}-{name}-{label}.pkl").read_bytes())
            if other["frame_sha256"] != frame_hash:
                raise AssertionError("Comparison frame changed")
            assert other["source_sha256"] == BASELINE_HASHES[label], "Wrong baseline code"
            row["comparisons"][label] = {
                "baseline_skill": other["skill"], "delta_skill": cached["skill"] - other["skill"],
                "delta_log": cached["log_score"] - other["log_score"],
                "probability_max_abs": difference(cached["vectors"], other["vectors"])}
        result["instruments"][name] = row
        (OUTPUT / f"{args.case}-{args.label}-{args.schemas}.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(name, json.dumps(row), flush=True)


if __name__ == "__main__":
    main()
