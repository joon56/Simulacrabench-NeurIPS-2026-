"""Run the pre-estimator E041 oracle on the existing clean UNHCR sandbox."""

import json
import os
from pathlib import Path
import re
import pickle
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import torch
from src.eval.runner import ensure_sandbox, KIT, load_predict
from src.eval.retrieval_oracle import candidate_indices, mixture_oracle
from src.models.dup_link import _sig_data_all
from src.models.hier_backoff import _layout
from make_sandbox import load_config
from score import load_frames, sample_rows, floored, score as grade


def main():
    torch.set_num_threads(2)
    config = load_config(str(KIT / "config.yml"))
    schema, path = ensure_sandbox("unhcr", config)
    frame, cells, truth = sample_rows(schema, load_frames(str(path), schema), 1)
    started = time.perf_counter()
    model = load_predict(ROOT / "submissions/2026-09-09-E025/main.py")
    cache = ROOT / "tmp/e041-clean-baseline.pkl"
    if cache.exists():
        vectors, base_seconds = pickle.loads(cache.read_bytes())
    else:
        vectors = model(frame, schema)
        base_seconds = time.perf_counter() - started
        cache.write_bytes(pickle.dumps((vectors, base_seconds)))
    vectors = floored(vectors, schema, cells, config["scoring"]["floor"])
    result = grade(schema, config, vectors, truth, cells)
    print("E025", result["skill"], base_seconds, flush=True)
    records, items, options = _layout(frame, schema)
    predicted = [n for n in items if records[n]["class"] == "PREDICT"]
    query = np.flatnonzero(frame[predicted].isna().any(axis=1))
    bank = np.flatnonzero(~frame[predicted].isna().any(axis=1))
    y = np.stack([frame[n].map({v: j for j, v in enumerate(options[n])})
                  .fillna(-1).to_numpy(dtype=int) for n in predicted], axis=1)
    # Official cells/truth order is respondent then schema item order.
    true_codes = np.array([options[item].index(value)
                          for (_, _, item), value in zip(cells, truth)]).reshape(-1, len(predicted))
    base_truth = np.array([p[t] for p, t in zip(vectors, true_codes.ravel())])
    base_truth = base_truth.reshape(len(query), len(predicted))
    codes, weights = _sig_data_all(frame, records, items)
    candidates = candidate_indices(codes, weights, query, bank, k=32)
    agree = (y[candidates] == true_codes[:, None, :]).transpose(0, 2, 1)
    sizes = np.array([len(options[n]) for n in predicted])
    floor = config["scoring"]["floor"]
    donor_truth = floor + (1 - sizes[None, :, None] * floor) * agree
    all_truth = np.concatenate((base_truth[:, :, None], donor_truth), axis=2)
    sections = {}
    for i, name in enumerate(predicted):
        match = re.match(r"s(\d+[a-z]?)_", name)
        sections.setdefault(match.group(1) if match else "other", []).append(i)
    lower_total = upper_total = 0.0
    rows = {}
    for section, indices in sections.items():
        lower, upper = mixture_oracle(all_truth[:, indices], iterations=300)
        weight = len(indices) / len(predicted)
        lower_total += weight * lower.mean()
        upper_total += weight * upper.mean()
        rows[section] = {"items": len(indices), "oracle_log": float(lower.mean()),
                         "upper_log": float(upper.mean())}
    u = float(result["uniform_reference"])
    delta = (lower_total - result["log_score"]) / u
    output = {"channel": "unchanged official clean sandbox; not real-data ceiling",
              "family": "query-specific section-shared simplex over frozen E025 + 32 donors",
              "baseline_skill": result["skill"], "baseline_seconds": base_seconds,
              "oracle_feasible_skill": 1 + lower_total / u,
              "oracle_upper_skill": 1 + upper_total / u,
              "delta_unhcr": delta, "delta_grand": delta / 3,
              "section_results": rows, "seconds": time.perf_counter() - started}
    out = ROOT / "docs/analysis/A008-outputs/e041-clean-oracle.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2), flush=True)


if __name__ == "__main__":
    main()
