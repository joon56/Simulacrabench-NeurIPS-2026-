"""Independent E053 scalar/provenance probe. No model fitting or label scoring."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
from scipy.optimize import minimize_scalar
from scripts import screen_e053 as screen

rng = np.random.default_rng(5381)
worst = 0.0
for trial in range(80):
    classes = int(rng.integers(2, 30))
    count = int(rng.integers(1, 100))
    base = rng.dirichlet(np.full(classes, .1), count)[:, 0]
    evidence = rng.dirichlet(np.full(classes, .1), count)[:, 0]
    result = screen.optimize_bucket(base, evidence, classes)
    def objective(weight):
        return float(np.log(.001 + (1 - classes * .001) *
                     (base + weight * (evidence - base))).mean())
    independent = minimize_scalar(lambda weight: -objective(weight),
        bounds=(0., .98), method='bounded', options={'xatol': 1e-14})
    value = max(objective(0.), objective(.98), -independent.fun)
    assert result['log_upper'] >= value - 1e-12, (trial, result, value)
    assert result['log_score'] >= value - 1e-10, (trial, result, value)
    worst = max(worst, abs(result['log_score'] - value))

prepared = []
for seed in (54, 55):
    frame, schema, masked, partitions, metadata = screen.prepare(seed)
    ids = np.asarray(metadata['source_ids'])
    assert len(ids) == len(np.unique(ids)) == 5000
    assert all(not set(partitions[a]) & set(partitions[b])
               for a in partitions for b in partitions if a != b)
    predicted = [n for n, item in schema['items'].items() if item['class'] == 'PREDICT']
    assert masked[predicted].iloc[2600:].isna().all().all()
    assert masked[predicted].iloc[:2600].notna().all().all()
    for relative, expected in metadata['prior_manifest_sha256'].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
    prepared.append({'seed': seed, 'unique_source_rows': len(ids),
        'prior_manifest_count': len(metadata['prior_manifest_sha256']),
        'audit_overlap_counts': {
            study: {role: len(rows) for role, rows in roles.items()}
            for study, roles in metadata['known_role_intersections']['audit'].items()}})

prior = json.loads((ROOT / 'docs/analysis/A011-outputs/adult-manifest.json').read_text())
compared = []
for relative, expected in prior['source_hashes'].items():
    if relative.startswith('src/'):
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected, relative
        compared.append(relative)
print(json.dumps({'scalar_probes_passed': 80, 'max_independent_score_difference': worst,
    'metadata_only_checks': prepared, 'unchanged_src_files': len(compared),
    'model_fits': 0, 'observed_label_scores': 0}, indent=2))
