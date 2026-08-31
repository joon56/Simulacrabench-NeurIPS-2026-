"""E010 tests: degenerate to E008 on exact-gate data; conditional gain
under group-dependent gate violations; no loss under uniform violations.

The unhcr sims share one ladder/weight selection (computed on the clean
frame) across both models so the comparison isolates the agreement layer.
"""

import numpy as np
import pytest

from src.models import cond_agree, hier_backoff, logit_blend
from tests.test_soft_gating import KIT, load, inject_violations

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def test_vectors_valid_sample():
    frame, schema = load("sample")
    merged, _, _ = sample_rows(schema, frame, 1)
    out = cond_agree.predict(merged, schema)
    assert len(out) > 0
    for vec in out:
        assert np.all(np.isfinite(vec))
        assert np.all(vec >= 0)
        assert vec.sum() == pytest.approx(1.0, abs=1e-6)


def test_clean_sandbox_close_to_e008():
    """Exact gates -> agreement ~1 -> E010 must track E008 closely."""
    frame, schema = load("sample")
    merged, _, _ = sample_rows(schema, frame, 1)
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)
    w, _ = logit_blend.tune_weight(merged, schema, cols, kappas)
    ours = cond_agree.predict(merged, schema, cols=cols, kappas=kappas,
                              w=w)
    e008 = logit_blend.predict(merged, schema, cols=cols, kappas=kappas,
                               w=w)
    assert len(ours) == len(e008)
    for a, b in zip(ours, e008):
        assert np.allclose(a, b, atol=5e-3)


def group_inject(frame, schema, group_col, rates, seed):
    """Flip gated child cells at a per-group rate (gate-violation sim)."""
    rng = np.random.default_rng(seed)
    out = frame.copy()
    gated_value = schema["gated_value"]
    group = out[group_col]
    rate = group.map(rates).fillna(0.0).to_numpy(dtype=float)
    for item, r in schema["items"].items():
        gate = r.get("gate")
        if not gate or r["class"] == "EXCLUDE" or item not in out.columns:
            continue
        flip = out[item].notna() & (rng.random(len(out)) < rate)
        values = list(r["values"])
        for i in out.index[flip]:
            if out.at[i, item] == gated_value:
                out.at[i, item] = values[rng.integers(len(values))]
            else:
                out.at[i, item] = gated_value
    return out


def scored(model, violated, schema, cols, kappas, w):
    config = load_config(str(KIT / "config.yml"))
    merged, cells, truth = sample_rows(schema, violated, 1)
    vectors = model.predict(merged, schema, cols=cols, kappas=kappas, w=w)
    vectors = floored(vectors, schema, cells, config["scoring"]["floor"])
    return grade(schema, config, vectors, truth, cells)["log_score"]


@pytest.fixture(scope="module")
def unhcr_setup():
    frame, schema = load("unhcr")
    merged, _, _ = sample_rows(schema, frame, 1)
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)
    w, _ = logit_blend.tune_weight(merged, schema, cols, kappas)
    records = schema["items"]
    group_col = next(n for n, r in records.items()
                     if r["class"] == "GIVEN" and len(r["values"]) <= 6)
    values = records[group_col]["values"]
    rates = {v: (0.35 if i % 2 == 0 else 0.02)
             for i, v in enumerate(values)}
    return frame, schema, cols, kappas, w, group_col, rates


def test_conditional_beats_scalar_under_group_violations(unhcr_setup):
    frame, schema, cols, kappas, w, group_col, rates = unhcr_setup
    violated = group_inject(frame, schema, group_col, rates, seed=1)
    scalar = scored(logit_blend, violated, schema, cols, kappas, w)
    cond = scored(cond_agree, violated, schema, cols, kappas, w)
    print(f"\ngroup-violation sim unhcr ({group_col}): "
          f"scalar {scalar:.4f} cond {cond:.4f} delta {cond - scalar:+.4f}")
    assert cond > scalar + 0.005, (scalar, cond)


def test_conditional_matches_scalar_under_uniform_violations(unhcr_setup):
    frame, schema, cols, kappas, w, _, _ = unhcr_setup
    violated = inject_violations(frame, schema, rate=0.17, seed=1)
    scalar = scored(logit_blend, violated, schema, cols, kappas, w)
    cond = scored(cond_agree, violated, schema, cols, kappas, w)
    print(f"\nuniform-violation sim unhcr: "
          f"scalar {scalar:.4f} cond {cond:.4f} delta {cond - scalar:+.4f}")
    assert cond >= scalar - 0.002, (scalar, cond)
