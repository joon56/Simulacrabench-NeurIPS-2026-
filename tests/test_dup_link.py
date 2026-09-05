"""E018 tests: self-exclusion in the calibration replay; within-round
duplicate sim where E014's cross-round pools are blind but the full
pool sees the twins."""

import numpy as np
import pandas as pd
import pytest

from src.models import dup_link, hier_backoff, prob_link, shared_trunk
from tests.test_soft_gating import KIT, load
from tests.test_prob_link import _marginal_model_dists

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def test_self_exclusion():
    codes = np.array([[0, 1], [0, 1], [2, 3]], dtype=np.int32)
    weights = np.array([1.0, 1.0])
    pos = np.arange(3)
    out = dup_link._topk_excl(codes, weights, pos, pos, k=3)
    for q, (cands, probs) in zip(pos, out):
        assert q not in cands  # never its own candidate
        assert probs.sum() == pytest.approx(1.0)
    # row 0's best match must be its duplicate row 1, not itself
    cands0, probs0 = out[0]
    assert cands0[np.argmax(probs0)] == 1


def dup_inject(frame, schema, frac, perturb, seed):
    """Duplicate a fraction of round-1 rows WITHIN round 1 (perturbed
    answers, straddling roles) — invisible to cross-round pools."""
    rng = np.random.default_rng(seed)
    records = schema["items"]
    gated_value = schema["gated_value"]
    base = frame.copy()
    take = base[base["wave"] == "1"].sample(frac=frac, random_state=seed)
    twins = take.copy()
    twins["respondent_id"] = ["dup_%d" % i for i in range(len(twins))]
    twins["role"] = rng.choice(["TRAIN", "DEV"], size=len(twins),
                               p=[0.8, 0.2])
    for item, r in records.items():
        if r["class"] != "PREDICT" or item not in twins.columns:
            continue
        vals = list(r["values"])
        flip = rng.random(len(twins)) < perturb
        cur = twins[item].to_numpy(dtype=object)
        for i in np.flatnonzero(flip):
            if pd.isna(cur[i]) or cur[i] == gated_value:
                continue
            cur[i] = vals[rng.integers(len(vals))]
        twins[item] = cur
    return pd.concat([base, twins], ignore_index=True)


@pytest.fixture(scope="module")
def dup_sim():
    frame, schema = load("unhcr")
    sim = dup_inject(frame, schema, frac=0.3, perturb=0.1, seed=5)
    merged, cells, truth = sample_rows(schema, sim, 1)
    return schema, merged, cells, truth


def test_full_pool_sees_within_round_twins(dup_sim):
    schema, merged, _, _ = dup_sim
    dists = _marginal_model_dists(merged, schema)
    ev14, lam14 = prob_link.cross_round_layer(merged, schema, dists)
    ev18, lam18 = dup_link.full_pool_layer(merged, schema, dists)
    strong14 = sum(1 for l in lam14.values() if l >= 0.5)
    strong18 = sum(1 for l in lam18.values() if l >= 0.5)
    print(f"\nwithin-round dup sim: E014 strong-lambda items {strong14}, "
          f"E018 {strong18}; evidence rows E014 {len(ev14)} "
          f"E018 {len(ev18)}")
    # cross-round pools are blind to within-round twins; the full pool
    # must arm far more strongly
    assert strong18 > strong14 + 50


def test_pipeline_gain_on_dup_sim(dup_sim):
    schema, merged, cells, truth = dup_sim
    config = load_config(str(KIT / "config.yml"))
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)

    def scored(model):
        vectors = model.predict(merged, schema, cols=cols, kappas=kappas)
        vectors = floored(vectors, schema, cells,
                          config["scoring"]["floor"])
        return grade(schema, config, vectors, truth, cells)["log_score"]

    e012 = scored(shared_trunk)
    e018 = scored(dup_link)
    print(f"\ndup sim unhcr: E012 {e012:.4f} E018 {e018:.4f} "
          f"delta {e018 - e012:+.4f}")
    assert e018 > e012 + 0.05, (e012, e018)
