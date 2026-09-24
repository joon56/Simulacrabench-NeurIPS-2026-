"""Frozen E050 recursive evidence and E051 direct-tree diagnostic libraries.

No selection policy is fitted here. ``e050_library(frame, schema)`` accepts
visible fit rows and completely masked query PREDICT blocks. It returns:
``base_raw`` (unchanged canonical E041 vectors), ``base`` (item -> query x K),
``arms_raw`` and ``arms`` (arm name -> either representation), ``query``
(positional frame indices), ``predicted`` (schema order), ``options``,
``components`` (lists of PREDICT names), and label-free ``diagnostics``.
``e051_library(frame, schema, frozen_e050)`` adds three complete-output tree
mixtures using exactly those fit/query rows, with the same return convention.

Each connected PREDICT gate component can choose one global arm exactly:
the renderer reads earlier beliefs only through gate parents, and all GIVEN
parents are fixed observed boundaries. Fitted products, donor evidence and
agreement tables are held fixed. No edge crosses two returned components.
"""

from copy import deepcopy
from types import FunctionType

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from threadpoolctl import threadpool_limits

from src.eval.logloss import floor_mix
from src.models import hh_cap, link_sharp, supervised_retrieval
from src.models.hier_backoff import _layout

E050_ARMS = ("identity", "zero", "half", "toward_one", "one")
E051_SHARES = (0., .25, .5)
TREE_PARAMETERS = dict(max_iter=40, max_leaf_nodes=15, learning_rate=.1,
                       l2_regularization=1., early_stopping=False,
                       random_state=0, max_bins=255)


def predict_components(schema):
    """Undirected PREDICT gate components in stable public schema order."""
    records = schema["items"]
    names = [n for n, r in records.items() if r["class"] == "PREDICT"]
    neighbors = {n: set() for n in names}
    for name in names:
        gate = records[name].get("gate")
        if gate and gate["parent"] in neighbors:
            neighbors[name].add(gate["parent"])
            neighbors[gate["parent"]].add(name)
    result, seen = [], set()
    for name in names:
        if name in seen:
            continue
        component, todo = set(), [name]
        while todo:
            node = todo.pop()
            if node not in component:
                component.add(node)
                todo.extend(neighbors[node] - component)
        seen.update(component)
        result.append([n for n in names if n in component])
    return result


def mask_query(frame, schema, query):
    """Copy and hide the entire query answer block before any fitting."""
    masked = frame.reset_index(drop=True).copy()
    predicted = [n for n, r in schema["items"].items() if r["class"] == "PREDICT"]
    masked.loc[np.asarray(query, dtype=int), predicted] = np.nan
    return masked


def _partition(frame, schema):
    records, items, options = _layout(frame, schema)
    predicted = [n for n in items if records[n]["class"] == "PREDICT"]
    missing = frame[predicted].isna().to_numpy()
    query = np.flatnonzero(missing.any(axis=1))
    if not len(query) or not missing[query].all():
        raise ValueError("Require nonempty query rows with whole PREDICT blocks hidden")
    given = [n for n in items if records[n]["class"] == "GIVEN"]
    if frame[given].isna().any().any():
        raise ValueError("GIVEN boundaries must be observed")
    return predicted, options, np.flatnonzero(~missing.any(axis=1)), query


def cached_renderer():
    """A fresh private function namespace per frame; never mutate E041 code."""
    namespace = link_sharp.predict.__globals__.copy()

    def memo(function, keyed=False):
        cache = {}

        def once(*args, **kwargs):
            key = (args[1], tuple(args[2])) if keyed else None
            if key not in cache:
                cache[key] = function(*args, **kwargs)
            return cache[key]
        return once

    for name in ("select_ladder", "tune_and_train", "_proba_maps", "conditional_agreement"):
        namespace[name] = memo(namespace[name])
    namespace["build_ladder"] = memo(namespace["build_ladder"], keyed=True)
    return FunctionType(link_sharp.predict.__code__, namespace,
                        argdefs=link_sharp.predict.__defaults__)


def transform_lambdas(evidence_rows, lambdas, arm):
    """Change both buckets only for captured evidence; missing lambda is zero.

    ``arm`` is one registered name, or an item -> name mapping used to verify
    exact component composition. No dormant evidence extraction is performed.
    """
    captured_items = dict.fromkeys(n for evidence, _ in evidence_rows.values() for n in evidence)
    result = {}
    for item in captured_items:
        choice = arm[item] if isinstance(arm, dict) else arm
        pair = np.asarray(lambdas.get(item, (0., 0.)), dtype=float)
        if choice == "identity":
            changed = pair
        elif choice == "zero":
            changed = pair * 0
        elif choice == "half":
            changed = pair * .5
        elif choice == "toward_one":
            changed = pair + .5 * (1. - pair)
        elif choice == "one":
            changed = np.ones(2)
        else:
            raise ValueError(f"Unknown E050 arm: {choice}")
        result[item] = tuple(float(x) for x in changed)
    return result


def _mapped(raw, predicted, query):
    if len(raw) != len(predicted) * len(query):
        raise ValueError("Raw vectors do not match whole query blocks")
    return {n: np.stack(raw[i::len(predicted)]) for i, n in enumerate(predicted)}


def e050_library(frame, schema):
    """Fit actual E041 once, freeze its evidence, fully recurse five arms."""
    predicted, options, visible, query = _partition(frame, schema)
    render, captured = cached_renderer(), []

    def layer(f, s, model_dists):
        if not captured:
            captured.append(supervised_retrieval.supervised_layer(f, s, model_dists))
        return captured[0]

    # Explicit generic invocation is essential for Adult, which has no UNHCR
    # marker: supervised_retrieval.predict would silently choose E025 instead.
    base_raw = render(frame, schema, layer_fn=layer, configs=hh_cap.CONFIGS)
    evidence, lambdas = captured[0]
    arms_raw = {"identity": base_raw}
    for arm in E050_ARMS[1:]:
        changed = transform_lambdas(evidence, lambdas, arm)
        arms_raw[arm] = render(frame, schema, layer_fn=lambda *a: (evidence, changed),
                               configs=hh_cap.CONFIGS)
    arms = {arm: _mapped(raw, predicted, query) for arm, raw in arms_raw.items()}
    return {"base_raw": base_raw, "base": arms["identity"], "arms_raw": arms_raw,
            "arms": arms, "query": query, "predicted": predicted,
            "options": options, "components": predict_components(schema),
            "diagnostics": {"fit_rows": len(visible), "query_rows": len(query),
                            "evidence_rows": len(evidence), "legacy_lambdas": deepcopy(lambdas),
                            "supervised_layer": deepcopy(supervised_retrieval.LAST_DIAGNOSTICS)}}


def direct_tree(frame, schema):
    """Fixed GIVEN-only HistGBM, trained on fully visible rows, all classes."""
    predicted, options, visible, query = _partition(frame, schema)
    if not len(visible):
        raise ValueError("Direct trees require visible fit rows")
    given = [n for n, r in schema["items"].items() if r["class"] == "GIVEN"]
    features = np.column_stack([
        frame[n].map({v: i for i, v in enumerate(options[n])}).to_numpy(dtype=float)
        for n in given])
    categorical = [len(options[n]) <= 255 for n in given]
    result = {}
    with threadpool_limits(limits=2):
        for name in predicted:
            labels = frame.iloc[visible][name].map(
                {v: i for i, v in enumerate(options[name])}).to_numpy(dtype=int)
            k = len(options[name])
            marginal = np.bincount(labels, minlength=k) + 1.
            marginal /= marginal.sum()
            probability = np.zeros((len(query), k))
            classes = np.unique(labels)
            if len(classes) == 1:
                probability[:, classes[0]] = 1.
            else:
                model = HistGradientBoostingClassifier(**TREE_PARAMETERS,
                    categorical_features=categorical)
                model.fit(features[visible], labels)
                probability[:, np.asarray(model.classes_, dtype=int)] = model.predict_proba(features[query])
            result[name] = .99 * probability + .01 * marginal
    return result, {"fit_rows": len(visible), "query_rows": len(query),
                    "parameters": dict(TREE_PARAMETERS), "given_features": given,
                    "categorical_features": categorical,
                    "ordinal_features": [n for n, cat in zip(given, categorical) if not cat],
                    "marginal_share": .01, "marginal_pseudocount": 1., "threads": 2}


def e051_library(frame, schema, frozen_e050):
    """Share E050 query/base, and fit only the preregistered direct trees."""
    predicted, options, _, query = _partition(frame, schema)
    if predicted != frozen_e050["predicted"] or not np.array_equal(query, frozen_e050["query"]):
        raise ValueError("E050/E051 fit-query alignment differs")
    tree, diagnostics = direct_tree(frame, schema)
    base, base_raw = frozen_e050["base"], frozen_e050["base_raw"]
    arms, arms_raw = {"tree_0": base}, {"tree_0": base_raw}
    for share in E051_SHARES[1:]:
        name = f"tree_{share:g}"
        arms[name] = {n: (1 - share) * (base[n] / base[n].sum(axis=1, keepdims=True))
                         + share * tree[n] for n in predicted}
        arms_raw[name] = [arms[name][n][i] for i in range(len(query)) for n in predicted]
    return {"base_raw": base_raw, "base": base, "arms_raw": arms_raw, "arms": arms,
            "tree": tree, "query": query, "predicted": predicted, "options": options,
            "components": frozen_e050["components"], "diagnostics": diagnostics}


def component_oracle(arms, labels, components, floor=.001):
    """Exact finite constant-component maximum on supplied ORACLE rows only.

    Every arm maps item -> (n_oracle, K); labels map item -> integer class.
    First arm is unchanged E041. This function never receives selection/audit
    labels. Whole-arm and pooled component bounds include the official floor.
    """
    names, predicted = list(arms), list(next(iter(arms.values())))
    if sorted(n for group in components for n in group) != sorted(predicted):
        raise ValueError("Components must partition every predicted head exactly once")
    logs = np.stack([np.column_stack([
        np.log(floor_mix(arms[a][n], floor)[np.arange(len(labels[n])), labels[n]])
        for n in predicted]) for a in names])
    uniform = float(np.mean([np.log(arms[names[0]][n].shape[1]) for n in predicted]))
    base_log = float(logs[0].mean())
    oracle_log, choices, detail = np.empty_like(logs[0]), [], []
    for group in components:
        indices = [predicted.index(n) for n in group]
        scores = logs[:, :, indices].mean(axis=(1, 2))
        choice = int(scores.argmax())
        oracle_log[:, indices] = logs[choice][:, indices]
        choices.append(names[choice])
        detail.append({"items": group, "choice": names[choice],
                       "arm_log_scores": dict(zip(names, map(float, scores)))})
    delta = float(oracle_log.mean()) - base_log
    return {"base_log_score": base_log, "oracle_log_score": float(oracle_log.mean()),
            "uniform_reference": uniform, "delta_log": delta,
            "delta_skill": delta / uniform, "delta_skill_over_3": delta / uniform / 3,
            "choices": choices, "components": detail, "rows": logs.shape[1],
            "whole_arm_delta_skill": {a: float(logs[i].mean() - base_log) / uniform
                                       for i, a in enumerate(names)}}
