"""E052 fixed exploratory endpoint; E041 remains the incumbent."""

from copy import deepcopy

from src.eval.evidence_routing import routing_library
from src.eval.recursive_candidates import _partition
from src.models import supervised_retrieval

LAST_DIAGNOSTICS = {}


def predict(frame, schema, cols=None, kappas=None):
    """Apply original own-item evidence after base-only UNHCR gate routing."""
    LAST_DIAGNOSTICS.clear()
    reason = None
    if "s3_11_intent_return_12m_lbl" not in schema["items"]:
        reason = "non_unhcr"
    elif cols is not None or kappas is not None:
        reason = "custom_base_options"
    else:
        try:
            _partition(frame, schema)
        except (ValueError, KeyError) as error:
            reason = str(error)
    if reason is not None:
        LAST_DIAGNOSTICS.update(mode="e041", fallback_reason=reason)
        return supervised_retrieval.predict(frame, schema, cols=cols, kappas=kappas)
    frozen = routing_library(frame, schema)
    LAST_DIAGNOSTICS.update(deepcopy(frozen["diagnostics"]))
    LAST_DIAGNOSTICS["mode"] = "after_gates"
    return frozen["arms_raw"]["after_gates"]
