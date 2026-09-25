"""Create deterministic notice-preserving ZIPs from the two frozen mains."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
frozen = json.loads((OUT / "preflight.json").read_text(encoding="utf-8"))
report = {}
for label in ("E041", "E025"):
    folder = ROOT / f"submissions/2026-09-25-{label}"
    archive = folder.with_suffix(".zip")
    expected = frozen["candidates"][label]["main_sha256"]
    assert hashlib.sha256((folder / "main.py").read_bytes()).hexdigest() == expected
    assert (folder / "LICENSE-starter-kit.txt").read_bytes() == (ROOT / "external/starter-kit/LICENSE").read_bytes()
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for name in ("main.py", "LICENSE-starter-kit.txt"):
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 25, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            bundle.writestr(info, (folder / name).read_bytes(), compresslevel=9)
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.namelist() == ["main.py", "LICENSE-starter-kit.txt"]
        assert bundle.read("main.py") == (folder / "main.py").read_bytes()
        # Flat safe names only; official checks run separately.
        assert all("/" not in name and "\\" not in name for name in bundle.namelist())
    report[label] = {"path": str(archive.relative_to(ROOT)), "bytes": archive.stat().st_size,
        "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(), "main_sha256": expected,
        "members": ["main.py", "LICENSE-starter-kit.txt"]}
    print(label, report[label], flush=True)
with (OUT / "archives.json").open("x", encoding="utf-8") as stream:
    json.dump(report, stream, indent=2)
    stream.write("\n")
