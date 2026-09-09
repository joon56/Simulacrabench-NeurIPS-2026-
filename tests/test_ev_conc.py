"""E027: concentrated-row evidence input over E025 — no-harm checks
(the household sim carries no cross-item structure)."""

import numpy as np

from src.models import ev_conc, hh_cap, hier_backoff
from tests.test_soft_gating import KIT, load
from tests.test_hh_sharp import hh_inject_rho

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def test_block_zero_on_clean_sandbox():
    """Independent rows: no concentrated posteriors -> block all zeros."""
    frame, schema = load("sample")
    merged, _, _ = sample_rows(schema, frame, 1)
    block = ev_conc.concentrated_evidence_block(
        merged.reset_index(drop=True), schema)
    assert block.shape[0] == len(merged)
    # the sandbox has no duplicates; at most a handful of rows can be
    # concentrated by chance
    assert (np.abs(block).sum(axis=1) > 0).mean() < 0.05


def test_no_harm_vs_e025_on_household_sim():
    frame, schema = load("unhcr")
    sim = hh_inject_rho(frame, schema, 0.3, 13, 0.2, 0.8)
    merged, cells, truth = sample_rows(schema, sim, 1)
    config = load_config(str(KIT / "config.yml"))
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)

    def scored(model):
        v = model.predict(merged, schema, cols=cols, kappas=kappas)
        v = floored(v, schema, cells, config["scoring"]["floor"])
        return grade(schema, config, v, truth, cells)["log_score"]

    e025 = scored(hh_cap)
    e027 = scored(ev_conc)
    print(f"\nhousehold sim: E025 {e025:.4f} E027 {e027:.4f} "
          f"delta {e027 - e025:+.4f}")
    assert e027 > e025 - 0.005, (e025, e027)
