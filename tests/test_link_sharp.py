"""E019 tests: bucket/λ structure; scored gain over E018 on the
validated within-round dup sim."""

import numpy as np
import pytest

from src.models import dup_link, hier_backoff, link_sharp
from tests.test_soft_gating import KIT, load
from tests.test_dup_link import dup_inject
from tests.test_prob_link import _marginal_model_dists

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


@pytest.fixture(scope="module")
def dup_sim():
    frame, schema = load("unhcr")
    sim = dup_inject(frame, schema, frac=0.3, perturb=0.1, seed=5)
    merged, cells, truth = sample_rows(schema, sim, 1)
    return schema, merged, cells, truth


def test_lambda_pairs_and_ceiling(dup_sim):
    schema, merged, _, _ = dup_sim
    ev_rows, lam = link_sharp.sharp_layer(
        merged, schema, _marginal_model_dists(merged, schema))
    assert lam
    highs = [pair[1] for pair in lam.values()]
    lows = [pair[0] for pair in lam.values()]
    # concentrated bucket (exact twins) must reach past the old 0.9 cap
    assert max(highs) > 0.9
    # on average, concentrated lambda >= diffuse lambda
    assert np.mean(highs) > np.mean(lows)
    # evidence rows carry a boolean concentration flag
    for ev, conc in ev_rows.values():
        assert isinstance(conc, bool)
        break


def test_scored_gain_over_e018(dup_sim):
    schema, merged, cells, truth = dup_sim
    config = load_config(str(KIT / "config.yml"))
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)

    def scored(model):
        vectors = model.predict(merged, schema, cols=cols, kappas=kappas)
        vectors = floored(vectors, schema, cells,
                          config["scoring"]["floor"])
        return grade(schema, config, vectors, truth, cells)["log_score"]

    e018 = scored(dup_link)
    e019 = scored(link_sharp)
    print(f"\nsharpened dup sim unhcr: E018 {e018:.4f} E019 {e019:.4f} "
          f"delta {e019 - e018:+.4f}")
    assert e019 > e018 + 0.005, (e018, e019)
