"""Append the fixed E052 endpoint to the immutable E041 standalone source."""

import ast
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PARENT_HASH = "22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073"
BASE_HASH = "00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9"


class StandaloneBindings(ast.NodeTransformer):
    """Bind source-module references to the frozen monolith's original objects."""

    def visit_Attribute(self, node):
        aliases = {
            "link_sharp.predict": "_SHARP_PREDICT",
            "hh_cap.CONFIGS": "CONFIGS",
            "supervised_retrieval.predict": "_E041_PREDICT",
            "supervised_retrieval.supervised_layer": "_E041_SUPERVISED_LAYER",
            "supervised_retrieval.LAST_DIAGNOSTICS": "LAST_DIAGNOSTICS",
        }
        replacement = aliases.get(ast.unparse(node))
        if replacement:
            return ast.copy_location(ast.Name(id=replacement, ctx=node.ctx), node)
        return self.generic_visit(node)


class WrapperDiagnostics(ast.NodeTransformer):
    """Keep wrapper reports separate from E041 supervised-layer diagnostics."""

    def visit_Name(self, node):
        if node.id == "LAST_DIAGNOSTICS":
            node.id = "_E052_DIAGNOSTICS"
        return node


def build_source():
    raw = (ROOT / "submissions/2026-09-19-E041/main.py").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PARENT_HASH
    base = (ROOT / "submissions/2026-09-09-E025/main.py").read_bytes()
    assert hashlib.sha256(base).hexdigest() == BASE_HASH
    assert raw.startswith(base.replace(b"\r\n", b"\n"))
    helpers = ast.parse((ROOT / "src/eval/recursive_candidates.py").read_text(encoding="utf-8"))
    selected = {"predict_components", "_partition", "cached_renderer", "_mapped"}
    nodes = [n for n in helpers.body if isinstance(n, ast.FunctionDef) and n.name in selected]
    assert {n.name for n in nodes} == selected
    routing = ast.parse((ROOT / "src/eval/evidence_routing.py").read_text(encoding="utf-8"))
    nodes.extend(n for n in routing.body if not isinstance(n, (ast.Import, ast.ImportFrom)))
    wrapper = ast.parse((ROOT / "src/models/evidence_after_gates.py").read_text(encoding="utf-8"))
    wrapper = WrapperDiagnostics().visit(wrapper)
    nodes.extend(n for n in wrapper.body if not isinstance(n, (ast.Import, ast.ImportFrom)))
    appended = StandaloneBindings().visit(ast.Module(body=nodes, type_ignores=[]))
    appended = ast.fix_missing_locations(appended)
    suffix = ("\n# E052: fixed evidence-after-gates exploratory control.\n"
              "from copy import deepcopy\nfrom types import FunctionType\nimport numpy as np\n"
              "_E041_PREDICT = predict\n_E041_SUPERVISED_LAYER = supervised_layer\n\n"
              + ast.unparse(appended) + "\n")
    source = raw + suffix.encode("utf-8")
    tree = ast.parse(source)
    assert not any(isinstance(n, ast.ImportFrom) and (n.module or "").startswith("src")
                   for n in ast.walk(tree))
    return source


def main():
    source = build_source()
    folder = ROOT / "submissions/2026-09-24-E052"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "main.py").write_bytes(source)
    archive = folder.with_suffix(".zip")
    info = zipfile.ZipInfo("main.py", (2026, 9, 24, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(archive, "w") as bundle:
        bundle.writestr(info, source)
    print("main.py SHA256", hashlib.sha256(source).hexdigest())
    print("ZIP SHA256", hashlib.sha256(archive.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
