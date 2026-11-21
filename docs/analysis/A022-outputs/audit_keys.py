"""One-shot key/eligibility audit; no model imports, response caches or fits."""
import hashlib
import json
import os
from pathlib import Path
import time

for variable in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ[variable] = '2'

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / 'verification.json'
SOURCE = ROOT / 'external/sipp-2023/a014-month12-restricted.parquet'
COLUMNS = ['SSUID', 'PNUM', 'MONTHCODE', 'THHLDSTATUS', 'TAGE_EHC']
ROLE_LIMITS = [('fit', 50), ('calibration', 65), ('oracle', 80), ('selection', 90), ('audit', 100)]


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(namespace, *parts):
    return hashlib.sha256('\0'.join((namespace, *parts)).encode()).digest()


def role(namespace, *parts):
    bucket = int.from_bytes(digest(namespace, *parts)[:8], 'big') % 100
    return next(name for name, upper in ROLE_LIMITS if bucket < upper)


def keys(frame):
    return list(frame[['SSUID', 'PNUM']].itertuples(index=False, name=None))


def key_digest(frame):
    payload = ''.join('\0'.join(pair) + '\n' for pair in sorted(keys(frame)))
    return hashlib.sha256(payload.encode()).hexdigest()


def counts(frame):
    return {'persons': len(frame), 'ssuids': int(frame.SSUID.nunique())}


def main():
    start = time.perf_counter()
    if OUT.exists():
        raise FileExistsError('Preserve completed A022 audit')
    import pandas as pd
    import pyarrow as pa
    pa.set_cpu_count(2)
    pa.set_io_thread_count(2)

    a019 = read(ROOT / 'docs/analysis/A019-outputs/entry-audit.json')
    a014 = read(ROOT / 'external/sipp-2023/a014-partitions.json')
    assert sha(SOURCE) == a019['source_sha256'] == a014['extract_sha256']
    paths = [SOURCE, ROOT / 'external/sipp-2023/a014-partitions.json']
    for name, expected in a019['local_key_hashes'].items():
        path = ROOT / 'external/a019' / name
        assert sha(path) == expected
        paths.append(path)
    for folder in ('external/e058', 'external/e059'):
        paths.extend(sorted((ROOT / folder).glob('*.json')))
    protected = {p.relative_to(ROOT).as_posix(): sha(p) for p in paths}
    assert not list((ROOT / 'external/e059').glob('audit*'))

    frame = pd.read_parquet(SOURCE, columns=COLUMNS)
    assert list(frame.columns) == COLUMNS
    assert frame.MONTHCODE.eq('12').all()
    assert not frame.duplicated(['SSUID', 'PNUM', 'MONTHCODE']).any()
    assert not frame[['SSUID', 'PNUM']].isna().any().any()
    assert not frame[['SSUID', 'PNUM']].eq('').any().any()
    frame['person_role'] = [role('A014-person-v1', s, p) for s, p in keys(frame)]
    frame['group_role'] = [role('A014-household-v1', s) for s in frame.SSUID]
    assert frame.person_role.value_counts().to_dict() == a014['roles']['person']
    assert frame.group_role.value_counts().to_dict() == a014['roles']['sample_unit']
    age = pd.to_numeric(frame.TAGE_EHC, errors='coerce')
    eligible = frame.loc[frame.THHLDSTATUS.isin(['1', '2']) & age.ge(1), ['SSUID', 'PNUM', 'person_role', 'group_role']].copy()
    assert age.loc[eligible.index].le(200).all()
    assert counts(eligible) == {'persons': a019['eligible_persons'], 'ssuids': a019['eligible_ssuids']}

    sample = eligible.copy()
    sample['sample_digest'] = [digest('E055-sample-v1', s, p) for s, p in keys(sample)]
    sample = sample.sort_values(['sample_digest', 'SSUID', 'PNUM']).head(12000).reset_index(drop=True)
    assert hashlib.sha256(b''.join(sample.sample_digest)).hexdigest() == a019['sample_hash']
    historical = pd.read_parquet(ROOT / 'external/a019/historical-keys.parquet',
                                 columns=['SSUID', 'PNUM', 'person_role', 'group_role'])
    query = pd.read_parquet(ROOT / 'external/a019/evaluation-keys.parquet', columns=['SSUID', 'PNUM', 'role'])
    fit = pd.read_parquet(ROOT / 'external/a019/fit-keys.parquet', columns=['SSUID', 'PNUM'])
    assert keys(sample) == keys(historical)
    for col in ('person_role', 'group_role'):
        assert sample[col].tolist() == historical[col].tolist()
    assert keys(sample.loc[sample.group_role.eq('fit')]) == keys(fit)
    assert counts(historical) == {'persons': 12000, 'ssuids': 8908}
    assert counts(query) == {'persons': 5999, 'ssuids': 3431}
    assert len(fit) == 5922
    old_units, query_units = set(historical.SSUID), set(query.SSUID)
    assert not old_units & query_units
    assert query.groupby('SSUID').role.nunique().max() == 1

    before_query = eligible.loc[~eligible.SSUID.isin(old_units)]
    sizes = before_query.groupby('SSUID').size().to_dict()
    ordered = sorted(sizes, key=lambda s: (digest('A019-evaluation-sample-v1', s), s))
    selected, total = [], 0
    for group in ordered:
        if total + sizes[group] > 6000:
            break
        selected.append(group)
        total += sizes[group]
    assert set(selected) == query_units
    reconstructed = before_query.loc[before_query.SSUID.isin(selected)].sort_values(['SSUID', 'PNUM'])
    assert keys(reconstructed) == keys(query)
    expected_roles = [('oracle', 'selection', 'audit')[int.from_bytes(digest('A019-evaluation-role-v1', s)[:8], 'big') % 3]
                      for s in query.SSUID]
    assert expected_roles == query.role.tolist()
    assert {r: counts(query.loc[query.role.eq(r)]) for r in ('oracle', 'selection', 'audit')} == a019['roles']

    used_units = old_units | query_units
    remainder = eligible.loc[~eligible.SSUID.isin(used_units)].copy()
    assert not set(remainder.SSUID) & used_units
    assert len(remainder) + int(eligible.SSUID.isin(used_units).sum()) == len(eligible)
    assert counts(remainder) == {'persons': 8700, 'ssuids': 4975}
    all_sizes = eligible.groupby('SSUID').size()
    remaining_sizes = remainder.groupby('SSUID').size()
    assert remaining_sizes.equals(all_sizes.loc[remaining_sizes.index])
    role_inventory = {r: counts(remainder.loc[remainder.group_role.eq(r)]) for r, _ in ROLE_LIMITS}
    original_fit_inventory = counts(fit)
    for path, expected in protected.items():
        assert sha(ROOT / path) == expected
    assert not list((ROOT / 'external/e059').glob('audit*'))
    result = {
        'status': 'PASS_KEYS_EMPIRICAL_HOLD', 'date': '2026-09-27',
        'input_head': '1d223340d4e1fa3993b411dc5daafab9cb37d0cd',
        'source_projection': COLUMNS,
        'existing_key_projection': {'historical': ['SSUID', 'PNUM', 'person_role', 'group_role'],
                                    'query': ['SSUID', 'PNUM', 'role'], 'fit': ['SSUID', 'PNUM']},
        'eligible': counts(eligible), 'historical_use': counts(historical), 'query_use': counts(query),
        'model_use_union': {'persons': len(set(keys(historical)) | set(keys(query))), 'ssuids': len(used_units)},
        'excluded_eligible_persons_by_used_ssuid': int(eligible.SSUID.isin(used_units).sum()),
        'remaining': counts(remainder), 'remaining_keys_sha256': key_digest(remainder),
        'key_digest_format': 'SHA256 UTF-8 of lexically sorted SSUID,PNUM pairs; NUL between fields, LF after each pair',
        'remaining_original_group_roles': role_inventory,
        'remaining_original_person_role_counts': {str(k): int(v) for k, v in remainder.person_role.value_counts().items()},
        'original_fit': original_fit_inventory,
        'protected_old_calibration': counts(historical.loc[historical.group_role.eq('calibration')]),
        'protected_e059_audit': counts(query.loc[query.role.eq('audit')]),
        'protected_ssuid_overlap': 0, 'remaining_groups_complete': True,
        'new_role_assignments': 0, 'new_samples': 0, 'remaining_key_file_created': False,
        'protected_hashes': protected, 'protected_after_match': True,
        'audit_script_sha256': sha(Path(__file__)),
        'registration_sha256': sha(OUT.parent / 'registration.md'),
        'technical_retry_record_sha256': sha(OUT.parent / 'technical-retry.md'),
        'source_projection_runs': 2,
        'predict_response_columns_read': [], 'model_given_columns_read': [],
        'eligibility_fields_read': ['THHLDSTATUS', 'TAGE_EHC'],
        'fits': 0, 'predictions': 0, 'scores': 0, 'cache_deserializations': 0,
        'wall_seconds_including_imports': time.perf_counter() - start,
        'limits': 'Group-disjoint remaining keys under recorded repository history, not new independent source or a power/transfer guarantee. Roles are inventoried, not reassigned.'
    }
    with OUT.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
    print(json.dumps({k: v for k, v in result.items() if k != 'protected_hashes'}, indent=2))


if __name__ == '__main__':
    main()
