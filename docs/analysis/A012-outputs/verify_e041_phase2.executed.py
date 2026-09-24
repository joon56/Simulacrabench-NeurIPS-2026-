"""Rehearse frozen E025/E041 on the official synthetic phase-2 frames."""

import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import pickle
import re
import shutil
import subprocess
import sys
import time
import zipfile


ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "external/starter-kit"
NAMES = ("unicef", "world_bank", "unhcr")
E025 = ROOT / "submissions/2026-09-09-E025/main.py"
E041 = ROOT / "submissions/2026-09-19-E041/main.py"
ARCHIVE = E041.parent.with_suffix(".zip")
HASHES = {E025: "00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9",
          E041: "22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073"}
OUTPUT = ROOT / "submissions/phase2-E041-preparation"
DETAIL = ROOT / "docs/analysis/A012-outputs"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require_hash(path, expected):
    actual = digest(path)
    assert actual == expected, (path, actual, expected)
    return actual


def write_new(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)


def require_phase2_roles(visible, hidden):
    assert set(visible) == {"TRAIN", "DEV"} and hidden == "TEST"


def require_complete(rows):
    assert set(rows) == set(NAMES), (set(rows), set(NAMES))


def require_exact_parity(first, second):
    assert len(first) == len(second), (len(first), len(second))
    for index, (left, right) in enumerate(zip(first, second)):
        assert left == right, index
    return 0.0


def source_worker(label, name, output):
    for variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        os.environ[variable] = "2"
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(KIT))
    import torch
    from src.eval.runner import load_predict
    from make_sandbox import load_config, load_schema
    from score import load_frames, sample_rows, PHASE_ROLES, floored, score

    torch.set_num_threads(2)
    require_phase2_roles(PHASE_ROLES[2]["visible"], PHASE_ROLES[2]["hidden"])
    config = load_config(str(KIT / "config.yml"))
    schema_path = KIT / "data" / f"{name}.json"
    data_path = KIT / "_sandbox" / name / "respondents.parquet"
    schema = load_schema(str(schema_path), config)
    respondents = load_frames(str(data_path.parent), schema)
    frame, cells, truth = sample_rows(schema, respondents, 2)
    frame_hash = hashlib.sha256(pickle.dumps((schema, frame, cells), protocol=5)).hexdigest()
    if label == "E025":
        predict = load_predict(E025)
        code_path = E025
    else:
        module = importlib.import_module("src.models.supervised_retrieval")
        predict = module.predict
        code_path = Path(module.__file__)
    start = time.perf_counter()
    vectors = predict(frame, schema)
    seconds = time.perf_counter() - start
    assert len(vectors) == len(cells)
    measured = score(schema, config, floored(vectors, schema, cells,
                                              config["scoring"]["floor"]), truth, cells)
    serial = [list(map(float, vector)) for vector in vectors]
    row = {"label": label, "instrument": name, "phase": 2,
           "visible_roles": list(PHASE_ROLES[2]["visible"]),
           "hidden_role": PHASE_ROLES[2]["hidden"], "n_cells": len(cells),
           "skill": measured["skill"], "log_score": measured["log_score"],
           "predict_seconds": seconds,
           "source_path": str(code_path.relative_to(ROOT)), "source_sha256": digest(code_path),
           "schema_sha256": digest(schema_path), "data_sha256": digest(data_path),
           "frame_sha256": frame_hash, "vectors": serial}
    write_new(output, json.dumps(row, separators=(",", ":"), allow_nan=False).encode())
    print(label, name, measured["skill"], len(cells), seconds, flush=True)


def execute(command, path, env, cwd=ROOT):
    start = time.perf_counter()
    done = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")
    write_new(path, (done.stdout + done.stderr).encode("utf-8"))
    if done.returncode:
        raise RuntimeError(f"{command[0]} exit {done.returncode}; see {path}")
    return done.stdout, time.perf_counter() - start


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-worker", nargs=3, metavar=("LABEL", "NAME", "OUTPUT"))
    args = parser.parse_args()
    if args.source_worker:
        source_worker(args.source_worker[0], args.source_worker[1], Path(args.source_worker[2]))
        return
    for path, expected in HASHES.items():
        require_hash(path, expected)
    with zipfile.ZipFile(ARCHIVE) as bundle:
        assert bundle.namelist() == ["main.py"]
        assert bundle.read("main.py") == E041.read_bytes()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    DETAIL.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update(OMP_NUM_THREADS="2", MKL_NUM_THREADS="2", OPENBLAS_NUM_THREADS="2",
               PYTHONIOENCODING="utf-8")
    env.pop("PYTHONPATH", None)
    checker_stdout, _ = execute([sys.executable, str(KIT / "tools/check_submission_zip.py"),
                                 str(ARCHIVE)], DETAIL / "zip-check.log", env)
    assert "OK:" in checker_stdout
    records = {}
    official_seconds = 0.0
    for name in NAMES:
        source_files = {}
        for label in ("E025", "E041"):
            path = DETAIL / f"{label}-{name}-source.json"
            execute([sys.executable, str(__file__), "--source-worker", label, name, str(path)],
                    DETAIL / f"{label}-{name}-source.log", env)
            source_files[label] = json.loads(path.read_text(encoding="utf-8"))
        e025, source = source_files["E025"], source_files["E041"]
        assert e025["frame_sha256"] == source["frame_sha256"]
        assert e025["n_cells"] == source["n_cells"]
        assert e025["schema_sha256"] == source["schema_sha256"]
        assert e025["data_sha256"] == source["data_sha256"]
        log = DETAIL / f"E041-{name}-official.json"
        stdout, wall_seconds = execute(
            [sys.executable, str(KIT / "score.py"), "--submission", str(E041.parent),
             "--data", str(KIT / "_sandbox" / name), "--schema", str(KIT / "data" / f"{name}.json"),
             "--phase", "2", "--keep", "--log", str(log)],
            DETAIL / f"E041-{name}-official.log", env, KIT)
        measured = json.loads(log.read_text(encoding="utf-8"))
        assert measured["status"] == "PASS" and measured["phase"] == 2
        assert measured["n_cells"] == e025["n_cells"]
        work = re.search(r"^\[work\] (.+)$", stdout, re.MULTILINE)
        assert work, "Official work path absent"
        work_path = Path(work.group(1).strip())
        predictions = json.loads((work_path / "predictions.json").read_text(encoding="utf-8"))
        parity = require_exact_parity(predictions, source["vectors"])
        assert measured["skill"] == source["skill"]
        assert measured["log_score"] == source["log_score"]
        write_new(DETAIL / f"E041-{name}-official-predictions.json",
                  (work_path / "predictions.json").read_bytes())
        official_seconds += measured["seconds"]
        records[name] = {
            "cells": e025["n_cells"], "frame_sha256": e025["frame_sha256"],
            "schema_sha256": e025["schema_sha256"], "data_sha256": e025["data_sha256"],
            "e025_skill": e025["skill"], "e041_source_skill": source["skill"],
            "e041_official_skill": measured["skill"],
            "e041_minus_e025": measured["skill"] - e025["skill"],
            "source_official_raw_max_abs": parity,
            "e025_predict_seconds": e025["predict_seconds"],
            "e041_source_predict_seconds": source["predict_seconds"],
            "e041_official_seconds": measured["seconds"],
            "e041_official_wall_seconds": wall_seconds,
            "local_no_regression": measured["skill"] - e025["skill"] >= -0.002,
        }
        print(name, json.dumps(records[name]), flush=True)
    require_complete(records)
    assert official_seconds < 3600
    manifest = {"phase": 2, "scope": "synthetic local engineering only",
                "e025_main_sha256": digest(E025), "e041_main_sha256": digest(E041),
                "e041_zip_sha256": digest(ARCHIVE), "zip_checker": checker_stdout.strip(),
                "starter_kit_score_sha256": digest(KIT / "score.py"),
                "local_threads": 2, "python": sys.version,
                "official_seconds_sum": official_seconds, "official_budget_seconds": 3600,
                "instruments": records,
                "all_local_no_regression": all(r["local_no_regression"] for r in records.values()),
                "hosted_result": None}
    write_new(OUTPUT / "verification.json", (json.dumps(manifest, indent=2) + "\n").encode())
    print("TOTAL", official_seconds, flush=True)


if __name__ == "__main__":
    main()
