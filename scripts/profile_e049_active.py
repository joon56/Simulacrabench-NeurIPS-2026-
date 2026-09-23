"""Measure real-size E049 inference when all four confidence policies activate.

The honest policy fitter still runs and its result is recorded. Its returned
policies are then replaced solely to exercise the costly final PFN path.
This is a runtime/format contract test, not a measured policy-gain experiment.
"""

import os
import time

STARTED = time.perf_counter()
for variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[variable] = "2"
os.environ["TABPFN_DISABLE_TELEMETRY"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import pickle
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
EXPECTED_MAIN = "a15e497d90e9cd26ae16ce55901ead704d5457163047c4d090574f9641a56cb8"
EXPECTED_CHECKPOINT = "f65a35685aeef42e31b796d9bfa34e68d6fc780bc98e7bff7763802964cf435f"

import numpy as np
import torch

from check_daily_retrieval import get_case
from score import check, floored, score as grade


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    torch.set_num_threads(2)
    assert not torch.cuda.is_available(), "This profile must use the CPU path"
    folder = ROOT / "submissions/2026-09-23-E049"
    archive = folder.with_suffix(".zip")
    model_path = folder / "main.py"
    checkpoint = folder / "tabpfn-v2-classifier.ckpt"
    assert digest(model_path) == EXPECTED_MAIN
    assert digest(checkpoint) == EXPECTED_CHECKPOINT
    archive_hash = digest(archive)
    with zipfile.ZipFile(archive) as bundle:
        assert hashlib.sha256(bundle.read("main.py")).hexdigest() == EXPECTED_MAIN
        assert hashlib.sha256(bundle.read(checkpoint.name)).hexdigest() == EXPECTED_CHECKPOINT
    config, schema, frame, cells, truth, frame_hash = get_case("unhcr", "clean")
    initial_frame_bytes = pickle.dumps((schema, config, frame, cells, truth), protocol=5)
    assert hashlib.sha256(initial_frame_bytes).hexdigest() == frame_hash
    predicted = [name for name, record in schema["items"].items() if record["class"] == "PREDICT"]
    held = frame[predicted].isna().any(axis=1).to_numpy()
    assert frame.loc[held, predicted].isna().all().all()
    assert len(cells) == int(held.sum()) * len(predicted)
    imported_at = time.perf_counter()
    spec = importlib.util.spec_from_file_location("e049_profile_active", model_path)
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    import_seconds = time.perf_counter() - imported_at
    print(json.dumps({"event": "main_imported", "import_seconds": import_seconds,
                      "rows": len(frame), "held_rows": int(held.sum()),
                      "predicted_items": len(predicted)}), flush=True)
    roots, groups = model.e049_groups(frame, schema)
    assert len(roots) == len(groups) == 4
    original_fit = model.e047_fit_policies
    honest = {}
    pfn_fits = []

    def forced_after_honest_fit(*args, **kwargs):
        started = time.perf_counter()
        policies, diagnostics = original_fit(*args, **kwargs)
        honest.update({"policies": copy.deepcopy(policies),
                       "diagnostics": copy.deepcopy(diagnostics),
                       "fit_seconds": time.perf_counter() - started})
        fixed = {section: {"center": [0.] * 7, "scale": [1.] * 7, "beta": [0.] * 7}
                 for section in range(len(groups))}
        print(json.dumps({"event": "honest_selection_completed",
                          "honest_accepted_sections": list(policies),
                          "forced_sections": list(fixed),
                          "elapsed_seconds": time.perf_counter() - STARTED}), flush=True)
        diagnostic = copy.deepcopy(diagnostics)
        diagnostic["forced_selection"] = True
        diagnostic["forced_sections"] = list(fixed)
        return fixed, diagnostic

    def profile(call_frame, event, arg):
        if (event == "call" and call_frame.f_code.co_name == "fit"
                and call_frame.f_globals.get("__name__") == "tabpfn.classifier"):
            labels = np.asarray(call_frame.f_locals["y"])
            pfn_fits.append({"reference_rows": len(labels), "classes": len(np.unique(labels))})

    model.e047_fit_policies = forced_after_honest_fit
    previous_profile = sys.getprofile()
    sys.setprofile(profile)
    try:
        prediction_started = time.perf_counter()
        vectors = model.predict(frame, schema)
        predict_seconds = time.perf_counter() - prediction_started
        import_predict_seconds = time.perf_counter() - imported_at
        elapsed_through_predict = time.perf_counter() - STARTED
    finally:
        model.e047_fit_policies = original_fit
        sys.setprofile(previous_profile)
    assert honest and len(pfn_fits) == 8
    assert all(fit["reference_rows"] == 512 and fit["classes"] >= 2 for fit in pfn_fits)
    assert model.E049_LAST_DIAGNOSTICS.get("reason") is None
    assert len(model.E049_LAST_DIAGNOSTICS["policies"]) == 4
    check(schema, vectors, cells)
    probabilities = floored(vectors, schema, cells, config["scoring"]["floor"])
    check(schema, probabilities, cells)
    assert all(np.all(np.asarray(vector) > 0) for vector in probabilities)
    grading = grade(schema, config, probabilities, truth, cells)
    assert np.isfinite(grading["skill"]) and np.isfinite(grading["log_score"])
    assert hashlib.sha256(pickle.dumps((schema, config, frame, cells, truth), protocol=5)).hexdigest() == frame_hash
    assert digest(model_path) == EXPECTED_MAIN
    assert digest(checkpoint) == EXPECTED_CHECKPOINT
    assert digest(archive) == archive_hash
    output = ROOT / "docs/analysis/E049-outputs/active-runtime.json"
    result = {
        "experiment": "E049", "case": "clean UNHCR, forced all-four active policies",
        "forced_selection": True, "honest_policy_fit_executed": True,
        "real_pretrained_inference": True, "forced_alpha": .25,
        "forced_section_indices": list(range(4)), "root_names": roots,
        "rows": len(frame), "visible_rows": int((~held).sum()), "held_rows": int(held.sum()),
        "predicted_items": len(predicted), "vectors": len(vectors),
        "probability_values": sum(len(vector) for vector in vectors),
        "main_sha256": EXPECTED_MAIN, "checkpoint_sha256": EXPECTED_CHECKPOINT,
        "archive_sha256": archive_hash, "frame_sha256": frame_hash,
        "script_sha256": digest(__file__), "official_score_sha256": digest(ROOT / "external/starter-kit/score.py"),
        "cpu_threads": torch.get_num_threads(), "device": "cpu",
        "main_import_seconds": import_seconds, "predict_seconds": predict_seconds,
        "main_import_plus_predict_seconds": import_predict_seconds,
        "total_seconds_through_predict_including_setup_imports": elapsed_through_predict,
        "total_seconds_including_validation": time.perf_counter() - STARTED,
        "real_pfn_fit_count": len(pfn_fits), "real_pfn_fits": pfn_fits,
        "honest_policy_result": honest,
        "official_raw_check_passed": True, "official_floor_check_passed": True,
        "official_grade_finite": True, "all_floored_values_positive": True,
        "unhcr_active_under_900_seconds": elapsed_through_predict < 900.,
        "all_three_budget_status": "Combine this full-path UNHCR time with separately measured official control times.",
        "interpretation": "Forced-path runtime/format contract only; no measured activation or efficacy claim. "
                          "Concurrent local CPU workloads and profiler overhead make this a conservative "
                          "observation for this run, not a hosted runtime guarantee. Main import plus predict "
                          "includes the original honest confidence-policy fitting cost and all final PFN fits.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"event": "active_runtime_complete", "output": str(output.relative_to(ROOT)),
                      "main_import_plus_predict_seconds": import_predict_seconds,
                      "total_seconds_through_predict": elapsed_through_predict,
                      "real_pfn_fits": len(pfn_fits), "official_checks_passed": True}), flush=True)


if __name__ == "__main__":
    main()
