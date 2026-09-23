"""Freeze local build constraints without modifying the baseline environment."""

import importlib.metadata
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
versions = {item.metadata["Name"]: item.version
            for item in importlib.metadata.distributions()}
record = json.loads((ROOT / "docs/analysis/E048-outputs/oracle-seed49.json").read_text(encoding="utf-8"))
versions.update(record["dependencies"]["versions"])
path = ROOT / "docs/analysis/E049-outputs/local-validation-constraints.txt"
path.write_text("".join(f"{name}=={version}\n" for name, version in sorted(versions.items())),
                encoding="utf-8")
print(path)
