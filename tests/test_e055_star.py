"""Finite coupled-star and adapter safeguards; synthetic data only."""

from itertools import product

import numpy as np
import pandas as pd

from scripts.screen_e055 import finite_star_oracle, make_adapter, mask_outer
from src.eval.logloss import floor_mix


def tiny_star(parent_pair, child_pair, bucket):
    root = np.array([[.7, .3], [.3, .7]])
    parent_ev = np.array([[.1, .9], [.8, .2]])
    p = (1 - np.array(parent_pair)[bucket, None]) * root + np.array(parent_pair)[bucket, None] * parent_ev
    hard = np.column_stack((.8 * p[:, 1], .2 * p[:, 1], p[:, 0]))
    soft = np.array([[.2, .3, .5], [.2, .3, .5]])
    base = .7 * hard + .3 * soft
    child_ev = np.array([[.8, .1, .12], [.1, .8, .11]])  # deliberately nonunit
    c = (1 - np.array(child_pair)[bucket, None]) * base + np.array(child_pair)[bucket, None] * child_ev
    return {"HOSPITALIZED": p, "EHREAS_DT": c}


def test_finite_oracle_equals_bruteforce_with_soft_gate_and_nonunit_floor():
    bucket = np.array([0, 1])
    labels = {"HOSPITALIZED": np.array([1, 0]), "EHREAS_DT": np.array([0, 2])}
    parent_ev = np.array([[.1, .9], [.8, .2]])
    child_ev = np.array([[.8, .1, .12], [.1, .8, .11]])
    evidence = {"HOSPITALIZED": parent_ev, "EHREAS_DT": child_ev}
    available = {name: np.ones(2, bool) for name in evidence}
    original = {name: (0., 0.) for name in evidence}
    grid = (0., .5)
    render = lambda pairs: tiny_star(pairs["HOSPITALIZED"], pairs["EHREAS_DT"], bucket)
    roots = {pair: render({"HOSPITALIZED": pair, "EHREAS_DT": (0., 0.)})
             for pair in product(grid, repeat=2)}
    result = finite_star_oracle(roots, render(original), evidence, available, bucket, labels, original, grid)
    brute = max(sum(np.log(floor_mix(v)[np.arange(2), labels[n]]).sum()
                    for n, v in render({"HOSPITALIZED": p, "EHREAS_DT": c}).items())
                for p in product(grid, repeat=2) for c in product(grid, repeat=2))
    assert np.isclose(result["best_log_sum"], brute, atol=1e-12)
    assert result["best_log_sum"] >= result["identity_log_sum"] - 1e-12
    selected = render(result["shares"])
    assert all(np.allclose(selected[n], result["composed"][n], atol=1e-12) for n in labels)


def test_unavailable_child_follows_changed_parent():
    bucket = np.array([0, 1])
    labels = {"HOSPITALIZED": np.array([1, 0]), "EHREAS_DT": np.array([0, 2])}
    evidence = {"HOSPITALIZED": np.array([[.1, .9], [.8, .2]]),
                "EHREAS_DT": np.array([[.8, .1, .12], [.1, .8, .11]])}
    available = {"HOSPITALIZED": np.ones(2, bool), "EHREAS_DT": np.zeros(2, bool)}
    render = lambda pairs: tiny_star(pairs["HOSPITALIZED"], (0., 0.), bucket)
    grid = (0., .5)
    roots = {pair: render({"HOSPITALIZED": pair, "EHREAS_DT": (0., 0.)})
             for pair in product(grid, repeat=2)}
    original = {n: (0., 0.) for n in evidence}
    result = finite_star_oracle(roots, render(original), evidence, available, bucket,
                                labels, original, grid)
    assert result["shares"]["EHREAS_DT"] == (0., 0.)
    assert all(np.allclose(render(result["shares"])[n], result["composed"][n]) for n in labels)


def test_adapter_excludes_keys_flags_and_masks_all_outer_targets():
    row = {"SSUID": "s", "PNUM": "1", "MONTHCODE": "12", "THHLDSTATUS": "1",
           "TAGE_EHC": "20", "TAGE": "20", "ESEX": "1", "ERACE": "2",
           "EORIGIN": "1", "EEDUC": "40", "EMS": "1", "THOSPNIT": "0",
           "AHOSPNIT": "1", "AHREASON": "0"}
    for reason in ("EHREAS_DT", "EHREAS_BIR", "EHREAS_OS", "EHREAS_NST", "EHREAS_OTH", "EHREAS_COR"):
        row[reason] = ""
    frame, schema = make_adapter(pd.DataFrame([row, {**row, "SSUID": "t", "PNUM": "2"}]))
    assert set(frame) == set(schema["items"])
    assert not ({"SSUID", "PNUM", "MONTHCODE", "AHREASON", "THOSPNIT"} & set(frame))
    masked = mask_outer(frame, schema, np.array([1]))
    predicted = [name for name, spec in schema["items"].items() if spec["class"] == "PREDICT"]
    assert masked.loc[1, predicted].isna().all()
    assert masked.loc[0, predicted].notna().all()


def test_exact_tie_preserves_explicit_identity():
    grid = (0., .5)
    identity = {"HOSPITALIZED": np.array([[.5, .5]]),
                "EHREAS_DT": np.array([[.3, .3, .4]])}
    roots = {pair: identity for pair in product(grid, repeat=2)}
    evidence = {name: value.copy() for name, value in identity.items()}
    available = {name: np.ones(1, bool) for name in identity}
    original = {name: (.5, .5) for name in identity}
    labels = {name: np.array([0]) for name in identity}
    result = finite_star_oracle(roots, identity, evidence, available, np.array([0]),
                                labels, original, grid)
    assert result["shares"] == original
    assert result["delta_skill_over_3"] == 0
