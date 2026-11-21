"""New E062 assembly boundaries only; no survey fit/optimizer or scoring."""
import ast
import types
import unittest
from unittest.mock import Mock
from pathlib import Path

import torch
from src.models import wb_ordinal_heads as source


class AssemblyBoundaryTests(unittest.TestCase):
    def assembly(self):
        if not (Path(__file__).resolve().parents[1] / 'scripts/assemble_e062.py').exists():
            self.fail('E062 assembler not implemented')
        from scripts.assemble_e062 import BASE, build_source
        raw = build_source()
        module = types.ModuleType('e062_assembly_fixture')
        exec(compile(raw, '<e062-assembly-fixture>', 'exec'), module.__dict__)
        return BASE, raw, module

    def test_frozen_prefix_and_standalone_import(self):
        base, raw, module = self.assembly()
        self.assertTrue(raw.startswith(base.read_bytes()))
        for node in ast.walk(ast.parse(raw)):
            if isinstance(node, ast.ImportFrom):
                self.assertFalse((node.module or '').startswith(('src', 'scripts')))
        self.assertNotIn(b'sys.path', raw)
        self.assertNotIn(b'SimulacraBench', raw)
        self.assertTrue(callable(module.predict))

    def test_original_and_ordinal_bindings_are_distinct(self):
        _, _, m = self.assembly()
        self.assertIn('_Net', m._train_on.__code__.co_names)
        self.assertIn('_train_on', m._train.__code__.co_names)
        self.assertIn('_e062_train_on', m._e062_train.__code__.co_names)
        self.assertIn('_e062_OrdinalNet', m._e062_train_on.__code__.co_names)
        self.assertIn('_e062_train', m._e062_tune_and_train.__code__.co_names)
        self.assertIn('_train', m.tune_and_train.__code__.co_names)
        self.assertIs(m._e062_OrdinalNet.__bases__[0], m._Net)
        self.assertIsNot(m._train_on, m._e062_train_on)

    def test_three_dispatches_and_wb_factory(self):
        _, _, m = self.assembly()
        control, renderer = Mock(return_value='control'), Mock(return_value='ordinal')
        m._E062_CONTROL_PREDICT, m._e062_render_predict = control, renderer
        for items in ({'faith': {}}, {'s3_11_intent_return_12m_lbl': {}}):
            self.assertEqual(m.predict(None, {'items': items}), 'control')
        self.assertEqual(m.predict(None, {'items': {'participant_id': {}, 'group': {}}}), 'ordinal')
        self.assertEqual(control.call_count, 2)
        self.assertIs(renderer.call_args.kwargs['tune_fn'], m._e062_tune_and_train)
        self.assertIs(renderer.call_args.kwargs['layer_fn'], m.hh_sharp_layer)
        self.assertEqual(renderer.call_args.kwargs['configs'], m.CONFIGS)

    def test_no_fit_source_assembly_forward_and_rng_exact(self):
        _, _, m = self.assembly()
        for config in ((4, 1, 0.), (4, 1, .1)):
            torch.manual_seed(0)
            left = source.OrdinalNet(2, [7, 3], [], config, (0,)).eval()
            left_rng = torch.get_rng_state().clone()
            torch.manual_seed(0)
            right = m._e062_OrdinalNet(2, [7, 3], [], config, (0,)).eval()
            self.assertTrue(torch.equal(left_rng, torch.get_rng_state()))
            with torch.no_grad():
                x = torch.tensor([[0., 1.], [2., -3.]])
                for group_a, group_b in zip(left(x), right(x)):
                    for a, b in zip(group_a, group_b):
                        torch.testing.assert_close(a, b, rtol=0, atol=0)


if __name__ == '__main__':
    unittest.main()
