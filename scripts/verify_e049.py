"""Validate the exact E049 archive including offline weights and dependencies."""

import argparse
import json
import os
from pathlib import Path
import pickle
import re
import subprocess
import sys
import time
import zipfile

from check_daily_retrieval import (ROOT, KIT, CACHE, OUTPUT, BASELINE_HASHES,
                                   digest, source_digest, get_case, difference)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", required=True)
    parser.add_argument("--date", default="2026-09-23")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    args = parser.parse_args()
    args.output_dir = args.output_dir.resolve()
    label = args.experiment
    snapshot = ROOT / f"submissions/{args.date}-{label}"
    archive = snapshot.with_suffix(".zip")
    temporary = ROOT / f"tmp/{label.lower()}-official"
    extracted = temporary / "submission"
    extracted.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        members = {"main.py", "requirements.txt", "NOTICE.txt",
                   "LICENSE-TabPFN.txt", "tabpfn-v2-classifier.ckpt"}
        assert set(bundle.namelist()) == members
        assert len(bundle.namelist()) == len(members)
        for member in bundle.namelist():
            data = bundle.read(member)
            assert data == (snapshot / member).read_bytes()
            (extracted / member).write_bytes(data)
        raw = bundle.read("main.py")
        assert raw == (snapshot / "main.py").read_bytes()
        (extracted / "main.py").write_bytes(raw)
    env = dict(os.environ)
    env.update(OMP_NUM_THREADS="2", MKL_NUM_THREADS="2", OPENBLAS_NUM_THREADS="2",
               PYTHONIOENCODING="utf-8", TEMP=str(temporary), TMP=str(temporary))
    env.pop("PYTHONPATH", None)
    constraints = ROOT / "docs/analysis/E049-outputs/local-validation-constraints.txt"
    env.update(PIP_CONSTRAINT=str(constraints),
               PIP_FIND_LINKS=str(ROOT / "tmp/e049-wheelhouse"),
               TABPFN_DISABLE_TELEMETRY="1")
    checker = subprocess.run([sys.executable, str(KIT / "tools/check_submission_zip.py"), str(archive)],
                             capture_output=True, text=True, encoding="utf-8", env=env, check=True)
    source_record = json.loads((args.output_dir / f"clean-{label}-unicef,world_bank,unhcr.json").read_text(encoding="utf-8"))
    assert set(source_record["instruments"]) == {"unicef", "world_bank", "unhcr"}, (
        "Source harness must finish all three instruments before official verification")
    assert source_digest(ROOT / source_record["source"]) == source_record["source_sha256"]
    manifest = {"package_files_sha256": {name: digest(snapshot / name) for name in sorted(members)},
                "local_constraints_sha256": digest(constraints),
                "archive_path": str(archive.relative_to(ROOT)), "archive_sha256": digest(archive),
                "main_sha256": digest(snapshot / "main.py"),
                "source_sha256": source_record["source_sha256"],
                "zip_checker": checker.stdout.strip(), "phase": 1,
                "local_threads": 2, "hosted_result": None, "instruments": {}}
    start = time.perf_counter()
    for name in ("unicef", "world_bank", "unhcr"):
        frame_hash = get_case(name, "clean")[-1]
        expected = pickle.loads((CACHE / f"clean-{name}-{label}.pkl").read_bytes())
        assert expected["frame_sha256"] == frame_hash
        assert expected["source_sha256"] == source_record["source_sha256"]
        log = args.output_dir / f"official-{label}-{name}.json"
        timing_path = args.output_dir / f"official-{label}-{name}-timing.json"
        done = subprocess.run([sys.executable, str(ROOT / "scripts/time_official_score.py"),
                               str(timing_path), "--submission", str(extracted),
                               "--data", str(KIT / "_sandbox" / name),
                               "--schema", str(KIT / "data" / f"{name}.json"),
                               "--phase", "1", "--keep", "--log", str(log)],
                              cwd=KIT, env=env, capture_output=True, text=True, encoding="utf-8")
        (temporary / f"{name}.log").write_text(done.stdout + done.stderr, encoding="utf-8")
        if done.returncode:
            raise RuntimeError(done.stdout + done.stderr)
        measured = json.loads(log.read_text(encoding="utf-8"))
        assert measured["status"] == "PASS"
        timing = json.loads(timing_path.read_text(encoding="utf-8"))
        assert timing["official_score_sha256"] == digest(KIT / "score.py")
        assert 0 < timing["seconds"]["run_submission"] <= measured["seconds"]
        work = re.search(r"^\[work\] (.+)$", done.stdout, re.MULTILINE)
        predictions = json.loads((Path(work.group(1).strip()) / "predictions.json").read_text(encoding="utf-8"))
        parity = difference(predictions, expected["vectors"])
        assert parity <= 1e-12
        comparison = source_record["instruments"][name]["comparisons"]
        assert set(comparison) == set(BASELINE_HASHES), "Both frozen baselines are mandatory"
        for baseline, expected_hash in BASELINE_HASHES.items():
            reference = pickle.loads((CACHE / f"clean-{name}-{baseline}.pkl").read_bytes())
            assert reference["source_sha256"] == expected_hash
            assert reference["frame_sha256"] == frame_hash
            actual = comparison[baseline]
            assert abs(actual["delta_skill"] - (measured["skill"] - reference["skill"])) < 1e-12
            assert actual["probability_max_abs"] == difference(predictions, reference["vectors"])
        for row in comparison.values():
            assert abs(row["delta_skill"]) <= .002, (name, row)
            if name != "unhcr":
                assert row["probability_max_abs"] == 0
        manifest["instruments"][name] = {
            "status": measured["status"], "skill": measured["skill"],
            "reported_skill": measured["reported_skill"], "seconds": measured["seconds"],
            "offline_execution_seconds": timing["seconds"]["run_submission"],
            "environment_build_seconds": timing["seconds"]["prepare_environment"],
            "source_parity_max_abs": parity, "comparisons": comparison}
        (snapshot / "verification.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(name, json.dumps(manifest["instruments"][name]), flush=True)
    manifest["official_seconds_sum"] = sum(x["seconds"] for x in manifest["instruments"].values())
    manifest["verification_wall_seconds"] = time.perf_counter() - start
    manifest["offline_execution_seconds_sum"] = sum(
        x["offline_execution_seconds"] for x in manifest["instruments"].values())
    assert manifest["offline_execution_seconds_sum"] < 900
    manifest["technical_checks_passed"] = True
    manifest["local_no_regression_passed"] = True
    (snapshot / "verification.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("TOTAL_OFFLINE", manifest["offline_execution_seconds_sum"], flush=True)


if __name__ == "__main__":
    main()
