"""Exercise real E049 source/archive inference under a forced constant policy.

This is an engineering contract check, not an honest policy-selection result
or an efficacy estimate. Only e047_fit_policies is replaced in each module.
"""

import os

for variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[variable] = "2"
os.environ["TABPFN_DISABLE_TELEMETRY"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
STARTED = time.perf_counter()
EXPECTED_SOURCE = "5ea710593814ea93cc86d7fd4c5f83bdb1bc3d89a7759decffeeb5ec1362bc77"
EXPECTED_MAIN = "a15e497d90e9cd26ae16ce55901ead704d5457163047c4d090574f9641a56cb8"
EXPECTED_CHECKPOINT = "f65a35685aeef42e31b796d9bfa34e68d6fc780bc98e7bff7763802964cf435f"

import numpy as np
import torch

from src.models import adaptive_tabpfn_parents as source
from tests.test_e049_tabpfn_parents import _disjoint_case


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def frame_digest(frame, schema):
    payload = {"schema": schema, "columns": list(frame.columns),
               "index": frame.index.tolist(),
               "values": frame.astype(object).where(frame.notna(), None).values.tolist()}
    return hashlib.sha256(json.dumps(payload, separators=(",", ":"),
                                    ensure_ascii=True).encode()).hexdigest()


def source_tree_digest():
    content = hashlib.sha256()
    for path in sorted((ROOT / "src").rglob("*.py")):
        content.update(path.relative_to(ROOT).as_posix().encode())
        content.update(path.read_bytes())
    return content.hexdigest()


def difference(first, second):
    assert len(first) == len(second)
    assert all(np.asarray(a).shape == np.asarray(b).shape for a, b in zip(first, second))
    return max(float(np.max(np.abs(np.asarray(a) - b))) for a, b in zip(first, second))


def main():
    torch.set_num_threads(2)
    source_path = ROOT / "src/models/adaptive_tabpfn_parents.py"
    folder = ROOT / "submissions/2026-09-23-E049"
    archive_path = folder.with_suffix(".zip")
    assert digest(source_path) == EXPECTED_SOURCE, "Production source changed"
    assert digest(folder / "main.py") == EXPECTED_MAIN, "Snapshot changed; rebind check"
    assert digest(source.E049_CHECKPOINT) == EXPECTED_CHECKPOINT
    initial_tree_hash = source_tree_digest()
    initial_archive_hash = digest(archive_path)
    frame, schema, roots = _disjoint_case(800)
    initial_frame_hash = frame_digest(frame, schema)
    duplicate, duplicate_schema, _ = _disjoint_case(800)
    assert frame_digest(duplicate, duplicate_schema) == initial_frame_hash
    predicted = [name for name, record in schema["items"].items() if record["class"] == "PREDICT"]
    selected_roots, groups = source.e049_groups(frame, schema)
    assert selected_roots == roots
    shadow, visible, fit, select, audit, reference = source.e049_shadow_split(frame, schema)
    assert [len(part) for part in (fit, select, audit, reference)] == [80, 80, 80, 512]
    final_reference = np.random.default_rng(4901).permutation(visible)[:512]
    class_counts = {
        phase: {root: int(data.iloc[rows][root].nunique()) for root in roots}
        for phase, data, rows in (("shadow", shadow, reference), ("final", frame, final_reference))}
    assert all(value >= 2 for counts in class_counts.values() for value in counts.values())
    del duplicate, shadow
    forced_calls, pfn_fits = [], []

    def forced_policy(base, candidate, labels, candidate_groups, correction, selection, audit_rows):
        assert candidate_groups == groups
        assert len(base[roots[0]]) == 240
        assert [len(rows) for rows in (correction, selection, audit_rows)] == [80, 80, 80]
        assert all(np.asarray(base[name]).shape == np.asarray(candidate[name]).shape for name in base)
        forced_calls.append({"fit_rows": len(correction), "selection_rows": len(selection),
                             "audit_rows": len(audit_rows)})
        policy = {"center": [0.] * 7, "scale": [1.] * 7, "beta": [0.] * 7}
        return {0: policy}, {"forced_selection": True, "selected": [0],
                             "audit": {"accepted": True, "forced": True}}

    def record_real_fit(call_frame, event, arg):
        if (event == "call" and call_frame.f_code.co_name == "fit"
                and call_frame.f_globals.get("__name__") == "tabpfn.classifier"):
            labels = np.asarray(call_frame.f_locals["y"])
            pfn_fits.append({"references": len(labels), "classes": len(np.unique(labels))})

    with tempfile.TemporaryDirectory(prefix="e049-active-parity-", dir=ROOT / "tmp") as temporary:
        extracted = Path(temporary)
        with zipfile.ZipFile(archive_path) as bundle:
            for name in ("main.py", "tabpfn-v2-classifier.ckpt"):
                (extracted / name).write_bytes(bundle.read(name))
        assert digest(extracted / "main.py") == EXPECTED_MAIN
        assert digest(extracted / "tabpfn-v2-classifier.ckpt") == EXPECTED_CHECKPOINT
        spec = importlib.util.spec_from_file_location("e049_active_archive", extracted / "main.py")
        assembled = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(assembled)
        assert assembled.E049_CHECKPOINT.parent == extracted
        original_source_policy, original_archive_policy = source.e047_fit_policies, assembled.e047_fit_policies
        source.e047_fit_policies = assembled.e047_fit_policies = forced_policy
        previous_profile = sys.getprofile()
        sys.setprofile(record_real_fit)
        try:
            started = time.perf_counter()
            source_vectors = source.predict(frame, schema)
            source_seconds = time.perf_counter() - started
            source_diagnostics = dict(source.E049_LAST_DIAGNOSTICS)
            print(json.dumps({"event": "source_complete", "seconds": source_seconds,
                              "real_pfn_fits": len(pfn_fits)}), flush=True)
            started = time.perf_counter()
            archive_vectors = assembled.predict(frame, schema)
            archive_seconds = time.perf_counter() - started
            archive_diagnostics = dict(assembled.E049_LAST_DIAGNOSTICS)
            print(json.dumps({"event": "archive_complete", "seconds": archive_seconds,
                              "real_pfn_fits": len(pfn_fits)}), flush=True)
        finally:
            sys.setprofile(previous_profile)
            source.e047_fit_policies = original_source_policy
            assembled.e047_fit_policies = original_archive_policy
    assert len(forced_calls) == 2
    assert len(pfn_fits) == 16, "Both real predictors must fit four roots in shadow and final phases"
    assert all(entry["references"] == 512 and entry["classes"] >= 2 for entry in pfn_fits)
    for diagnostics in (source_diagnostics, archive_diagnostics):
        assert diagnostics["forced_selection"] and diagnostics["selected"] == [0]
        assert diagnostics["roots"] == roots
        assert diagnostics.get("reason") is None, "A singleton or other fallback occurred"
        assert list(diagnostics["policies"]) == [0]
    maximum = difference(source_vectors, archive_vectors)
    assert maximum <= 1e-12, maximum
    started = time.perf_counter()
    baseline = source.parent.predict(frame, schema)
    baseline_seconds = time.perf_counter() - started
    parent_difference = difference(source_vectors, baseline)
    assert parent_difference > 1e-12, "Forced active correction must change actual probabilities"
    assert len(source_vectors) == 2 * len(predicted)
    active_indices = [row * len(predicted) + column for row in range(2)
                      for column, name in enumerate(predicted) if name in groups[0]]
    inactive_indices = [index for index in range(len(source_vectors)) if index not in active_indices]
    assert max(float(np.max(np.abs(source_vectors[index] - baseline[index])))
               for index in inactive_indices) == 0.
    assert frame_digest(frame, schema) == initial_frame_hash, "Input mutated"
    assert source_tree_digest() == initial_tree_hash, "Source dependencies changed during run"
    assert digest(source_path) == EXPECTED_SOURCE
    assert digest(folder / "main.py") == EXPECTED_MAIN
    assert digest(archive_path) == initial_archive_hash
    result = {
        "experiment": "E049", "case": "deterministic engineering fixture",
        "forced_selection": True, "real_pretrained_inference": True,
        "forced_alpha": .25, "forced_section_indices": [0],
        "frame_sha256": initial_frame_hash, "source_sha256": EXPECTED_SOURCE,
        "source_tree_sha256": initial_tree_hash, "main_sha256": EXPECTED_MAIN,
        "archive_sha256": initial_archive_hash, "checkpoint_sha256": EXPECTED_CHECKPOINT,
        "fixture_helper_sha256": digest(ROOT / "tests/test_e049_tabpfn_parents.py"),
        "script_sha256": digest(__file__), "visible_rows": 800, "held_rows": 2,
        "predicted_items": len(predicted), "vectors": len(source_vectors),
        "probability_values": sum(len(vector) for vector in source_vectors),
        "active_vectors": len(active_indices), "unchanged_vectors": len(inactive_indices),
        "root_names": roots, "reference_class_counts": class_counts,
        "real_pfn_fit_count": len(pfn_fits), "reference_rows_per_pfn_fit": 512,
        "source_archive_max_abs": maximum, "source_E041_max_abs": parent_difference,
        "inactive_E041_max_abs": 0., "source_seconds": source_seconds,
        "archive_seconds": archive_seconds, "baseline_seconds": baseline_seconds,
        "total_seconds_including_imports": time.perf_counter() - STARTED,
        "source_diagnostics": source_diagnostics, "archive_diagnostics": archive_diagnostics,
        "active_assembly_parity_passed": True,
        "interpretation": "Engineering contract test with forced policy selection only. "
                          "Actual E041 fits, actual checkpoint inference and actual rendering. "
                          "No measured policy acceptance, gain, efficacy or runtime-budget claim.",
    }
    output = ROOT / "docs/analysis/E049-outputs/active-assembly-parity.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
