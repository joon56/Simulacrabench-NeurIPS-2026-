"""Masking utilities for local validation.

The official task (per the starter kit README — the earlier Track A/B
framing is obsolete) holds out whole respondents: their GIVEN block stays
visible and every PREDICT cell is blanked. `holdout_respondents` mirrors
that. `mcar_mask` is kept as an extra, cheaper validation signal for
within-respondent structure; it does not correspond to the official split.
"""

import numpy as np
import pandas as pd


def mcar_mask(df, frac, rng):
    """Mask a random `frac` of observed cells, MCAR (auxiliary validation
    only — not the official test structure).

    Returns a boolean DataFrame (True = masked / to be predicted).
    """
    observed = df.notna().to_numpy()
    coins = rng.random(df.shape) < frac
    return pd.DataFrame(observed & coins, index=df.index, columns=df.columns)


def holdout_respondents(df, demo_cols, frac, rng):
    """Official test structure: pick `frac` of respondents, mask all their
    observed cells outside the always-visible block (`demo_cols` = the
    GIVEN items).

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
