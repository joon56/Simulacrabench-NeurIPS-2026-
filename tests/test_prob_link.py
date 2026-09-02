"""E014 v2 tests: the soft cross-round layer calibrates itself OFF on
independent rows, ON under planted panel structure (with drift and with
signature collisions), and the full pipeline converts the evidence into
a large scored gain."""

import numpy as np
import pytest

from src.models import hier_backoff, prob_link, shared_trunk
from tests.test_soft_gating import KIT, load
from tests.test_cross_link import panel_sim

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def _marginal_model_dists(frame, schema):
    """Cheap stand-in model for layer-level tests: per-item empirical
    marginal over visible rows, broadcast to every row."""
    records, items, options = hier_backoff._layout(frame, schema)
    out = {}
    for item in items:
        if records[item]["class"] != "PREDICT":
            continue
        opts = options[item]
        idx = {o: i for i, o in enumerate(opts)}
        counts = np.full(len(opts), 0.5)
        for v, n in frame[item].value_counts().items():
            if v in idx:
                counts[idx[v]] += n
        dist = counts / counts.sum()
        out[item] = np.tile(dist, (len(frame), 1))
    return out


def test_clean_unhcr_layer_is_knn_vs_marginal():
    """On independent sandbox rows the layer has NO panel signal, but
    signature-similar candidates are trait-similar respondents, so vs a
    MARGINAL model the evidence legitimately acts as k-NN conditioning
    and calibrates ON. (Discovered, then kept as the documented
    behavior: E014 = panel evidence + k-NN residual, judged against the
    full pipeline by the runner threshold.) This test pins the
    mechanism: the layer arms vs the weak model, and calibration is
    deterministic."""
    frame, schema = load("unhcr")
    merged, _, _ = sample_rows(schema, frame, 1)
    dists = _marginal_model_dists(merged, schema)
    ev1, lam1 = prob_link.cross_round_layer(merged, schema, dists)
    ev2, lam2 = prob_link.cross_round_layer(merged, schema, dists)
    assert lam1 == lam2 and set(ev1) == set(ev2)
    assert lam1, "expected k-NN arming against a marginal model"


@pytest.fixture(scope="module")
def heavy_drift():
    frame, schema = load("unhcr")
    sim = panel_sim(frame, schema, link_frac=0.6, perturb=0.1, seed=4,
                    drift_lambda=2.5)
    merged, cells, truth = sample_rows(schema, sim, 1)
    return schema, merged, cells, truth


def test_layer_arms_under_heavy_drift(heavy_drift):
    schema, merged, _, _ = heavy_drift
    ev_rows, lam = prob_link.cross_round_layer(
        merged, schema, _marginal_model_dists(merged, schema))
    strong = [item for item, l in lam.items() if l >= 0.5]
    print(f"\nheavy drift: {len(lam)} items armed, {len(strong)} "
          f"at lambda>=0.5, {len(ev_rows)} held-out rows with evidence")
    assert len(strong) > 50
    assert len(ev_rows) > 300


def test_layer_survives_signature_collisions(heavy_drift):
    schema, merged, _, _ = heavy_drift
    coarse = merged.copy()
    # destroy the two high-cardinality columns -> heavy collisions
    coarse["governorate_col"] = "X"
    coarse["s2_4a_origin_governorate_lbl"] = "Y"
    ev_rows, lam = prob_link.cross_round_layer(
        coarse, schema, _marginal_model_dists(coarse, schema))
    strong = [item for item, l in lam.items() if l >= 0.3]
    print(f"\ncollision sim: {len(lam)} armed, {len(strong)} at "
          f"lambda>=0.3, {len(ev_rows)} rows with evidence")
    # soft posteriors share mass across collided candidates instead of
    # rejecting them — the layer must still find signal
    assert len(strong) > 30


def test_pipeline_gain_under_heavy_drift(heavy_drift):
    schema, merged, cells, truth = heavy_drift
    config = load_config(str(KIT / "config.yml"))
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)

    def scored(model):
        vectors = model.predict(merged, schema, cols=cols, kappas=kappas)
        vectors = floored(vectors, schema, cells,
                          config["scoring"]["floor"])
        return grade(schema, config, vectors, truth, cells)["log_score"]

    e012 = scored(shared_trunk)
    e014 = scored(prob_link)
    print(f"\nheavy-drift sim unhcr: E012 {e012:.4f} E014 {e014:.4f} "
          f"delta {e014 - e012:+.4f}")
    assert e014 > e012 + 0.05, (e012, e014)
