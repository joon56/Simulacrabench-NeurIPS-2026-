"""Windows stdlib-only process-tree observer, pre-import handshake and budget latch."""
import ctypes as C
from ctypes import wintypes as W
import datetime
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
TEMP = ROOT / 'tmp/a044-e025-phase2'
LIMIT = 8 * 1024**3


def write(path, obj):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(obj, stream, indent=2)


def bootstrap(token, action):
    gate = TEMP / (token + '.go')
    deadline = time.monotonic() + 20
    while not gate.exists():
        if time.monotonic() > deadline:
            raise RuntimeError('observer startup handshake missing')
        time.sleep(.02)
    try:
        if action == 'checks':
            sys.argv = [str(OUT / 'check_boundaries.py')]
            runpy.run_path(sys.argv[0], run_name='__main__')
        else:
            sys.argv = [str(OUT / 'task.py'), action]
            runpy.run_path(sys.argv[0], run_name='__main__')
    finally:
        (TEMP / (token + '.done')).write_text('ready for final memory sample')
        deadline = time.monotonic() + 20
        while not (TEMP / (token + '.ack')).exists():
            if time.monotonic() > deadline:
                raise RuntimeError('observer final sample handshake missing')
            time.sleep(.02)


class Entry(C.Structure):
    _fields_ = [('size', W.DWORD), ('usage', W.DWORD), ('pid', W.DWORD),
                ('heap', C.c_size_t), ('module', W.DWORD), ('threads', W.DWORD),
                ('parent', W.DWORD), ('priority', W.LONG), ('flags', W.DWORD),
                ('name', W.WCHAR * 260)]


class Memory(C.Structure):
    _fields_ = [('cb', W.DWORD), ('faults', W.DWORD)] + [(name, C.c_size_t) for name in
        ('peak_rss', 'rss', 'peak_paged', 'paged', 'peak_nonpaged', 'nonpaged',
         'pagefile', 'peak_pagefile', 'private')]


K = C.WinDLL('kernel32', use_last_error=True)
K.CreateToolhelp32Snapshot.argtypes = [W.DWORD, W.DWORD]
K.CreateToolhelp32Snapshot.restype = W.HANDLE
K.Process32FirstW.argtypes = [W.HANDLE, C.POINTER(Entry)]
K.Process32NextW.argtypes = [W.HANDLE, C.POINTER(Entry)]
K.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
K.OpenProcess.restype = W.HANDLE
K.CloseHandle.argtypes = [W.HANDLE]
K.K32GetProcessMemoryInfo.argtypes = [W.HANDLE, C.POINTER(Memory), W.DWORD]
K.SetProcessAffinityMask.argtypes = [W.HANDLE, C.c_size_t]
K.TerminateProcess.argtypes = [W.HANDLE, W.UINT]


def census():
    handle = K.CreateToolhelp32Snapshot(2, 0)
    if handle == C.c_void_p(-1).value:
        raise C.WinError(C.get_last_error())
    entry = Entry()
    entry.size = C.sizeof(entry)
    rows = {}
    try:
        good = K.Process32FirstW(handle, C.byref(entry))
        while good:
            rows[entry.pid] = entry.parent
            good = K.Process32NextW(handle, C.byref(entry))
    finally:
        K.CloseHandle(handle)
    return rows


def memory(pid):
    handle = K.OpenProcess(0x410, False, pid)
    if not handle:
        return None
    info = Memory()
    info.cb = C.sizeof(info)
    try:
        if not K.K32GetProcessMemoryInfo(handle, C.byref(info), info.cb):
            raise C.WinError(C.get_last_error())
        return {'pid': pid, **{key: getattr(info, key) for key in
                               ('rss', 'private', 'peak_rss', 'peak_pagefile')}}
    finally:
        K.CloseHandle(handle)


def supervise(action, token):
    from task import over_memory, remaining
    TEMP.mkdir(parents=True, exist_ok=True)
    previous = [json.loads(path.read_text()) for path in OUT.glob('resource-*.json')]
    # Charge all initial shell inspections/red check/administration conservatively once.
    administrative_reserve = 120.0
    consumed = administrative_reserve + sum(row['elapsed_seconds'] for row in previous)
    limit = 900 if action in ('source', 'official') else 120
    limit = min(limit, remaining(2700, consumed))
    if action == 'checks':
        checks = [row for row in previous if row['action'] == 'checks']
        assert len(checks) < 3
        limit = min(limit, remaining(120, .3690211 + sum(row['elapsed_seconds'] for row in checks)))
    old_latches = [json.loads(path.read_text()) for path in OUT.glob('latch-*.json')]
    if action in ('source', 'official'):
        all3 = [row for row in old_latches if row['action'] in ('source', 'official')]
        assert len(all3) < 3
        assert action not in [row['action'] for row in all3], 'repeat requires documented invalid-arm repair gate'
        assert (OUT / 'baseline-reuse.json').exists()
        assert all(row['passed'] for row in previous if row['action'] == 'checks')
        assert any(row['action'] == 'checks' for row in previous)
    assert datetime.datetime.now().astimezone() < datetime.datetime.fromisoformat('2026-10-23T18:10:00+09:00')
    latch = {'action': action, 'token': token, 'created': datetime.datetime.now().astimezone().isoformat(),
             'shared_seconds': limit, 'charged_before': consumed, 'administrative_reserve': administrative_reserve}
    write(OUT / ('latch-' + token + '.json'), latch)
    env = dict(os.environ)
    env.update(OMP_NUM_THREADS='2', MKL_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2',
               NUMEXPR_NUM_THREADS='2', CUDA_VISIBLE_DEVICES='', PYTHONDONTWRITEBYTECODE='1',
               PYTHONIOENCODING='utf-8', HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
               TEMP=str(TEMP), TMP=str(TEMP))
    env.pop('PYTHONPATH', None)
    known, samples, failure = set(), [], None
    final_sample = False
    start = time.monotonic()  # Monitor active before launching bootstrap or imports.
    log = OUT / ('run-' + token + '.log')
    with log.open('x', encoding='utf-8') as stream:
        process = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()),
                                    '--child', token, action], cwd=ROOT, env=env,
                                   stdout=stream, stderr=subprocess.STDOUT)
        known.add(process.pid)
        try:
            if not K.SetProcessAffinityMask(int(process._handle), 3):
                raise C.WinError(C.get_last_error())
            while True:
                parents = census()
                expanded = True
                while expanded:
                    new = {pid for pid, parent in parents.items() if parent in known} - known
                    known.update(new)
                    expanded = bool(new)
                rows = [row for pid in known | {os.getpid()} if (row := memory(pid)) is not None]
                sample = {'seconds': time.monotonic() - start, 'processes': rows,
                          'rss': sum(row['rss'] for row in rows),
                          'private': sum(row['private'] for row in rows)}
                samples.append(sample)
                if over_memory(rows, LIMIT):
                    raise RuntimeError('owned tree RSS/private memory cap breached')
                remaining(limit, sample['seconds'])
                gate = TEMP / (token + '.go')
                if not gate.exists():
                    gate.write_text('observer sampled; CPU affinity2 before scientific imports')
                done = TEMP / (token + '.done')
                ack = TEMP / (token + '.ack')
                if done.exists() and not ack.exists():
                    # This sample participates in exactly the same cap predicate above.
                    final_sample = True
                    ack.write_text('final sample checked')
                if process.poll() is not None:
                    break
                time.sleep(.2)
        except BaseException as exc:
            failure = repr(exc)
        finally:
            if failure or process.poll() is None:
                parents = census()
                for _ in range(4):
                    known.update(pid for pid, parent in parents.items() if parent in known)
                for pid in sorted(known, reverse=True):
                    handle = K.OpenProcess(1, False, pid)
                    if handle:
                        K.TerminateProcess(handle, 91)
                        K.CloseHandle(handle)
            process.wait(timeout=10)
    remnant = sorted(known.intersection(census()))
    elapsed = time.monotonic() - start
    passed = failure is None and process.returncode == 0 and final_sample and not remnant and elapsed < limit
    report = {**latch, 'elapsed_seconds': elapsed, 'exit_code': process.returncode,
              'failure': failure, 'passed': passed, 'owned_pids': sorted(known), 'remnant_pids': remnant,
              'final_sample_enforced': final_sample, 'cpu_affinity_mask': 3,
              'sample_count': len(samples), 'max_sample_gap_seconds': max(
                  (b['seconds'] - a['seconds'] for a, b in zip(samples, samples[1:])), default=0),
              'peak_sampled_tree_rss': max((row['rss'] for row in samples), default=0),
              'peak_sampled_tree_private': max((row['private'] for row in samples), default=0),
              'peak_semantics': 'Concurrent sampled process-tree sums include supervisor; .2s requested cadence. '
                  'Observed maximum gap reported. Not an unsampled instantaneous or hosted-memory guarantee.',
              'samples': samples}
    write(OUT / ('resource-' + token + '.json'), report)
    print(json.dumps({key: value for key, value in report.items() if key != 'samples'}), flush=True)
    if not passed:
        raise SystemExit(1)


if __name__ == '__main__':
    if sys.argv[1] == '--child':
        bootstrap(sys.argv[2], sys.argv[3])
    else:
        supervise(sys.argv[1], sys.argv[2])
