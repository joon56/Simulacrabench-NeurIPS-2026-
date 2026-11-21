"""Isolated source/assembly arithmetic and candidate integration checks."""
import ast
import importlib.util
import numpy as np
import pytest

from scripts.assemble_e060 import BASE, build_source
from src.models import content_target_retrieval as source
from tests.test_content_target_retrieval import objective_case
from tests.test_supervised_retrieval import _layer_case


@pytest.fixture(scope='module')
def assembly(tmp_path_factory):
    path = tmp_path_factory.mktemp('e060') / 'main.py'
    path.write_bytes(build_source())
    spec = importlib.util.spec_from_file_location('e060_fixture', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_frozen_prefix_and_no_repository_imports():
    raw = build_source()
    assert raw == build_source()
    assert raw.startswith(BASE.read_bytes())
    assert not any(isinstance(n, ast.ImportFrom) and (n.module or '').startswith('src')
                   for n in ast.walk(ast.parse(raw)))


def test_masked_objective_exact_parity(assembly):
    params, args = objective_case()
    mask = np.ones((9, 4), dtype=bool)
    mask[::2, 1:3] = False
    actual = assembly._e060_metric_objective(params, *args, cell_mask=mask)
    expected = source.metric_objective(params, *args, cell_mask=mask)
    assert actual[0] == expected[0]
    np.testing.assert_array_equal(actual[1], expected[1])


@pytest.mark.parametrize('active', [False, True])
def test_layer_active_and_inactive_parity(assembly, monkeypatch, active):
    frame, schema, item = _layer_case()
    model_dists = {item: np.full((len(frame), 5), .2)}
    def fit(*args, **kwargs):
        assert kwargs['sentinel_codes'] == [-1]
        return [np.ones(1)], [0] if active else [], []
    monkeypatch.setattr(source, 'fit_sections', fit)
    monkeypatch.setattr(assembly, '_e060_fit_sections', fit)
    expected, expected_lambda = source.supervised_layer(frame, schema, model_dists)
    actual, actual_lambda = assembly._e060_supervised_layer(frame, schema, model_dists)
    assert actual_lambda == expected_lambda
    assert actual.keys() == expected.keys()
    for row in expected:
        assert actual[row][1] == expected[row][1]
        for name in expected[row][0]:
            np.testing.assert_array_equal(actual[row][0][name], expected[row][0][name])
