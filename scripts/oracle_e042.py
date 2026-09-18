"""Bound one post-pipeline per-item blend with unchanged E025 evidence."""

import json
import os
from pathlib import Path
import pickle
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
from src.eval.runner import KIT, ensure_sandbox
from src.models.hh_sharp import hh_sharp_layer
from src.models.hier_backoff import _layout
from tests.test_hh_sharp import hh_inject_rho
from make_sandbox import load_config
from score import load_frames, sample_rows


def main():
    config = load_config(str(KIT / "config.yml"))
    schema, path = ensure_sandbox("unhcr", config)
    raw = hh_inject_rho(load_frames(str(path), schema), schema, .3, 13, .2, .8)
    frame, cells, truth = sample_rows(schema, raw, 1)
    baseline, _ = pickle.loads((ROOT / "tmp/e041-household-unhcr-13-baseline.pkl").read_bytes())
    records, items, options = _layout(frame, schema)
    predicted = [n for n in items if records[n]["class"] == "PREDICT"]
    uniform = {n: np.full((len(frame), len(options[n])), 1 / len(options[n])) for n in predicted}
    started = time.perf_counter()
    # Uniform is only a vehicle to expose fixed donor vectors; its lambda is ignored.
    rows, _ = hh_sharp_layer(frame, schema, uniform)
    nt = len(predicted)
    p0, pe, sizes = [], [], []
    for (pos, _, item), value, vector in zip(cells, truth, baseline):
        index, size = options[item].index(value), len(options[item])
        donor = rows.get(pos, ({}, False))[0].get(item, vector)
        p0.append(vector[index])
        pe.append(donor[index])
        sizes.append(size)
    p0, pe, sizes = (np.asarray(a).reshape(-1, nt) for a in (p0, pe, sizes))
    floor = config["scoring"]["floor"]
    logs = []
    grid = [0., .1, .2, .3, .4, .5, .6, .7, .8, .9, .95, .98]
    for share in grid:
        p = floor + (1 - floor * sizes) * ((1 - share) * p0 + share * pe)
        logs.append(np.log(p).mean(axis=0))
    logs = np.stack(logs)
    selected = logs.argmax(axis=0)
    delta_log = float((logs.max(axis=0) - logs[0]).mean())
    u = float(np.log(sizes[0]).mean())
    out = {"family": "one extra fixed share per item; final E025 vs same donor evidence",
           "channel": "existing household sim seed13; not real-data proof",
           "oracle_delta_log": delta_log, "oracle_delta_skill": delta_log / u,
           "oracle_delta_grand_equivalent": delta_log / u / 3,
           "selected_nonzero_items": int(np.count_nonzero(selected)),
           "grid": grid, "seconds": time.perf_counter() - started,
           "gate_log_threshold": .005, "estimator_allowed": delta_log > .005}
    target = ROOT / "docs/analysis/A008-outputs/e042-postblend-oracle.json"
    target.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2), flush=True)


if __name__ == "__main__":
    main()
