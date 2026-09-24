"""Independent aggregate-only E055 artifact verification; no model imports/fits."""
import gzip
import hashlib
import itertools
import json
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
GRID = tuple(round(.1 * i, 1) for i in range(10)) + (.95, .98)
PAIRS = list(itertools.product(GRID, repeat=2))
NAMES = ['HOSPITALIZED', 'EHREAS_DT', 'EHREAS_BIR', 'EHREAS_OS',
         'EHREAS_NST', 'EHREAS_OTH', 'EHREAS_COR']
GIVEN = ['TAGE', 'ESEX', 'ERACE', 'EORIGIN', 'EEDUC', 'EMS']
ROLES = [('fit', 50), ('calibration', 65), ('oracle', 80), ('selection', 90), ('audit', 100)]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def role(parts, namespace):
    value = int.from_bytes(hashlib.sha256('\0'.join([namespace, *parts]).encode()).digest()[:8], 'big') % 100
    return next(name for name, end in ROLES if value < end)


def logsum(raw, labels):
    raw = np.asarray(raw, float)
    assert raw.ndim == 2 and np.isfinite(raw).all() and (raw >= 0).all()
    assert (raw.sum(1) > 0).all()
    probability = .001 + (1 - raw.shape[1] * .001) * raw / raw.sum(1, keepdims=True)
    return float(np.log(probability[np.arange(len(labels)), labels]).sum())


def verify(view):
    local = ROOT / 'external/e055'
    aggregate = ROOT / 'docs/analysis/E055-outputs'
    stem = 'sipp-' + view
    manifest = json.loads((local / f'{stem}-manifest.json').read_text())
    result = json.loads((aggregate / f'{stem}-oracle.json').read_text())
    for field, path in [
        ('capture_sha256', local / f'{stem}-capture.pkl.gz'),
        ('root_arrays_sha256', local / f'{stem}-roots.npz'),
        ('masked_archive_sha256', local / f'{stem}-masked.pkl.gz'),
        ('registration_sha256', aggregate / f'{stem}-registration.md'),
        ('source_sha256', ROOT / 'external/sipp-2023/a014-month12-restricted.parquet'),
    ]:
        assert sha(path.read_bytes()) == manifest[field], field
    # The archived registration above is immutable. The live experiment record
    # legitimately adds results/status after execution and is not a hash target.
    for path, expected in manifest['source_code_sha256'].items():
        assert sha((ROOT / path).read_bytes()) == expected, path
    assert result['capture_sha256'] == manifest['capture_sha256']
    capture = pickle.loads(gzip.decompress((local / f'{stem}-capture.pkl.gz').read_bytes()))
    masked_payload = gzip.decompress((local / f'{stem}-masked.pkl.gz').read_bytes())
    schema, masked = pickle.loads(masked_payload)
    # Re-pickling pandas objects is not a canonical semantic hash. The archive
    # byte hash above is authoritative; compare its original payload directly.
    prefit_payload_matches = sha(masked_payload) == manifest['masked_frame_sha256']
    assert prefit_payload_matches, 'Pre-fit masked snapshot payload changed'
    assert list(masked.columns) == GIVEN + NAMES
    assert list(schema['items']) == GIVEN + NAMES
    assert all(schema['items'][name]['class'] == 'GIVEN' for name in GIVEN)
    assert all(schema['items'][name]['class'] == 'PREDICT' for name in NAMES)
    assert all(schema['items'][name]['gate'] == {'parent': NAMES[0], 'observed_if': ['1']} for name in NAMES[1:])
    source = pd.read_parquet(ROOT / 'external/sipp-2023/a014-month12-restricted.parquet')
    source = source.loc[source.THHLDSTATUS.isin(['1', '2']) & pd.to_numeric(source.TAGE_EHC).ge(1)].copy()
    source['hash'] = [hashlib.sha256('\0'.join(['E055-sample-v1', a, b]).encode()).digest()
                      for a, b in zip(source.SSUID, source.PNUM)]
    source = source.sort_values(['hash', 'SSUID', 'PNUM']).head(12000).reset_index(drop=True)
    assert len(source) == len(masked) == 12000
    assert sha(b''.join(source['hash'])) == manifest['sample_hash']
    namespace = 'A014-person-v1' if view == 'person' else 'A014-household-v1'
    roles = np.array([role([a, b] if view == 'person' else [a], namespace)
                      for a, b in zip(source.SSUID, source.PNUM)])
    for name, _ in ROLES:
        assert np.flatnonzero(roles == name).tolist() == manifest['role_positions'][name]
    if view == 'group':
        assert pd.DataFrame({'id': source.SSUID, 'role': roles}).groupby('id').role.nunique().max() == 1
    query = np.flatnonzero(roles != 'fit')
    assert np.array_equal(query, capture['query'])
    fit_positions = np.flatnonzero(roles == 'fit')
    donor_records = capture['capture']['fitted_state']['query_donor_records']
    for record in donor_records:
        assert np.isin(record['query'], query).all()
        assert np.isin(record['bank'], fit_positions).all()
        returned = record['result']
        donors = returned if isinstance(returned, np.ndarray) else np.concatenate([indices for indices, _ in returned])
        assert np.isin(donors, fit_positions).all()
    assert masked.iloc[query][NAMES].isna().all().all()
    assert masked.iloc[np.flatnonzero(roles == 'fit')][NAMES].notna().all().all()
    expected_given = source[GIVEN].copy()
    for name in ['EEDUC', 'EMS']:
        expected_given[name] = expected_given[name].replace('', 'MISSING')
    assert masked[GIVEN].equals(expected_given)
    selected = np.flatnonzero(roles[query] == 'oracle')
    oracle = source.iloc[query[selected]]
    truth = {NAMES[0]: (pd.to_numeric(oracle.THOSPNIT).to_numpy() > 0).astype(int)}
    for name in NAMES[1:]:
        blank = oracle[name].eq('')
        assert (~blank | oracle.AHREASON.eq('0')).all()
        truth[name] = oracle[name].map({'1': 0, '2': 1, '': 2}).to_numpy(dtype=int)
    buckets = capture['bucket'][selected]
    assert set(np.unique(buckets)) <= {0, 1}
    arrays = np.load(local / f'{stem}-roots.npz')
    identity = {name: arrays[f'identity/{name}'][selected] for name in NAMES}
    for name in NAMES:
        assert np.array_equal(arrays[f'identity/{name}'], capture['identity'][name])
    evidence = {name: capture['evidence'][name][selected] for name in NAMES}
    available = {name: capture['available'][name][selected] for name in NAMES}
    base_score = sum(logsum(identity[name], truth[name]) for name in NAMES)
    best = base_score
    for index, pair in enumerate(PAIRS):
        roots = {name: arrays[f'root/{index:03d}/{name}'] for name in NAMES}
        for raw in roots.values():
            assert np.isfinite(raw).all() and (raw >= 0).all() and (raw.sum(1) > 0).all()
        score = logsum(roots[NAMES[0]][selected], truth[NAMES[0]])
        for name in NAMES[1:]:
            base = roots[name][selected]
            for bucket in [0, 1]:
                rows = np.flatnonzero(buckets == bucket)
                if not len(rows):
                    continue
                live = available[name][rows]
                values = []
                for weight in GRID:
                    candidate = base[rows].copy()
                    candidate[live] = (1 - weight) * candidate[live] + weight * evidence[name][rows][live]
                    values.append(logsum(candidate, truth[name][rows]))
                score += max(values)
        best = max(best, score)
    chosen_index = PAIRS.index(tuple(result['shares'][NAMES[0]]))
    chosen = {name: arrays[f'root/{chosen_index:03d}/{name}'][selected].copy() for name in NAMES}
    for name in NAMES[1:]:
        weights = np.array(result['shares'][name])[buckets]
        live = available[name]
        chosen[name][live] = (1 - weights[live, None]) * chosen[name][live] + weights[live, None] * evidence[name][live]
    chosen_score = sum(logsum(chosen[name], truth[name]) for name in NAMES)
    uniform = (np.log(2) + 6 * np.log(3)) / 7
    delta = (best - base_score) / (len(selected) * 7 * uniform * 3)
    assert abs(best - result['best_log_sum']) < 1e-8
    assert abs(chosen_score - result['best_log_sum']) < 1e-8
    assert abs(base_score - result['identity_log_sum']) < 1e-8
    assert abs(delta - result['delta_skill_over_3']) < 1e-12
    assert best >= base_score
    gate = 'PASS' if delta > .005 + 1e-10 else 'STOP' if delta <= .005 - 1e-10 else 'UNRESOLVED'
    assert result['gate'] == gate
    assert result['buckets'] == {str(b): int((buckets == b).sum()) for b in [0, 1]}
    assert result['available'] == {name: int(available[name].sum()) for name in NAMES}
    for name in NAMES:
        assert abs(logsum(chosen[name], truth[name]) - logsum(identity[name], truth[name]) - result['per_head_gain'][name]) < 1e-8
    report = {'view': view, 'verified': True, 'oracle_rows': len(selected), 'gate': gate,
              'delta_skill_over_3': delta, 'best_log_sum_recomputed': best,
              'reported_log_sum_abs_error': abs(best - result['best_log_sum']),
              'selected_composition_log_sum_abs_error': abs(chosen_score - result['best_log_sum']),
              'source_dependency_files_verified': len(manifest['source_code_sha256']),
              'fit_only_donor_records_verified': len(donor_records),
              'masked_archive_payload_matches_prefit_pickle_hash': prefit_payload_matches,
              'all_144_raw_root_scenarios_valid': True, 'only_oracle_labels_scored': True,
              'selected_changed_vectors_by_head': {name: int(np.any(chosen[name] != identity[name], axis=1).sum()) for name in NAMES},
              'root_endpoint_changed_child_vectors': {name: int(np.any(arrays[f'root/000/{name}'][selected] != arrays[f'root/143/{name}'][selected], axis=1).sum()) for name in NAMES[1:]},
              'verifier_sha256': sha(Path(__file__).read_bytes())}
    (aggregate / f'{stem}-independent-verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report), flush=True)


verify(sys.argv[1])
