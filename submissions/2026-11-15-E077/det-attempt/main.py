"""E073: E072 plus gradient-boosted tree experts (plain GIVEN and neighbour-answer features).

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
XSTACK_KINDS = ("g", "n")  # set at build: experts offered to the per-head multi-expert stack
XSTACK_BY = {}         # set at build: instrument -> experts offered there (overrides XSTACK_KINDS)
E_Z = 1.645            # set at build: one-sided normal quantile of the E-row confirmation
BASE_TREES = {}        # set at build: instrument -> weight of GIVEN-only trees inside E041's base
BASE_FOLDS = 5         # set at build: out-of-fold splits for the base trees on visible rows
HGB_THREADS = 8        # OpenMP cap for tree fitting (the hosted container has 8 CPUs)
HGB_OVERRIDE = {}      # set at build: tree parameters replacing the defaults (probes)
STRICT = True         # DEV builds: failures raise instead of falling back to E041
BUDGET_SECONDS = None  # optional wall-clock guard for non-strict builds

_T0 = time.monotonic()
_XSTACK_DEFAULT = tuple(XSTACK_KINDS)
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

import re  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import torch  # noqa: E402
from scipy.optimize import minimize  # noqa: E402
from scipy.special import softmax  # noqa: E402
from sklearn.ensemble import HistGradientBoostingClassifier  # noqa: E402
from threadpoolctl import threadpool_limits  # noqa: E402

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


HGB_PARAMS = dict(learning_rate=0.1, max_iter=120, max_leaf_nodes=15, min_samples_leaf=10,
                  l2_regularization=1.0, max_bins=255, early_stopping=True, validation_fraction=0.15,
                  n_iter_no_change=6, random_state=0)
HGB_SMOOTH = 0.002
NEIGHBORS = 3
_COUNT = re.compile(r"^(\d+)(?:-(\d+)|\+)?$")


def _given_codes(frame, schema, given):
    """Schema-order integer codes of the GIVEN block; values outside the schema become NaN."""
    items = schema["items"]
    columns = []
    for name in given:
        levels = list(items[name]["values"]) + ([schema["gated_value"]] if items[name].get("gate") else [])
        columns.append(frame[name].map({v: i for i, v in enumerate(levels)}).to_numpy(dtype=np.float64))
    return np.column_stack(columns)


def _count_value(level):
    match = _COUNT.match(str(level))
    if not match:
        return None
    low = float(match.group(1))
    if match.group(2):
        return (low + float(match.group(2))) / 2.0
    return low + 1.0 if str(level).endswith("+") else low


def _derived(frame, schema, given):
    """Totals over families of count-banded GIVEN columns (e.g. household roster counts)."""
    items = schema["items"]
    groups = {}
    for name in given:
        values = [_count_value(v) for v in items[name]["values"]]
        if values and all(v is not None for v in values):
            groups.setdefault("_".join(name.split("_")[:2]), []).append(name)
    columns = []
    for members in groups.values():
        if len(members) < 4:
            continue
        numeric = {name: frame[name].map({v: _count_value(v) for v in items[name]["values"]})
                   .to_numpy(dtype=np.float64) for name in members}
        columns.append(np.nansum([numeric[n] for n in members], axis=0))
        young = [n for n in members if "boys" in n or "girls" in n]
        if young and len(young) < len(members):
            columns.append(np.nansum([numeric[n] for n in young], axis=0))
    return np.column_stack(columns) if columns else None


def _signature(frame, given):
    """Factorized GIVEN codes and rarity weights (-log of the random-agreement rate)."""
    codes = np.empty((len(frame), len(given)), dtype=np.int32)
    weights = np.empty(len(given))
    for j, name in enumerate(given):
        values = frame[name].astype(object).where(frame[name].notna(), "__NA__")
        codes[:, j] = pd.factorize(values)[0]
        share = np.bincount(codes[:, j]) / len(frame)
        weights[j] = -np.log(np.clip((share ** 2).sum(), 1e-6, 1.0))
    return codes, weights


def _top_neighbors(codes, weights, query, pool, k=NEIGHBORS, chunk=256):
    """Top-k pool rows per query by rarity-weighted GIVEN agreement; a row never matches itself."""
    query, pool = np.asarray(query, dtype=np.int64), np.asarray(pool, dtype=np.int64)
    pool_codes = codes[pool]
    where = {int(p): i for i, p in enumerate(pool)}
    k = max(1, min(k, len(pool) - 1))
    index = np.empty((len(query), k), dtype=np.int64)
    score = np.empty((len(query), k))
    count = np.empty((len(query), k))
    for start in range(0, len(query), chunk):
        rows = query[start:start + chunk]
        s = np.zeros((len(rows), len(pool)), dtype=np.float32)
        c = np.zeros((len(rows), len(pool)), dtype=np.int16)
        for j, weight in enumerate(weights):
            equal = codes[rows, j][:, None] == pool_codes[None, :, j]
            s += np.float32(weight) * equal
            c += equal
        for i, row in enumerate(rows):
            self_i = where.get(int(row))
            if self_i is not None:
                s[i, self_i] = -np.inf
        part = np.argpartition(-s, k - 1, axis=1)[:, :k]
        for i in range(len(rows)):
            chosen = part[i][np.lexsort((pool[part[i]], -s[i, part[i]]))]
            index[start + i] = pool[chosen]
            score[start + i] = s[i, chosen]
            count[start + i] = c[i, chosen]
    return index, score, count


def _match_weights(codes, rarity, pool, sample=3000, min_pairs=30, pair_mass=0.5):
    """Fellegi-Sunter agreement weights from provisional top-1 pairs (the E021 rule that E025/E041
    use for their donor evidence); rarity weights when too few concentrated pairs exist."""
    pool = np.asarray(pool, dtype=np.int64)
    queries = pool
    if len(queries) > sample:
        queries = np.sort(np.random.default_rng(0).choice(pool, sample, replace=False))
    index, score, _ = _top_neighbors(codes, rarity, queries, pool, k=10)
    mass = np.exp(score - score.max(axis=1, keepdims=True))
    mass = mass / mass.sum(axis=1, keepdims=True)
    paired = mass[:, 0] >= pair_mass
    if int(paired.sum()) < min_pairs:
        return rarity
    agree = (codes[queries[paired]] == codes[index[paired, 0]]).mean(axis=0)
    n = int(paired.sum())
    m = np.clip((agree * n + 1.0) / (n + 2.0), 1e-4, 1.0 - 1e-4)
    u = np.clip(np.exp(-rarity), 1e-4, 1.0 - 1e-4)
    weights = np.maximum(np.log(m / u) - np.log((1.0 - m) / (1.0 - u)), 0.0)
    return weights if weights.sum() > 0 else rarity


def _fit_hgb(x_context, y, x_query, categorical, width):
    present = np.bincount(y, minlength=width)
    marginal = (present + 0.5) / (present + 0.5).sum()
    if (present > 0).sum() == 1:
        return np.tile(marginal, (len(x_query), 1))
    params = dict(HGB_PARAMS)
    params.update(HGB_OVERRIDE)
    if present[present > 0].min() < 8:
        params.update(early_stopping=False, max_iter=40)
    try:
        model = HistGradientBoostingClassifier(categorical_features=categorical, **params).fit(x_context, y)
    except ValueError:
        params.update(early_stopping=False, max_iter=40)
        model = HistGradientBoostingClassifier(categorical_features=categorical, **params).fit(x_context, y)
    raw = np.asarray(model.predict_proba(x_query), dtype=np.float64)
    if not np.isfinite(raw).all() or (raw < 0).any() or (raw.sum(axis=1) <= 0).any():
        raise ValueError("Invalid tree distribution")
    p = np.zeros((len(x_query), width))
    p[:, np.asarray(model.classes_).astype(int)] = _normalize(raw)
    return (1.0 - HGB_SMOOTH) * p + HGB_SMOOTH * marginal


VOTE_NEIGHBORS = 10


def _votes(answers, near, score, width):
    """Posterior-weighted class shares among the nearest rows (softmax of the match scores,
    the same kernel E025/E041 use for donor evidence)."""
    weight = np.exp(score - score.max(axis=1, keepdims=True))
    weight = weight / weight.sum(axis=1, keepdims=True)
    out = np.zeros((len(near), width))
    rows = np.repeat(np.arange(len(near)), near.shape[1])
    np.add.at(out, (rows, answers[near].ravel()), weight.ravel())
    return out


RETRIEVAL_TOP = 3
PAIR_STRONG = 5.0   # robust z of a labelled row's best answer agreement among its nearest labelled rows
PAIR_WEAK = 3.5
PAIR_LEVELS = (2.5, PAIR_WEAK, PAIR_STRONG)


def _pair_flags(score):
    """Graded donor-only metric fields from a pairing z-score: per level "no twin among the
    labelled rows at this level" (their non-negative weights add up to a monotone bonus for
    unpaired donors) and one field "has a twin" for the opposite, cluster-like case."""
    return np.stack([score < level for level in PAIR_LEVELS] + [score >= PAIR_LEVELS[-1]], axis=-1)


def _pair_scores(codes, weights, labels, bank):
    """Per bank row: robust z-scores of the best and second-best answer agreement with its
    GIVEN-nearest bank rows (median / MAD over those rows) and the frame position of the best
    one. A high z marks a labelled row whose twin is already among the labelled rows."""
    bank = np.sort(np.asarray(bank, dtype=np.int64))
    donors = e041_core.candidate_indices(codes, weights, bank, bank, k=e041_core.RETRIEVAL_K)
    best, second = np.zeros(len(bank)), np.zeros(len(bank))
    partner = np.full(len(bank), -1, dtype=np.int64)
    if donors.shape[1] >= 4:
        for start in range(0, len(bank), 256):
            block = slice(start, start + 256)
            agreement = (labels[bank[block], None, :] == labels[donors[block]]).mean(axis=2)
            center = np.median(agreement, axis=1)
            spread = 1.4826 * np.median(np.abs(agreement - center[:, None]), axis=1) + 0.01
            order = np.argsort(-agreement, axis=1)
            rows = np.arange(agreement.shape[0])
            best[block] = (agreement[rows, order[:, 0]] - center) / spread
            second[block] = (agreement[rows, order[:, 1]] - center) / spread
            partner[block] = donors[block][rows, order[:, 0]]
    return bank, best, second, partner


def _retrieval_features(frame, schema, heads, options, context, query, pairing=False):
    """E041's supervised section metrics, refitted on the context rows, as per-head tree features:
    donor-weighted class shares under the learned and under the initial metric (E041's 32
    candidates, self excluded for context rows) plus the weights and answers of the three
    heaviest donors. Labels of query rows are never read."""
    core = e041_core
    records, items, _ = core._layout(frame, schema)
    codes, rarity = core._sig_data_all(frame, records, items)
    cal = context
    if len(cal) > core.CAL_QUERIES:
        cal = np.sort(np.random.default_rng(core.CAL_SEED).choice(cal, core.CAL_QUERIES, replace=False))
    initial, _ = core.estimate_weights(codes, rarity, cal, core._topk_excl(codes, rarity, cal, context))
    initial = np.maximum(np.asarray(initial, dtype=np.float64), 0.0)
    labels = np.full((len(frame), len(heads)), -1, dtype=np.int64)
    for j, name in enumerate(heads):
        labels[context, j] = _labels(frame, context, name, options)
    shuffled = np.random.default_rng(4101).permutation(context)
    nfit = min(core.FIT_QUERIES, max(1, len(context) // 5))
    nselect = min(core.SELECT_QUERIES, max(1, len(context) // 10))
    groups = core._groups(heads)
    sizes = [len(options[n]) for n in heads]
    fit_codes, fit_initial = codes, initial
    if pairing:   # donor-only metric fields from the pairing score (weights learned, start 0)
        bank, best, _, _ = _pair_scores(codes, initial, labels, shuffled[nfit + nselect:])
        flags = np.ones((len(frame), len(PAIR_LEVELS) + 1), dtype=codes.dtype)   # non-bank rows compare equal to 1
        flags[bank] = _pair_flags(best)
        fit_codes = np.hstack((codes, flags))
        fit_initial = np.concatenate((initial, np.zeros(flags.shape[1])))
    learned, _, _ = core.fit_sections(fit_codes, labels, shuffled[nfit + nselect:], shuffled[:nfit],
                                      shuffled[nfit:nfit + nselect], fit_initial, sizes, groups)
    rows = np.concatenate((context, query))
    donors = core.candidate_indices(codes, initial, rows, context, k=core.RETRIEVAL_K)
    agree = (codes[rows, None, :] == codes[donors]).astype(np.float64)
    post_i = softmax(agree @ initial, axis=1)
    paired = None
    if pairing:   # the donor's pairing is judged without the row that is asking (leave-one-out)
        bank, best, second, partner = _pair_scores(codes, initial, labels, context)
        full_best, full_second = np.zeros(len(frame)), np.zeros(len(frame))
        full_partner = np.full(len(frame), -1, dtype=np.int64)
        full_best[bank], full_second[bank], full_partner[bank] = best, second, partner
        paired = np.where(full_partner[donors] == rows[:, None], full_second[donors], full_best[donors])
        agree = np.concatenate((agree, _pair_flags(paired).astype(np.float64)), axis=2)
    blocks = {}
    for g, members in enumerate(groups):
        post_l = softmax(agree @ learned[g], axis=1)
        top = np.argsort(-post_l, axis=1)[:, :RETRIEVAL_TOP]
        weight_top = np.take_along_axis(post_l, top, axis=1)
        for j in members:
            answers = labels[donors, j]
            share_l = np.stack([(post_l * (answers == c)).sum(axis=1) for c in range(sizes[j])], axis=1)
            share_i = np.stack([(post_i * (answers == c)).sum(axis=1) for c in range(sizes[j])], axis=1)
            parts = [share_l, share_i, weight_top]
            if paired is not None:
                parts.append(np.clip(np.take_along_axis(paired, top, axis=1), -3.0, 12.0))
            parts.append(np.take_along_axis(answers, top, axis=1).astype(np.float64))
            blocks[heads[j]] = np.column_stack(parts)
    cut = len(context)
    return {"c": {n: b[:cut] for n, b in blocks.items()}, "q": {n: b[cut:] for n, b in blocks.items()},
            "cat": {n: [False] * (b.shape[1] - top.shape[1]) + [True] * top.shape[1] for n, b in blocks.items()}}


def _expert_hgb(frame, schema, given, heads, options, context, query, neighbors, votes=0, retrieval=None):
    """Per-head boosted trees on GIVEN (+ roster totals); optionally the answers and match
    scores of the nearest labelled context rows (leave-one-out for context rows), and with
    votes > 0 also the weighted class shares among that many nearest rows."""
    context, query = np.asarray(context, dtype=np.int64), np.asarray(query, dtype=np.int64)
    coded = _given_codes(frame, schema, given)
    blocks_c, blocks_q = [coded[context]], [coded[query]]
    categorical = [True] * coded.shape[1]
    extra = _derived(frame, schema, given)
    if extra is not None:
        blocks_c.append(extra[context])
        blocks_q.append(extra[query])
        categorical += [False] * extra.shape[1]
    if neighbors:
        codes, rarity = _signature(frame, given)
        weights = _match_weights(codes, rarity, context)
        wide = max(NEIGHBORS, votes)
        wide_c = _top_neighbors(codes, weights, context, context, k=wide)
        wide_q = _top_neighbors(codes, weights, query, context, k=wide)
        near_c, score_c, count_c = (a[:, :NEIGHBORS] for a in wide_c)
        near_q, score_q, count_q = (a[:, :NEIGHBORS] for a in wide_q)
        blocks_c += [score_c, count_c, (codes[context] == codes[near_c[:, 0]]).astype(np.float64)]
        blocks_q += [score_q, count_q, (codes[query] == codes[near_q[:, 0]]).astype(np.float64)]
        categorical += [False] * (score_c.shape[1] + count_c.shape[1] + codes.shape[1])
    x_context, x_query = np.column_stack(blocks_c), np.column_stack(blocks_q)
    maps = {}
    with threadpool_limits(limits=HGB_THREADS, user_api="openmp"):
        for name in heads:
            y = _labels(frame, context, name, options)
            width = len(options[name])
            if neighbors:
                answers = np.full(len(frame), -1, dtype=np.int64)
                answers[context] = y
                parts_c = [x_context, answers[near_c].astype(np.float64)]
                parts_q = [x_query, answers[near_q].astype(np.float64)]
                kinds = categorical + [True] * near_c.shape[1]
                if votes:
                    parts_c.append(_votes(answers, wide_c[0], wide_c[1], width))
                    parts_q.append(_votes(answers, wide_q[0], wide_q[1], width))
                    kinds = kinds + [False] * width
                if retrieval is not None:
                    parts_c.append(retrieval["c"][name])
                    parts_q.append(retrieval["q"][name])
                    kinds = kinds + retrieval["cat"][name]
                maps[name] = _fit_hgb(np.column_stack(parts_c), y, np.column_stack(parts_q), kinds, width)
            else:
                maps[name] = _fit_hgb(x_context, y, x_query, categorical, width)
    return maps


def _fit_expert(kind, frame, schema, given, heads, options, context, query):
    """t = TabICLv2, g = boosted trees on GIVEN, n = + answers of the three nearest rows,
    m = n + soft votes of the ten nearest rows."""
    if kind == "t":
        return _expert(frame, given, heads, options, context, query)
    if kind in ("r", "q"):   # m plus E041's supervised retrieval as features (q: pairing-aware)
        context = np.sort(np.asarray(context, dtype=np.int64))
        query = np.asarray(query, dtype=np.int64)
        retrieval = _retrieval_features(frame, schema, heads, options, context, query, pairing=kind == "q")
        return _expert_hgb(frame, schema, given, heads, options, context, query, neighbors=True,
                           votes=VOTE_NEIGHBORS, retrieval=retrieval)
    return _expert_hgb(frame, schema, given, heads, options, context, query,
                       neighbors=(kind in ("n", "m")), votes=(VOTE_NEIGHBORS if kind == "m" else 0))


def _split(part):
    """(expert kind, operation) of a chain part; TabICL is the default expert."""
    if part[:1] in ("g", "n", "m", "r", "q") and part[1:].startswith(("mix", "conf", "stack", "sent", "lpool")):
        return part[0], part[1:]
    return "t", part


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


def _all_row_trees(frame, schema, given, heads, options, visible, held, folds=None):
    """GIVEN-only tree distributions for every row: out-of-fold for visible rows (so the
    lambda replay inside E041 sees honest base predictions), all-visible fit for held rows."""
    folds = BASE_FOLDS if folds is None else folds
    out = {name: np.zeros((len(frame), len(options[name]))) for name in heads}
    parts = np.array_split(np.random.Generator(np.random.PCG64(4502)).permutation(visible), folds)
    for k in range(folds):
        test = np.sort(parts[k])
        train = np.sort(np.concatenate([parts[j] for j in range(folds) if j != k]))
        q = _expert_hgb(frame, schema, given, heads, options, train, test, neighbors=False)
        for name in heads:
            out[name][test] = q[name]
    q = _expert_hgb(frame, schema, given, heads, options, visible, held, neighbors=False)
    for name in heads:
        out[name][held] = q[name]
    return out


def _e041_tree_base(frame, schema, weight, seeds):
    """E041 with its network probabilities replaced by (1 - weight) * network + weight * trees
    before the ladder mix, gate coupling, donor-evidence replay and rendering."""
    given, heads, options = _layout(schema)
    visible, held = _roles(frame, heads)
    if len(held) == 0 or len(visible) < 50:
        return _e041(frame, schema, seeds)
    started = time.monotonic()
    trees = _all_row_trees(frame, schema, given, heads, options, visible, held)
    STATS["base_trees_seconds"] = round(time.monotonic() - started, 3)
    original = e041_core._proba_maps
    n_rows = len(frame)

    def mixed(net, x_all, predict_items, gated_items):
        full, cond = original(net, x_all, predict_items, gated_items)
        if x_all.shape[0] != n_rows:
            return full, cond          # holdout-only call inside tune_and_train stays the pure network
        for item in predict_items:
            full[item] = (1.0 - weight) * full[item] + weight * trees[item]
        for item in gated_items:
            content = trees[item][:, :-1]
            total = content.sum(axis=1, keepdims=True)
            tree_cond = np.where(total > 1e-9, content / np.where(total > 1e-9, total, 1.0), cond[item])
            cond[item] = (1.0 - weight) * cond[item] + weight * tree_cond
        STATS["base_trees_applied"] = STATS.get("base_trees_applied", 0) + 1
        return full, cond

    e041_core._proba_maps = mixed
    try:
        return _e041(frame, schema, seeds)
    finally:
        e041_core._proba_maps = original


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
    """Expert kinds a chain uses (empty set when it needs none)."""
    kinds = set()
    for part in chain.split("+"):
        if part in ("xstack", "xstackc", "xlpool", "xlpoolh"):
            kinds.update(XSTACK_KINDS)
        elif part in ("twin", "twinh"):
            kinds.add("w")
        elif _split(part)[1].startswith(("mix", "conf", "sent", "stack", "lpool")):
            kinds.add(_split(part)[0])
    return kinds


CAL_EDGES = np.array([0.5, 0.7, 0.8, 0.9, 0.95, 0.98, 0.99, 0.995, 0.999])
CAL_PRIOR = 50.0      # pseudo-cells pulling each bin toward its stated confidence
CAL_CAP = 1.0 - 1e-4


def _cal_fit(maps, idx, truth, heads):
    """Reliability map of the top-class probability on the rows idx: per confidence bin above .5,
    (mean stated confidence, smoothed observed accuracy), made monotone and anchored at (.5, .5)."""
    tops, hits = [], []
    for n in heads:
        p = _normalize(maps[n][idx])
        if p.shape[1] < 2:
            continue
        top = p.argmax(axis=1)
        tops.append(p[np.arange(len(top)), top])
        hits.append(top == truth[n])
    if not tops:
        return np.array([0.5]), np.array([0.5])
    tops, hits = np.concatenate(tops), np.concatenate(hits).astype(np.float64)
    which = np.digitize(tops, CAL_EDGES)
    xs, ys = [0.5], [0.5]
    for b in range(1, len(CAL_EDGES) + 1):
        sel = which == b
        if not sel.any():
            continue
        stated = float(tops[sel].mean())
        xs.append(stated)
        ys.append(float((hits[sel].sum() + CAL_PRIOR * stated) / (sel.sum() + CAL_PRIOR)))
    return np.array(xs), np.minimum(np.maximum.accumulate(np.array(ys)), CAL_CAP)


def _cal_apply(maps, params, heads):
    """Move the top-class probability onto the fitted reliability curve (only where it is at
    least .5); the remaining classes keep their proportions."""
    xs, ys = params
    if len(xs) < 2:
        return maps
    out = {}
    for n in heads:
        p = _normalize(maps[n])
        if p.shape[1] < 2:
            out[n] = p
            continue
        rows = np.arange(len(p))
        top = p.argmax(axis=1)
        p_top = p[rows, top]
        new = np.where(p_top >= 0.5, np.clip(np.interp(p_top, xs, ys), 0.5, CAL_CAP), p_top)
        rest = 1.0 - p_top
        thin = rest <= 1e-12
        q = p * np.where(thin, 0.0, (1.0 - new) / np.where(thin, 1.0, rest))[:, None]
        if thin.any():
            q[thin] = ((1.0 - new[thin]) / (p.shape[1] - 1))[:, None]
        q[rows, top] = new
        out[n] = q
    return out


POOL_BOUNDS = (0.0, 3.0)
POOL_RIDGE = 0.02
LOG_EPS = 1e-6


def _clog(p):
    return np.log(np.clip(_normalize(p), LOG_EPS, 1.0))


def _pool(logs, weights):
    """Log-linear pool: p proportional to prod_j p_j ** w_j (first entry is the base model)."""
    z = weights[0] * logs[0]
    for w, part in zip(weights[1:], logs[1:]):
        z = z + w * part
    z = z - z.max(axis=1, keepdims=True)
    p = np.exp(z)
    return p / p.sum(axis=1, keepdims=True)


def _pool_fit(log_sets, truths, start, anchor=None, ridge=0.0):
    """Exponents maximizing the mean log-likelihood of the pooled distribution (concave problem:
    multinomial logistic regression on log-probabilities), optionally shrunk toward `anchor`."""
    start = np.asarray(start, dtype=np.float64)
    cells = float(sum(len(y) for y in truths))

    def objective(w):
        value, grad = 0.0, np.zeros(len(w))
        for logs, y in zip(log_sets, truths):
            p = _pool(logs, w)
            rows = np.arange(len(y))
            value += float(np.log(np.maximum(p[rows, y], 1e-300)).sum())
            for j, part in enumerate(logs):
                grad[j] += float((part[rows, y] - (p * part).sum(axis=1)).sum())
        value, grad = value / cells, grad / cells
        if ridge and anchor is not None:
            diff = w - anchor
            value -= ridge * float(diff @ diff)
            grad = grad - 2.0 * ridge * diff
        return -value, -grad

    result = minimize(objective, start, jac=True, method="L-BFGS-B",
                      bounds=[POOL_BOUNDS] * len(start), options={"maxiter": 60})
    return result.x if np.isfinite(result.x).all() else start


POOL_ONLY_BASE = ("tpool", "tpoolh")   # exponent on the base model alone (learned temperature)


def _pool_kinds(raw_part, experts):
    if raw_part in POOL_ONLY_BASE:
        return []
    if raw_part.startswith("x"):
        return [k for k in XSTACK_KINDS if k in experts]
    return [_split(raw_part)[0]]


def _pool_params(raw_part, base, experts, idx, truth, heads):
    """Global exponents fitted on the rows idx; for the 'h' variant also per-head exponents
    shrunk toward the global ones. Starting point (1, 0, ...) is the base model itself."""
    kinds = _pool_kinds(raw_part, experts)
    sets = [[_clog(base[n][idx])] + [_clog(experts[k][n][idx]) for k in kinds] for n in heads]
    ys = [truth[n] for n in heads]
    start = np.array([1.0] + [0.0] * len(kinds))
    overall = _pool_fit(sets, ys, start)
    params = {"kinds": kinds, "global": overall}
    if raw_part.endswith("h"):
        params["heads"] = {n: _pool_fit([logs], [y], overall, anchor=overall, ridge=POOL_RIDGE)
                           for n, logs, y in zip(heads, sets, ys)}
    return params


def _pool_apply(maps, experts, params, heads):
    out = {}
    for n in heads:
        weights = params.get("heads", {}).get(n, params["global"])
        out[n] = _pool([_clog(maps[n])] + [_clog(experts[k][n]) for k in params["kinds"]], weights)
    return out


def _pool_oof(raw_part, base, experts, idx, truth, heads):
    """Two-fold out-of-fold S score of a pooled chain (fit exponents on one half, score the other)."""
    half = len(idx) // 2
    folds = ((np.arange(half), np.arange(half, len(idx))), (np.arange(half, len(idx)), np.arange(half)))
    total, cells = 0.0, 0
    for fit, held_out in folds:
        params = _pool_params(raw_part, base, experts, idx[fit], {n: truth[n][fit] for n in heads}, heads)
        rows = np.arange(len(held_out))
        sub_base = {n: base[n][idx[held_out]] for n in heads}
        sub_experts = {k: {n: experts[k][n][idx[held_out]] for n in heads} for k in params["kinds"]}
        pooled = _pool_apply(sub_base, sub_experts, params, heads)
        for n in heads:
            total += float(np.log(_floored(pooled[n])[rows, truth[n][held_out]]).sum())
            cells += len(held_out)
    return total / cells


def _xstack_choice(base, experts, idx, truth, heads, conf):
    """Per head: the (expert kind, weight) with the best floored log score on the rows idx;
    ("", 0.0) keeps the base."""
    choice = {}
    for n in heads:
        b, y = base[n][idx], truth[n]
        rows = np.arange(len(y))
        best = ("", 0.0, float(np.log(_floored(b)[rows, y]).mean()))
        for kind in XSTACK_KINDS:
            if kind not in experts:
                continue
            q = experts[kind][n][idx]
            for a in STACK_GRID[1:]:
                v = float(np.log(_floored(_mix(b, q, a, conf))[rows, y]).mean())
                if v > best[2] + 1e-12:
                    best = (kind, a, v)
        choice[n] = best[:2]
    return choice


def _xstack_oof(base, experts, idx, truth, heads, conf):
    """Two-fold out-of-fold S score of the per-head multi-expert choice."""
    half = len(idx) // 2
    folds = ((np.arange(half), np.arange(half, len(idx))), (np.arange(half, len(idx)), np.arange(half)))
    total, cells = 0.0, 0
    for fit, held_out in folds:
        choice = _xstack_choice(base, experts, idx[fit], {n: truth[n][fit] for n in heads}, heads, conf)
        rows = np.arange(len(held_out))
        for n in heads:
            kind, a = choice[n]
            b = base[n][idx[held_out]]
            p = _floored(_mix(b, experts[kind][n][idx[held_out]], a, conf) if kind else b)
            total += float(np.log(p[rows, truth[n][held_out]]).sum())
            cells += len(held_out)
    return total / cells


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


TWIN_NEIGHBORS = 5
TWIN_MAX = 0.9995         # ceiling of the copy share
TWIN_START = -4.0         # cautious start: a constant share of about .018
TWIN_FIELD_START = -3.0   # second start: each disagreeing field cuts the odds of copying
TWIN_RIDGE = 0.002        # on the match-quality coefficients
TWIN_HEAD_RIDGE = 0.005   # on the per-head shifts
TWIN_PARTS = ("twin", "twinh")


def _twin_evidence(frame, given, heads, options, context, query):
    """Answers of the best-matching labelled rows of each query row (ties share the weight) and
    label-free features of that match: per-field disagreement with the best row, how many
    labelled rows agree on the whole GIVEN block, and how alike the two best rows answer."""
    context, query = np.asarray(context, dtype=np.int64), np.asarray(query, dtype=np.int64)
    codes, rarity = _signature(frame, given)
    weights = _match_weights(codes, rarity, context)
    index, score, count = _top_neighbors(codes, weights, query, context, k=TWIN_NEIGHBORS)
    tied = score >= score[:, :1] - 1e-6
    share = tied / tied.sum(axis=1, keepdims=True)
    rows = np.repeat(np.arange(len(query)), index.shape[1])
    answers = np.zeros((len(frame), len(heads)), dtype=np.int64)
    evidence = {}
    for j, name in enumerate(heads):
        answers[context, j] = _labels(frame, context, name, options)
        mat = np.zeros((len(query), len(options[name])))
        np.add.at(mat, (rows, answers[index, j].ravel()), share.ravel())
        evidence[name] = mat
    exact = (count >= codes.shape[1]).sum(axis=1)
    if index.shape[1] > 1:
        same = (answers[index[:, 0]] == answers[index[:, 1]]).mean(axis=1)
    else:
        same = np.zeros(len(query))
    pair = (exact >= 2).astype(np.float64)
    features = np.column_stack((
        (codes[query] != codes[index[:, 0]]).astype(np.float64),
        pair, (exact >= 3).astype(np.float64), same, pair * same, pair * (same >= 0.98),
        (tied.sum(axis=1) > 1).astype(np.float64)))
    return {"ev": evidence, "x": features, "fields": codes.shape[1]}


def _twin_share(z):
    return TWIN_MAX / (1.0 + np.exp(-np.clip(z, -30.0, 30.0)))


def _twin_fit(maps, twin, idx, truth, heads, per_head):
    """Copy share r = TWIN_MAX * sigmoid(a + x.g [+ d_head]) maximizing the officially floored
    log-likelihood of (1 - r) * current + r * twin evidence on the rows idx. The start is a
    small constant share; x are the label-free match features of the row."""
    rows = np.arange(len(idx))
    base, ev, width, head = [], [], [], []
    for j, name in enumerate(heads):
        p = _normalize(maps[name][idx])
        base.append(p[rows, truth[name]])
        ev.append(twin["ev"][name][idx][rows, truth[name]])
        width.append(np.full(len(idx), float(p.shape[1])))
        head.append(np.full(len(idx), j))
    base, ev, width, head = (np.concatenate(a) for a in (base, ev, width, head))
    row = np.tile(rows, len(heads))
    x = twin["x"][idx]
    m, h, fields = x.shape[1], len(heads), twin["fields"]
    scale = 1.0 - FLOOR * width

    def objective(theta):
        g, d = theta[1:1 + m], theta[1 + m:]
        z = theta[0] + (x @ g)[row] + (d[head] if per_head else 0.0)
        r = _twin_share(z)
        lik = FLOOR + scale * ((1.0 - r) * base + r * ev)
        dz = scale * (ev - base) * r * (1.0 - r / TWIN_MAX) / lik / len(lik)
        value = float(np.log(lik).mean()) - TWIN_RIDGE * float(g @ g)
        grad = [np.array([dz.sum()]), x.T @ np.bincount(row, weights=dz, minlength=len(x)) - 2.0 * TWIN_RIDGE * g]
        if per_head:
            value -= TWIN_HEAD_RIDGE * float(d @ d) / h
            grad.append(np.bincount(head, weights=dz, minlength=h) - 2.0 * TWIN_HEAD_RIDGE * d / h)
        return -value, -np.concatenate(grad)

    size = 1 + m + (h if per_head else 0)
    cautious = np.zeros(size)
    cautious[0] = TWIN_START
    exact = np.zeros(size)          # trust rows whose best match agrees on every GIVEN field
    exact[0] = 1.0
    exact[1:1 + fields] = TWIN_FIELD_START
    theta, best = cautious, np.inf
    for start in (cautious, exact):
        result = minimize(objective, start, jac=True, method="L-BFGS-B",
                          bounds=[(-12.0, 12.0)] * size, options={"maxiter": 100})
        if np.isfinite(result.x).all() and result.fun < best:
            theta, best = result.x, float(result.fun)
    return {"a": float(theta[0]), "g": theta[1:1 + m].copy(), "d": theta[1 + m:].copy()}


def _twin_apply(maps, twin, params, heads):
    out = {}
    z = params["a"] + twin["x"] @ params["g"]
    for j, name in enumerate(heads):
        r = _twin_share(z + (params["d"][j] if len(params["d"]) else 0.0))[:, None]
        p, ev = _normalize(maps[name]), twin["ev"][name]
        out[name] = np.where(ev.sum(axis=1, keepdims=True) > 0, (1.0 - r) * p + r * ev, p)
    return out


DET_MIN_ROWS = 200        # labelled rows a GIVEN stratum needs
DET_MIN_EXPECTED = 30.0   # expected count of the unseen side in the stratum at the instrument-wide rate
DET_UPPER = 3.0           # "rule of three": 95 % upper bound on the rate of an event unseen in n rows
_DET_CACHE = {}


def _det_bounds(frame, schema, heads, options):
    """Routing exclusions read off the labelled rows, for gated heads only. Where at least
    DET_MIN_ROWS labelled rows share one GIVEN value (or one pair of GIVEN values) and every one
    of them carries the gate value (never asked there), or none does (always asked), although
    the other side would be expected DET_MIN_EXPECTED times at the instrument-wide rate, the
    gate-value probability of held rows in that stratum is bounded below by
    1 - DET_UPPER / (n + 2), respectively above by DET_UPPER / (n + 2). Labels of held rows are
    never read. Returns {head: (lower, upper)} per held row for heads with at least one bound."""
    key = id(frame)
    if key in _DET_CACHE:
        return _DET_CACHE[key]
    given, _, _ = _layout(schema)
    items = schema["items"]
    visible, held = _roles(frame, heads)
    bounds = {}
    if len(held) and len(visible) >= DET_MIN_ROWS and given:
        codes = []
        for column in given:
            values = frame[column].astype(object).where(frame[column].notna(), "__NA__")
            codes.append(pd.factorize(values)[0].astype(np.int64))
        strata = [(code, int(code.max()) + 1) for code in codes]
        for a in range(len(codes)):
            for b in range(a + 1, len(codes)):
                width = int(codes[b].max()) + 1
                strata.append((codes[a] * width + codes[b], (int(codes[a].max()) + 1) * width))
        usable = []
        for code, size in strata:
            counts = np.bincount(code[visible], minlength=size)
            if (counts >= DET_MIN_ROWS).any():
                usable.append((code[visible], code[held], size, counts))
        total = 0
        for name in heads:
            if not items[name].get("gate"):
                continue
            skipped = _labels(frame, visible, name, options) == len(options[name]) - 1
            rate = float(skipped.mean())
            lower, upper = np.zeros(len(held)), np.ones(len(held))
            for vis_code, held_code, size, counts in usable:
                hits = np.bincount(vis_code[skipped], minlength=size)
                big = counts >= DET_MIN_ROWS
                never_asked = big & (hits == counts) & (counts * (1.0 - rate) >= DET_MIN_EXPECTED)
                always_asked = big & (hits == 0) & (counts * rate >= DET_MIN_EXPECTED)
                if never_asked.any():
                    lower = np.maximum(lower, np.where(never_asked, 1.0 - DET_UPPER / (counts + 2.0), 0.0)[held_code])
                if always_asked.any():
                    upper = np.minimum(upper, np.where(always_asked, DET_UPPER / (counts + 2.0), 1.0)[held_code])
            active = (lower > 0.0) | (upper < 1.0)
            if active.any():
                bounds[name] = (lower, upper)
                total += int(active.sum())
        STATS.setdefault("det_bounded_cells", []).append(total)
    _DET_CACHE[key] = bounds
    return bounds


def _det_apply(frame, schema, maps, heads, options):
    """Move the gate-value probability inside its bounds; the asked answers keep their
    proportions. Rows inside their bounds, and rows whose bounds contradict each other, are
    returned bit for bit."""
    bounds = _det_bounds(frame, schema, heads, options)
    out = dict(maps)
    for name in heads:
        if name not in bounds:
            continue
        lower, upper = bounds[name]
        p = _normalize(maps[name])
        gate = p[:, -1]
        target = np.where(lower <= upper, np.clip(gate, lower, upper), gate)
        moved = np.flatnonzero(target != gate)
        if len(moved) == 0:
            continue
        q = np.array(maps[name], dtype=np.float64, copy=True)
        content = p[moved, :-1]
        mass = content.sum(axis=1, keepdims=True)
        share = np.where(mass > 0, content / np.where(mass > 0, mass, 1.0), 1.0 / content.shape[1])
        q[moved, :-1] = share * (1.0 - target[moved])[:, None]
        q[moved, -1] = target[moved]
        out[name] = q
    return out


def _apply(chain, frame, schema, maps, experts, heads, options, stack=None, fit=None):
    """Apply a '+'-joined transform chain to maps over the held rows of `frame`.
    fit = (row positions, truth) makes data-fitted parts (cal) estimate and store their
    parameters in `stack`; without it they reuse the stored ones."""
    out = dict(maps)
    items = schema["items"]
    for raw_part in chain.split("+"):
        kind, part = _split(raw_part)
        expert = (experts or {}).get(kind)
        if part.startswith("temp"):
            temperature = int(part[4:]) / 100.0
            out = {n: _temper(out[n], temperature) for n in heads}
        elif raw_part == "cal":
            key = "cal@" + chain
            if fit is not None:
                stack[key] = _cal_fit(out, fit[0], fit[1], heads)
            out = _cal_apply(out, stack[key], heads)
        elif raw_part in TWIN_PARTS:
            key = "twin@" + chain
            if fit is not None:
                stack[key] = _twin_fit(out, experts["w"], fit[0], fit[1], heads, raw_part == "twinh")
            out = _twin_apply(out, experts["w"], stack[key], heads)
        elif part.startswith("lpool") or raw_part in ("xlpool", "xlpoolh") + POOL_ONLY_BASE:
            out = _pool_apply(out, experts, stack[raw_part], heads)
        elif raw_part in ("xstack", "xstackc"):
            choice = stack[raw_part]
            out = {n: (_mix(out[n], experts[choice[n][0]][n], choice[n][1], raw_part == "xstackc")
                       if choice[n][0] else out[n]) for n in heads}
        elif part in ("stack", "stackc"):
            alphas = stack[raw_part]
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
        elif raw_part == "det":
            out = _det_apply(frame, schema, out, heads, options)
        elif part in ("regate", "transfer"):
            vectors = _flatten(out, heads)
            vectors = regate(frame, schema, vectors) if part == "regate" else transfer(frame, schema, vectors)
            out = _restore(vectors, heads, len(out[heads[0]]), options)
        else:
            raise ValueError("Unknown transform " + part)
    return out


def _is_fitted(chain):
    """True when a chain has a part whose parameters are estimated on the S rows."""
    for raw_part in chain.split("+"):
        part = _split(raw_part)[1]
        if raw_part in ("cal", "twin", "twinh") \
                or raw_part in ("xstack", "xstackc", "xlpool", "xlpoolh") + POOL_ONLY_BASE \
                or part in ("stack", "stackc") or part.startswith("lpool"):
            return True
    return False


def _chain_params(chain, base, experts, idx, truth, heads, skip=()):
    """Parameters of the pool / stack parts of a chain fitted on the rows idx (cal fits in _apply)."""
    params = {}
    for raw_part in chain.split("+"):
        if raw_part in skip or raw_part in params:
            continue
        kind, part = _split(raw_part)
        if part.startswith("lpool") or raw_part in ("xlpool", "xlpoolh") + POOL_ONLY_BASE:
            params[raw_part] = _pool_params(raw_part, base, experts, idx, truth, heads)
        elif raw_part in ("xstack", "xstackc"):
            params[raw_part] = _xstack_choice(base, experts, idx, truth, heads, raw_part == "xstackc")
        elif part in ("stack", "stackc"):
            params[raw_part] = _stack_alphas(base, experts[kind], idx, truth, heads, part == "stackc")
    return params


def _chain_oof(chain, frame, schema, base, experts, idx, truth, heads, options):
    """Two-fold out-of-fold S score of a whole chain: every fitted part (pool exponents, stack
    weights, reliability curve) is estimated on one half of the S rows and scored on the other."""
    half = len(idx) // 2
    total, cells = 0.0, 0
    for fit, held_out in ((slice(0, half), slice(half, None)), (slice(half, None), slice(0, half))):
        fit_truth = {n: truth[n][fit] for n in heads}
        params = _chain_params(chain, base, experts, idx[fit], fit_truth, heads)
        out = _apply(chain, frame, schema, base, experts, heads, options, params, fit=(idx[fit], fit_truth))
        rows = np.arange(len(idx[held_out]))
        for n in heads:
            total += float(np.log(_floored(out[n][idx[held_out]])[rows, truth[n][held_out]]).sum())
            cells += len(rows)
    return total / cells


def _stack_summary(key, value):
    if key.startswith("twin@"):
        return {"a": round(value["a"], 3), "g": [round(float(v), 2) for v in value["g"]],
                "d_abs_mean": round(float(np.abs(value["d"]).mean()), 3) if len(value["d"]) else 0.0}
    if key.startswith("cal@"):
        return [[round(float(a), 4), round(float(b), 5)] for a, b in zip(*value)]
    if isinstance(value, dict) and "kinds" in value:
        return {"kinds": value["kinds"], "global": [round(float(x), 4) for x in value["global"]]}
    return dict(collections.Counter(str(x) for x in value.values()))


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
    experts = {}
    for kind in ("g", "n", "m", "r", "q", "t"):
        if not any(kind in _needs_expert(c) for c in chains):
            continue
        if _over_budget(0.7):
            STATS.setdefault("expert_skipped", []).append(kind)
            continue
        started = time.monotonic()
        q = _fit_expert(kind, shadow, schema, given, heads, options, f_rows, np.concatenate((s_rows, e_rows)))
        STATS["shadow_expert_%s_seconds" % kind] = round(time.monotonic() - started, 3)
        experts[kind] = {n: base[n].copy() for n in heads}
        for n in heads:
            experts[kind][n][np.concatenate((idx_s, idx_e))] = q[n]
    if any("w" in _needs_expert(c) for c in chains):
        started = time.monotonic()
        both = np.concatenate((idx_s, idx_e))
        found = _twin_evidence(shadow, given, heads, options, f_rows, np.concatenate((s_rows, e_rows)))
        twin = {"ev": {n: np.zeros_like(base[n]) for n in heads}, "fields": found["fields"],
                "x": np.zeros((len(shadow_held), found["x"].shape[1]))}
        for n in heads:
            twin["ev"][n][both] = found["ev"][n]
        twin["x"][both] = found["x"]
        experts["w"] = twin
        STATS["shadow_twin_seconds"] = round(time.monotonic() - started, 3)
    chains = tuple(c for c in chains
                   if (bool(experts) if c in ("xstack", "xstackc", "xlpool", "xlpoolh")
                       else _needs_expert(c) <= set(experts)))
    if not chains:
        return final_vectors
    truth_s = {n: _labels(frame, s_rows, n, options) for n in heads}
    truth_e = {n: _labels(frame, e_rows, n, options) for n in heads}

    def logs(maps, idx, truth):
        return _cell_logs({n: maps[n][idx] for n in heads}, truth, heads)

    stack = {}
    for chain in chains:
        for key, value in _chain_params(chain, base, experts, idx_s, truth_s, heads, skip=stack).items():
            stack[key] = value
    reference_s = float(logs(base, idx_s, truth_s).mean())
    reference_e = logs(base, idx_e, truth_e).mean(axis=1)
    scores, transformed = {}, {}
    for chain in chains:
        transformed[chain] = _apply(chain, shadow, schema, base, experts, heads, options, stack,
                                    fit=(idx_s, truth_s))
        if _is_fitted(chain):   # honest ranking: parameters from one half of S, score on the other
            scores[chain] = _chain_oof(chain, shadow, schema, base, experts, idx_s, truth_s, heads, options)
        else:
            scores[chain] = float(logs(transformed[chain], idx_s, truth_s).mean())
    ranked = []
    for c in sorted(chains, key=lambda c: -scores[c]):   # one and the same S score = one candidate
        if scores[c] > reference_s and all(abs(scores[c] - scores[k]) > 1e-12 for k in ranked):
            ranked.append(c)
    record = dict(reference_s=reference_s, scores=scores, e_z=E_Z, xstack_kinds=list(XSTACK_KINDS),
                  stack={k: _stack_summary(k, v) for k, v in stack.items()})
    STATS["guard"] = record
    best = None
    if ranked and _instrument(schema) in NO_E_CHECK:
        best = ranked[0]
        record["e_check"] = "skipped"
    for chain in ([] if best else ranked[:MAX_E_TESTS]):
        d = logs(transformed[chain], idx_e, truth_e).mean(axis=1) - reference_e
        sd = float(d.std(ddof=1))
        lower = float(d.mean() - E_Z * sd / np.sqrt(len(d))) if sd > 0 else float(d.mean())
        record.setdefault("e_tests", {})[chain] = lower
        if lower > 0:
            best = chain
            break
    record["accepted"] = best
    if best is None:
        return final_vectors
    if _is_fitted(best):   # the E rows confirmed the procedure: refit its parameters on S and E
        idx_all = np.concatenate((idx_s, idx_e))
        truth_all = {n: np.concatenate((truth_s[n], truth_e[n])) for n in heads}
        stack = _chain_params(best, base, experts, idx_all, truth_all, heads)
        _apply(best, shadow, schema, base, experts, heads, options, stack, fit=(idx_all, truth_all))
        record["refit_rows"] = int(len(idx_all))
    final = _restore(final_vectors, heads, len(held), options)
    experts_final = {}
    used = _needs_expert(best)
    if best in stack and "kinds" in stack[best]:
        used = set(stack[best]["kinds"])
    elif best in ("xstack", "xstackc"):
        used = {kind for kind, _ in stack[best].values() if kind}
    for kind in sorted(used):
        if _over_budget(0.85):
            record["final_skipped"] = "budget"
            return final_vectors
        started = time.monotonic()
        if kind == "w":
            experts_final[kind] = _twin_evidence(frame, given, heads, options, visible, held)
        else:
            experts_final[kind] = _fit_expert(kind, frame, schema, given, heads, options, visible, held)
        STATS["final_expert_%s_seconds" % kind] = round(time.monotonic() - started, 3)
    return _flatten(_apply(best, frame, schema, final, experts_final, heads, options, stack), heads)


def _direct(frame, schema, final_vectors, chain):
    """Probe: apply one non-stack chain to the final output with the expert fit on all visible rows."""
    given, heads, options = _layout(schema)
    visible, held = _roles(frame, heads)
    if len(held) == 0 or len(visible) < 2:
        return final_vectors
    final = _restore(final_vectors, heads, len(held), options)
    experts = {}
    for kind in sorted(_needs_expert(chain)):
        started = time.monotonic()
        experts[kind] = _fit_expert(kind, frame, schema, given, heads, options, visible, held)
        STATS["final_expert_%s_seconds" % kind] = round(time.monotonic() - started, 3)
    STATS["direct"] = chain
    return _flatten(_apply(chain, frame, schema, final, experts, heads, options), heads)


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
    global XSTACK_KINDS
    started = time.monotonic()
    STATS.clear()
    _DET_CACHE.clear()
    name = _instrument(schema)
    XSTACK_KINDS = tuple(XSTACK_BY.get(name, _XSTACK_DEFAULT))
    if name in DIRECT and "+" not in DIRECT[name] and DIRECT[name].endswith("mix100"):
        _, heads, options = _layout(schema)   # the expert replaces the base entirely: no E041 fit
        _, held = _roles(frame, heads)
        vectors = [[1.0 / len(options[n])] * len(options[n]) for _ in range(len(held)) for n in heads]
    elif name in BASE_TREES:
        vectors = _e041_tree_base(frame, schema, float(BASE_TREES[name]), _seeds_for(name))
    else:
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
