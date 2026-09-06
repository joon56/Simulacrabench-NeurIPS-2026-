"""E021 tests on a HOUSEHOLD sim: twins share the roster GIVEN block,
resample the person-level GIVEN columns, and copy answers per item
with item-specific probability. The instrument must (a) reproduce the
real E019 flat and (b) show E021's learned weights separating roster
from person columns and beating E018."""

import numpy as np
import pandas as pd
import pytest

from src.models import dup_link, hh_link, hier_backoff, link_sharp
from tests.test_soft_gating import KIT, load
from tests.test_prob_link import _marginal_model_dists

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402

ROSTER_PREFIXES = ("s2_3_", "governorate_col", "s2_4a_", "s1_2_")


def hh_inject(frame, schema, frac, seed):
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
        rho = rng.uniform(0.3, 0.95)
        vals = list(r["values"])
        cur = twins[item].to_numpy(dtype=object)
        keep = rng.random(len(twins)) < rho
        for i in np.flatnonzero(~keep):
            if pd.isna(cur[i]) or cur[i] == gated_value:
                continue
            cur[i] = vals[rng.integers(len(vals))]
        twins[item] = cur
    return pd.concat([base, twins], ignore_index=True), roster, person


@pytest.fixture(scope="module")
def hh_sim():
    frame, schema = load("unhcr")
    sim, roster, person = hh_inject(frame, schema, frac=0.3, seed=11)
    merged, cells, truth = sample_rows(schema, sim, 1)
    config = load_config(str(KIT / "config.yml"))
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)

    def scored(model):
        vectors = model.predict(merged, schema, cols=cols, kappas=kappas)
        vectors = floored(vectors, schema, cells,
                          config["scoring"]["floor"])
        return grade(schema, config, vectors, truth, cells)["log_score"]

    return {"schema": schema, "merged": merged, "roster": roster,
            "person": person, "scored": scored,
            "e018": scored(dup_link)}


def test_learned_weights_separate_roster_from_person(hh_sim):
    schema, merged = hh_sim["schema"], hh_sim["merged"]
    records, items, options = hier_backoff._layout(merged, schema)
    given = [n for n in items if records[n]["class"] == "GIVEN"]
    _, _, weights = hh_link.household_layer(
        merged, schema, _marginal_model_dists(merged, schema),
        return_weights=True)
    assert weights is not None
    w = dict(zip(given, weights))
    roster_w = np.mean([w[c] for c in hh_sim["roster"]])
    person_w = np.mean([w[c] for c in hh_sim["person"]])
    print(f"\nlearned weights: roster mean {roster_w:.2f} "
          f"person mean {person_w:.2f}")
    assert roster_w > 2 * person_w


def test_instrument_reproduces_e019_flat(hh_sim):
    e018 = hh_sim["e018"]
    e019 = hh_sim["scored"](link_sharp)
    print(f"\nhousehold sim: E018 {e018:.4f} E019 {e019:.4f} "
          f"delta {e019 - e018:+.4f}")
    assert abs(e019 - e018) < 0.012


def test_e021_beats_e018(hh_sim):
    e018 = hh_sim["e018"]
    e021 = hh_sim["scored"](hh_link)
    print(f"\nhousehold sim: E018 {e018:.4f} E021 {e021:.4f} "
          f"delta {e021 - e018:+.4f}")
    assert e021 > e018 + 0.005, (e018, e021)
