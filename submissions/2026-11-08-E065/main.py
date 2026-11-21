"""E065: E041 with a TabICLv2 expert mixture on World Bank only.

UNICEF and UNHCR call the unchanged E041 predictor (e041_core.py is a byte copy
of submissions/2026-09-19-E041/main.py). World Bank mixes E041's final
distributions with a pretrained in-context tabular classifier fitted per
PREDICT head on the GIVEN features. Weights are bundled and loaded at import.
"""
import collections
import hashlib
import os
import sys
import time
import types

VARIANT = "a25"   # set by scripts/build_e065.py: a25 | a50 | guard
STRICT = True     # DEV builds: any expert failure raises instead of falling back
BUDGET_SECONDS = None  # optional wall-clock guard for non-strict builds

_T0 = time.monotonic()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor", "primary"))   # pinned tabicl, einops
sys.path.append(os.path.join(HERE, "vendor", "fallback"))     # tqdm if the image lacks it


def _psutil_shim():
    """Stand-in used only if the image has no psutil.

    TabICL's inference path reads virtual_memory().total and .available only
    (its cgroup code then caps the figure at the container limit).
    """
    module = types.ModuleType("psutil")
    svmem = collections.namedtuple("svmem", "total available")

    def virtual_memory():
        info = {}
        with open("/proc/meminfo", encoding="ascii") as fh:
            for line in fh:
                key, _, rest = line.partition(":")
                fields = rest.split()
                if fields:
                    info[key] = int(fields[0]) * 1024
        total = info["MemTotal"]
        return svmem(total, info.get("MemAvailable", info.get("MemFree", total)))

    def cpu_count(logical=True):
        return os.cpu_count()

    module.virtual_memory = virtual_memory
    module.cpu_count = cpu_count
    return module


try:
    import psutil  # noqa: F401
except ImportError:
    sys.modules["psutil"] = _psutil_shim()

import numpy as np  # noqa: E402
import torch  # noqa: E402

import e041_core  # noqa: E402
from tabicl import TabICLClassifier  # noqa: E402

CHECKPOINT = os.path.join(HERE, "weights", "tabicl-classifier-v2-20260212.ckpt")
CHECKPOINT_SHA256 = "bdc7dbd5e4ff21f8f0456fcf90c6b7cdf72dbea960f2d05b19bec19f9b3d4ed0"
with open(CHECKPOINT, "rb") as _fh:
    if hashlib.sha256(_fh.read()).hexdigest() != CHECKPOINT_SHA256:
        raise ValueError("TabICL checkpoint hash mismatch")

OPTIONS = dict(n_estimators=8, norm_methods=["none", "power"],
               feat_shuffle_method="latin", class_shuffle_method="shift",
               random_state=42, softmax_temperature=.9, average_logits=True,
               support_many_classes=True, batch_size=8, kv_cache=False,
               device="cuda", use_amp=True, use_fa3=False, offload_mode=False,
               n_jobs=2, verbose=False, model_path=CHECKPOINT,
               allow_auto_download=False,
               checkpoint_version="tabicl-classifier-v2-20260212.ckpt")

_loader = TabICLClassifier(**OPTIONS)
_loader._load_model()
SHARED_MODEL = _loader.model_.to("cuda").eval()
SHARED_CONFIG = _loader.model_config_.copy()
del _loader

ALPHAS = (0.0, 0.25, 0.5)
FIXED_ALPHA = {"a25": 0.25, "a50": 0.5}
FLOOR = 0.001
WB_MARKERS = ("user.lowestAcceptablePay", "user.wageOfSimilarEmployees")
STATS = collections.OrderedDict()


class _SharedClassifier(TabICLClassifier):
    """Reuse the one checkpoint loaded at import; per-head contexts stay separate."""

    def _load_model(self):
        SHARED_MODEL.clear_cache()
        self.model_ = SHARED_MODEL
        self.model_config_ = SHARED_CONFIG.copy()
        self.model_path_ = CHECKPOINT


def _layout(schema):
    items = schema["items"]
    given = [n for n, r in items.items() if r["class"] == "GIVEN"]
    heads = [n for n, r in items.items() if r["class"] == "PREDICT"]
    options = {n: list(items[n]["values"]) + ([schema["gated_value"]] if items[n].get("gate") else [])
               for n in heads}
    return given, heads, options


def _roles(frame, heads):
    block = frame[heads]
    held = np.flatnonzero(block.isna().all(axis=1).to_numpy())
    visible = np.flatnonzero(block.notna().all(axis=1).to_numpy())
    if len(held) + len(visible) != len(frame):
        raise ValueError("Partially visible PREDICT blocks")
    return visible, held


def _restore(vectors, heads, n_rows, options):
    if len(vectors) != n_rows * len(heads):
        raise ValueError("Unexpected E041 vector count")
    maps = {}
    for j, name in enumerate(heads):
        p = np.asarray(vectors[j::len(heads)], dtype=np.float64)
        if p.shape != (n_rows, len(options[name])) or not np.isfinite(p).all() \
                or (p < 0).any() or (p.sum(axis=1) <= 0).any():
            raise ValueError("Invalid E041 distribution for " + name)
        maps[name] = p
    return maps


def _flatten(maps, heads):
    n = len(maps[heads[0]])
    return [maps[name][i].tolist() for i in range(n) for name in heads]


def _normalize(p):
    return p / p.sum(axis=1, keepdims=True)


def _mix(base, expert, alpha):
    if alpha == 0:
        return base
    return (1.0 - alpha) * _normalize(base) + alpha * _normalize(expert)


def _floored(p):
    return FLOOR + (1.0 - FLOOR * p.shape[1]) * _normalize(p)


def _labels(frame, rows, name, options):
    code = {v: i for i, v in enumerate(options[name])}
    y = frame[name].iloc[rows].map(code)
    if y.isna().any():
        raise ValueError("Label outside schema for " + name)
    return y.to_numpy(dtype=int)


def _expert(frame, given, heads, options, context, query):
    """One TabICL fit/predict per head; context rows carry labels, queries GIVEN only."""
    X_ctx = frame[given].iloc[context].astype(object).reset_index(drop=True)
    X_q = frame[given].iloc[query].astype(object).reset_index(drop=True)
    if not any(X_ctx[n].nunique(dropna=False) > 1 for n in given):
        raise ValueError("No usable GIVEN feature")
    maps = {}
    for name in heads:
        y = _labels(frame, context, name, options)
        width = len(options[name])
        observed = np.unique(y)
        if len(observed) == 1:
            p = np.zeros((len(query), width))
            p[:, observed[0]] = 1.0
        else:
            estimator = _SharedClassifier(**OPTIONS)
            estimator.fit(X_ctx, y)
            raw = np.asarray(estimator.predict_proba(X_q), dtype=np.float64)
            classes = np.asarray(estimator.classes_)
            if raw.shape != (len(query), len(classes)) or not np.isfinite(raw).all() \
                    or (raw < 0).any() or (raw.sum(axis=1) <= 0).any():
                raise ValueError("Invalid expert distribution for " + name)
            p = np.zeros((len(query), width))
            p[:, classes.astype(int)] = _normalize(raw)
        maps[name] = p
    SHARED_MODEL.clear_cache()
    return maps


def _cell_logs(maps, truth, heads):
    rows = np.arange(len(truth[heads[0]]))
    return np.stack([np.log(_floored(maps[name])[rows, truth[name]]) for name in heads], axis=1)


def _guarded(frame, schema, given, heads, options, visible):
    """A045 procedure: shadow E041/expert on F, alpha on S, lower-bound guard on E."""
    if len(visible) < 2001:
        STATS["guard"] = "small_visible"
        return 0.0
    order = np.random.Generator(np.random.PCG64(4501)).permutation(np.sort(visible))
    s_rows, e_rows = np.sort(order[:1000]), np.sort(order[1000:2000])
    f_rows = np.sort(order[2000:])
    shadow = frame.copy()
    hide = shadow.index[np.concatenate((s_rows, e_rows))]
    shadow.loc[hide, heads] = np.nan
    _, shadow_held = _roles(shadow, heads)
    started = time.monotonic()
    shadow_base = _restore(e041_core.predict(shadow, schema), heads, len(shadow_held), options)
    STATS["shadow_e041_seconds"] = round(time.monotonic() - started, 3)
    position = {row: i for i, row in enumerate(shadow_held)}
    pick_s = [position[r] for r in s_rows]
    pick_e = [position[r] for r in e_rows]
    started = time.monotonic()
    q = _expert(shadow, given, heads, options, f_rows, np.concatenate((s_rows, e_rows)))
    STATS["shadow_expert_seconds"] = round(time.monotonic() - started, 3)
    truth_s = {n: _labels(frame, s_rows, n, options) for n in heads}
    truth_e = {n: _labels(frame, e_rows, n, options) for n in heads}
    base_s = {n: shadow_base[n][pick_s] for n in heads}
    base_e = {n: shadow_base[n][pick_e] for n in heads}
    q_s = {n: q[n][:1000] for n in heads}
    q_e = {n: q[n][1000:] for n in heads}
    totals = [float(_cell_logs({n: _mix(base_s[n], q_s[n], a) for n in heads}, truth_s, heads).mean())
              for a in ALPHAS]
    alpha = ALPHAS[int(np.argmax(totals))]
    reference = _cell_logs(base_e, truth_e, heads).mean(axis=1)
    candidate = _cell_logs({n: _mix(base_e[n], q_e[n], alpha) for n in heads}, truth_e, heads).mean(axis=1)
    d = candidate - reference
    sd = float(d.std(ddof=1))
    lower = float(d.mean() - 1.645 * sd / np.sqrt(len(d))) if sd > 0 else float(d.mean())
    accepted = bool(alpha > 0 and lower > 0)
    STATS["guard"] = dict(selection=totals, alpha=alpha, lower=lower, accepted=accepted)
    return alpha if accepted else 0.0


def _world_bank(frame, schema, base_vectors):
    given, heads, options = _layout(schema)
    visible, held = _roles(frame, heads)
    if len(held) == 0 or len(visible) < 2:
        return base_vectors
    base = _restore(base_vectors, heads, len(held), options)
    started = time.monotonic()
    if VARIANT == "guard":
        alpha = _guarded(frame, schema, given, heads, options, visible)
    else:
        alpha = FIXED_ALPHA[VARIANT]
    STATS["alpha"] = alpha
    STATS["shadow_seconds"] = round(time.monotonic() - started, 3)
    if alpha == 0:
        return base_vectors
    if BUDGET_SECONDS is not None and time.monotonic() - _T0 > BUDGET_SECONDS:
        STATS["skipped"] = "budget"
        return base_vectors
    started = time.monotonic()
    q = _expert(frame, given, heads, options, visible, held)
    STATS["final_expert_seconds"] = round(time.monotonic() - started, 3)
    return _flatten({n: _mix(base[n], q[n], alpha) for n in heads}, heads)


def _diagnostics(name, seconds):
    """Local rehearsal only: written when E065_DIAG is set; never on the platform."""
    path = os.environ.get("E065_DIAG")
    if not path:
        return
    import json
    record = dict(instrument=name, variant=VARIANT, seconds=round(seconds, 3),
                  since_import=round(time.monotonic() - _T0, 3),
                  psutil_shim=not hasattr(sys.modules["psutil"], "__file__"), **STATS)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, default=str) + "\n")


def predict(frame, schema):
    started = time.monotonic()
    STATS.clear()
    items = schema["items"]
    if not all(marker in items for marker in WB_MARKERS):
        vectors = e041_core.predict(frame, schema)
        _diagnostics("control", time.monotonic() - started)
        return vectors
    base_vectors = e041_core.predict(frame, schema)
    STATS["e041_seconds"] = round(time.monotonic() - started, 3)
    if STRICT:
        vectors = _world_bank(frame, schema, base_vectors)
    else:
        try:
            vectors = _world_bank(frame, schema, base_vectors)
        except Exception:  # non-strict builds keep E041's output on any expert failure
            STATS["fallback"] = True
            vectors = base_vectors
    _diagnostics("world_bank", time.monotonic() - started)
    return vectors
