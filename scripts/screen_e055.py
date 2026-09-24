"""E055 finite coupled-star diagnostic. Real fits require explicit root GO."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import pickle
import sys
from itertools import product
from time import perf_counter

for variable in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[variable] = "2"

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd

from scripts.audit_a014_sipp import CACHE, GIVEN, REASONS, assign_roles
from scripts.screen_e053 import capture_layer
from src.eval.logloss import floor_mix
from src.eval.recursive_candidates import _mapped, cached_renderer, mask_query
from src.models import hh_cap, link_sharp


SOURCE = CACHE / "a014-month12-restricted.parquet"
REGISTRATION = ROOT / "docs/experiments/E055-coupled-star-replay.md"
LOCAL = ROOT / "external/e055"
AGGREGATE = ROOT / "docs/analysis/E055-outputs"
PARENT = "HOSPITALIZED"
TARGETS = [PARENT, *REASONS]
GRID = link_sharp.LAMBDA_GRID_X
GIVEN_VOCAB = {
    "TAGE": [str(i) for i in range(91)],
    "ESEX": ["1", "2"],
    "ERACE": ["1", "2", "3", "4"],
    "EORIGIN": ["1", "2"],
    "EEDUC": [str(i) for i in range(31, 47)] + ["MISSING"],
    "EMS": [str(i) for i in range(1, 7)] + ["MISSING"],
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sample_digest(row: pd.Series) -> bytes:
    return hashlib.sha256("\0".join(("E055-sample-v1", row.SSUID, row.PNUM)).encode("utf-8")).digest()


def make_adapter(source: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Project only registered model fields; audit keys and flags cannot enter fit."""
    if source.duplicated(["SSUID", "PNUM", "MONTHCODE"]).any():
        raise ValueError("Duplicate person-month")
    if not source["MONTHCODE"].eq("12").all():
        raise ValueError("Only preregistered month 12 is accepted")
    eligible = source["THHLDSTATUS"].isin(["1", "2"]) & pd.to_numeric(source["TAGE_EHC"], errors="coerce").ge(1)
    if not eligible.all():
        raise ValueError("Adapter accepts eligible rows only")
    frame = source[GIVEN].copy().reset_index(drop=True)
    for field in ("EEDUC", "EMS"):
        under_15 = pd.to_numeric(source["TAGE"], errors="coerce").lt(15)
        if not source[field].eq("").equals(under_15):
            raise ValueError(f"{field} blank does not match registered under-15 universe")
        frame[field] = frame[field].replace("", "MISSING")
    for field, values in GIVEN_VOCAB.items():
        unexpected = set(frame[field]) - set(values)
        if unexpected:
            raise ValueError(f"Unexpected {field} values: {sorted(unexpected)}")
    parent = pd.to_numeric(source["THOSPNIT"], errors="coerce")
    if not (source["THOSPNIT"].str.fullmatch(r"\d+").all() and parent.between(0, 365).all()):
        raise ValueError("Invalid hospital parent")
    frame[PARENT] = np.where(parent.to_numpy() > 0, "1", "0")
    for field in REASONS:
        blank = source[field].eq("")
        if (blank & source["AHREASON"].ne("0")).any():
            raise ValueError(f"Ambiguous {field} blank")
        if (~blank & ~source[field].isin(["1", "2"])).any():
            raise ValueError(f"Invalid {field} response")
        frame[field] = source[field].where(~blank, "NA_GATED").to_numpy()
    items = {field: {"class": "GIVEN", "values": values} for field, values in GIVEN_VOCAB.items()}
    items[PARENT] = {"class": "PREDICT", "values": ["0", "1"]}
    for field in REASONS:
        items[field] = {"class": "PREDICT", "values": ["1", "2"],
                        "gate": {"parent": PARENT, "observed_if": ["1"]}}
    return frame, {"items": items, "gated_value": "NA_GATED"}


def mask_outer(frame: pd.DataFrame, schema: dict, outer: np.ndarray) -> pd.DataFrame:
    return mask_query(frame, schema, outer)


def prepare(view: str):
    if view not in ("person", "group"):
        raise ValueError("view must be person or group")
    source = pd.read_parquet(SOURCE)
    eligible = source["THHLDSTATUS"].isin(["1", "2"]) & pd.to_numeric(source["TAGE_EHC"], errors="coerce").ge(1)
    source = source.loc[eligible].copy()
    source["sample_digest"] = source.apply(sample_digest, axis=1)
    source.sort_values(["sample_digest", "SSUID", "PNUM"], inplace=True)
    source = source.head(12000).reset_index(drop=True)
    if len(source) != 12000:
        raise ValueError("Registered sample requires 12000 eligible people")
    roles = assign_roles(source, grouped=view == "group").reset_index(drop=True)
    if any((roles == name).sum() == 0 for name in ("fit", "calibration", "oracle", "selection", "audit")):
        raise ValueError("Empty registered role")
    frame, schema = make_adapter(source)
    outer = np.flatnonzero(roles.ne("fit"))
    masked = mask_outer(frame, schema, outer)
    if not masked.loc[outer, TARGETS].isna().all().all():
        raise AssertionError("Incomplete outer target masking")
    manifest = {"view": view, "rows": len(source), "role_counts": roles.value_counts().to_dict(),
                "sample_hash": digest(b"".join(source["sample_digest"])),
                "sample_namespace": "E055-sample-v1", "role_namespace":
                "A014-household-v1" if view == "group" else "A014-person-v1"}
    return frame, masked, schema, roles, manifest


def _score(vector: np.ndarray, truth: np.ndarray) -> float:
    probability = np.asarray(vector, dtype=float)
    if probability.ndim != 2 or len(probability) != len(truth) or not np.isfinite(probability).all() or (probability < 0).any() or (probability.sum(1) <= 0).any():
        raise ValueError("Invalid raw probability vector")
    return float(np.log(floor_mix(probability)[np.arange(len(truth)), truth]).sum())


def finite_star_oracle(roots: dict, identity: dict, evidence: dict, available: dict,
                       bucket: np.ndarray, labels: dict, original: dict, grid=GRID) -> dict:
    """Exact finite maximum: root pair enumeration, independent child buckets."""
    names = list(labels)
    if names[0] != PARENT or any(name not in evidence for name in names):
        raise ValueError("Expected parent-first complete star")
    n = len(bucket)
    for name in names:
        if len(labels[name]) != n or len(evidence[name]) != n or len(available[name]) != n:
            raise ValueError("Unaligned star arrays")
        if any(value not in grid for value in original[name]):
            raise ValueError("Original share outside registered grid")
    identity_score = sum(_score(identity[name], labels[name]) for name in names)
    best_score, best_pairs, best_composed = identity_score, dict(original), identity
    order = lambda old: (old,) + tuple(value for value in grid if value != old)
    for parent_pair in ((a, b) for a in order(original[PARENT][0])
                        for b in order(original[PARENT][1])):
        bases = roots[parent_pair]
        composed = {PARENT: bases[PARENT].copy()}
        score = _score(composed[PARENT], labels[PARENT])
        pairs = {PARENT: tuple(parent_pair)}
        for name in names[1:]:
            base = bases[name]
            chosen = [original[name][0], original[name][1]]
            final = base.copy()
            for b in (0, 1):
                rows = np.flatnonzero(bucket == b)
                if not len(rows):
                    continue
                active = np.asarray(available[name][rows], bool)
                scores = []
                ranked = order(original[name][b])
                for share in ranked:
                    candidate = base[rows].copy()
                    candidate[active] = (1 - share) * candidate[active] + share * evidence[name][rows][active]
                    scores.append(_score(candidate, labels[name][rows]))
                maximum = max(scores)
                chosen[b] = ranked[scores.index(maximum)]
                final[rows[active]] = ((1 - chosen[b]) * base[rows[active]]
                                       + chosen[b] * evidence[name][rows[active]])
            pairs[name] = tuple(chosen)
            composed[name] = final
            score += _score(final, labels[name])
        if score > best_score:
            best_score, best_pairs, best_composed = score, pairs, composed
    uniform = float(np.mean([np.log(identity[name].shape[1]) for name in names]))
    cells = n * len(names)
    return {"best_log_sum": best_score, "identity_log_sum": identity_score,
            "uniform_reference": uniform, "baseline_skill": 1 + identity_score / (cells * uniform),
            "oracle_skill": 1 + best_score / (cells * uniform),
            "delta_skill_over_3": (best_score - identity_score) / (cells * uniform * 3),
            "shares": best_pairs, "composed": best_composed,
            "per_head_gain": {name: _score(best_composed[name], labels[name]) - _score(identity[name], labels[name])
                              for name in names}}


def build_library(masked: pd.DataFrame, schema: dict):
    """One generic E041 fit with frozen legacy and dormant evidence."""
    query = np.flatnonzero(masked[TARGETS].isna().all(axis=1))
    captured = {}

    def layer(frame, schema_arg, model):
        if captured:
            raise AssertionError("Second evidence fit forbidden")
        captured.update(capture_layer(frame, schema_arg, model))
        return captured["legacy_evidence"], captured["lambdas"]

    renderer = cached_renderer()
    original_raw = renderer(masked, schema, layer_fn=layer, configs=hh_cap.CONFIGS)
    original = {name: tuple(captured["lambdas"].get(name, (0., 0.))) for name in TARGETS}
    if any(len(pair) != 2 or any(share not in GRID for share in pair) for pair in original.values()):
        raise ValueError("Original shares outside registered grid")
    evidence_rows = captured["evidence"]
    evidence = {name: np.zeros((len(query), 2 if name == PARENT else 3)) for name in TARGETS}
    available = {name: np.zeros(len(query), bool) for name in TARGETS}
    bucket = np.zeros(len(query), dtype=int)
    for i, row in enumerate(query):
        entry = evidence_rows.get(int(row))
        if entry is None:
            continue
        values, bucket[i] = entry
        for name in TARGETS:
            vector = values.get(name)
            if vector is not None:
                vector = np.asarray(vector, dtype=float)
                if not np.isfinite(vector).all() or (vector < 0).any():
                    raise ValueError(f"Invalid captured evidence: {name}")
                if vector.sum() == 0:
                    continue
                evidence[name][i] = vector
                available[name][i] = True

    def render(pairs):
        layer_rows = evidence_rows if any(any(pairs[name]) for name in TARGETS) else captured["legacy_evidence"]
        raw = renderer(masked, schema, layer_fn=lambda *args: (layer_rows, pairs), configs=hh_cap.CONFIGS)
        return _mapped(raw, TARGETS, query)

    baseline = render(original)
    original_mapped = _mapped(original_raw, TARGETS, query)
    for name in TARGETS:
        vector = baseline[name]
        if not np.isfinite(vector).all() or (vector < 0).any() or (vector.sum(1) <= 0).any():
            raise ValueError(f"Invalid original endpoint: {name}")
    if any(not np.array_equal(baseline[name], original_mapped[name]) for name in TARGETS):
        parity = max(float(np.max(np.abs(baseline[name] - original_mapped[name]))) for name in TARGETS)
        raise AssertionError(f"Original endpoint parity failed: {parity}")
    zero = {name: (0., 0.) for name in TARGETS}
    roots = {}
    for index, pair in enumerate(product(GRID, repeat=2), 1):
        roots[pair] = render({**zero, PARENT: pair})
        for name in TARGETS:
            vector = roots[pair][name]
            if not np.isfinite(vector).all() or (vector < 0).any() or (vector.sum(1) <= 0).any():
                raise ValueError(f"Invalid frozen root scenario: {pair} {name}")
        if index % 20 == 0:
            print(f"root scenarios {index}/144", flush=True)
    return {"render": render, "roots": roots, "original": original,
            "evidence": evidence, "available": available,
            "bucket": bucket, "query": query, "capture": captured, "identity": baseline,
            "original_parity_max_abs": 0.}


def run(view: str):
    """Explicit execution entry point. Root controls preregistration and GO."""
    stem = f"sipp-{view}"
    outputs = [LOCAL / f"{stem}-capture.pkl.gz", LOCAL / f"{stem}-manifest.json",
               AGGREGATE / f"{stem}-registration.md", AGGREGATE / f"{stem}-oracle.json",
               LOCAL / f"{stem}-roots.npz", LOCAL / f"{stem}-masked.pkl.gz"]
    if any(path.exists() for path in outputs):
        raise FileExistsError("Refusing existing E055 artifacts before fit")
    frame, masked, schema, roles, manifest = prepare(view)
    manifest["registration_sha256"] = digest(REGISTRATION.read_bytes())
    manifest["script_sha256"] = digest(Path(__file__).read_bytes())
    manifest["source_sha256"] = digest(SOURCE.read_bytes())
    manifest["masked_frame_sha256"] = digest(pickle.dumps((schema, masked), protocol=5))
    source_paths = sorted((ROOT / "src").rglob("*.py")) + [Path(__file__),
        ROOT / "scripts/screen_e053.py", ROOT / "scripts/audit_a014_sipp.py",
        ROOT / "tests/test_e055_star.py"]
    manifest["source_code_sha256"] = {path.relative_to(ROOT).as_posix(): digest(path.read_bytes())
                                       for path in source_paths}
    manifest["role_positions"] = {name: np.flatnonzero(roles.eq(name)).tolist()
                                  for name in ("fit", "calibration", "oracle", "selection", "audit")}
    print(f"{view}: fitting one frozen E041 library", flush=True)
    started = perf_counter()
    library = build_library(masked, schema)
    manifest["fit_seconds"] = perf_counter() - started
    frozen = {key: value for key, value in library.items() if key not in ("render", "roots")}
    packed = gzip.compress(pickle.dumps(frozen, protocol=5), mtime=0)
    LOCAL.mkdir(parents=True, exist_ok=True)
    AGGREGATE.mkdir(parents=True, exist_ok=True)
    with outputs[0].open("xb") as stream:
        stream.write(packed)
    manifest["capture_sha256"] = digest(packed)
    matrices = {f"root/{index:03d}/{name}": library["roots"][pair][name]
                for index, pair in enumerate(product(GRID, repeat=2)) for name in TARGETS}
    matrices.update({f"identity/{name}": library["identity"][name] for name in TARGETS})
    with outputs[4].open("xb") as stream:
        np.savez_compressed(stream, **matrices)
    manifest["root_arrays_sha256"] = digest(outputs[4].read_bytes())
    with outputs[5].open("xb") as stream:
        stream.write(gzip.compress(pickle.dumps((schema, masked), protocol=5), mtime=0))
    manifest["masked_archive_sha256"] = digest(outputs[5].read_bytes())
    with outputs[1].open("x", encoding="utf-8") as stream:
        json.dump(manifest, stream, indent=2)
    with outputs[2].open("xb") as stream:
        stream.write(REGISTRATION.read_bytes())
    # Only now map oracle labels; calibration, selection, audit stay unopened.
    query_roles = roles.iloc[library["query"]].to_numpy()
    selected = np.flatnonzero(query_roles == "oracle")
    labels = {name: frame.iloc[library["query"][selected]][name].map(
        {value: i for i, value in enumerate(["0", "1"] if name == PARENT else ["1", "2", "NA_GATED"])}
    ).to_numpy(dtype=int) for name in TARGETS}
    outcome = finite_star_oracle(
                                 {pair: {name: value[selected] for name, value in head.items()}
                                  for pair, head in library["roots"].items()},
                                 {name: value[selected] for name, value in library["identity"].items()},
                                 {name: value[selected] for name, value in library["evidence"].items()},
                                 {name: value[selected] for name, value in library["available"].items()},
                                 library["bucket"][selected], labels, library["original"])
    rendered = library["render"](outcome["shares"])
    parity = max(float(np.max(np.abs(rendered[name][selected] - outcome["composed"][name])))
                 for name in TARGETS)
    if not np.isfinite(parity) or parity > 1e-12:
        raise AssertionError(f"Selected renderer parity failed: {parity}")
    outcome.pop("composed")
    outcome["renderer_parity_max_abs"] = parity
    delta = outcome["delta_skill_over_3"]
    outcome["gate"] = "PASS" if delta > .005 + 1e-10 else "STOP" if delta <= .005 - 1e-10 else "UNRESOLVED"
    outcome["view"] = view
    outcome["oracle_rows"] = len(selected)
    outcome["capture_sha256"] = manifest["capture_sha256"]
    outcome["buckets"] = {str(b): int((library["bucket"][selected] == b).sum()) for b in (0, 1)}
    outcome["available"] = {name: int(library["available"][name][selected].sum()) for name in TARGETS}
    outcome["original_active"] = {name: int((library["available"][name][selected] &
        (np.asarray(library["original"][name])[library["bucket"][selected]] > 0)).sum()) for name in TARGETS}
    outcome["selected_active"] = {name: int((library["available"][name][selected] &
        (np.asarray(outcome["shares"][name])[library["bucket"][selected]] > 0)).sum()) for name in TARGETS}
    outcome["legacy_returned"] = bool(library["capture"]["legacy_evidence"])
    outcome["materialized_dormant"] = bool(library["capture"]["materialized_dormant"])
    with outputs[3].open("x", encoding="utf-8") as stream:
        json.dump(outcome, stream, indent=2, allow_nan=False)
    print(json.dumps({"view": view, "oracle_rows": len(selected), "gate": outcome["gate"],
                      "delta_skill_over_3": delta}), flush=True)
    return outcome


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--view", required=True, choices=("person", "group"))
    args = parser.parse_args()
    run(args.view)
