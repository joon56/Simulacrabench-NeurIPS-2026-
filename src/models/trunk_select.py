"""E015 — trunk capacity selection for the shared multi-head net.

Same model as E012/shared_trunk; the architecture is chosen per
instrument from a small grid by pooled CE on the outer holdout split
(net alone), then the blend weight is tuned and the winner retrains on
all complete rows. Dropout guards the wider settings.
"""

from src.models import shared_trunk

CONFIGS = (
    (64, 2, 0.0),    # E012 baseline
    (128, 2, 0.1),
    (256, 2, 0.1),
    (128, 3, 0.1),
)


def predict(frame, schema, cols=None, kappas=None):
    return shared_trunk.predict(frame, schema, cols=cols, kappas=kappas,
                                configs=CONFIGS)
