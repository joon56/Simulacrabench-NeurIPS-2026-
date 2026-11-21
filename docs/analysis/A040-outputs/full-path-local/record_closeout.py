"""Metadata-only closeout. No scientific imports, fixture generation or model calls."""
import ast
from datetime import datetime, timezone
import difflib
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
TEMP = ROOT / 'tmp/a040-full-path-local'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path), 'bytes': path.stat().st_size}


entry = read(HERE / 'entry.json')
checks = []
for item in entry['protected'] + entry['reused_input_checks']:
    relative = item['path'].replace('\\', '/')
    if relative.startswith('tmp/'):
        assert relative.startswith('tmp/a040-local-technical/source/') or relative == 'tmp/a040-local-technical/acquisition/tabicl-classifier-v2-20260212.ckpt'
    assert not relative.endswith(('.parquet', '.npz'))
    checks.append(dict(path=relative, expected=item['sha256'], actual=digest(ROOT / relative)))
assert all(c['expected'] == c['actual'] for c in checks)
pins = [{'name': p['name'], 'expected': p['version'], 'actual': importlib.metadata.version(p['name'])} for p in entry['pins']]
assert all(p['expected'] == p['actual'] for p in pins)
adapter_same = (HERE / 'adapter.py').read_bytes() == (ROOT / 'docs/analysis/A040-outputs/local-technical-retry1/prototype.py').read_bytes()
assert adapter_same

schemas = []
for name in ('unicef', 'world_bank', 'unhcr'):
    path = ROOT / 'external/starter-kit/data' / (name + '.json')
    schema = read(path)
    schemas.append(dict(row(path), instrument=name, top_keys=list(schema), gated_value=schema.get('gated_value'),
                        given=sum(i['class'] == 'GIVEN' for i in schema['items'].values()),
                        predict=sum(i['class'] == 'PREDICT' for i in schema['items'].values()),
                        gated_items=sum(bool(i.get('gate')) for i in schema['items'].values())))
roles = read(HERE / 'roles.json')
assert [len(roles[k]) for k in ('fit', 'selection', 'evaluation', 'external')] == [6279, 1000, 1000, 621]
assert sorted(roles['fit'] + roles['selection'] + roles['evaluation']) == list(range(8279))
assert set(roles['external']) == set(range(8279, 8900))
assert not list(TEMP.rglob('*.json'))
assert not list(HERE.rglob('scientific-started.json'))
assert not (HERE / 'frozen-inputs/manifest.json').exists()

source_diff = ['# Post-failure source evidence; not a scientific freeze.\n',
               '# adapter.py byte-identical to retry1/prototype.py; no model change.\n']
parsed = []
for path in sorted(HERE.glob('*.py')):
    source = path.read_text(encoding='utf-8-sig')
    ast.parse(source, filename=str(path))
    parsed.append(path.name)
    if path.name != 'adapter.py':
        source_diff.extend(difflib.unified_diff([], source.splitlines(keepends=True), fromfile='/dev/null', tofile=path.name))
(HERE / 'source.diff').write_text(''.join(source_diff), encoding='utf-8')
now = datetime.now(timezone.utc)
head = subprocess.check_output(['git', '-c', 'safe.directory=' + ROOT.as_posix(), 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
assert head == entry['head']
dirty = subprocess.check_output(['git', '-c', 'safe.directory=' + ROOT.as_posix(), 'status', '--short'], cwd=ROOT, text=True)
(HERE / 'dirty-at-closeout.txt').write_text(dirty, encoding='utf-8')
save(HERE / 'active-jobs-at-closeout.json', dict(evidence='5121eb elevated read-only CIM query', named_python_jupyter_jobs=[],
      sandbox_query_denied=True, successful_query_exit=0, scientific_children_started=0))
old = read(ROOT / 'docs/analysis/A040-outputs/local-technical/result.json')
old_res = read(ROOT / 'docs/analysis/A040-outputs/local-technical/run-resources.json')
retry = read(ROOT / 'docs/analysis/A040-outputs/local-technical-retry1/resources.json')['current']
resources = dict(decision='LOCAL_FULL_PATH_FAIL', recorded_utc=now.isoformat(),
    task_start_utc=entry['start_utc'], task_deadline_utc=entry['deadline_utc'],
    task_wall_seconds_at_record=(now-datetime.fromisoformat(entry['start_utc'].replace('Z','+00:00'))).total_seconds(),
    current=dict(scientific_processes=0, child_seconds=0, parent_scientific_seconds=0, fits=0, predicts=0, loads=0, scores=0,
                 model_free_seconds=read(HERE / 'model-free-result.json')['elapsed_seconds'],
                 generator_invocations=1, generator_exit=1, generator_tool_wall_seconds=.7898181,
                 generator_internal_elapsed=None, rss_peak=None, commitment_peak=None, cuda_allocated_peak=None,
                 cuda_reserved_peak=None, resource_watchdog_started=False, full_path_measured=False),
    preflight=dict(device='NVIDIA GeForce RTX 3070', total_MiB=8192, used_MiB=637, utilization_percent=2,
                   evidence='0d1818 nvidia-smi', device_snapshot_not_task_peak=True, host_available_not_measured=True),
    original=dict(outcome=old['outcome'], child_seconds=old['elapsed_seconds'], parent_seconds=old_res['elapsed_seconds'],
                  counters=old['counters'], rss_peak_sampled=old_res['rss_peak_sampled'],
                  commitment_peak_sampled=old_res['commitment_peak_sampled'], gpu=old_res['gpu']),
    retry1=dict(outcome='LOCAL_CONTRACT_PASS', child_seconds=retry['child_elapsed_seconds'], parent_seconds=retry['parent_elapsed_seconds'],
                counters=retry['counts'], rss_peak_sampled=retry['watchdog']['rss_peak_sampled'],
                commitment_peak_sampled=retry['watchdog']['commitment_peak_sampled'], gpu=retry['watchdog']['gpu']),
    cumulative=dict(scientific_processes=2, child_seconds=old['elapsed_seconds']+retry['child_elapsed_seconds'],
                    parent_seconds=old_res['elapsed_seconds']+retry['parent_elapsed_seconds'], fits=230, predicts=232, loads=4,
                    memory_peaks_added=False, full_path_estimate=False))
save(HERE / 'resources.json', resources)
for mode in ('reference','candidate'):
    save(HERE / mode / 'result.json', dict(record_kind='closeout_not_runner_output', outcome='NOT_RUN', scientific_invocations=0,
         reason='First input generation failed before scientific freeze; reference gate never opened'))
    save(HERE / mode / 'resources.json', dict(record_kind='closeout_not_watchdog_output', outcome='NOT_RUN', started=False,
         elapsed_seconds=0, rss_peak=None, commitment_peak=None, cuda_peak=None, model_calls=0))
save(HERE / 'frozen-inputs/state.json', dict(state='NOT_REACHED', scientific_manifest_created=False,
     reason='Input generation failed; source-manifest.json is post-failure evidence only', registered_before_generation=True))
save(HERE / 'result.json', dict(outcome='LOCAL_FULL_PATH_FAIL', stage='input_generation_unicef_layout', error="KeyError: 'gated_value'",
     scientific_invocations=0, reference='NOT_RUN', candidate='NOT_RUN', model_free='PASS_MODEL_FREE_ONLY',
     fixture_generation_invocations=1, generated_inputs=0, generated_outputs=0, roles_created=True,
     post_failure_scientific_source_edits=False, retry=False, s2_candidate=False, next_owner='S0', evidence='generation-failure.txt'))
save(HERE / 'dependency-identity.json', dict(pins=pins, package_imports_for_check=0, method='importlib.metadata versions only'))
save(HERE / 'source-manifest.json', dict(kind='POST_FAILURE_EVIDENCE_NOT_SCIENTIFIC_FREEZE', recorded_utc=now.isoformat(),
     head=head, files=[row(p) for p in sorted(HERE.glob('*.py'))] + [row(HERE / n) for n in
       ('registration.md','plan.md','requirements.lock.txt','entry.json','roles.json','model-free-result.json')]
       + [row(ROOT / 'submissions/2026-09-19-E041/main.py')] + [row(ROOT / s['path']) for s in schemas],
     schemas=schemas, reused_source_and_checkpoint=[c for c in checks if c['path'].startswith('tmp/')],
     role_counts={k:len(roles[k]) for k in ('fit','selection','evaluation','external')},
     role_sha256=digest(HERE / 'roles.json'), fake_input_files=[], fake_data_hashes=None,
     source_diff_sha256=digest(HERE / 'source.diff'), adapter_byte_identity=adapter_same))
save(HERE / 'verification.json', dict(outcome='LOCAL_FULL_PATH_FAIL', metadata_record_checks='PASS', head=head,
     workflow_revision=entry['workflow_revision'], workflow_sha256=entry['workflow_sha256'],
     read_evidence=entry['read_evidence']+['eca2fd source/contract/policy', '073bd7 required records and setup',
      'fff6ce actual raw schema key diagnosis; no invocation', '5121eb closeout process check'],
     protected_and_reused_checks=checks, protected_count=len(entry['protected']), reused_count=len(entry['reused_input_checks']),
     pins_matched=len(pins), adapter_unchanged=True, parsed_new_python_files=parsed,
     static_parse_not_execution_validation=True, original_failure_and_retry_preserved=True,
     full_fake_input_files=0, scientific_latches=0, model_imports=0, fits=0, predicts=0, scores=0, checkpoint_deserializations=0,
     model_free_pass_not_schema_or_full_path_pass=True, scientific_freeze_reached=False,
     source_or_model_repair_after_failure=False, full_runtime_memory_parity_unverified=True,
     new_role_positions_only=True, real_data_or_old_fixtures_read=False,
     releases_commits_pushes_agents_installs_downloads=0, s0_review_required=True,
     residual_obligations=['public runtime schema entry contract','actual E041 all3','full-context shadow and final expert',
         'S/E freeze and guard with actual models','exact control/inactive/empty parity','forced-active full output',
         'whole runtime/RSS/private commitment/CUDA peaks','H100/hosted900s','native network protection','release gates','efficacy']))
print(json.dumps(dict(outcome='LOCAL_FULL_PATH_FAIL', protected=len(entry['protected']), reused=len(entry['reused_input_checks']),
                     pins=len(pins), scientific_runs=0, task_wall_seconds=resources['task_wall_seconds_at_record'])))
