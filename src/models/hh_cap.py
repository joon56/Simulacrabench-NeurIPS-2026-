"""E025 — E022 (household weights o sharpened lambda) with the trunk
architecture selected per instrument from {64x2, 128x2+dropout} on the
internal holdout (E017's grid, whose leaderboard reading was unhcr
+0.01 — the same size E022's sim-predicted gain turned out to be).
The data picks the config; everything else is E022.
"""

from src.models import link_sharp
from src.models.hh_sharp import hh_sharp_layer

CONFIGS = (
    (64, 2, 0.0),    # E012 baseline
    (128, 2, 0.1),   # the full grid's winner on wb and unhcr (E017)
)


def predict(frame, schema, cols=None, kappas=None):
    return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                              layer_fn=hh_sharp_layer, configs=CONFIGS)
