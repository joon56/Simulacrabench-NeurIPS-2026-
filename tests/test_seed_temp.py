"""E029 tests: the ensemble wrapper is exact at identity settings, and a
multi-seed ensemble averages member distributions at temperature T."""

import numpy as np
import torch
import pytest

from src.models import hh_cap, seed_temp
from src.models.shared_trunk import _Net, _proba_maps
from tests.test_soft_gating import KIT, load

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def test_identity_settings_reproduce_e025():
    frame, schema = load("unicef")
    merged, cells, truth = sample_rows(schema, frame, 1)
    config = load_config(str(KIT / "config.yml"))

    def scored(fn):
        v = fn(merged, schema)
        v = floored(v, schema, cells, config["scoring"]["floor"])
        return grade(schema, config, v, truth, cells)["log_score"]

    base = scored(hh_cap.predict)
    same = scored(lambda f, s: seed_temp.predict(f, s, n_seeds=1,
                                                 t_grid=(1.0,)))
    assert abs(base - same) < 1e-8


def test_ensemble_is_mean_of_member_softmax_at_temperature():
    torch.manual_seed(0)
    members = [_Net(5, [3, 4], [2]) for _ in range(3)]
    ens = seed_temp._Ensemble(members, temperature=1.5)
    X = torch.randn(7, 5)
    full, cond = _proba_maps(ens, X, ["a", "b"], ["g"])
    with torch.no_grad():
        exp_a = np.mean([torch.softmax(m(X)[0][0] / 1.5, 1).numpy()
                         for m in members], axis=0)
        exp_g = np.mean([torch.softmax(m(X)[1][0] / 1.5, 1).numpy()
                         for m in members], axis=0)
    assert np.allclose(full["a"], exp_a, atol=1e-6)
    assert np.allclose(cond["g"], exp_g, atol=1e-6)
    assert np.allclose(full["a"].sum(1), 1.0)
