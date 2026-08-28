"""Internal holdout of visible rows, for tuning inside predict().

The only rows a submission can score itself on are the complete visible
rows (TRAIN). holdout_visible splits them: a fit part and a held-out part
whose PREDICT cells the caller treats as blank, mimicking the grader's
role structure without touching schema roles (which predict() cannot see).
"""

import numpy as np
import pandas as pd


def holdout_visible(frame, schema, frac=0.2, seed=0):
    """Split the complete visible rows of `frame`.

    Returns (fit_rows, eval_rows): both DataFrames of complete rows;
    eval_rows' PREDICT columns are the tuning targets (caller masks them).
    Rows with any NaN in GIVEN/PREDICT columns (the held-out respondents)
    are always kept in neither part — they carry no tuning signal.
    """
    items = [name for name, r in schema["items"].items()
             if r["class"] in ("GIVEN", "PREDICT")]
    complete = frame[frame[items].notna().all(axis=1)]
    rng = np.random.default_rng(seed)
    mask = rng.random(len(complete)) < frac
    return complete[~mask], complete[mask]
