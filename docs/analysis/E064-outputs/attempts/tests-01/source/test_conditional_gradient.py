"""E064 focused artificial contracts, no parquet or previous model artifacts."""
import ast
import importlib
import importlib.util
import inspect
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
import torch

torch.set_num_threads(2)
torch.set_num_interop_threads(2)
from src.models import shared_trunk as r, hh_cap, link_sharp, supervised_retrieval
from scripts import check_e064_conditional_gradient as runner


class GradientTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('src.models.conditional_gradient'),
                             'E064 implementation absent: expected pre-implementation RED')
        return importlib.import_module('src.models.conditional_gradient')

    def nets(self, config=(8, 2, 0.), cond=(2, 1, 2)):
        h = self.module()
        torch.manual_seed(0); a = r._Net(3, [3, 2], cond, config).double()
        state = torch.get_rng_state().clone()
        torch.manual_seed(0); b = h.ConditionalGradientNet(3, [3, 2], cond, config).double()
        self.assertTrue(torch.equal(state, torch.get_rng_state()))
        return a, b

    def tensors(self):
        return (torch.tensor([[.3, -.5, .7], [.1, .2, -.3], [.8, .4, .2], [-.2, .6, .9]], dtype=torch.float64),
                torch.tensor([[0, 1], [1, 0], [2, 1], [1, 1]]),
                torch.tensor([[0, 0, -1], [1, -1, -1], [-1, 0, -1], [1, 0, -1]]))

    def test_initial_state_forward_rng_and_denominator(self):
        x, f, c = self.tensors()
        for config in hh_cap.CONFIGS:
            a, b = self.nets(config)
            self.assertEqual(list(a.state_dict()), list(b.state_dict()))
            self.assertEqual([n for n, _ in a.named_parameters()], [n for n, _ in b.named_parameters()])
            for key in a.state_dict(): self.assertTrue(torch.equal(a.state_dict()[key], b.state_dict()[key]))
            for train in (True, False):
                a.train(train); b.train(train)
                torch.manual_seed(7); fl, cl = a(x); state = torch.get_rng_state().clone()
                torch.manual_seed(7); fh, ch = b(x)
                self.assertTrue(torch.equal(state, torch.get_rng_state()))
                for u, v in zip(fl + cl, fh + ch): self.assertTrue(torch.equal(u, v))
                la = r._pooled_ce(fl, cl, f, c); lb = r._pooled_ce(fh, ch, f, c)
                self.assertTrue(torch.equal(la, lb))
                total = sum(torch.nn.functional.cross_entropy(y, f[:, i], reduction='sum') for i, y in enumerate(fl))
                for j, y in enumerate(cl):
                    mask = c[:, j] >= 0
                    if mask.any(): total += torch.nn.functional.cross_entropy(y[mask], c[mask, j], reduction='sum')
                self.assertEqual(14, f.numel() + int((c >= 0).sum()))
                torch.testing.assert_close(la, total / 14, atol=1e-10, rtol=1e-10)

    def test_branch_gradients_head_learning_and_adam(self):
        a, b = self.nets(); x, f, c = self.tensors()
        fl, cl = a(x); fh, ch = b(x)
        full_loss = sum(torch.nn.functional.cross_entropy(y, f[:, i], reduction='sum') for i, y in enumerate(fl)) / 14
        full_grad = torch.autograd.grad(full_loss, tuple(a.trunk.parameters()), retain_graph=True)
        cond_loss = sum(torch.nn.functional.cross_entropy(y[c[:, j]>=0], c[c[:, j]>=0, j], reduction='sum')
                        for j, y in enumerate(cl) if (c[:, j]>=0).any()) / 14
        cond_grad = torch.autograd.grad(cond_loss, tuple(a.trunk.parameters()), retain_graph=True)
        self.assertGreater(sum(float(g.abs().sum()) for g in cond_grad), 0.)
        detached_loss = torch.nn.functional.cross_entropy(ch[0][c[:, 0]>=0], c[c[:, 0]>=0, 0])
        blocked = torch.autograd.grad(detached_loss, tuple(b.trunk.parameters()), allow_unused=True, retain_graph=True)
        self.assertTrue(all(g is None for g in blocked))
        r._pooled_ce(fl, cl, f, c).backward(); r._pooled_ce(fh, ch, f, c).backward()
        for p, q, gf, gc in zip(a.trunk.parameters(), b.trunk.parameters(), full_grad, cond_grad):
            torch.testing.assert_close(p.grad, gf + gc, atol=1e-10, rtol=1e-10)
            torch.testing.assert_close(q.grad, gf, atol=1e-10, rtol=1e-10)
        for pa, pb in zip(list(a.full_heads.parameters()) + list(a.cond_heads.parameters()),
                          list(b.full_heads.parameters()) + list(b.cond_heads.parameters())):
            if pa.grad is None: self.assertIsNone(pb.grad)
            else: torch.testing.assert_close(pa.grad, pb.grad, atol=1e-10, rtol=1e-10)
        self.assertIsNone(b.cond_heads[2].weight.grad)
        self.assertIsNotNone(b.cond_heads[1].weight.grad)
        self.assertEqual(int(torch.count_nonzero(b.cond_heads[1].weight.grad)), 0)
        before = [p.detach().clone() for p in b.cond_heads.parameters()]
        oa = torch.optim.Adam(a.parameters(), lr=r.LR, weight_decay=r.WEIGHT_DECAY)
        ob = torch.optim.Adam(b.parameters(), lr=r.LR, weight_decay=r.WEIGHT_DECAY)
        oa.step(); ob.step()
        for pa, pb in zip(list(a.full_heads.parameters()) + list(a.cond_heads.parameters()),
                          list(b.full_heads.parameters()) + list(b.cond_heads.parameters())):
            torch.testing.assert_close(pa, pb, atol=1e-10, rtol=1e-10)
            self.assertEqual(set(oa.state[pa]), set(ob.state[pb]))
            for key in oa.state[pa]: torch.testing.assert_close(oa.state[pa][key], ob.state[pb][key], atol=1e-10, rtol=1e-10)
        self.assertFalse(torch.equal(before[0], b.cond_heads[0].weight))
        self.assertFalse(torch.equal(before[2], b.cond_heads[1].weight))  # zero grad still decay
        self.assertTrue(torch.equal(before[4], b.cond_heads[2].weight))  # None skipped
        self.assertEqual(len(ob.state[b.cond_heads[2].weight]), 0)

    def test_no_conditional_heads_and_local_train_factory(self):
        h = self.module(); x, f, _ = self.tensors(); c = torch.zeros((4, 0), dtype=torch.int64)
        a, b = self.nets(cond=())
        for net in (a, b):
            fl, cl = net(x); r._pooled_ce(fl, cl, f, c).backward()
        for pa, pb in zip(a.parameters(), b.parameters()): self.assertTrue(torch.equal(pa.grad, pb.grad))
        ca = (8, 2, 0.)
        a, _ = r._train_on(torch.device('cpu'), x.float(), f, c, None, None, None, [3, 2], [], 2, ca)
        b, epoch = h._train_on(torch.device('cpu'), x.float(), f, c, None, None, None, [3, 2], [], 2, ca)
        self.assertIsInstance(b, h.ConditionalGradientNet); self.assertEqual(epoch, 2)
        for key in a.state_dict(): self.assertTrue(torch.equal(a.state_dict()[key], b.state_dict()[key]))

    def test_original_train_tune_arithmetic_and_entry_dispatch(self):
        h = self.module()
        for name in ('_train', '_train_on', 'tune_and_train'):
            expected = inspect.getsource(getattr(r, name))
            actual = inspect.getsource(getattr(h, name)).replace('ConditionalGradientNet(', '_Net(')
            self.assertEqual(ast.dump(ast.parse(expected)), ast.dump(ast.parse(actual)))
        token = object()
        with patch.object(supervised_retrieval, 'predict', return_value=token) as control:
            self.assertIs(h.predict(None, {'items': {}}), token); control.assert_called_once()
        with patch.object(link_sharp, 'predict', return_value=token) as entry:
            self.assertIs(h.predict(None, {'items': {'s3_11_intent_return_12m_lbl': {}}}), token)
            self.assertIs(entry.call_args.kwargs['tune_fn'], h.tune_and_train)
            self.assertIs(entry.call_args.kwargs['layer_fn'], supervised_retrieval.supervised_layer)
            self.assertEqual(entry.call_args.kwargs['configs'], hh_cap.CONFIGS)


class BoundaryTests(GradientTests):
    # Loader below selects only each class's own tests (no inherited repetition).
    def public_fixture(self, n=8, q=2):
        off = runner.load_module('e064_test_official', runner.KIT / 'score.py')
        cfg = off.load_config(str(runner.KIT / 'config.yml'))
        schema = off.load_schema(str(runner.KIT / 'data/unhcr.json'), cfg)
        frame = pd.DataFrame({name: [off.options_for(schema, name)[i % len(off.options_for(schema, name))]
                                    for i in range(n+q)] for name in off.generated_items(schema)})
        frame.loc[n:, off.scored_items(schema)] = np.nan
        return off, schema, frame

    def test_small_fallback_real_all213_renderer_and_empty_query(self):
        h = self.module(); off, schema, frame = self.public_fixture()
        with patch.object(link_sharp, 'select_ladder', return_value=([], [], [])):
            old = supervised_retrieval.predict(frame, schema, cols=[], kappas=[])
            new = h.predict(frame, schema, cols=[], kappas=[])
            self.assertEqual(len(old), 426)
            for a, b in zip(old, new): np.testing.assert_array_equal(a, b)
            self.assertEqual(h.predict(frame.iloc[:8], schema, cols=[], kappas=[]), [])
        with patch.object(h, '_train', side_effect=AssertionError('Fit in small fallback')):
            self.assertEqual(h.tune_and_train(frame, schema, [], [])[0:2], (0., None))

    def test_tune_roles_two_configs_and_fresh_final_refit(self):
        h = self.module()
        schema = {'gated_value': '__G__', 'items': {
            'x': {'class': 'GIVEN', 'values': ['a','b']},
            'p': {'class': 'PREDICT', 'values': ['0','1']},
            'c': {'class': 'PREDICT', 'values': ['u','v'], 'gate': {'parent':'p','observed_if':['1']}}}}
        frame = pd.DataFrame({'x':['a','b']*32, 'p':['0','1']*32, 'c':['__G__','v','u','v']*16})
        held = frame.iloc[:2].copy(); held[['p','c']] = np.nan
        frame = pd.concat((frame, held), ignore_index=True)
        calls = []; original = h._train
        def tiny(*args, **kw):
            # Fixed 2-epoch engineering backend; real local factory/optimizer.
            calls.append((args, dict(kw)))
            kw['max_epochs'] = 2
            return original(*args, **kw)
        with patch.object(h, '_train', side_effect=tiny):
            w, net, layout = h.tune_and_train(frame, schema, [], [], configs=hh_cap.CONFIGS)
        self.assertEqual(len(calls), 3)
        self.assertEqual([v[1]['config'] for v in calls[:2]], list(hh_cap.CONFIGS))
        self.assertEqual(len(calls[-1][0][0]), 64)
        self.assertIsNone(calls[-1][0][3]); self.assertIn(calls[-1][1]['max_epochs'], (1, 2))
        self.assertIsInstance(net, h.ConditionalGradientNet)
        outer = np.random.default_rng(0).random(64) < .2
        inner = np.random.default_rng(1).random(int((~outer).sum())) < .2
        self.assertEqual(len(calls[0][0][0]), int((~inner).sum()))
        self.assertEqual(len(calls[0][0][3]), int(inner.sum()))
        self.assertTrue(all(int(x.min()) >= 0 for x in (calls[0][0][1], calls[-1][0][1])))

    def test_whole_predict_mask_and_given_only_features(self):
        off, schema, frame = self.public_fixture(3, 2)
        items = off.generated_items(schema)
        train = frame.iloc[:3].copy(); train['respondent_id']=['T0','T1','T2']; train['role']='TRAIN'
        dev = frame.iloc[3:].copy(); dev['respondent_id']=['D0','D1']; dev['role']='DEV'
        for n in off.scored_items(schema): dev[n] = 'POISON_RESPONSE'
        dev['excluded_secret'] = 'DO_NOT_USE'
        masked, cells = runner.masked_phase1(off, schema, train, dev)
        self.assertEqual(len(cells), 426)
        self.assertTrue(masked.iloc[3:][off.scored_items(schema)].isna().all().all())
        self.assertNotIn('excluded_secret', masked)
        records, names, options = r._layout(masked, schema)
        a = r._given_matrix(masked, records, names, options)
        changed = masked.copy(); changed[off.scored_items(schema)] = 'OTHER_POISON'
        b = r._given_matrix(changed, records, names, options)
        np.testing.assert_array_equal(a.toarray(), b.toarray())

    def test_six_output_freeze_and_aggregate_budget_gate(self):
        self.assertEqual(runner.stage_limit('R', 1000., 2000.), 800.)
        self.assertEqual(runner.stage_limit('tests', 1790., 2000.), 10.)
        with self.assertRaises(RuntimeError): runner.stage_limit('H', 1800., 1000.)
        with tempfile.TemporaryDirectory(dir=runner.OUT) as temporary:
            with patch.object(runner, 'OUT', Path(temporary)):
                with self.assertRaises(RuntimeError): runner.require_all_outputs()
        # Actual evaluator gate precedes phase_inputs(with_truth=True).
        source = inspect.getsource(runner.worker)
        self.assertLess(source.index('require_all_outputs()'), source.index('phase_inputs('))


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(cls(name) for cls in (GradientTests, BoundaryTests)
                              for name in cls.__dict__ if name.startswith('test_'))
