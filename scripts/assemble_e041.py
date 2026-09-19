"""Deterministically append E041 to the immutable E025 submission snapshot."""

import argparse
import ast
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
INCUMBENT_HASH = "00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9"


class LocalNames(ast.NodeTransformer):
    def visit_Attribute(self, node):
        replacements = {("hh_cap", "predict"): "_E025_PREDICT",
                        ("hh_cap", "CONFIGS"): "CONFIGS",
                        ("link_sharp", "predict"): "_SHARP_PREDICT"}
        if isinstance(node.value, ast.Name):
            name = replacements.get((node.value.id, node.attr))
            if name:
                return ast.copy_location(ast.Name(id=name, ctx=node.ctx), node)
        return self.generic_visit(node)


def build_source():
    incumbent = ROOT / "submissions/2026-09-09-E025/main.py"
    raw = incumbent.read_bytes()
    if hashlib.sha256(raw).hexdigest() != INCUMBENT_HASH:
        raise ValueError("E025 snapshot hash changed")
    source = ast.parse((ROOT / "src/models/supervised_retrieval.py").read_text(encoding="utf-8"))
    source.body = [node for node in source.body
                   if not (isinstance(node, ast.ImportFrom) and (node.module or "").startswith("src."))]
    source = ast.fix_missing_locations(LocalNames().visit(source))
    helper = ast.parse((ROOT / "src/eval/retrieval_oracle.py").read_text(encoding="utf-8"))
    candidate = next(node for node in helper.body if isinstance(node, ast.FunctionDef)
                     and node.name == "candidate_indices")
    combined = (raw.decode("utf-8").replace("\r\n", "\n") +
                "\n# E041: supervised section retrieval; E025 remains the fallback.\n" +
                "_E025_PREDICT = predict\n\n" + ast.unparse(candidate) + "\n\n" +
                ast.unparse(source) + "\n")
    tree = ast.parse(combined)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and (node.module or "").startswith("src"):
            raise ValueError("Local repository import survived assembly")
    return combined


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "submissions/2026-09-19-E041")
    parser.add_argument("--zip", type=Path, default=ROOT / "submissions/2026-09-19-E041.zip")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    source = build_source().encode("utf-8")
    (args.out / "main.py").write_bytes(source)
    print("main.py SHA256", hashlib.sha256(source).hexdigest())
    if args.zip:
        args.zip.parent.mkdir(parents=True, exist_ok=True)
        info = zipfile.ZipInfo("main.py", (2026, 9, 18, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        with zipfile.ZipFile(args.zip, "w") as archive:
            archive.writestr(info, source)
        print("ZIP SHA256", hashlib.sha256(args.zip.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
