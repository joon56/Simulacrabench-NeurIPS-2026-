"""A021 pure handwritten selector fixtures and public-schema audit; no model runs."""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
HEADS = ('s1_parent', 's2_child')
GRID = tuple(round(i*.1, 1) for i in range(10)) + (.95, .98)
ROLES = ('reference', 'fitting', 'calibration_legacy', 'calibration_replay', 'selection', 'evaluation')
DEADLINE = datetime(2026, 9, 26, 13, 56, tzinfo=timezone.utc).timestamp()


def section(name):
    match = re.match(r's(\d+[a-z]?)_', name)
    return match.group(1) if match else 'other'


def schema_links(schema):
    records = schema['items']
    links, given = [], 0
    for child, item in records.items():
        gate = item.get('gate')
        if item['class'] != 'PREDICT' or not gate:
            continue
        parent = gate['parent']
        if records[parent]['class'] == 'PREDICT':
            links.append((parent, child, section(parent) != section(child)))
        elif records[parent]['class'] == 'GIVEN':
            given += 1
    counts = {}
    for parent, child, cross in links:
        if cross:
            pair = section(parent)+' -> '+section(child)
            counts[pair] = counts.get(pair, 0)+1
    return {'predict_parent_edges': len(links), 'cross_section_edges': sum(x[2] for x in links),
            'given_parent_edges': given, 'cross_section_counts': counts,
            'cross_section_item_edges': [[p, c] for p, c, cross in links if cross],
            'definition': 'PREDICT child with PREDICT parent; section regex s(\\d+[a-z]?)_; no response data'}


def floor(values):
    if not values or not all(math.isfinite(x) and x >= 0 for x in values) or sum(values) <= 0:
        raise ValueError('Invalid probability vector')
    total = sum(values)
    return tuple(.001+(1-len(values)*.001)*(p/total) for p in values)


def row_log(vectors, labels):
    if set(vectors) != set(HEADS) or len(labels) != len(HEADS):
        raise ValueError('Head alignment')
    for name, label in zip(HEADS, labels):
        if not isinstance(label, int) or not 0 <= label < len(vectors[name]):
            raise ValueError('Option alignment')
    return sum(math.log(floor(vectors[n])[v]) for n, v in zip(HEADS, labels))/len(HEADS)


def blend(a, b, share):
    if not 0 <= share <= 1 or len(a) != len(b):
        raise ValueError('Mixture contract')
    return tuple(a) if share == 0 else tuple((1-share)*x+share*y for x, y in zip(a, b))


def render(table, evidence, lambdas):
    """Two-head exact-gate fixture, including cross-section parent propagation."""
    root = blend(table['full']['s1_parent'], evidence['s1_parent'], lambdas['s1_parent'])
    asked = root[1]
    hard = tuple(asked*p for p in table['conditional']) + (1-asked,)
    child_core = blend(table['full']['s2_child'], hard, table['agreement'])
    child = blend(child_core, evidence['s2_child'], lambdas['s2_child'])
    result = {'s1_parent': root, 's2_child': child}
    for p in result.values():
        floor(p)
    return result


def cluster_mean_se(differences, groups):
    if not differences or len(differences) != len(groups):
        raise ValueError('Group alignment')
    mean = sum(differences)/len(differences)
    totals, counts = {}, {}
    for value, group in zip(differences, groups):
        totals[group] = totals.get(group, 0.)+value
        counts[group] = counts.get(group, 0)+1
    g = len(counts)
    if g < 2:
        return mean, math.inf
    return mean, math.sqrt(g/(g-1)*sum((totals[k]-counts[k]*mean)**2 for k in counts)/len(differences)**2)


@dataclass(frozen=True)
class Rules:
    minimum_gain: float = .003
    se_multiplier: float = 2.


def qualifies(mean, se, rules):
    return mean > rules.minimum_gain and mean > rules.se_multiplier*se


@dataclass(frozen=True)
class Library:
    payload: str
    digest: str


@dataclass(frozen=True)
class Choice:
    candidate: str
    objective: str
    library_digest: str


def fixture_spec(child_change=False):
    """Literal mechanical cases, no random generator or fitted model."""
    rows = {'r0': {'role': 'reference', 'group': 'R0'}, 'r1': {'role': 'reference', 'group': 'R1'},
            'f0': {'role': 'fitting', 'group': 'F0'},
            'c0': {'role': 'calibration_legacy', 'group': 'C0'},
            'c1': {'role': 'calibration_replay', 'group': 'C1'}}
    rows.update({f's{i}': {'role': 'selection', 'group': f'S{i//2}'} for i in range(4)})
    rows.update({f'e{i}': {'role': 'evaluation', 'group': f'E{i}'} for i in range(2)})
    tables = {}
    for row, rec in rows.items():
        if rec['role'] in ('reference', 'fitting'):
            continue
        tables[row] = {'full': {'s1_parent': (.5, .5), 's2_child': (.1, .1, .8)},
                       'prior': {'s1_parent': (.5, .5), 's2_child': (.1, .1, .8)},
                       'conditional': (.8, .2), 'agreement': 1., 'legacy_bucket': 0,
                       'legacy': {'s1_parent': (.5, .5), 's2_child': (0., 0., 1.)},
                       'learned': {'s1_parent': (.1, .9), 's2_child': (.6, 0., .4) if child_change else (0., 0., 1.)}}
    return {'rows': rows, 'tables': tables, 'donors': ['r0', 'r1'],
            'calibration_labels': {'c0': (1, 0), 'c1': (1, 0)}}


def fixture_labels(role):
    if role == 'selection':
        return {f's{i}': (1, 2) for i in range(4)}
    if role == 'evaluation':
        return {f'e{i}': (1, 2) for i in range(2)}
    raise ValueError('Fixture role')


def validate_spec(spec):
    groups = {}
    for row, record in spec['rows'].items():
        if record['role'] not in ROLES:
            raise ValueError('Unknown role')
        previous = groups.setdefault(record['group'], record['role'])
        if previous != record['role']:
            raise ValueError('Cross-role group leakage')
    calibration = {r for r, v in spec['rows'].items() if v['role'].startswith('calibration_')}
    if set(spec['calibration_labels']) != calibration:
        raise ValueError('Only exact calibration response set is accepted')
    if not spec['donors'] or len(set(spec['donors'])) != len(spec['donors']):
        raise ValueError('Invalid donor bank')
    for donor in spec['donors']:
        if donor not in spec['rows'] or spec['rows'][donor]['role'] != 'reference':
            raise ValueError('Forbidden query donor')
    query = {r for r, v in spec['rows'].items() if v['role'] not in ('reference', 'fitting')}
    if query != set(spec['tables']) or query & set(spec['donors']):
        raise ValueError('Query/donor boundary')
    for table in spec['tables'].values():
        if table['legacy_bucket'] not in (0, 1):
            raise ValueError('Invalid frozen concentration bucket')
        for name in HEADS:
            width = 2 if name == HEADS[0] else 3
            for kind in ('full', 'prior', 'legacy', 'learned'):
                vec = table[kind][name]
                floor(vec)
                if len(vec) != width or abs(sum(vec)-1) > 1e-12:
                    raise ValueError('Manual table shape or mass')


def calibrate(spec, name, active):
    rows = [r for r, rec in spec['rows'].items() if rec['role'].startswith('calibration_')
            and (not active or rec['role'] == 'calibration_replay')]
    pair = []
    for bucket in (0, 1):
        selected = [r for r in rows if spec['tables'][r]['legacy_bucket'] == bucket]
        best, best_score = 0., -math.inf
        for lam in GRID:
            values = []
            for row in selected:
                table = spec['tables'][row]
                truth = spec['calibration_labels'][row][HEADS.index(name)]
                p = max(table['full'][name][truth], .001)
                e = table['learned' if active else 'legacy'][name][truth]
                values.append(math.log(max((1-lam)*p+lam*e, .001)))
            if not values:
                break  # Fixture threshold1; empty bucket uses original zero fallback.
            score = sum(values)/len(values)
            if score > best_score:
                best, best_score = lam, score
        pair.append(best)
    return tuple(pair), rows


def build_library(spec):
    validate_spec(spec)
    candidates = []
    masks = ((), ('1',), ('2',), ('1', '2'))
    for index, mask in enumerate(masks):
        lambdas, eligible = {}, {}
        for name in HEADS:
            lambdas[name], eligible[name] = calibrate(spec, name, section(name) in mask)
        proxy, deployed = {}, {}
        for row, table in spec['tables'].items():
            ev = {n: table['learned' if section(n) in mask else 'legacy'][n] for n in HEADS}
            proxy[row] = {n: blend(table['prior'][n], ev[n], .5) for n in HEADS}
            deployed[row] = render(table, ev, {n: lambdas[n][table['legacy_bucket']] for n in HEADS})
        candidates.append({'id': f'C{index}', 'active_sections': mask, 'lambdas': lambdas,
                           'calibration_rows': eligible, 'proxy': proxy, 'deployed': deployed})
    document = {'scope': 'HANDWRITTEN_FIXTURE_ONLY', 'heads': HEADS, 'rows': spec['rows'],
                'donors': spec['donors'], 'candidate_order': [x['id'] for x in candidates],
                'tables': spec['tables'], 'candidates': candidates,
                'calibration_rule': {'grid': GRID, 'minimum_bucket_rows': 1, 'production_minimum': 30}}
    payload = json.dumps(document, sort_keys=True, separators=(',', ':'), allow_nan=False)
    return Library(payload, hashlib.sha256(payload.encode()).hexdigest())


def decode(library):
    if hashlib.sha256(library.payload.encode()).hexdigest() != library.digest:
        raise ValueError('Frozen candidate hash mismatch')
    data = json.loads(library.payload)
    if data['scope'] != 'HANDWRITTEN_FIXTURE_ONLY':
        raise ValueError('Not a fixture library')
    return data


def role_rows(data, labels, role):
    rows = [r for r, rec in data['rows'].items() if rec['role'] == role]
    if not rows or set(labels) != set(rows):
        raise ValueError('Response role boundary')
    return rows


def select(library, objective, labels, rules):
    data = decode(library)
    rows = role_rows(data, labels, 'selection')
    if objective not in ('proxy', 'deployed'):
        raise ValueError('Unknown objective')
    logs = [[row_log(candidate[objective][r], labels[r]) for r in rows] for candidate in data['candidates']]
    # Stable first maximum implements the same candidate-order tie rule.
    winner = max(range(len(logs)), key=lambda i: sum(logs[i])/len(rows))
    mean, se = cluster_mean_se([a-b for a, b in zip(logs[winner], logs[0])],
                              [data['rows'][r]['group'] for r in rows])
    if not qualifies(mean, se, rules):
        winner = 0
    return Choice(data['candidate_order'][winner], objective, library.digest)


def compare_selectors(library, labels, objectives=('proxy', 'deployed'), rules=Rules()):
    """One library, information boundary, compute budget and rules for both arms."""
    if len(objectives) != 2:
        raise ValueError('Two controlled policies required')
    return tuple(select(library, objective, labels, rules) for objective in objectives)


def evaluate_fixture(library, choice, labels):
    data = decode(library)
    if choice.library_digest != library.digest:
        raise ValueError('Choice belongs to another candidate library')
    rows = role_rows(data, labels, 'evaluation')
    candidate = next(x for x in data['candidates'] if x['id'] == choice.candidate)
    # Always evaluate deployed outputs, including the proxy-selected policy.
    return sum(row_log(candidate['deployed'][r], labels[r]) for r in rows)/len(rows)


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify():
    """Run bounded fixture tests; write only the permitted verification record."""
    started = time.perf_counter()
    if time.time() >= DEADLINE:
        raise TimeoutError('A021 session deadline')
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[name] = '2'
    os.environ.update(CUDA_VISIBLE_DEVICES='', PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    sys.path.insert(0, str(ROOT))
    from scripts.check_e057 import MemoryTree  # Standard-library Windows resource monitor only.
    path = ROOT/'docs/analysis/A021-outputs/verification.json'
    report = json.loads(path.read_text(encoding='utf-8-sig'))
    for p, expected in {**report['protected_entry_hashes'], **report['input_hashes']}.items():
        if file_sha(ROOT/p) != expected:
            raise ValueError(f'Protected/input bytes changed: {p}')
    command = [sys.executable, '-m', 'pytest', 'tests/test_a021_selector_contract.py', '-q', '-p', 'no:cacheprovider']
    memory = MemoryTree(os.getpid())
    peak = memory.sample()
    process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               creationflags=subprocess.CREATE_NO_WINDOW)
    reason = 'COMPLETE'
    try:
        while process.poll() is None:
            try:
                for k, v in memory.sample().items():
                    peak[k] = max(peak[k], v)
            except OSError:
                if process.poll() is None:
                    reason = 'MONITOR_FAILURE'
            if max(peak.values()) >= 2*1024**3:
                reason = 'MEMORY_CAP'
            if time.time() >= DEADLINE:
                reason = 'TIME_CAP'
            if reason != 'COMPLETE':
                break
            time.sleep(.1)
    finally:
        if process.poll() is None:
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
        output = process.communicate(timeout=10)[0].decode('utf-8', errors='replace')
    schema_path = ROOT/'external/starter-kit/data/unhcr.json'
    schema = schema_links(json.loads(schema_path.read_text(encoding='utf-8')))
    fixture = build_library(fixture_spec())
    choices = compare_selectors(fixture, fixture_labels('selection'))
    attempt = {'command': '.venv/Scripts/python.exe scripts/check_a021_selector_contract.py',
               'child_command': ' '.join(command), 'test_output': output, 'test_exit_code': process.returncode,
               'resource_stop': reason, 'seconds': time.perf_counter()-started, 'peak_tree_bytes': peak,
               'script_sha256': file_sha(__file__), 'test_sha256': file_sha(ROOT/'tests/test_a021_selector_contract.py')}
    report.setdefault('attempts', []).append(attempt)
    report.update(status='TECHNICAL_PASS' if process.returncode == 0 and reason == 'COMPLETE' else 'TECHNICAL_FAIL',
                  empirical_disposition='HOLD', schema_sha256=file_sha(schema_path), schema=schema,
                  fixture_library_sha256=fixture.digest, mechanical_choices=[asdict(c) for c in choices],
                  scope='Handwritten fixture and public-schema mechanics only; no efficacy or frequency claim')
    path.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    print(output)
    print(json.dumps({k: report[k] for k in ('status', 'empirical_disposition', 'schema_sha256')}))
    print(json.dumps(schema))
    if report['status'] != 'TECHNICAL_PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    verify()
