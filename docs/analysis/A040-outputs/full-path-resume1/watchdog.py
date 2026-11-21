"""Sequential per-mode900s watchdog; one exclusive latch per scientific mode."""
import argparse
import ctypes
from datetime import datetime,timezone
import json
from pathlib import Path
import subprocess
import sys
import time

import psutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CAP=16_000_000_000
DEADLINE=datetime(2026,10,2,10,5,10,tzinfo=timezone.utc)
PARSER=argparse.ArgumentParser();PARSER.add_argument('mode',choices=['reference','candidate'])
MODE=PARSER.parse_args().mode
OUT=HERE/MODE


class MemoryStatus(ctypes.Structure):
    _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong)]+[(n,ctypes.c_ulonglong) for n in
        ('total_phys','avail_phys','total_page','avail_page','total_virtual','avail_virtual','extended')]


def save(value):
    (OUT/'resources.json').write_text(json.dumps(value,indent=2),encoding='utf-8')


def main():
    if (OUT/'scientific-started.json').exists():raise PermissionError('Scientific mode already invoked')
    regression=json.loads((HERE/'model-free-result.json').read_text())
    if regression['outcome']!='PASS_MODEL_FREE_ONLY':raise PermissionError('Model-free checks failed')
    prior_seconds=0
    if MODE=='candidate':
        ref=json.loads((HERE/'reference/resources.json').read_text())
        if ref['outcome']!='REFERENCE_PASS' or ref['child_exit']!=0:raise PermissionError('Reference gate failed')
        prior_seconds=ref['elapsed_seconds']
    mem=MemoryStatus();mem.length=ctypes.sizeof(mem)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem)):
        save(dict(outcome='BLOCKED_RESOURCE',started=False,reason='Host memory measurement unavailable'));return 2
    available=dict(physical=mem.avail_phys,commitment=mem.avail_page)
    if min(available.values())<CAP:
        save(dict(outcome='BLOCKED_RESOURCE',started=False,available=available));return 2
    minimum=1900 if MODE=='reference' else 950
    if (DEADLINE-datetime.now(timezone.utc)).total_seconds()<minimum:
        save(dict(outcome='INCOMPLETE',started=False,reason='Not enough original task time'));return 2
    cap=min(900,1800-prior_seconds)
    controller=psutil.Process();affinity=controller.cpu_affinity()[:2];controller.cpu_affinity(affinity)
    with (OUT/'scientific-started.json').open('x',encoding='utf-8') as stream:
        json.dump(dict(mode=MODE,start_utc=datetime.now(timezone.utc).isoformat(),invocations=1,
                       seconds_cap=cap,host_cap=CAP,affinity=affinity),stream)
    start=time.perf_counter();reason=None;samples=[]
    with (OUT/'stdout.txt').open('xb') as stdout,(OUT/'stderr.txt').open('xb') as stderr:
        child=subprocess.Popen([sys.executable,'-I','-B','-u',str(HERE/'runner.py'),MODE],
                               cwd=ROOT,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            while child.poll() is None:
                elapsed=time.perf_counter()-start;rss=commitment=0
                processes=[controller]+controller.children(recursive=True)
                for process in processes:
                    try:
                        process.cpu_affinity(affinity);info=process.memory_info();rss+=info.rss;commitment+=info.private
                    except psutil.NoSuchProcess:continue
                sample=dict(elapsed=elapsed,rss=rss,commitment=commitment,pids=[p.pid for p in processes])
                samples.append(sample)
                with (OUT/'resource-samples.jsonl').open('a',encoding='utf-8') as stream:stream.write(json.dumps(sample)+'\n')
                if elapsed>=cap:reason='Scientific process time cap';break
                if max(rss,commitment)>CAP:reason='Host resource cap';break
                time.sleep(min(1,max(.001,cap-(time.perf_counter()-start))))
        except BaseException as exc:reason='Controller/measurement error: '+repr(exc)
        finally:
            if reason:
                for process in reversed(controller.children(recursive=True)):
                    try:process.kill()
                    except psutil.NoSuchProcess:pass
            child.wait(timeout=10)
    elapsed=time.perf_counter()-start
    result=json.loads((OUT/'result.json').read_text()) if (OUT/'result.json').exists() else {}
    outcome=result.get('outcome','INCOMPLETE')
    if reason:outcome='LOCAL_RESOURCE_LIMIT' if 'cap' in reason else 'INCOMPLETE'
    events=[]
    if (OUT/'events.jsonl').exists():
        for line in (OUT/'events.jsonl').read_text().splitlines():
            try:events.append(json.loads(line))
            except json.JSONDecodeError:pass
    gpu=result.get('gpu')
    if gpu is None:
        known=[e for e in events if 'gpu_allocated_peak' in e]
        gpu={'allocated_peak_lower_bound':max((e['gpu_allocated_peak'] for e in known),default=None),
             'reserved_peak_lower_bound':max((e['gpu_reserved_peak'] for e in known),default=None),
             'complete_peak_measured':False}
    record=dict(mode=MODE,outcome=outcome,reason=reason,child_exit=child.returncode,
                elapsed_seconds=elapsed,prior_process_seconds=prior_seconds,cumulative_parent_seconds=prior_seconds+elapsed,
                samples=len(samples),sampling_seconds=1,rss_peak_sampled=max((s['rss'] for s in samples),default=0),
                commitment_peak_sampled=max((s['commitment'] for s in samples),default=0),includes_controller=True,
                available_before=available,host_cap=CAP,gpu=gpu,last_event=events[-1] if events else None,
                remaining_children=[p.pid for p in controller.children(recursive=True)])
    save(record)
    print(json.dumps(dict(mode=MODE,outcome=outcome,seconds=elapsed,reason=reason)))
    return 0 if outcome in ('REFERENCE_PASS','LOCAL_FULL_PATH_PASS') else 1


if __name__=='__main__':sys.exit(main())
