"""Build and verify the E054 measurement; never upload or alter an incumbent."""
import argparse
import gzip
import hashlib
import inspect
import json
import os
from pathlib import Path
import pickle
import re
import subprocess
import sys
import time
import zipfile

for variable in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ[variable] = '2'
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
KIT = ROOT / 'external/starter-kit'
SNAPSHOT = ROOT / 'submissions/2026-09-24-E054'
DETAIL = ROOT / 'docs/analysis/E054-outputs'
NAMES = ('unicef', 'world_bank', 'unhcr')
BASE = ROOT / 'submissions/2026-09-19-E041/main.py'
BASE_HASH = '22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_new(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as handle:
        handle.write(raw)


def source_worker(name):
    import torch
    from unittest.mock import patch
    from scripts.check_daily_retrieval import get_case, CACHE, BASELINE_HASHES, difference
    from src.models import e041_gated_probe as probe, probes
    from score import floored, score
    torch.set_num_threads(2)
    path = DETAIL / f'{name}-source.pkl.gz'
    if path.exists():
        raise FileExistsError(path)
    config, schema, frame, cells, truth, frame_hash = get_case(name, 'clean')
    references, reference_hashes = {}, {}
    for label in ('E025', 'E041'):
        cache = CACHE / f'clean-{name}-{label}.pkl'
        record = pickle.loads(cache.read_bytes())
        assert record['frame_sha256'] == frame_hash
        assert record['source_sha256'] == BASELINE_HASHES[label]
        references[label] = record
        reference_hashes[cache.relative_to(ROOT).as_posix()] = digest(cache)
    captured = {}
    original = probe.retrieval.predict
    def capture(*args, **kwargs):
        if captured:
            raise AssertionError('Unexpected repeated base fit')
        captured['vectors'] = original(*args, **kwargs)
        return captured['vectors']
    start = time.perf_counter()
    with patch.object(probe.retrieval, 'predict', side_effect=capture):
        vectors = probe.predict(frame, schema)
    elapsed = time.perf_counter() - start
    base = captured['vectors']
    # Freeze both endpoints before scoring this fixed measurement.
    bundle = {'base': base, 'probe': vectors, 'frame_sha256': frame_hash}
    write_new(path, gzip.compress(pickle.dumps(bundle, protocol=5), mtime=0))
    measured = score(schema, config, floored(vectors, schema, cells, .001), truth, cells)
    base_score = score(schema, config, floored(base, schema, cells, .001), truth, cells)
    assert difference(base, references['E041']['vectors']) == 0
    assert abs(base_score['skill'] - references['E025']['skill']) <= .002
    untouched, changed = 0, 0
    for before, after, cell in zip(base, vectors, cells):
        intended = name == 'unhcr' and schema['items'][cell[2]].get('gate') is not None
        if intended:
            assert all(x == 1/len(after) for x in after)
            changed += 1
        else:
            assert list(before) == list(after)
            untouched += 1
    decomposition = None
    if name == 'unhcr':
        decomposition = probes.decompose(base, truth, cells, schema, .001, probes.gated_items)
        assert abs(decomposition['probe_skill'] - measured['skill']) < 1e-12
    else:
        assert measured['skill'] == base_score['skill']
    result = {'instrument': name, 'phase': 1, 'cells': len(cells),
              'skill': measured['skill'], 'base_skill': base_score['skill'],
              'base_delta_e025': base_score['skill']-references['E025']['skill'],
              'base_raw_parity_e041': 0, 'untouched_vectors': untouched,
              'uniform_replacements': changed, 'seconds': elapsed,
              'decomposition': decomposition, 'frame_sha256': frame_hash,
              'schema_sha256': digest(KIT/'data'/f'{name}.json'),
              'data_sha256': digest(KIT/'_sandbox'/name/'respondents.parquet'),
              'baseline_cache_hashes': reference_hashes,
              'predictions_sha256': digest(path)}
    write_new(DETAIL/f'{name}-source.json', json.dumps(result, indent=2).encode())
    print(json.dumps(result), flush=True)


def execute(command, log, env, cwd=ROOT):
    done = subprocess.run(command, cwd=cwd, env=env, text=True, encoding='utf-8',
                          errors='replace', capture_output=True)
    write_new(log, (done.stdout+done.stderr).encode('utf-8'))
    if done.returncode:
        raise RuntimeError(f'Command failed; see {log}')
    return done.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-worker', choices=NAMES)
    args = parser.parse_args()
    if args.source_worker:
        source_worker(args.source_worker)
        return
    if (SNAPSHOT/'main.py').exists() or SNAPSHOT.with_suffix('.zip').exists() or DETAIL.exists():
        raise FileExistsError('Refuse existing E054 package/run namespace')
    assert digest(BASE) == BASE_HASH
    resolution = ROOT/'docs/analysis/A013-outputs/e054-resolution.json'
    assert json.loads(resolution.read_text(encoding='utf-8'))['decision'] == 'PASS'
    assert (SNAPSHOT/'SCORES.md').exists()
    from src.models.e041_gated_probe import apply_probe
    wrapper = ('\n\n'+inspect.getsource(apply_probe)+'\n_e054_base_predict = predict\n'
               'def predict(frame, schema):\n'
               '    return apply_probe(_e054_base_predict(frame, schema), frame, schema)\n')
    raw = BASE.read_bytes() + wrapper.encode('utf-8')
    write_new(SNAPSHOT/'main.py', raw)
    archive = SNAPSHOT.with_suffix('.zip')
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as bundle:
        bundle.writestr('main.py', raw)
    extracted = DETAIL/'extracted'
    write_new(extracted/'main.py', raw)
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    env.pop('PYTHONPATH', None)
    checker = execute([sys.executable, str(KIT/'tools/check_submission_zip.py'), str(archive)],
                      DETAIL/'zip-check.log', env)
    assert 'OK:' in checker
    manifest = {'phase': 1, 'purpose': 'measurement only, not score improvement',
                'resolution_sha256': digest(resolution), 'main_sha256': digest(SNAPSHOT/'main.py'),
                'zip_sha256': digest(archive), 'base_main_sha256': digest(BASE),
                'scorecard_prerun_sha256': digest(SNAPSHOT/'SCORES.md'),
                'source_hashes': {p.relative_to(ROOT).as_posix(): digest(p)
                    for p in sorted((ROOT/'src').rglob('*.py'))+[Path(__file__),
                        ROOT/'tests/test_e054_probe.py', KIT/'score.py', KIT/'config.yml']},
                'zip_checker': checker.strip(), 'instruments': {}, 'hosted_result': None}
    write_new(DETAIL/'prerun.json', json.dumps(manifest, indent=2).encode())
    write_new(DETAIL/'scorecard-prerun.md', (SNAPSHOT/'SCORES.md').read_bytes())
    for name in NAMES:
        execute([sys.executable, str(__file__), '--source-worker', name],
                DETAIL/f'{name}-source.log', env)
        summary = json.loads((DETAIL/f'{name}-source.json').read_text(encoding='utf-8'))
        stdout = execute([sys.executable, str(KIT/'score.py'), '--submission', str(extracted),
            '--data', str(KIT/'_sandbox'/name), '--schema', str(KIT/'data'/f'{name}.json'),
            '--phase', '1', '--keep', '--log', str(DETAIL/f'{name}-official.json')],
            DETAIL/f'{name}-official.log', env, KIT)
        official = json.loads((DETAIL/f'{name}-official.json').read_text(encoding='utf-8'))
        assert official['status'] == 'PASS' and official['phase'] == 1
        work = Path(re.search(r'^\[work\] (.+)$', stdout, re.MULTILINE).group(1).strip())
        predictions = json.loads((work/'predictions.json').read_text(encoding='utf-8'))
        saved = pickle.loads(gzip.decompress((DETAIL/f'{name}-source.pkl.gz').read_bytes()))
        assert len(predictions) == len(saved['probe']) == official['n_cells']
        assert all(a == list(b) for a,b in zip(predictions, saved['probe']))
        assert official['skill'] == summary['skill']
        write_new(DETAIL/f'{name}-official-predictions.json.gz',
                  gzip.compress((work/'predictions.json').read_bytes(), mtime=0))
        manifest['instruments'][name] = {**summary, 'official_seconds': official['seconds'],
                                        'source_official_raw_parity': 0, 'status': 'PASS'}
        print(name, json.dumps(manifest['instruments'][name]), flush=True)
    assert set(manifest['instruments']) == set(NAMES)
    total = sum(r['official_seconds'] for r in manifest['instruments'].values())
    assert total < 900
    manifest.update(official_seconds_sum=total, technical_checks_passed=True,
                    local_unchanged_base_no_regression=True, probe_adopted=False)
    manifest['artifact_hashes'] = {p.relative_to(ROOT).as_posix(): digest(p)
                                  for p in sorted(DETAIL.rglob('*')) if p.is_file()}
    write_new(SNAPSHOT/'verification.json', json.dumps(manifest, indent=2).encode())
    print('COMPLETE', total, flush=True)


if __name__ == '__main__':
    main()
