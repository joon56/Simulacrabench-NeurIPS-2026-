"""E072: E071 plus high-risk probe switches (DIRECT chains, NO_E_CHECK, expert size).

Each instrument's E041 output (cellwise mean over SEEDS; Jensen) may receive one
candidate transform chain from CANDIDATES: TabICLv2 expert mixing (mixNN / confNN),
sentinel replacement on approximate gates (sent, E069), UNHCR re-gating (regate, E068)
or wave-coded sentinel transfer (transfer, E066). The choice is made inside the run on
the delivered visible rows: a fixed PCG64(4501) split S1000/E1000/F, shadow E041 and
expert fitted on F, best chain by pooled floored log score on S, applied only if the
one-sided E lower bound mean(d) - 1.645 sd(d)/sqrt(n) is positive. Otherwise E041.
e041_core.py is a byte copy of submissions/2026-09-19-E041/main.py.
"""
import collections
import hashlib
import os
import sys
import time
import types

SEEDS = (0,)          # set at build: E041 network seeds averaged cellwise
CANDIDATES = {}       # set at build: instrument -> tuple of candidate chains
DIRECT = {}           # set at build: instrument -> chain applied without any guard (probes)
NO_E_CHECK = ()       # set at build: instruments whose best S chain is applied without the E test
EXPERT_ESTIMATORS = 8  # set at build: TabICL ensemble size
STRICT = True         # DEV builds: failures raise instead of falling back to E041
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

OPTIONS = dict(n_estimators=EXPERT_ESTIMATORS, norm_methods=["none", "power"],
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

FLOOR = 0.001
MARKERS = {"world_bank": ("user.lowestAcceptablePay", "user.wageOfSimilarEmployees"),
           "unicef": ("Country", "Q06", "Q18"),
           "unhcr": ("s3_11_intent_return_12m_lbl", "wave")}
STATS = collections.OrderedDict()
AGREE_MAX = float(os.environ.get("E069_AGREE_MAX", "0.95"))
PARENT_OLD = "s3_11_intent_return_12m_lbl"
PARENT_NEW = "s3_12_hope_return_someday_lbl"
BRANCHES = ("s7a_", "s7b_", "s7c_")
MIN_WAVE_ROWS = 300
SMOOTH = 20.0
LL_MARGIN = 0.01
LAST = {}
FAMILIES = ("s6_4_", "s6_6_", "s6_11_", "s7a_7_", "s7b_1_")
MIN_ROWS = 300


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


def _e041(frame, schema, seeds=(0,)):
    """E041 output, or the cellwise mean of E041 runs over SEEDS (network seed only).

    Averaging probabilities cannot lower the expected log score of a single run
    (Jensen), and the grader's floor is affine, so the bound survives flooring.
    """
    if tuple(seeds) == (0,):
        return e041_core.predict(frame, schema)
    runs = []
    original = e041_core.TORCH_SEED
    try:
        for seed in seeds:
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


def _instrument(schema):
    items = schema["items"]
    for name, markers in MARKERS.items():
        if all(marker in items for marker in markers):
            return name
    return None


def _seeds_for(name):
    """SEEDS is a tuple for every instrument or a dict instrument -> tuple (default (0,))."""
    if isinstance(SEEDS, dict):
        return tuple(SEEDS.get(name, (0,)))
    return tuple(SEEDS)


def _over_budget(fraction):
    return BUDGET_SECONDS is not None and time.monotonic() - _T0 > fraction * BUDGET_SECONDS


STACK_GRID = (0.0, 0.25, 0.5, 0.75, 1.0)
MAX_E_TESTS = 2


def _needs_expert(chain):
    return any(part.startswith(("mix", "conf", "sent", "stack")) for part in chain.split("+"))


def _temper(p, temperature):
    """Power-calibrate a distribution: p ** (1 / T), renormalized (T < 1 sharpens)."""
    q = np.power(_normalize(p), 1.0 / temperature)
    return q / q.sum(axis=1, keepdims=True)


def _stack_alphas(base, expert, idx, truth, heads, conf):
    """Per-head expert weight from STACK_GRID by floored log score on the selection rows."""
    alphas = {}
    for n in heads:
        b, q, y = base[n][idx], expert[n][idx], truth[n]
        rows = np.arange(len(y))
        best_a, best_v = 0.0, None
        for a in STACK_GRID:
            v = float(np.log(_floored(_mix(b, q, a, conf))[rows, y]).mean())
            if best_v is None or v > best_v + 1e-12:
                best_a, best_v = a, v
        alphas[n] = best_a
    return alphas


def _stack_oof(base, expert, idx, truth, heads, conf):
    """Two-fold out-of-fold S score for a per-head weight choice (removes selection optimism)."""
    half = len(idx) // 2
    folds = ((np.arange(half), np.arange(half, len(idx))), (np.arange(half, len(idx)), np.arange(half)))
    total, cells = 0.0, 0
    for fit, held_out in folds:
        alphas = _stack_alphas(base, expert, idx[fit], {n: truth[n][fit] for n in heads}, heads, conf)
        rows = np.arange(len(held_out))
        for n in heads:
            p = _floored(_mix(base[n][idx[held_out]], expert[n][idx[held_out]], alphas[n], conf))
            total += float(np.log(p[rows, truth[n][held_out]]).sum())
            cells += len(held_out)
    return total / cells


def _apply(chain, frame, schema, maps, expert, heads, options, stack=None):
    """Apply a '+'-joined transform chain to maps over the held rows of `frame`."""
    out = dict(maps)
    items = schema["items"]
    for part in chain.split("+"):
        if part.startswith("temp"):
            temperature = int(part[4:]) / 100.0
            out = {n: _temper(out[n], temperature) for n in heads}
        elif part in ("stack", "stackc"):
            alphas = stack[part]
            out = {n: _mix(out[n], expert[n], alphas[n], part == "stackc") for n in heads}
        elif part.startswith(("mix", "conf")):
            conf = part.startswith("conf")
            alpha = int(part[4:] if conf else part[3:]) / 100.0
            out = {n: _mix(out[n], expert[n], alpha, conf) for n in heads}
        elif part == "sent":
            visible, _ = _roles(frame, heads)
            for n in heads:
                if items[n].get("gate") and _gate_agreement(frame, schema, n, visible) < AGREE_MAX:
                    out[n] = _replace_sentinel(out[n], expert[n])
        elif part in ("regate", "transfer"):
            vectors = _flatten(out, heads)
            vectors = regate(frame, schema, vectors) if part == "regate" else transfer(frame, schema, vectors)
            out = _restore(vectors, heads, len(out[heads[0]]), options)
        else:
            raise ValueError("Unknown transform " + part)
    return out


def _guard(frame, schema, final_vectors, chains):
    """Choose at most one chain on S, confirm on E, then apply it to the final output."""
    given, heads, options = _layout(schema)
    visible, held = _roles(frame, heads)
    if len(held) == 0 or len(visible) < 2001 or not chains:
        STATS["guard"] = "skipped"
        return final_vectors
    order = np.random.Generator(np.random.PCG64(4501)).permutation(np.sort(visible))
    s_rows, e_rows = np.sort(order[:1000]), np.sort(order[1000:2000])
    f_rows = np.sort(order[2000:])
    shadow = frame.copy()
    shadow.loc[shadow.index[np.concatenate((s_rows, e_rows))], heads] = np.nan
    _, shadow_held = _roles(shadow, heads)
    started = time.monotonic()
    base = _restore(e041_core.predict(shadow, schema), heads, len(shadow_held), options)
    STATS["shadow_e041_seconds"] = round(time.monotonic() - started, 3)
    position = {row: i for i, row in enumerate(shadow_held)}
    idx_s = np.array([position[r] for r in s_rows])
    idx_e = np.array([position[r] for r in e_rows])
    expert = None
    if any(_needs_expert(c) for c in chains):
        if _over_budget(0.7):
            chains = tuple(c for c in chains if not _needs_expert(c))
            STATS["expert_skipped"] = "budget"
        else:
            started = time.monotonic()
            q = _expert(shadow, given, heads, options, f_rows, np.concatenate((s_rows, e_rows)))
            STATS["shadow_expert_seconds"] = round(time.monotonic() - started, 3)
            expert = {n: base[n].copy() for n in heads}
            for n in heads:
                expert[n][np.concatenate((idx_s, idx_e))] = q[n]
    if not chains:
        return final_vectors
    truth_s = {n: _labels(frame, s_rows, n, options) for n in heads}
    truth_e = {n: _labels(frame, e_rows, n, options) for n in heads}

    def logs(maps, idx, truth):
        return _cell_logs({n: maps[n][idx] for n in heads}, truth, heads)

    stack = {}
    for kind in ("stack", "stackc"):
        if expert is not None and any(kind in c.split("+") for c in chains):
            stack[kind] = _stack_alphas(base, expert, idx_s, truth_s, heads, kind == "stackc")
    reference_s = float(logs(base, idx_s, truth_s).mean())
    reference_e = logs(base, idx_e, truth_e).mean(axis=1)
    scores, transformed = {}, {}
    for chain in chains:
        transformed[chain] = _apply(chain, shadow, schema, base, expert, heads, options, stack)
        if chain in ("stack", "stackc"):
            scores[chain] = _stack_oof(base, expert, idx_s, truth_s, heads, chain == "stackc")
        else:
            scores[chain] = float(logs(transformed[chain], idx_s, truth_s).mean())
    ranked = [c for c in sorted(chains, key=lambda c: -scores[c]) if scores[c] > reference_s]
    record = dict(reference_s=reference_s, scores=scores,
                  stack={k: dict(collections.Counter(v.values())) for k, v in stack.items()})
    STATS["guard"] = record
    best = None
    if ranked and _instrument(schema) in NO_E_CHECK:
        best = ranked[0]
        record["e_check"] = "skipped"
    for chain in ([] if best else ranked[:MAX_E_TESTS]):
        d = logs(transformed[chain], idx_e, truth_e).mean(axis=1) - reference_e
        sd = float(d.std(ddof=1))
        lower = float(d.mean() - 1.645 * sd / np.sqrt(len(d))) if sd > 0 else float(d.mean())
        record.setdefault("e_tests", {})[chain] = lower
        if lower > 0:
            best = chain
            break
    record["accepted"] = best
    if best is None:
        return final_vectors
    final = _restore(final_vectors, heads, len(held), options)
    expert_final = None
    if _needs_expert(best):
        if _over_budget(0.85):
            record["final_skipped"] = "budget"
            return final_vectors
        started = time.monotonic()
        expert_final = _expert(frame, given, heads, options, visible, held)
        STATS["final_expert_seconds"] = round(time.monotonic() - started, 3)
    return _flatten(_apply(best, frame, schema, final, expert_final, heads, options, stack), heads)


def _direct(frame, schema, final_vectors, chain):
    """Probe: apply one non-stack chain to the final output with the expert fit on all visible rows."""
    given, heads, options = _layout(schema)
    visible, held = _roles(frame, heads)
    if len(held) == 0 or len(visible) < 2:
        return final_vectors
    final = _restore(final_vectors, heads, len(held), options)
    expert = None
    if _needs_expert(chain):
        started = time.monotonic()
        expert = _expert(frame, given, heads, options, visible, held)
        STATS["final_expert_seconds"] = round(time.monotonic() - started, 3)
    STATS["direct"] = chain
    return _flatten(_apply(chain, frame, schema, final, expert, heads, options), heads)


def _diagnostics(name, seconds):
    """Local rehearsal only: written when E065_DIAG is set; never on the platform."""
    path = os.environ.get("E065_DIAG")
    if not path:
        return
    import json
    record = dict(instrument=name, seeds=list(_seeds_for(name)), candidates=list(CANDIDATES.get(name, ())),
                  seconds=round(seconds, 3), since_import=round(time.monotonic() - _T0, 3), **STATS)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, default=str) + "\n")


def predict(frame, schema):
    started = time.monotonic()
    STATS.clear()
    name = _instrument(schema)
    vectors = _e041(frame, schema, _seeds_for(name))
    STATS["e041_seconds"] = round(time.monotonic() - started, 3)
    if name in DIRECT:
        vectors = _direct(frame, schema, vectors, DIRECT[name])
        _diagnostics(name, time.monotonic() - started)
        return vectors
    chains = tuple(CANDIDATES.get(name, ()))
    if chains and not _over_budget(0.75):
        if STRICT:
            vectors = _guard(frame, schema, vectors, chains)
        else:
            try:
                vectors = _guard(frame, schema, vectors, chains)
            except Exception:  # non-strict builds keep the seed-mean E041 output on any failure
                STATS["fallback"] = True
    _diagnostics(name or "other", time.monotonic() - started)
    return vectors
