"""Measure E041 against the frozen incumbent; no hosted submission actions."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import pickle
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import torch
from src.eval.runner import KIT, ensure_sandbox, load_predict
from src.models import supervised_retrieval
from make_sandbox import load_config
from score import load_frames, sample_rows, floored, score as grade


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=["clean", "household"], default="clean")
    parser.add_argument("--schemas", default="unhcr")
    parser.add_argument("--seed", type=int, default=13)
    parser.add_argument("--assembly", type=Path)
    args = parser.parse_args()
    torch.set_num_threads(2)
    config = load_config(str(KIT / "config.yml"))
    outputs = ROOT / "docs/analysis/A008-outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    incumbent_path = ROOT / "submissions/2026-09-09-E025/main.py"
    incumbent = load_predict(incumbent_path)
    candidate = load_predict(args.assembly) if args.assembly else supervised_retrieval.predict
    result = {"case": args.case, "seed": args.seed, "assembly": str(args.assembly),
              "incumbent_sha256": hashlib.sha256(incumbent_path.read_bytes()).hexdigest(),
              "instruments": {}}
    for name in args.schemas.split(","):
        schema, path = ensure_sandbox(name, config)
        data = load_frames(str(path), schema)
        frame, cells, truth = sample_rows(schema, data, 1)
        if args.case == "household":
            from tests.test_hh_sharp import hh_inject_rho
            data = hh_inject_rho(data, schema, .3, args.seed, .2, .8)
            frame, cells, truth = sample_rows(schema, data, 1)
        cache = ROOT / f"tmp/e041-{args.case}-{name}-{args.seed}-baseline.pkl"
        if args.case == "clean" and name == "unhcr":
            cache = ROOT / "tmp/e041-clean-baseline.pkl"
        if cache.exists():
            old, old_seconds = pickle.loads(cache.read_bytes())
        else:
            started = time.perf_counter()
            old = incumbent(frame, schema)
            old_seconds = time.perf_counter() - started
            cache.write_bytes(pickle.dumps((old, old_seconds)))
        print(name, "incumbent", round(old_seconds, 2), flush=True)
        started = time.perf_counter()
        new = candidate(frame, schema)
        new_seconds = time.perf_counter() - started
        if len(old) != len(new):
            raise ValueError("Candidate changed canonical output length")
        old_score = grade(schema, config, floored(old, schema, cells, .001), truth, cells)
        new_score = grade(schema, config, floored(new, schema, cells, .001), truth, cells)
        max_probability_delta = max(float(np.max(np.abs(np.asarray(a) - b)))
                                    for a, b in zip(old, new))
        row = {"baseline_skill": old_score["skill"], "candidate_skill": new_score["skill"],
               "delta_skill": new_score["skill"] - old_score["skill"],
               "delta_log": new_score["log_score"] - old_score["log_score"],
               "baseline_seconds": old_seconds, "candidate_seconds": new_seconds,
               "max_probability_delta": max_probability_delta,
               "diagnostics": dict(supervised_retrieval.LAST_DIAGNOSTICS)}
        result["instruments"][name] = row
        tag = "assembly" if args.assembly else "source"
        pickle_path = ROOT / f"tmp/e041-{args.case}-{name}-{args.seed}-{tag}.pkl"
        pickle_path.write_bytes(pickle.dumps(new))
        if args.assembly:
            source = ROOT / f"tmp/e041-{args.case}-{name}-{args.seed}-source.pkl"
            expected = pickle.loads(source.read_bytes())
            row["source_parity_max_abs"] = max(float(np.max(np.abs(np.asarray(a) - b)))
                                               for a, b in zip(new, expected))
            if row["source_parity_max_abs"] > 1e-12:
                raise AssertionError("Assembly probabilities differ from source")
        output = outputs / f"e041-{args.case}-{args.seed}-{tag}-{args.schemas}.json"
        output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(row, indent=2), flush=True)


if __name__ == "__main__":
    main()
