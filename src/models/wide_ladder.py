"""E016 — E012 with the ladder's cardinality cap lifted to 64.

Admits high-cardinality GIVEN columns (unhcr: governorate_col K=46,
origin governorate K=16) into the greedy ladder selection. Selection
stays data-driven; per-level kappa absorbs cell fragmentation. The cap
is patched only for the duration of the call.
"""

from src.models import hier_backoff, shared_trunk

WIDE_MAX_CARD = 64


def predict(frame, schema, cols=None, kappas=None):
    old = hier_backoff.MAX_CARD
    hier_backoff.MAX_CARD = WIDE_MAX_CARD
    try:
        return shared_trunk.predict(frame, schema, cols=cols,
                                    kappas=kappas)
    finally:
        hier_backoff.MAX_CARD = old
