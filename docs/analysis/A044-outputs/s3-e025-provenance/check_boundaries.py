"""Only new observer and masking boundary checks; no model or real input."""
import importlib.util
from pathlib import Path
import unittest


class Boundaries(unittest.TestCase):
    def test_observer_and_mask_contract(self):
        path = Path(__file__).with_name('task.py')
        self.assertTrue(path.exists(), 'new task boundary implementation missing')
        spec = importlib.util.spec_from_file_location('task', path)
        task = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(task)
        # Final samples count; children are aggregated, not maxed individually.
        self.assertTrue(task.over_memory([{'rss': 5, 'private': 2},
                                         {'rss': 4, 'private': 2}], 8))
        self.assertTrue(task.over_memory([{'rss': 1, 'private': 9}], 8))
        self.assertFalse(task.over_memory([{'rss': 7, 'private': 7}], 8))
        # Failure is closed at the exact boundary; equality isn't below the cap.
        self.assertTrue(task.over_memory([{'rss': 8, 'private': 1}], 8))
        self.assertEqual(task.remaining(900, 899), 1)
        with self.assertRaises(RuntimeError):
            task.remaining(900, 900)
        # Pure generated fixture; reader records projection/filter requests.
        import pandas as pd
        schema = {'items': [{'name': 'g', 'role': 'GIVEN'},
                            {'name': 'p', 'role': 'PREDICT'}]}
        rows = pd.DataFrame({'respondent_id': ['a', 'b', 'c'],
                             'role': ['TRAIN', 'DEV', 'TEST'],
                             'g': ['x', 'y', 'z'], 'p': ['one', 'two', 'secret']})
        calls = []
        def reader(path, columns, filters):
            calls.append((columns, filters))
            col, op, val = filters[0]
            mask = rows[col].isin(val) if op == 'in' else rows[col] == val
            return rows.loc[mask, columns].copy()
        frame, cells = task.masked_frame('fixture', schema, reader=reader,
                                        items=['g', 'p'], scored=['p'], role='role')
        self.assertEqual(list(frame.respondent_id), ['a', 'b', 'c'])
        self.assertEqual(list(frame.p[:2]), ['one', 'two'])
        self.assertTrue(pd.isna(frame.p.iloc[2]))
        self.assertEqual(cells, [(2, 'c', 'p')])
        self.assertNotIn('p', calls[1][0])
        self.assertEqual(calls[1][1], [('role', '==', 'TEST')])


if __name__ == '__main__':
    unittest.main()
