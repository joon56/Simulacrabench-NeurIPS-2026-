"""E036 tests. (a) Household sim with same-round twins only: the
cross-round buckets fall back and E036 equals E025. (b) Panel sim:
half the twins are moved to the other round with a HIGHER copy rate
(panel recurrence is more stable than co-respondent agreement) — the
relation-split λ must beat the pooled λ."""

import numpy as np
import pandas as pd
import pytest

from src.models import hh_cap, hier_backoff, wave_lam
from tests.test_soft_gating import KIT, load
from tests.test_hh_link import ROSTER_PREFIXES

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def panel_inject(frame, schema, frac, seed, same_rho, cross_rho,
                 cross_frac=0.5):
    """Twins of wave-1 rows: a cross_frac share is placed in wave 2 with
    per-item copy rates from cross_rho, the rest stay in wave 1 with
    rates from same_rho. Person columns resampled as in hh_inject_rho."""
    rng = np.random.default_rng(seed)
    records = schema["items"]
    gv = schema["gated_value"]
    given = [n for n, r in records.items()
             if r["class"] == "GIVEN" and n != "wave"]
    roster = [n for n in given if n.startswith(ROSTER_PREFIXES)]
    person = [n for n in given if n not in roster]
    base = frame.copy()
    take = base[base["wave"] == "1"].sample(frac=frac, random_state=seed)
    twins = take.copy()
    twins["respondent_id"] = ["hh_%d" % i for i in range(len(twins))]
    twins["role"] = rng.choice(["TRAIN", "DEV"], size=len(twins),
                               p=[0.8, 0.2])
    cross = rng.random(len(twins)) < cross_frac
    twins["wave"] = np.where(cross, "2", "1").astype(object)
    for col in person:
        vals = list(records[col]["values"])
        twins[col] = [vals[rng.integers(len(vals))]
                      for _ in range(len(twins))]
    for item, r in records.items():
        if r["class"] != "PREDICT" or item not in twins.columns:
            continue
        rho_same = rng.uniform(*same_rho)
        rho_cross = rng.uniform(*cross_rho)
        vals = list(r["values"])
        cur = twins[item].to_numpy(dtype=object)
        rho = np.where(cross, rho_cross, rho_same)
        keep = rng.random(len(twins)) < rho
        for i in np.flatnonzero(~keep):
            if pd.isna(cur[i]) or cur[i] == gv:
                continue
            cur[i] = vals[rng.integers(len(vals))]
        twins[item] = cur
    return pd.concat([base, twins], ignore_index=True)


def _scorer(sim, schema):
    merged, cells, truth = sample_rows(schema, sim, 1)
    config = load_config(str(KIT / "config.yml"))
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)

    def scored(model):
        v = model.predict(merged, schema, cols=cols, kappas=kappas)
        v = floored(v, schema, cells, config["scoring"]["floor"])
        return grade(schema, config, v, truth, cells)["log_score"]
    return scored


def test_same_round_twins_only_reduce_to_e025():
    frame, schema = load("unhcr")
    sim = panel_inject(frame, schema, 0.3, 13, (0.2, 0.8), (0.2, 0.8),
                       cross_frac=0.0)
    scored = _scorer(sim, schema)
    e025, e036 = scored(hh_cap), scored(wave_lam)
    print(f"\nsame-round sim: E025 {e025:.4f} E036 {e036 - e025:+.4f}")
    # not bit-exact: random k-NN top candidates from the other round
    # populate the cross buckets even without cross-round twins
    # (measured +0.0010) — must stay within noise of E025
    assert abs(e036 - e025) < 0.002


def test_panel_relation_split_beats_pooled():
    frame, schema = load("unhcr")
    sim = panel_inject(frame, schema, 0.4, 21, (0.2, 0.5), (0.7, 0.95),
                       cross_frac=0.5)
    scored = _scorer(sim, schema)
    e025, e036 = scored(hh_cap), scored(wave_lam)
    print(f"\npanel sim: E025 {e025:.4f} E036 {e036 - e025:+.4f}")
    assert e036 > e025 + 0.003
