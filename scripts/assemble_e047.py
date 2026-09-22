"""Append the E047 final-evidence correction to the immutable E041 snapshot."""

import ast
import hashlib
import zipfile

from assemble_e044 import ROOT, PARENT_HASH, BASE_HASH


class LocalNames(ast.NodeTransformer):
    def visit_Attribute(self, node):
        replacements = {
            ("parent", "predict"): "_E041_PREDICT",
            ("parent", "supervised_layer"): "_E041_SUPERVISED_LAYER",
            ("parent", "_groups"): "_E041_GROUPS",
            ("link_sharp", "predict"): "_SHARP_PREDICT",
            ("hh_cap", "CONFIGS"): "CONFIGS",
        }
        if isinstance(node.value, ast.Name):
            name = replacements.get((node.value.id, node.attr))
            if name:
                return ast.copy_location(ast.Name(id=name, ctx=node.ctx), node)
        return self.generic_visit(node)


def build_source():
    raw = (ROOT / "submissions/2026-09-19-E041/main.py").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PARENT_HASH
    base = (ROOT / "submissions/2026-09-09-E025/main.py").read_bytes()
    assert hashlib.sha256(base).hexdigest() == BASE_HASH
    assert raw.startswith(base.replace(b"\r\n", b"\n"))
    tree = ast.parse((ROOT / "src/models/adaptive_final_evidence.py").read_text(encoding="utf-8"))
    tree.body = [node for node in tree.body if not (
        isinstance(node, ast.ImportFrom) and (node.module or "").startswith("src."))
        and not (isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "LAST_DIAGNOSTICS"
            for target in node.targets))]
    tree = ast.fix_missing_locations(LocalNames().visit(tree))
    forbidden = {"parent", "link_sharp", "hh_cap"}
    assert not any(isinstance(node, ast.Name) and node.id in forbidden
                   for node in ast.walk(tree)), "Unresolved repository module reference"
    suffix = ("\n# E047: query-adaptive evidence after the complete E041 prediction.\n"
              "_E041_PREDICT = predict\n"
              "_E041_SUPERVISED_LAYER = supervised_layer\n"
              "_E041_GROUPS = _groups\n\n" + ast.unparse(tree) + "\n")
    combined = raw + suffix.encode("utf-8")
    for node in ast.walk(ast.parse(combined)):
        if isinstance(node, ast.ImportFrom):
            assert not (node.module or "").startswith("src.")
    return combined


def main():
    raw = build_source()
    folder = ROOT / "submissions/2026-09-22-E047"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "main.py").write_bytes(raw)
    archive = folder.with_suffix(".zip")
    info = zipfile.ZipInfo("main.py", (2026, 9, 22, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(archive, "w") as bundle:
        bundle.writestr(info, raw)
    print("main.py SHA256", hashlib.sha256(raw).hexdigest())
    print("ZIP SHA256", hashlib.sha256(archive.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
