"""E011 tests: kernel safety properties; degenerate to E010 on the clean
sandbox; clear gain on a synthetic ordinal-structure sim (the sandbox has
no ordinal structure by construction — A004 — so the sim is the only
local positive-evidence channel, as with E003/E010)."""

import numpy as np
import pytest

from src.models import cond_agree, hier_backoff, ordinal_smooth
from tests.test_soft_gating import KIT, load

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def test_numeric_ranks_detection():
    # coded labels must NOT be treated as numeric
    assert ordinal_smooth._numeric_ranks(
        ["0. No", "1. Yes", "98. I don't know", "NA_GATED"]) is None
    # spans with one non-numeric tail (sentinel) pass the K-1 rule
    ranks = ordinal_smooth._numeric_ranks(["0", "2", "3", "5", "NA_GATED"])
    assert ranks == {0: 0, 1: 1, 2: 2, 3: 3}
    # too small / too worded lists are rejected
    assert ordinal_smooth._numeric_ranks(["1", "2", "3"]) is None
    assert ordinal_smooth._numeric_ranks(
        ["1", "2", "Often", "Never"]) is None
    # unsorted numeric labels get value-ordered ranks
    ranks = ordinal_smooth._numeric_ranks(["10", "2", "0", "5"])
    assert ranks == {0: 3, 1: 1, 2: 0, 3: 2}


def test_kernel_matrix_properties():
    opts = ["0", "2", "3", "5", "NA_GATED"]
    M = ordinal_smooth.kernel_matrix(opts, 1.0)
    assert M.shape == (5, 5)
    assert np.allclose(M.sum(axis=1), 1.0)
    # sentinel row/column untouched
    assert M[4, 4] == 1.0 and np.allclose(M[4, :4], 0.0) \
        and np.allclose(M[:4, 4], 0.0)
    # smoothing decays with rank distance
    assert M[0, 1] > M[0, 3]
    # non-ordinal list -> no kernel
    assert ordinal_smooth.kernel_matrix(["a", "b", "c", "d"], 1.0) is None


def test_vectors_valid_sample():
    frame, schema = load("sample")
    merged, _, _ = sample_rows(schema, frame, 1)
    out = ordinal_smooth.predict(merged, schema)
    assert len(out) > 0
    for vec in out:
        assert np.all(np.isfinite(vec))
        assert np.all(vec >= 0)
        assert vec.sum() == pytest.approx(1.0, abs=1e-6)


def test_clean_sample_close_to_e010():
    frame, schema = load("sample")
    merged, _, _ = sample_rows(schema, frame, 1)
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)
    w, bw = ordinal_smooth.tune_weight_and_bandwidth(merged, schema,
                                                     cols, kappas)
    ours = ordinal_smooth.predict(merged, schema, cols=cols,
                                  kappas=kappas, w=w, bandwidths=bw)
    e010 = cond_agree.predict(merged, schema, cols=cols, kappas=kappas,
                              w=w)
    assert len(ours) == len(e010)
    diffs = [np.abs(a - b).max() for a, b in zip(ours, e010)]
    # off-by-default: engaged items (if any, on pure noise) must be few
    # and mild — mean deviation tiny
    assert float(np.mean(diffs)) < 5e-3


def ordinal_inject(frame, schema, driver_cols, seed):
    """Regenerate numeric-option PREDICT cells from a discretized
    Gaussian over ranks — plants the ordinal structure the sandbox lacks
    by construction.

    v2: the cell mean is a NON-ADDITIVE function of TWO GIVEN columns
    ((3*i1 + i2) mod 7), so no shallow ladder level and no logistic main
    effect can capture it — only deep (thin) cells see the signal, which
    is exactly the regime the kernel exists for. v1 (single-column
    additive mean) was fully captured by the existing conditioning and
    measured the kernel's headroom as ~0 (see E011 attempt log)."""
    rng = np.random.default_rng(seed)
    out = frame.copy()
    records = schema["items"]
    c1, c2 = driver_cols
    i1 = out[c1].map({v: i for i, v in
                      enumerate(records[c1]["values"])}).fillna(0)
    i2 = out[c2].map({v: i for i, v in
                      enumerate(records[c2]["values"])}).fillna(0)
    cell_code = ((3 * i1 + i2) % 7).to_numpy(dtype=float) / 6.0
    for item, r in records.items():
        if r["class"] != "PREDICT" or item not in out.columns:
            continue
        ranks = ordinal_smooth._numeric_ranks(list(r["values"]))
        if ranks is None:
            continue
        by_rank = sorted(ranks, key=ranks.get)
        m = len(by_rank)
        mu = cell_code * (m - 1)
        draw = np.clip(np.round(rng.normal(mu, 1.5)), 0, m - 1).astype(int)
        vals = [r["values"][by_rank[j]] for j in draw]
        editable = out[item].notna() & (out[item] != schema["gated_value"])
        out.loc[editable, item] = np.asarray(vals, dtype=object)[
            editable.to_numpy()]
    return out


@pytest.mark.xfail(
    reason="E011 rejected: sim v1/v2 measured the option-axis pooling "
           "headroom at ~0 (see E011 attempt log) — kept as the record "
           "of the null result; revive with the experiment",
    strict=True)
def test_ordinal_sim_gain_wb():
    frame, schema = load("world_bank")
    records = schema["items"]
    drivers = [n for n, r in records.items()
               if r["class"] == "GIVEN" and len(r["values"]) <= 12][:2]
    injected = ordinal_inject(frame, schema, drivers, seed=2)

    config = load_config(str(KIT / "config.yml"))
    merged, cells, truth = sample_rows(schema, injected, 1)
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)
    w, bw = ordinal_smooth.tune_weight_and_bandwidth(merged, schema,
                                                     cols, kappas)
    assert bw, "no bandwidth engaged despite planted ordinal structure"

    def scored(model, **kw):
        vectors = model.predict(merged, schema, cols=cols, kappas=kappas,
                                **kw)
        vectors = floored(vectors, schema, cells,
                          config["scoring"]["floor"])
        return grade(schema, config, vectors, truth, cells)["log_score"]

    e010 = scored(cond_agree, w=w)
    e011 = scored(ordinal_smooth, w=w, bandwidths=bw)
    print(f"\nordinal sim wb (drivers={drivers}, {len(bw)} items "
          f"engaged): E010 {e010:.4f} E011 {e011:.4f} "
          f"delta {e011 - e010:+.4f}")
    assert e011 > e010 + 0.005, (e010, e011)
