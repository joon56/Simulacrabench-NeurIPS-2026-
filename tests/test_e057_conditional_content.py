"""E057 structural and complete-policy fixtures; no survey score evidence."""

import ast
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.models import conditional_leaf_content as model

PARENT = 's3_11_intent_return_12m_lbl'


def fixture_frame(n=2000, hidden=6):
    x = np.arange(n + hidden) % 2
    frame = pd.DataFrame({'X': x.astype(str), PARENT: ['1'] * (n + hidden),
                          'C': np.where(x == 0, 'a', 'b')})
    frame.loc[n:, [PARENT, 'C']] = np.nan
    schema = {'gated_value': 'NA_GATED', 'items': {
        'X': {'class': 'GIVEN', 'values': ['0', '1']},
        PARENT: {'class': 'PREDICT', 'values': ['0', '1']},
        'C': {'class': 'PREDICT', 'values': ['a', 'b'],
              'gate': {'parent': PARENT, 'observed_if': ['1']}}}}
    return frame, schema


def stub_base(frame, schema):
    return [np.array([.4, .6]) if name == PARENT else np.array([.3, .3, .4])
            for _, row in frame.iterrows() for name, rec in schema['items'].items()
            if rec['class'] == 'PREDICT' and pd.isna(row[name])]


def test_scope_schema_order_and_nonpredict_descendant():
    _, schema = fixture_frame()
    assert model.layout(schema)[1] == ['C']
    schema['items']['unused'] = {'class': 'EXCLUDE', 'values': ['z'],
                                'gate': {'parent': 'C', 'observed_if': ['a']}}
    assert model.layout(schema)[1] == []
    assert model.layout(schema)[0] == [PARENT, 'C']


def test_split_fixed_disjoint_sizes():
    fit, selection, validation = model.split_visible(np.arange(8279))
    assert (len(fit), len(selection), len(validation)) == (5879, 1200, 1200)
    assert len(set(fit) | set(selection) | set(validation)) == 8279
    for first, second in ((fit, selection), (fit, validation), (selection, validation)):
        assert not set(first) & set(second)
    expected = np.random.default_rng(5701).permutation(np.arange(8279))
    np.testing.assert_array_equal(selection, np.sort(expected[:1200]))


def test_raw_mass_sentinel_and_zero_are_preserved():
    p = np.array([[.1, .3, .8], [0., 0., .7]])
    q = np.array([[.9, .1], [.2, .8]])
    assert model.mix_content(p, q, 0) is p
    new = model.mix_content(p, q, .5)
    np.testing.assert_array_equal(new[:, -1], p[:, -1])
    np.testing.assert_array_equal(new[1], p[1])
    np.testing.assert_allclose(new.sum(1), p.sum(1), rtol=0, atol=1e-15)


def test_official_floor_nonunit_parity():
    code = ast.parse(Path('external/starter-kit/score.py').read_text(encoding='utf-8'))
    node = next(n for n in code.body if isinstance(n, ast.FunctionDef) and n.name == 'floored')
    scope = {'np': np}
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<official floor>', 'exec'), scope)
    vectors = np.array([[0., .2, 1.], [.2, .3, .8]])
    expected = scope['floored'](vectors, {}, [(0, 0, 'C'), (1, 0, 'C')], .001)
    np.testing.assert_array_equal(model.floor_mix(vectors), expected)


def test_schema_class_alignment_sparse_and_constant_fallback():
    frame, schema = fixture_frame(110, 5)
    schema['items']['C']['values'] = ['b', 'unseen', 'a']
    tree, details = model.fit_trees(frame, schema, np.arange(110, 115), ['C'])
    assert details['C']['asked_rows'] == 110
    assert tree['C'].shape == (5, 3)
    assert np.all(tree['C'][:, 1] > 0)
    assert np.argmax(tree['C'][0]) == 2  # X=0 gives schema answer a, index2.
    frame.loc[:10, 'C'] = 'NA_GATED'
    assert model.fit_trees(frame, schema, np.arange(110, 115), ['C'])[0]['C'] is None
    frame.loc[:109, 'C'] = 'a'
    assert model.fit_trees(frame, schema, np.arange(110, 115), ['C'])[0]['C'] is None


def test_partial_mask_cannot_enter_tree_fit():
    frame, schema = fixture_frame(110, 5)
    frame.loc[110, PARENT] = '1'
    with pytest.raises(ValueError, match='mask'):
        model.fit_trees(frame, schema, np.arange(110, 115), ['C'])


def run_policy(monkeypatch, bad_validation=False, no_gain=False):
    frame, schema = fixture_frame()
    fit, selection, validation = model.split_visible(np.arange(2000))
    seen, events = [], []

    def base(f, s):
        complete = np.flatnonzero(f[[PARENT, 'C']].notna().all(axis=1))
        seen.append(('base', complete))
        return stub_base(f, s)

    def trees(f, s, query, leaves):
        complete = np.flatnonzero(f[[PARENT, 'C']].notna().all(axis=1))
        seen.append(('tree', complete))
        assert f.iloc[query][[PARENT, 'C']].isna().all().all()
        x = f.iloc[query]['X'].astype(int).to_numpy()
        q = np.full((len(query), 2), .5) if no_gain else np.eye(2)[x] * .98 + .01
        if bad_validation and len(complete) < 2000:
            q[np.isin(query, validation)] = q[np.isin(query, validation), ::-1]
        return {'C': q}, {'C': {'asked_rows': len(complete), 'trained': True}}

    monkeypatch.setattr(model, 'fit_trees', trees)
    output = model.predict(frame[['C', 'X', PARENT]], schema, base_predict=base,
                           observer=lambda event, data: events.append((event, data)))
    return frame, schema, fit, selection, validation, seen, events, output


def test_active_policy_is_frozen_before_independent_validation_and_refit(monkeypatch):
    frame, schema, fit, _, _, seen, events, output = run_policy(monkeypatch)
    assert [kind for kind, _ in seen] == ['base', 'tree', 'base', 'tree']
    np.testing.assert_array_equal(seen[0][1], fit)
    np.testing.assert_array_equal(seen[1][1], fit)
    np.testing.assert_array_equal(seen[2][1], np.arange(2000))
    np.testing.assert_array_equal(seen[3][1], np.arange(2000))
    names = [e for e, _ in events]
    assert names.index('shadow_frozen') < names.index('selection_frozen') < names.index('validation_scored') < names.index('policy_frozen') < names.index('refit_frozen')
    details = dict(events)
    assert details['policy_frozen']['shares'] == {'C': .5}
    assert details['validation_scored']['accepted']
    expected = stub_base(frame, schema)
    for i in range(0, len(output), 2):
        np.testing.assert_array_equal(output[i], expected[i])
        assert output[i + 1][-1] == expected[i + 1][-1]
        assert not np.array_equal(output[i + 1], expected[i + 1])


def test_global_validation_rejection_is_exact_full_refit_e041(monkeypatch):
    frame, schema, _, _, _, _, events, output = run_policy(monkeypatch, bad_validation=True)
    assert dict(events)['selection_frozen']['shares'] == {'C': .5}
    assert dict(events)['policy_frozen']['shares'] == {'C': 0.}
    for actual, expected in zip(output, stub_base(frame, schema)):
        np.testing.assert_array_equal(actual, expected)


def test_zero_policy_does_not_score_validation(monkeypatch):
    _, _, _, _, _, seen, events, _ = run_policy(monkeypatch, no_gain=True)
    assert 'validation_scored' not in [name for name, _ in events]
    assert dict(events)['policy_frozen']['shares'] == {'C': 0.}
    assert [kind for kind, _ in seen] == ['base', 'tree', 'base', 'tree']


@pytest.mark.parametrize('mode', ['small', 'other_instrument', 'unknown_given'])
def test_unsupported_inputs_return_original_baseline_object(mode):
    frame, schema = fixture_frame(100 if mode == 'small' else 2000)
    if mode == 'other_instrument':
        schema['items']['P'] = schema['items'].pop(PARENT)
        schema['items']['C']['gate']['parent'] = 'P'
        frame.rename(columns={PARENT: 'P'}, inplace=True)
    elif mode == 'unknown_given':
        frame.loc[0, 'X'] = 'unknown'
    sentinel = [np.array([.1, .9])]
    calls = []
    def base(f, s):
        calls.append(1)
        return sentinel
    assert model.predict(frame, schema, base_predict=base) is sentinel
    assert calls == [1]


def test_invalid_probability_stops_instead_of_silent_fallback():
    with pytest.raises(ValueError, match='probability'):
        model.validate_vectors([np.array([np.nan, 1.])], [PARENT], [0],
                               {PARENT: {'values': ['0', '1']}})
