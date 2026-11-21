"""Own-tree 120s watchdog; no model imports; persistent one-invocation latch."""
import ctypes
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import psutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CAP = 16_000_000_000
DEADLINE = datetime(2026, 10, 2, 3, 45, tzinfo=timezone.utc)


class MemoryStatus(ctypes.Structure):
    _fields_ = [('length', ctypes.c_ulong), ('load', ctypes.c_ulong)] + [
        (name, ctypes.c_ulonglong) for name in ('total_phys', 'avail_phys', 'total_page',
                                              'avail_page', 'total_virtual', 'avail_virtual', 'extended')]


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2), encoding='utf-8')


def main():
    mem = MemoryStatus()
    mem.length = ctypes.sizeof(mem)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem)):
        raise RuntimeError('Host availability measurement unavailable')
    available = dict(physical=mem.avail_phys, commitment=mem.avail_page)
    if min(available.values()) < CAP:
        save('run-resources.json', dict(outcome='BLOCKED_RESOURCE', available=available, started=False))
        return 2
    if (DEADLINE - datetime.now(timezone.utc)).total_seconds() < 150:
        save('run-resources.json', dict(outcome='INCOMPLETE', reason='Insufficient original task time', started=False))
        return 2
    controller = psutil.Process()
    affinity = controller.cpu_affinity()[:2]
    controller.cpu_affinity(affinity)
    with (HERE / 'scientific-started.json').open('x', encoding='utf-8') as latch:
        json.dump(dict(start_utc=datetime.now(timezone.utc).isoformat(), invocations=1,
                       deadline_seconds=120, memory_cap=CAP, affinity=affinity), latch)
    start = time.perf_counter()
    reason = None
    samples = []
    processes = []
    with (HERE / 'stdout.txt').open('wb') as out, (HERE / 'stderr.txt').open('wb') as err:
        child = subprocess.Popen([sys.executable, '-I', '-B', '-u', str(HERE / 'runner.py')],
                                 cwd=ROOT, stdout=out, stderr=err,
                                 creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            while child.poll() is None:
                elapsed = time.perf_counter() - start
                descendants = controller.children(recursive=True)
                processes = [controller] + descendants
                rss = private = 0
                for process in processes:
                    try:
                        process.cpu_affinity(affinity)
                        info = process.memory_info()
                        rss += info.rss
                        private += info.private
                    except psutil.NoSuchProcess:
                        continue
                sample = dict(elapsed=elapsed, rss=rss, commitment=private,
                              pids=[p.pid for p in processes])
                samples.append(sample)
                with (HERE / 'resource-samples.jsonl').open('a', encoding='utf-8') as stream:
                    stream.write(json.dumps(sample) + '\n')
                if elapsed >= 120:
                    reason = '120-second scientific deadline'
                    break
                if max(rss, private) > CAP:
                    reason = 'Host process-tree resource cap'
                    break
                time.sleep(min(1, max(.001, 120-(time.perf_counter()-start))))
        except BaseException as exc:
            reason = 'Measurement/controller error: ' + repr(exc)
        finally:
            if reason is not None:
                for process in reversed(controller.children(recursive=True)):
                    try:
                        process.kill()
                    except psutil.NoSuchProcess:
                        pass
            child.wait(timeout=10)
    elapsed = time.perf_counter() - start
    result_path = HERE / 'result.json'
    result = json.loads(result_path.read_text()) if result_path.exists() else {}
    outcome = result.get('outcome', 'INCOMPLETE')
    if reason:
        outcome = 'LOCAL_RESOURCE_LIMIT' if 'resource cap' in reason else 'INCOMPLETE'
    save('run-resources.json', dict(outcome=outcome, reason=reason, child_exit=child.returncode,
         elapsed_seconds=elapsed, sample_period_seconds=1, samples=len(samples),
         rss_peak_sampled=max((x['rss'] for x in samples), default=0),
         commitment_peak_sampled=max((x['commitment'] for x in samples), default=0),
         includes_watchdog=True, available_before=available, host_cap=CAP,
         gpu=result.get('gpu'), full_path_measured=False,
         remaining_children=[p.pid for p in controller.children(recursive=True)]))
    print(json.dumps(dict(outcome=outcome, seconds=elapsed, reason=reason)))
    return 0 if outcome == 'LOCAL_CONTRACT_PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
