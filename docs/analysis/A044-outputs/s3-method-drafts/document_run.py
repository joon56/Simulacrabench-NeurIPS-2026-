"""Bounded Windows document-only subprocess runner. No scientific imports."""
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


def save(path, obj):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(obj, stream, indent=2)


if sys.argv[1] == '--child':
    token, script, *arguments = sys.argv[2:]
    while not (OUT / (token + '.go')).exists():
        time.sleep(.02)
    sys.path.insert(0, str(ROOT / 'tmp/pdf-deps'))
    try:
        sys.argv = [str(OUT / script), *arguments]
        runpy.run_path(sys.argv[0], run_name='__main__')
    finally:
        (OUT / (token + '.done')).write_text('final sample requested')
        deadline = time.monotonic() + 10
        while not (OUT / (token + '.ack')).exists():
            if time.monotonic() > deadline:
                raise RuntimeError('observer final handshake missing')
            time.sleep(.02)
    raise SystemExit(0)


class Entry(C.Structure):
    _fields_ = [('size', W.DWORD), ('usage', W.DWORD), ('pid', W.DWORD),
        ('heap', C.c_size_t), ('module', W.DWORD), ('threads', W.DWORD),
        ('parent', W.DWORD), ('priority', W.LONG), ('flags', W.DWORD), ('name', W.WCHAR * 260)]


class Memory(C.Structure):
    _fields_ = [('cb', W.DWORD), ('faults', W.DWORD)] + [(name, C.c_size_t) for name in
        ('peak_rss', 'rss', 'peak_paged', 'paged', 'peak_nonpaged', 'nonpaged',
         'pagefile', 'peak_pagefile', 'private')]


kernel = C.WinDLL('kernel32', use_last_error=True)
kernel.CreateToolhelp32Snapshot.argtypes = [W.DWORD, W.DWORD]
kernel.CreateToolhelp32Snapshot.restype = W.HANDLE
kernel.Process32FirstW.argtypes = [W.HANDLE, C.POINTER(Entry)]
kernel.Process32NextW.argtypes = [W.HANDLE, C.POINTER(Entry)]
kernel.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
kernel.OpenProcess.restype = W.HANDLE
kernel.CloseHandle.argtypes = [W.HANDLE]
kernel.K32GetProcessMemoryInfo.argtypes = [W.HANDLE, C.POINTER(Memory), W.DWORD]
kernel.SetProcessAffinityMask.argtypes = [W.HANDLE, C.c_size_t]
kernel.TerminateProcess.argtypes = [W.HANDLE, W.UINT]


def census():
    handle = kernel.CreateToolhelp32Snapshot(2, 0)
    if handle == C.c_void_p(-1).value:
        raise C.WinError(C.get_last_error())
    entry = Entry()
    entry.size = C.sizeof(entry)
    result = {}
    try:
        good = kernel.Process32FirstW(handle, C.byref(entry))
        while good:
            result[entry.pid] = entry.parent
            good = kernel.Process32NextW(handle, C.byref(entry))
    finally:
        kernel.CloseHandle(handle)
    return result


def memory(pid):
    handle = kernel.OpenProcess(0x410, False, pid)
    if not handle:
        return None
    info = Memory()
    info.cb = C.sizeof(info)
    try:
        if not kernel.K32GetProcessMemoryInfo(handle, C.byref(info), info.cb):
            raise C.WinError(C.get_last_error())
        return {'pid': pid, 'rss': info.rss, 'private': info.private}
    finally:
        kernel.CloseHandle(handle)


token, script, *arguments = sys.argv[1:]
assert script in ('render_method.py', 'pdf_inspect.py')
previous = [json.loads(path.read_text()) for path in OUT.glob('resource-*.json')]
consumed = 30 + sum(row['seconds'] for row in previous)  # Conservative administration charge.
assert consumed < 300
assert datetime.datetime.now().astimezone() < datetime.datetime.fromisoformat('2026-10-23T18:16:00+09:00')
if script == 'render_method.py':
    candidate, attempt = arguments
    latches = [json.loads(path.read_text()) for path in OUT.glob('latch-*.json')]
    count = sum(row['script'] == script and row['arguments'][0] == candidate for row in latches)
    assert int(attempt) == count + 1 and count < 3
save(OUT / ('latch-' + token + '.json'), {'script': script, 'arguments': arguments,
     'charged_before': consumed, 'limit_remaining_seconds': 300-consumed,
     'at': datetime.datetime.now().astimezone().isoformat()})
env = dict(os.environ)
env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8', CUDA_VISIBLE_DEVICES='',
           OMP_NUM_THREADS='2', MKL_NUM_THREADS='2', OPENBLAS_NUM_THREADS='2')
env.pop('PYTHONPATH', None)
known, samples, failure, final = set(), [], None, False
start = time.monotonic()
with (OUT / ('run-' + token + '.log')).open('x', encoding='utf-8') as stream:
    child = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()),
             '--child', token, script, *arguments], cwd=ROOT, env=env,
             stdout=stream, stderr=subprocess.STDOUT)
    known.add(child.pid)
    try:
        assert kernel.SetProcessAffinityMask(int(child._handle), 3)
        while True:
            parents = census()
            while True:
                new = {pid for pid, parent in parents.items() if parent in known} - known
                if not new:
                    break
                known.update(new)
            rows = [value for pid in known | {os.getpid()} if (value := memory(pid)) is not None]
            now = time.monotonic() - start
            sample = {'seconds': now, 'rss': sum(row['rss'] for row in rows),
                      'private': sum(row['private'] for row in rows), 'processes': rows}
            samples.append(sample)
            assert sample['rss'] < 2*1024**3 and sample['private'] < 2*1024**3, 'memory cap'
            assert now < 300-consumed, 'aggregate document time cap'
            go = OUT / (token + '.go')
            if not go.exists():
                go.write_text('observer active; CPU affinity2 before document imports')
            ack = OUT / (token + '.ack')
            if (OUT / (token + '.done')).exists() and not ack.exists():
                final = True
                ack.write_text('final sample checked')
            if child.poll() is not None:
                break
            time.sleep(.1)
    except BaseException as exc:
        failure = repr(exc)
    finally:
        if failure or child.poll() is None:
            parents = census()
            for _ in range(4):
                known.update(pid for pid, parent in parents.items() if parent in known)
            for pid in sorted(known, reverse=True):
                handle = kernel.OpenProcess(1, False, pid)
                if handle:
                    kernel.TerminateProcess(handle, 91)
                    kernel.CloseHandle(handle)
        child.wait(timeout=10)
seconds = time.monotonic()-start
remnants = sorted(known.intersection(census()))
passed = child.returncode == 0 and failure is None and final and not remnants
report = {'token': token, 'script': script, 'arguments': arguments, 'seconds': seconds,
          'exit_code': child.returncode, 'failure': failure, 'passed': passed,
          'owned_pids': sorted(known), 'remnant_pids': remnants, 'final_sample_checked': final,
          'peak_tree_rss': max(row['rss'] for row in samples),
          'peak_tree_private': max(row['private'] for row in samples),
          'max_sample_gap_seconds': max((b['seconds']-a['seconds'] for a,b in zip(samples,samples[1:])), default=0),
          'memory_semantics': 'sampled concurrent process-tree sums including supervisor, not unsampled instantaneous peak',
          'samples': samples}
save(OUT / ('resource-' + token + '.json'), report)
print(json.dumps({key:value for key,value in report.items() if key != 'samples'}))
if not passed:
    raise SystemExit(1)
