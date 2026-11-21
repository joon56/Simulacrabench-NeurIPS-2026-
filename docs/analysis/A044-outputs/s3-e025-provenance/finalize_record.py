"""Document/preservation closeout only. Never imports scientific packages or fits."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
TEMP = ROOT / 'tmp/a044-e025-phase2'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(name, value):
    with (OUT / name).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)


def relative(path):
    return str(path.relative_to(ROOT)).replace('\\', '/')


def git(*args):
    return subprocess.check_output(['git', '-c', 'safe.directory=' + ROOT.as_posix(), *args],
                                   cwd=ROOT, text=True, encoding='utf-8')


assert not (OUT / 'verification.json').exists(), 'do not overwrite a closeout'
head = git('rev-parse', 'HEAD').strip()
assert head == 'a43f4379ec78dbc2de260463eef67bb1d567d7e1'
entry = read(OUT / 'entry.json')
assert sha(ROOT / 'docs/workflow.md') == entry['workflow_sha256']
freeze = read(OUT / 'pre-run-freeze.json')
for path, expected in freeze['sha256'].items():
    assert sha(OUT / path) == expected, ('pre-run artifact changed', path)

preserved = []
for key in ('input', 'source', 'kit'):
    for row in read(OUT / 'identity-gate.json')[key]:
        current = sha(ROOT / row['path'])
        assert current == row['actual'] and row['match'], row['path']
        preserved.append({'path': row['path'], 'sha256': current, 'match': True})
for path, expected in read(OUT / 'static-freeze.json')['sha256'].items():
    assert sha(ROOT / path) == expected, path
    preserved.append({'path': path, 'sha256': expected, 'match': True})
for freeze_name, raw_pattern in [('source-all3-freeze.json', 'E025-{}-source.json'),
                                 ('official-all3-freeze.json', 'E025-{}-official-predictions.json')]:
    for name, row in read(OUT / freeze_name)['instruments'].items():
        assert sha(OUT / raw_pattern.format(name)) == row['raw_sha256']

resources = [read(path) for path in sorted(OUT.glob('resource-*.json'))]
assert {row['action'] for row in resources} == {'checks', 'gate', 'source', 'official', 'evaluate'}
assert len(resources) == 5
for row in resources:
    assert row['passed'] and row['exit_code'] == 0 and row['failure'] is None
    assert row['final_sample_enforced'] and not row['remnant_pids']
    assert row['elapsed_seconds'] < row['shared_seconds']
    assert max(row['peak_sampled_tree_rss'], row['peak_sampled_tree_private']) < 8 * 1024**3
    assert row['sample_count'] == len(row['samples'])
    assert max(sample['rss'] for sample in row['samples']) == row['peak_sampled_tree_rss']
    assert max(sample['private'] for sample in row['samples']) == row['peak_sampled_tree_private']
    for sample in row['samples']:
        assert sample['rss'] == sum(proc['rss'] for proc in sample['processes'])
        assert sample['private'] == sum(proc['private'] for proc in sample['processes'])
comparison = read(OUT / 'comparison.json')
assert comparison['all_raw_exact'] and comparison['all_absolute_gate']
assert comparison['ordered_vectors'] == 442425
for row in comparison['instruments'].values():
    assert row['source_archive_raw_exact'] and abs(row['e025_minus_e041']) <= .002
assert read(OUT / 'static-freeze.json')['checker']['decision'] == 'REUSE_NO_RERUN'

measured = sum(row['elapsed_seconds'] for row in resources)
charged = measured + 120
assert charged < 2700
checks = .3690211 + sum(row['elapsed_seconds'] for row in resources if row['action'] == 'checks')
assert checks < 120
all3 = [read(path) for path in OUT.glob('latch-*.json')
        if read(path)['action'] in ('source', 'official')]
assert len(all3) == 2 and {row['action'] for row in all3} == {'source', 'official'}

# Read-only local process census; no stop, remote query or new computation worker.
command = "$rows=@(Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(python|pythonw|uv)\\.exe$' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine); ConvertTo-Json -InputObject $rows -Depth 3"
raw = subprocess.check_output(['powershell', '-NoProfile', '-Command', command], text=True,
                              encoding='utf-8', errors='strict')
processes = json.loads(raw) if raw.strip() else []
# This closeout is itself a stdlib-only Python command, plus its venv launcher.
assert all('finalize_record.py' in (row.get('CommandLine') or '') for row in processes), processes
save('process-closeout.json', {'observed_at': datetime.datetime.now().astimezone().isoformat(),
     'processes': processes, 'only_current_document_closeout_command': True,
     'model_observer_workers_running': [], 'remote_all_chat_census': False})

before_dirty = set((OUT / 'dirty-entry.txt').read_text(encoding='utf-8-sig').splitlines())
dirty = git('status', '--porcelain=v1', '--untracked-files=all')
current_dirty = set(dirty.splitlines())
assert not (before_dirty - current_dirty), 'existing dirty pathname record removed'
added = sorted(current_dirty - before_dirty)
assert all(line[3:].startswith('docs/analysis/A044-outputs/s3-e025-provenance/')
           or line[3:].startswith('tmp/a044-e025-phase2/') for line in added), added
(OUT / 'dirty-closeout.txt').write_text(dirty, encoding='utf-8')

# Reconstruct the exact pre-task shared document bytes before adding notices.
shared = read(OUT / 'shared-entry-identities.json')
status_path = ROOT / 'docs/status.md'
status = status_path.read_bytes()
anchor = b'## Current position\r\n\r\n'
start = status.index(anchor) + len(anchor)
endmark = '### Earlier notices — historical; active ownership above governs\n\n'.encode()
end = status.index(endmark, start) + len(endmark)
assert b'S3-E025-PROVENANCE-A044 /root' in status[start:end]
original_status = status[:start] + status[end:]
assert hashlib.sha256(original_status).hexdigest() == shared['status_original_sha256']
log_path, phase_path = ROOT / 'docs/log.md', ROOT / 'docs/phase2-preparation.md'
original_log, original_phase = log_path.read_bytes(), phase_path.read_bytes()
assert hashlib.sha256(original_log).hexdigest() == shared['log_original_sha256']
assert hashlib.sha256(original_phase).hexdigest() == shared['phase2_original_sha256']

release = datetime.datetime.now().astimezone()
gross = (release - datetime.datetime.fromisoformat(entry['gross_start_conservative'])).total_seconds()
assert gross < 120 * 60
budget = {'measured_supervised_seconds': measured, 'administrative_charge_seconds': 120,
          'charged_seconds': charged, 'limit_seconds': 2700, 'remaining_seconds': 2700 - charged,
          'gross_seconds_conservative': gross, 'gross_limit_seconds': 7200,
          'all3_normal_starts': 2, 'invalid_arm_repair_starts': 0, 'all3_total_limit': 3,
          'check_cycles': 1, 'red_green_check_seconds': checks, 'check_limit_seconds': 120,
          'ordinary_scientific_repairs': 0, 'e041_model_calls': 0, 'checker_runs': 0,
          'no_unused_budget_continuation': True,
          'resources': [{key: value for key, value in row.items() if key != 'samples'} for row in resources]}
save('budget-ledger.json', budget)

notice = '''- **2026-10-23 S3-E025-PROVENANCE-A044 complete: LOCAL_E025_PHASE2_PROVENANCE_COMPLETE_FOR_S0.**
  Unchanged E025 modular source versus preserved archive:442425 raw vectors exact,
  official3 PASS; E025-E041 skill deltas0/0/+0.000508449, absolute.002 gate all3 PASS.
  E041 frozen raw reuse qualified before models; historical environment omissions remain.
  All3 source429.930s/official450.277s, each shared900s; charged1030.964/2700s,
  CPU2/GPU0/tree RSS/private below8GiB; normal starts2, repair0, checker reuse only.
- **Writer: none; S3 released to S0 review.** No owned model/observer jobs remain.
  [Handoff](analysis/A044-outputs/s3-e025-provenance/s0-handoff.ko.md),
  [closeout](analysis/A044-outputs/s3-e025-provenance/closeout.md),
  [verification/release](analysis/A044-outputs/s3-e025-provenance/verification.json).
  E041 provisional TEST/E025 fallback/E064 parked; final user TEST choice remains open.
  Method/license/Terms/timestamps remain separate. No new ZIP/upload/commit/push.
  All STOP/HOLD/protected exposure roles unchanged; no unused-budget continuation.

### Earlier notices — historical; S3 closeout above governs

'''.encode()
new_status = original_status[:start] + notice + original_status[start:]
log_notice = '''## 2026-10-23 - S3 E025 phase2 provenance completed and returned to S0

- User explicitly approved S3-E025-PROVENANCE-A044 and its new finite budget.
  S0 release checked; sole writer accepted; workflow r6/read receipt recorded.
- Exact9 input and13 traced source identities frozen; no blanket src hashing.
  E041 old raw reuse gate passed before models, with post-run/environment limits retained.
- Unchanged modular E025 source all3 once; preserved ZIP stock official all3 once.
  Source raw frozen before dedicated truth evaluation; original official truth order retained.
  All442425 ordered vectors raw-exact; official3 PASS. E025-E041 deltas0/0/+0.000508449
  satisfy absolute.002 per instrument. No new subgroup/head diagnosis or tuning.
- Whole all3 walls429.9301762/450.2767931s<900 each. Sampled tree maxima RSS2035314688,
  private2067001344bytes<8GiB; final sample checked, maximum sample gap<=.221341s.
  CPU2/GPU0; measured910.9642052+administrative charge120=1030.9642052/2700s.
  One new red/green check cycle; normal all3 starts2, repair0, old checker PASS reused.
- E025 ZIP11240bytes unchanged, SHA256142921c3ea843c653821cf06a8b3fab89e8e6c96592581590f7e970064d90c6f.
  Existing model/snapshot/method/PDF/manifest/ZIP files not edited. No E041 fit/new ZIP/
  network/install/remote/subagent/final choice/upload/commit/push. Prior dirty work preserved.
- Remaining: historical E025 drift cause, A012 environment omissions/post-run provenance,
  hosted/TEST uncertainty and separate method/license/Terms/timestamp/user-choice work.
  E041 provisional/E025 fallback/E064 parked; all STOP/HOLD/A_half/A018 and exposure roles intact.
  Writer released, no owned model/observer workers; S0 reviews, unused budget is not authority.
  [S0 handoff](analysis/A044-outputs/s3-e025-provenance/s0-handoff.ko.md),
  [verification](analysis/A044-outputs/s3-e025-provenance/verification.json).

'''.encode()
log_offset = original_log.index(b'\n\n') + 2 if b'\n\n' in original_log[:50] else original_log.index(b'\r\n\r\n') + 4
new_log = original_log[:log_offset] + log_notice + original_log[log_offset:]
phase_notice = '''## Current status — 2026-10-23, S3-E025-PROVENANCE-A044

E025 local phase2 provenance complete for S0: unchanged modular source/preserved
archive442425 vectors raw-exact, official3 PASS, absolute E041 difference.002 gate
all3 PASS. Source429.930s and official450.277s each below shared900s; observed tree
memory below8GiB. [Closeout](analysis/A044-outputs/s3-e025-provenance/closeout.md),
[release](analysis/A044-outputs/s3-e025-provenance/verification.json).

E041 remains provisional, E025 fallback; final TEST choice is not user-confirmed.
No new ZIP/upload/commit/push. A012 historical environment omissions, private hosted
equivalence and TEST efficacy remain unverified. Method/license/current Terms/exact
Final timestamps remain separate work. Writer released to S0 review; no automatic
continuation. The S3-PREP notice below is historical; its E025 provenance gap is
superseded only within the exact local scope above.

### Earlier S3 preparation notice — historical

'''.encode()
phase_offset = original_phase.index(b'\r\n\r\n') + 4 if b'\r\n\r\n' in original_phase[:120] else original_phase.index(b'\n\n') + 2
new_phase = original_phase[:phase_offset] + phase_notice + original_phase[phase_offset:]
status_path.write_bytes(new_status)
log_path.write_bytes(new_log)
phase_path.write_bytes(new_phase)
assert status_path.read_bytes().replace(notice, b'', 1) == original_status
assert log_path.read_bytes().replace(log_notice, b'', 1) == original_log
assert phase_path.read_bytes().replace(phase_notice, b'', 1) == original_phase

artifact_hashes = {relative(path): sha(path) for path in sorted(OUT.rglob('*')) if path.is_file()}
temporary_hashes = {relative(path): sha(path) for path in sorted(TEMP.rglob('*')) if path.is_file()}
for path in (status_path, log_path, phase_path):
    artifact_hashes[relative(path)] = sha(path)
verification = {'task': entry['task'], 'verdict': 'LOCAL_E025_PHASE2_PROVENANCE_COMPLETE_FOR_S0',
     'head': head, 'workflow_revision': entry['workflow_revision'], 'workflow_sha256': entry['workflow_sha256'],
     'read_receipt': 'entry.json and protocol.md plus actual tool transcript',
     'comparison': comparison, 'budget': budget, 'preserved_identities': preserved,
     'shared_document_histories_reconstructed_exactly': True,
     'existing_dirty_path_records_preserved': len(before_dirty), 'new_dirty_paths_at_audit': added,
     'writes': ['docs/analysis/A044-outputs/s3-e025-provenance/', 'tmp/a044-e025-phase2/',
                'docs/status.md', 'docs/log.md', 'docs/phase2-preparation.md'],
     'artifact_sha256': artifact_hashes, 'temporary_output_sha256': temporary_hashes,
     'counts': {'normal_all3': 2, 'invalid_arm_retries': 0, 'e041_fit': 0, 'checker_runs': 0,
                'new_zip': 0, 'upload': 0, 'network_queries': 0, 'installs': 0,
                'remote_compute': 0, 'subagents': 0, 'commit': 0, 'push': 0},
     'final_TEST_choice': 'not user-confirmed; E041 provisional/E025 fallback/E064 parked',
     'remaining_uncertainties': ['A012 post-run provenance and unrecorded environment fields',
        'older E025 UNICEF/WB drift cause unresolved', 'private hosted environment and hidden runtime/efficacy',
        'method/PDF, code license, current Terms/exact Final timestamps, final user choice'],
     'owned_model_or_observer_jobs': [], 'owned_running_after_this_document_command': [],
     'local_process_census': 'process-closeout.json; only this stdlib document closeout at census',
     'remote_all_chat_census': False, 'outgoing_owner': 'S3-E025-PROVENANCE-A044 /root',
     'incoming_owner': 'none; returned to S0 review, awaiting separate acceptance',
     'exclusive_writer_released': True, 'release_at': release.isoformat(),
     'scope_limit': 'Local engineering provenance only; no final TEST selection/hosted equivalence/efficacy claim'}
save('verification.json', verification)
print(json.dumps({'verdict': verification['verdict'], 'charged_seconds': charged,
      'gross_minutes_conservative': gross / 60, 'preserved_identities': len(preserved),
      'artifact_hashes': len(artifact_hashes), 'temporary_hashes': len(temporary_hashes),
      'release_at': release.isoformat(), 'verification_sha256': sha(OUT / 'verification.json')}, indent=2))
