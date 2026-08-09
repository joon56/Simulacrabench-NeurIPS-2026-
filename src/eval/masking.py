"""Masking utilities for local validation, mirroring the two tracks.

Track A: MCAR masking of individual cells within each respondent.
Track B: hold out whole respondents; only demographic items stay visible.
"""

import numpy as np
import pandas as pd


def mcar_mask(df, frac, rng):
    """Track A style: mask a random `frac` of observed cells, MCAR.

    Returns a boolean DataFrame (True = masked / to be predicted).
    """
    observed = df.notna().to_numpy()
    coins = rng.random(df.shape) < frac
    return pd.DataFrame(observed & coins, index=df.index, columns=df.columns)


def holdout_respondents(df, demo_cols, frac, rng):
    """Track B style: pick `frac` of respondents, mask all their
    non-demographic observed cells.

    Returns (mask, holdout_index). mask is a boolean DataFrame
    (True = masked / to be predicted).
    """
    n = len(df)
    holdout = rng.random(n) < frac
    mask = pd.DataFrame(False, index=df.index, columns=df.columns)
    non_demo = [c for c in df.columns if c not in demo_cols]
    mask.loc[holdout, non_demo] = df.loc[holdout, non_demo].notna()
    return mask, df.index[holdout]


def apply_mask(df, mask):
    """Return a copy of df with masked cells set to NaN (the model's view)."""
    out = df.astype("float64").copy()
    out[mask] = np.nan
    return out
