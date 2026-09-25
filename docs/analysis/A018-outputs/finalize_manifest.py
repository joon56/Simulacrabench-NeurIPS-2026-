"""Freeze/check release files after all scoring and PDF review; no model fits."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tmp/pdf-deps"))
from pypdf import PdfReader


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


manifest_path = OUT / "freeze-manifest.json"
if manifest_path.exists():
    existing = read(manifest_path)
    for relative, expected in existing["frozen_files_sha256"].items():
        assert digest(ROOT / relative) == expected, relative
    for relative, expected in existing["originals_preserved_sha256"].items():
        assert digest(ROOT / relative) == expected, relative
    print("PASS: immutable manifest", len(existing["frozen_files_sha256"]), "files")
    sys.exit(0)

preflight = read(OUT / "preflight.json")
assert digest(OUT / "selection-registration.md") == preflight["protocol_sha256"]
assert digest(OUT / "verify_release.executed.py") == preflight["verifier_sha256"]
for relative, expected in preflight["inputs"].items():
    assert digest(ROOT / relative) == expected, relative
originals = {}
for candidate in preflight["candidates"].values():
    for key in ("main", "archive"):
        relative = candidate[key]
        assert digest(ROOT / relative) == candidate[f"{key}_sha256"]
        originals[relative.replace("\\", "/")] = candidate[f"{key}_sha256"]
old_methods = read(ROOT / "submissions/phase2-E041-preparation/method-validation.json")
for row in old_methods["files"]:
    if row["path"].startswith("submissions/"):
        assert digest(ROOT / row["path"]) == row["sha256"]
        originals[row["path"]] = row["sha256"]

archives = read(OUT / "archives.json")
official = read(OUT / "official-summary.json")
assert official["archive_sha256"] == archives["E041"]["sha256"]
assert set(official["instruments"]) == {"unicef", "world_bank", "unhcr"}
assert official["cells_exact"] == 442425 and official["inclusive_wall_seconds"] < 3600
checks = {}
for label in ("E041", "E025"):
    folder = ROOT / f"submissions/2026-09-25-{label}"
    archive = folder.with_suffix(".zip")
    assert digest(archive) == archives[label]["sha256"]
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.namelist() == ["main.py", "LICENSE-starter-kit.txt"]
        for name in bundle.namelist():
            assert bundle.read(name) == (folder / name).read_bytes()
    shared = read(OUT / f"{label}-shared.json")
    assert shared["inclusive_seconds"] < 3600
    assert max(shared["memory"].values()) < 16_000_000_000
    assert sum(v["cells"] for v in shared["instruments"].values()) == 442425
    assert all(v["a012_source_raw_max_abs"] == 0 for v in shared["instruments"].values())
    assert len(PdfReader(folder / "method-4p.pdf").pages) == 4
    checker = subprocess.run([sys.executable, str(ROOT / "external/starter-kit/tools/check_submission_zip.py"), str(archive)],
                             capture_output=True, text=True, check=True)
    checks[label] = {"zip_checker": checker.stdout.strip(), "method_pages": 4,
                     "method_sha256": digest(folder / "method-4p.pdf"),
                     "shared_seconds": shared["inclusive_seconds"], "memory": shared["memory"]}
assert (ROOT / "docs/method-4p.md").read_bytes() == (ROOT / "submissions/2026-09-25-E041/method-4p.md").read_bytes()
assert (ROOT / "output/pdf/method-4p.pdf").read_bytes() == (ROOT / "submissions/2026-09-25-E041/method-4p.pdf").read_bytes()
for name, row in official["instruments"].items():
    assert row["status"] == "PASS" and row["raw_max_abs"] == 0 and abs(row["e025_delta"]) <= .002

paths = [ROOT / "docs/analysis/A018-test-selection.md", ROOT / "docs/method-4p.md", ROOT / "output/pdf/method-4p.pdf",
         ROOT / "submissions/phase2-E025-preparation/verification.json"]
paths += [p for p in OUT.rglob("*") if p.is_file() and p.suffix in {".json", ".md", ".txt", ".py", ".png", ".log"}]
for label in ("E041", "E025"):
    folder = ROOT / f"submissions/2026-09-25-{label}"
    paths.extend(p for p in folder.iterdir() if p.is_file())
    paths.append(folder.with_suffix(".zip"))
frozen = {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(set(paths))}
manifest = {"frozen_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "selected": "E041", "fallback": "E025", "test_uploaded": False,
    "model_change_cutoff_utc": "2026-11-12T00:00:00Z", "preferred_upload_by_utc": "2026-11-13T00:00:00Z",
    "official_test_end_utc": "2026-11-14T00:00:00Z", "license_status": "Scoped team MIT proposal only; owner choice required before award-stage source delivery",
    "checks": checks, "visual_review": "All eight final pages inspected; bounds PASS; model-specific footer/title",
    "a012_input_hashes_rechecked": len(preflight["inputs"]), "originals_preserved_sha256": originals,
    "frozen_files_sha256": frozen}
with manifest_path.open("x", encoding="utf-8") as stream:
    json.dump(manifest, stream, indent=2, ensure_ascii=False)
    stream.write("\n")
print("FROZEN", manifest["frozen_utc"], len(frozen), "files", json.dumps(checks, indent=2))
