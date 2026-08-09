"""Per-item marginal baseline (the trivial starter-kit baseline).

Predicts, for every respondent, the Laplace-smoothed empirical level
frequencies of each item computed on visible (unmasked) cells.
"""

import numpy as np


class MarginalBaseline:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.probs_ = {}

    def fit(self, train_df, n_levels):
        """train_df: DataFrame with NaN for masked cells.
        n_levels: dict item -> number of levels K."""
        for item, k in n_levels.items():
            values = train_df[item].dropna().to_numpy().astype(int)
            counts = np.bincount(values, minlength=k).astype(float)
            counts += self.alpha
            self.probs_[item] = counts / counts.sum()
        return self

    def predict_proba(self, n_rows):
        """Returns dict item -> (n_rows, k) array, identical rows."""
        return {
            item: np.tile(p, (n_rows, 1)) for item, p in self.probs_.items()
        }
