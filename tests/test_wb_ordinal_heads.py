"""E062 affected contracts only: no optimizer fitting or response-file reads."""
import copy
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
import torch
from torch.nn import functional as F

from src.models import wb_ordinal_heads as candidate, shared_trunk, hh_cap

torch.set_num_threads(2)
torch.set_num_interop_threads(2)


class OrdinalTests(unittest.TestCase):
    def test_probability_and_nll(self):
        for dtype, atol, rtol in ((torch.float64, 1e-10, 1e-10),
                                   (torch.float32, 1e-6, 1e-5)):
            x = torch.linspace(-3, 3, 42, dtype=dtype).reshape(7, 6).requires_grad_()
            logp = candidate.ordinal_log_probs(x)
            self.assertEqual(tuple(logp.shape), (7, 7))
            r, m = x[:, :5].sigmoid(), x[:, 5:].sigmoid()
            survival = torch.cat((torch.ones_like(m), r.cumprod(1), torch.zeros_like(m)), 1)
            content = survival[:, :-1] - survival[:, 1:]
            expected = torch.cat(((1 - m) * content, m), 1)
            torch.testing.assert_close(logp.exp(), expected, atol=atol, rtol=rtol)
            torch.testing.assert_close(logp.exp().sum(1), torch.ones(7, dtype=dtype), atol=atol, rtol=rtol)
            self.assertTrue(bool((logp.exp() >= 0).all()))
            losses = []
            for row, label in enumerate(range(7)):
                loss = F.binary_cross_entropy_with_logits(x[row, 5], x.new_tensor(float(label == 6)))
                if label < 6:
                    for k in range(5):
                        if label >= k:
                            loss = loss + F.binary_cross_entropy_with_logits(x[row, k], x.new_tensor(float(label > k)))
                losses.append(loss)
            expected_nll = torch.stack(losses)
            nll = F.cross_entropy(logp, torch.arange(7), reduction='none')
            torch.testing.assert_close(nll, expected_nll, atol=atol, rtol=rtol)
            grad = torch.autograd.grad(nll.sum(), x, retain_graph=True)[0]
            expected_grad = torch.autograd.grad(expected_nll.sum(), x)[0]
            torch.testing.assert_close(grad, expected_grad, atol=atol, rtol=rtol)

    def test_extremes_finite_without_floor(self):
        for dtype in (torch.float64, torch.float32):
            x = torch.tensor([[1000]*6, [-1000]*6, [1000,-1000,1000,-1000,1000,-1000]], dtype=dtype, requires_grad=True)
            p = candidate.ordinal_log_probs(x)
            self.assertTrue(bool(torch.isfinite(p).all()))
            self.assertTrue(bool((p.exp() == 0).any()))
            loss = F.cross_entropy(p, torch.tensor([0, 6, 5]))
            loss.backward()
            self.assertTrue(bool(torch.isfinite(x.grad).all()))
            torch.testing.assert_close(p.exp().sum(1), torch.ones(3, dtype=dtype), atol=1e-6, rtol=1e-5)

    def test_nonresponse_and_empty_risk_gradients(self):
        x = torch.tensor([[.2,-.3,.7,-1.,.5,.4], [.1,.2,.3,.4,.5,-.6]], dtype=torch.float64, requires_grad=True)
        lp = candidate.ordinal_log_probs(x)
        F.cross_entropy(lp, torch.tensor([6, 6])).backward()
        torch.testing.assert_close(x.grad[:, :5], torch.zeros_like(x.grad[:, :5]), atol=1e-10, rtol=1e-10)
        self.assertTrue(bool((x.grad[:, 5] < 0).all()))
        x.grad = None
        F.cross_entropy(candidate.ordinal_log_probs(x), torch.tensor([0, 0])).backward()
        torch.testing.assert_close(x.grad[:, 1:5], torch.zeros_like(x.grad[:, 1:5]), atol=1e-10, rtol=1e-10)
        self.assertEqual(tuple(lp.shape), (2, 7))

    def test_original_pooled_count(self):
        x = torch.tensor([[.2,.3,.4,.5,.6,.7], [-.7,-.6,-.5,-.4,-.3,-.2]], dtype=torch.float64)
        lp = candidate.ordinal_log_probs(x)
        other = torch.tensor([[.4,-.2],[.3,.1]], dtype=torch.float64)
        conditional = torch.tensor([[.8,-.4],[.5,-.3]], dtype=torch.float64)
        full_t = torch.tensor([[0,1],[6,0]])
        cond_t = torch.tensor([[1],[-1]])
        total = -lp[0,0]-lp[1,6] + F.cross_entropy(other, full_t[:,1], reduction='sum') + F.cross_entropy(conditional[:1], cond_t[:1,0], reduction='sum')
        actual = shared_trunk._pooled_ce([lp,other], [conditional], full_t, cond_t)
        torch.testing.assert_close(actual, total/5, atol=1e-10, rtol=1e-10)

    def test_initial_parameters_and_rng_both_configs(self):
        for config in hh_cap.CONFIGS:
            torch.manual_seed(0)
            baseline = shared_trunk._Net(4, [7,3,7], [2], config)
            original_rng = torch.get_rng_state().clone()
            torch.manual_seed(0)
            net = candidate.OrdinalNet(4, [7,3,7], [2], config, (0,2))
            self.assertTrue(torch.equal(original_rng, torch.get_rng_state()))
            for prefix in ('trunk.', 'full_heads.1.', 'cond_heads.'):
                for key, value in baseline.state_dict().items():
                    if key.startswith(prefix):
                        self.assertTrue(torch.equal(value, net.state_dict()[key]), key)
            for i in (0,2):
                self.assertTrue(torch.equal(net.full_heads[i].weight, baseline.full_heads[i].weight[[0,1,2,3,4,6]]))
                self.assertTrue(torch.equal(net.full_heads[i].bias, baseline.full_heads[i].bias[[0,1,2,3,4,6]]))
            baseline.eval(); net.eval()
            given = torch.ones(2,4)
            bf, bc = baseline(given); nf, nc = net(given)
            self.assertTrue(torch.equal(bf[1], nf[1]))
            self.assertTrue(torch.equal(bc[0], nc[0]))

    def schema(self):
        items = {'given': {'class':'GIVEN', 'values':['a','b'], 'gate':None}}
        items.update({name:{'class':'PREDICT', 'values':list(candidate.LABELS), 'gate':None} for name in candidate.TARGETS})
        return {'items':items, 'gated_value':'NA_GATED'}

    def test_schema_exact_and_no_partial_rescue(self):
        schema = self.schema()
        records, items, options = candidate._layout(pd.DataFrame(columns=schema['items']), schema)
        predicted = [n for n in items if records[n]['class']=='PREDICT']
        self.assertEqual(candidate.ordinal_indices(predicted, records, options), tuple(range(16)))
        for mutation in ('missing','order','gate','class'):
            bad = copy.deepcopy(schema)
            name = candidate.TARGETS[0]
            if mutation == 'missing': del bad['items'][name]
            elif mutation == 'order': bad['items'][name]['values'].reverse()
            elif mutation == 'gate': bad['items'][name]['gate']={'parent':'given','observed_if':['a']}
            else: bad['items'][name]['class']='GIVEN'
            rec, names, opt = candidate._layout(pd.DataFrame(columns=bad['items']), bad)
            pred=[n for n in names if rec[n]['class']=='PREDICT']
            with self.assertRaises(ValueError): candidate.ordinal_indices(pred, rec, opt)

    def test_small_fit_fallback_without_optimizer(self):
        schema=self.schema()
        frame=pd.DataFrame({'given':['a']*3, **{n:[candidate.LABELS[0]]*3 for n in candidate.TARGETS}})
        with patch.object(candidate, '_train', side_effect=AssertionError('Unexpected fit')):
            w, net, layout=candidate.tune_and_train(frame,schema,[],[])
        self.assertEqual(w,0.); self.assertIsNone(net); self.assertEqual(len(layout[0]),16)

    def test_full_query_mask_and_exclude(self):
        from scripts.check_e062_wb_ordinal import masked_phase1, load_module, KIT
        official=load_module('e062_test_official',KIT/'score.py')
        schema=self.schema(); schema['items']['secret']={'class':'EXCLUDE','values':['hidden'],'gate':None}
        train=pd.DataFrame({'respondent_id':[1], 'role':['TRAIN'], 'given':['a'], **{n:[candidate.LABELS[1]] for n in candidate.TARGETS}})
        dev=pd.DataFrame({'respondent_id':[2], 'role':['DEV'], 'given':['b'], **{n:[candidate.LABELS[5]] for n in candidate.TARGETS}, 'secret':['hidden']})
        frame,cells=masked_phase1(official,schema,train,dev)
        self.assertNotIn('secret',frame)
        self.assertTrue(frame.loc[1,list(candidate.TARGETS)].isna().all())
        self.assertEqual([c[2] for c in cells],list(candidate.TARGETS))
        self.assertEqual(frame.loc[1,'given'],'b')

    def test_zero_weight_still_refits_with_frozen_config_epoch(self):
        # Engineering fake neural endpoint only; actual tune/w/refit orchestration.
        schema=self.schema()
        frame=pd.DataFrame({'given':['a']*25, **{n:[candidate.LABELS[0]]*25 for n in candidate.TARGETS}})
        class UniformNet(torch.nn.Module):
            def __init__(self):
                super().__init__(); self.anchor=torch.nn.Parameter(torch.zeros(1))
            def forward(self,x):
                return [torch.zeros(len(x),7) for _ in range(16)], []
        calls=[]
        def fake_train(*args,**kwargs):
            calls.append((args,kwargs))
            return UniformNet(),3
        with patch.object(candidate,'_train',side_effect=fake_train):
            w,net,_=candidate.tune_and_train(frame,schema,[],[],configs=hh_cap.CONFIGS)
        self.assertEqual(w,0.)
        self.assertEqual(len(calls),3)
        self.assertEqual(len(calls[-1][0][0]),25)
        self.assertIsNone(calls[-1][0][3])
        self.assertEqual(calls[-1][1]['max_epochs'],3)
        self.assertEqual(calls[-1][1]['config'],hh_cap.CONFIGS[0])

    def test_dispatch_and_inactive_tune_path(self):
        schema=self.schema()
        with patch.object(candidate.link_sharp,'predict',return_value='inactive') as call:
            self.assertEqual(candidate.predict(pd.DataFrame(),schema),'inactive')
            self.assertIs(call.call_args.kwargs['tune_fn'],candidate.tune_and_train)
            self.assertIs(call.call_args.kwargs['layer_fn'],candidate.hh_sharp_layer)
        with patch.object(candidate.supervised_retrieval,'predict',return_value='control') as call:
            self.assertEqual(candidate.predict(pd.DataFrame(),{'items':{}}),'control')
            call.assert_called_once()


class HarnessTests(unittest.TestCase):
    def test_reader_role_filters_and_dev_projection(self):
        from scripts import check_e062_wb_ordinal as runner
        official=runner.load_module('e062_reader_official',runner.KIT/'score.py')
        schema={'gated_value':'NA_GATED','items':{
            'g':{'class':'GIVEN','values':['a'],'gate':None},
            'y':{'class':'PREDICT','values':['b'],'gate':None},
            'excluded':{'class':'EXCLUDE','values':None,'gate':None}}}
        def endpoint(path,columns,filters):
            role=filters[0][2]
            return pd.DataFrame({k:[role if k=='role' else 1 if k=='respondent_id' else 'a' if k=='g' else 'b'] for k in columns})
        with patch.object(pd,'read_parquet',side_effect=endpoint) as reader:
            train,dev=runner.phase_frames(pd,official,schema,'world_bank')
        self.assertEqual(reader.call_count,2)
        self.assertEqual(reader.call_args_list[0].kwargs['filters'],[('role','==','TRAIN')])
        self.assertEqual(reader.call_args_list[1].kwargs['filters'],[('role','==','DEV')])
        self.assertEqual(list(train.columns),['respondent_id','role','g','y'])
        self.assertEqual(list(dev.columns),['respondent_id','role','g'])
        with patch.object(pd,'read_parquet',side_effect=endpoint) as reader:
            _,dev=runner.phase_frames(pd,official,schema,'world_bank',with_truth=True)
        self.assertEqual(list(dev.columns),['respondent_id','role','g','y'])

    def test_nine_outputs_required_before_evaluation(self):
        from scripts import check_e062_wb_ordinal as runner
        missing=set()
        def metadata(path):
            name=path.name
            if name in missing: raise FileNotFoundError(name)
            if name.endswith('-resources.json'): return {'status':'PASS'}
            return {'outputs':{n:{'file':name+n+'.npz','sha256':'frozen'} for n in runner.NAMES}}
        with patch.object(runner,'read',side_effect=metadata),patch.object(runner,'sha',return_value='frozen'):
            self.assertEqual(len(runner.require_all_outputs()),9)
            missing.add('candidate-complete.json')
            with self.assertRaises(FileNotFoundError): runner.require_all_outputs()
        with patch.object(runner,'read',side_effect=metadata),patch.object(runner,'sha',return_value='changed'):
            with self.assertRaises(RuntimeError): runner.require_all_outputs()

    def test_all_wb_targets_missing_cannot_silently_fallback(self):
        schema={'gated_value':'NA_GATED','items':{
            'participant_id':{'class':'EXCLUDE','values':None,'gate':None},
            'group':{'class':'GIVEN','values':['a'],'gate':None}}}
        with patch.object(candidate.link_sharp,'predict',return_value='wb_path') as path:
            self.assertEqual(candidate.predict(pd.DataFrame(),schema),'wb_path')
            self.assertIs(path.call_args.kwargs['tune_fn'],candidate.tune_and_train)
        with self.assertRaises(ValueError): candidate.tune_and_train(pd.DataFrame(),schema,[],[])


if __name__ == '__main__':
    unittest.main()
