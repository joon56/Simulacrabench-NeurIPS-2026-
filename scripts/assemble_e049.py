"""Assemble TabPFN-HSCC E049 over immutable E041 with offline V2 weights."""

import ast
import hashlib
from pathlib import Path
import zipfile

from assemble_e044 import ROOT, PARENT_HASH, BASE_HASH


class LocalNames(ast.NodeTransformer):
    def visit_Attribute(self, node):
        replacements = {
            ("parent", "predict"): "_E041_PREDICT",
            ("parent", "supervised_layer"): "_E041_SUPERVISED_LAYER",
            ("link_sharp", "predict"): "_SHARP_PREDICT",
            ("hh_cap", "CONFIGS"): "CONFIGS",
        }
        if isinstance(node.value, ast.Name):
            name = replacements.get((node.value.id, node.attr))
            if name:
                return ast.copy_location(ast.Name(id=name, ctx=node.ctx), node)
        return self.generic_visit(node)

    def visit_Assign(self, node):
        if any(isinstance(target, ast.Name) and target.id == "E049_CHECKPOINT"
               for target in node.targets):
            node.value = ast.parse(
                "Path(__file__).resolve().parent / 'tabpfn-v2-classifier.ckpt'",
                mode="eval").body
        return self.generic_visit(node)


def build_source():
    raw = (ROOT / "submissions/2026-09-19-E041/main.py").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PARENT_HASH
    base = (ROOT / "submissions/2026-09-09-E025/main.py").read_bytes()
    assert hashlib.sha256(base).hexdigest() == BASE_HASH
    assert raw.startswith(base.replace(b"\r\n", b"\n"))
    helper = ast.parse((ROOT / "src/models/adaptive_final_evidence.py").read_text(encoding="utf-8"))
    end = next(node.lineno for node in helper.body if isinstance(node, ast.FunctionDef)
               and node.name == "e047_shadow_split")
    helper.body = [node for node in helper.body if node.lineno < end and (
        isinstance(node, ast.FunctionDef)
        or isinstance(node, ast.Import)
        or (isinstance(node, ast.ImportFrom) and (node.module or "").startswith("scipy"))
        or (isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id in {"E047_FLOOR", "E047_PENALTY"}
            for target in node.targets)))]
    candidate = ast.parse((ROOT / "src/models/adaptive_tabpfn_parents.py").read_text(encoding="utf-8"))
    candidate.body = [node for node in candidate.body if not (
        isinstance(node, ast.ImportFrom) and (node.module or "").startswith("src."))
        and not (isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "LAST_DIAGNOSTICS"
            for target in node.targets))]
    candidate = ast.fix_missing_locations(LocalNames().visit(candidate))
    assert not any(isinstance(node, ast.Name) and node.id in {"parent", "link_sharp", "hh_cap"}
                   for node in ast.walk(candidate))
    suffix = ("\n# TabPFN-HSCC E049. Built with PriorLabs-TabPFN.\n"
              "_E041_PREDICT = predict\n"
              "_E041_SUPERVISED_LAYER = supervised_layer\n\n"
              + ast.unparse(helper) + "\n\n" + ast.unparse(candidate) + "\n")
    combined = raw + suffix.encode("utf-8")
    for node in ast.walk(ast.parse(combined)):
        if isinstance(node, ast.ImportFrom):
            assert not (node.module or "").startswith("src.")
    return combined


def main():
    folder = ROOT / "submissions/2026-09-23-E049"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "main.py").write_bytes(build_source())
    members = ("main.py", "requirements.txt", "NOTICE.txt", "LICENSE-TabPFN.txt",
               "tabpfn-v2-classifier.ckpt")
    checkpoint = folder / members[-1]
    assert hashlib.sha256(checkpoint.read_bytes()).hexdigest() == (
        "f65a35685aeef42e31b796d9bfa34e68d6fc780bc98e7bff7763802964cf435f")
    archive = folder.with_suffix(".zip")
    with zipfile.ZipFile(archive, "w") as bundle:
        for member in members:
            info = zipfile.ZipInfo(member, (2026, 9, 23, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, (folder / member).read_bytes())
    print("main.py SHA256", hashlib.sha256((folder / "main.py").read_bytes()).hexdigest())
    print("ZIP SHA256", hashlib.sha256(archive.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
