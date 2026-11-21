"""Only new cumulative-time and mutation-lock boundaries; stdlib, no Modal."""
import json
from pathlib import Path
import sys
import tempfile
import time

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
assert (here / 'runtime.py').exists(), 'Cumulative runtime boundary not implemented yet'
from runtime import remaining, check_start, charge, claim_termination, run_process

passed = []
state = {'used_seconds': 0., 'attempts': [], 'active_attempt': None}
assert remaining(state) == 120
charge(state, 10, 14.25)
assert remaining(state) == 115.75
time.sleep(.01)  # Local repair time must not consume child-runtime allowance.
assert remaining(state) == 115.75
charge(state, 100, 181)
assert remaining(state) == 34.75
check_start(state, mutation_possible=False)
passed.append('cumulative_actual_child_only')
charge(state, 200, 205)
try:
    check_start(state, mutation_possible=False)
except TimeoutError:
    passed.append('last30_blocks_full_helper')
else:
    raise AssertionError('Discovery allowed in read reserve')
try:
    check_start({'used_seconds': 0, 'active_attempt': 'unknown'}, mutation_possible=False)
except RuntimeError:
    passed.append('unclosed_child_blocks_reentry')
else:
    raise AssertionError('Active child ignored')
with tempfile.TemporaryDirectory(prefix='budget-', dir=str(here.parents[3] / 'tmp' / 'a040-termination-query-run2')) as temp:
    path = Path(temp)
    journal = path / 'termination-intent.json'
    claim_termination(journal, {'sandbox_id': 'fixed-protocol-id'})
    try:
        claim_termination(journal, {'sandbox_id': 'fixed-protocol-id'})
    except FileExistsError:
        passed.append('durable_single_termination')
    else:
        raise AssertionError('Duplicate mutation accepted')
    try:
        check_start({'used_seconds': 0, 'active_attempt': None}, mutation_possible=True)
    except RuntimeError:
        passed.append('prior_or_uncertain_mutation_blocks_full_helper')
    else:
        raise AssertionError('Possible mutation ignored')
    result = run_process([sys.executable, '-I', '-c', 'import time;time.sleep(.05)'], path, .8)
    assert result['exit_code'] == 0 and result['wall_seconds'] >= .05
    result2 = run_process([sys.executable, '-I', '-c', 'import time;time.sleep(2)'], path, .35, stem='limited')
    assert result2['killed'] and result2['exit_code'] is not None and result2['wall_seconds'] < .8
    passed.extend(['real_child_lifetime_accounted', 'deadline_kills_owned_child'])
print(json.dumps({'outcome': 'BUDGET_BOUNDARY_PASS', 'cases': passed, 'actual_sdk_auth_rpc': 0}))
