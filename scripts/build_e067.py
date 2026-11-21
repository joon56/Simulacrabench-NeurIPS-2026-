"""Assemble an E067 composition package (heavy artifacts stay under tmp/).

python scripts/build_e067.py --name u25 --plan '{"unicef": 0.25}'
python scripts/build_e067.py --name final --plan '{"world_bank": "guard"}' --unhcr-fix --no-strict --budget 3000
"""
import argparse
import json
import re
import shutil
import zipfile
from pathlib import Path

import build_e065 as base

SOURCE_MAIN = base.ROOT / "submissions" / "2026-11-09-E067" / "main.py"


def render_main(plan, unhcr_fix, strict, budget, seeds=(0,), regate=False):
    text = SOURCE_MAIN.read_text(encoding="utf-8")
    replacements = (
        (r"^PLAN = .*$", "PLAN = %r" % dict(sorted(plan.items()))),
        (r"^UNHCR_FIX = .*$", "UNHCR_FIX = %s" % bool(unhcr_fix)),
        (r"^SEEDS = .*$", "SEEDS = %r" % (tuple(int(s) for s in seeds),)),
        (r"^REGATE = .*$", "REGATE = %s" % bool(regate)),
        (r"^STRICT = .*$", "STRICT = %s" % bool(strict)),
        (r"^BUDGET_SECONDS = .*$", "BUDGET_SECONDS = %s" % budget),
    )
    for pattern, value in replacements:
        text, n = re.subn(pattern, value, text, count=1, flags=re.M)
        if n != 1:
            raise ValueError("build marker missing: " + pattern)
    return text


def build(name, plan, unhcr_fix, strict, budget, out_root, seeds=(0,), regate=False):
    label = "2026-11-09-E067%s" % name
    build_dir = out_root / ("build-" + label)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    for sub in ("vendor/primary", "vendor/fallback", "weights", "LICENSES"):
        (build_dir / sub).mkdir(parents=True)
    if base.sha256(base.E041_MAIN) != base.E041_SHA256:
        raise ValueError("E041 main.py identity mismatch")
    if base.CHECKPOINT.stat().st_size != 110368038 or base.sha256(base.CHECKPOINT) != base.CHECKPOINT_SHA256:
        raise ValueError("Checkpoint identity mismatch")
    (build_dir / "main.py").write_text(render_main(plan, unhcr_fix, strict, budget, seeds, regate),
                                       encoding="utf-8")
    shutil.copy2(base.E041_MAIN, build_dir / "e041_core.py")
    base.copy_tree(base.TABICL_SRC / "src" / "tabicl", build_dir / "vendor" / "primary" / "tabicl")
    base.copy_tree(base.SITE / "einops", build_dir / "vendor" / "primary" / "einops")
    base.copy_tree(base.SITE / "tqdm", build_dir / "vendor" / "fallback" / "tqdm")
    shutil.copy2(base.CHECKPOINT, build_dir / "weights" / base.CHECKPOINT.name)
    shutil.copy2(base.TABICL_SRC / "LICENSE", build_dir / "LICENSES" / "tabicl-LICENSE")
    shutil.copy2(base.SITE / "einops-0.8.1.dist-info" / "licenses" / "LICENSE",
                 build_dir / "LICENSES" / "einops-LICENSE")
    shutil.copy2(base.SITE / "tqdm-4.67.1.dist-info" / "LICENCE", build_dir / "LICENSES" / "tqdm-LICENCE")
    shutil.copy2(base.KIT_LICENSE, build_dir / "LICENSES" / "starter-kit-LICENSE")
    (build_dir / "NOTICE.txt").write_text(base.NOTICE.replace("E065", "E067"), encoding="utf-8")
    files = sorted(p for p in build_dir.rglob("*") if p.is_file())
    zip_path = out_root / (label + ".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(build_dir).as_posix(), date_time=(2026, 11, 9, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(path, "rb") as fh:
                zf.writestr(info, fh.read())
    manifest = dict(name=name, plan=plan, unhcr_fix=unhcr_fix, seeds=list(seeds), regate=regate, strict=strict,
                    budget_seconds=budget,
                    zip=str(zip_path), zip_bytes=zip_path.stat().st_size, zip_sha256=base.sha256(zip_path),
                    main_sha256=base.sha256(build_dir / "main.py"),
                    e041_core_sha256=base.sha256(build_dir / "e041_core.py"), files=len(files))
    (out_root / (label + ".manifest.json")).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return build_dir, manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--plan", default="{}")
    parser.add_argument("--unhcr-fix", action="store_true")
    parser.add_argument("--no-strict", action="store_true")
    parser.add_argument("--budget", type=int, default=None)
    parser.add_argument("--seeds", default="0", help="comma-separated E041 network seeds")
    parser.add_argument("--regate", action="store_true", help="E068 data-checked re-gating (UNHCR)")
    parser.add_argument("--out", default=str(base.ROOT / "tmp" / "e067"))
    args = parser.parse_args()
    seeds = tuple(int(s) for s in args.seeds.split(","))
    plan = json.loads(args.plan)
    for key, value in plan.items():
        alpha = value["alpha"] if isinstance(value, dict) else value
        if key not in ("world_bank", "unicef", "unhcr") or not (alpha == "guard" or 0 <= float(alpha) <= 1):
            raise ValueError("bad plan entry %r: %r" % (key, value))
    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    build_dir, manifest = build(args.name, plan, args.unhcr_fix, not args.no_strict, args.budget, out_root,
                                seeds, args.regate)
    print(json.dumps(dict(build_dir=str(build_dir), **manifest), indent=2))


if __name__ == "__main__":
    main()
