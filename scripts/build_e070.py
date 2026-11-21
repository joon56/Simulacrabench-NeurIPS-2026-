"""Assemble an E070 package (internally validated additions; heavy artifacts under submissions/ or tmp/).

python scripts/build_e070.py --name dev1 --seeds 0 \
    --candidates '{"world_bank": ["sent", "mix25", "mix50", "mix50+sent"], "unicef": ["mix25", "mix50"],
                   "unhcr": ["regate", "transfer", "regate+transfer"]}'
"""
import argparse
import json
import re
import shutil
import zipfile
from pathlib import Path

import build_e065 as base

SOURCE_MAIN = base.ROOT / "submissions" / "2026-11-10-E070" / "main.py"
PARTS = ("mix", "conf", "sent", "regate", "transfer", "temp", "stack", "xstack", "lpool", "xlpool", "cal", "tpool", "twin", "det")
EXTRA = {}


def render_main(candidates, seeds, strict, budget, source=SOURCE_MAIN):
    text = Path(source).read_text(encoding="utf-8")
    replacements = (
        (r"^SEEDS = .*$", "SEEDS = %r" % (({k: tuple(int(s) for s in v) for k, v in sorted(seeds.items())},) if isinstance(seeds, dict) else (tuple(int(s) for s in seeds),))),
        (r"^CANDIDATES = .*$", "CANDIDATES = %r" % {k: tuple(v) for k, v in sorted(candidates.items())}),
        (r"^STRICT = .*$", "STRICT = %s" % bool(strict)),
        (r"^BUDGET_SECONDS = .*$", "BUDGET_SECONDS = %s" % budget),
    )
    for pattern, value in replacements:
        text, n = re.subn(pattern, value, text, count=1, flags=re.M)
        if n != 1:
            raise ValueError("build marker missing: " + pattern)
    for pattern, value in EXTRA.items():  # E072+ probe switches, only when requested
        text, n = re.subn(pattern, value, text, count=1, flags=re.M)
        if n != 1:
            raise ValueError("build marker missing: " + pattern)
    return text


def build(name, candidates, seeds, strict, budget, out_root, source=SOURCE_MAIN, tag="2026-11-10-E070"):
    label = "%s%s" % (tag, name)
    build_dir = out_root / ("build-" + label)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    for sub in ("vendor/primary", "vendor/fallback", "weights", "LICENSES"):
        (build_dir / sub).mkdir(parents=True)
    if base.sha256(base.E041_MAIN) != base.E041_SHA256:
        raise ValueError("E041 main.py identity mismatch")
    if base.CHECKPOINT.stat().st_size != 110368038 or base.sha256(base.CHECKPOINT) != base.CHECKPOINT_SHA256:
        raise ValueError("Checkpoint identity mismatch")
    (build_dir / "main.py").write_text(render_main(candidates, seeds, strict, budget, source), encoding="utf-8")
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
    (build_dir / "NOTICE.txt").write_text(base.NOTICE.replace("E065", "E070"), encoding="utf-8")
    files = sorted(p for p in build_dir.rglob("*") if p.is_file())
    zip_path = out_root / (label + ".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(build_dir).as_posix(), date_time=(2026, 11, 10, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(path, "rb") as fh:
                zf.writestr(info, fh.read())
    manifest = dict(name=name, candidates=candidates, seeds=seeds if isinstance(seeds, dict) else list(seeds), strict=strict, budget_seconds=budget,
                    zip=str(zip_path), zip_bytes=zip_path.stat().st_size, zip_sha256=base.sha256(zip_path),
                    main_sha256=base.sha256(build_dir / "main.py"),
                    e041_core_sha256=base.sha256(build_dir / "e041_core.py"), files=len(files))
    (out_root / (label + ".manifest.json")).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return build_dir, manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--candidates", default="{}")
    parser.add_argument("--seeds", default="0")
    parser.add_argument("--no-strict", action="store_true")
    parser.add_argument("--budget", type=int, default=None)
    parser.add_argument("--out", default=str(base.ROOT / "tmp" / "e070"))
    parser.add_argument("--source", default=str(SOURCE_MAIN))
    parser.add_argument("--tag", default="2026-11-10-E070")
    parser.add_argument("--direct", default=None, help="JSON instrument -> chain (E072+)")
    parser.add_argument("--no-e-check", default=None, help="comma-separated instruments (E072+)")
    parser.add_argument("--estimators", type=int, default=None, help="TabICL n_estimators (E072+)")
    parser.add_argument("--xstack-kinds", default=None, help="comma-separated expert kinds for xstack (E073+)")
    parser.add_argument("--base-trees", default=None, help="JSON instrument -> tree weight inside E041's base (E073+)")
    parser.add_argument("--base-folds", type=int, default=None, help="out-of-fold splits for base trees (E073+)")
    parser.add_argument("--hgb", default=None, help="JSON tree-parameter override (E075+)")
    parser.add_argument("--ez", type=float, default=None, help="one-sided z of the E-row confirmation (E076+)")
    parser.add_argument("--xstack-by", default=None, help="JSON instrument -> expert kinds for x-chains (E076+)")
    args = parser.parse_args()
    candidates = json.loads(args.candidates)
    for key, chains in candidates.items():
        if key not in ("world_bank", "unicef", "unhcr"):
            raise ValueError("bad instrument " + key)
        for chain in chains:
            for part in chain.split("+"):
                op = part[1:] if part[:1] in ("g", "n", "m", "r", "q") and part[1:].startswith(("mix", "conf", "stack", "sent", "lpool")) else part
                if not op.startswith(PARTS):
                    raise ValueError("bad transform " + part)
    if args.direct is not None:
        EXTRA[r"^DIRECT = .*$"] = "DIRECT = %r" % dict(sorted(json.loads(args.direct).items()))
    if args.no_e_check is not None:
        EXTRA[r"^NO_E_CHECK = .*$"] = "NO_E_CHECK = %r" % (tuple(s for s in args.no_e_check.split(",") if s),)
    if args.ez is not None:
        EXTRA[r"^E_Z = .*$"] = "E_Z = %r" % float(args.ez)
    if args.xstack_by is not None:
        EXTRA[r"^XSTACK_BY = .*$"] = "XSTACK_BY = %r" % {k: tuple(v) for k, v in sorted(json.loads(args.xstack_by).items())}
    if args.hgb is not None:
        EXTRA[r"^HGB_OVERRIDE = .*$"] = "HGB_OVERRIDE = %r" % dict(sorted(json.loads(args.hgb).items()))
    if args.base_folds is not None:
        EXTRA[r"^BASE_FOLDS = .*$"] = "BASE_FOLDS = %d" % args.base_folds
    if args.base_trees is not None:
        EXTRA[r"^BASE_TREES = .*$"] = "BASE_TREES = %r" % dict(sorted(json.loads(args.base_trees).items()))
    if args.xstack_kinds is not None:
        EXTRA[r"^XSTACK_KINDS = .*$"] = "XSTACK_KINDS = %r" % (tuple(s for s in args.xstack_kinds.split(",") if s),)
    if args.estimators is not None:
        EXTRA[r"^EXPERT_ESTIMATORS = .*$"] = "EXPERT_ESTIMATORS = %d" % args.estimators
    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    seeds = json.loads(args.seeds) if args.seeds.strip().startswith("{") else tuple(int(s) for s in args.seeds.split(","))
    build_dir, manifest = build(args.name, candidates, seeds, not args.no_strict, args.budget, out_root,
                                args.source, args.tag)
    print(json.dumps(dict(build_dir=str(build_dir), **manifest), indent=2))


if __name__ == "__main__":
    main()
