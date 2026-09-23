"""E049: honestly selected TabPFN root beliefs through the unchanged E041 tree.

Both alternatives share fitted first-stage products and E041 evidence. Four
disjoint descendant closures receive bounded E047 confidence mixtures; all
other raw vectors and all control instruments remain exactly E041.
"""

import os

os.environ["TABPFN_DISABLE_TELEMETRY"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

import hashlib
from importlib.metadata import version as e049_package_version
from pathlib import Path
from types import FunctionType

import numpy as np
from tabpfn import TabPFNClassifier
from tabpfn.base import ClassifierModelSpecs
from tabpfn.constants import ModelVersion
from tabpfn.model_loading import load_model_criterion_config

from src.models import supervised_retrieval as parent
from src.models import hh_cap, link_sharp
from src.models.hier_backoff import _layout
from src.models.adaptive_final_evidence import e047_alpha, e047_apply, e047_fit_policies

E049_SEED = 4901
E049_REFERENCE_ROWS = 512
E049_MARKER = "s3_11_intent_return_12m_lbl"
E049_CHECKPOINT = Path(__file__).resolve().parents[2] / "tmp/e048-model/tabpfn-v2-classifier.ckpt"
E049_CHECKPOINT_SHA256 = "f65a35685aeef42e31b796d9bfa34e68d6fc780bc98e7bff7763802964cf435f"
E049_LAST_DIAGNOSTICS = {}
LAST_DIAGNOSTICS = E049_LAST_DIAGNOSTICS

# Never download or lazily load weights inside prediction.
assert e049_package_version("tabpfn") == "8.0.8"
assert hashlib.sha256(E049_CHECKPOINT.read_bytes()).hexdigest() == E049_CHECKPOINT_SHA256
E049_MODELS, E049_CRITERION, E049_CONFIGS, E049_INFERENCE_CONFIG = load_model_criterion_config(
    model_path=E049_CHECKPOINT,
    check_bar_distribution_criterion=False,
    cache_trainset_representation=False,
    which="classifier",
    version="v2",
    download_if_not_exists=False,
)
E049_V2_SPEC = ClassifierModelSpecs(E049_MODELS[0], E049_CONFIGS[0], E049_INFERENCE_CONFIG)


def e049_groups(frame, schema):
    """Rank four schema parents; reject any intersecting descendant closures."""
    records, items, options = _layout(frame, schema)
    predicted = [name for name in items if records[name]["class"] == "PREDICT"]
    children = {name: [] for name in items}
    for name in predicted:
        gate = records[name].get("gate")
        if gate and gate["parent"] in children:
            children[gate["parent"]].append(name)
    eligible = [name for name in predicted if children[name] and len(options[name]) <= 10]
    roots = sorted(eligible, key=lambda name: -len(children[name]))[:4]
    if len(roots) != 4:
        return [], []
    groups, seen = [], set()
    for root in roots:
        closure, todo = set(), [root]
        while todo:
            name = todo.pop()
            if name not in closure:
                closure.add(name)
                todo.extend(children[name])
        if closure & seen:
            return [], []
        seen.update(closure)
        groups.append([name for name in predicted if name in closure])
    return roots, groups


def e049_shadow_split(frame, schema):
    """Hide all correction labels; reserve references in the same shuffle."""
    predicted = [name for name, record in schema["items"].items() if record["class"] == "PREDICT"]
    visible = np.flatnonzero(~frame[predicted].isna().any(axis=1).to_numpy())
    shadow = frame.iloc[visible].copy().reset_index(drop=True)
    shuffled = np.random.default_rng(E049_SEED).permutation(len(visible))
    nfit, nselect, naudit = (min(cap, len(visible) // 10) for cap in (800, 600, 400))
    fit = shuffled[:nfit]
    select = shuffled[nfit:nfit + nselect]
    end = nfit + nselect + naudit
    audit = shuffled[nfit + nselect:end]
    reference = shuffled[end:end + E049_REFERENCE_ROWS]
    shadow.loc[np.concatenate((fit, select, audit)), predicted] = np.nan
    return shadow, visible, fit, select, audit, reference


def e049_tabpfn(frame, schema, roots, reference, query):
    """GIVEN-only CPU predictions in complete schema order; omit singletons."""
    records, items, options = _layout(frame, schema)
    predicted = [name for name in items if records[name]["class"] == "PREDICT"]
    reference, query = np.asarray(reference, dtype=int), np.asarray(query, dtype=int)
    if (len(reference) != E049_REFERENCE_ROWS or len(np.unique(reference)) != len(reference)
            or np.intersect1d(reference, query).size
            or frame.iloc[reference][predicted].isna().any().any()):
        raise ValueError("PFN requires 512 distinct visible reference rows excluding every query")
    if not frame.iloc[query][predicted].isna().all().all():
        raise ValueError("PFN query PREDICT blocks must be completely hidden")
    given = [name for name in items if records[name]["class"] == "GIVEN"]
    features = np.column_stack([
        frame[name].map({value: index for index, value in enumerate(options[name])}).to_numpy(dtype=float)
        for name in given])
    result = {}
    for root in roots:
        labels = frame.iloc[reference][root].map(
            {value: index for index, value in enumerate(options[root])}).to_numpy(dtype=int)
        if len(np.unique(labels)) < 2:
            continue
        classifier = TabPFNClassifier.create_default_for_version(
            ModelVersion.V2, model_path=E049_V2_SPEC, n_estimators=1,
            device="cpu", fit_mode="fit_preprocessors", n_jobs=1, random_state=0,
            categorical_features_indices=list(range(len(given))),
        )
        classifier.fit(features[reference], labels)
        probability = np.zeros((len(query), len(options[root])), dtype=float)
        probability[:, np.asarray(classifier.classes_, dtype=int)] = classifier.predict_proba(features[query])
        if (not np.isfinite(probability).all() or (probability < 0).any()
                or not np.allclose(probability.sum(axis=1), 1.)):
            raise ValueError("Invalid PFN root probability vector")
        result[root] = probability
        del classifier
    return result


def e049_cached_renderer():
    """One frame's private E041 function globals, caching only fixed products."""
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


def e049_root_layer(rows, shares, root_probability, query):
    """Replace entire root belief, including old evidence; keep descendants."""
    replaced_rows = dict(rows)
    replaced_shares = dict(shares)
    for root in root_probability:
        replaced_shares[root] = (1., 1.)
    for index, position in enumerate(query):
        evidence, concentrated = rows.get(position, ({}, False))
        replaced = dict(evidence)
        replaced.update({root: probability[index] for root, probability in root_probability.items()})
        replaced_rows[position] = (replaced, concentrated)
    return replaced_rows, replaced_shares


def e049_capture(frame, schema, roots, reference, cols=None, kappas=None):
    """Render both subtree endpoints with identical fitting and evidence."""
    records, items, options = _layout(frame, schema)
    predicted = [name for name in items if records[name]["class"] == "PREDICT"]
    query = np.flatnonzero(frame[predicted].isna().any(axis=1).to_numpy())
    render = e049_cached_renderer()
    captured = []

    def layer(f, s, model_dists):
        if not captured:
            captured.append(parent.supervised_layer(f, s, model_dists))
        return captured[0]

    output = render(frame, schema, cols=cols, kappas=kappas,
                    layer_fn=layer, configs=hh_cap.CONFIGS)
    base = {name: np.stack(output[index::len(predicted)])
            for index, name in enumerate(predicted)}
    roots_probability = e049_tabpfn(frame, schema, roots, reference, query)
    if not roots_probability:
        return output, base, {}, query
    replacement = e049_root_layer(*captured[0], roots_probability, query)
    candidate_output = render(frame, schema, cols=cols, kappas=kappas,
                              layer_fn=lambda *args: replacement, configs=hh_cap.CONFIGS)
    candidate = {name: np.stack(candidate_output[index::len(predicted)])
                 for index, name in enumerate(predicted)}
    # Neither the trained net nor its cached maps survive this capture call.
    return output, base, candidate, query


def predict(frame, schema, cols=None, kappas=None):
    E049_LAST_DIAGNOSTICS.clear()
    if E049_MARKER not in schema["items"]:
        return parent.predict(frame, schema, cols=cols, kappas=kappas)
    predicted = [name for name, record in schema["items"].items() if record["class"] == "PREDICT"]
    blank = frame[predicted].isna().to_numpy()
    held = blank.any(axis=1)
    if not held.any() or not blank[held].all():
        return parent.predict(frame, schema, cols=cols, kappas=kappas)
    roots, groups = e049_groups(frame, schema)
    if not roots:
        E049_LAST_DIAGNOSTICS["reason"] = "four disjoint eligible root closures required"
        return parent.predict(frame, schema, cols=cols, kappas=kappas)
    shadow, visible, fit, select, audit, reference = e049_shadow_split(frame, schema)
    if len(reference) < E049_REFERENCE_ROWS or min(len(fit), len(select), len(audit)) == 0:
        E049_LAST_DIAGNOSTICS["reason"] = "insufficient shadow references"
        return parent.predict(frame, schema, cols=cols, kappas=kappas)
    shadow_output, base, candidate, query = e049_capture(
        shadow, schema, roots, reference, cols=cols, kappas=kappas)
    del shadow_output
    if not candidate:
        E049_LAST_DIAGNOSTICS["reason"] = "single-class shadow roots"
        return parent.predict(frame, schema, cols=cols, kappas=kappas)
    _, _, options = _layout(frame, schema)
    labels = {name: frame.iloc[visible[query]][name].map(
        {value: index for index, value in enumerate(options[name])}).to_numpy(dtype=int)
        for name in predicted}
    lookup = np.full(len(shadow), -1, dtype=int)
    lookup[query] = np.arange(len(query))
    policies, diagnostics = e047_fit_policies(base, candidate, labels, groups,
                                              lookup[fit], lookup[select], lookup[audit])
    E049_LAST_DIAGNOSTICS.update(diagnostics)
    E049_LAST_DIAGNOSTICS.update({"roots": roots, "groups": groups, "policies": policies,
                                  "reference_rows": len(reference)})
    del shadow, base, candidate, query, labels, lookup
    if not policies:
        return parent.predict(frame, schema, cols=cols, kappas=kappas)
    reference = np.random.default_rng(E049_SEED).permutation(visible)[:E049_REFERENCE_ROWS]
    output, base, candidate, query = e049_capture(
        frame, schema, roots, reference, cols=cols, kappas=kappas)
    if not candidate:
        E049_LAST_DIAGNOSTICS["reason"] = "single-class final roots"
        return output
    # A final reference singleton contributes no new root belief. In that case
    # even normalization of its untouched E041 subtree must be avoided.
    policies = {section: policy for section, policy in policies.items()
                if not np.array_equal(base[roots[int(section)]], candidate[roots[int(section)]])}
    mixed = e047_apply(base, candidate, groups, policies)
    active = {name for section in policies for name in groups[int(section)]}
    result = list(output)
    for row in range(len(query)):
        for col, name in enumerate(predicted):
            if name in active:
                result[row * len(predicted) + col] = mixed[name][row]
    return result
