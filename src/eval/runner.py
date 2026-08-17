"""Local experiment runner: score any predict() the way the grader does,
but in-process (no venv install) and with the exact, un-noised skill.

Uses the starter kit's own modules — nothing here reimplements scoring.
"""

import importlib.util
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KIT = ROOT / "external" / "starter-kit"
sys.path.insert(0, str(KIT))

from make_sandbox import load_config, load_schema, write_sandbox  # noqa: E402
from score import load_frames, sample_rows, floored, score as grade  # noqa: E402

SCHEMAS = ["sample", "unicef", "world_bank", "unhcr"]


def ensure_sandbox(name, config, seed=0):
    """Build the sandbox for a schema if it does not exist yet."""
    schema = load_schema(str(KIT / "data" / f"{name}.json"), config)
    out = KIT / "_sandbox" / name
    if not (out / "respondents.parquet").exists():
        write_sandbox(schema, config, str(out), seed=seed)
    return schema, out


def run(predict_fn, schemas=SCHEMAS, phase=1, seed=0):
    """Score predict_fn on each schema's sandbox. Returns
    {schema: {skill, log_score, cells, seconds}} with exact (un-noised) skill."""
    config = load_config(str(KIT / "config.yml"))
    results = {}
    for name in schemas:
        schema, data_dir = ensure_sandbox(name, config)
        respondents = load_frames(str(data_dir), schema)
        frame, cells, truth = sample_rows(schema, respondents, config, phase,
                                          seed=seed)
        t0 = time.perf_counter()
        vectors = predict_fn(frame, schema)
        elapsed = time.perf_counter() - t0
        vectors = floored(vectors, schema, cells, config["scoring"]["floor"])
        res = grade(schema, config, vectors, truth, cells)
        results[name] = {
            "skill": res["skill"],
            "log_score": res["log_score"],
            "cells": len(cells),
            "seconds": round(elapsed, 2),
        }
    return results


def load_predict(main_py):
    """Import a submission-style main.py and return its predict()."""
    spec = importlib.util.spec_from_file_location("submission_main", main_py)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.predict


def summarize(results):
    lines = [f"{'schema':<12} {'skill':>8} {'log_score':>10} {'cells':>8} {'sec':>7}"]
    for name, r in results.items():
        lines.append(f"{name:<12} {r['skill']:>8.4f} {r['log_score']:>10.4f} "
                     f"{r['cells']:>8} {r['seconds']:>7.2f}")
    mean_skill = sum(r["skill"] for r in results.values()) / len(results)
    lines.append(f"{'mean':<12} {mean_skill:>8.4f}")
    return "\n".join(lines)


if __name__ == "__main__":
    predict = load_predict(sys.argv[1])
    schemas = sys.argv[2].split(",") if len(sys.argv) > 2 else SCHEMAS
    print(summarize(run(predict, schemas=schemas)))
