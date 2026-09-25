"""E056 invariants and independent calculations, using synthetic labels only."""

import ast
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from scripts import screen_e056 as screen


def test_identity_and_zero_content_mass_are_exact():
    p = np.array([[.1, .3, .8], [0., 0., .7]])
    q = np.array([[.9, .1], [.2, .8]])
    assert screen.intervene(p, q, 0) is p
    changed = screen.intervene(p, q, .5)
    np.testing.assert_array_equal(changed[1], p[1])
    np.testing.assert_array_equal(changed[:, -1], p[:, -1])
    np.testing.assert_allclose(changed.sum(1), p.sum(1), atol=1e-15)
    np.testing.assert_allclose(changed[0], [.23, .17, .8])


def test_class_alignment_and_laplace_unseen_class():
    result = screen.smooth_tree(np.array([[.8, .2]]), [2, 0], [3, 0, 7])
    expected = .99 * np.array([[.2, 0., .8]]) + .01 * np.array([4, 1, 8]) / 13
    np.testing.assert_allclose(result, expected)
    assert np.all(result > 0)


def test_leaf_library_preserves_parent_and_uses_no_target_features():
    n = 110
    frame = pd.DataFrame({'X': ['0', '1'] * 55, 'P': ['1'] * 100 + [None] * 10,
                          'C': ['a', 'b'] * 50 + [None] * 10})
    schema = {'gated_value': 'NA_GATED', 'items': {
        'X': {'class': 'GIVEN', 'values': ['0', '1']},
        'P': {'class': 'PREDICT', 'values': ['0', '1']},
        'C': {'class': 'PREDICT', 'values': ['a', 'b'],
              'gate': {'parent': 'P', 'observed_if': ['1']}}}}
    query = np.arange(100, n)
    trees, info = screen.fit_trees(frame, schema, query, ['C'])
    assert info['given'] == ['X']
    assert info['heads']['C']['asked_fit_rows'] == 100
    assert info['fit_count'] == 1
    assert trees['C'].shape == (10, 2)
    bad = frame.copy()
    bad.loc[100, 'P'] = '1'
    with pytest.raises(ValueError, match='mask'):
        screen.fit_trees(bad, schema, query, ['C'])
    sparse = frame.copy()
    sparse.loc[0, 'C'] = 'NA_GATED'
    tree, info = screen.fit_trees(sparse, schema, query, ['C'])
    assert tree['C'] is None and info['fit_count'] == 0
    singleton = frame.copy()
    singleton.loc[:99, 'C'] = 'a'
    assert screen.fit_trees(singleton, schema, query, ['C'])[0]['C'] is None


def test_official_floor_matches_actual_source_with_nonunit_vectors():
    source = Path('external/starter-kit/score.py').read_text(encoding='utf-8')
    function = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'floored')
    namespace = {'np': np}
    exec(compile(ast.Module(body=[function], type_ignores=[]), '<official floored>', 'exec'), namespace)
    p = np.array([[0., .2, .9], [.7, .1, .3]])
    expected = namespace['floored'](p, {}, [(0, 0, 'C'), (1, 0, 'C')], .001)
    np.testing.assert_array_equal(screen.floor_mix(p), np.array(expected))
    altered = screen.intervene(p, np.array([[.3, .7], [.9, .1]]), .5)
    np.testing.assert_allclose(screen.floor_mix(altered)[:, -1], screen.floor_mix(p)[:, -1], atol=2e-16)


def test_finite_oracle_equals_all_729_combinations():
    rng = np.random.default_rng(56)
    base = {'P': rng.dirichlet([1, 1], 8)}
    tree = {}
    labels = {'P': rng.integers(0, 2, 8)}
    for i in range(6):
        name = f'C{i}'
        base[name] = rng.dirichlet([1, 1, 1], 8) * 1.13
        tree[name] = rng.dirichlet([1, 1], 8)
        labels[name] = rng.integers(0, 3, 8)
    arms = screen.make_arms(base, tree)
    scores = screen.score_arms(arms, labels)
    result = screen.oracle(scores, list(base), base)
    brute = max(sum(scores[n][a].sum() for n, a in zip(tree, choice)) + scores['P'][0].sum()
                for choice in product(range(3), repeat=6))
    assert result['best_log_sum'] == pytest.approx(brute, abs=1e-12)
    assert all(arms['P'][i] is base['P'] for i in range(3))
    assert result['delta_skill'] >= -1e-15


def test_cluster_se_matches_hand_calculation_with_unequal_groups():
    d = np.array([1., 3., 2., -2., 4.])
    groups = np.array(['a', 'a', 'b', 'c', 'c'])
    mean, se = screen.cluster_mean_se(d, groups)
    assert mean == pytest.approx(1.6)
    assert se == pytest.approx(np.sqrt(1.5 * (.8**2 + .4**2 + (-1.2)**2) / 25))
    assert screen.cluster_mean_se(d, np.zeros(5))[1] == float('inf')


def test_selector_ties_and_uncertain_gain_return_zero():
    scores = {'C': np.array([[0., 0., 0., 0.], [2., 2., -1., -1.], [0., 0., 0., 0.]])}
    selected, detail = screen.select(scores, ['C'], np.array(['a', 'a', 'b', 'b']))
    assert selected == {'C': 0}
    assert detail['C']['proposed_index'] == 1
    scores['C'][1] = 1
    scores['C'][2] = 1
    assert screen.select(scores, ['C'], np.array(['a', 'a', 'b', 'b']))[0] == {'C': 1}


def test_bootstrap_resamples_whole_groups_with_person_weighted_ratio():
    d = np.array([1., 3., -2.])
    groups = np.array(['a', 'a', 'b'])
    result = screen.cluster_bootstrap(d, groups)
    rng = np.random.default_rng(5601)
    expected = []
    for _ in range(2000):
        draw = rng.integers(0, 2, 2)
        expected.append(np.array([4., -2.])[draw].sum() / np.array([2, 1])[draw].sum())
    np.testing.assert_array_equal(result, np.quantile(expected, [.025, .975]))


def test_stage_boundaries_and_no_intervention_audit_stop():
    with pytest.raises(ValueError):
        screen.allow_stage('selection', {})
    with pytest.raises(ValueError):
        screen.allow_stage('audit', {'oracle': {'gate': 'PASS'}, 'selection': {'shares': {'C': 0}}})
    with pytest.raises(ValueError):
        screen.allow_stage('calibration', {})
    screen.allow_stage('selection', {'oracle': {'gate': 'PASS'}})
    screen.allow_stage('audit', {'oracle': {'gate': 'PASS'}, 'selection': {'shares': {'C': 1}}})
