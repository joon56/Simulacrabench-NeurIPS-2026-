"""Independent no-fit E054 artifact review; only public synthetic labels read."""
import gzip
import hashlib
import json
from pathlib import Path
import pickle
import sys
import zipfile
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'external/starter-kit'
sys.path.insert(0, str(KIT))
from make_sandbox import load_config, load_schema
from score import load_frames, sample_rows

DETAIL = ROOT / 'docs/analysis/E054-outputs'
SNAP = ROOT / 'submissions/2026-09-24-E054'
checks = 0


def check(condition, label):
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


manifest = read(SNAP / 'verification.json')
for group in ('source_hashes', 'artifact_hashes'):
    for name, expected in manifest[group].items():
        check(digest(ROOT / name) == expected, f'{group}:{name}')
base_path = ROOT / 'submissions/2026-09-19-E041/main.py'
raw = (SNAP / 'main.py').read_bytes()
check(digest(base_path) == manifest['base_main_sha256'], 'frozen E041 hash')
check(raw.startswith(base_path.read_bytes()), 'exact immutable E041 prefix')
check(digest(SNAP / 'main.py') == manifest['main_sha256'], 'main hash')
check(digest(SNAP.with_suffix('.zip')) == manifest['zip_sha256'], 'zip hash')
with zipfile.ZipFile(SNAP.with_suffix('.zip')) as archive:
    check(archive.namelist() == ['main.py'], 'main-only ZIP root')
    check(archive.read('main.py') == raw, 'ZIP source bytes')
check((DETAIL / 'extracted/main.py').read_bytes() == raw, 'extracted bytes')
check('OK:' in manifest['zip_checker'], 'checker recorded success')
check(digest(DETAIL / 'scorecard-prerun.md') == manifest['scorecard_prerun_sha256'], 'scorecard frozen')
config = load_config(str(KIT / 'config.yml'))
floor = config['scoring']['floor']
results = {}
for name in ('unicef', 'world_bank', 'unhcr'):
    summary = manifest['instruments'][name]
    source = read(DETAIL / f'{name}-source.json')
    official = read(DETAIL / f'{name}-official.json')
    bundle = pickle.loads(gzip.decompress((DETAIL / f'{name}-source.pkl.gz').read_bytes()))
    vectors = json.loads(gzip.decompress((DETAIL / f'{name}-official-predictions.json.gz').read_bytes()))
    schema = load_schema(str(KIT / 'data' / f'{name}.json'), config)
    respondents = load_frames(str(KIT / '_sandbox' / name), schema)
    frame, cells, truth = sample_rows(schema, respondents, 1)
    frame_hash = hashlib.sha256(pickle.dumps((schema, config, frame, cells, truth), protocol=5)).hexdigest()
    check(frame_hash == summary['frame_sha256'] == bundle['frame_sha256'], name + ' frame')
    check(digest(KIT / 'data' / f'{name}.json') == summary['schema_sha256'], name + ' schema')
    check(digest(KIT / '_sandbox' / name / 'respondents.parquet') == summary['data_sha256'], name + ' data')
    for path, expected in summary['baseline_cache_hashes'].items():
        check(digest(ROOT / path) == expected, path)
    cache41 = pickle.loads((ROOT / f'tmp/e043-eval/clean-{name}-E041.pkl').read_bytes())
    cache25 = pickle.loads((ROOT / f'tmp/e043-eval/clean-{name}-E025.pkl').read_bytes())
    check(cache41['source_sha256'] == manifest['base_main_sha256'], name + ' E041 provenance')
    check(cache41['frame_sha256'] == cache25['frame_sha256'] == frame_hash, name + ' cache inputs')
    check(cache25['source_sha256'] == '00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9', name + ' E025 provenance')
    check(len(vectors) == len(bundle['base']) == len(bundle['probe']) == len(cache41['vectors']) == len(cells) == official['n_cells'], name + ' lengths')
    options = {n: list(r['values']) + ([schema['gated_value']] if r.get('gate') is not None else [])
               for n, r in schema['items'].items() if r['class'] == 'PREDICT'}
    U = np.mean([np.log(len(v)) for v in options.values()])
    base_logs, probe_logs, gated = [], [], []
    for i, ((_, _, item), answer) in enumerate(zip(cells, truth)):
        old, new = np.asarray(bundle['base'][i]), np.asarray(bundle['probe'][i])
        check(np.array_equal(old, cache41['vectors'][i]), name + ' E041 raw parity')
        check(np.array_equal(new, vectors[i]), name + ' source official raw parity')
        is_gated = schema['items'][item].get('gate') is not None
        intended = name == 'unhcr' and is_gated
        check(np.array_equal(new, np.full(len(old), 1/len(old))) if intended else np.array_equal(new, old), name + ' target mask')
        check(len(new) == len(options[item]) and np.isfinite(new).all() and (new >= 0).all() and new.sum() > 0, name + ' vector contract')
        k = options[item].index(answer)
        base_logs.append(np.log(floor + (1-len(old)*floor) * old[k]/old.sum()))
        probe_logs.append(np.log(floor + (1-len(new)*floor) * new[k]/new.sum()))
        gated.append(is_gated)
    base_skill = float(1 + np.mean(base_logs)/U)
    probe_skill = float(1 + np.mean(probe_logs)/U)
    check(abs(base_skill-source['base_skill']) < 1e-12, name + ' independent base score')
    check(abs(probe_skill-source['skill']) < 1e-12 and abs(probe_skill-official['skill']) < 1e-12, name + ' independent probe score')
    check(abs(base_skill-cache25['skill']) <= .002, name + ' base no regression')
    replacements = sum(gated) if name == 'unhcr' else 0
    check(replacements == source['uniform_replacements'] and len(cells)-replacements == source['untouched_vectors'], name + ' mask counts')
    if name == 'unhcr':
        mask = np.asarray(gated)
        uniform_part = sum(np.log(len(options[cell[2]])) for cell in cells if schema['items'][cell[2]].get('gate') is not None)/(len(cells)*U)
        lg = -np.asarray(base_logs)[mask].sum()/(len(cells)*U)
        lc = -np.asarray(base_logs)[~mask].sum()/(len(cells)*U)
        check(abs(lg-(uniform_part-base_skill+probe_skill)) < 1e-12, 'independent gated decomposition')
        check(abs(lc-(1-uniform_part-probe_skill)) < 1e-12, 'independent ungated decomposition')
    check(official['status'] == 'PASS' and official['phase'] == 1, name + ' official qualification')
    check(summary['official_seconds'] == official['seconds'], name + ' timing provenance')
    results[name] = {'base_skill': base_skill, 'probe_skill': probe_skill, 'cells': len(cells), 'replacements': replacements, 'official_seconds': official['seconds']}
total = sum(value['official_seconds'] for value in results.values())
check(total == manifest['official_seconds_sum'] and total < 900, 'total local time')
check(manifest['technical_checks_passed'] and not manifest['probe_adopted'] and manifest['hosted_result'] is None, 'qualification only')
method = read(ROOT / 'submissions/phase2-E041-preparation/method-validation.json')
for entry in method['files']:
    check(digest(ROOT / entry['path']) == entry['sha256'], 'method hash ' + entry['path'])
check(method['rendered_pages'] == 4 and all(method['checks'].values()), 'method qualification record')
print(json.dumps({'status': 'PASS', 'checks': checks, 'model_fits': 0, 'public_synthetic_only': True,
                  'instruments': results, 'official_seconds_sum': total,
                  'interpretation': 'Technical measurement qualification, no model gain or hosted result'}, indent=2))
