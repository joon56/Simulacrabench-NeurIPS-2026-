"""Official CLI validation of the extracted, final E041 archive on all schemas."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
KIT = ROOT / "external/starter-kit"
archive = ROOT / "submissions/2026-09-25-E041.zip"
record = json.loads((OUT / "archives.json").read_text())["E041"]
assert hashlib.sha256(archive.read_bytes()).hexdigest() == record["sha256"]
extracted = OUT / "E041-extracted"
extracted.mkdir(exist_ok=False)
with zipfile.ZipFile(archive) as bundle:
    assert bundle.namelist() == ["main.py", "LICENSE-starter-kit.txt"]
    for name in bundle.namelist():
        (extracted / name).write_bytes(bundle.read(name))
assert hashlib.sha256((extracted / "main.py").read_bytes()).hexdigest() == record["main_sha256"]
env = os.environ.copy()
env.update(OMP_NUM_THREADS="2", MKL_NUM_THREADS="2", OPENBLAS_NUM_THREADS="2", PYTHONIOENCODING="utf-8")
env.pop("PYTHONPATH", None)
results = {}
total_start = time.perf_counter()
for name in ("unicef", "world_bank", "unhcr"):
    log_path = OUT / f"E041-{name}-official.json"
    assert not log_path.exists()
    command = [sys.executable, str(KIT / "score.py"), "--submission", str(extracted),
               "--data", str(KIT / "_sandbox" / name), "--schema", str(KIT / "data" / f"{name}.json"),
               "--phase", "2", "--keep", "--log", str(log_path)]
    start = time.perf_counter()
    done = subprocess.run(command, cwd=KIT, env=env, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=3600, check=False)
    wall = time.perf_counter() - start
    with (OUT / f"E041-{name}-official.log").open("x", encoding="utf-8") as stream:
        stream.write(done.stdout + done.stderr)
    assert done.returncode == 0, (name, done.returncode)
    measured = json.loads(log_path.read_text(encoding="utf-8"))
    assert measured["status"] == "PASS" and measured["phase"] == 2
    work = Path(re.search(r"^\[work\] (.+)$", done.stdout, re.MULTILINE).group(1).strip())
    raw_path = work / "predictions.json"
    vectors = json.loads(raw_path.read_text(encoding="utf-8"))
    reference = json.loads((ROOT / f"docs/analysis/A012-outputs/E041-{name}-source.json").read_text(encoding="utf-8"))
    assert vectors == reference["vectors"], name
    assert measured["skill"] == reference["skill"]
    baseline = json.loads((ROOT / f"docs/analysis/A012-outputs/E025-{name}-source.json").read_text(encoding="utf-8"))
    delta = measured["skill"] - baseline["skill"]
    assert abs(delta) <= .002
    results[name] = {"status": "PASS", "skill": measured["skill"], "e025_delta": delta,
        "cells": len(vectors), "raw_max_abs": 0.0, "inclusive_wall_seconds": wall,
        "official_seconds": measured["seconds"], "kept_work": str(work),
        "raw_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest()}
    print(name, results[name], flush=True)
elapsed = time.perf_counter() - total_start
assert elapsed < 3600
with (OUT / "official-summary.json").open("x", encoding="utf-8") as stream:
    json.dump({"archive_sha256": record["sha256"], "instruments": results,
               "inclusive_wall_seconds": elapsed, "cells_exact": 442425,
               "official_seconds_sum": sum(row["official_seconds"] for row in results.values())}, stream, indent=2)
    stream.write("\n")
