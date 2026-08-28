import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.eval.split import holdout_visible
from src.models import gated_marginal, stratum_backoff

KIT = Path(__file__).resolve().parents[1] / "external" / "starter-kit"


def load_sample():
    with open(KIT / "data" / "sample.json", encoding="utf-8") as f:
        schema = json.load(f)
    schema.setdefault("gated_value", "NA_GATED")
    frame = pd.read_parquet(KIT / "_sandbox" / "sample" / "respondents.parquet")
    items = [n for n, r in schema["items"].items()
             if r["class"] in ("GIVEN", "PREDICT")]
    train = frame[frame["role"] == "TRAIN"]
    dev = frame[frame["role"] == "DEV"].copy()
    predict_cols = [n for n, r in schema["items"].items()
                    if r["class"] == "PREDICT"]
    dev[predict_cols] = np.nan
    merged = pd.concat([train, dev], ignore_index=True)
    return merged[["respondent_id"] + items], schema


def test_kappa_infinity_equals_e002():
    frame, schema = load_sample()
    ours = stratum_backoff.predict(frame, schema,
                                   strat_cols=["region"], kappa=1e12)
    e002 = gated_marginal.predict(frame, schema)
    assert len(ours) == len(e002)
    for a, b in zip(ours, e002):
        assert np.allclose(a, b, atol=1e-9)


def test_vectors_valid():
    frame, schema = load_sample()
    out = stratum_backoff.predict(frame, schema)
    assert len(out) > 0
    for vec in out:
        assert np.all(np.isfinite(vec))
        assert np.all(vec >= 0)
        assert vec.sum() == pytest.approx(1.0, abs=1e-6)


def test_holdout_visible_masks_only_predict():
    frame, schema = load_sample()
    fit_rows, eval_rows = holdout_visible(frame, schema, frac=0.25, seed=0)
    items = [n for n, r in schema["items"].items()
             if r["class"] in ("GIVEN", "PREDICT")]
    # both parts are complete visible rows; together they are all of them
    assert fit_rows[items].notna().all().all()
    assert eval_rows[items].notna().all().all()
    n_complete = frame[items].notna().all(axis=1).sum()
    assert len(fit_rows) + len(eval_rows) == n_complete
    assert 0.15 < len(eval_rows) / n_complete < 0.35


def test_stratum_conditioning_changes_predictions():
    frame, schema = load_sample()
    flat = stratum_backoff.predict(frame, schema, strat_cols=[], kappa=1.0)
    strat = stratum_backoff.predict(frame, schema,
                                    strat_cols=["region"], kappa=1.0)
    diffs = [np.abs(a - b).max() for a, b in zip(flat, strat)]
    assert max(diffs) > 1e-4
