"""Small in-process synthetic fixture for unit tests.

The official sandbox now exists (`external/starter-kit/make_sandbox.py`)
and is the source of truth for integration testing; this module stays
only because it is fast and dependency-free for the test suite. It mimics
the item types, including a skip-logic gated item where "not shown" is
its own response level.

A single latent factor induces cross-item correlation so that
structure-aware models (IRT, low-rank) can beat the marginal baseline.
"""

import numpy as np
import pandas as pd

DEMO_COLS = ["age_group", "gender"]


def generate(n=1000, seed=0):
    """Returns (df, n_levels, demo_cols).

    df: full (unmasked) response matrix of integer level codes.
    n_levels: dict item -> K (gated item's K includes the "not shown" level).
    """
    rng = np.random.default_rng(seed)
    z = rng.normal(size=n)  # latent trait

    age_group = rng.integers(0, 4, size=n)
    gender = rng.integers(0, 2, size=n)

    # Binary item driven by latent trait.
    q_bin = (rng.random(n) < 1 / (1 + np.exp(-1.5 * z))).astype(int)

    # 5-level ordered Likert via thresholds on noisy latent.
    likert_latent = z + rng.normal(scale=0.8, size=n)
    q_likert = np.digitize(likert_latent, [-1.5, -0.5, 0.5, 1.5])

    # 4-level nominal, weakly trait-dependent.
    logits = np.stack([0.3 * z, np.zeros(n), -0.3 * z, 0.1 * z], axis=1)
    probs = np.exp(logits) / np.exp(logits).sum(axis=1, keepdims=True)
    q_nom = np.array([rng.choice(4, p=p) for p in probs])

    # Skip-logic pair: child only shown when gate == 1.
    q_gate = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)
    child_shown = np.digitize(z + rng.normal(scale=1.0, size=n), [-0.5, 0.5])
    NOT_SHOWN = 3  # gated-out cells get their own level
    q_child = np.where(q_gate == 1, child_shown, NOT_SHOWN)

    df = pd.DataFrame(
        {
            "age_group": age_group,
            "gender": gender,
            "q_bin": q_bin,
            "q_likert": q_likert,
            "q_nom": q_nom,
            "q_gate": q_gate,
            "q_child": q_child,
        }
    )
    n_levels = {
        "age_group": 4,
        "gender": 2,
        "q_bin": 2,
        "q_likert": 5,
        "q_nom": 4,
        "q_gate": 2,
        "q_child": 4,
    }
    return df, n_levels, DEMO_COLS
