"""E044: ablate learned metric use, conditional on unchanged E041 activation.

Copy the parent layer's function binding, not its implementation or globals.
Only evidence construction changes; no shared parent namespace is mutated.
Learned metrics still determine active sections. Lambda is recalibrated using
the same procedure, so this is not an ablation at fixed mixture shares.
"""

from types import FunctionType
from src.models import supervised_retrieval as parent


def fixed_metric_evidence(evidence, frame, records, items, options, codes,
                          query, bank, initial, predicted, groups, learned, active):
    """Keep original candidate identities and active mask; use initial weights."""
    return parent._replace_evidence(
        evidence, frame, records, items, options, codes, query, bank, initial,
        predicted, groups, [initial] * len(groups), active)


control_layer = FunctionType(
    parent.supervised_layer.__code__,
    dict(parent.supervised_layer.__globals__, _replace_evidence=fixed_metric_evidence),
    name="control_layer", argdefs=parent.supervised_layer.__defaults__,
    closure=parent.supervised_layer.__closure__)


def predict(frame, schema, cols=None, kappas=None):
    if "s3_11_intent_return_12m_lbl" not in schema["items"]:
        return parent.predict(frame, schema, cols=cols, kappas=kappas)
    return parent.link_sharp.predict(frame, schema, cols=cols, kappas=kappas,
                                    layer_fn=control_layer, configs=parent.hh_cap.CONFIGS)
