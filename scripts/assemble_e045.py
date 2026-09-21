"""Append E045 fit/evidence overrides to the immutable E041 snapshot."""

import ast
import hashlib
import zipfile

from assemble_e044 import ROOT, PARENT_HASH, BASE_HASH


class ParentNames(ast.NodeTransformer):
    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == "parent":
            names = {"fit_sections": "_E041_FIT_SECTIONS",
                     "_replace_evidence": "_E041_REPLACE_EVIDENCE"}
            return ast.copy_location(ast.Name(id=names.get(node.attr, node.attr),
                                              ctx=node.ctx), node)
        return self.generic_visit(node)


def build_source():
    raw = (ROOT / "submissions/2026-09-19-E041/main.py").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PARENT_HASH
    base = (ROOT / "submissions/2026-09-09-E025/main.py").read_bytes()
    assert hashlib.sha256(base).hexdigest() == BASE_HASH
    assert raw.startswith(base.replace(b"\r\n", b"\n"))
    tree = ast.parse((ROOT / "src/models/union_retrieval.py").read_text(encoding="utf-8"))
    retained = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and (
                (node.module or "").startswith("src.") or node.module == "types"):
            continue
        if isinstance(node, ast.FunctionDef) and node.name == "predict":
            continue
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id in
                ("union_layer", "fit_sections", "_replace_evidence") for target in node.targets):
            continue
        retained.append(node)
    tree.body = retained
    tree = ast.fix_missing_locations(ParentNames().visit(tree))
    assert not any(isinstance(node, ast.Name) and node.id == "parent"
                   for node in ast.walk(tree))
    suffix = ("\n# E045: preserve original donors; select learned-metric candidate union.\n"
              "_E041_FIT_SECTIONS = fit_sections\n"
              "_E041_REPLACE_EVIDENCE = _replace_evidence\n\n" +
              ast.unparse(tree) + "\n\n"
              "fit_sections = fit_union_sections\n"
              "_replace_evidence = union_evidence\n")
    combined = raw + suffix.encode("utf-8")
    parsed = ast.parse(combined)
    for node in ast.walk(parsed):
        if isinstance(node, ast.ImportFrom):
            assert not (node.module or "").startswith("src.")
    return combined


def main():
    raw = build_source()
    folder = ROOT / "submissions/2026-09-21-E045"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "main.py").write_bytes(raw)
    archive = folder.with_suffix(".zip")
    info = zipfile.ZipInfo("main.py", (2026, 9, 21, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(archive, "w") as bundle:
        bundle.writestr(info, raw)
    print("main.py SHA256", hashlib.sha256(raw).hexdigest())
    print("ZIP SHA256", hashlib.sha256(archive.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
