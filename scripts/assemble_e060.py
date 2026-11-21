"""Isolated content-target retrieval suffix on immutable E041 source."""
import ast
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'submissions/2026-09-19-E041/main.py'
BASE_SHA = '22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073'
SNAP = ROOT / 'submissions/2026-09-27-E060'


class Isolate(ast.NodeTransformer):
    def __init__(self, names):
        self.names = names

    def visit_Name(self, node):
        if node.id in self.names:
            node.id = '_e060_' + node.id
        return node

    def visit_FunctionDef(self, node):
        if node.name in self.names:
            node.name = '_e060_' + node.name
        return self.generic_visit(node)

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name):
            replace = {('hh_cap', 'predict'): '_E025_PREDICT',
                       ('hh_cap', 'CONFIGS'): 'CONFIGS',
                       ('link_sharp', 'predict'): '_SHARP_PREDICT'}
            name = replace.get((node.value.id, node.attr))
            if name:
                return ast.copy_location(ast.Name(id=name, ctx=node.ctx), node)
        return self.generic_visit(node)


def build_source():
    raw = BASE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != BASE_SHA:
        raise ValueError('Frozen E041 changed')
    tree = ast.parse((ROOT / 'src/models/content_target_retrieval.py').read_text(encoding='utf-8'))
    names = {'original_objective'}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
    tree.body = [n for n in tree.body if not
                 (isinstance(n, ast.ImportFrom) and (n.module or '').startswith('src.'))]
    tree = ast.fix_missing_locations(Isolate(names).visit(tree))
    suffix = ('\n# E060 isolated globals; original snapshots unchanged.\n'
              '_e060_original_objective = metric_objective\n' + ast.unparse(tree) +
              '\npredict = _e060_predict\n')
    combined = raw + suffix.encode('utf-8')
    if any(isinstance(n, ast.ImportFrom) and (n.module or '').startswith('src')
           for n in ast.walk(ast.parse(combined))):
        raise ValueError('Local import survived assembly')
    return combined


def package():
    raw = build_source()
    if not (SNAP / 'SCORES.md').is_file():
        raise FileNotFoundError('Register scorecard before packaging')
    paths = (SNAP / 'main.py', SNAP / 'NOTICE.txt', SNAP.with_suffix('.zip'))
    if any(p.exists() for p in paths):
        raise FileExistsError('Preserve existing E060 archive')
    notice = (ROOT / 'external/starter-kit/LICENSE').read_bytes()
    for path, value in zip(paths[:2], (raw, notice)):
        with path.open('xb') as stream:
            stream.write(value)
    with zipfile.ZipFile(paths[2], 'x') as archive:
        for name, value in (('main.py', raw), ('NOTICE.txt', notice)):
            info = zipfile.ZipInfo(name, (2026, 9, 27, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, value)
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


if __name__ == '__main__':
    print(package())
