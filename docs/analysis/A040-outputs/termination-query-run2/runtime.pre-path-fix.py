"""Cumulative actual-child allowance; one manually reviewed attempt per launch."""
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

EXPECTED = '0e68a80ce1237aaa0f95d42777a24154b5cee110858e0bf0a692c17a2d75939a'

def save(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)

def remaining(state):
    return max(0., 120. - state['used_seconds'])

def charge(state, started, ended):
    assert ended >= started
    state['used_seconds'] += ended - started

def check_start(state, *, mutation_possible, read_only=False, known_id=None):
    if state.get('active_attempt'):
        raise RuntimeError('Previous child not closed; reconcile before reentry')
    if remaining(state) <= 1:
        raise TimeoutError('Cumulative child allowance exhausted')
    if read_only:
        if not known_id:
            raise RuntimeError('Exact prior identity required for read-only confirmation')
    elif mutation_possible:
        raise RuntimeError('Possible termination already recorded; exact-ID reads only')
    elif remaining(state) <= 30:
        raise TimeoutError('Final30s reserved for exact-ID reads and receipt')

def claim_termination(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2)

def run_process(command, folder, limit, stem='child'):
    started = time.monotonic()
    killed = False
    with (folder / (stem + '-stdout.txt')).open('xb') as out, (folder / (stem + '-stderr.txt')).open('xb') as err:
        process = subprocess.Popen(command, stdout=out, stderr=err,
            creationflags=subprocess.CREATE_NO_WINDOW)
        save(folder / (stem + '-pid.json'), {'pid': process.pid, 'started_monotonic': started})
        try:
            process.wait(timeout=max(.001, limit - (time.monotonic() - started)))
        except subprocess.TimeoutExpired:
            killed = True
            process.kill()  # This helper cannot spawn subprocesses; kill only owned child.
            process.wait(timeout=1)
    ended = time.monotonic()
    return {'pid': process.pid, 'started_monotonic': started, 'ended_monotonic': ended,
            'wall_seconds': ended-started, 'exit_code': process.returncode, 'killed': killed}

def launch(read_only=False):
    folder = Path(__file__).resolve().parent
    entry = json.loads((folder / 'entry.json').read_text(encoding='utf-8-sig'))
    if datetime.now(timezone.utc) >= datetime.fromisoformat(entry['work_cutoff_utc']):
        raise TimeoutError('Session closeout reserve reached')
    ledger_path = folder / 'runtime-ledger.json'
    state = json.loads(ledger_path.read_text()) if ledger_path.exists() else {
        'used_seconds': 0., 'attempts': [], 'active_attempt': None, 'allowance_seconds': 120}
    prior = None
    possible = (folder / 'termination-intent.json').exists()
    for attempt in state['attempts']:
        path = folder / attempt['name'] / 'receipt.json'
        if path.exists():
            receipt = json.loads(path.read_text())
            possible |= bool(receipt.get('terminate_requests'))
            possible |= any(c['method'].startswith('SandboxTerminate') for c in receipt.get('calls', []))
            if receipt.get('sandbox_id') and receipt.get('identity'):
                prior = receipt
    check_start(state, mutation_possible=possible, read_only=read_only,
                known_id=prior.get('sandbox_id') if prior else None)
    paths = [folder / 'original/confirm_terminal.py', folder / 'runtime.py', folder / 'attempt.py']
    hashes = {str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert hashes['original/confirm_terminal.py'] == EXPECTED
    name = 'attempt-%02d' % (len(state['attempts']) + 1)
    attempt_dir = folder / name
    attempt_dir.mkdir()
    available = min(remaining(state), (datetime.fromisoformat(entry['work_cutoff_utc']) - datetime.now(timezone.utc)).total_seconds())
    assert available > (1 if read_only else 30)
    # Deadline begins only here, immediately before this child; one second is kept
    # for forced exit/reaping, also charged to the aggregate child allowance.
    started = time.monotonic()
    config = {'source_hashes': hashes, 'available_seconds': available,
        'deadline_monotonic': started + available - 1,
        'deadline_utc': (datetime.now(timezone.utc) + timedelta(seconds=available-1)).isoformat(),
        'read_only': read_only, 'prior': prior, 'call_cap_seconds': 14.5,
        'cumulative_used_before': state['used_seconds']}
    save(attempt_dir / 'config.json', config)
    state['active_attempt'] = name
    save(ledger_path, state)
    result = run_process([sys.executable, '-I', str(folder / 'attempt.py'), str(attempt_dir)],
                         attempt_dir, max(.001, config['deadline_monotonic'] - time.monotonic()))
    # Includes process construction, import/auth/waits, cancellation and reaping.
    charge(state, result['started_monotonic'], result['ended_monotonic'])
    result.update(name=name, closed_utc=datetime.now(timezone.utc).isoformat(), read_only=read_only)
    state['attempts'].append(result)
    state['active_attempt'] = None
    save(attempt_dir / 'usage.json', result)
    save(ledger_path, state)
    print(json.dumps({'attempt': name, 'exit_code': result['exit_code'],
        'child_seconds': result['wall_seconds'], 'cumulative_seconds': state['used_seconds'],
        'remaining_seconds': remaining(state), 'killed': result['killed']}))

if __name__ == '__main__':
    import ctypes
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    assert kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 3)
    launch(read_only='--read-only' in sys.argv)
