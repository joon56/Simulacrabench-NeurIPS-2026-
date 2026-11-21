"""Small fixtures only; no cache decoding, response access or optimizer run."""
import ast
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy.special import softmax


def test_implementation_exists():
    assert importlib.util.find_spec('scripts.screen_e059') is not None


@pytest.fixture
def study():
    from scripts import screen_e059
    screen_e059.numerical()
    return screen_e059


def test_pairs_beta0_and_gradient(study):
    rng = np.random.default_rng(59)
    features = rng.integers(0, 2, (5, 4, 6)).astype(float)
    weights = np.arange(6) / 5
    expected = np.stack([features[..., j] * features[..., k]
                         for j in range(6) for k in range(j + 1, 6)], -1)
    np.testing.assert_array_equal(study.pair_features(features), expected)
    np.testing.assert_array_equal(study.posterior(features, weights, np.zeros(15)),
                                  softmax(np.einsum('qkd,d->qk', features, weights), 1))
    args = (features, rng.integers(0, 2, (5, 4, 7)), np.full((5, 7), .3),
            np.array([2, 3, 3, 3, 3, 3, 3]), weights, .2867)
    original = [x.copy() if hasattr(x, 'copy') else x for x in args]
    beta = np.linspace(-.3, .3, 15)
    _, grad = study.objective(beta, *args)
    numeric = [(study.objective(beta + d, *args)[0] - study.objective(beta - d, *args)[0]) / 2e-6
               for d in np.eye(15) * 1e-6]
    np.testing.assert_allclose(grad, numeric, atol=2e-8)
    for x, y in zip(args, original):
        np.testing.assert_array_equal(x, y)


def test_leaf_algebra_identity_and_frozen_buckets(study):
    g = {'parent': np.array([[.4, .6], [.7, .3]]), 'leaf': np.array([[.1, .2, .7], [.2, .5, .3]])}
    old = {'leaf': np.array([[0., .5, .5], [.3, .2, .5]])}
    new = {'leaf': np.array([[.2, .7, .1], [.1, .8, .1]])}
    lambdas = {'leaf': (0., .1)}
    bucket = np.array([False, True])
    lam = np.array([0., .1])[:, None]
    r = {'parent': g['parent'].copy(), 'leaf': (1-lam)*g['leaf']+lam*old['leaf']}
    a = study.leaf_replace(r, old, new, lambdas, bucket)
    np.testing.assert_allclose(a['leaf'], (1-lam)*g['leaf']+lam*new['leaf'], atol=1e-12)
    np.testing.assert_array_equal(a['parent'], r['parent'])
    np.testing.assert_array_equal(a['leaf'][0], r['leaf'][0])
    identity = study.leaf_replace(r, old, old, lambdas, bucket)
    for n in r:
        np.testing.assert_array_equal(identity[n], r[n])
    assert lambdas == {'leaf': (0., .1)} and bucket.tolist() == [False, True]
    with pytest.raises(ValueError):
        study.valid({'bad': np.array([[-1e-16, 1.]])})


def test_evidence_uses_only_fixed_visible_donors(study):
    labels = np.array([[0, 1], [1, 2], [-1, -1]])
    donors = np.array([[0, 1]])
    post = np.array([[.2, .8]])
    before = donors.copy()
    result = study.evidence(labels, donors, post, [2, 3], np.array([0, 1]))
    poisoned = labels.copy()
    poisoned[2] = [1, 1]
    again = study.evidence(poisoned, donors, post, [2, 3], np.array([0, 1]))
    for a, b in zip(result, again):
        np.testing.assert_array_equal(a, b)
    np.testing.assert_array_equal(result[1], [[0, .2, .8]])
    np.testing.assert_array_equal(donors, before)
    with pytest.raises(ValueError):
        study.evidence(labels, np.array([[0, 2]]), post, [2, 3], np.array([0, 1]))


def test_pair_constant_gate_checks_each_query_and_donor(study):
    features = np.ones((2, 3, 6))
    assert study.constant_pairs(features)
    features[1, 1, 2] = 0
    assert not study.constant_pairs(features)


def test_official_floor_and_two_contrasts(study):
    source = ast.parse(Path('external/starter-kit/score.py').read_text(encoding='utf-8'))
    node = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'floored')
    scope = {'np': np}
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<official-floor>', 'exec'), scope)
    raw = np.array([[0., .3, .9], [1., 0., 0.]])
    expected = scope['floored'](raw, {}, [(i, 0, 'n') for i in range(2)], .001)
    np.testing.assert_array_equal(study.floor_mix(raw), np.asarray(expected))
    arms = {name: {'n': raw.copy()} for name in ('R', 'A_half', 'B_half')}
    np.testing.assert_array_equal(study.upper_bounds(arms), [0., 0.])
    logs = np.array([[1., 2.], [2., 3.], [4., 4.]])
    np.testing.assert_array_equal(study.contrasts(logs), [[3., 2.], [2., 1.]])


def test_cluster_selection_requires_both(study):
    groups = np.array(['a', 'a', 'b', 'c', 'c'])
    d = np.array([1., 3., 2., -2., 1.])
    mean, se = study.cluster_mean_se(d, groups)
    assert mean == 1 and se == pytest.approx(np.sqrt(1.5*(4+1+9)/25))
    assert study.selection_gate(np.stack([np.ones(5), d]), groups)['gate'].startswith('STOP')
    assert study.selection_gate(np.ones((2, 5)), groups)['gate'] == 'AUDIT'


def test_bootstrap_shared_draws_group_ratio_and_quantiles(study):
    delta = np.array([[1., 3., -1.], [2., 6., -2.]])
    groups = np.array(['a', 'a', 'b'])
    draws = np.random.default_rng(5801).integers(0, 2, (2000, 2))
    values = np.array([4., -1.])[draws].sum(1)/np.array([2, 1])[draws].sum(1)
    expected = np.stack([np.quantile(values, [.0125, .9875]), np.quantile(2*values, [.0125, .9875])])
    np.testing.assert_array_equal(study.bootstrap(delta, groups), expected)


def test_stage_guards_and_exclusive_markers(study, tmp_path):
    with pytest.raises(ValueError):
        study.allow_stage('oracle', {})
    with pytest.raises(ValueError):
        study.allow_stage('audit', {'fit': {'gate': 'ORACLE'}, 'oracle': {'gate': 'SELECT'}})
    study.allow_stage('audit', {'fit': {'gate': 'ORACLE'}, 'oracle': {'gate': 'SELECT'}, 'selection': {'gate': 'AUDIT'}})
    study.save(tmp_path/'marker.json', {'opened': True})
    with pytest.raises(FileExistsError):
        study.save(tmp_path/'marker.json', {'opened': True})


def test_exact_pair_filter_excludes_cross_product(study):
    import pyarrow as pa
    import pyarrow.dataset as ds
    keys = pd.DataFrame({'SSUID': ['a', 'b'], 'PNUM': ['1', '2']})
    source = pa.table({'SSUID': ['a', 'a', 'b', 'b'], 'PNUM': ['1', '2', '1', '2'], 'response': [1, 99, 88, 2]})
    assert ds.dataset(source).to_table(filter=study.key_filter(keys))['response'].to_pylist() == [1, 2]
