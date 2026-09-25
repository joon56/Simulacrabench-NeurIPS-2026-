"""E057 assembly parity fixtures; no efficacy evidence."""
import ast
import importlib.util
from pathlib import Path

import numpy as np
import pytest

from scripts.assemble_e057 import build_source
from src.models import conditional_leaf_content as source
from tests.test_e057_conditional_content import fixture_frame, stub_base


@pytest.fixture(scope='module')
def assembled(tmp_path_factory):
    path = tmp_path_factory.mktemp('e057') / 'main.py'
    path.write_bytes(build_source())
    spec = importlib.util.spec_from_file_location('e057_test_assembly', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_archive_source_is_deterministic_and_local_import_free():
    raw = build_source()
    assert raw == build_source()
    assert raw.startswith(Path('submissions/2026-09-19-E041/main.py').read_bytes())
    assert not any(isinstance(n, ast.ImportFrom) and (n.module or '').startswith('src')
                   for n in ast.walk(ast.parse(raw)))


@pytest.mark.parametrize('mode', ['active', 'reject', 'zero', 'sparse'])
def test_complete_active_and_fallback_policy_parity(assembled, monkeypatch, mode):
    frame, schema = fixture_frame()
    _, _, validation = source.split_visible(np.arange(2000))

    def trees(f, s, query, leaves):
        x = f.iloc[query]['X'].astype(int).to_numpy()
        q = np.eye(2)[x] * .98 + .01
        if mode == 'zero':
            q[:] = .5
        if mode == 'reject' and len(query) > 6:
            q[np.isin(query, validation)] = q[np.isin(query, validation), ::-1]
        return {'C': None if mode == 'sparse' else q}, {'C': {'trained': mode != 'sparse'}}

    monkeypatch.setattr(source, 'incumbent_predict', stub_base)
    monkeypatch.setattr(source, 'fit_trees', trees)
    monkeypatch.setattr(assembled, '_e057_incumbent_predict', stub_base)
    monkeypatch.setattr(assembled, '_e057_fit_trees', trees)
    events = []
    expected = source.predict(frame[['C', 'X', 's3_11_intent_return_12m_lbl']], schema)
    actual = assembled.predict(frame, schema, observer=lambda n, d: events.append((n, d)))
    assert len(actual) == len(expected)
    for a, b in zip(actual, expected):
        np.testing.assert_array_equal(a, b)
    shares = dict(events)['policy_frozen']['shares']
    assert shares == {'C': .5 if mode == 'active' else 0.}
    assert [n for n, _ in events].index('policy_frozen') < [n for n, _ in events].index('refit_frozen')


def test_nonunit_zero_mass_floor_and_sparse_parity(assembled):
    p = np.array([[.1, .3, .8], [0., 0., .7]])
    q = np.array([[.9, .1], [.2, .8]])
    for alpha in (0., .25, .5):
        a = assembled._e057_mix_content(p, q, alpha)
        np.testing.assert_array_equal(a, source.mix_content(p, q, alpha))
        np.testing.assert_array_equal(a[:, -1], p[:, -1])
        np.testing.assert_allclose(a.sum(1), p.sum(1), atol=1e-15)
        np.testing.assert_array_equal(assembled._e057_floor_mix(a), source.floor_mix(a))
    assert assembled._e057_mix_content(p, None, .5) is p


def test_release_refuses_existing_outputs_before_loading_inputs(tmp_path, monkeypatch):
    from scripts import release_e057 as release
    monkeypatch.setattr(release, 'OUT', tmp_path)
    with pytest.raises(FileExistsError, match='occupied'):
        release.preflight()


def test_release_detects_changed_frozen_input(tmp_path, monkeypatch):
    import hashlib
    import json
    from scripts import release_e057 as release
    model = tmp_path / 'model.py'
    model.write_bytes(b'original')
    (tmp_path / 'preflight.json').write_text(json.dumps({'hashes': {
        'model.py': hashlib.sha256(b'original').hexdigest()}}))
    monkeypatch.setattr(release, 'ROOT', tmp_path)
    monkeypatch.setattr(release, 'OUT', tmp_path)
    release.verify_freeze()
    model.write_bytes(b'changed')
    with pytest.raises(AssertionError, match='freeze changed'):
        release.verify_freeze()
