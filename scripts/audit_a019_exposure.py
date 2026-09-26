"""A019 key-only audit. Never import a predictor or deserialize response caches."""

import hashlib
import json
import os
from pathlib import Path
import time

for variable in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ[variable] = '2'

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/analysis/A019-outputs'
LOCAL = ROOT / 'external/a019'
COLUMNS = ['SSUID', 'PNUM', 'MONTHCODE', 'ERESIDENCEID', 'THHLDSTATUS', 'TAGE_EHC']
ROLES = ('oracle', 'selection', 'audit')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest(namespace, *parts):
    return hashlib.sha256('\0'.join((namespace, *parts)).encode()).digest()


def historical_role(namespace, *parts):
    bucket = int.from_bytes(digest(namespace, *parts)[:8], 'big') % 100
    return next(role for role, upper in [('fit', 50), ('calibration', 65),
                                        ('oracle', 80), ('selection', 90), ('audit', 100)] if bucket < upper)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def select_groups(frame, cap=6000):
    counts = frame.groupby('SSUID').size().to_dict()
    order = sorted(counts, key=lambda s: (digest('A019-evaluation-sample-v1', s), s))
    chosen, total = [], 0
    for group in order:
        if total + counts[group] > cap:
            break
        chosen.append(group)
        total += counts[group]
    selected = frame.loc[frame.SSUID.isin(chosen)].copy()
    selected['role'] = [ROLES[int.from_bytes(digest('A019-evaluation-role-v1', s)[:8], 'big') % 3]
                        for s in selected.SSUID]
    return selected.sort_values(['SSUID', 'PNUM']).reset_index(drop=True)


def main():
    start = time.perf_counter()
    if OUT.exists() or LOCAL.exists():
        raise FileExistsError('Preserve existing A019 outputs')
    import pandas as pd
    source = ROOT / 'external/sipp-2023/a014-month12-restricted.parquet'
    manifests = [ROOT / f'external/e055/sipp-{v}-manifest.json' for v in ('person', 'group')]
    manifests.append(ROOT / 'docs/analysis/E056-outputs/manifest.json')
    expected = read(ROOT / 'external/sipp-2023/a014-partitions.json')['extract_sha256']
    assert sha(source) == expected
    frame = pd.read_parquet(source, columns=COLUMNS)
    assert list(frame.columns) == COLUMNS and frame.MONTHCODE.eq('12').all()
    assert not frame.duplicated(['SSUID', 'PNUM', 'MONTHCODE']).any()
    age = pd.to_numeric(frame.TAGE_EHC, errors='coerce')
    eligible = frame.loc[frame.THHLDSTATUS.isin(['1', '2']) & age.ge(1)].copy()
    assert age.loc[eligible.index].le(200).all()
    eligible['source_position'] = eligible.index
    sample = eligible.copy()
    sample['sample_digest'] = [digest('E055-sample-v1', s, p) for s, p in zip(sample.SSUID, sample.PNUM)]
    sample = sample.sort_values(['sample_digest', 'SSUID', 'PNUM']).head(12000).reset_index(drop=True)
    sample_hash = hashlib.sha256(b''.join(sample.sample_digest)).hexdigest()
    person = [historical_role('A014-person-v1', s, p) for s, p in zip(sample.SSUID, sample.PNUM)]
    group = [historical_role('A014-household-v1', s) for s in sample.SSUID]
    counts = {'person': pd.Series(person).value_counts().to_dict(), 'group': pd.Series(group).value_counts().to_dict()}
    for path in manifests:
        old = read(path)
        assert old['source_sha256'] == expected and old['sample_hash'] == sample_hash
        assert old['rows'] == len(sample) == 12000
        assert old['role_counts'] == counts[old['view']]
    sample['person_role'], sample['group_role'] = person, group
    used = set(sample.SSUID)
    remaining = eligible.loc[~eligible.SSUID.isin(used)].copy()
    selected = select_groups(remaining)
    assert not set(selected.SSUID) & used
    assert selected.groupby('SSUID').role.nunique().max() == 1
    for s, block in selected.groupby('SSUID'):
        assert len(block) == int(eligible.SSUID.eq(s).sum())
    sizes = {role: {'persons': int(selected.role.eq(role).sum()),
                    'ssuids': int(selected.loc[selected.role.eq(role), 'SSUID'].nunique())} for role in ROLES}
    passed = all(v['persons'] >= 1000 and v['ssuids'] >= 500 for v in sizes.values())
    OUT.mkdir(parents=True)
    LOCAL.mkdir(parents=True)
    key_columns = COLUMNS + ['source_position']
    sample[key_columns + ['person_role', 'group_role']].to_parquet(LOCAL / 'historical-keys.parquet', index=False)
    selected[key_columns + ['role']].to_parquet(LOCAL / 'evaluation-keys.parquet', index=False)
    sample.loc[sample.group_role.eq('fit'), key_columns].to_parquet(LOCAL / 'fit-keys.parquet', index=False)
    result = {'status': 'PASS' if passed else 'STOP_SIZE', 'source_sha256': expected,
        'columns_read': COLUMNS, 'sample_hash': sample_hash, 'historical_role_counts': counts,
        'eligible_persons': len(eligible), 'eligible_ssuids': int(eligible.SSUID.nunique()),
        'historical_persons': len(sample), 'historical_ssuids': len(used),
        'excluded_persons_by_ssuid': int(eligible.SSUID.isin(used).sum()),
        'remaining_persons': len(remaining), 'remaining_ssuids': int(remaining.SSUID.nunique()),
        'selected_persons': len(selected), 'selected_ssuids': int(selected.SSUID.nunique()), 'roles': sizes,
        'role_ssuid_overlap': 0, 'old_new_ssuid_overlap': 0,
        'manifest_hashes': {p.relative_to(ROOT).as_posix(): sha(p) for p in manifests},
        'local_key_hashes': {p.name: sha(p) for p in LOCAL.glob('*.parquet')},
        'script_sha256': sha(__file__), 'wall_seconds': time.perf_counter() - start,
        'fit_calls': 0, 'new_score_calls': 0,
        'scope': 'Same aggregate-exposed A014 source. Provenance conditional on recorded repository run history.'}
    with (OUT / 'entry-audit.json').open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
