"""Schema-only E054 resolution envelope. No model fits or respondent data."""
import hashlib
from importlib.metadata import version
import itertools
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'external/starter-kit'
OUTPUT = ROOT / 'docs/analysis/A013-outputs'
NAMES = ('unicef', 'world_bank', 'unhcr')


def schema_summary(schema, floor):
    items = [r for r in schema['items'].values() if r['class'] == 'PREDICT']
    gated = np.array([r.get('gate') is not None for r in items])
    classes = np.array([len(r['values']) + int(g) for r, g in zip(items, gated)])
    if not len(items) or np.any(classes * floor >= 1):
        raise ValueError('Invalid public class counts/floor')
    U = float(np.log(classes).mean())
    best_loss = -np.log(1 - (classes - 1) * floor) / (len(items) * U)
    max_loss = -np.log(floor) / (len(items) * U)
    return {'items': len(items), 'gated_items': int(gated.sum()), 'U': U,
            'n_dev': schema['split']['n_dev'], 'share': float(gated.mean()),
            'A': float(np.log(classes[gated]).sum() / (len(items) * U)),
            'gated_min_loss': float(best_loss[gated].sum()),
            'ungated_min_loss': float(best_loss[~gated].sum()),
            'gated_max_loss': float(gated.sum() * max_loss),
            'ungated_max_loss': float((~gated).sum() * max_loss),
            'min_skill': float(1 + np.log(floor) / U),
            'max_skill': float(1 - best_loss.sum())}


def losses(baseline, probe, A):
    return A - baseline + probe, 1 - A - probe


def noise_tails(summaries, floor, epsilon, draws, alpha):
    return [-np.log(floor) / (s['n_dev'] * s['U'] * epsilon)
            * np.log(draws / alpha) for s in summaries]


def priority(interval, margin=.015):
    if interval[0] > margin + 1e-10:
        return 'gated'
    if interval[1] < -margin - 1e-10:
        return 'ungated'
    return 'unresolved'


def make_problem(summaries, displayed, baseline_grand, probe_grand, tails, step, order):
    # True C1,C2,H,P; unrounded noised baseline Z0[3]; probe Z1[3].
    half = step / 2
    h = summaries[2]
    bounds = [(s['min_skill'], s['max_skill']) for s in summaries]
    bounds += [(1-h['A']-h['ungated_max_loss'], 1-h['A']-h['ungated_min_loss'])]
    bounds += [(x-half, x+half) for x in displayed] + [(None, None)] * 3
    rows, limits = [], []

    def constrain(coeff, lower, upper):
        rows.extend([np.asarray(coeff), -np.asarray(coeff)])
        limits.extend([upper, -lower])

    for offset, indices in ((4, (0, 1, 2)), (7, (0, 1, 3))):
        for j, index in enumerate(indices):
            row = np.zeros(10); row[offset+j] = 1; row[index] = -1
            constrain(row, -tails[j], tails[j])
    row = np.zeros(10); row[2] = -1; row[3] = 1
    constrain(row, h['gated_min_loss']-h['A'], h['gated_max_loss']-h['A'])
    if order == 'before':
        row = np.zeros(10); row[4:7] = 1 / 3
        constrain(row, baseline_grand-half, baseline_grand+half)
        probe_error = half
    elif order == 'after':
        if abs(np.mean(displayed) - baseline_grand) > half + 1e-12:
            return None
        # Outer relaxation of three individual rounding errors plus Grand rounding.
        # Informative arms require an additional literal rounded-score witness.
        probe_error = step
    else:
        raise ValueError('Reporting order must be before or after')
    row = np.zeros(10); row[7:10] = 1 / 3
    constrain(row, probe_grand-probe_error, probe_grand+probe_error)
    return {'A_ub': np.asarray(rows), 'b_ub': np.asarray(limits), 'bounds': bounds}


def solve(problem, objective):
    answer = linprog(objective, method='highs', **problem)
    if answer.status == 2:
        return None
    if not answer.success:
        raise RuntimeError(answer.message)
    return answer


def rounded_witness(problem, displayed, probe_grand, tails, step):
    if step == 0:
        return solve(problem, np.zeros(10)) is not None
    # Enumerate only rounded control values permitted by both bounded noises.
    choices = []
    for value, tail in zip(displayed[:2], tails[:2]):
        lo = int(np.ceil((value-step-2*tail) / step - 1e-10))
        hi = int(np.floor((value+step+2*tail) / step + 1e-10))
        choices.append(range(lo, hi+1))
    sum_lo = int(np.ceil(3*probe_grand/step-1.5+1e-9))
    sum_hi = int(np.floor(3*probe_grand/step+1.5-1e-9))
    for first, second, total in itertools.product(*choices, range(sum_lo, sum_hi+1)):
        published = np.array([first, second, total-first-second]) * step
        bounds = list(problem['bounds'])
        for j, value in enumerate(displayed):
            bounds[4+j] = (value-step/2+1e-6, value+step/2-1e-6)
        for j, value in enumerate(published):
            bounds[7+j] = (value-step/2+1e-6, value+step/2-1e-6)
        candidate = {**problem, 'bounds': bounds}
        answer = solve(candidate, np.zeros(10))
        if answer is not None:
            # Check the literal reporting path rather than only continuous bounds.
            actual = np.round(answer.x[7:10] / step) * step
            grand = round(float(actual.mean()) / step) * step
            baseline_actual = np.round(answer.x[4:7] / step) * step
            if (abs(grand - probe_grand) < 1e-9
                    and np.allclose(baseline_actual, displayed, atol=1e-10, rtol=0)):
                return {'true_skills': answer.x[:4].tolist(),
                        'baseline_noised': answer.x[4:7].tolist(),
                        'probe_noised': answer.x[7:10].tolist(),
                        'probe_published': actual.tolist(), 'grand': grand}
    return None


def reading_intervals(summaries, displayed, baseline_grand, probe_grand,
                      tails, step, order):
    problem = make_problem(summaries, displayed, baseline_grand, probe_grand,
                           tails, step, order)
    if problem is None or solve(problem, np.zeros(10)) is None:
        return None
    A = summaries[2]['A']
    objectives = {'gated_loss': (A, {2: -1, 3: 1}),
                  'ungated_loss': (1-A, {3: -1}),
                  'difference': (2*A-1, {2: -1, 3: 2})}
    result = {}
    for name, (constant, entries) in objectives.items():
        row = np.zeros(10)
        for index, value in entries.items():
            row[index] = value
        low, high = solve(problem, row), solve(problem, -row)
        result[name] = [float(constant+low.fun), float(constant-high.fun)]
    result['priority'] = priority(result['difference'])
    result['interval_kind'] = 'outer envelope; not point estimate'
    if order == 'after' and result['priority'] != 'unresolved':
        result['literal_rounding_witness'] = rounded_witness(
            problem, displayed, probe_grand, tails, step)
    return result


def run():
    if OUTPUT.exists() and any(OUTPUT.glob('e054-*')):
        raise FileExistsError('Refuse existing E054 resolution outputs')
    sys.path.insert(0, str(KIT))
    from make_sandbox import load_config
    config = load_config(str(KIT / 'config.yml'))
    floor, epsilon = config['scoring']['floor'], config['privacy']['epsilon']
    step = config['phases'][1]['round_to']
    summaries = [schema_summary(json.loads((KIT/'data'/f'{n}.json').read_text(encoding='utf-8')), floor)
                 for n in NAMES]
    displayed, baseline_grand = [.52, .49, .92], .64
    scenarios = {}
    for draws in (6, 93):
        tails = noise_tails(summaries, floor, epsilon, draws, .05)
        rows = []
        for tick in range(-100, 101):
            grand = tick / 100
            arms = {order: reading_intervals(summaries, displayed, baseline_grand,
                    grand, tails, step, order) for order in ('before', 'after')}
            if all(value is None for value in arms.values()):
                continue
            robust = (all(value is not None for value in arms.values())
                      and arms['before']['priority'] == arms['after']['priority']
                      and arms['before']['priority'] != 'unresolved'
                      and bool(arms['after'].get('literal_rounding_witness')))
            rows.append({'grand': grand, 'orders': arms, 'robust_informative': robust})
        scenarios[str(draws)] = {'laplace_tail_bounds': tails, 'readings': rows}
    informative = [r['grand'] for r in scenarios['93']['readings'] if r['robust_informative']]
    registration = (ROOT/'docs/experiments/E054-gated-loss-resolution.md').read_bytes()
    files = [Path(__file__), ROOT/'tests/test_e054_resolution.py', KIT/'score.py',
             KIT/'config.yml', KIT/'make_sandbox.py'] + [KIT/'data'/f'{n}.json' for n in NAMES]
    result = {'protocol': 'E054-schema-resolution-v1', 'model_fits': 0,
              'respondent_data_read': False, 'summaries': dict(zip(NAMES, summaries)),
              'baseline_display': displayed, 'baseline_grand': baseline_grand,
              'floor': floor, 'epsilon': epsilon, 'round_step': step,
              'alpha': .05, 'loss_priority_margin': .015,
              'scenarios': scenarios, 'informative_grand_readings': informative,
              'decision': 'PASS' if informative else 'STOP',
              'interpretation': 'Conditional public-mechanism sensitivity envelope; '
                '93 draws cover at most30 prior submissions plus one probe. Reporting '
                'order unverified; outside-envelope events and unknown extra noise '
                'are not excluded. Feasible arms are not probable-arm forecasts.',
              'source_hashes': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in files},
              'registration_sha256': hashlib.sha256(registration).hexdigest(),
              'versions': {n: version(n) for n in ('numpy', 'scipy')}}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT/'e054-registration.md').write_bytes(registration)
    with (OUTPUT/'e054-resolution.json').open('x', encoding='utf-8') as f:
        json.dump(result, f, indent=2, allow_nan=False)
    print(json.dumps({'decision': result['decision'], 'informative_grand': informative,
                      'readings93': scenarios['93']['readings']}, indent=2))


if __name__ == '__main__':
    run()
