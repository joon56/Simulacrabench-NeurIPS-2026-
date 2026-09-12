"""E032 probe instrument: the local decomposition must predict the
uniform-on-subset probe exactly, and the inversion must recover the
subset's per-cell skill."""

import numpy as np

from src.models import hh_cap, probes
from tests.test_soft_gating import KIT, load

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def test_probe_arithmetic_matches_grader_on_unicef():
    frame, schema = load("unicef")
    merged, cells, truth = sample_rows(schema, frame, 1)
    config = load_config(str(KIT / "config.yml"))
    floor = config["scoring"]["floor"]
    base = hh_cap.predict(merged, schema)
    dec = probes.decompose(base, truth, cells, schema, floor,
                           probes.gated_items)
    probed = probes.uniform_on(hh_cap.predict, probes.gated_items)
    s_ref = grade(schema, config, floored(base, schema, cells, floor),
                  truth, cells)["skill"]
    s_probe = grade(schema, config,
                    floored(probed(merged, schema), schema, cells, floor),
                    truth, cells)["skill"]
    assert abs(dec["share"] - probes.item_share(schema, probes.gated_items)) < 1e-12
    assert abs(dec["probe_skill"] - s_probe) < 1e-9
    assert abs(probes.read_probe(schema, probes.gated_items, s_ref, s_probe)
               - dec["skill_S"]) < 1e-9
    assert abs(dec["skill"] - s_ref) < 1e-9
