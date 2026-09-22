"""Bind the active household source/snapshot comparison to current bytes/inputs."""

import json
import pickle

from check_daily_retrieval import (ROOT, CACHE, BASELINE_HASHES, digest,
                                   source_digest, get_case, difference)


def main():
    source = pickle.loads((CACHE / "household-unhcr-E047.pkl").read_bytes())
    assembled = pickle.loads((CACHE / "household-unhcr-E047-assembled.pkl").read_bytes())
    parent = pickle.loads((CACHE / "household-unhcr-E041.pkl").read_bytes())
    frame_hash = get_case("unhcr", "household")[-1]
    assert all(record["frame_sha256"] == frame_hash for record in (source, assembled, parent))
    assert source["source_sha256"] == source_digest(ROOT / "src/models/adaptive_final_evidence.py")
    assert assembled["source_sha256"] == digest(ROOT / "submissions/2026-09-22-E047/main.py")
    assert parent["source_sha256"] == BASELINE_HASHES["E041"]
    assert source["diagnostics"]["selected"]
    assert source["diagnostics"]["audit"]["accepted"]
    maximum = difference(source["vectors"], assembled["vectors"])
    assert maximum == 0.
    assert source["skill"] == assembled["skill"]
    parent_difference = difference(assembled["vectors"], parent["vectors"])
    assert parent_difference > 0., "Active comparison must differ from the parent"
    result = {
        "experiment": "E047", "case": "household", "seed": 13,
        "frame_sha256": frame_hash, "source_sha256": source["source_sha256"],
        "main_sha256": assembled["source_sha256"],
        "selected_section_indices": source["diagnostics"]["selected"],
        "source_skill": source["skill"], "assembled_skill": assembled["skill"],
        "source_parity_max_abs": maximum, "parent_probability_max_abs": parent_difference,
        "delta_skill_vs_E041": assembled["skill"] - parent["skill"],
        "source_seconds": source["seconds"], "assembled_seconds": assembled["seconds"],
        "active_assembly_parity_passed": True,
        "interpretation": "Actual active-path parity on a fixed assumption-injected "
                          "diagnostic, not evidence of hosted gain. Concurrent local runs; "
                          "official clean all-three timing is recorded separately.",
    }
    output = ROOT / "docs/analysis/E047-outputs/active-assembly-parity.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
