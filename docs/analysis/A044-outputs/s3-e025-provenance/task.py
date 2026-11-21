"""Bounded A044 provenance work. Existing scientific files are read-only."""
import ast
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import pickle
import platform
import re
import shutil
import subprocess
import sys
import time
import zipfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
KIT = ROOT / 'external/starter-kit'
TEMP = ROOT / 'tmp/a044-e025-phase2'
NAMES = ('unicef', 'world_bank', 'unhcr')
COUNTS = dict(zip(NAMES, (41676, 92112, 308637)))


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(name, obj):
    path = OUT / name
    with path.open('x', encoding='utf-8') as stream:
        json.dump(obj, stream, indent=2, allow_nan=False)
    return digest(path)


def over_memory(rows, cap):
    return any(sum(row[key] for row in rows) >= cap for key in ('rss', 'private'))


def remaining(limit, elapsed):
    result = limit - elapsed
    if result <= 0:
        raise RuntimeError('shared time budget exhausted')
    return result


def scientific_imports():
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(KIT))
    import numpy as np
    import pandas as pd
    import score
    import make_sandbox
    return np, pd, score, make_sandbox


def masked_frame(path, schema, reader=None, items=None, scored=None, role=None):
    import numpy as np
    import pandas as pd
    if items is None:
        from make_sandbox import generated_items, scored_items, ROLE_COLUMN
        items, scored, role = generated_items(schema), scored_items(schema), ROLE_COLUMN
    reader = reader or pd.read_parquet
    # No TEST PREDICT column is requested in the hidden-role read.
    columns = ['respondent_id'] + items
    visible = reader(path, columns=columns,
                     filters=[(role, 'in', ['TRAIN', 'DEV'])]).astype(object)
    given = [item for item in items if item not in set(scored)]
    hidden = reader(path, columns=['respondent_id'] + given,
                    filters=[(role, '==', 'TEST')]).astype(object)
    visible = visible[columns].reset_index(drop=True)
    hidden = hidden.reindex(columns=columns).astype(object).reset_index(drop=True)
    blanked = hidden.copy()
    blanked[scored] = np.nan
    frame = pd.concat([visible, blanked], ignore_index=True)
    ids = hidden.respondent_id.to_numpy(dtype=object)
    cells = [(len(visible) + row, ids[row], item)
             for row in range(len(hidden)) for item in items if item in set(scored)]
    assert frame.iloc[len(visible):][scored].isna().all().all()
    return frame, cells


def frame_hash(schema, frame, cells):
    return hashlib.sha256(pickle.dumps((schema, frame, cells), protocol=5)).hexdigest()


def assert_identities():
    for group in read(OUT / 'identity-gate.json').values():
        if isinstance(group, list):
            for row in group:
                assert row['match'] and digest(ROOT / row['path']) == row['actual'], row['path']


def gate():
    assert_identities()
    baseline = read(ROOT / 'submissions/phase2-E041-preparation/verification.json')
    supplement = read(ROOT / 'submissions/phase2-E041-preparation/supplemental-verification.json')
    closure = read(OUT / 'source-closure.json')['files']
    # Validate the frozen manual trace, without searching any unrelated source.
    imports = {}
    for path in closure:
        tree = ast.parse((ROOT / path).read_text(encoding='utf-8-sig'))
        local = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and (node.module or '').startswith('src'):
                modules = ([node.module + '.' + item.name for item in node.names]
                           if node.module in ('src', 'src.models') else [node.module])
                for module in modules:
                    target = module.replace('.', '/') + '.py'
                    assert target in closure, (path, target)
                    local.append(target)
        imports[path] = sorted(set(local))
    packages = {name: importlib.metadata.version(name) for name in supplement['packages']}
    assert packages == supplement['packages'], (packages, supplement['packages'])
    assert sys.version == baseline['python'], sys.version
    extra = {name: importlib.metadata.version(name) for name in ('PyYAML', 'threadpoolctl')}
    environment = {'python': sys.version, 'executable': sys.executable, 'packages': packages,
                   'additional_current_only': extra, 'platform_current_only': platform.platform(),
                   'historical_threads': baseline['local_threads'],
                   'environment_variables': {key: os.environ.get(key) for key in
                       ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'CUDA_VISIBLE_DEVICES')},
                   'limitation': 'A012 package/source provenance collected post-run. Historical PyYAML, '
                       'threadpoolctl, OS, native BLAS/build and affinity were not recorded; no values reconstructed. '
                       'Frozen raw reuse is qualified for exact identities/ordered values, not environment replay or hosted equivalence.'}
    save('environment.json', environment)
    static_paths = ['external/starter-kit/config.yml', 'external/starter-kit/tools/check_submission_zip.py',
                    'submissions/2026-09-25-E025/main.py', 'submissions/2026-09-25-E025.zip',
                    'submissions/2026-09-25-E041/main.py']
    static = {path: digest(ROOT / path) for path in static_paths}
    for path in static_paths[:2]:
        assert static[path] == supplement['artifacts_sha256'][path]
    assert static[static_paths[2]] == baseline['e025_main_sha256']
    assert static[static_paths[3]] == '142921c3ea843c653821cf06a8b3fab89e8e6c96592581590f7e970064d90c6f'
    assert (ROOT / static_paths[3]).stat().st_size == 11240
    assert static[static_paths[4]] == baseline['e041_main_sha256']
    frozen = read(ROOT / 'docs/analysis/A018-outputs/freeze-manifest.json')
    assert frozen['frozen_files_sha256'][static_paths[3]] == static[static_paths[3]]
    assert 'OK:' in frozen['checks']['E025']['zip_checker']
    with zipfile.ZipFile(ROOT / static_paths[3]) as archive:
        members = archive.namelist()
        assert 'main.py' in members and 'requirements.txt' not in members
        assert all(name in ('main.py', 'LICENSE-starter-kit.txt') for name in members), members
        assert archive.read('main.py') == (ROOT / static_paths[2]).read_bytes()
        member_hashes = {name: hashlib.sha256(archive.read(name)).hexdigest() for name in members}
    save('static-freeze.json', {'sha256': static, 'imports': imports, 'archive_members': member_hashes,
         'checker': {'decision': 'REUSE_NO_RERUN', 'prior_pass': frozen['checks']['E025']['zip_checker'],
                     'checker_sha256': static[static_paths[1]],
                     'basis': 'A018 freeze manifest same ZIP plus A012 historical and pinned kit checker identity'},
         'kit_compatibility': 'Reuse s3-prep pinned ee427a9/f980ef5 comparison; no network query'})
    np, pd, scorer, sandbox = scientific_imports()
    config = sandbox.load_config(str(KIT / 'config.yml'))
    assert config['scoring']['floor'] == .001
    assert scorer.PHASE_ROLES[2] == {'visible': ('TRAIN', 'DEV'), 'hidden': 'TEST'}
    results = {}
    for name in NAMES:
        schema = sandbox.load_schema(str(KIT / 'data' / (name + '.json')), config)
        path = KIT / '_sandbox' / name / 'respondents.parquet'
        frame, cells = masked_frame(path, schema)
        reference = baseline['instruments'][name]
        current_hash = frame_hash(schema, frame, cells)
        assert current_hash == reference['frame_sha256'], (name, current_hash, reference['frame_sha256'])
        assert len(cells) == COUNTS[name]
        raw = read(ROOT / f'docs/analysis/A012-outputs/E041-{name}-source.json')
        official = read(ROOT / f'docs/analysis/A012-outputs/E041-{name}-official-predictions.json')
        assert raw['phase'] == 2 and raw['visible_roles'] == ['TRAIN', 'DEV'] and raw['hidden_role'] == 'TEST'
        assert raw['frame_sha256'] == current_hash and raw['n_cells'] == len(cells)
        assert raw['schema_sha256'] == reference['schema_sha256']
        assert raw['data_sha256'] == reference['data_sha256']
        source_path = raw['source_path'].replace('\\', '/')
        assert raw['source_sha256'] == supplement['artifacts_sha256'][source_path]
        assert raw['vectors'] == official
        scorer.check(schema, raw['vectors'], cells)
        assert raw['skill'] == reference['e041_source_skill'] == reference['e041_official_skill']
        results[name] = {'cells': len(cells), 'frame_sha256': current_hash,
                         'ordered_cells_sha256': hashlib.sha256(pickle.dumps(cells, protocol=5)).hexdigest(),
                         'historical_source_path': source_path, 'historical_source_sha256': raw['source_sha256'],
                         'full_raw_exact': True, 'completion_receipt': True,
                         'validation': 'stock check: width, finite, nonnegative, positive sum'}
        print('GATE', name, len(cells), 'exact', flush=True)
    save('baseline-reuse.json', {'verdict': 'QUALIFIED_FROZEN_RAW_REUSE', 'instruments': results,
          'scope': 'Exact frozen ordered E041 outputs on exact synthetic inputs/scorer; no E041 refit.',
          'historical_provenance': supplement['provenance_timing'],
          'environment_limitations': environment['limitation'],
          'truth': 'TEST PREDICT not requested in frame preparation; no fresh scoring at this gate.'})


def source():
    assert read(OUT / 'baseline-reuse.json')['verdict'] == 'QUALIFIED_FROZEN_RAW_REUSE'
    assert_identities()
    np, pd, scorer, sandbox = scientific_imports()
    import torch
    torch.set_num_threads(2)
    from src.models.hh_cap import predict
    config = sandbox.load_config(str(KIT / 'config.yml'))
    rows = {}
    for name in NAMES:
        schema = sandbox.load_schema(str(KIT / 'data' / (name + '.json')), config)
        frame, cells = masked_frame(KIT / '_sandbox' / name / 'respondents.parquet', schema)
        fh = frame_hash(schema, frame, cells)
        assert fh == read(OUT / 'baseline-reuse.json')['instruments'][name]['frame_sha256']
        start = time.monotonic()
        vectors = [[float(value) for value in row] for row in predict(frame, schema)]
        seconds = time.monotonic() - start
        scorer.check(schema, vectors, cells)
        raw_hash = save(f'E025-{name}-source.json', {'instrument': name, 'phase': 2,
                       'frame_sha256': fh, 'n_cells': len(cells), 'vectors': vectors})
        rows[name] = {'cells': len(cells), 'predict_seconds': seconds, 'raw_sha256': raw_hash,
                      'frame_sha256': fh}
        print('SOURCE', name, len(cells), seconds, flush=True)
    # This all3 freeze must exist before any dedicated evaluator can read truth.
    save('source-all3-freeze.json', {'instruments': rows, 'at_unix': time.time(),
         'identity_gate_sha256': digest(OUT / 'identity-gate.json'),
         'source_closure_sha256': digest(OUT / 'source-closure.json'),
         'environment_sha256': digest(OUT / 'environment.json'),
         'truth_read_by_source': False})


def official():
    assert_identities()
    assert set(read(OUT / 'source-all3-freeze.json')['instruments']) == set(NAMES)
    archive_path = ROOT / 'submissions/2026-09-25-E025.zip'
    assert digest(archive_path) == read(OUT / 'static-freeze.json')['sha256'][str(archive_path.relative_to(ROOT)).replace('\\', '/')]
    extracted = TEMP / 'preserved-E025'
    extracted.mkdir(parents=True, exist_ok=False)
    with zipfile.ZipFile(archive_path) as archive:
        for name, expected in read(OUT / 'static-freeze.json')['archive_members'].items():
            data = archive.read(name)
            assert hashlib.sha256(data).hexdigest() == expected
            (extracted / name).write_bytes(data)
    assert not (extracted / 'requirements.txt').exists()
    records = {}
    for name in NAMES:
        command = [sys.executable, '-B', str(KIT / 'score.py'), '--submission', str(extracted),
                   '--data', str(KIT / '_sandbox' / name), '--schema', str(KIT / 'data' / (name + '.json')),
                   '--config', str(KIT / 'config.yml'), '--phase', '2', '--keep',
                   '--log', str(OUT / f'E025-{name}-official.json')]
        log_path = OUT / f'E025-{name}-official.log'
        start = time.monotonic()
        with log_path.open('x', encoding='utf-8') as stream:
            done = subprocess.run(command, cwd=KIT, stdout=stream, stderr=subprocess.STDOUT)
        assert done.returncode == 0, (name, done.returncode)
        text = log_path.read_text(encoding='utf-8')
        match = re.search(r'^\[work\] (.+)$', text, re.MULTILINE)
        assert match, name
        work = Path(match.group(1).strip()).resolve()
        assert work.is_relative_to(TEMP.resolve()), work
        raw_path = work / 'predictions.json'
        target = OUT / f'E025-{name}-official-predictions.json'
        with target.open('xb') as stream:
            stream.write(raw_path.read_bytes())
        summary = read(OUT / f'E025-{name}-official.json')
        assert summary['status'] == 'PASS' and summary['phase'] == 2
        assert summary['n_cells'] == COUNTS[name]
        records[name] = {'raw_sha256': digest(target), 'status': summary['status'],
                         'cells': summary['n_cells'], 'skill': summary['skill'],
                         'official_seconds': summary['seconds'],
                         'wall_seconds': time.monotonic() - start,
                         'work': str(work.relative_to(ROOT)).replace('\\', '/')}
        print('OFFICIAL', name, 'PASS', records[name]['wall_seconds'], flush=True)
    save('official-all3-freeze.json', {'instruments': records, 'at_unix': time.time(),
         'truth_policy': 'Stock official scorer owns truth in its original sequence; predictor receives only masked frame.'})


def evaluate():
    assert_identities()
    source_freeze = read(OUT / 'source-all3-freeze.json')
    official_freeze = read(OUT / 'official-all3-freeze.json')
    assert set(source_freeze['instruments']) == set(official_freeze['instruments']) == set(NAMES)
    for name in NAMES:
        assert digest(OUT / f'E025-{name}-source.json') == source_freeze['instruments'][name]['raw_sha256']
        assert digest(OUT / f'E025-{name}-official-predictions.json') == official_freeze['instruments'][name]['raw_sha256']
    np, pd, scorer, sandbox = scientific_imports()
    config = sandbox.load_config(str(KIT / 'config.yml'))
    rows = {}
    for name in NAMES:
        schema = sandbox.load_schema(str(KIT / 'data' / (name + '.json')), config)
        # Dedicated evaluation begins only after BOTH all3 freezes were checked above.
        respondents = scorer.load_frames(str(KIT / '_sandbox' / name), schema)
        frame, cells, truth = scorer.sample_rows(schema, respondents, 2)
        assert frame_hash(schema, frame, cells) == source_freeze['instruments'][name]['frame_sha256']
        source_raw = read(OUT / f'E025-{name}-source.json')['vectors']
        official_raw = read(OUT / f'E025-{name}-official-predictions.json')
        baseline_raw = read(ROOT / f'docs/analysis/A012-outputs/E041-{name}-source.json')
        assert source_raw == official_raw, ('raw parity', name)
        values = []
        for vectors in (source_raw, baseline_raw['vectors']):
            scorer.check(schema, vectors, cells)
            normalized = scorer.floored(vectors, schema, cells, .001)
            logp = [float(np.log(vector[sandbox.options_for(schema, cell[2]).index(answer)]))
                    for vector, cell, answer in zip(normalized, cells, truth)]
            skill = 1 + float(np.mean(logp)) / scorer.uniform_reference(schema)
            values.append(skill)
        e025, e041 = values
        assert abs(e025 - official_freeze['instruments'][name]['skill']) < 1e-12
        assert abs(e041 - baseline_raw['skill']) < 1e-12
        rows[name] = {'cells': len(cells), 'source_archive_raw_exact': True,
                      'e025_skill': e025, 'reused_e041_skill': e041,
                      'e025_minus_e041': e025 - e041,
                      'absolute_difference_le_0p002': abs(e025 - e041) <= .002}
        print('EVALUATION', name, json.dumps(rows[name]), flush=True)
    save('comparison.json', {'instruments': rows,
         'all_raw_exact': True, 'all_absolute_gate': all(row['absolute_difference_le_0p002'] for row in rows.values()),
         'ordered_vectors': sum(row['cells'] for row in rows.values()),
         'no_new_subgroup_head_diagnostics': True})


if __name__ == '__main__':
    globals()[sys.argv[1]]()
