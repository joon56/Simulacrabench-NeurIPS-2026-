"""Post-hoc paired respondent uncertainty for frozen E052 simulations; no fits."""

import json
from pathlib import Path
import pickle

import numpy as np

from check_daily_retrieval import ROOT, digest, get_case, source_digest
from src.eval.logloss import floor_mix

OUTPUT = ROOT / "docs/analysis/A011-outputs"
FROZEN = ROOT / "docs/analysis/E052-outputs"
DRAWS = 1000
SEED = 5302


def run():
    output = OUTPUT / "e052-uncertainty.json"
    if output.exists():
        raise FileExistsError("Refusing to overwrite frozen A011 uncertainty results")
    snapshot = ROOT / "submissions/2026-09-24-E052"
    verification = json.loads((snapshot / "verification.json").read_text(encoding="utf-8"))
    assert digest(snapshot / "main.py") == verification["main_sha256"]
    assert digest(snapshot.with_suffix(".zip")) == verification["archive_sha256"]
    assert source_digest(ROOT / "src/models/evidence_after_gates.py") == verification["source_sha256"]
    results = {}
    for case in ("clean", "household"):
        manifest = json.loads((FROZEN / f"{case}-manifest.json").read_text(encoding="utf-8"))
        screen = json.loads((FROZEN / f"{case}-screen.json").read_text(encoding="utf-8"))
        path = FROZEN / f"{case}-endpoints.pkl"
        assert digest(path) == manifest["library_sha256"] == screen["library_sha256"]
        _, schema, _, cells, truth, frame_hash = get_case("unhcr", case)
        assert frame_hash == manifest["frame_sha256"] == screen["frame_sha256"]
        library = pickle.loads(path.read_bytes())
        predicted, query, options = library["predicted"], library["query"], library["options"]
        assert [(int(row), name) for row in query for name in predicted] == [(r, n) for r, _, n in cells]
        truth_matrix = np.asarray(truth, dtype=object).reshape(len(query), len(predicted))
        rows = np.arange(len(query))
        logs = {}
        for arm in ("identity", "after_gates"):
            logs[arm] = np.column_stack([
                np.log(floor_mix(library["arms"][arm][name])[rows,
                    [options[name].index(v) for v in truth_matrix[:, i]]])
                for i, name in enumerate(predicted)])
        uniform = float(np.mean([np.log(len(options[n])) for n in predicted]))
        row_delta_skill = (logs["after_gates"] - logs["identity"]).mean(axis=1) / uniform
        measured = float(row_delta_skill.mean())
        assert abs(measured - screen["delta_skill"]) < 1e-12
        indices = np.random.default_rng(SEED).integers(len(query), size=(DRAWS, len(query)))
        means = row_delta_skill[indices].mean(axis=1)
        changed = np.column_stack([np.any(library["arms"]["after_gates"][n]
                                         != library["arms"]["identity"][n], axis=1)
                                   for n in predicted])
        results[case] = {
            "frame_sha256": frame_hash, "endpoints_sha256": digest(path),
            "rows": len(query), "cells": len(cells), "delta_skill": measured,
            "respondent_bootstrap_95_interval": np.quantile(means, [.025, .975]).tolist(),
            "bootstrap_fraction_positive": float(np.mean(means > 0)),
            "affected_rows": int(changed.any(axis=1).sum()),
            "affected_row_fraction": float(changed.any(axis=1).mean()),
            "improved_rows": int((row_delta_skill > 0).sum()),
            "worsened_rows": int((row_delta_skill < 0).sum()),
            "changed_vectors": int(changed.sum()),
        }
    report = {
        "analysis": "A011", "post_hoc": True, "model_fits": 0,
        "bootstrap_draws": DRAWS, "bootstrap_seed": SEED,
        "main_sha256": verification["main_sha256"],
        "archive_sha256": verification["archive_sha256"],
        "source_sha256": verification["source_sha256"], "script_sha256": digest(Path(__file__)),
        "cases": results,
        "limits": "Conditional on fixed models and simulations, not hosted transfer or a calibrated success probability. "
                  "Respondent resampling ignores family/donor dependence, training variability and post-hoc selection.",
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run()
