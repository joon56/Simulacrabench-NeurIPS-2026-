"""This invocation's config/source gate only. No SDK/model/payload import."""
import hashlib
import json
from pathlib import Path
import sys
import time

START = time.monotonic()
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE = ROOT / 'docs/analysis/A040-outputs/local-preparation-repair2'
sys.path.insert(0, str(SOURCE))
from live_launcher import load_contract

freeze = json.loads((HERE / 'config-source-input-freeze.json').read_text(encoding='utf-8'))
assert hashlib.sha256((HERE / 'live-config.json').read_bytes()).hexdigest() == freeze['config_sha256']
assert hashlib.sha256((HERE / 'user-authority.ko.md').read_bytes()).hexdigest() == freeze['authority_sha256']
config, plan, manifest = load_contract(HERE / 'live-config.json')
assert Path(config['output_directory']) == HERE / 'run'
assert Path(config['launcher_directory']) == ROOT / 'tmp/a040-modal-full-path1-resume5/launcher'
assert not Path(config['output_directory']).exists()
assert not Path(config['launcher_directory']).exists()
assert Path(config['authority_record']) == HERE / 'user-authority.ko.md'
assert plan.app_name == 'a040-resume5-20261005-094405'
assert plan.gpu_latest_end - plan.prepare_deadline == 2400
assert plan.whole_deadline - plan.gpu_latest_end == 1200
assert plan.execution_authorized and plan.scope == 'LIVE'
assert len(manifest['files']) == len(config['extra_files']) == 12
assert hashlib.sha256(Path(config['pins_path']).read_bytes()).hexdigest() == freeze['pins_sha256']
assert len([line for line in Path(config['pins_path']).read_text().splitlines() if line.strip()]) == 34
assert hashlib.sha256(Path(config['allowlist_path']).read_bytes()).hexdigest() == freeze['allowlist_sha256']
result = {'outcome': 'CONFIG_SOURCE_PASS', 'elapsed_seconds': time.monotonic()-START,
          'source12': True, 'pins34': True, 'authority_link': True, 'new_paths_deadlines': True,
          'payload_content_reads': 0, 'model_sdk_imports': 0, 'rpc': 0}
(HERE / 'static-config-verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result))
