"""E063 fixed round metric suffix; preserve the exact E041 prefix and globals."""
import ast
import hashlib
from datetime import datetime
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'submissions/2026-09-19-E041/main.py'
SOURCE = ROOT / 'src/models/round_metric_retrieval.py'
RENDERER = ROOT / 'src/models/link_sharp.py'
HASHES = {
    BASE: '22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073',
    SOURCE: '5595bebdcdc697fc9e1eba149e10735cac4ae434b20b0ce3e93c968e8b35106b',
    RENDERER: '4a7921a00d7758e52a63a3ca7cd5ebf2285cef445b57fd89f15580d6fc108524',
}


class Isolate(ast.NodeTransformer):
    def __init__(self, names):
        self.names = names

    def visit_Name(self, node):
        node.id = self.names.get(node.id, node.id)
        return node

    def visit_FunctionDef(self, node):
        node.name = self.names.get(node.name, node.name)
        return self.generic_visit(node)

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name):
            mapping = {
                ('original', 'predict'): '_E063_CONTROL_PREDICT',
                ('hh_cap', 'CONFIGS'): 'CONFIGS',
                ('link_sharp', 'predict'): '_e063_render_predict',
            }
            pair = node.value.id, node.attr
            if pair in mapping:
                return ast.copy_location(ast.Name(id=mapping[pair], ctx=node.ctx), node)
            if node.value.id in ('original', 'hh_cap', 'link_sharp'):
                raise ValueError('Unmapped repository attribute: ' + repr(pair))
        return self.generic_visit(node)


def build_source():
    for path, expected in HASHES.items():
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen assembly input changed: ' + str(path))
    tree = ast.parse(SOURCE.read_text(encoding='utf-8'))
    names = {n.name: '_e063_' + n.name.lstrip('_') for n in tree.body
             if isinstance(n, ast.FunctionDef)}
    names['LAST_DIAGNOSTICS'] = '_e063_LAST_DIAGNOSTICS'
    tree.body = [n for n in tree.body if not
                 (isinstance(n, ast.ImportFrom) and (n.module or '').startswith('src.'))]
    tree = ast.fix_missing_locations(Isolate(names).visit(tree))
    renderer = next(n for n in ast.parse(RENDERER.read_text(encoding='utf-8')).body
                    if isinstance(n, ast.FunctionDef) and n.name == 'predict')
    renderer.name = '_e063_render_predict'
    suffix = ('\n# E063 fixed H; E041 fallback and imported helper globals untouched.\n'
              '_E063_CONTROL_PREDICT = predict\n' + ast.unparse(renderer) + '\n\n' +
              ast.unparse(tree) + '\npredict = _e063_predict\n')
    combined = BASE.read_bytes() + suffix.encode('utf-8')
    for n in ast.walk(ast.parse(combined)):
        modules = ([n.module or ''] if isinstance(n, ast.ImportFrom) else
                   [a.name for a in n.names] if isinstance(n, ast.Import) else [])
        if any(m.startswith(('src', 'scripts')) for m in modules):
            raise ValueError('Repository import survived assembly')
    return combined


def package(snapshot, frozen_main):
    snapshot, frozen_main = Path(snapshot), Path(frozen_main)
    if not (snapshot / 'SCORES.md').is_file():
        raise FileNotFoundError('Preregistered scorecard required')
    raw = build_source()
    if raw != frozen_main.read_bytes():
        raise ValueError('Assembly bytes changed after qualification')
    paths = snapshot / 'main.py', snapshot / 'NOTICE.txt', snapshot.with_suffix('.zip')
    if any(p.exists() for p in paths):
        raise FileExistsError('Never overwrite a snapshot/archive')
    notice = (ROOT / 'external/starter-kit/LICENSE').read_bytes()
    for path, value in zip(paths[:2], (raw, notice)):
        with path.open('xb') as stream:
            stream.write(value)
    stamp = datetime.now().timetuple()[:6]
    with zipfile.ZipFile(paths[2], 'x') as archive:
        for name, value in (('main.py', raw), ('NOTICE.txt', notice)):
            info = zipfile.ZipInfo(name, stamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, value)
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
