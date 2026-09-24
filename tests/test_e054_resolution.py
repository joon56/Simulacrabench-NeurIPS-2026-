"""Analytic and uncertainty checks for the E054 information gate; no fits."""
import unittest
import numpy as np
from scripts import analyze_e054_resolution as screen


class ResolutionTests(unittest.TestCase):
    def setUp(self):
        self.spec = {'items': {
            'given': {'class': 'GIVEN', 'values': [0, 1]},
            'plain': {'class': 'PREDICT', 'values': [0, 1], 'gate': None},
            'gated': {'class': 'PREDICT', 'values': [0, 1], 'gate': {'parent': 'given'}},
        }, 'split': {'n_dev': 100}}
        self.summary = screen.schema_summary(self.spec, .001)

    def test_loss_identity_matches_direct_log_score_with_unequal_classes(self):
        U = self.summary['U']
        truth_prob = np.array([.7, .8])
        baseline = 1 + np.log(truth_prob).mean() / U
        probe = 1 + (np.log(.7) + np.log(1 / 3)) / (2 * U)
        gated, plain = screen.losses(baseline, probe, self.summary['A'])
        self.assertAlmostEqual(gated, -np.log(.8) / (2 * U))
        self.assertAlmostEqual(plain, -np.log(.7) / (2 * U))
        self.assertAlmostEqual(gated + plain, 1 - baseline)

    def test_floor_best_loss_is_positive_and_normalized(self):
        s = self.summary
        self.assertGreater(s['gated_min_loss'], 0)
        self.assertGreater(s['ungated_min_loss'], 0)
        self.assertAlmostEqual(s['max_skill'], 1 - s['gated_min_loss'] - s['ungated_min_loss'])

    def test_laplace_union_bound(self):
        tail = screen.noise_tails([self.summary] * 3, .001, 10, 93, .05)[0]
        scale = -np.log(.001) / (100 * self.summary['U'] * 10)
        self.assertAlmostEqual(93 * np.exp(-tail / scale), .05)

    def test_zero_error_lp_recovers_known_group_losses(self):
        h, p = .8, .35
        baseline = [.5, .5, h]
        result = screen.reading_intervals([self.summary] * 3, baseline,
            sum(baseline) / 3, (1 + p) / 3, [0] * 3, 0, 'before')
        self.assertIsNotNone(result)
        lg, lc = screen.losses(h, p, self.summary['A'])
        np.testing.assert_allclose(result['gated_loss'], [lg, lg], atol=1e-10)
        np.testing.assert_allclose(result['ungated_loss'], [lc, lc], atol=1e-10)

    def test_wider_noise_cannot_narrow_lp_intervals(self):
        args = ([self.summary] * 3, [.5, .5, .8], .6, .45)
        narrow = screen.reading_intervals(*args, [.001] * 3, .01, 'before')
        broad = screen.reading_intervals(*args, [.01] * 3, .01, 'before')
        for key in ('gated_loss', 'ungated_loss', 'difference'):
            self.assertLessEqual(broad[key][0], narrow[key][0] + 1e-10)
            self.assertGreaterEqual(broad[key][1], narrow[key][1] - 1e-10)

    def test_impossible_probe_reading_is_rejected(self):
        result = screen.reading_intervals([self.summary] * 3, [.5, .5, .8],
            .6, .9, [0] * 3, .01, 'after')
        self.assertIsNone(result)

    def test_after_rounding_witness_uses_literal_display_values(self):
        args = ([self.summary] * 3, [.5, .5, .8], .6, .45, [.003] * 3, .01)
        problem = screen.make_problem(*args, 'after')
        witness = screen.rounded_witness(problem, [.5, .5, .8], .45, [.003] * 3, .01)
        self.assertIsNotNone(witness)
        self.assertAlmostEqual(round(np.mean(witness['probe_published']) / .01) * .01, .45)

    def test_inconsistent_baseline_grand_is_not_feasible_after_rounding(self):
        result = screen.reading_intervals([self.summary] * 3, [.5, .5, .8],
            .7, .45, [.01] * 3, .01, 'after')
        self.assertIsNone(result)

    def test_priority_requires_complete_interval_and_margin(self):
        self.assertEqual(screen.priority([.016, .08]), 'gated')
        self.assertEqual(screen.priority([-.08, -.016]), 'ungated')
        self.assertEqual(screen.priority([-.001, .08]), 'unresolved')
        self.assertEqual(screen.priority([.015, .08]), 'unresolved')


if __name__ == '__main__':
    unittest.main()
