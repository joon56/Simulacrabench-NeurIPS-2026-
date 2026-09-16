"""The sandbox oracle (Bayes-optimal GIVEN-only predictor) must bound every
GIVEN-only model from above; E025's base is within 0.004 of it on every
sandbox (A005), which is why base-model changes cannot clear the local
adoption threshold."""

from src.eval.oracle import oracle
from src.models import hh_cap
from tests.test_soft_gating import KIT, load

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def test_oracle_bounds_e025_on_unicef():
    frame, schema = load("unicef")
    merged, cells, truth = sample_rows(schema, frame, 1)
    config = load_config(str(KIT / "config.yml"))
    v = floored(hh_cap.predict(merged, schema), schema, cells,
                config["scoring"]["floor"])
    e025 = grade(schema, config, v, truth, cells)["skill"]
    best = oracle("unicef")["skill"]
    print(f"\nunicef oracle {best:.4f} E025 {e025:.4f}")
    assert best >= e025 - 1e-9
    assert best - e025 < 0.004
