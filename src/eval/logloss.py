"""Local reproduction of the official metric.

Verified against the official grader (external/starter-kit/score.py,
2026-08-11): the log score is pooled over all blank cells (not per-item
averaged), vectors are floored by mixing with a flat vector
(scoring.floor = 1e-3), and the leaderboard metric is
skill = 1 + log_score / U with U the schema-only mean of log K over
scored items (K includes the gate sentinel).

Data conventions used across this repo:
- Response matrix: pandas DataFrame, one row per respondent, one column
  per item. Values are integer level codes 0..K-1. Skip-logic "not shown"
  is a regular level (part of K), per the competition spec.
- Masked/unobserved cells are NaN.
- Predictions: dict mapping item name -> ndarray of shape (n_respondents,
  n_levels) with rows summing to 1.
"""

import numpy as np

EPS = 1e-15


def mean_log_loss(y_true, proba, eps=EPS):
    """Mean negative log-likelihood of integer labels under predicted distributions.

    y_true: (n,) integer level codes.
    proba: (n, k) predicted probabilities.
    Probabilities are clipped to [eps, 1] to avoid -inf; the official
    harness may differ (verify), but any submission emitting exact zeros
    on a realized level deserves the penalty anyway.
    """
    y_true = np.asarray(y_true, dtype=int)
    proba = np.asarray(proba, dtype=float)
    if proba.ndim != 2 or len(y_true) != len(proba):
        raise ValueError("proba must be (n, k) aligned with y_true")
    p = np.clip(proba[np.arange(len(y_true)), y_true], eps, 1.0)
    return float(-np.mean(np.log(p)))


def evaluate(truth, mask, proba):
    """Mean log-loss over all masked cells, pooled across items.

    truth: DataFrame of true level codes (no NaN in masked positions).
    mask: boolean DataFrame, same shape/index/columns; True = cell is
      held out and must be scored.
    proba: dict item -> (n, k) ndarray of predicted probabilities.

    Returns (overall_mean, per_item) where per_item is a dict
    item -> (mean_log_loss, n_cells) for diagnostics.
    """
    total = 0.0
    count = 0
    per_item = {}
    for item in truth.columns:
        m = mask[item].to_numpy()
        if not m.any():
            continue
        if item not in proba:
            raise KeyError(f"missing predictions for item {item!r}")
        y = truth[item].to_numpy()[m].astype(int)
        p = np.asarray(proba[item], dtype=float)[m]
        losses = -np.log(np.clip(p[np.arange(len(y)), y], EPS, 1.0))
        per_item[item] = (float(losses.mean()), int(len(y)))
        total += float(losses.sum())
        count += len(y)
    if count == 0:
        raise ValueError("mask selects no cells")
    return total / count, per_item


def floor_mix(proba, floor=1e-3):
    """Official flooring: renormalize, then mix with a flat vector so every
    entry is at least `floor` and the vector still sums to 1 (score.py's
    `floored`). Clip-then-renormalize would not keep both properties."""
    proba = np.asarray(proba, dtype=float)
    p = proba / proba.sum(axis=-1, keepdims=True)
    k = p.shape[-1]
    return floor + (1.0 - k * floor) * p


def uniform_reference(n_levels, scored_items):
    """U: mean surprisal of a uniform guess over scored items, in nats.
    Schema-only; n_levels counts must include the gate sentinel level."""
    return float(np.mean([np.log(n_levels[item]) for item in scored_items]))


def skill(mean_loss, u):
    """Leaderboard metric: 1 + log_score / U, where log_score = -mean_loss.
    0 = uniform guess, 1 = perfect, negative = worse than guessing."""
    return 1.0 - mean_loss / u
