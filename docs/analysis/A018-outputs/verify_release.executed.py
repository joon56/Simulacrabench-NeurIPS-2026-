"""A018 frozen artifact checks and single-process phase-2 resource rehearsal.

No model tuning, private data, or proxy-label access. Run from repository root.
"""
import argparse
import ctypes
from ctypes import wintypes
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import pickle
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
KIT = ROOT / "external/starter-kit"
NAMES = ("unicef", "world_bank", "unhcr")
DATES = {"E025": "2026-09-09", "E041": "2026-09-19", "E044": "2026-09-20",
         "E045": "2026-09-21", "E047": "2026-09-22", "E049": "2026-09-23",
         "E052": "2026-09-24"}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


class Memory(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD)] + [
        (name, ctypes.c_size_t) for name in (
            "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
            "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage",
            "PagefileUsage", "PeakPagefileUsage", "PrivateUsage")]


def memory():
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    api = ctypes.WinDLL("psapi", use_last_error=True).GetProcessMemoryInfo
    api.argtypes = (wintypes.HANDLE, ctypes.POINTER(Memory), wintypes.DWORD)
    api.restype = wintypes.BOOL
    counters = Memory()
    counters.cb = ctypes.sizeof(counters)
    if not api(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
        raise ctypes.WinError(ctypes.get_last_error())
    return {"peak_working_set_bytes": counters.PeakWorkingSetSize,
            "peak_pagefile_bytes": counters.PeakPagefileUsage,
            "private_bytes_now": counters.PrivateUsage}


def freeze():
    manifest = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "protocol_sha256": digest(OUT.parent / "A018-test-selection.md"),
                "verifier_sha256": digest(__file__), "candidates": {}, "inputs": {}}
    for label, date in DATES.items():
        main = ROOT / f"submissions/{date}-{label}/main.py"
        archive = main.parent.with_suffix(".zip")
        with zipfile.ZipFile(archive) as bundle:
            assert bundle.read("main.py") == main.read_bytes(), label
            members = bundle.namelist()
        manifest["candidates"][label] = {"main": str(main.relative_to(ROOT)),
            "main_sha256": digest(main), "archive": str(archive.relative_to(ROOT)),
            "archive_sha256": digest(archive), "members": members}
    old = read(ROOT / "submissions/phase2-E041-preparation/supplemental-verification.json")
    # Bind every prior A012 artifact and source file, not just convenient inputs.
    for name, expected in old["artifacts_sha256"].items():
        actual = digest(ROOT / name)
        assert actual == expected, (name, actual, expected)
        manifest["inputs"][name] = actual
    for name in NAMES:
        source = read(ROOT / f"docs/analysis/A012-outputs/E041-{name}-source.json")
        vectors = read(ROOT / f"docs/analysis/A012-outputs/E041-{name}-official-predictions.json")
        assert vectors == source["vectors"], name
        for path, expected in ((KIT / "data" / f"{name}.json", source["schema_sha256"]),
                               (KIT / "_sandbox" / name / "respondents.parquet", source["data_sha256"])):
            assert digest(path) == expected
            manifest["inputs"][str(path.relative_to(ROOT))] = expected
    manifest["a012_raw_exact_cells"] = 442425
    save(OUT / "preflight.json", manifest)
    print("FROZEN: seven candidates; all A012 hashes and 442425 vectors exact", flush=True)


def worker(label):
    started = time.perf_counter()
    for variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        os.environ[variable] = "2"
    sys.path.insert(0, str(KIT))
    import torch
    from make_sandbox import load_config, load_schema
    from score import load_frames, sample_rows, PHASE_ROLES, check, floored, score
    torch.set_num_threads(2)
    assert set(PHASE_ROLES[2]["visible"]) == {"TRAIN", "DEV"}
    assert PHASE_ROLES[2]["hidden"] == "TEST"
    frozen = read(OUT / "preflight.json")
    candidate = frozen["candidates"][label]
    path = ROOT / candidate["main"]
    assert digest(path) == candidate["main_sha256"]
    spec = importlib.util.spec_from_file_location("submission", path)
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    imported_seconds = time.perf_counter() - started
    config = load_config(str(KIT / "config.yml"))
    results = {}
    for name in NAMES:
        schema = load_schema(str(KIT / "data" / f"{name}.json"), config)
        respondents = load_frames(str(KIT / "_sandbox" / name), schema)
        frame, cells, truth = sample_rows(schema, respondents, 2)
        frame_sha = hashlib.sha256(pickle.dumps((schema, frame, cells), protocol=5)).hexdigest()
        reference = read(ROOT / f"docs/analysis/A012-outputs/{label}-{name}-source.json")
        assert frame_sha == reference["frame_sha256"]
        before = time.perf_counter()
        vectors = model.predict(frame, schema)
        seconds = time.perf_counter() - before
        check(schema, vectors, cells)
        assert len(vectors) == len(reference["vectors"])
        # Compare every raw probability, not just a score or selected sample.
        max_abs = max(abs(float(x) - float(y)) for left, right in zip(vectors, reference["vectors"])
                      for x, y in zip(left, right))
        assert all(len(left) == len(right) for left, right in zip(vectors, reference["vectors"]))
        assert max_abs == 0, (name, max_abs)
        measured = score(schema, config, floored(vectors, schema, cells, config["scoring"]["floor"]), truth, cells)
        assert measured["skill"] == reference["skill"]
        results[name] = {"cells": len(cells), "frame_sha256": frame_sha,
            "skill": measured["skill"], "predict_seconds": seconds,
            "a012_source_raw_max_abs": max_abs, "memory": memory(),
            "activation": getattr(model, "LAST_DIAGNOSTICS", {}) if name == "unhcr" else None}
        save(OUT / f"{label}-{name}-shared.json", results[name])
        print(label, name, seconds, results[name]["memory"], flush=True)
        assert max(results[name]["memory"].values()) < 16_000_000_000
    elapsed = time.perf_counter() - started
    assert elapsed < 3600
    save(OUT / f"{label}-shared.json", {"label": label, "python": sys.version,
        "torch": torch.__version__, "cuda": torch.cuda.is_available(), "threads": 2,
        "import_seconds": imported_seconds, "inclusive_seconds": elapsed,
        "memory": memory(), "instruments": results,
        "scope": "Windows CPU single process all3, includes imports/data/scoring/cache comparisons; not hosted guarantee"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["freeze", "E025", "E041"])
    args = parser.parse_args()
    if args.mode == "freeze":
        freeze()
    else:
        # The parent bounds our own worker; no unrelated process is touched.
        if os.environ.get("A018_WORKER") == "1":
            worker(args.mode)
        else:
            env = os.environ.copy()
            env["A018_WORKER"] = "1"
            with (OUT / f"{args.mode}-shared.log").open("x", encoding="utf-8") as log:
                subprocess.run([sys.executable, __file__, args.mode], env=env,
                               stdout=log, stderr=subprocess.STDOUT, timeout=3600, check=True)
