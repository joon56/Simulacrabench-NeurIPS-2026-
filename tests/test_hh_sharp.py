"""E022 tests: on the harder household sim (per-item copy rate
rho in [0.2, 0.8]) the composition must beat both parents and E018."""

import numpy as np
import pandas as pd
import pytest

from src.models import dup_link, hh_link, hh_sharp, hier_backoff, link_sharp
from tests.test_soft_gating import KIT, load
from tests.test_hh_link import ROSTER_PREFIXES

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def hh_inject_rho(frame, schema, frac, seed, lo, hi):
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
    twins["role"] = rng.choice(["TRAIN", "DEV"], size=len(twins),
                               p=[0.8, 0.2])
    for col in person:
        vals = list(records[col]["values"])
        twins[col] = [vals[rng.integers(len(vals))]
                      for _ in range(len(twins))]
    for item, r in records.items():
        if r["class"] != "PREDICT" or item not in twins.columns:
            continue
        rho = rng.uniform(lo, hi)
        vals = list(r["values"])
        cur = twins[item].to_numpy(dtype=object, copy=True)
        keep = rng.random(len(twins)) < rho
        for i in np.flatnonzero(~keep):
            if pd.isna(cur[i]) or cur[i] == gated_value:
                continue
            cur[i] = vals[rng.integers(len(vals))]
        twins[item] = cur
    return pd.concat([base, twins], ignore_index=True)


@pytest.fixture(scope="module")
def hard_sim():
    frame, schema = load("unhcr")
    sim = hh_inject_rho(frame, schema, 0.3, 13, 0.2, 0.8)
    merged, cells, truth = sample_rows(schema, sim, 1)
    config = load_config(str(KIT / "config.yml"))
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)

    def scored(model):
        v = model.predict(merged, schema, cols=cols, kappas=kappas)
        v = floored(v, schema, cells, config["scoring"]["floor"])
        return grade(schema, config, v, truth, cells)["log_score"]

    return {m.__name__.split(".")[-1]: scored(m)
            for m in (dup_link, link_sharp, hh_link, hh_sharp)}


def test_composition_beats_parents(hard_sim):
    e018, e019 = hard_sim["dup_link"], hard_sim["link_sharp"]
    e021, e022 = hard_sim["hh_link"], hard_sim["hh_sharp"]
    print(f"\nhard household sim: E018 {e018:.4f} | E019 {e019 - e018:+.4f}"
          f" E021 {e021 - e018:+.4f} E022 {e022 - e018:+.4f}")
    assert e022 > max(e019, e021) + 0.003
    assert e022 > e018 + 0.010
