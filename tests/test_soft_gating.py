"""E003 tests: identity on exact-gate data, gain under simulated violations."""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.models import gated_marginal, soft_gated_marginal

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "external" / "starter-kit"
sys.path.insert(0, str(KIT))


def load(name):
    with open(KIT / "data" / f"{name}.json", encoding="utf-8") as f:
        schema = json.load(f)
    schema.setdefault("gated_value", "NA_GATED")
    frame = pd.read_parquet(KIT / "_sandbox" / name / "respondents.parquet")
    return frame, schema


def build_phase1(frame, schema):
    items = [n for n, r in schema["items"].items()
             if r["class"] in ("GIVEN", "PREDICT")]
    predict_cols = [n for n, r in schema["items"].items()
                    if r["class"] == "PREDICT"]
    train = frame[frame["role"] == "TRAIN"]
    dev = frame[frame["role"] == "DEV"].copy()
    truth = dev[predict_cols].copy()
    dev[predict_cols] = np.nan
    merged = pd.concat([train, dev], ignore_index=True)
    return merged[["respondent_id"] + items], truth, items, predict_cols


def test_forced_full_agreement_equals_e002(monkeypatch):
    frame, schema = load("sample")
    merged, _, _, _ = build_phase1(frame, schema)
    monkeypatch.setattr(soft_gated_marginal, "agreement_weights",
                        lambda f, s: ({}, 1.0))
    ours = soft_gated_marginal.predict(merged, schema)
    e002 = gated_marginal.predict(merged, schema)
    for a, b in zip(ours, e002):
        assert np.allclose(a, b, atol=1e-12)


def test_natural_sandbox_weights_near_one():
    frame, schema = load("sample")
    merged, _, _, _ = build_phase1(frame, schema)
    weights, m = soft_gated_marginal.agreement_weights(merged, schema)
    assert weights, "no gated items found"
    assert m == pytest.approx(1.0, abs=1e-9)
    for a in weights.values():
        assert a > 0.99


def inject_violations(frame, schema, rate, seed):
    """Flip `rate` of gated child cells so they violate the gate."""
    rng = np.random.default_rng(seed)
    out = frame.copy()
    gated_value = schema["gated_value"]
    records = schema["items"]
    for item, r in records.items():
        gate = r.get("gate")
        if not gate or r["class"] == "EXCLUDE" or item not in out.columns:
            continue
        cells = out[item].notna()
        flip = cells & (rng.random(len(out)) < rate)
        idx = out.index[flip]
        values = list(r["values"])
        for i in idx:
            if out.at[i, item] == gated_value:
                out.at[i, item] = values[rng.integers(len(values))]
            else:
                out.at[i, item] = gated_value
    return out


def violation_log_score(model, frame, schema, rate=0.17, seed=1):
    from make_sandbox import load_config
    from score import floored, sample_rows, score as grade

    violated = inject_violations(frame, schema, rate, seed)
    config = load_config(str(KIT / "config.yml"))
    merged, cells, truth = sample_rows(schema, violated, 1)
    vectors = model.predict(merged, schema)
    vectors = floored(vectors, schema, cells, config["scoring"]["floor"])
    res = grade(schema, config, vectors, truth, cells)
    return res["log_score"]


def test_soft_beats_hard_under_violations_sample():
    # sample has only 2 gates; direction must hold, magnitude is small
    frame, schema = load("sample")
    hard = violation_log_score(gated_marginal, frame, schema)
    soft = violation_log_score(soft_gated_marginal, frame, schema)
    assert soft > hard, (hard, soft)


def test_soft_beats_hard_under_violations_unhcr():
    # unhcr carries 156 gates — the instrument the softening exists for
    frame, schema = load("unhcr")
    hard = violation_log_score(gated_marginal, frame, schema)
    soft = violation_log_score(soft_gated_marginal, frame, schema)
    print(f"\nviolation sim unhcr: hard {hard:.4f} soft {soft:.4f} "
          f"delta {soft - hard:+.4f}")
    assert soft > hard + 0.01, (hard, soft)
