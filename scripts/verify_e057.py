"""Verify frozen E057 execution artifacts without fitting or scoring labels."""

import pickle
import subprocess

from check_e057 import ROOT, OUT, LOCAL, BASE, BASE_HASH, imports, read, save, sha


def main():
    imports()
    import numpy as np
    from src.models.conditional_leaf_content import layout, split_visible, apply_policy

    manifest = read(OUT / 'preflight.json')
    checked = {**manifest['source_files'], **manifest['prior_source_files']}
    for path, expected in checked.items():
        assert sha(ROOT / path) == expected, path
    assert sha(BASE) == BASE_HASH
    assert sha(OUT / 'registration.md') == manifest['registration_sha256']
    records = {n: read(OUT / f'{n}-execution.json') for n in manifest['inputs']}
    local_hashes = {}
    for name, record in records.items():
        path = LOCAL / f'{name}-vectors.pkl'
        assert sha(path) == record['predictions_sha256']
        local_hashes[path.relative_to(ROOT).as_posix()] = sha(path)
    record = records['unhcr']
    for filename, key in [('split.json', 'split_sha256'), ('masked-shadow.pkl', 'masked_shadow_sha256'),
                          ('shadow-library.pkl', 'shadow_library_sha256'), ('refit-library.pkl', 'refit_library_sha256'),
                          ('forced-vectors.pkl', 'forced_predictions_sha256')]:
        path = LOCAL / filename
        assert sha(path) == record[key], filename
        local_hashes[path.relative_to(ROOT).as_posix()] = sha(path)
    roles = read(LOCAL / 'split.json')
    schema, masked = pickle.loads((LOCAL / 'masked-shadow.pkl').read_bytes())
    predicted, leaves, _ = layout(schema)
    audit = read(OUT / 'schema-audit.json')
    assert leaves == [entry['name'] for entry in audit['targets']]
    visible = np.sort(roles['fit'] + roles['selection'] + roles['validation'])
    for name, actual in zip(('fit', 'selection', 'validation'), split_visible(visible)):
        np.testing.assert_array_equal(roles[name], actual)
    assert len(set(roles['fit']) | set(roles['selection']) | set(roles['validation'])) == len(visible)
    assert masked.iloc[roles['shadow_query']][predicted].isna().all().all()
    assert masked.iloc[roles['fit']][predicted].notna().all().all()
    assert set(roles['query']).isdisjoint(visible)
    assert set(roles['shadow_query']) == set(roles['selection'] + roles['validation'] + roles['query'])
    selection, policy = read(OUT / 'selection.json'), read(OUT / 'policy.json')
    for file, key in [('selection.json', 'selection_sha256'), ('policy.json', 'policy_sha256')]:
        assert sha(OUT / file) == record[key]
    events = [entry['event'] for entry in record['events']]
    assert events.index('shadow_frozen') < events.index('selection_frozen') < events.index('policy_frozen') < events.index('refit_frozen')
    if any(selection['shares'].values()):
        validation = read(OUT / 'validation.json')
        assert events.index('selection_frozen') < events.index('validation_scored') < events.index('policy_frozen')
        expected = selection['shares'] if validation['accepted'] else dict.fromkeys(leaves, 0.)
        assert policy['shares'] == expected
        path = LOCAL / 'validation-differences.pkl'
        assert sha(path) == validation['differences_sha256']
        local_hashes[path.relative_to(ROOT).as_posix()] = sha(path)
    else:
        assert 'validation_scored' not in events and not (OUT / 'validation.json').exists()
        assert not any(policy['shares'].values())
    library = pickle.loads((LOCAL / 'refit-library.pkl').read_bytes())
    frozen = pickle.loads((LOCAL / 'unhcr-vectors.pkl').read_bytes())['candidate']
    rebuilt = apply_policy(library['base'], predicted, library['query'], library['trees'], policy['shares'])
    assert len(frozen) == len(rebuilt)
    assert all(np.array_equal(a, b) for a, b in zip(frozen, rebuilt))
    result, runtime = read(OUT / 'result.json'), read(OUT / 'runtime.json')
    aggregate = read(OUT / 'aggregate-memory.json')
    assert runtime['exit_code'] == 0 and runtime['reason'] == 'COMPLETE'
    assert runtime['parent_inclusive_seconds'] < 900 and result['conservative_fit_seconds'] < 1200
    assert aggregate['reason'] == 'COMPLETE'
    assert max(aggregate['peak_sum_lifetime_rss_bytes'], aggregate['peak_sum_lifetime_commitment_bytes']) < 8 * 1024**3
    assert result['no_regression_pass']
    assert record['forced_fixture']['changed_vectors'] > 0 and not record['forced_fixture']['score_access']
    protected = subprocess.check_output(['git', '-c', f'safe.directory={ROOT.as_posix()}', 'diff',
        '9284bf4d277e339a9ae4a334d6cf7ee7bde2c6ba', '--name-only', '--', 'submissions',
        'docs/analysis/E056-outputs', 'docs/experiments/E056-conditional-leaf-content.md',
        'scripts/screen_e056.py', 'src/models/link_sharp.py', 'src/models/supervised_retrieval.py',
        'src/models/shared_trunk.py'], cwd=ROOT, text=True)
    assert not protected.strip(), protected
    summary = {'status': 'PASS', 'checked_source_hashes': len(checked), 'local_hashes': local_hashes,
        'schema_targets': len(leaves), 'split_counts': record['role_counts'], 'frozen_refit_vectors_exact': len(frozen),
        'protected_paths_unchanged': True, 'new_fits': 0, 'new_label_scores': 0,
        'verifier_sha256': sha(__file__),
        'aggregate_hashes': {p.name: sha(p) for p in OUT.glob('*.json')},
        'scope': 'Frozen arithmetic, role masking, hashes and limits; no independent efficacy audit.'}
    save(OUT / 'frozen-verification.json', summary)
    print({k: v for k, v in summary.items() if k not in ('local_hashes', 'aggregate_hashes')})


if __name__ == '__main__':
    main()
