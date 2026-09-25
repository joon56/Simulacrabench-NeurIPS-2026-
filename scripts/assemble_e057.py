"""Deterministic isolated E057 wrapper on the immutable E041 archive source."""
import ast
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'submissions/2026-09-19-E041/main.py'
BASE_SHA = '22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073'
SNAP = ROOT / 'submissions/2026-09-25-E057'


class Isolate(ast.NodeTransformer):
    def __init__(self, names):
        self.names = names

    def visit_Name(self, node):
        if node.id in self.names:
            node.id = '_e057_' + node.id
        return node

    def visit_FunctionDef(self, node):
        if node.name in self.names:
            node.name = '_e057_' + node.name
        return self.generic_visit(node)

    def visit_alias(self, node):
        local = node.asname or node.name
        if local in self.names:
            node.asname = '_e057_' + local
        return node


def build_source():
    raw = BASE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != BASE_SHA:
        raise ValueError('Frozen E041 changed')
    tree = ast.parse((ROOT / 'src/models/conditional_leaf_content.py').read_text(encoding='utf-8'))
    names = {'floor_mix', 'incumbent_predict'}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            names.update(a.asname or a.name for a in node.names)
    tree.body = [n for n in tree.body if not
                 (isinstance(n, ast.ImportFrom) and (n.module or '').startswith('src.'))]
    helper = ast.parse((ROOT / 'src/eval/logloss.py').read_text(encoding='utf-8'))
    tree.body.insert(0, next(n for n in helper.body if isinstance(n, ast.FunctionDef) and n.name == 'floor_mix'))
    tree = ast.fix_missing_locations(Isolate(names).visit(tree))
    suffix = ('\n# E057: names isolated to preserve immutable E041 globals.\n'
              '_e057_incumbent_predict = predict\n' + ast.unparse(tree) + '\n'
              'predict = _e057_predict\n')
    return raw + suffix.encode('utf-8')


def main():
    raw = build_source()
    paths = [SNAP / 'main.py', SNAP / 'NOTICE.txt', SNAP.with_suffix('.zip')]
    if any(p.exists() for p in paths):
        raise FileExistsError('Refuse an existing E057 package before writing')
    if not (SNAP / 'SCORES.md').is_file():
        raise FileNotFoundError('Preregister SCORES.md before packaging')
    notice = (ROOT / 'external/starter-kit/LICENSE').read_bytes()
    for path, value in ((paths[0], raw), (paths[1], notice)):
        with path.open('xb') as stream:
            stream.write(value)
    with zipfile.ZipFile(paths[2], 'x') as archive:
        for name, value in (('main.py', raw), ('NOTICE.txt', notice)):
            info = zipfile.ZipInfo(name, (2026, 9, 25, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, value)
    print({p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})


if __name__ == '__main__':
    main()
