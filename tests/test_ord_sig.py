"""E030 tests. (a) With no ordinal drift among near-duplicates the
adjacency weights calibrate to ~0 and E030 stays within noise of E025.
(b) On a household sim whose twins drift one level on roster counts /
age band (a birth, a departure, a birthday between CATI rounds), E030
recovers the matches E025 loses and beats it."""

import numpy as np
import pandas as pd
import pytest

from src.models import hh_cap, hier_backoff, ord_sig
from src.models.ord_sig import ordinal_ranks
from tests.test_soft_gating import KIT, load
from tests.test_hh_sharp import hh_inject_rho
from tests.test_prob_link import _marginal_model_dists

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402

ROSTER_PREFIX = "s2_3_"
AGE_COL = "s2_1b_age"


def drift_ordinal(sim, schema, p_roster, p_age, seed):
    """Shift twins' roster counts by ±1 level with prob p_roster per
    column and the age band by +1 with prob p_age (clamped to range)."""
    rng = np.random.default_rng(seed)
    records = schema["items"]
    out = sim.copy()
    twins = out["respondent_id"].astype(str).str.startswith("hh_")
    idx = np.flatnonzero(twins.to_numpy())
    for col, r in records.items():
        if r["class"] != "GIVEN":
            continue
        table = ordinal_ranks(list(r["values"]))
        if table is None:
            continue
        if col.startswith(ROSTER_PREFIX):
            p, steps = p_roster, (-1, 1)
        elif col == AGE_COL:
            p, steps = p_age, (1,)
        else:
            continue
        inv = {v: k for k, v in table.items()}
        vals = out[col].to_numpy(dtype=object)
        for i in idx:
            if rng.random() >= p:
                continue
            rk = table.get(vals[i])
            if rk is None:
                continue
            new = rk + steps[rng.integers(len(steps))]
            if new in inv:
                vals[i] = inv[new]
        out[col] = vals
    return out


def test_ordinal_ranks_parse_schema_bands():
    assert ordinal_ranks(["0", "1", "2", "6-10", "11+"]) == \
        {"0": 0, "1": 1, "2": 2, "6-10": 3, "11+": 4}
    assert ordinal_ranks(["18-24", "25-34", "65+", "[generalised:s2]"]) \
        == {"18-24": 0, "25-34": 1, "65+": 2}
    assert ordinal_ranks(["1. Head", "2. Spouse", "3. Child"]) is None
    assert ordinal_ranks(["Yes", "No"]) is None


def _scorer(merged, schema, cells, truth):
    config = load_config(str(KIT / "config.yml"))
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)

    def scored(model):
        v = model.predict(merged, schema, cols=cols, kappas=kappas)
        v = floored(v, schema, cells, config["scoring"]["floor"])
        return grade(schema, config, v, truth, cells)["log_score"]
    return scored


@pytest.fixture(scope="module")
def sims():
    frame, schema = load("unhcr")
    base = hh_inject_rho(frame, schema, 0.3, 13, 0.2, 0.8)
    drift = drift_ordinal(base, schema, p_roster=0.15, p_age=0.10,
                          seed=17)
    out = {}
    for name, sim in (("nodrift", base), ("drift", drift)):
        merged, cells, truth = sample_rows(schema, sim, 1)
        out[name] = (schema, merged, _scorer(merged, schema, cells, truth))
    return out


def test_no_drift_adjacency_weights_near_zero(sims):
    schema, merged, _ = sims["nodrift"]
    _, _, (w, v) = ord_sig.ord_sharp_layer(
        merged, schema, _marginal_model_dists(merged, schema),
        return_weights=True)
    print(f"\nno-drift adjacency weights: max {v.max():.3f} "
          f"(exact max {w.max():.2f})")
    assert v.max() < 0.25 * w.max()


def test_drift_adjacency_weights_arm(sims):
    schema, merged, _ = sims["drift"]
    records, items, _ = hier_backoff._layout(merged, schema)
    given = [n for n in items if records[n]["class"] == "GIVEN"]
    _, _, (w, v) = ord_sig.ord_sharp_layer(
        merged, schema, _marginal_model_dists(merged, schema),
        return_weights=True)
    vv = dict(zip(given, v))
    roster_v = np.mean([vv[c] for c in given if c.startswith(ROSTER_PREFIX)])
    print(f"\ndrift adjacency weights: roster mean {roster_v:.2f} "
          f"age {vv[AGE_COL]:.2f}")
    assert roster_v > 0.5


def test_no_drift_parity_with_e025(sims):
    _, _, scored = sims["nodrift"]
    e025, e030 = scored(hh_cap), scored(ord_sig)
    print(f"\nno-drift household sim: E025 {e025:.4f} E030 {e030 - e025:+.4f}")
    assert abs(e030 - e025) < 0.002


@pytest.mark.xfail(strict=True, reason="E030 recorded null: drift sim "
                   "+0.0013 (ceiling +0.0025 at forced half credit)")
def test_drift_e030_beats_e025(sims):
    _, _, scored = sims["drift"]
    e025, e030 = scored(hh_cap), scored(ord_sig)
    print(f"\ndrift household sim: E025 {e025:.4f} E030 {e030 - e025:+.4f}")
    assert e030 > e025 + 0.005
