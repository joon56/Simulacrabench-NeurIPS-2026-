"""Isolated A040 contract prototype. Import loads one verified checkpoint.

Only new fake fixtures are authorized. This is not a submission predictor.
"""
import hashlib
import os
from pathlib import Path

import numpy as np
from tabicl import TabICLClassifier

CHECKPOINT = Path(os.environ['A040_CHECKPOINT']).resolve()
CHECKPOINT_SHA256 = 'bdc7dbd5e4ff21f8f0456fcf90c6b7cdf72dbea960f2d05b19bec19f9b3d4ed0'
if CHECKPOINT.stat().st_size != 110368038 or hashlib.sha256(CHECKPOINT.read_bytes()).hexdigest() != CHECKPOINT_SHA256:
    raise ValueError('Unverified checkpoint: no deserialization allowed')

OPTIONS = dict(n_estimators=8, norm_methods=['none', 'power'],
               feat_shuffle_method='latin', class_shuffle_method='shift',
               random_state=42, softmax_temperature=.9, average_logits=True,
               support_many_classes=True, batch_size=8, kv_cache=False,
               device='cuda', use_amp=True, use_fa3=False, offload_mode=False,
               n_jobs=2, verbose=False, model_path=str(CHECKPOINT),
               allow_auto_download=False,
               checkpoint_version='tabicl-classifier-v2-20260212.ckpt')
COUNTS = dict(adapter_injections=0, singleton=0, empty=0)
_loader = TabICLClassifier(**OPTIONS)
_loader._load_model()
SHARED_MODEL = _loader.model_.to('cuda').eval()
SHARED_CONFIG = _loader.model_config_.copy()
del _loader


class SharedClassifier(TabICLClassifier):
    """Version-bound injection; no monkeypatch or head/context sharing."""

    def _load_model(self):
        SHARED_MODEL.clear_cache()
        self.model_ = SHARED_MODEL
        self.model_config_ = SHARED_CONFIG.copy()
        self.model_path_ = CHECKPOINT
        COUNTS['adapter_injections'] += 1


def schema_options(schema):
    return {name: list(spec['values']) + ([schema['gated_value']] if spec.get('gate') else [])
            for name, spec in schema['items'].items() if spec['class'] in ('GIVEN', 'PREDICT')}


class RoleViews:
    """Fitted components only receive the masked view and the exact F slice."""

    def __init__(self, frame, schema, fit, selection, evaluation, query):
        self.fit_rows, self.s_rows, self.e_rows, self.q_rows = map(list, (fit, selection, evaluation, query))
        all_rows = self.fit_rows + self.s_rows + self.e_rows + self.q_rows
        if len(set(all_rows)) != len(all_rows) or set(all_rows) != set(frame.index):
            raise ValueError('Roles must partition the fixture')
        self.given = [n for n, r in schema['items'].items() if r['class'] == 'GIVEN']
        self.heads = [n for n, r in schema['items'].items() if r['class'] == 'PREDICT']
        self.options = schema_options(schema)
        self.query_rows = sorted(self.s_rows + self.e_rows + self.q_rows)
        self._selection = self._encode(frame, self.s_rows)
        self._evaluation = self._encode(frame, self.e_rows)
        self.shadow = frame.copy(deep=True)
        self.shadow.loc[self.query_rows, self.heads] = np.nan
        self._phase = 'fit'
        self._alpha = None

    def _encode(self, frame, rows):
        result = {}
        for name in self.heads:
            codes = frame.loc[rows, name].map({v: i for i, v in enumerate(self.options[name])})
            if codes.isna().any():
                raise ValueError('Invalid label in sealed fake role')
            result[name] = codes.to_numpy(dtype=int)
            result[name].setflags(write=False)
        return result

    def fit_input(self, name, rows=None):
        if self._phase != 'fit':
            raise PermissionError('No learning after selection access')
        if rows is not None and list(rows) != self.fit_rows:
            raise PermissionError('Only F may reach fit')
        if not self.shadow.loc[self.query_rows, self.heads].isna().all().all():
            raise PermissionError('Unmasked held-role target')
        X = self.shadow.loc[self.fit_rows, self.given].copy().astype(object)
        if len(X) and not any(X[n].nunique(dropna=False) > 1 for n in self.given):
            raise ValueError('No usable given features')
        y = self.shadow.loc[self.fit_rows, name].map({v: i for i, v in enumerate(self.options[name])})
        if y.isna().any():
            raise ValueError('Invalid target in F')
        return X, y.to_numpy(dtype=int)

    def selection(self):
        if self._phase != 'fit':
            raise PermissionError('Selection is one-shot')
        self._phase = 'selection'
        return self._selection

    def freeze(self, alpha):
        if self._phase != 'selection' or alpha not in (0, .25, .5):
            raise PermissionError('Freeze once after S, before E')
        self._alpha = alpha
        self._phase = 'frozen'

    def evaluation(self):
        if self._phase != 'frozen':
            raise PermissionError('E requires frozen alpha and opens once')
        self._phase = 'evaluated'
        return self._evaluation


def valid(values):
    p = np.asarray(values)
    if p.ndim != 2 or p.shape[1] == 0 or not np.issubdtype(p.dtype, np.number):
        raise ValueError('Expected numeric probability matrix')
    if not np.isfinite(p).all() or (p < 0).any() or (p.sum(axis=1) <= 0).any():
        raise ValueError('Invalid distribution')
    return p


def align(values, classes, width):
    values = valid(values)
    classes = np.asarray(classes)
    if len(classes) != values.shape[1] or not np.issubdtype(classes.dtype, np.integer):
        raise ValueError('Invalid classes_ alignment')
    if len(set(classes.tolist())) != len(classes) or (classes < 0).any() or (classes >= width).any():
        raise ValueError('Class outside schema')
    result = np.zeros((len(values), width), dtype=np.float64)
    result[:, classes] = values / values.sum(axis=1, keepdims=True)
    return result


def empty_fallback(base):
    valid(base)
    COUNTS['empty'] += 1
    return base


def predict_head(roles, name, base=None):
    X, y = roles.fit_input(name)
    width = len(roles.options[name])
    query = roles.shadow.loc[roles.query_rows, roles.given].astype(object)
    if len(y) == 0:
        if base is None:
            raise ValueError('Empty context requires retained baseline')
        return None, empty_fallback(base)
    if len(np.unique(y)) == 1:
        COUNTS['singleton'] += 1
        return None, np.tile(np.eye(width)[int(y[0])], (len(query), 1))
    estimator = SharedClassifier(**OPTIONS)
    estimator.fit(X, y)
    return estimator, align(estimator.predict_proba(query), estimator.classes_, width)


def mix(base, expert, alpha):
    p = valid(base)
    if alpha not in (0, .25, .5):
        raise ValueError('Alpha outside fixed family')
    if alpha == 0:
        return base
    q = valid(expert)
    if p.shape != q.shape:
        raise ValueError('Mixture shape mismatch')
    return (1 - alpha) * (p / p.sum(axis=1, keepdims=True)) + alpha * (q / q.sum(axis=1, keepdims=True))


def floored(values):
    p = valid(values).astype(np.float64)
    p = p / p.sum(axis=1, keepdims=True)
    return .001 + (1 - .001 * p.shape[1]) * p


def row_log_scores(base, expert, truth, alpha):
    scores = []
    for name in base:
        values = floored(mix(base[name], expert[name], alpha))
        labels = truth[name]
        if len(labels) != len(values) or (labels < 0).any() or (labels >= values.shape[1]).any():
            raise ValueError('Invalid scoring fixture labels')
        scores.append(np.log(values[np.arange(len(labels)), labels]))
    return np.mean(np.stack(scores, axis=1), axis=1)


def select_alpha(base, expert, truth):
    values = [float(row_log_scores(base, expert, truth, a).mean()) for a in (0, .25, .5)]
    return (0, .25, .5)[int(np.argmax(values))]


def independent_check(base, expert, truth, alpha):
    delta = row_log_scores(base, expert, truth, alpha) - row_log_scores(base, expert, truth, 0)
    if len(delta) < 2:
        raise ValueError('Independent fixture needs at least two rows')
    lower = float(delta.mean() - 1.645 * delta.std(ddof=1) / np.sqrt(len(delta)))
    return bool(alpha > 0 and lower > 0), lower


def flatten(frame, schema, predictions, query_rows):
    heads = [n for n, r in schema['items'].items() if r['class'] == 'PREDICT']
    options = schema_options(schema)
    if set(predictions) != set(heads):
        raise ValueError('Entire target schema required')
    for name in heads:
        if valid(predictions[name]).shape != (len(query_rows), len(options[name])):
            raise ValueError('Bad output width/row count')
    return [predictions[name][j].tolist() for j, row in enumerate(query_rows)
            for name in heads if frame.loc[row, name] != frame.loc[row, name]]
