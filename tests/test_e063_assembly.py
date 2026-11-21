"""Only new assembly namespace/dispatch boundaries; no fit or score."""
import ast
import types
import unittest
from unittest.mock import Mock


class AssemblyBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from scripts.assemble_e063 import BASE, build_source
        cls.raw = build_source()
        cls.base = BASE.read_bytes()

    def assembly(self):
        module = types.ModuleType('e063_assembly_fixture')
        exec(compile(self.raw, '<e063-assembly-fixture>', 'exec'), module.__dict__)
        return module

    def test_exact_prefix_and_standalone_import(self):
        self.assertTrue(self.raw.startswith(self.base))
        for n in ast.walk(ast.parse(self.raw)):
            if isinstance(n, ast.ImportFrom):
                self.assertFalse((n.module or '').startswith(('src', 'scripts')))
        self.assertNotIn(b'sys.path', self.raw)
        self.assertNotIn(b'SimulacraBench', self.raw)
        self.assertTrue(callable(self.assembly().predict))

    def test_original_globals_and_round_helpers_are_isolated(self):
        m = self.assembly()
        for name in ('metric_objective', 'fit_sections', '_replace_evidence'):
            self.assertIsNot(getattr(m, name), getattr(m, '_e063_' + name.lstrip('_')))
        self.assertIsNot(m.LAST_DIAGNOSTICS, m._e063_LAST_DIAGNOSTICS)
        self.assertIn('fit_sections', m.supervised_layer.__code__.co_names)
        self.assertIn('_e063_fit_sections', m._e063_round_layer.__code__.co_names)
        self.assertIn('_retrieval_log', m._e063_fit_sections.__code__.co_names)
        self.assertIs(m._e063_fit_sections.__globals__['_retrieval_log'], m._retrieval_log)
        self.assertIn('supervised_layer', m._E063_CONTROL_PREDICT.__code__.co_names)
        self.assertIn('tune_and_train', m._e063_render_predict.__code__.co_names)

    def test_real_control_fallback_and_supported_dispatch_without_fit(self):
        import numpy as np
        import pandas as pd
        m = self.assembly()
        control, renderer = Mock(return_value='R'), Mock(return_value='H')
        m._E063_CONTROL_PREDICT, m._e063_render_predict = control, renderer
        for marker in ('faith', 'participant_id'):
            self.assertEqual(m.predict(None, {'items': {marker: {}}}), 'R')
        target = 's3_11_intent_return_12m_lbl'
        items = {'wave': {'class': 'GIVEN', 'values': ['1', '2']}}
        items.update({f'g{i}': {'class': 'GIVEN', 'values': ['a']} for i in range(16)})
        items[target] = {'class': 'PREDICT', 'values': ['a', 'b']}
        frame = pd.DataFrame({k: ['a'] * 801 for k in items})
        frame['wave'] = ['1', '2'] * 400 + ['1']
        frame.loc[800, target] = np.nan
        self.assertEqual(m.predict(frame, {'items': items}), 'H')
        self.assertIs(renderer.call_args.kwargs['layer_fn'], m._e063_round_layer)
        self.assertIs(renderer.call_args.kwargs['configs'], m.CONFIGS)
        self.assertTrue(m._e063_LAST_DIAGNOSTICS['eligible'])
        frame.loc[0, 'wave'] = 'unknown'
        self.assertEqual(m.predict(frame, {'items': items}), 'R')
        self.assertEqual(renderer.call_count, 1)
        self.assertEqual(control.call_count, 3)
        self.assertEqual(m.LAST_DIAGNOSTICS, {})


if __name__ == '__main__':
    unittest.main()
