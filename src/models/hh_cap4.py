"""E026 — E022's household evidence layer with the trunk selected per
instrument from E017's full grid (4 configs). Training runs on the
hosted H100 (confirmed by E025); the data picks the config.
"""

from src.models import link_sharp
from src.models.hh_sharp import hh_sharp_layer

CONFIGS = (
    (64, 2, 0.0),    # E012 baseline
    (128, 2, 0.1),   # E025's selection on wb/unhcr
    (256, 2, 0.1),
    (128, 3, 0.1),
)


def predict(frame, schema, cols=None, kappas=None):
    return link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                              layer_fn=hh_sharp_layer, configs=CONFIGS)
