"""Assemble the test-phase submission archive from this repository.

The file list, its order and the archive metadata follow MANIFEST.sha256, which was written
from the archive uploaded to the test phase. Every file is checked against its SHA256 before
it is written, so the archive content is the submitted content or the script stops.

    python tools/fetch_checkpoint.py
    python tools/make_zip.py submission.zip
"""
import hashlib
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBMITTED_SHA256 = "7ebb1972e327adc57947a977baa188036ee28c6fd30bb860a357ed2a6cd62ac8"


def main(out):
    lines = (ROOT / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    entries = [line.split("  ", 1) for line in lines if line.strip()]
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
        for digest, name in entries:
            path = ROOT / name
            if not path.is_file():
                raise SystemExit("missing %s (run tools/fetch_checkpoint.py first)" % name)
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != digest:
                raise SystemExit("content differs from the submitted file: " + name)
            info = zipfile.ZipInfo(name, date_time=(2026, 11, 10, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 0
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    digest = hashlib.sha256(Path(out).read_bytes()).hexdigest()
    print("%s  %s" % (digest, out))
    print("identical to the submitted archive" if digest == SUBMITTED_SHA256 else
          "same files as the submitted archive; the compressed bytes differ (zlib build)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "submission.zip")
