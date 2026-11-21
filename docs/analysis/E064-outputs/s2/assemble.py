"""E064 isolated conditional-gradient suffix; frozen E041 prefix remains byte-identical."""
import ast
import hashlib
from pathlib import Path
import zipfile
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / 'submissions/2026-09-19-E041/main.py'
SOURCE = ROOT / 'src/models/conditional_gradient.py'
RENDERER = ROOT / 'src/models/link_sharp.py'
HASHES = {
    BASE: '22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073',
    SOURCE: '19cd35b7d0069e3244a6a89b9baec6a61e702cc80b6e3f91f1a5689926e40927',
    RENDERER: '4a7921a00d7758e52a63a3ca7cd5ebf2285cef445b57fd89f15580d6fc108524',
}


class Isolate(ast.NodeTransformer):
    def __init__(self, names):
        self.names = names

    def visit_Name(self, node):
        if node.id in self.names:
            node.id = self.names[node.id]
        return node

    def visit_FunctionDef(self, node):
        node.name = self.names.get(node.name, node.name)
        return self.generic_visit(node)

    def visit_ClassDef(self, node):
        node.name = self.names.get(node.name, node.name)
        return self.generic_visit(node)

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name):
            mapping = {
                ('shared_trunk', '_Net'): '_Net',
                ('supervised_retrieval', 'predict'): '_E064_CONTROL_PREDICT',
                ('supervised_retrieval', 'supervised_layer'): 'supervised_layer',
                ('hh_cap', 'CONFIGS'): 'CONFIGS',
                ('link_sharp', 'predict'): '_e064_render_predict',
            }
            pair = node.value.id, node.attr
            if pair in mapping:
                return ast.copy_location(ast.Name(id=mapping[pair], ctx=node.ctx), node)
            if node.value.id in ('shared_trunk', 'supervised_retrieval', 'hh_cap', 'link_sharp'):
                raise ValueError('Unmapped repository module attribute: ' + repr(pair))
        return self.generic_visit(node)


def build_source():
    for path, expected in HASHES.items():
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen assembly dependency changed: ' + str(path))
    tree = ast.parse(SOURCE.read_text(encoding='utf-8'))
    names = {node.name: '_e064_' + node.name.lstrip('_')
             for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    tree.body = [node for node in tree.body if not
                 (isinstance(node, ast.ImportFrom) and (node.module or '').startswith('src.'))]
    tree = ast.fix_missing_locations(Isolate(names).visit(tree))
    original_renderer = ast.parse(RENDERER.read_text(encoding='utf-8'))
    renderer = next(node for node in original_renderer.body
                    if isinstance(node, ast.FunctionDef) and node.name == 'predict')
    renderer.name = '_e064_render_predict'
    suffix = ('\n# E064: fixed stop-gradient source, isolated names, original control globals retained.\n'
              '_E064_CONTROL_PREDICT = predict\n' + ast.unparse(renderer) + '\n\n' +
              ast.unparse(tree) + '\npredict = _e064_predict\n')
    combined = BASE.read_bytes() + suffix.encode('utf-8')
    for node in ast.walk(ast.parse(combined)):
        if isinstance(node, ast.ImportFrom) and (node.module or '').startswith(('src', 'scripts')):
            raise ValueError('Repository import survived assembly')
    return combined


def package(snapshot, frozen_main):
    snapshot, frozen_main = Path(snapshot), Path(frozen_main)
    if not (snapshot / 'SCORES.md').is_file():
        raise FileNotFoundError('Scorecard must precede package')
    raw = build_source()
    if raw != frozen_main.read_bytes():
        raise ValueError('Source changed after assembly qualification')
    paths = (snapshot / 'main.py', snapshot / 'NOTICE.txt', snapshot.with_suffix('.zip'))
    if any(path.exists() for path in paths):
        raise FileExistsError('Never overwrite an E064 snapshot/archive')
    notice = (ROOT / 'external/starter-kit/LICENSE').read_bytes()
    for path, value in zip(paths[:2], (raw, notice)):
        with path.open('xb') as stream:
            stream.write(value)
    with zipfile.ZipFile(paths[2], 'x') as archive:
        for name, value in (('main.py', raw), ('NOTICE.txt', notice)):
            info = zipfile.ZipInfo(name, datetime.now(timezone(timedelta(hours=9))).timetuple()[:6])
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, value)
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
