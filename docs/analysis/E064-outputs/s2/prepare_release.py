"""Mechanical local adaptation of completed release tools; no model imports."""
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent

def put(name, text):
    with (OUT / name).open('x', encoding='utf-8', newline='\n') as f:
        f.write(text)

builder = (ROOT/'scripts/assemble_e061.py').read_text(encoding='utf-8')
builder = builder.replace('E061','E064').replace('e061','e064')
builder = builder.replace('parents[1]', 'parents[4]').replace('tied_content_heads.py','conditional_gradient.py')
builder = builder.replace('f9449d41d30041f6e9714c7a25777965ec4d25cfa2563b018fb08c94dde20833',
                          '19cd35b7d0069e3244a6a89b9baec6a61e702cc80b6e3f91f1a5689926e40927')
builder = builder.replace('import zipfile','import zipfile\nfrom datetime import datetime, timezone, timedelta')
builder = builder.replace('(2026, 9, 28, 0, 0, 0)', 'datetime.now(timezone(timedelta(hours=9))).timetuple()[:6]')
builder = builder.replace('tied-head', 'conditional-gradient').replace('fixed source, isolated names', 'fixed stop-gradient source, isolated names')
put('assemble.py', builder)

runner = (ROOT/'scripts/check_e063_release.py').read_text(encoding='utf-8')
runner = runner.replace('E063','E064').replace('e063','e064')
runner = runner.replace('parents[1]', 'parents[4]').replace("'entry.json'", "'batch-entry.json'")
runner = runner.replace('from scripts.assemble_e064 import', 'from assemble import')
runner = runner.replace('from scripts.check_e057 import MemoryTree', 'from memory_tree import MemoryTree')
runner = runner.replace("'scripts/assemble_e064.py', 'scripts/check_e064_release.py',\n             'tests/test_e064_assembly.py',",
                        "str((OUT/'assemble.py').relative_to(ROOT)), str((OUT/'release.py').relative_to(ROOT)),\n             str((OUT/'tests_assembly.py').relative_to(ROOT)), str((OUT/'memory_tree.py').relative_to(ROOT)),")
runner = runner.replace("prior = sum(read(p)['wall_seconds'] for p in OUT.glob('*-resources.json'))", "prior = entry['administrative_compute_reserve_seconds'] + sum(read(p)['wall_seconds'] for p in OUT.glob('*-resources.json'))")
runner = runner.replace("'tests.test_e064_assembly.AssemblyBoundaryTests.test_frozen_prefix_and_standalone_import' if mode == 'tests-red' else 'tests.test_e064_assembly'", "str(OUT/'tests_assembly.py')")
runner = runner.replace("'-B', '-m', 'unittest',", "'-B',")
runner = runner.replace('!= 46405', '!= 132225')
runner = runner.replace('if delta025 < -.002 or delta041 < -.002:', 'if abs(delta025) > .002 or delta041 < -.002:')
runner = runner.replace("    if previous != baseline_previous:\n        raise RuntimeError('E062/E064 frozen phase1 metadata mismatch')\n", '')
runner = runner.replace("if any(actual[k] != previous[k] for k in actual):", "if any(actual[k] != previous[k] or actual[k] != baseline_previous[k] for k in actual):")
runner = runner.replace("read(S1 / 'attempts/H-01/environment.json')", "read(S1 / 'freeze-01.json')['environment']")
runner = runner.replace("actual['executable_sha256'] = sha(Path(sys.executable))", "actual['executable_sha256'] = sha(Path(sys.executable))\n    actual['base_executable_sha256'] = sha(Path(sys._base_executable))")
runner = runner.replace("('python','packages','executable_sha256','torch_threads'", "('python','packages','executable_sha256','base_executable_sha256','torch_threads'")
runner = runner.replace("if name == 'unhcr':\n            events =", "if True:\n            events =")
runner = runner.replace("if name == 'unhcr':\n            row['natural_policy']", "if True:\n            row['natural_policy']")
runner = runner.replace('check_round_observations(events)', 'check_observations(events, name)')
start = runner.index('def check_observations(')
end = runner.index('def preflight():', start)
runner = runner[:start] + '''def check_observations(events, name):
    expected = read(S1/'attempts/H-01/complete.json')
    observed = {}
    for e in events:
        if e.get('event') == 'invariant':
            row = observed.setdefault(e['key'], {'phase':e['phase'], 'hashes':[]})
            if row['phase'] != e['phase']: raise RuntimeError('Invariant phase changed')
            row['hashes'].append(e['sha256'])
    if observed != expected['invariants'][name]:
        save(OUT/('invariant-mismatch-'+os.environ.get('E064_STAGE','unknown')+'-'+name+'.json'),
             {'observed':observed, 'expected':expected['invariants'][name]})
        raise RuntimeError('Source/assembly metric/donor/replay invariant mismatch')
    lambdas = [e['values'] for e in events if e.get('event') == 'lambda']
    if not lambdas or lambdas[-1] != expected['retrieval'][name]['lambda']:
        raise RuntimeError('Source/assembly lambda mismatch')
    neural = [e for e in events if e.get('event') == 'return' and e.get('kind') == 'neural']
    if len(neural) != 3: raise RuntimeError('Three neural fits expected')
    if name == 'unhcr' and any(e['network_class'] != '_e064_ConditionalGradientNet' for e in neural):
        raise RuntimeError('Candidate local factory disconnected')
    return {'status':'PASS', 'invariant_keys':len(observed), 'lambda_exact':True, 'neural_calls':len(neural)}


''' + runner[end:]
# Replace the old observer class; production code itself is never modified.
start = runner.index('class Audit:')
end = runner.index('def environment():', start)
runner = runner[:start] + (OUT/'audit_body.txt').read_text(encoding='utf-8') + '\n\n' + runner[end:]
# Include the exact structured digest helper in the external CLI observer.
s1tree = ast.parse((ROOT/'scripts/check_e064_conditional_gradient.py').read_text(encoding='utf-8'))
digest = ast.unparse(next(n for n in s1tree.body if isinstance(n, ast.FunctionDef) and n.name=='structured_digest'))
runner = runner.replace("class Audit:", digest+'\n\nclass Audit:',1)
runner = runner.replace("inspect.getsource(Audit) + '\\n'", "inspect.getsource(structured_digest) + '\\n' + inspect.getsource(Audit) + '\\n'")
runner = runner.replace("return dict(full_stack=9, neural=27, metric=24)", "return dict(full_stack=12, neural=36, metric=24)")
# Explicit raw allowlist before any NPZ load. Freeze includes their bytes plus synthetic files.
runner = runner.replace("    expected = record['sha256']\n", "    expected = record['sha256']\n    allowed = read(OUT/'batch-entry.json')['numeric_allowlist_expected']\n    if allowed.get(path.relative_to(ROOT).as_posix()) != expected:\n        raise RuntimeError('Raw path outside exact B01 allowlist')\n")
runner = runner.replace("    env = environment()\n    official = official_module()\n    inputs = {}", "    env = environment()\n    numeric = read(OUT/'batch-entry.json')\n    for field in ('numeric_allowlist_expected','synthetic_allowlist_expected'):\n        for p,h in numeric[field].items():\n            if sha(ROOT/p) != h: raise RuntimeError('Allowed numerical identity mismatch: '+p)\n    save(OUT/'numeric-identity.json', {'status':'PASS', 'hashes':dict(numeric['numeric_allowlist_expected'], **numeric['synthetic_allowlist_expected'])})\n    official = official_module()\n    inputs = {}")
runner = runner.replace("    hashes.update(staging_hashes)", "    hashes.update(staging_hashes)\n    hashes.update(read(OUT/'numeric-identity.json')['hashes'])")
runner = runner.replace("    verify()\n    if mode == 'assembly'", "    verify()\n    if mode in ('assembly','official'):\n        starts=list(OUT.glob('all3-start-*.json'))\n        if len(starts)>=4: raise RuntimeError('All3 start cap')\n        save(OUT/('all3-start-'+str(len(starts)+1)+'.json'), {'stage':mode, 'utc':datetime.now(timezone.utc).isoformat()})\n    if mode == 'assembly'")
# Enforce aggregate budget before launch; keep 2s shutdown reserve.
runner = runner.replace("    limit = 900 if", "    limit = 900 if")
runner = runner.replace("    with log_path.open('x', encoding='utf-8') as log:", "    if prior + limit > 3600 or time.time()+limit > deadline:\n        raise RuntimeError('Insufficient remaining full-stage budget')\n    if mode.startswith('tests') and len(list(OUT.glob('tests*-resources.json'))) >= 3:\n        raise RuntimeError('Focused cycle cap')\n    with log_path.open('x', encoding='utf-8') as log:")
put('release.py', runner)
put('memory_tree.py', (ROOT/'docs/analysis/E064-outputs/memory_tree.py').read_text(encoding='utf-8'))
print('Local assembly/harness copies created; no model import or numerical input access.')
