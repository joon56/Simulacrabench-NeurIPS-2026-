"""Verify natural active-path parity and UNHCR-only routing scope from official output."""

import json
import pickle
import re
import zipfile

import numpy as np

from check_daily_retrieval import (
    ROOT, CACHE, BASELINE_HASHES, digest, source_digest, get_case, difference,
)


def main():
    snapshot = ROOT / "submissions/2026-09-24-E052"
    output = ROOT / "docs/analysis/E052-outputs"
    for case in ("clean", "household"):
        manifest = json.loads((output / f"{case}-manifest.json").read_text(encoding="utf-8"))
        assert digest(output / f"{case}-endpoints.pkl") == manifest["library_sha256"]
        assert digest(output / f"{case}-arrays.npz") == manifest["arrays_sha256"]
        for relative, expected in manifest["source_sha256"].items():
            executed = (output / "screen-executed.py" if relative == "scripts/screen_e052.py"
                        else ROOT / relative)
            assert digest(executed) == expected, f"Diagnostic provenance changed: {relative}"
    verification = json.loads((snapshot / "verification.json").read_text(encoding="utf-8"))
    assert verification["technical_checks_passed"]
    assert verification["local_no_regression_passed"]
    assert verification["main_sha256"] == digest(snapshot / "main.py")
    assert verification["archive_sha256"] == digest(snapshot.with_suffix(".zip"))
    with zipfile.ZipFile(snapshot.with_suffix(".zip")) as bundle:
        assert bundle.namelist() == ["main.py"]
        assert bundle.read("main.py") == (snapshot / "main.py").read_bytes()

    source = pickle.loads((CACHE / "clean-unhcr-E052.pkl").read_bytes())
    parent = pickle.loads((CACHE / "clean-unhcr-E041.pkl").read_bytes())
    _, schema, _, cells, _, frame_hash = get_case("unhcr", "clean")
    assert source["source_sha256"] == source_digest(ROOT / "src/models/evidence_after_gates.py")
    assert source["source_sha256"] == verification["source_sha256"]
    assert parent["source_sha256"] == BASELINE_HASHES["E041"]
    assert source["frame_sha256"] == parent["frame_sha256"] == frame_hash
    log = (ROOT / "tmp/e052-official/unhcr.log").read_text(encoding="utf-8")
    match = re.search(r"^\[work\] (.+)$", log, re.MULTILINE)
    from pathlib import Path
    predictions = json.loads((Path(match.group(1).strip()) / "predictions.json").read_text(encoding="utf-8"))
    assert difference(predictions, source["vectors"]) == 0
    assert len(predictions) == len(cells)
    changed = {}
    for (_, _, item), actual, original in zip(cells, predictions, parent["vectors"]):
        is_changed = not np.array_equal(actual, original)
        changed[item] = changed.get(item, 0) + int(is_changed)
        gate = schema["items"][item].get("gate")
        if not gate or schema["items"][gate["parent"]]["class"] != "PREDICT":
            assert not is_changed, f"Unexpected unchanged-boundary edit: {item}"
    count = sum(changed.values())
    assert count > 0, "Active-path check requires a real intervention"
    screen = json.loads((output / "clean-screen.json").read_text(encoding="utf-8"))
    assert screen["frame_sha256"] == frame_hash
    frozen = pickle.loads((output / "clean-endpoints.pkl").read_bytes())
    assert digest(output / "clean-endpoints.pkl") == screen["library_sha256"]
    assert difference(predictions, frozen["arms_raw"]["after_gates"]) == 0
    assert count == screen["changed_vectors"]
    result = {
        "experiment": "E052", "case": "clean", "natural_activation": True,
        "frame_sha256": frame_hash, "source_sha256": source["source_sha256"],
        "main_sha256": verification["main_sha256"],
        "archive_sha256": verification["archive_sha256"],
        "source_parity_max_abs": 0., "screen_endpoint_parity_max_abs": 0.,
        "changed_vectors": count, "cells": len(cells),
        "changed_fraction": count / len(cells), "changed_by_item": changed,
        "parent_probability_max_abs": difference(predictions, parent["vectors"]),
        "structural_boundaries_exact": True, "active_assembly_parity_passed": True,
        "both_diagnostic_manifests_verified": True,
        "interpretation": "Natural active routing verified on official clean simulation; no hosted efficacy claim.",
    }
    (output / "active-assembly-parity.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "changed_by_item"}, indent=2))


if __name__ == "__main__":
    main()
