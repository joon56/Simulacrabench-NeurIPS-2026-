"""Verify frozen E056 arithmetic and provenance without fits or response labels."""

from itertools import product
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
LOCAL = ROOT / 'external/e056'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))


def verify():
    manifest = read('manifest.json')
    assert sha(LOCAL / 'library.npz') == manifest['library_sha256']
    assert sha(OUT / 'registration.md') == manifest['registration_sha256']
    assert sha(OUT / 'executed-screen-e056.py') == manifest['script_sha256']
    for path, expected in manifest['source_code_sha256'].items():
        assert sha(ROOT / path) == expected, path
    assert not (LOCAL / 'calibration-opened.json').exists()
    old = json.loads((ROOT / 'external/e055/sipp-group-manifest.json').read_text())
    assert sha(ROOT / 'external/e055/sipp-group-manifest.json') == manifest['cache_manifest_sha256']
    assert sha(ROOT / 'external/e055/sipp-group-capture.pkl.gz') == manifest['cache_capture_sha256']
    names = ['HOSPITALIZED', 'EHREAS_DT', 'EHREAS_BIR', 'EHREAS_OS', 'EHREAS_NST', 'EHREAS_OTH', 'EHREAS_COR']
    checks = {'source_hashes': len(manifest['source_code_sha256']), 'cache_identity_vectors': 0, 'roles': []}
    with np.load(LOCAL / 'library.npz') as library, np.load(ROOT / 'external/e055/sipp-group-roots.npz') as previous:
        assert np.array_equal(library['query'], np.sort(np.concatenate([
            old['role_positions'][role] for role in ('calibration', 'oracle', 'selection', 'audit')])))
        for name in names:
            base = library[f'{name}/0']
            np.testing.assert_array_equal(base, previous[f'identity/{name}'])
            checks['cache_identity_vectors'] += len(base)
            for i in range(3):
                changed = library[f'{name}/{i}']
                assert np.isfinite(changed).all() and (changed >= 0).all()
                np.testing.assert_allclose(changed.sum(1), base.sum(1), atol=1e-12, rtol=0)
                if name == names[0]:
                    np.testing.assert_array_equal(changed, base)
                else:
                    np.testing.assert_array_equal(changed[:, -1], base[:, -1])
        u = sum(np.log(library[f'{name}/0'].shape[1]) for name in names) / 7
    for role in ('oracle', 'selection', 'audit'):
        if not (OUT / f'{role}.json').exists():
            assert not (LOCAL / f'{role}-opened.json').exists()
            continue
        result = read(f'{role}.json')
        assert result['library_sha256'] == manifest['library_sha256']
        assert sha(LOCAL / f'{role}-scores.npz') == result['scores_sha256']
        with np.load(LOCAL / f'{role}-scores.npz') as arrays:
            groups = arrays['groups']
            unique = sorted(set(groups))
            positions = [np.flatnonzero(groups == g) for g in unique]
            assert len(groups) == result['rows']
            if role == 'oracle':
                maximum = max(arrays[names[0]][0].sum() + sum(arrays[n][i].sum()
                    for n, i in zip(names[1:], choices)) for choices in product(range(3), repeat=6))
                baseline = sum(arrays[n][0].sum() for n in names)
                delta = (maximum - baseline) / (len(groups) * 7 * u)
                np.testing.assert_allclose(delta, result['delta_skill'], rtol=0, atol=2e-15)
                assert result['gate'] == ('PASS' if delta > 1e-10 else 'STOP')
                checks['oracle_assignments'] = 729
            elif role == 'selection':
                assert read('oracle.json')['gate'] == 'PASS'
                for name in names[1:]:
                    choice = int(np.argmax([sum(row) for row in arrays[name]]))
                    d = arrays[name][choice] - arrays[name][0]
                    mean = sum(d) / len(d)
                    centered = [sum(d[p] - mean) for p in positions]
                    se = np.sqrt(len(positions) / (len(positions) - 1) * sum(x*x for x in centered)) / len(d)
                    assert result['shares'][name] == (choice if mean > max(0, se) else 0)
                    np.testing.assert_allclose(se, result['detail'][name]['cluster_se'], atol=1e-15, rtol=0)
            else:
                assert any(read('selection.json')['shares'].values())
                d = sum(arrays[f'selected/{n}'] - arrays[f'base/{n}'] for n in names) / (7 * u)
                sums = np.array([sum(d[p]) for p in positions])
                sizes = np.array([len(p) for p in positions])
                rng = np.random.default_rng(5601)
                replicates = []
                for _ in range(2000):
                    draw = rng.integers(len(positions), size=len(positions))
                    replicates.append(sum(sums[draw]) / sum(sizes[draw]))
                interval = np.percentile(replicates, [2.5, 97.5])
                np.testing.assert_allclose(interval, result['bootstrap_95'], atol=1e-15, rtol=0)
                np.testing.assert_allclose(d.mean(), result['delta_skill'], atol=1e-15, rtol=0)
                assert result['gate'] == ('FOLLOWUP_RESEARCH' if d.mean() > 0 and interval[0] > 0 else 'STOP_INCONCLUSIVE_OR_NONPOSITIVE')
        checks['roles'].append(role)
    checks.update({'result': 'PASS', 'new_response_label_access': False, 'new_fits': 0})
    with (OUT / 'frozen-verification.json').open('x', encoding='utf-8') as stream:
        json.dump(checks, stream, indent=2)
    print(json.dumps(checks))


if __name__ == '__main__':
    verify()
