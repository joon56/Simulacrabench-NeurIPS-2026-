"""Only new source-to-standalone integration boundaries; no scientific fixtures."""
import ast
import types
import unittest
from unittest.mock import Mock
from assemble import BASE, SOURCE, Isolate, build_source

class AssemblyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=build_source()
        cls.module=types.ModuleType('e064_assembly_boundary')
        exec(compile(cls.raw,'<e064-assembly-boundary>','exec'),cls.module.__dict__)

    def test_prefix_isolation_and_factory(self):
        m=self.module
        self.assertTrue(self.raw.startswith(BASE.read_bytes()))
        self.assertIn('_train_on',m._train.__code__.co_names)
        self.assertIn('_Net',m._train_on.__code__.co_names)
        self.assertIn('_e064_train_on',m._e064_train.__code__.co_names)
        self.assertIn('_e064_ConditionalGradientNet',m._e064_train_on.__code__.co_names)
        self.assertIn('_e064_train',m._e064_tune_and_train.__code__.co_names)
        self.assertIs(m._e064_ConditionalGradientNet.__init__,m._Net.__init__)
        self.assertIsNot(m._train,m._e064_train)
        for n in ast.walk(ast.parse(self.raw)):
            modules=([n.module or ''] if isinstance(n,ast.ImportFrom) else
                     [a.name for a in n.names] if isinstance(n,ast.Import) else [])
            self.assertFalse(any(x.startswith(('src','scripts')) for x in modules))

    def test_explicit_controls_and_candidate_dispatch(self):
        m=self.module
        old=m._E064_CONTROL_PREDICT,m._e064_render_predict
        a,b=Mock(return_value='R'),Mock(return_value='H')
        try:
            m._E064_CONTROL_PREDICT,m._e064_render_predict=a,b
            self.assertEqual(m.predict(None,{'items':{}}),'R')
            self.assertEqual(m.predict(None,{'items':{'s3_11_intent_return_12m_lbl':{}}}),'H')
            self.assertIs(b.call_args.kwargs['tune_fn'],m._e064_tune_and_train)
            self.assertIs(b.call_args.kwargs['layer_fn'],m.supervised_layer)
            self.assertEqual(b.call_args.kwargs['configs'],m.CONFIGS)
            self.assertEqual(a.call_count,1)
        finally: m._E064_CONTROL_PREDICT,m._e064_render_predict=old

    def test_every_candidate_definition_matches_transformed_source(self):
        source=ast.parse(SOURCE.read_text(encoding='utf-8'))
        names={n.name:'_e064_'+n.name.lstrip('_') for n in source.body if isinstance(n,(ast.ClassDef,ast.FunctionDef))}
        assembled=ast.parse(self.raw)
        defs={n.name:n for n in assembled.body if isinstance(n,(ast.ClassDef,ast.FunctionDef))}
        for n in source.body:
            if isinstance(n,(ast.ClassDef,ast.FunctionDef)):
                expected=Isolate(names).visit(n)
                self.assertEqual(ast.dump(expected,include_attributes=False),ast.dump(defs[expected.name],include_attributes=False))

if __name__=='__main__': unittest.main()
