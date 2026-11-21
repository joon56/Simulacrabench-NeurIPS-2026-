"""One monitored Modal image build. No model imports, data transfer, or science."""
import asyncio
import dataclasses
from datetime import datetime, timezone
import importlib
import json
from pathlib import Path
import time
import traceback
import modal
from modal_proto import api_pb2

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
DEADLINE = datetime.fromisoformat('2026-10-02T16:04:10+00:00').timestamp()
REQUIREMENTS = (ROOT/'docs/analysis/A040-outputs/full-path-resume1/requirements.lock.txt').read_text()

def record(name, value):
    with (HERE/name).open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(dict(utc=datetime.now(timezone.utc).isoformat(), **value), default=str)+'\n')

def install_pins(requirements, absolute_deadline):
    import json
    from pathlib import Path
    import subprocess
    import sys
    import time
    if sys.version_info[:3] != (3, 13, 14):
        raise RuntimeError('Pinned Python unavailable')
    pins = Path('/a040-requirements.txt')
    pins.write_text(requirements)
    seconds = min(600, int(absolute_deadline-time.time())-30)
    if seconds <= 0:
        raise TimeoutError('Preparation deadline before installer')
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-cache-dir',
                    '--only-binary=:all:', '--extra-index-url',
                    'https://download.pytorch.org/whl/cu126', '-r', str(pins),
                    '--report', '/a040-install-report.json'], check=True, timeout=seconds)
    inventory = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze', '--all'], text=True)
    Path('/a040-linux-requirements.lock.txt').write_text(inventory)
    print('A040_LINUX_PINS='+json.dumps(inventory), flush=True)

async def main():
    with (HERE/'build-intent.json').open('x', encoding='utf-8') as stream:
        json.dump({'created_utc': datetime.now(timezone.utc).isoformat(), 'client_build_invocations': 1}, stream)
    workspace = modal.Workspace.from_context()
    await workspace.hydrate.aio()
    if workspace.name != 'joon56':
        raise RuntimeError('Workspace mismatch')
    baseline = await workspace.billing.summary.aio()
    (HERE/'billing-baseline.json').write_text(json.dumps(dataclasses.asdict(baseline), default=str, indent=2))
    if float(baseline.billed_cost) != 0:
        raise RuntimeError('Cash billing contradiction')
    app = await modal.App.lookup.aio('a040-modal-resume2-20261003', create_if_missing=True, environment_name='main')
    (HERE/'remote-app.json').write_text(json.dumps({'app_id':app.app_id, 'workspace':'joon56', 'environment':'main'}))
    record('remote-ids.jsonl', {'kind':'app','id':app.app_id})
    module = importlib.import_module('modal._image')
    original_join = module._image_await_build_result
    async def observed_join(image_id, client):
        record('remote-ids.jsonl', {'kind':'image','id':image_id})
        return await original_join(image_id, client)
    module._image_await_build_result = observed_join
    image = modal.Image.from_registry('python:3.13.14-slim').run_function(
        install_pins, args=(REQUIREMENTS, DEADLINE), cpu=(1,1), memory=(8192,8192),
        timeout=600, include_source=False)
    started = time.monotonic()
    task = None
    try:
        with modal.enable_output():
            task = asyncio.create_task(image.build.aio(app))
            last_bill = 0.0
            delta = 0.0
            while not task.done():
                elapsed = time.monotonic()-started
                if elapsed-last_bill >= 45 or last_bill == 0:
                    try:
                        summary = await asyncio.wait_for(workspace.billing.summary.aio(), 10)
                        delta = max(0, float(summary.metered_cost)-float(baseline.metered_cost))
                        record('billing-samples.jsonl', {'account':dataclasses.asdict(summary), 'unattributed_account_delta':delta})
                    except Exception as exc:
                        record('billing-samples.jsonl', {'read_error_type':type(exc).__name__})
                    last_bill = max(elapsed, 0.001)
                estimate = .65 + elapsed*(.0000131+8*.00000222)
                record('cost-samples.jsonl', {'stage':'build','elapsed':elapsed,'estimate':estimate,
                                           'management_value':max(estimate,delta),'overhead_unmeasured':True})
                if max(estimate, delta) >= 4 or time.time() >= DEADLINE-45:
                    raise TimeoutError('Preparation time/cost stop')
                await asyncio.wait({task}, timeout=10)
            await task
        result = dict(outcome='IMAGE_BUILT', image_id=image.object_id, app_id=app.app_id,
                      elapsed_seconds=time.monotonic()-started, recipe='single fixed registry plus installer',
                      scientific_imports=0)
        (HERE/'build-result.json').write_text(json.dumps(result,indent=2))
        record('remote-ids.jsonl', {'kind':'image_final','id':image.object_id})
        print(json.dumps(result), flush=True)
    except BaseException as exc:
        if task is not None:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
        result=dict(outcome='BUILD_FAILED',error=repr(exc),traceback=traceback.format_exc(),
                    app_id=app.app_id,elapsed_seconds=time.monotonic()-started)
        (HERE/'build-result.json').write_text(json.dumps(result,indent=2))
        raise
    finally:
        # Stop only the explicitly created task App, even when the client build fails.
        try:
            client = await modal.Client.from_env.aio()
            await client._stub.AppStop(api_pb2.AppStopRequest(app_id=app.app_id,source=api_pb2.APP_STOP_SOURCE_CLI))
            record('termination-events.jsonl',{'kind':'app_stop_ack','id':app.app_id,
                                             'terminal_state_still_requires_query':True})
        except Exception as exc:
            record('termination-events.jsonl',{'kind':'app_stop_error','id':app.app_id,'error_type':type(exc).__name__})

if __name__ == '__main__':
    asyncio.run(main())
