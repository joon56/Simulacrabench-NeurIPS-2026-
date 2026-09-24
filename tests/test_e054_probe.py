"""E054 must flatten only final gated UNHCR targets, with no new model fits."""
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
from src.models import e041_gated_probe as probe


class ProbeTests(unittest.TestCase):
    def setUp(self):
        self.schema = {'items': {
            's3_11_intent_return_12m_lbl': {'class': 'GIVEN', 'gate': None},
            'plain': {'class': 'PREDICT', 'gate': None},
            'gated': {'class': 'PREDICT', 'gate': {'parent': 'plain'}},
            'excluded': {'class': 'EXCLUDE', 'gate': {'parent': 'plain'}},
        }}
        self.frame = pd.DataFrame({'gated': [1, None, None], 'plain': [1, None, None]}, index=[4, 9, 12])
        self.vectors = [np.array([.7, .3]), np.array([.1, .2, .7]),
                        np.array([.8, .2]), np.array([.3, .3, .4])]

    def test_only_final_gated_vectors_change_in_schema_order(self):
        result = probe.apply_probe(self.vectors, self.frame, self.schema)
        self.assertIs(result[0], self.vectors[0])
        self.assertIs(result[2], self.vectors[2])
        np.testing.assert_array_equal(result[1], np.full(3, 1/3))
        np.testing.assert_array_equal(result[3], np.full(3, 1/3))
        np.testing.assert_array_equal(self.vectors[1], [.1, .2, .7])

    def test_other_instruments_exact_noop(self):
        del self.schema['items']['s3_11_intent_return_12m_lbl']
        self.assertIs(probe.apply_probe(self.vectors, self.frame, self.schema), self.vectors)

    def test_predict_calls_original_once_before_transform(self):
        with patch.object(probe.retrieval, 'predict', return_value=self.vectors) as original:
            result = probe.predict(self.frame, self.schema)
        original.assert_called_once_with(self.frame, self.schema)
        self.assertIs(result[0], self.vectors[0])

    def test_wrong_output_count_rejected(self):
        with self.assertRaises(ValueError):
            probe.apply_probe(self.vectors[:-1], self.frame, self.schema)


if __name__ == '__main__':
    unittest.main()
