"""E020 tests on the RE-CALIBRATED dup sim (40% answer perturbation —
E019's real flat showed the 10% sim was too clean): E019 ≈ E018
reproduces the leaderboard, and the evidence-as-input net beats E018."""

import numpy as np
import pytest

from src.models import dup_link, ev_net, hier_backoff, link_sharp
from tests.test_soft_gating import KIT, load
from tests.test_dup_link import dup_inject

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


@pytest.fixture(scope="module")
def noisy_sim():
    frame, schema = load("unhcr")
    sim = dup_inject(frame, schema, frac=0.3, perturb=0.4, seed=7)
    merged, cells, truth = sample_rows(schema, sim, 1)
    config = load_config(str(KIT / "config.yml"))
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)

    def scored(model):
        vectors = model.predict(merged, schema, cols=cols, kappas=kappas)
        vectors = floored(vectors, schema, cells,
                          config["scoring"]["floor"])
        return grade(schema, config, vectors, truth, cells)["log_score"]

    return {"e018": scored(dup_link), "scored": scored}


def test_evidence_block_shape():
    frame, schema = load("sample")
    merged, _, _ = sample_rows(schema, frame, 1)
    block, predict_items = ev_net.evidence_block(
        merged.reset_index(drop=True), schema)
    records, items, options = hier_backoff._layout(merged, schema)
    assert block.shape == (len(merged),
                           sum(len(options[n]) for n in predict_items))
    # each item's slice is a (sub-)distribution: sums in [0, 1]
    off = 0
    for item in predict_items:
        k = len(options[item])
        s = block[:, off:off + k].sum(axis=1)
        assert np.all(s <= 1.0 + 1e-6) and np.all(s >= -1e-6)
        off += k


@pytest.mark.xfail(
    reason="E020 rejected: on the noisy dup sim the copy-mixture (E018) beats the evidence-input net, and the sim itself over-credits E019 — kept as the recorded null (see E020 attempt log)", strict=True)
def test_recalibrated_sim_reproduces_e019_flat(noisy_sim):
    e018 = noisy_sim["e018"]
    e019 = noisy_sim["scored"](link_sharp)
    print(f"\nnoisy sim: E018 {e018:.4f} E019 {e019:.4f} "
          f"delta {e019 - e018:+.4f}")
    # on the clean 10% sim E019 was +0.031; the real leaderboard was
    # flat — a well-calibrated instrument shows |delta| small here
    assert abs(e019 - e018) < 0.012


@pytest.mark.xfail(
    reason="E020 rejected: on the noisy dup sim the copy-mixture (E018) beats the evidence-input net, and the sim itself over-credits E019 — kept as the recorded null (see E020 attempt log)", strict=True)
def test_ev_net_beats_e018_on_noisy_sim(noisy_sim):
    e018 = noisy_sim["e018"]
    e020 = noisy_sim["scored"](ev_net)
    print(f"\nnoisy sim: E018 {e018:.4f} E020 {e020:.4f} "
          f"delta {e020 - e018:+.4f}")
    assert e020 > e018 + 0.005, (e018, e020)
