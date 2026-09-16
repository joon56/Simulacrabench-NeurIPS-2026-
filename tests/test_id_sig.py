"""E038 tests. (a) Sequential ids + random order (the plain household sim):
every derived id column gets ~0 weight and E038 stays within noise of
E025. (b) Ids that share a household key between a row and its twin
(src 'R000123' -> twin 'R000123-2'): the key column arms and E038 beats
E025 clearly (near-perfect twin recall)."""

import numpy as np
import pytest

from src.models import hh_cap, hier_backoff, id_sig
from tests.test_soft_gating import KIT, load
from tests.test_hh_sharp import hh_inject_rho
from tests.test_prob_link import _marginal_model_dists

from make_sandbox import load_config  # noqa: E402 (KIT on sys.path)
from score import floored, sample_rows, score as grade  # noqa: E402


def keyed_ids(sim, weak_given=False, seed=0):
    """Give each twin the id of its source row plus a member suffix.
    weak_given: also resample the twins' roster and governorate columns
    so the GIVEN signature no longer finds them (a recall problem that
    only the identifier can solve)."""
    out = sim.copy()
    ids = out["respondent_id"].astype(str).to_numpy(dtype=object)
    n_base = int((~out["respondent_id"].astype(str).str.startswith("hh_")).sum())
    # hh_inject_rho appends the twins in the order of `take`; recover the
    # source by replaying the same sample
    base = out.iloc[:n_base]
    take = base[base["wave"] == "1"].sample(frac=0.3, random_state=13)
    src = take["respondent_id"].astype(str).to_numpy()
    for k, i in enumerate(range(n_base, len(out))):
        ids[i] = src[k] + "-2"
    out["respondent_id"] = ids
    if weak_given:
        # scramble HALF the twins' household columns: the other half stay
        # discoverable by GIVEN, so the key can be learned from them and
        # then recover the scrambled half (the real-data situation)
        rng = np.random.default_rng(seed)
        given = [c for c in out.columns
                 if c.startswith(("s2_3_", "governorate_col", "s2_4a_"))]
        n_tw = len(out) - n_base
        scr = out.index[n_base:][rng.random(n_tw) < 0.5]
        for col in given:
            vals = list(out[col].dropna().unique())
            out.loc[scr, col] = [vals[rng.integers(len(vals))]
                                 for _ in range(len(scr))]
    return out


def _scorer(sim, schema):
    merged, cells, truth = sample_rows(schema, sim, 1)
    config = load_config(str(KIT / "config.yml"))
    cols, kappas, _ = hier_backoff.select_ladder(merged, schema)

    def scored(model):
        v = model.predict(merged, schema, cols=cols, kappas=kappas)
        v = floored(v, schema, cells, config["scoring"]["floor"])
        return grade(schema, config, v, truth, cells)["log_score"]
    return merged, scored


def test_id_columns_derive_from_sandbox_ids():
    frame, schema = load("unhcr")
    cols = id_sig.id_columns(frame)
    assert cols.shape[0] == len(frame)
    assert any(c.startswith("id_block_") for c in cols.columns)
    assert "id_tok_1" in cols.columns          # the digit run


def test_sequential_ids_get_no_weight_and_parity():
    frame, schema = load("unhcr")
    sim = hh_inject_rho(frame, schema, 0.3, 13, 0.2, 0.8)
    merged, scored = _scorer(sim, schema)
    _, _, (w, n_given) = id_sig.id_sharp_layer(
        merged, schema, _marginal_model_dists(merged, schema),
        return_weights=True)
    id_w = w[n_given:]
    print(f"\nsequential ids: derived-column weights max {id_w.max():.3f} "
          f"(GIVEN max {w[:n_given].max():.2f})")
    assert id_w.max() < 0.25 * w[:n_given].max()
    e025, e038 = scored(hh_cap), scored(id_sig)
    print(f"household sim: E025 {e025:.4f} E038 {e038 - e025:+.4f}")
    assert abs(e038 - e025) < 0.002


def test_household_key_in_ids_arms_and_wins():
    """Twins whose GIVEN signature is scrambled (roster + governorate
    resampled) but whose id shares the source's key: E025 cannot find
    them, E038 can."""
    frame, schema = load("unhcr")
    sim = keyed_ids(hh_inject_rho(frame, schema, 0.3, 13, 0.2, 0.8),
                    weak_given=True)
    merged, scored = _scorer(sim, schema)
    _, _, (w, n_given) = id_sig.id_sharp_layer(
        merged, schema, _marginal_model_dists(merged, schema),
        return_weights=True)
    id_w = w[n_given:]
    print(f"\nkeyed ids: derived-column weights max {id_w.max():.2f} "
          f"(GIVEN max {w[:n_given].max():.2f})")
    assert id_w.max() > w[:n_given].max()
    e025, e038 = scored(hh_cap), scored(id_sig)
    print(f"keyed household sim: E025 {e025:.4f} E038 {e038 - e025:+.4f}")
    assert e038 > e025 + 0.01
