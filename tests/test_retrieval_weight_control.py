"""E044 tests isolate weight use while preserving E041's activation decision."""

import numpy as np
from src.models import supervised_retrieval as parent
from src.models import retrieval_weight_control as control


def test_replacement_passes_initial_weights_but_preserves_activation(monkeypatch):
    captured = {}
    def spy(*args):
        captured['args'] = args
        return args[0]
    monkeypatch.setattr(parent, '_replace_evidence', spy)
    initial = np.array([1., 2.])
    groups, active = [[0], [1]], [1]
    learned = [np.array([5., 0.]), np.array([0., 5.])]
    marker = {}
    result = control.fixed_metric_evidence(marker, None, None, None, None,
        None, None, None, initial, ['a', 'b'], groups, learned, active)
    assert result is marker
    assert captured['args'][-1] is active
    assert captured['args'][-3] is groups
    for weight in captured['args'][-2]:
        np.testing.assert_array_equal(weight, initial)
    np.testing.assert_array_equal(learned[0], [5., 0.])


def test_control_layer_has_exact_parent_code_and_only_one_global_override():
    layer = control.control_layer
    assert layer.__code__ is parent.supervised_layer.__code__
    different = {k for k, value in parent.supervised_layer.__globals__.items()
                 if layer.__globals__.get(k) is not value}
    assert different == {'_replace_evidence'}
    assert layer.__globals__['_replace_evidence'] is control.fixed_metric_evidence
    assert parent.supervised_layer.__globals__['_replace_evidence'] is parent._replace_evidence


def test_non_unhcr_uses_exact_parent(monkeypatch):
    sentinel = object()
    monkeypatch.setattr(parent, 'predict', lambda *a, **kw: sentinel)
    assert control.predict(None, {'items': {}}) is sentinel


def test_actual_posterior_changes_only_active_items():
    import pandas as pd
    # Two disagreeing donors: initial favours column0, learned favours column1.
    frame = pd.DataFrame({'a': ['x', 'y', None], 'b': ['x', 'y', None]})
    records = {n: {'class': 'PREDICT', 'values': ['x', 'y']} for n in frame}
    options = {n: ['x', 'y'] for n in frame}
    codes = np.array([[1, 0], [0, 1], [1, 1]])
    initial, learned = np.array([4., 0.]), [np.array([0., 4.]), np.ones(2)]
    args = (frame, records, ['a', 'b'], options, codes, np.array([2]),
            np.array([0, 1]), initial, ['a', 'b'], [[0], [1]], learned, [0])
    seed = {'b': np.array([[.3, .7]])}
    old = parent._replace_evidence(dict(seed), *args)
    new = control.fixed_metric_evidence(dict(seed), *args)
    assert old['a'][0, 1] > .95
    assert new['a'][0, 0] > .95
    np.testing.assert_array_equal(new['b'], seed['b'])
    np.testing.assert_allclose(new['a'].sum(axis=1), 1.)
