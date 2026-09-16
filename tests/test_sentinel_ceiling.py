"""E037 — recorded null: sentinel-mass recalibration (H1) ceiling.

Per-item isotonic recalibration of E025's sentinel mass against the
HELD-OUT truth, cross-fitted 2-fold by row, on the clean unhcr sandbox
and the E028 branch-overlap sim. Measured 2026-09-18 (log score):
clean -0.0150, light overlap -0.0143, heavy overlap -0.0035 — even a
calibrator that sees the truth cannot beat the model's own sentinel
mass out of sample at this data size (in-sample it showed +0.012 to
+0.024: pure optimism). The gain assertion is a strict xfail."""

import numpy as np
import pytest
from sklearn.isotonic import IsotonicRegression

from src.models import hh_cap
from tests.test_soft_gating import KIT, load
from tests.test_pvc_gate import overlap_inject

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def recalibrate_sentinel(vectors, cells, truth, schema, cross_fit=True):
    """Rescale each gated vector's sentinel mass by a per-item isotonic
    map fitted on the held-out truth (2-fold by row when cross_fit)."""
    records = schema["items"]
    gv = schema["gated_value"]
    by_item = {}
    for i, (_, _, item) in enumerate(cells):
        if records[item].get("gate"):
            by_item.setdefault(item, []).append(i)
    out = [np.asarray(v, dtype=float) / np.sum(v) for v in vectors]
    for item, idx in by_item.items():
        p = np.array([out[i][-1] for i in idx])
        y = np.array([truth[i] == gv for i in idx], dtype=float)
        if len(idx) < 50 or y.min() == y.max():
            continue
        f = np.empty(len(idx))
        if cross_fit:
            rows = np.array([cells[i][0] for i in idx])
            fold = rows % 2 == 0
            folds = (fold, ~fold)
        else:
            folds = (np.ones(len(idx), dtype=bool),)
        for m in folds:
            tr = ~m if cross_fit else m
            if y[tr].min() == y[tr].max() or tr.sum() < 25:
                f[m] = p[m]
                continue
            iso = IsotonicRegression(y_min=1e-4, y_max=1 - 1e-4,
                                     out_of_bounds="clip")
            f[m] = iso.fit(p[tr], y[tr]).predict(p[m])
        for k, i in enumerate(idx):
            v = out[i].copy()
            s_old, s_new = v[-1], f[k]
            if s_old < 1 - 1e-9:
                v[:-1] *= (1 - s_new) / (1 - s_old)
            else:
                v[:-1] = (1 - s_new) / (len(v) - 1)
            v[-1] = s_new
            out[i] = v
    return out


def _delta(sim, schema):
    config = load_config(str(KIT / "config.yml"))
    floor = config["scoring"]["floor"]
    merged, cells, truth = sample_rows(schema, sim, 1)
    base = hh_cap.predict(merged, schema)
    s0 = grade(schema, config, floored(base, schema, cells, floor),
               truth, cells)["log_score"]
    rec = recalibrate_sentinel(base, cells, truth, schema)
    s1 = grade(schema, config, floored(rec, schema, cells, floor),
               truth, cells)["log_score"]
    return s1 - s0


@pytest.mark.xfail(strict=True, reason="E037 recorded null: cross-fitted "
                   "isotonic sentinel recalibration -0.0035 on the heavy "
                   "overlap sim (-0.0150 clean)")
def test_sentinel_recalibration_helps_on_heavy_overlap():
    frame, schema = load("unhcr")
    sim, _ = overlap_inject(frame, schema, frac=0.7, seed=23)
    d = _delta(sim, schema)
    print(f"\nheavy overlap sim: cross-fitted sentinel recalibration {d:+.4f}")
    assert d > 0.005
