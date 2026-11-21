"""Assemble an E065 submission directory and ZIP (heavy artifacts stay under tmp/).

python scripts/build_e065.py --variant a25            # strict DEV build
python scripts/build_e065.py --variant a50 --no-strict --budget 3000
"""
import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = ROOT / "submissions" / "2026-11-08-E065" / "main.py"
E041_MAIN = ROOT / "submissions" / "2026-09-19-E041" / "main.py"
E041_SHA256 = "22c911806ea91234ae350341adfb9c0df2ce4be41cc88e73be304e4bb1023073"
LOCAL = ROOT / "tmp" / "a040-local-technical"
TABICL_SRC = LOCAL / "source" / "tabicl-0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3"
SITE = LOCAL / "venv" / "Lib" / "site-packages"
CHECKPOINT = LOCAL / "acquisition" / "tabicl-classifier-v2-20260212.ckpt"
CHECKPOINT_SHA256 = "bdc7dbd5e4ff21f8f0456fcf90c6b7cdf72dbea960f2d05b19bec19f9b3d4ed0"
KIT_LICENSE = ROOT / "external" / "starter-kit" / "LICENSE"

NOTICE = """E065 submission third-party components (unmodified copies)

- TabICL 2.2.0 source, git 0dbff3ec8fc68c123c87af77b0ea8b25cd2d23f3 (soda-inria/tabicl),
  vendor/primary/tabicl. BSD 3-Clause; see LICENSES/tabicl-LICENSE.
- TabICL v2 classifier checkpoint tabicl-classifier-v2-20260212.ckpt, Hugging Face
  jingang/TabICL revision 4dcd344ece2c00be9e831fdd35bed57b5ad83e19, SHA256
  bdc7dbd5e4ff21f8f0456fcf90c6b7cdf72dbea960f2d05b19bec19f9b3d4ed0, weights/.
  Model metadata declares bsd-3-clause.
- einops 0.8.1, vendor/primary/einops. MIT; see LICENSES/einops-LICENSE.
- tqdm 4.67.1, vendor/fallback/tqdm (used only if the runtime image lacks tqdm).
  MPL-2.0 AND MIT; see LICENSES/tqdm-LICENCE.
- HSCC starter kit material, MIT; see LICENSES/starter-kit-LICENSE.

Team code: main.py and e041_core.py.
"""


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def copy_tree(src, dst):
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def render_main(variant, strict, budget):
    text = SOURCE_MAIN.read_text(encoding="utf-8")
    text, n1 = re.subn(r'^VARIANT = "[a-z0-9]+"', 'VARIANT = "%s"' % variant, text, flags=re.M)
    text, n2 = re.subn(r"^STRICT = (True|False)", "STRICT = %s" % strict, text, flags=re.M)
    text, n3 = re.subn(r"^BUDGET_SECONDS = (None|\d+)", "BUDGET_SECONDS = %s" % budget, text, flags=re.M)
    if (n1, n2, n3) != (1, 1, 1):
        raise ValueError("main.py build markers not found exactly once")
    return text


def build(variant, strict, budget, out_root):
    name = "2026-11-08-E065%s%s" % (variant, "" if strict else "-final")
    build_dir = out_root / ("build-" + name)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    (build_dir / "vendor" / "primary").mkdir(parents=True)
    (build_dir / "vendor" / "fallback").mkdir(parents=True)
    (build_dir / "weights").mkdir()
    (build_dir / "LICENSES").mkdir()

    if sha256(E041_MAIN) != E041_SHA256:
        raise ValueError("E041 main.py identity mismatch")
    if CHECKPOINT.stat().st_size != 110368038 or sha256(CHECKPOINT) != CHECKPOINT_SHA256:
        raise ValueError("Checkpoint identity mismatch")

    (build_dir / "main.py").write_text(render_main(variant, strict, budget), encoding="utf-8")
    shutil.copy2(E041_MAIN, build_dir / "e041_core.py")
    copy_tree(TABICL_SRC / "src" / "tabicl", build_dir / "vendor" / "primary" / "tabicl")
    copy_tree(SITE / "einops", build_dir / "vendor" / "primary" / "einops")
    copy_tree(SITE / "tqdm", build_dir / "vendor" / "fallback" / "tqdm")
    shutil.copy2(CHECKPOINT, build_dir / "weights" / CHECKPOINT.name)
    shutil.copy2(TABICL_SRC / "LICENSE", build_dir / "LICENSES" / "tabicl-LICENSE")
    shutil.copy2(SITE / "einops-0.8.1.dist-info" / "licenses" / "LICENSE",
                 build_dir / "LICENSES" / "einops-LICENSE")
    shutil.copy2(SITE / "tqdm-4.67.1.dist-info" / "LICENCE", build_dir / "LICENSES" / "tqdm-LICENCE")
    shutil.copy2(KIT_LICENSE, build_dir / "LICENSES" / "starter-kit-LICENSE")
    (build_dir / "NOTICE.txt").write_text(NOTICE, encoding="utf-8")

    files = sorted(p for p in build_dir.rglob("*") if p.is_file())
    zip_path = out_root / (name + ".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(build_dir).as_posix(), date_time=(2026, 11, 8, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(path, "rb") as fh:
                zf.writestr(info, fh.read())
    manifest = dict(variant=variant, strict=strict, budget_seconds=budget,
                    zip=str(zip_path), zip_bytes=zip_path.stat().st_size, zip_sha256=sha256(zip_path),
                    main_sha256=sha256(build_dir / "main.py"),
                    e041_core_sha256=sha256(build_dir / "e041_core.py"),
                    checkpoint_sha256=CHECKPOINT_SHA256, files=len(files))
    (out_root / (name + ".manifest.json")).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return build_dir, manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=["a25", "a50", "guard"], required=True)
    parser.add_argument("--no-strict", action="store_true")
    parser.add_argument("--budget", type=int, default=None)
    parser.add_argument("--out", default=str(ROOT / "tmp" / "e065"))
    args = parser.parse_args()
    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    build_dir, manifest = build(args.variant, not args.no_strict, args.budget, out_root)
    print(json.dumps(dict(build_dir=str(build_dir), **manifest), indent=2))


if __name__ == "__main__":
    main()
