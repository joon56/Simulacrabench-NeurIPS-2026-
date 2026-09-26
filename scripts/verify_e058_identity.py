"""Certify E058's collapsed library without reading any evaluation response."""
import hashlib
import json
import os
from pathlib import Path
import pickle
import sys
import time

for key in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ[key] = '2'
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / 'docs/analysis/E058-outputs'
LOCAL = ROOT / 'external/e058'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    started = time.perf_counter()
    import numpy as np
    import pandas as pd
    preflight, record = read(OUT / 'preflight.json'), read(OUT / 'library.json')
    for path, expected in preflight['source_hashes'].items():
        assert sha(ROOT / path) == expected, path
    assert sha(OUT / 'registration.md') == preflight['registration_sha256']
    for name, expected in preflight['key_hashes'].items():
        assert sha(ROOT / 'external/a019' / name) == expected
    for name, key in [('library.npz', 'library_sha256'), ('masked-frame.pkl', 'masked_sha256'), ('first-stage.pkl', 'first_stage_sha256')]:
        assert sha(LOCAL / name) == record[key]
    schema, frame = pickle.loads((LOCAL / 'masked-frame.pkl').read_bytes())
    first = pickle.loads((LOCAL / 'first-stage.pkl').read_bytes())
    state, names = first['state'], record['predicted']
    assert state['active'] == record['active_sections'] == [] and record['beta_details'] == {}
    assert frame.iloc[state['query']][names].isna().all().all()
    assert frame.iloc[state['visible']][names].notna().all().all()
    np.testing.assert_array_equal(state['visible'], np.arange(5922))
    np.testing.assert_array_equal(state['query'], np.arange(5922, 11921))
    args = state['metric_arguments']
    assert (args[1][state['query']] == -1).all()
    assert all(np.isin(args[i], state['visible']).all() for i in (2, 3, 4))
    for call in state['donor_calls']:
        assert np.isin(call['donors'], state['visible']).all()
        assert np.isin(call['bank'], state['visible']).all()
        assert not np.any(call['donors'] == call['query'][:, None])
    keys = pd.read_parquet(ROOT / 'external/a019/evaluation-keys.parquet')
    bounds, max_raw = [], 0.
    with np.load(LOCAL / 'library.npz', allow_pickle=False) as library:
        np.testing.assert_array_equal(library['roles'], keys.role.to_numpy(dtype=str))
        np.testing.assert_array_equal(library['groups'], keys.SSUID.to_numpy(dtype=str))
        for j, name in enumerate(names):
            np.testing.assert_array_equal(library[f'base/{name}'], library[f'candidate/{name}'])
            np.testing.assert_array_equal(library[f'base/{name}'], library[f'zero/{name}'])
            np.testing.assert_array_equal(library[f'base/{name}'], np.stack(first['baseline'][j::len(names)]))
        take = keys.role.eq('oracle').to_numpy()
        u = np.mean([np.log(library[f'base/{n}'].shape[1]) for n in names])
        for alpha in (0., .25, .5):
            per_item = []
            for name in names:
                p, c = library[f'base/{name}'][take], library[f'candidate/{name}'][take]
                mixed = p if alpha == 0 else (1 - alpha) * p + alpha * c
                max_raw = max(max_raw, float(np.max(np.abs(mixed - p))))
                floor = lambda x: .001 + (1 - x.shape[1] * .001) * x / x.sum(1, keepdims=True)
                p0, p1 = floor(p), floor(mixed)
                # log(p1/p0) <= abs(p1-p0)/p0 for every possible true class.
                per_item.append(np.max(np.abs(p1 - p0) / p0, axis=1))
            bounds.append(float(np.column_stack(per_item).mean() / u))
    upper = max(bounds) + 1e-12  # Conservative roundoff allowance, below fixed1e-10 gate.
    assert upper <= 1e-10
    assert all(not (LOCAL / f'{role}-opened.json').exists() for role in ('oracle', 'selection', 'audit'))
    assert all(not (LOCAL / f'{role}-scores.npz').exists() for role in ('oracle', 'selection', 'audit'))
    runtime = read(OUT / 'library-runtime.json')
    resources = read(OUT / 'library-resources.json')
    assert runtime['exit_code'] == 0 and runtime['reason'] == 'COMPLETE'
    assert max(runtime['peak_tree_bytes'].values()) < 8 * 1024**3 and resources['fit_seconds'] < 1200
    result = {'gate': 'STOP_FINITE_LIBRARY', 'reason': 'Frozen original E041 active-section set is empty.',
        'exact_arithmetic_oracle_delta_skill': 0., 'floating_point_gain_lower': 0.,
        'floating_point_gain_upper': upper, 'per_arm_label_free_upper': bounds,
        'roundoff_allowance_skill': 1e-12, 'registered_stop_tolerance': 1e-10,
        'mixture_raw_max_abs': max_raw, 'baseline_candidate_beta0_vectors_exact': len(first['baseline']),
        'all_new_evaluation_roles_unopened': True, 'new_evaluation_label_reads': 0, 'new_score_calls': 0,
        'new_e041_fits': 1, 'beta_fits': 0, 'checked_source_hashes': len(preflight['source_hashes']),
        'library_sha256': record['library_sha256'], 'verifier_sha256': sha(__file__),
        'seconds': time.perf_counter()-started,
        'scope': 'Exact identity family in real arithmetic; conservative float bound for any possible oracle labels. No effect-size estimate or efficacy audit.'}
    with (OUT / 'oracle-identity-certificate.json').open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
