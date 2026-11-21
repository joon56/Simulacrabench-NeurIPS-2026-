"""Real launcher parent/child; new invalid protocol pins stop before any client."""
from dataclasses import asdict
import json
import os
from pathlib import Path
import subprocess
import sys
import time
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
WORK=HERE.parents[3]/'tmp/a040-production-lifecycle-repair1'
directory=WORK/('cli-parent-'+sys.argv[1])
directory.mkdir(exist_ok=False)
config_path=directory/'contract.json'
command=[sys.executable,'-X','utf8','-B',str(HERE/'live_launcher.py'),str(config_path),'--child']
import local_guard
local_guard.install(allowed_child=command)
local_guard.block_sdk_auth()
from contract import Plan,sha
import live_launcher
manifest=json.loads((HERE/'source-manifest.json').read_text())
now=time.time()
# This is fixture metadata, not authority for any actual remote operation.
plan=Plan('LIVE','a040-local-cli-negative','im-protocol',sha(b'protocol'),now+2000,now+4000,now+5000,execution_authorized=True)
allow=directory/'protocol-empty-allowlist.json'; allow.write_text('{"files":[]}')
pins=directory/'protocol-invalid-pins.txt'; pins.write_text('LOCAL PROTOCOL; NOT THE FIXED PINS')
config={'plan':asdict(plan),'source_manifest_sha256':sha((HERE/'source-manifest.json').read_bytes()),
    'extra_files':[dict(r,path='docs/analysis/A040-outputs/production-lifecycle-repair1/'+r['path'],reason='protocol metadata') for r in manifest['files']],
    'launcher_directory':str(directory/'launcher'), 'allowlist_path':str(allow),'allowlist_sha256':sha(allow.read_bytes()),
    'pins_path':str(pins)}
config_path.write_text(json.dumps(config))
site=directory/'site'; site.mkdir()
site.joinpath('sitecustomize.py').write_text(
    'import sys\nfrom pathlib import Path\nsys.dont_write_bytecode=True\n'
    + 'sys.path.insert(0,'+repr(str(HERE))+')\n'
    + 'import local_guard\nlocal_guard.install()\nlocal_guard.block_sdk_auth()\n'
    + 'Path('+repr(str(directory/'child-guard.json'))+').write_text(\'{"auth_transport_blocked":true}\')\n')
os.environ['PYTHONPATH']=str(site)
code=live_launcher.main([str(config_path)])
assert code!=0
assert json.loads((directory/'child-guard.json').read_text())['auth_transport_blocked']
error=(directory/'launcher/stderr.txt').read_text()
assert 'Fixed pins mismatch' in error,error
assert not (directory/'launcher/forced-stop.json').exists()
assert json.loads((directory/'launcher/exit.json').read_text())['exit_code']==code
assert not local_guard.blocked,local_guard.blocked
try: subprocess.Popen([sys.executable,'-c','pass'])
except PermissionError: pass
else: raise AssertionError('Unlisted child allowed')
assert local_guard.blocked==['subprocess.Popen']
print(json.dumps({'outcome':'REAL_PARENT_CHILD_CLI_GATE_PASS','exact_owned_child':1,
    'fresh_child_import_guard':True,'entry':'main parent -> actual live_launcher.py --child',
    'stop':'fixed pins gate on new protocol text; old pins/payload not accessed',
    'real_auth_rpc_model':0,'unlisted_child_rejected':True}))
