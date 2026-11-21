"""Run only A023 tiny fixtures with a Windows process-tree resource watchdog."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/analysis/A023-outputs'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--red', action='store_true')
    args = parser.parse_args()
    path = OUT / ('red-resources.json' if args.red else 'verification.json')
    if path.exists():
        raise FileExistsError('Preserve prior verification; no silent rerun')
    started = time.perf_counter()
    entry = json.loads((OUT / 'entry.json').read_text(encoding='utf-8'))
    deadline = datetime.fromisoformat(entry['deadline_utc'].replace('Z', '+00:00')).timestamp()
    for name in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[name] = '2'
    os.environ.update(CUDA_VISIBLE_DEVICES='', PYTHONDONTWRITEBYTECODE='1',
                      PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    sys.path.insert(0, str(ROOT))
    # Module top-level imports only stdlib; no E057 operation is invoked.
    from scripts.check_e057 import MemoryTree
    command = ([sys.executable, '-B', '-m', 'pytest', 'tests/test_a023_candidate_boundary.py',
                '-q', '-p', 'no:cacheprovider'] if args.red else
               [sys.executable, '-B', 'scripts/check_a023_candidate_boundary.py', '--verify'])
    report = {'started_utc': datetime.now(timezone.utc).isoformat(), 'command': command,
              'real_fits': 0, 'real_optimizer_calls': 0, 'response_reads': 0,
              'parquet_reads': 0, 'cache_decodes': 0, 'real_predictions': 0, 'real_scores': 0,
              'scope': 'Owned tiny-fixture worker plus monitor, not real model runtime',
              'cpu_threads_limit': 2, 'memory_limit_bytes': 2 * 1024**3,
              'sample_seconds': .1, 'worker_wall_limit_seconds': 60}
    process = None
    peak = None
    reason = 'COMPLETE'
    output = ''
    try:
        monitor = MemoryTree(os.getpid())
        peak = monitor.sample()  # Must work before launching fixtures.
        if time.time() >= deadline or max(peak.values()) >= 2 * 1024**3:
            raise RuntimeError('Prelaunch resource cap')
        process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
        while process.poll() is None:
            try:
                sample = monitor.sample()
                peak = {key: max(peak[key], sample[key]) for key in peak}
            except OSError:
                if process.poll() is None:
                    raise
            if max(peak.values()) >= 2 * 1024**3:
                reason = 'MEMORY_CAP'
                break
            if time.time() >= deadline or time.perf_counter() - started >= 60:
                reason = 'TIME_CAP'
                break
            time.sleep(.1)
    except Exception as exc:
        reason = 'MONITOR_OR_LAUNCH_FAILURE'
        report['error'] = repr(exc)
    finally:
        if process is not None:
            if process.poll() is None:
                subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
            output = process.communicate(timeout=10)[0].decode('utf-8', errors='replace')
        report.update(resource_stop=reason, peak_tree_bytes=peak,
                      seconds_including_worker_imports=time.perf_counter() - started,
                      test_output=output, exit_code=None if process is None else process.returncode)
        expected_red = args.red and 'No module named' in output and 'check_a023_candidate_boundary' in output
        passed = process is not None and process.returncode == 0 and reason == 'COMPLETE'
        report['status'] = 'EXPECTED_RED' if expected_red and reason == 'COMPLETE' else (
            'TECHNICAL_PASS' if passed else 'TECHNICAL_STOP')
        report['empirical_disposition'] = 'HOLD'
        report['code_hashes'] = {
            str(p.relative_to(ROOT)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (ROOT / 'scripts').glob('check_a023_*.py')}
        report['code_hashes'].update({
            str(p.relative_to(ROOT)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (ROOT / 'tests').glob('test_a023_*.py')})
        path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        print(output)
        print(json.dumps({k: report[k] for k in ('status', 'resource_stop', 'seconds_including_worker_imports', 'peak_tree_bytes')}))
    return 0 if report['status'] in ('EXPECTED_RED', 'TECHNICAL_PASS') else 1


if __name__ == '__main__':
    raise SystemExit(main())
