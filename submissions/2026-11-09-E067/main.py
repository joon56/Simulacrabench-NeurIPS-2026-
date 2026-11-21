"""E067: E041 plus composable per-instrument additions.

- TabICLv2 expert mixture (E065 code path) on any instrument listed in PLAN with a
  fixed alpha or the A045 guarded selection ("guard").
- UNHCR wave-coded sentinel transfer (E066 code path) when UNHCR_FIX is True.
Instruments not listed call the unchanged E041 predictor (e041_core.py is a byte
copy of submissions/2026-09-19-E041/main.py). Weights are bundled, loaded at import.
"""
import collections
import hashlib
import os
import sys
import time
import types

PLAN = {"world_bank": 0.5}   # set at build: instrument -> alpha | "guard"
UNHCR_FIX = False            # set at build
SEEDS = (0,)                 # set at build: E041 network seeds averaged cellwise
REGATE = False               # set at build: E068 data-checked re-gating (UNHCR)
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
FLOOR = 0.001
MARKERS = {"world_bank": ("user.lowestAcceptablePay", "user.wageOfSimilarEmployees"),
           "unicef": ("Country", "Q06", "Q18"),
           "unhcr": ("s3_11_intent_return_12m_lbl", "wave")}
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


def _mix(base, expert, alpha, conf=False):
    """Linear pool. conf=True scales alpha per cell by E041's uncertainty,
    (1 - max p) / (1 - 1/K), so confident (e.g. linked) cells stay near E041."""
    if alpha == 0:
        return base
    if not conf:
        return (1.0 - alpha) * _normalize(base) + alpha * _normalize(expert)
    p = _normalize(base)
    k = p.shape[1]
    w = alpha * (1.0 - p.max(axis=1, keepdims=True)) / (1.0 - 1.0 / k)
    return (1.0 - w) * p + w * _normalize(expert)


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


def _guarded(frame, schema, given, heads, options, visible, conf=False):
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
    totals = [float(_cell_logs({n: _mix(base_s[n], q_s[n], a, conf) for n in heads}, truth_s, heads).mean())
              for a in ALPHAS]
    alpha = ALPHAS[int(np.argmax(totals))]
    reference = _cell_logs(base_e, truth_e, heads).mean(axis=1)
    candidate = _cell_logs({n: _mix(base_e[n], q_e[n], alpha, conf) for n in heads},
                           truth_e, heads).mean(axis=1)
    d = candidate - reference
    sd = float(d.std(ddof=1))
    lower = float(d.mean() - 1.645 * sd / np.sqrt(len(d))) if sd > 0 else float(d.mean())
    accepted = bool(alpha > 0 and lower > 0)
    STATS["guard"] = dict(selection=totals, alpha=alpha, lower=lower, accepted=accepted)
    return alpha if accepted else 0.0


AGREE_MAX = float(os.environ.get("E069_AGREE_MAX", "0.95"))  # E069 threshold; env only in local tests


def _gate_agreement(frame, schema, name, visible):
    """Share of visible rows where the schema gate predicts the child's sentinel correctly."""
    gate = schema["items"][name]["gate"]
    parent = frame[gate["parent"]].iloc[visible]
    child = frame[name].iloc[visible]
    asked = parent.isin(gate["observed_if"]).to_numpy()
    skipped = (child == schema["gated_value"]).to_numpy()
    return float(np.mean(skipped == ~asked))


def _replace_sentinel(base, expert):
    p = _normalize(base)
    content = p[:, :-1]
    total = content.sum(axis=1, keepdims=True)
    flat = np.full_like(content, 1.0 / content.shape[1])
    content = np.where(total > 0, content / np.where(total > 0, total, 1.0), flat)
    s = _normalize(expert)[:, -1:]
    return np.hstack(((1.0 - s) * content, s))


def _sentinel_only(frame, schema, base_vectors, base, given, heads, options, visible, held):
    """E069: replace E041's sentinel mass by a direct classifier's where the gate is approximate."""
    items = schema["items"]
    flagged = [n for n in heads if items[n].get("gate")
               and _gate_agreement(frame, schema, n, visible) < AGREE_MAX]
    STATS["sentinel_heads"] = len(flagged)
    if not flagged:
        return base_vectors
    started = time.monotonic()
    q = _expert(frame, given, flagged, options, visible, held)
    STATS["sentinel_expert_seconds"] = round(time.monotonic() - started, 3)
    maps = dict(base)
    for n in flagged:
        maps[n] = _replace_sentinel(base[n], q[n])
    return _flatten(maps, heads)


def _with_expert(frame, schema, base_vectors, setting):
    given, heads, options = _layout(schema)
    visible, held = _roles(frame, heads)
    if len(held) == 0 or len(visible) < 2:
        return base_vectors
    base = _restore(base_vectors, heads, len(held), options)
    conf = False
    if isinstance(setting, dict):
        conf = bool(setting.get("conf", False))
        if setting.get("sentinel") and setting["alpha"] == 0:
            return _sentinel_only(frame, schema, base_vectors, base, given, heads, options, visible, held)
        setting = setting["alpha"]
    started = time.monotonic()
    if setting == "guard":
        alpha = _guarded(frame, schema, given, heads, options, visible, conf)
    else:
        alpha = float(setting)
    STATS["alpha"] = alpha
    STATS["conf"] = conf
    STATS["shadow_seconds"] = round(time.monotonic() - started, 3)
    if alpha == 0:
        return base_vectors
    if BUDGET_SECONDS is not None and time.monotonic() - _T0 > BUDGET_SECONDS:
        STATS["skipped"] = "budget"
        return base_vectors
    started = time.monotonic()
    q = _expert(frame, given, heads, options, visible, held)
    STATS["final_expert_seconds"] = round(time.monotonic() - started, 3)
    dump = os.environ.get("E067_DUMP")  # local rehearsal only; unset on the platform
    if dump:
        np.savez_compressed("%s-%d.npz" % (dump, len(heads)),
                            **{"b%d" % i: base[n] for i, n in enumerate(heads)},
                            **{"q%d" % i: q[n] for i, n in enumerate(heads)})
    return _flatten({n: _mix(base[n], q[n], alpha, conf) for n in heads}, heads)


def _diagnostics(name, seconds):
    """Local rehearsal only: written when E065_DIAG is set; never on the platform."""
    path = os.environ.get("E065_DIAG")
    if not path:
        return
    import json
    record = dict(instrument=name, plan=PLAN, unhcr_fix=UNHCR_FIX, seconds=round(seconds, 3),
                  since_import=round(time.monotonic() - _T0, 3),
                  psutil_shim=not hasattr(sys.modules["psutil"], "__file__"), **STATS)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, default=str) + "\n")


# --- E068 re-gating of the s3_11 return branches (verbatim logic of submissions/2026-11-09-E068) ---
PARENT_OLD = "s3_11_intent_return_12m_lbl"
PARENT_NEW = "s3_12_hope_return_someday_lbl"
BRANCHES = ("s7a_", "s7b_", "s7c_")
MIN_WAVE_ROWS = 300
SMOOTH = 20.0
LL_MARGIN = 0.01
LAST = {}


def _options(items, gated, name):
    return list(items[name]["values"]) + ([gated] if items[name].get("gate") else [])


def _rates(parent_values, skip, levels):
    """Smoothed per-parent-value skip rate pooled over children, and its log-likelihood."""
    overall = skip.mean()
    rates, ll = {}, 0.0
    for level in levels:
        sel = parent_values == level
        n = int(sel.sum()) * skip.shape[1]
        k = float(skip[sel].sum())
        r = (k + SMOOTH * overall) / (n + SMOOTH)
        r = min(max(r, 1e-6), 1 - 1e-6)
        rates[level] = r
        ll += k * np.log(r) + (n - k) * np.log(1 - r)
    return rates, ll


def regate(frame, schema, vectors, force=False):
    items = schema["items"]
    gated = schema["gated_value"]
    heads = [n for n, r in items.items() if r["class"] == "PREDICT"]
    if PARENT_NEW not in heads or PARENT_OLD not in heads or "wave" not in frame:
        return vectors
    block = frame[heads]
    held = block.isna().all(axis=1).to_numpy().nonzero()[0]
    visible = block.notna().all(axis=1).to_numpy().nonzero()[0]
    width = len(heads)
    if len(held) + len(visible) != len(frame) or len(vectors) != len(held) * width:
        return vectors
    waves_all = frame["wave"].astype(str).to_numpy()
    vis = frame.iloc[visible]
    vis_wave = waves_all[visible]
    new_levels = _options(items, gated, PARENT_NEW)
    old_levels = _options(items, gated, PARENT_OLD)
    j_new = heads.index(PARENT_NEW)
    belief = np.array([vectors[i * width + j_new] for i in range(len(held))], dtype=np.float64)
    belief = belief / belief.sum(axis=1, keepdims=True)
    out = None
    LAST.clear()
    for branch in BRANCHES:
        children = [n for n in heads if n.startswith(branch) and items[n].get("gate")
                    and items[n]["gate"]["parent"] == PARENT_OLD]
        for wave in ("1", "2"):
            in_w = vis_wave == wave
            if int(in_w.sum()) < MIN_WAVE_ROWS:
                continue
            active = [c for c in children if (vis[c].to_numpy()[in_w] == gated).any()]
            if not active:
                continue
            skip = np.stack([(vis[c].to_numpy()[in_w] == gated) for c in active], axis=1).astype(float)
            rates_new, ll_new = _rates(vis[PARENT_NEW].to_numpy()[in_w], skip, new_levels)
            _, ll_old = _rates(vis[PARENT_OLD].to_numpy()[in_w], skip, old_levels)
            switch = bool(force or ll_new > ll_old + LL_MARGIN * abs(ll_old))
            LAST[(branch, wave)] = dict(children=len(active), ll_new=float(ll_new), ll_old=float(ll_old),
                                        switch=switch)
            if not switch:
                continue
            r = np.array([rates_new[level] for level in new_levels])
            if out is None:
                out = [list(v) for v in vectors]
            rows = [i for i, row in enumerate(held) if waves_all[row] == wave]
            for c in active:
                j = heads.index(c)
                for i in rows:
                    v = np.asarray(out[i * width + j], dtype=np.float64)
                    v = v / v.sum()
                    content = v[:-1]
                    total = content.sum()
                    content = content / total if total > 0 else np.full(len(content), 1.0 / len(content))
                    s_new = float(belief[i] @ r)
                    out[i * width + j] = list(np.append((1.0 - s_new) * content, s_new))
    return vectors if out is None else out



# --- E066 wave-coded sentinel transfer (verbatim logic of submissions/2026-11-08-E066) ---
FAMILIES = ("s6_4_", "s6_6_", "s6_11_", "s7a_7_", "s7b_1_")
MIN_ROWS = 300


def flagged_cells(frame, schema, heads, visible):
    """(item, wave) cells where the visible rows show the round-specific coding."""
    items = schema["items"]
    gated = schema["gated_value"]
    wave = frame["wave"].astype(str).iloc[visible]
    flags = set()
    for name in heads:
        rec = items[name]
        if not name.startswith(FAMILIES) or not rec.get("gate") or "0" not in rec["values"]:
            continue
        values = frame[name].iloc[visible]
        for this, other in (("1", "2"), ("2", "1")):
            in_this = wave == this
            if int(in_this.sum()) < MIN_ROWS:
                continue
            sentinel_this = int(((values == gated) & in_this).sum())
            sentinel_other = int(((values == gated) & (wave == other)).sum())
            if sentinel_this == 0 and sentinel_other > 0:
                flags.add((name, this))
    return flags


def transfer(frame, schema, vectors):
    items = schema["items"]
    heads = [n for n, r in items.items() if r["class"] == "PREDICT"]
    block = frame[heads]
    held = block.isna().all(axis=1).to_numpy().nonzero()[0]
    visible = block.notna().all(axis=1).to_numpy().nonzero()[0]
    if len(held) + len(visible) != len(frame) or len(vectors) != len(held) * len(heads):
        return vectors
    flags = flagged_cells(frame, schema, heads, visible)
    STATS["unhcr_flags"] = len(flags)
    if not flags:
        return vectors
    out = [list(v) for v in vectors]
    waves = frame["wave"].astype(str).to_numpy()
    width = len(heads)
    for j, name in enumerate(heads):
        for this in ("1", "2"):
            if (name, this) not in flags:
                continue
            zero = items[name]["values"].index("0")
            sentinel = len(items[name]["values"])
            for i, row in enumerate(held):
                if waves[row] == this:
                    vector = out[i * width + j]
                    vector[zero] += vector[sentinel]
                    vector[sentinel] = 0.0
    return out


def _e041(frame, schema):
    """E041 output, or the cellwise mean of E041 runs over SEEDS (network seed only).

    Averaging probabilities cannot lower the expected log score of a single run
    (Jensen), and the grader's floor is affine, so the bound survives flooring.
    """
    if tuple(SEEDS) == (0,):
        return e041_core.predict(frame, schema)
    runs = []
    original = e041_core.TORCH_SEED
    try:
        for seed in SEEDS:
            if runs and BUDGET_SECONDS is not None and time.monotonic() - _T0 > 0.6 * BUDGET_SECONDS:
                STATS["seeds_skipped"] = True
                break
            e041_core.TORCH_SEED = seed
            runs.append(e041_core.predict(frame, schema))
    finally:
        e041_core.TORCH_SEED = original
    STATS["seeds_used"] = len(runs)
    if len(runs) == 1:
        return runs[0]
    out = []
    for vectors in zip(*runs):
        total = None
        for vector in vectors:
            p = np.asarray(vector, dtype=np.float64)
            p = p / p.sum()
            total = p if total is None else total + p
        out.append((total / len(runs)).tolist())
    return out


def _instrument(schema):
    items = schema["items"]
    for name, markers in MARKERS.items():
        if all(marker in items for marker in markers):
            return name
    return None


def predict(frame, schema):
    started = time.monotonic()
    STATS.clear()
    name = _instrument(schema)
    vectors = _e041(frame, schema)
    STATS["e041_seconds"] = round(time.monotonic() - started, 3)
    if name in PLAN:
        if STRICT:
            vectors = _with_expert(frame, schema, vectors, PLAN[name])
        else:
            try:
                vectors = _with_expert(frame, schema, vectors, PLAN[name])
            except Exception:  # non-strict builds keep E041's output on any expert failure
                STATS["fallback"] = True
    if name == "unhcr" and REGATE and "wave" in frame:
        vectors = regate(frame, schema, vectors)
        STATS["regate"] = {"%s/%s" % key: value["switch"] for key, value in LAST.items()}
    if name == "unhcr" and UNHCR_FIX and "wave" in frame:
        vectors = transfer(frame, schema, vectors)
    _diagnostics(name or "other", time.monotonic() - started)
    return vectors
