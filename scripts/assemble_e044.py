"""Append a single evidence-construction override to frozen E041."""

import ast
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PARENT_HASH = "22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073"
BASE_HASH = "00793cf9d720d6f7511ffd738935206b3a5401f2454255409429db8d55e991b9"


def build_source():
    raw = (ROOT / "submissions/2026-09-19-E041/main.py").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PARENT_HASH
    base = (ROOT / "submissions/2026-09-09-E025/main.py").read_bytes()
    assert hashlib.sha256(base).hexdigest() == BASE_HASH
    assert raw.startswith(base.replace(b"\r\n", b"\n"))
    tree = ast.parse((ROOT / "src/models/retrieval_weight_control.py").read_text(encoding="utf-8"))
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                    and n.name == "fixed_metric_evidence")
    function.name = "_replace_evidence"
    call = function.body[-1].value
    assert isinstance(call.func, ast.Attribute) and call.func.attr == "_replace_evidence"
    assert isinstance(call.func.value, ast.Name) and call.func.value.id == "parent"
    call.func = ast.Name(id="_E041_REPLACE_EVIDENCE", ctx=ast.Load())
    function = ast.fix_missing_locations(function)
    suffix = ("\n# E044: conditional weight-use ablation; activation remains E041.\n"
              "_E041_REPLACE_EVIDENCE = _replace_evidence\n\n" + ast.unparse(function) + "\n")
    source = raw + suffix.encode("utf-8")
    ast.parse(source)
    return source


def main():
    source = build_source()
    folder = ROOT / "submissions/2026-09-20-E044"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "main.py").write_bytes(source)
    archive = folder.with_suffix(".zip")
    info = zipfile.ZipInfo("main.py", (2026, 9, 20, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(archive, "w") as bundle:
        bundle.writestr(info, source)
    print("main.py SHA256", hashlib.sha256(source).hexdigest())
    print("ZIP SHA256", hashlib.sha256(archive.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
