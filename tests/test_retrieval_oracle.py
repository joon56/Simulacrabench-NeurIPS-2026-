"""Analytic checks for the constrained donor-mixture oracle."""

import numpy as np

from src.eval.retrieval_oracle import mixture_oracle, candidate_indices


def test_section_mixture_cannot_pick_a_different_donor_per_cell():
    # Opposite answers: a single shared mixture reaches .5 on both cells.
    a = np.array([[[.5, .999, .001], [.5, .001, .999]]])
    score, upper = mixture_oracle(a)
    assert abs(score[0] - np.log(.5)) < 1e-9
    assert upper[0] >= score[0] - 1e-12
    assert upper[0] - score[0] < 1e-8


def test_oracle_includes_the_baseline_and_bounds_a_known_optimum():
    a = np.array([[[.2, .8, .3], [.3, .7, .4]]])
    score, upper = mixture_oracle(a, iterations=400)
    optimum = np.log([.8, .7]).mean()
    assert score[0] >= np.log([.2, .3]).mean()
    assert score[0] <= optimum + 1e-10
    assert upper[0] >= optimum - 1e-10
    assert optimum - score[0] < 1e-5


def test_donor_self_exclusion_and_small_bank():
    codes = np.array([[0, 0], [0, 0], [1, 1]])
    bank = np.array([0, 1, 2])
    idx = candidate_indices(codes, np.ones(2), bank, bank, k=9)
    assert idx.shape == (3, 2)
    assert all(q not in row for q, row in zip(bank, idx))
    assert candidate_indices(codes, np.ones(2), [0], [0], k=3).shape == (1, 0)


def test_tied_candidate_membership_is_bank_order_invariant():
    codes = np.zeros((30, 3), dtype=int)
    bank = np.arange(29)
    first = candidate_indices(codes, np.ones(3), [29], bank, k=7)
    second = candidate_indices(codes, np.ones(3), [29], bank[::-1], k=7)
    np.testing.assert_array_equal(first, second)
