"""A023 injected boundary contract. No production imports, fitting or scoring."""
import ast
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sys
from types import MappingProxyType

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/analysis/A023-outputs'
FIT = frozenset(('reference', 'fit'))
CAL = frozenset(('calibration_legacy', 'calibration_replay'))
DEV = FIT | CAL | {'selection'}


@dataclass(frozen=True)
class Response:
    row: str
    role: str
    value: str


@dataclass(frozen=True)
class Frozen:
    payload: str
    digest: str

    def decode(self):
        if hashlib.sha256(self.payload.encode()).hexdigest() != self.digest:
            raise ValueError('Invalid digest')
        return json.loads(self.payload)


def seal(value):
    payload = json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)
    return Frozen(payload, hashlib.sha256(payload.encode()).hexdigest())


def fixture_roles():
    return {row: (role, 'group-' + role) for row, role in (
        ('r0', 'reference'), ('f0', 'fit'), ('c0', 'calibration_legacy'),
        ('c1', 'calibration_replay'), ('s0', 'selection'), ('e0', 'evaluation'))}


class RecordingStub:
    """Inert injected artifact/selector. IDs are prescribed, never score-selected."""
    def __init__(self):
        self.events = []

    def __call__(self, stage, labels, context):
        event = {'stage': stage, 'access': [(x.row, x.role) for x in labels], 'context': context}
        self.events.append(json.loads(json.dumps(event)))
        if stage.startswith('select_'):
            return context['candidate_order'][0]  # Mechanical fallback, no objective computation.
        return seal(event).digest


class Boundary:
    """Enforce prospective capability boundaries, not actual model nonleakage."""
    def __init__(self, roles, backend):
        group_roles = {}
        if {role for role, _ in roles.values()} != DEV | {'evaluation'}:
            raise ValueError('Incomplete role registry')
        for role, group in roles.values():
            if group in group_roles and group_roles[group] != role:
                raise ValueError('Cross-role group overlap')
            group_roles[group] = role
        self.roles = MappingProxyType(dict(roles))
        self.backend = backend
        self.library = None
        self.choices = None
        self.r_artifact = None
        self.started = False
        self.selection_started = False
        self.evaluation_started = False
        self.r_started = False

    def check_labels(self, labels, allowed):
        rows = [x.row for x in labels]
        expected = {row for row, (role, _) in self.roles.items() if role in allowed}
        if len(set(rows)) != len(rows) or set(rows) != expected:
            raise ValueError('Response role boundary')
        for response in labels:
            if response.role not in allowed or self.roles[response.row][0] != response.role:
                raise ValueError('Forged response role')

    def build(self, family, fitting, calibration):
        if self.started:
            raise ValueError('Builder frozen; no feedback or retry')
        # Validate all capabilities before even the first injected operation.
        self.check_labels(fitting, FIT)
        self.check_labels(calibration, CAL)
        if not family or family[0] != ('legacy', ()) or len({x[0] for x in family}) != len(family):
            raise ValueError('Invalid finite candidate family')
        if len({tuple(mask) for _, mask in family}) != len(family):
            raise ValueError('Duplicate masks')
        self.started = True
        base = self.backend('base_pd', fitting, {'normal_neural_calls': 3})
        metric = self.backend('metric', fitting, {'donor_role': 'reference', 'query_role': 'fit'})
        candidates = []
        for name, mask in family:
            context = {'id': name, 'mask': tuple(mask), 'base_artifact': base,
                       'metric_artifact': metric,
                       'inactive_roles': ['calibration_legacy', 'calibration_replay'],
                       'active_roles': ['calibration_replay'], 'minimum_bucket': 30,
                       'bucket_source': 'legacy_common_top10', 'empty_lambda': 0}
            lam = self.backend('lambda', calibration, context)
            render = self.backend('render', (), {'id': name, 'mask': tuple(mask),
                                  'lambda_artifact': lam, 'base_artifact': base,
                                  'metric_artifact': metric, 'order': 'global_schema_recursion',
                                  'representations': ['A021_proxy', 'recursive_deployed']})
            candidates.append({'id': name, 'mask': tuple(mask), 'lambda_artifact': lam,
                               'render_artifact': render})
        self.library = seal({
            'candidates': candidates, 'roles': dict(self.roles), 'base_artifact': base,
            'metric_artifact': metric,
            'rules': {'min_gain': .003, 'cluster_se_multiple': 2, 'minimum_bucket': 30,
                      'tie': 'candidate_order', 'fallback': 'legacy', 'floor': .001},
            'budget': {'base_pipelines': 2, 'normal_neural_calls': 6,
                       'pd_library_builds': 1, 'refits': 0}})
        return self.library

    def check_library(self, frozen):
        data = frozen.decode()
        if self.library is None or frozen != self.library:
            raise ValueError('Candidate/lambda identity changed')
        return data

    def choose(self, frozen, labels):
        data = self.check_library(frozen)
        if self.selection_started:
            raise ValueError('Selection frozen; no second attempt')
        self.check_labels(labels, {'selection'})
        self.selection_started = True
        context = {'library_digest': frozen.digest,
                   'candidate_order': [c['id'] for c in data['candidates']],
                   'rules': data['rules'], 'budget': data['budget']}
        choices = {}
        for policy in ('P', 'D'):
            # A fresh plain copy prevents a callback mutating the other policy's input.
            choice = self.backend('select_' + policy, labels, json.loads(json.dumps(context)))
            if choice not in context['candidate_order']:
                raise ValueError('Choice outside frozen candidate family')
            choices[policy] = choice
        self.choices = seal({'library_digest': frozen.digest, 'choices': choices})
        return self.choices

    def build_r(self, labels):
        if self.r_started or self.evaluation_started:
            raise ValueError('R construction budget exhausted')
        self.check_labels(labels, DEV)
        self.r_started = True
        self.r_artifact = self.backend('base_r', labels, {'normal_neural_calls': 3,
                                       'allocation': 'exact_R_development_visible_E_masked'})
        return self.r_artifact

    def evaluate(self, frozen, choices, labels):
        self.check_library(frozen)
        choices.decode()
        if choices != self.choices or self.evaluation_started:
            raise ValueError('Missing/changed frozen choices or evaluation already consumed')
        self.check_labels(labels, {'evaluation'})
        self.evaluation_started = True
        return self.backend('evaluate', labels, {'library_digest': frozen.digest,
                            'choices_digest': choices.digest, 'r_artifact': self.r_artifact,
                            'scores_computed': False})


def schema_family(schema):
    predicted = {n: r for n, r in schema['items'].items() if r['class'] == 'PREDICT'}
    def group(name):
        match = re.match(r's(\d+[a-z]?)_', name)
        return match.group(1) if match else 'other'
    sections = {}
    for item in predicted:
        sections.setdefault(group(item), []).append(item)
    edges = [(r['gate']['parent'], name) for name, r in predicted.items()
             if r.get('gate') and r['gate']['parent'] in predicted]
    cross = [(p, c) for p, c in edges if group(p) != group(c)]
    upstream = {group(p) for p, _ in cross}
    endpoints = upstream | {group(c) for _, c in cross}
    raw = (('legacy', ()), ('upstream', tuple(g for g in sections if g in upstream)),
           ('endpoints', tuple(g for g in sections if g in endpoints)))
    seen, family = set(), []
    for candidate in raw:
        if candidate[1] not in seen:
            family.append(candidate)
            seen.add(candidate[1])
    return {'sections': sections, 'candidates': tuple(family), 'predict_parent_edges': len(edges),
            'cross_section_edges': cross, 'mechanism_identifiable': len(family) > 1}


def static_cost():
    """Parse syntax only; fail if expected source call structure has changed."""
    def tree(relative):
        return ast.parse((ROOT / relative).read_text(encoding='utf-8-sig'))
    config_tree = tree('src/models/hh_cap.py')
    configs = next(ast.literal_eval(n.value) for n in config_tree.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'CONFIGS' for t in n.targets))
    source = tree('src/models/shared_trunk.py')
    tune = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == 'tune_and_train')
    loops = [n for n in ast.walk(tune) if isinstance(n, ast.For) and isinstance(n.iter, ast.Name)
             and n.iter.id == 'configs']
    def trains(node):
        return [n for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == '_train']
    assert len(configs) == 2 and len(loops) == 1
    assert len(trains(loops[0])) == 1 and len(trains(tune)) == 2
    metric = tree('src/models/supervised_retrieval.py')
    fit = next(n for n in metric.body if isinstance(n, ast.FunctionDef) and n.name == 'fit_sections')
    optimizers = [n for n in ast.walk(fit) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                  and n.func.id == 'minimize']
    assert len(optimizers) == 1
    return {'configs': configs, 'normal_base_pipelines': 2,
            'normal_neural_calls_per_pipeline': len(configs) + 1,
            'normal_neural_calls_total': 2 * (len(configs) + 1),
            'train_call_source_lines': [n.lineno for n in trains(tune)],
            'metric_optimizer_source_line': optimizers[0].lineno,
            'metric_optimizer_calls': 'M_PD + M_R; one per section per build',
            'actual_fits': 0, 'real_time_seconds': None, 'real_memory_bytes': None,
            'scope': 'Normal nonempty path only; see cost contract for branches'}


def verify():
    sys.path.insert(0, str(ROOT))
    import pytest
    result = pytest.main(['tests/test_a023_candidate_boundary.py', '-q', '-p', 'no:cacheprovider'])
    if result:
        return result
    schema = json.loads((ROOT / 'external/starter-kit/data/unhcr.json').read_text(encoding='utf-8'))
    family = schema_family(schema)
    cost = static_cost()
    stub = RecordingStub()
    boundary = Boundary(fixture_roles(), stub)
    def labels(allowed):
        return tuple(Response(row, role, 'invented') for row, (role, _) in boundary.roles.items()
                     if role in allowed)
    frozen = boundary.build(family['candidates'], labels(FIT), labels(CAL))
    choices = boundary.choose(frozen, labels({'selection'}))
    boundary.build_r(labels(DEV))
    boundary.evaluate(frozen, choices, labels({'evaluation'}))
    report = {'schema': family, 'static_cost': cost, 'events': stub.events,
              'fixture_library': json.loads(frozen.payload), 'fixture_library_sha256': frozen.digest,
              'fixture_choices_sha256': choices.digest,
              'fixture_role_digest': seal(fixture_roles()).digest,
              'real_split_hash': None, 'real_split_status': 'No real roles assigned or keys opened',
              'actual_fit_optimizer_predict_score_calls': 0,
              'production_modules_imported': [n for n in sys.modules if n.startswith('src.models')],
              'scope': 'Injected artifact tokens; no upstream computations or model parity tested'}
    assert not report['production_modules_imported']
    with (OUT / 'fixture-results.json').open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'schema_candidates': family['candidates'], 'static_cost': cost}))
    return 0


if __name__ == '__main__':
    if sys.argv[1:] != ['--verify']:
        raise SystemExit('Only --verify is supported; no empirical execution path')
    raise SystemExit(verify())
