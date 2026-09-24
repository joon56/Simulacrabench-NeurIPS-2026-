"""E052 fixed control: original own-item evidence after base-only gate routing."""

from copy import deepcopy

import numpy as np

from src.eval.recursive_candidates import (
    _mapped, _partition, cached_renderer, predict_components,
)
from src.models import hh_cap, supervised_retrieval


def routing_library(frame, schema):
    """Freeze one E041 fit and return E041/E052 raw and mapped endpoints.

    ``base_raw`` means the incumbent E041, not the evidence-free recursion.
    ``base_routed_raw`` is the latter. Original ``evidence_rows`` and ``lambdas``
    are returned unchanged. Partial query blocks are rejected before fitting.
    """
    predicted, options, visible, query = _partition(frame, schema)
    render, captured = cached_renderer(), []

    def layer(f, s, model_dists):
        if not captured:
            captured.append(supervised_retrieval.supervised_layer(f, s, model_dists))
        return captured[0]

    original = render(frame, schema, layer_fn=layer, configs=hh_cap.CONFIGS)
    evidence, lambdas = captured[0]
    base_routed = render(frame, schema, layer_fn=lambda *a: ({}, {}),
                         configs=hh_cap.CONFIGS)
    original_map = _mapped(original, predicted, query)
    routed_map = _mapped(base_routed, predicted, query)
    endpoint, changed_by_item = [], {n: 0 for n in predicted}
    records = schema["items"]
    for row_i, row in enumerate(query):
        entry = evidence.get(row)
        ev, concentration = entry if entry is not None else ({}, False)
        for item_i, item in enumerate(predicted):
            index = row_i * len(predicted) + item_i
            original_vector = original[index]
            gate = records[item].get("gate")
            pair, own_evidence = lambdas.get(item), ev.get(item)
            share = (pair[int(concentration)] if pair is not None
                     and own_evidence is not None and own_evidence.sum() > 0 else 0.)
            # Exact structural boundaries avoid even floating-point-only edits.
            unchanged = gate is None or gate["parent"] not in original_map or share == 1
            if not unchanged:
                parent = gate["parent"]
                asked = [options[parent].index(v) for v in gate["observed_if"]]
                unchanged = (original_map[parent][row_i, asked].sum()
                             == routed_map[parent][row_i, asked].sum())
            candidate = original_vector
            if not unchanged:
                candidate = base_routed[index]
                if share > 0:
                    candidate = (1. - share) * candidate + share * own_evidence
                if np.array_equal(candidate, original_vector):
                    candidate = original_vector
            changed_by_item[item] += int(candidate is not original_vector)
            endpoint.append(candidate)
    arms_raw = {"identity": original, "after_gates": endpoint}
    arms = {n: _mapped(raw, predicted, query) for n, raw in arms_raw.items()}
    return {"base_raw": original, "base": original_map, "base_routed_raw": base_routed,
            "arms_raw": arms_raw, "arms": arms, "evidence_rows": evidence,
            "lambdas": lambdas, "query": query, "predicted": predicted,
            "options": options, "components": predict_components(schema),
            "diagnostics": {"fit_rows": len(visible), "query_rows": len(query),
                            "evidence_rows": len(evidence), "legacy_lambdas": deepcopy(lambdas),
                            "changed_vectors": sum(changed_by_item.values()),
                            "changed_by_item": changed_by_item,
                            "supervised_layer": deepcopy(supervised_retrieval.LAST_DIAGNOSTICS)}}
