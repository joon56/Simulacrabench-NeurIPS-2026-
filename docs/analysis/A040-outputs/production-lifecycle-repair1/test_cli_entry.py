"""Actual __main__ import/parser rejection; positive child path covered by integration."""
import json
from pathlib import Path
import runpy
import sys
import time
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import local_guard
local_guard.install()
local_guard.block_sdk_auth()
WORK=HERE.parents[3]/'tmp/a040-production-lifecycle-repair1'
records=[]
for scope in ('LOCAL_PROTOCOL_FIXTURE','LIVE'):
    now=time.time()
    config={'plan':dict(scope=scope,app_name='a040-entry-negative',base_id='im-fixture',
        base_result_sha256='0'*64,prepare_deadline=now+2000,gpu_latest_end=now+4000,
        whole_deadline=now+5000,execution_authorized=False)}
    path=WORK/('cli-entry-'+scope+'.json')
    with path.open('x') as stream: json.dump(config,stream)
    sys.argv=[str(HERE/'live_launcher.py'),str(path),'--child']
    try: runpy.run_path(str(HERE/'live_launcher.py'),run_name='__main__')
    except PermissionError as error: records.append({'scope':scope,'rejected':str(error)})
    else: raise AssertionError('CLI allowed unauthorised/default fixture scope')
assert not local_guard.blocked,local_guard.blocked
print(json.dumps({'outcome':'ACTUAL_SCRIPT_ENTRY_GATE_PASS','cases':records,
    'positive_child_path':'tests_lifecycle.py calls same main/parser/child/dispatch with input factory',
    'live_payload_gate_and_parent_watchdog':'not executed in this local task'}))
