"""E024: evidence-input net as base inside E022. The household sim has
little cross-item structure, so the pre-registered local check is
NO-HARM (> -0.005 vs E022); a real gain is a leaderboard question."""

import pytest

from src.models import ev_base, hh_sharp, hier_backoff
from tests.test_soft_gating import KIT, load
from tests.test_hh_sharp import hh_inject_rho

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def test_no_harm_vs_e022_on_household_sim():
    frame, schema = load("unhcr")
    sim = hh_inject_rho(frame, schema, 0.3, 13, 0.2, 0.8)
    merged, cells, truth = sample_rows(schema, sim, 1)
    config = load_config(str(KIT / "config.yml"))
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)

    def scored(model):
        v = model.predict(merged, schema, cols=cols, kappas=kappas)
        v = floored(v, schema, cells, config["scoring"]["floor"])
        return grade(schema, config, v, truth, cells)["log_score"]

    e022 = scored(hh_sharp)
    e024 = scored(ev_base)
    print(f"\nhousehold sim: E022 {e022:.4f} E024 {e024:.4f} "
          f"delta {e024 - e022:+.4f}")
    assert e024 > e022 - 0.005, (e022, e024)
