"""New E061 assembly boundaries only; no survey data, fitting or scoring."""
import ast
import types
import unittest
from unittest.mock import Mock

import torch

from scripts.assemble_e061 import BASE, build_source
from src.models import tied_content_heads as source


class AssemblyBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = build_source()
        cls.module = types.ModuleType('e061_assembly_fixture')
        exec(compile(cls.raw, '<e061-assembly-fixture>', 'exec'), cls.module.__dict__)

    def test_frozen_control_prefix_and_no_repository_import(self):
        self.assertTrue(self.raw.startswith(BASE.read_bytes()))
        tree = ast.parse(self.raw)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                self.assertFalse((node.module or '').startswith(('src', 'scripts')))
        self.assertNotIn(b'SimulacraBench', self.raw)
        self.assertNotIn(b'sys.path', self.raw)

    def test_original_and_tied_training_globals_are_distinct(self):
        m = self.module
        self.assertIn('_train_on', m._train.__code__.co_names)
        self.assertNotIn('_e061_train_on', m._train.__code__.co_names)
        self.assertIn('_Net', m._train_on.__code__.co_names)
        self.assertIn('_e061_train_on', m._e061_train.__code__.co_names)
        self.assertIn('_e061_TiedNet', m._e061_train_on.__code__.co_names)
        self.assertIn('_train', m.tune_and_train.__code__.co_names)
        self.assertIn('_e061_train', m._e061_tune_and_train.__code__.co_names)
        self.assertIsNot(m._train, m._e061_train)
        self.assertIsNot(m._Net, m._e061_TiedNet)

    def test_control_and_unhcr_dispatch_use_explicit_bindings(self):
        m = self.module
        old_control, old_renderer = m._E061_CONTROL_PREDICT, m._e061_render_predict
        control, renderer = Mock(return_value='control'), Mock(return_value='tied')
        try:
            m._E061_CONTROL_PREDICT, m._e061_render_predict = control, renderer
            self.assertEqual(m.predict(None, {'items': {}}), 'control')
            self.assertEqual(m.predict(None, {'items': {'s3_11_intent_return_12m_lbl': {}}}), 'tied')
            self.assertIs(renderer.call_args.kwargs['tune_fn'], m._e061_tune_and_train)
            self.assertIs(renderer.call_args.kwargs['layer_fn'], m.supervised_layer)
            self.assertEqual(renderer.call_args.kwargs['configs'], m.CONFIGS)
            self.assertEqual(control.call_count, 1)
        finally:
            m._E061_CONTROL_PREDICT, m._e061_render_predict = old_control, old_renderer

    def test_tied_source_network_forward_and_mapping_exact(self):
        records = {'a': {'gate': {'parent': 'g'}, 'values': ['yes', 'no']}}
        options = {'a': ['no', 'NA', 'yes']}
        expected = source.conditional_columns(['a'], records, options, 'NA')
        actual = self.module._e061_conditional_columns(['a'], records, options, 'NA')
        self.assertEqual(actual, expected)
        torch.manual_seed(0)
        left = source.TiedNet(2, [3], [2], (4, 1, 0.), expected).eval()
        torch.manual_seed(0)
        right = self.module._e061_TiedNet(2, [3], [2], (4, 1, 0.), actual).eval()
        with torch.no_grad():
            x = torch.tensor([[0., 1.], [2., -3.]])
            a, b = left(x), right(x)
        for group_a, group_b in zip(a, b):
            for va, vb in zip(group_a, group_b):
                torch.testing.assert_close(va, vb, rtol=0, atol=0)


if __name__ == '__main__':
    unittest.main()
