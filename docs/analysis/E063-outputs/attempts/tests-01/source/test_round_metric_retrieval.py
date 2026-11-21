"""E063 new artificial-fixture contracts; no survey or cached outputs."""
import importlib
import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
import pandas as pd
from scipy.special import softmax

ROOT = Path(__file__).resolve().parents[1]


class MetricTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(importlib.util.find_spec('src.models.round_metric_retrieval'),
                             'E063 implementation is absent')
        return importlib.import_module('src.models.round_metric_retrieval')

    def fixture(self):
        x = np.array([[[1, 0, 1], [0, 1, 0], [1, 1, 0]],
                      [[0, 1, 1], [1, 0, 0], [0, 0, 1]],
                      [[1, 0, 0], [0, 1, 1], [1, 1, 1]],
                      [[0, 1, 0], [1, 0, 1], [0, 0, 0]]], dtype=float)
        matches = np.array([[[1, 0], [0, 1], [0, 0]],
                            [[0, 1], [1, 0], [0, 0]],
                            [[1, 0], [0, 0], [0, 1]],
                            [[0, 0], [1, 0], [0, 1]]], dtype=float)
        return x, matches, np.full((4, 2), .25), np.array([3, 4]), np.array([14., 1., 2.]), np.array([1, 0, 0, 1])

    def test_common_reduction(self):
        h = self.module()
        from src.models import supervised_retrieval as r
        x, m, pr, sizes, initial, waves = self.fixture()
        w = np.array([1.2, 2.3, .7]); eta = -.4
        old, go = r.metric_objective(np.r_[w, eta], x, m, pr, sizes, initial)
        new, gn = h.metric_objective(np.r_[w, w, eta], x, m, pr, sizes, initial, waves)
        np.testing.assert_allclose(new, old, atol=1e-10, rtol=1e-10)
        np.testing.assert_allclose(gn[:3] + gn[3:6], go[:3], atol=1e-10, rtol=1e-10)
        np.testing.assert_allclose(gn[-1], go[-1], atol=1e-10, rtol=1e-10)

    def test_gradient_and_bounds_extremes(self):
        h = self.module(); args = self.fixture()
        p = np.array([1.1, 2.2, 3.3, 2.4, 1.3, .9, -.7])
        value, g = h.metric_objective(p, *args)
        numeric = []
        for j in range(len(p)):
            a, b = p.copy(), p.copy(); a[j] += 1e-6; b[j] -= 1e-6
            numeric.append((h.metric_objective(a, *args)[0] - h.metric_objective(b, *args)[0]) / 2e-6)
        np.testing.assert_allclose(g, numeric, atol=1e-6, rtol=1e-5)
        for weights, eta in ((0., -5.), (12., 5.)):
            loss, grad = h.metric_objective(np.r_[np.full(6, weights), eta], *args)
            self.assertTrue(np.isfinite(loss) and np.isfinite(grad).all())

    def test_constant_invariance_and_round_reversal(self):
        h = self.module()
        x = np.array([[[1., 0., 1.], [0., 1., 1.]],
                      [[1., 0., 1.], [0., 1., 1.]]])
        w = np.array([[2., 1., 0.], [1., 2., 0.]])
        pi = h.round_posterior(x, w, np.array([0, 1]))
        self.assertGreater(pi[0, 0], pi[0, 1]); self.assertLess(pi[1, 0], pi[1, 1])
        w[:, 2] = [12., 7.]
        np.testing.assert_allclose(h.round_posterior(x, w, np.array([0, 1])), pi, atol=1e-10, rtol=1e-10)
        np.testing.assert_allclose(pi.sum(axis=1), 1., atol=1e-10, rtol=1e-10)

    def test_optimizer_sees_F_only_and_frozen_bounds(self):
        h = self.module()
        codes = np.array([[i % 2, (i // 2) % 2, (i // 3) % 2] for i in range(48)])
        labels = (np.arange(48) % 2)[:, None]
        bank, fit, select = np.arange(40), np.arange(40, 44), np.arange(44, 48)
        waves = np.arange(48) % 2
        calls = []
        def optimizer(fun, start, args, **kw):
            self.assertEqual(len(start), 7)
            self.assertEqual(kw['bounds'], [(0., 12.)] * 6 + [(-5., 5.)])
            self.assertEqual(kw['options'], {'maxiter': 50, 'ftol': 1e-7})
            self.assertEqual(kw['method'], 'L-BFGS-B'); self.assertTrue(kw['jac'])
            self.assertEqual(args[0].shape[0], 4)
            calls.append(tuple(np.array(a, copy=True) for a in args))
            fun(start, *args)
            return SimpleNamespace(x=start.copy(), nit=0)
        with patch.object(h, 'minimize', optimizer):
            first = h.fit_sections(codes, labels, bank, fit, select, np.array([14., 1., 2.]), [2], [[0]], waves)
            changed = labels.copy(); changed[select] = 1 - changed[select]
            second = h.fit_sections(codes, changed, bank, fit, select, np.array([14., 1., 2.]), [2], [[0]], waves)
        for a, b in zip(calls[0], calls[1]): np.testing.assert_array_equal(a, b)
        np.testing.assert_array_equal(first[0], second[0])
        self.assertEqual(calls[0][4][0], 14.)


class EntryTests(MetricTests):
    # Inherited math tests are not duplicated in the registered suite.
    def schema(self):
        from scripts import check_e063_round_metric as runner
        official = runner.load_module('e063_test_official', runner.KIT / 'score.py')
        config = official.load_config(str(runner.KIT / 'config.yml'))
        return official, official.load_schema(str(runner.KIT / 'data/unhcr.json'), config)

    def frame(self, n=600, q=2):
        official, schema = self.schema()
        items = official.generated_items(schema); pred = official.scored_items(schema)
        frame = pd.DataFrame({name: [official.options_for(schema, name)[i % len(official.options_for(schema, name))]
                                     for i in range(n + q)] for name in items})
        frame['wave'] = ['2' if i % 2 == 0 else '1' for i in range(n + q)]
        order = np.random.default_rng(4101).permutation(n)
        nf, ns = min(1200, max(1, n // 5)), min(800, max(1, n // 10))
        for subset in (order[:nf], order[nf:nf+ns]):
            for j, ix in enumerate(subset): frame.loc[ix, 'wave'] = '1' if j % 2 == 0 else '2'
        frame.loc[n:, pred] = np.nan
        return official, schema, frame

    def test_support_and_original_dispatch(self):
        h = self.module(); r = h.original
        _, schema, good = self.frame()
        wave, support = h.round_support(good, schema)
        self.assertTrue(support['eligible'])
        np.testing.assert_array_equal(wave, good.wave.map({'1': 0, '2': 1}).to_numpy())
        cases = []
        one = good.copy(); one.wave = '1'; cases.append(one)
        unknown = good.copy(); unknown.loc[600, 'wave'] = 'unknown'; cases.append(unknown)
        sparse = good.copy(); select = np.random.default_rng(4101).permutation(600)[120:180]
        sparse.loc[select[0], 'wave'] = '2'; cases.append(sparse)
        cases.append(good.iloc[:12].copy()); cases.append(good.iloc[:600].copy())
        token = [np.array([.2, .8])]
        for frame in cases:
            with patch.object(r, 'predict', return_value=token) as common, patch.object(h, 'minimize', side_effect=AssertionError('H fit in fallback')):
                actual = h.predict(frame, schema)
                self.assertIs(actual, token); common.assert_called_once()
                self.assertFalse(h.LAST_DIAGNOSTICS['eligible'])
        with patch.object(r, 'predict', return_value=token) as common:
            self.assertIs(h.predict(good, {'items': {}}), token)
            common.assert_called_once()

    def test_small_fallback_raw_exact_with_real_renderer(self):
        h = self.module(); r = h.original
        official, schema, frame = self.frame(12, 2)
        pred = official.scored_items(schema); gated = [x for x in pred if schema['items'][x].get('gate')]
        with patch.object(r.link_sharp, 'select_ladder', return_value=([], [], [])), \
             patch.object(r.link_sharp, 'tune_and_train', return_value=(0., None, (pred, gated))):
            expected = r.predict(frame, schema)
            actual = h.predict(frame, schema)
        self.assertEqual(len(actual), 426)
        for a, b in zip(actual, expected): np.testing.assert_array_equal(a, b)

    def test_K32_and_distinct_legacy_K10(self):
        h = self.module(); r = h.original
        from src.eval.retrieval_oracle import candidate_indices
        codes = np.array([[i % 2, (i // 2) % 3] for i in range(40)])
        q = np.array([0, 17]); bank = np.arange(40)[::-1]; weights = np.array([1., 2.])
        expected = candidate_indices(codes, weights, q, bank)
        np.testing.assert_array_equal(h.candidate_indices(codes, weights, q, bank), expected)
        self.assertFalse(any(row in ds for row, ds in zip(q, expected)))
        self.assertIs(h._topk_excl, r._topk_excl)
        self.assertEqual(len(h._topk_excl(codes, weights, q, bank)[0][0]), 10)

    def test_forced_active_all213_actual_entry_replay_and_renderer(self):
        h = self.module(); r = h.original
        official, schema, frame = self.frame()
        pred = official.scored_items(schema); gated = [x for x in pred if schema['items'][x].get('gate')]
        order = np.random.default_rng(4101).permutation(600); replay = order[180:240]
        high = set(replay[:29]); weights = np.stack((np.linspace(.1, 2., 17), np.linspace(2., .1, 17)))
        events = []; observed = {}; lambda_sizes = []
        actual_replace = h._replace_evidence
        def fit(codes, labels, bank, fit, select, initial, sizes, groups, waves):
            events.append('fit_select')
            self.assertEqual((len(fit), len(select), len(bank)), (120, 60, 360))
            self.assertTrue((labels[600:] == -1).all())
            return [weights.copy() for _ in groups], list(range(len(groups))), [{'selected': True} for _ in groups]
        def replace(*args):
            query = args[7]; events.append('cal' if len(query) > 2 else 'Q')
            output = actual_replace(*args)
            if len(query) == 2:
                observed['ev'] = output
                codes, initial, waves = args[6], args[9], args[-1]
                donors = h.candidate_indices(codes, initial, query, args[8])
                x = (codes[query, None, :] == codes[donors]).astype(float)
                pi = softmax(np.stack([x[i] @ weights[int(frame.wave.iloc[row]) - 1] for i, row in enumerate(query)]), axis=1)
                direct = r._evidence(frame, pred, schema['items'], {n: official.options_for(schema, n) for n in official.generated_items(schema)},
                                     list(zip(donors, pi)), query)
                for item in pred: np.testing.assert_allclose(output[item], direct[item], atol=1e-10, rtol=1e-10)
            return output
        def concentrations(post):
            if len(post) == 600: return np.array([1. if i in high else 0. for i in range(600)])
            self.assertEqual(len(post), 2); return np.array([0., 1.])
        def lam(a, b):
            events.append('lambda'); lambda_sizes.append(len(a)); return .5
        def ladder(rows, item, options, cols, kappas):
            return np.full(len(options), 1 / len(options)), []
        with patch.object(h, 'fit_sections', fit), patch.object(h, '_replace_evidence', replace), \
             patch.object(h, '_max_q', concentrations), patch.object(h, '_best_lambda', lam), \
             patch.object(r.link_sharp, 'select_ladder', return_value=([], [], [])), \
             patch.object(r.link_sharp, 'tune_and_train', return_value=(0., None, (pred, gated))), \
             patch.object(r.link_sharp, 'build_ladder', ladder), \
             patch.object(r.link_sharp, 'conditional_agreement', return_value={n: (.5, None, {}) for n in gated}):
            result = h.predict(frame, schema)
        self.assertEqual(events[0:2], ['fit_select', 'cal']); self.assertEqual(events[-1], 'Q')
        self.assertEqual(lambda_sizes, [31] * 213)  # 29-row bucket stays exactly zero.
        self.assertEqual(len(result), 426)
        expected = []
        for row in range(600, 602):
            belief = {}
            for item in official.generated_items(schema):
                opts = official.options_for(schema, item); rec = schema['items'][item]
                if rec['class'] == 'GIVEN':
                    belief[item] = np.eye(len(opts))[opts.index(frame.loc[row, item])]; continue
                soft = np.full(len(opts), 1 / len(opts)); gate = rec.get('gate')
                if gate:
                    parent_opts = official.options_for(schema, gate['parent'])
                    asked = sum(belief[gate['parent']][parent_opts.index(v)] for v in gate['observed_if'])
                    hard = np.r_[np.full(len(opts)-1, asked / (len(opts)-1)), 1-asked]
                    base = .5 * hard + .5 * soft
                else: base = soft
                if row == 600: base = .5 * base + .5 * observed['ev'][item][0]
                belief[item] = base; expected.append(base)
        for a, b in zip(result, expected): np.testing.assert_allclose(a, b, atol=1e-10, rtol=1e-10)
        self.assertTrue(all(np.isfinite(v).all() and (v >= 0).all() and abs(v.sum()-1) <= 1e-6 for v in result))


class HarnessTests(unittest.TestCase):
    def test_projection_and_complete_query_mask(self):
        from scripts import check_e063_round_metric as runner
        official, schema, frame = EntryTests().frame(4, 2)
        items = official.generated_items(schema); given = [x for x in items if schema['items'][x]['class'] == 'GIVEN']
        train = frame.iloc[:4].copy(); train.insert(0, 'role', 'TRAIN'); train.insert(0, 'respondent_id', range(4))
        dev = frame.iloc[4:][given].copy(); dev.insert(0, 'role', 'DEV'); dev.insert(0, 'respondent_id', range(4, 6))
        calls = []
        def read_parquet(path, columns, filters):
            calls.append((columns, filters))
            return (train if filters == [('role', '==', 'TRAIN')] else dev)[columns].copy()
        with patch.object(pd, 'read_parquet', read_parquet):
            t, q = runner.phase_frames(pd, official, schema, 'unhcr')
        self.assertEqual(calls[1][0], ['respondent_id', 'role'] + given)
        self.assertEqual(calls[1][1], [('role', '==', 'DEV')])
        masked, cells = runner.masked_phase1(official, schema, t, q)
        self.assertTrue(masked.iloc[4:][official.scored_items(schema)].isna().all().all())
        self.assertFalse(any(schema['items'].get(c, {}).get('class') == 'EXCLUDE' for c in masked))

    def test_budget_and_output_gate(self):
        from scripts import check_e063_round_metric as runner
        self.assertEqual(runner.stage_limit('R', 100., 1000.), 900.)
        self.assertEqual(runner.stage_limit('H', 1750., 1000.), 50.)
        self.assertEqual(runner.stage_limit('tests', 0., 1000.), 60.)
        with self.assertRaises(RuntimeError): runner.stage_limit('H', 1800., 1000.)
        with self.assertRaises(RuntimeError): runner.require_all_outputs()


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for cls in (MetricTests, EntryTests, HarnessTests):
        for name in sorted(cls.__dict__):
            if name.startswith('test_'): suite.addTest(cls(name))
    return suite


if __name__ == '__main__': unittest.main()
