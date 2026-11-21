"""Single scientific invocation. Never invoke without the parent watchdog."""
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import traceback

START = time.perf_counter()
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
TEMP = ROOT / 'tmp/a040-local-technical'
SOURCE = TEMP / 'source/tabicl-0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3/src'
CHECKPOINT = TEMP / 'acquisition/tabicl-classifier-v2-20260212.ckpt'
COUNTERS = dict(fits=0, predicts=0, loads=0)
TIMINGS = dict(fit_seconds=0., predict_seconds=0., load_seconds=0.)
NETWORK = dict(deliberate_blocked=0, package_attempts=0, subprocess_attempts=0)
EVENTS = (HERE / 'events.jsonl').open('x', encoding='utf-8')


def event(name, **values):
    EVENTS.write(json.dumps(dict(event=name, elapsed=time.perf_counter()-START, **values)) + '\n')
    EVENTS.flush()


def main():
    import psutil
    me = psutil.Process()
    me.cpu_affinity(me.cpu_affinity()[:2])
    for name in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[name] = '2'
    os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
                      HF_HOME=str(ROOT / 'tmp/a040-local-technical-retry1/hf-cache'), A040_CHECKPOINT=str(CHECKPOINT))
    deliberate = [True]

    def audit(name, args):
        if name in ('socket.connect', 'socket.getaddrinfo', 'socket.sendto'):
            NETWORK['deliberate_blocked' if deliberate[0] else 'package_attempts'] += 1
            raise PermissionError('A040 runtime network denied')
        if name in ('subprocess.Popen', 'os.system', 'os.posix_spawn'):
            NETWORK['subprocess_attempts'] += 1
            raise PermissionError('A040 child subprocess denied')

    sys.addaudithook(audit)
    import socket
    with socket.socket() as probe:
        try:
            probe.connect(('127.0.0.1', 9))
        except PermissionError:
            pass
        else:
            raise AssertionError('Network guard did not block')
    deliberate[0] = False
    event('network_guard', scope='Python audit, not OS firewall', passed=True)
    manifest = json.loads((HERE / 'frozen-inputs/run-manifest.json').read_text(encoding='utf-8-sig'))
    for row in manifest['files']:
        assert hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest() == row['sha256'], row['path']
    event('frozen_hashes', files=len(manifest['files']), passed=True)
    sys.path[:0] = [str(HERE), str(SOURCE)]
    import torch
    global TORCH
    TORCH = torch
    torch.set_num_threads(2)
    torch.set_num_interop_threads(2)
    if not torch.cuda.is_available():
        raise RuntimeError('CUDA unavailable; CPU retry prohibited')
    assert '3070' in torch.cuda.get_device_name(0)
    torch.cuda.reset_peak_memory_stats()
    event('runtime', torch=torch.__version__, cuda=torch.version.cuda,
          device=torch.cuda.get_device_name(0), affinity=me.cpu_affinity())
    original_load = torch.load

    def counted_load(path, *args, **kwargs):
        assert Path(path).resolve() == CHECKPOINT.resolve(), 'Unexpected model file'
        COUNTERS['loads'] += 1
        start = time.perf_counter()
        try:
            return original_load(path, *args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            TIMINGS['load_seconds'] += elapsed
            event('load', count=COUNTERS['loads'], seconds=elapsed)

    torch.load = counted_load
    from tabicl import TabICLClassifier
    schema = json.loads((ROOT / 'external/starter-kit/data/unhcr.json').read_text(encoding='utf-8-sig'))
    given = [n for n, r in schema['items'].items() if r['class'] == 'GIVEN']
    original_fit, original_predict = TabICLClassifier.fit, TabICLClassifier.predict_proba

    def counted_fit(self, X, y, *args, **kwargs):
        assert list(X.index) == list(range(45)) and list(X.columns) == given, 'Non-F input reached fit'
        assert len(y) == 45
        COUNTERS['fits'] += 1
        start = time.perf_counter()
        event('fit_start', count=COUNTERS['fits'], rows=len(X), features=len(X.columns))
        try:
            return original_fit(self, X, y, *args, **kwargs)
        finally:
            torch.cuda.synchronize()
            elapsed = time.perf_counter() - start
            TIMINGS['fit_seconds'] += elapsed
            event('fit_end', count=COUNTERS['fits'], seconds=elapsed)

    def counted_predict(self, X, *args, **kwargs):
        assert list(X.columns) == given and list(X.index) == list(range(45, 54))
        COUNTERS['predicts'] += 1
        start = time.perf_counter()
        event('predict_start', count=COUNTERS['predicts'], classes=int(self.n_classes_))
        try:
            return original_predict(self, X, *args, **kwargs)
        finally:
            torch.cuda.synchronize()
            elapsed = time.perf_counter() - start
            TIMINGS['predict_seconds'] += elapsed
            event('predict_end', count=COUNTERS['predicts'], seconds=elapsed)

    TabICLClassifier.fit, TabICLClassifier.predict_proba = counted_fit, counted_predict
    import prototype
    event('adapter_import', checkpoint_loads=COUNTERS['loads'])
    assert COUNTERS['loads'] == 1
    import tests_local
    summary = tests_local.run_tests(prototype, schema, torch, event, ROOT, COUNTERS)
    assert NETWORK == dict(deliberate_blocked=1, package_attempts=0, subprocess_attempts=0), NETWORK
    return summary


if __name__ == '__main__':
    result = dict(outcome='LOCAL_CONTRACT_FAIL', scientific_invocations=1)
    code = 1
    try:
        result['tests'] = main()
        result['outcome'] = 'LOCAL_CONTRACT_PASS'
        code = 0
    except BaseException as exc:
        result['error'] = repr(exc)
        result['traceback'] = traceback.format_exc()
        if 'out of memory' in str(exc).lower():
            result['outcome'] = 'LOCAL_RESOURCE_LIMIT'
        event('failure', error=repr(exc))
    finally:
        result.update(elapsed_seconds=time.perf_counter()-START, counters=COUNTERS,
                      timings=TIMINGS, network=NETWORK, full_path_measured=False)
        if 'TORCH' in globals() and TORCH.cuda.is_initialized():
            result['gpu'] = dict(allocated_peak=TORCH.cuda.max_memory_allocated(),
                                 reserved_peak=TORCH.cuda.max_memory_reserved(),
                                 device_capacity=TORCH.cuda.get_device_properties(0).total_memory)
        (HERE / 'result.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        EVENTS.close()
    sys.exit(code)
