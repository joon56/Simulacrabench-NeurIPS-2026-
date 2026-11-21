"""E061 invariants on fabricated tensors/rows, never survey efficacy tests."""
import importlib
import sys
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
import torch

torch.set_num_threads(2)


class TiedHeadsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = importlib.import_module('src.models.tied_content_heads')

    def net(self, columns=((0, (2, 0)),)):
        return self.m.TiedNet(2, [3, 2], [2], (4, 2, 0.), columns)

    def test_schema_mapping_does_not_assume_sentinel_position(self):
        records = {'plain': {'values': ['b', 'a']},
                   'gated': {'values': ['z', 'x'], 'gate': {'parent': 'plain'}}}
        result = self.m.conditional_columns(
            ['plain', 'gated'], records,
            {'plain': ['b', 'a'], 'gated': ['x', 'SKIP', 'z']}, 'SKIP')
        self.assertEqual(result, ((1, (2, 0)),))

    def test_invalid_schema_mapping_fails(self):
        records = {'g': {'values': ['a', 'b'], 'gate': {'parent': 'p'}}}
        for options in (['a', 'b'], ['a', 'SKIP', 'SKIP']):
            with self.assertRaises(ValueError):
                self.m.conditional_columns(['g'], records, {'g': options}, 'SKIP')

    def test_conditional_probability_identity_and_no_extra_parameters(self):
        torch.manual_seed(0)
        net = self.net().eval()
        full, cond = net(torch.tensor([[.3, -.2], [1., .5]]))
        p = full[0].softmax(1)[:, [2, 0]]
        self.assertTrue(torch.allclose(cond[0].softmax(1),
                                       p / p.sum(1, keepdim=True), atol=1e-6, rtol=0))
        self.assertTrue(torch.equal(full[0][:, [2, 0]], cond[0]))
        self.assertFalse(any('cond_heads' in n for n, _ in net.named_parameters()))
        self.assertEqual(len(full), 2)

    def test_extreme_sentinel_logit_is_stable(self):
        net = self.net().eval()
        with torch.no_grad():
            net.full_heads[0].weight.zero_()
            net.full_heads[0].bias.copy_(torch.tensor([1., 10000., -1.]))
        full, cond = net(torch.zeros(3, 2))
        self.assertEqual(float(full[0].detach().softmax(1)[:, [2, 0]].sum()), 0.)
        p = cond[0].detach().softmax(1)
        self.assertTrue(torch.isfinite(p).all())
        self.assertTrue(torch.allclose(p.sum(1), torch.ones(3), atol=1e-6))
        self.assertGreater(float(p[0, 1]), .8)

    def test_full_and_conditional_losses_share_parameter_gradients(self):
        torch.manual_seed(0)
        net = self.net().eval()
        full, cond = net(torch.tensor([[.1, .2], [.5, -.2]]))
        full_loss = torch.nn.functional.cross_entropy(full[0], torch.tensor([0, 1]))
        cond_loss = torch.nn.functional.cross_entropy(cond[0], torch.tensor([0, 1]))
        parameter = net.full_heads[0].weight
        a = torch.autograd.grad(full_loss, parameter, retain_graph=True)[0]
        b = torch.autograd.grad(cond_loss, parameter, retain_graph=True)[0]
        total = torch.autograd.grad(full_loss + cond_loss, parameter)[0]
        self.assertGreater(float(b.abs().sum()), 0.)
        self.assertTrue(torch.equal(b[1], torch.zeros_like(b[1])))
        self.assertTrue(torch.allclose(total, a + b, atol=1e-6, rtol=0))

    def test_asked_mask_and_pooled_denominator_unchanged(self):
        from src.models.shared_trunk import _pooled_ce
        f = [torch.tensor([[1., 2., 0.], [2., -1., 0.], [0., 1., 3.]])]
        c = [f[0][:, [0, 1]]]
        ft, ct = torch.tensor([[0], [1], [2]]), torch.tensor([[0], [1], [-1]])
        expected = (torch.nn.functional.cross_entropy(f[0], ft[:, 0], reduction='sum')
                    + torch.nn.functional.cross_entropy(c[0][:2], ct[:2, 0], reduction='sum')) / 5
        self.assertIs(self.m._pooled_ce, _pooled_ce)
        self.assertTrue(torch.allclose(self.m._pooled_ce(f, c, ft, ct), expected))
        missing = torch.full((3, 1), -1)
        self.assertTrue(torch.allclose(self.m._pooled_ce(f, c, ft, missing),
                                      torch.nn.functional.cross_entropy(f[0], ft[:, 0])))

    def test_heldout_predict_block_never_reaches_training_targets(self):
        schema = {'gated_value': 'SKIP', 'items': {
            'x': {'class': 'GIVEN', 'values': ['fit', 'held']},
            'p': {'class': 'PREDICT', 'values': ['yes', 'no']},
            'c': {'class': 'PREDICT', 'values': ['b', 'a'],
                  'gate': {'parent': 'p', 'observed_if': ['yes']}}}}
        frame = pd.DataFrame({'x': ['fit'] * 80 + ['held'] * 5,
                              'p': ['yes', 'no'] * 40 + [None] * 5,
                              'c': ['a', 'SKIP'] * 40 + [None] * 5})
        target_calls, train_calls = [], []
        original = self.m._targets

        def checked_targets(rows, *args):
            self.assertTrue((rows.x == 'fit').all())
            self.assertFalse(rows[['p', 'c']].isna().any().any())
            target_calls.append(len(rows))
            return original(rows, *args)

        def fake_train(X_fit, full_fit, cond_fit, X_val, full_val, cond_val,
                       full_dims, cond_dims, max_epochs=500, config=(4, 2, 0.),
                       conditional_map=()):
            self.assertTrue(torch.equal(X_fit[:, 1], torch.zeros(len(X_fit))))
            if X_val is not None:
                self.assertTrue(torch.equal(X_val[:, 1], torch.zeros(len(X_val))))
            train_calls.append(len(X_fit))
            return self.m.TiedNet(X_fit.shape[1], full_dims, cond_dims,
                                  config, conditional_map).eval(), 1

        before = frame.copy(deep=True)
        with patch.object(self.m, '_targets', checked_targets), patch.object(
                self.m, '_train', fake_train):
            self.m.tune_and_train(frame, schema, [], (), configs=((4, 2, 0.), (5, 2, 0.)))
        self.assertEqual(len(train_calls), 3)  # injected stubs, not real fits
        self.assertEqual(train_calls[-1], 80)
        self.assertEqual(target_calls[-1], 80)
        pd.testing.assert_frame_equal(frame, before)

    def test_control_dispatch_is_original_e041_and_unhcr_uses_fixed_hook(self):
        marker = object()
        for name in ('unicef', 'world_bank'):
            with patch.object(self.m.supervised_retrieval, 'predict', return_value=marker) as old:
                self.assertIs(self.m.predict('frame', {'items': {}, 'name': name}), marker)
                old.assert_called_once()
        schema = {'items': {'s3_11_intent_return_12m_lbl': {}}}
        with patch.object(self.m.link_sharp, 'predict', return_value=marker) as linked:
            self.assertIs(self.m.predict('frame', schema), marker)
            self.assertIs(linked.call_args.kwargs['tune_fn'], self.m.tune_and_train)
            self.assertIs(linked.call_args.kwargs['layer_fn'], self.m.supervised_retrieval.supervised_layer)
            self.assertEqual(linked.call_args.kwargs['configs'], ((64, 2, 0.), (128, 2, .1)))

    def test_runtime_audit_rejects_heldout_training_target_access(self):
        from scripts.check_e061_tied_heads import CallAudit
        from src.models.shared_trunk import _targets
        audit = CallAudit.__new__(CallAudit)
        audit.n_train, audit.target_calls = 1, 0
        records = {'p': {'class': 'PREDICT', 'values': ['a', 'b']}}
        previous = sys.gettrace()
        try:
            sys.settrace(audit.trace)
            with self.assertRaisesRegex(RuntimeError, 'Held-out PREDICT'):
                _targets(pd.DataFrame({'p': ['a']}, index=[1]), ['p'],
                         {'p': ['a', 'b']}, records, 'SKIP')
        finally:
            sys.settrace(previous)
        self.assertEqual(audit.target_calls, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
