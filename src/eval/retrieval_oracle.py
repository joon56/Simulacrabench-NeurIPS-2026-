"""Constrained section-shared donor oracle; never part of a submission."""

import numpy as np


def candidate_indices(codes, weights, query, bank, k=32, chunk=128):
    """Return frame positions of GIVEN-only nearest donors, excluding queries."""
    query, bank = np.asarray(query, dtype=int), np.sort(np.asarray(bank, dtype=int))
    overlap = np.isin(query, bank).any()
    width = max(0, min(k, len(bank) - int(overlap)))
    result = np.empty((len(query), width), dtype=int)
    if width == 0:
        return result
    bank_codes = codes[bank]
    for start in range(0, len(query), chunk):
        rows = query[start:start + chunk]
        scores = np.zeros((len(rows), len(bank)), dtype=np.float64)
        for j, weight in enumerate(weights):
            scores += weight * (codes[rows, j, None] == bank_codes[None, :, j])
        scores[rows[:, None] == bank[None, :]] = -np.inf
        idx = np.argpartition(scores, -width, axis=1)[:, -width:]
        for row in range(len(rows)):
            order = np.lexsort((bank[idx[row]], -scores[row, idx[row]]))
            result[start + row] = bank[idx[row, order]]
    return result


def mixture_oracle(truth_prob, iterations=300, tolerance=1e-7):
    """Lower/upper log-score bounds for a section-shared convex mixture.

    Input [queries, section items, candidates], already officially floored.
    Candidate 0 is the baseline. EM gives a feasible lower bound; the
    concave objective's simplex first-order gap certifies an upper bound.
    The best single candidate is retained if EM has not converged to it.
    Query-specific weights are an oracle privilege, never inference inputs.
    """
    a = np.asarray(truth_prob, dtype=np.float64)
    if a.ndim != 3 or a.shape[1] == 0 or a.shape[2] == 0:
        raise ValueError("Expected nonempty [queries, items, candidates]")
    if not np.isfinite(a).all() or np.any(a <= 0) or np.any(a > 1):
        raise ValueError("Truth probabilities must be finite in (0, 1]")
    weights = np.full((a.shape[0], a.shape[2]), 1.0 / a.shape[2])
    for _ in range(iterations):
        p = np.einsum("qik,qk->qi", a, weights)
        gradient = (a / p[:, :, None]).mean(axis=1)
        if np.max(gradient.max(axis=1) - 1.0) < tolerance:
            break
        weights *= gradient
        weights /= weights.sum(axis=1, keepdims=True)
    p = np.einsum("qik,qk->qi", a, weights)
    score = np.log(p).mean(axis=1)
    gradient = (a / p[:, :, None]).mean(axis=1)
    upper = np.minimum(0.0, score + np.maximum(0, gradient.max(axis=1) - 1))
    lower = np.maximum(score, np.log(a).mean(axis=1).max(axis=1))
    return lower, np.maximum(lower, upper)
