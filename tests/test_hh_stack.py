"""E023 tests on the hard household sim: each refinement alone and the
composition vs E022."""

import functools

import pytest

from src.models import hh_sharp, hh_stack, hier_backoff
from tests.test_soft_gating import KIT, load
from tests.test_hh_sharp import hh_inject_rho

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


class _Variant:
    def __init__(self, **kw):
        self.kw = kw

    def predict(self, frame, schema, cols=None, kappas=None):
        return hh_stack.predict(frame, schema, cols=cols, kappas=kappas,
                                **self.kw)


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

    return {
        "e022": scored(hh_sharp),
        "k_only": scored(_Variant(k_grid=(3, 5, 10), em_iters=1)),
        "em_only": scored(_Variant(k_grid=(10,), em_iters=2)),
        "both": scored(hh_stack),
    }


@pytest.mark.xfail(reason="E023 rejected: K-select and a second EM iteration are null on the household sim (layer saturated at E022) — recorded null", strict=True)
def test_stack2_vs_e022(hard_sim):
    e022 = hard_sim["e022"]
    print(f"\nhard household sim: E022 {e022:.4f} | K-select "
          f"{hard_sim['k_only'] - e022:+.4f} | EM2 "
          f"{hard_sim['em_only'] - e022:+.4f} | both "
          f"{hard_sim['both'] - e022:+.4f}")
    assert hard_sim["both"] > e022 + 0.005
