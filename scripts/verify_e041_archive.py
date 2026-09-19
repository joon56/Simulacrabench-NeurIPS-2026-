"""Official phase-1 scoring and raw source parity from an extracted E041 ZIP."""

import hashlib
import json
import os
from pathlib import Path
import pickle
import re
import subprocess
import sys
import time
import zipfile

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "external/starter-kit"


def main():
    archive = ROOT / "submissions/2026-09-19-E041.zip"
    snapshot = ROOT / "submissions/2026-09-19-E041"
    temp_root = ROOT / "tmp/e041-grader"
    extracted = temp_root / "submission"
    extracted.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        if bundle.namelist() != ["main.py"]:
            raise ValueError("Expected a root-only main.py archive")
        source = bundle.read("main.py")
        if source != (snapshot / "main.py").read_bytes():
            raise ValueError("Archive differs from snapshot")
        (extracted / "main.py").write_bytes(source)
    env = dict(os.environ)
    env.update(OMP_NUM_THREADS="2", MKL_NUM_THREADS="2", OPENBLAS_NUM_THREADS="2",
               PYTHONIOENCODING="utf-8", TEMP=str(temp_root), TMP=str(temp_root))
    env.pop("PYTHONPATH", None)
    checker = subprocess.run([sys.executable, str(KIT / "tools/check_submission_zip.py"),
                              str(archive)], capture_output=True, text=True,
                             encoding="utf-8", env=env)
    if checker.returncode:
        raise RuntimeError(checker.stdout + checker.stderr)
    manifest = {"archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
                "main_sha256": hashlib.sha256(source).hexdigest(),
                "model_sha256": hashlib.sha256((ROOT / "src/models/supervised_retrieval.py").read_bytes()).hexdigest(),
                "zip_checker": checker.stdout.strip(), "phase": 1,
                "local_threads": 2, "local_cuda": False,
                "performance_qualified": False, "hosted_result": None,
                "instruments": {}}
    output_path = snapshot / "verification.json"
    started = time.perf_counter()
    for name in ("unicef", "world_bank", "unhcr"):
        log = ROOT / f"docs/analysis/A008-outputs/e041-official-{name}.json"
        cmd = [sys.executable, str(KIT / "score.py"), "--submission", str(extracted),
               "--data", str(KIT / "_sandbox" / name), "--schema", str(KIT / "data" / f"{name}.json"),
               "--phase", "1", "--keep", "--log", str(log)]
        done = subprocess.run(cmd, cwd=KIT, env=env, capture_output=True,
                              text=True, encoding="utf-8")
        (temp_root / f"{name}.log").write_text(done.stdout + done.stderr, encoding="utf-8")
        if done.returncode:
            raise RuntimeError(done.stdout + done.stderr)
        measured = json.loads(log.read_text(encoding="utf-8"))
        if measured["status"] != "PASS":
            raise AssertionError(f"{name} did not PASS")
        workdir = Path(re.search(r"^\[work\] (.+)$", done.stdout, re.MULTILINE).group(1).strip())
        emitted = json.loads((workdir / "predictions.json").read_text(encoding="utf-8"))
        expected = pickle.loads((ROOT / f"tmp/e041-clean-{name}-13-source.pkl").read_bytes())
        if len(emitted) != len(expected):
            raise AssertionError("Canonical output count differs from source")
        maximum = max(float(np.max(np.abs(np.asarray(a) - b)))
                      for a, b in zip(emitted, expected))
        if maximum > 1e-12:
            raise AssertionError(f"{name} source parity delta {maximum}")
        cache = ROOT / f"tmp/e041-clean-{name}-13-baseline.pkl"
        if name == "unhcr":
            cache = ROOT / "tmp/e041-clean-baseline.pkl"
        baseline, _ = pickle.loads(cache.read_bytes())
        old_probability_delta = max(float(np.max(np.abs(np.asarray(a) - b)))
                                    for a, b in zip(emitted, baseline))
        manifest["instruments"][name] = {
            "status": measured["status"], "exact_skill": measured["skill"],
            "reported_noised_skill": measured["reported_skill"],
            "log_score": measured["log_score"], "seconds": measured["seconds"],
            "source_parity_max_abs": maximum,
            "incumbent_probability_max_abs": old_probability_delta,
            "cells": len(emitted)}
        output_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(name, json.dumps(manifest["instruments"][name]), flush=True)
    manifest["official_seconds_sum"] = sum(row["seconds"] for row in manifest["instruments"].values())
    manifest["verification_wall_seconds"] = time.perf_counter() - started
    manifest["technical_checks_passed"] = manifest["official_seconds_sum"] < 900
    if not manifest["technical_checks_passed"]:
        raise AssertionError("Combined local runtime exceeds the phase-1 budget")
    output_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("TOTAL", manifest["official_seconds_sum"], flush=True)


if __name__ == "__main__":
    main()
