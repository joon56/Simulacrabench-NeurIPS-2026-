"""Phase-2 instruments: a household sim whose twins land in
TRAIN/DEV/TEST at the split's proportions (DEV twins visible, TEST twins
scored under sample_rows(phase=2)), and the recorded null of lifting the
calibration replay cap (E031: +0.0000 phase 1, +0.0005 phase 2)."""

import numpy as np
import pandas as pd
import pytest

from src.models import hh_cap, hh_sharp, hier_backoff
from tests.test_soft_gating import KIT, load
from tests.test_hh_link import ROSTER_PREFIXES

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def hh_inject_rho_p2(frame, schema, frac, seed, lo, hi):
    """tests.test_hh_sharp.hh_inject_rho with twins assigned to
    TRAIN/DEV/TEST in the dataset's own role proportions."""
    rng = np.random.default_rng(seed)
    records = schema["items"]
    gated_value = schema["gated_value"]
    given = [n for n, r in records.items()
             if r["class"] == "GIVEN" and n != "wave"]
    roster = [n for n in given if n.startswith(ROSTER_PREFIXES)]
    person = [n for n in given if n not in roster]
    base = frame.copy()
    take = base[base["wave"] == "1"].sample(frac=frac, random_state=seed)
    twins = take.copy()
    twins["respondent_id"] = ["hh_%d" % i for i in range(len(twins))]
    split = base["role"].value_counts(normalize=True)
    twins["role"] = rng.choice(
        ["TRAIN", "DEV", "TEST"], size=len(twins),
        p=[split["TRAIN"], split["DEV"], split["TEST"]])
    for col in person:
        vals = list(records[col]["values"])
        twins[col] = [vals[rng.integers(len(vals))]
                      for _ in range(len(twins))]
    for item, r in records.items():
        if r["class"] != "PREDICT" or item not in twins.columns:
            continue
        rho = rng.uniform(lo, hi)
        vals = list(r["values"])
        cur = twins[item].to_numpy(dtype=object)
        keep = rng.random(len(twins)) < rho
        for i in np.flatnonzero(~keep):
            if pd.isna(cur[i]) or cur[i] == gated_value:
                continue
            cur[i] = vals[rng.integers(len(vals))]
        twins[item] = cur
    return pd.concat([base, twins], ignore_index=True)


def test_phase2_sim_has_all_roles():
    frame, schema = load("unhcr")
    sim = hh_inject_rho_p2(frame, schema, 0.3, 13, 0.2, 0.8)
    twins = sim[sim["respondent_id"].astype(str).str.startswith("hh_")]
    assert set(twins["role"]) == {"TRAIN", "DEV", "TEST"}
    merged, cells, truth = sample_rows(schema, sim, 2)
    assert len(cells) > 0


def test_cap_lift_is_within_noise_phase2():
    """Recorded E031 measurement: lifting CAL_QUERIES from 6000 to all
    visible rows moves the phase-2 household sim by +0.0005."""
    frame, schema = load("unhcr")
    sim = hh_inject_rho_p2(frame, schema, 0.3, 13, 0.2, 0.8)
    merged, cells, truth = sample_rows(schema, sim, 2)
    config = load_config(str(KIT / "config.yml"))
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)
    out = {}
    for cap in (6000, 10 ** 9):
        hh_sharp.CAL_QUERIES = cap
        try:
            v = hh_cap.predict(merged, schema, cols=cols, kappas=kappas)
        finally:
            hh_sharp.CAL_QUERIES = 6000
        v = floored(v, schema, cells, config["scoring"]["floor"])
        out[cap] = grade(schema, config, v, truth, cells)["log_score"]
    delta = out[10 ** 9] - out[6000]
    print(f"\nphase-2 household sim cap lift: {delta:+.4f}")
    assert abs(delta) < 0.002
