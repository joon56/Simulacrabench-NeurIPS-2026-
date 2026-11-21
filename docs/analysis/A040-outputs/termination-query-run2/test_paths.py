"""Execute the actual launch hash expression from source; no launcher or SDK."""
import ast
import hashlib
import json
from pathlib import Path

folder = Path(__file__).resolve().parent
paths = [folder / 'original/confirm_terminal.py', folder / 'runtime.py', folder / 'attempt.py']
def expression(path):
    tree = ast.parse(path.read_text(encoding='utf-8'))
    launch = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'launch')
    assignment = next(n for n in launch.body if isinstance(n, ast.Assign)
                      and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'hashes')
    return eval(compile(ast.Expression(assignment.value), str(path), 'eval'), globals())

old = expression(folder / 'runtime.pre-path-fix.py')
assert 'original/confirm_terminal.py' not in old
new = expression(folder / 'runtime.py')
assert new['original/confirm_terminal.py'] == '0e68a80ce1237aaa0f95d42777a24154b5cee110858e0bf0a692c17a2d75939a'
assert all('\\' not in name for name in new)
print(json.dumps({'outcome': 'WINDOWS_HASH_KEY_PASS', 'original_failure_reproduced': True, 'new_keys': list(new), 'sdk_auth_rpc': 0}))
