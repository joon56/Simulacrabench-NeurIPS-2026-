"""E058 fixed-family and role-boundary fixtures; no real fits or responses."""
import ast
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy.special import softmax

from scripts import screen_e058 as study


@pytest.fixture(autouse=True, scope='module')
def numerical():
    study.load_numerical()


def objective_fixture():
    rng = np.random.default_rng(3)
    e = rng.integers(0, 2, (7, 4, 6)).astype(float)
    matches = rng.integers(0, 2, (7, 4, 2)).astype(float)
    return e, matches, np.full((7, 2), .3), np.array([2, 3]), np.arange(6) / 5, .7


def test_all_pairs_and_beta_zero_exact_posterior():
    e, _, _, _, w, _ = objective_fixture()
    pairs = study.pair_features(e)
    assert pairs.shape == (7, 4, 15)
    np.testing.assert_array_equal(pairs[..., 0], e[..., 0] * e[..., 1])
    np.testing.assert_array_equal(pairs[..., -1], e[..., 4] * e[..., 5])
    np.testing.assert_array_equal(study.posterior(e, w, np.zeros(15)),
                                  softmax(np.einsum('qkd,d->qk', e, w), axis=1))


def test_analytic_gradient_and_fixed_first_order_share():
    args = objective_fixture()
    copies = [x.copy() if hasattr(x, 'copy') else x for x in args]
    beta = np.linspace(-.3, .3, 15)
    value, grad = study.objective(beta, *args)
    numeric = []
    for j in range(15):
        offset = np.eye(15)[j] * 1e-6
        numeric.append((study.objective(beta + offset, *args)[0] - study.objective(beta - offset, *args)[0]) / 2e-6)
    np.testing.assert_allclose(grad, numeric, atol=2e-8, rtol=2e-6)
    for current, original in zip(args, copies):
        np.testing.assert_array_equal(current, original)
    assert np.isfinite(value)


def test_beta_zero_matches_original_marginal_retrieval_loss():
    from src.models.supervised_retrieval import _retrieval_log
    e, matches, prior, sizes, weights, share = objective_fixture()
    value, _ = study.objective(np.zeros(15), e, matches, prior, sizes, weights, share)
    assert value == pytest.approx(-_retrieval_log(e, matches, prior, sizes, weights, share).mean(), abs=1e-15)


def test_exact_pair_filter_does_not_admit_cross_product_people():
    import pyarrow as pa
    import pyarrow.dataset as ds
    keys = pd.DataFrame({'SSUID': ['a', 'b'], 'PNUM': ['1', '2']})
    table = pa.table({'SSUID': ['a', 'a', 'b', 'b'], 'PNUM': ['1', '2', '1', '2'],
                      'response': [10, 99, 88, 20]})
    got = ds.dataset(table).to_table(filter=study.key_filter(keys)).to_pandas()
    assert got.response.tolist() == [10, 20]


def test_query_given_projection_never_requires_response():
    from scripts.screen_e055 import GIVEN_VOCAB, PARENT, REASONS
    rows = pd.DataFrame({n: [v[0], v[-1]] for n, v in GIVEN_VOCAB.items()})
    result = study.query_frame(rows)
    assert list(result) == list(GIVEN_VOCAB) + [PARENT] + REASONS
    assert result[[PARENT] + REASONS].isna().all().all()
    changed = rows.copy()
    changed['THOSPNIT'] = ['999', '-1']
    changed['EHREAS_BIR'] = ['secret', 'secret']
    pd.testing.assert_frame_equal(result, study.query_frame(changed))


def test_partial_mask_and_donor_contamination_stop():
    frame = pd.DataFrame({'P': ['a', np.nan, np.nan], 'C': ['x', np.nan, 'x']})
    with pytest.raises(ValueError, match='block'):
        study.partition(frame, ['P', 'C'])
    frame.loc[2, 'C'] = np.nan
    visible, query = study.partition(frame, ['P', 'C'])
    np.testing.assert_array_equal(visible, [0])
    np.testing.assert_array_equal(query, [1, 2])
    with pytest.raises(ValueError, match='donor'):
        study.check_donors(np.array([[0, 1]]), visible)


def test_inactive_evidence_is_original_object():
    original = {0: ({'P': np.array([.2, .8])}, False)}
    assert study.replace_evidence(None, None, {'active': [], 'legacy': original}, {}) is original


def test_official_floor_and_pooled_global_mixture():
    source = ast.parse(Path('external/starter-kit/score.py').read_text(encoding='utf-8'))
    node = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'floored')
    scope = {'np': np}
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<floor>', 'exec'), scope)
    base = {'P': np.array([[.2, .8], [.7, .3]]), 'C': np.array([[.1, .2, .8], [.1, .6, .2]])}
    candidate = {n: p[:, ::-1] for n, p in base.items()}
    labels = {'P': np.array([0, 1]), 'C': np.array([1, 2])}
    for alpha in study.SHARES:
        mixed = study.mix(base, candidate, alpha)
        expected = []
        for n in base:
            p = scope['floored'](mixed[n], {}, [(i, 0, n) for i in range(2)], .001)
            expected.append(np.log(np.asarray(p)[np.arange(2), labels[n]]))
        np.testing.assert_array_equal(study.log_rows(mixed, labels), np.column_stack(expected).mean(1))
    assert study.mix(base, candidate, 0) is base


def test_cluster_se_uses_whole_units_and_two_se_guard():
    d = np.array([1., 3., 2., -2., 1.])
    g = np.array(['a', 'a', 'b', 'c', 'c'])
    mean, se = study.cluster_mean_se(d, g)
    expected = np.sqrt(1.5 * ((4 - 2)**2 + (2 - 1)**2 + (-1 - 2)**2) / 25)
    assert mean == 1 and se == pytest.approx(expected)
    assert study.choose(np.stack([np.zeros(5), d, d]), g)['alpha'] == 0
    assert study.choose(np.stack([np.zeros(5), np.ones(5), np.ones(5)]), g)['alpha'] == .25


def test_stage_guards_do_not_open_audit_after_zero_selection():
    with pytest.raises(ValueError):
        study.allow_stage('selection', {})
    with pytest.raises(ValueError):
        study.allow_stage('audit', {'oracle': {'gate': 'SELECT'}, 'selection': {'alpha': 0}})
    study.allow_stage('audit', {'oracle': {'gate': 'SELECT'}, 'selection': {'alpha': .25}})


def test_bootstrap_is_group_ratio_and_fixed_seed():
    delta = np.array([1., 3., -1.])
    groups = np.array(['a', 'a', 'b'])
    draws = np.random.default_rng(5801).integers(0, 2, (2000, 2))
    expected = np.array([4., -1.])[draws].sum(1) / np.array([2, 1])[draws].sum(1)
    np.testing.assert_array_equal(study.bootstrap(delta, groups), np.quantile(expected, [.025, .975]))


def test_active_evidence_endpoint_fixed_donors_buckets_and_hidden_labels():
    from src.models import supervised_retrieval as retrieval
    rng = np.random.default_rng(7)
    codes = rng.integers(0, 3, (38, 6))
    frame = pd.DataFrame({f'G{i}': codes[:, i].astype(str) for i in range(6)})
    frame['P'] = (codes[:, 0] % 2).astype(str)
    frame['C'] = (codes[:, 1] % 2).astype(str)
    frame.loc[34:, ['P', 'C']] = np.nan
    schema = {'gated_value': 'NA_GATED', 'items': {
        **{f'G{i}': {'class': 'GIVEN', 'values': ['0', '1', '2']} for i in range(6)},
        'P': {'class': 'PREDICT', 'values': ['0', '1']},
        'C': {'class': 'PREDICT', 'values': ['0', '1'], 'gate': {'parent': 'P', 'observed_if': ['1']}}}}
    records, items, options = retrieval._layout(frame, schema)
    query, visible, weights = np.arange(34, 38), np.arange(34), np.arange(6) / 3
    donors = retrieval.candidate_indices(codes, weights, query, visible, k=32)
    original = retrieval._replace_evidence({}, frame, records, items, options, codes, query,
                                           visible, weights, ['P', 'C'], [[0, 1]], [weights], [0])
    legacy = {int(row): ({n: p[i] for n, p in original.items()}, bool(i % 2)) for i, row in enumerate(query)}
    state = {'active': [0], 'legacy': legacy, 'query': query, 'visible': visible,
             'signature': (codes, None), 'sections': ([weights], [0], []), 'predicted': ['P', 'C'],
             'metric_arguments': (None,) * 7 + ([[0, 1]],),
             'donor_calls': [{'kind': 'section', 'query': query, 'donors': donors}]}
    zero = study.replace_evidence(frame, schema, state, {0: np.zeros(15)})
    changed = study.replace_evidence(frame, schema, state, {0: np.ones(15) * .5})
    poisoned = frame.copy()
    poisoned.loc[34:, ['P', 'C']] = '0'
    again = study.replace_evidence(poisoned, schema, state, {0: np.ones(15) * .5})
    for row in query:
        assert zero[row][1] == changed[row][1] == legacy[row][1]
        for name in original:
            np.testing.assert_array_equal(zero[row][0][name], legacy[row][0][name])
            np.testing.assert_array_equal(changed[row][0][name], again[row][0][name])
    np.testing.assert_array_equal(state['donor_calls'][0]['donors'], donors)
    np.testing.assert_array_equal(state['sections'][0][0], weights)
