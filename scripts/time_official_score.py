"""Execute untouched official score.py while observing build/run wall times."""

import hashlib
import json
from pathlib import Path
import runpy
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL = ROOT / "external/starter-kit/score.py"
OUTPUT = Path(sys.argv[1])
sys.argv = [str(OFFICIAL), *sys.argv[2:]]
sys.path.insert(0, str(OFFICIAL.parent))
times = {}
starts = {}


def observe(frame, event, argument):
    """Profile only entry/exit; no arguments, code or return values are changed."""
    name = frame.f_code.co_name
    if name not in ("prepare_environment", "run_submission"):
        return
    if Path(frame.f_code.co_filename).resolve() != OFFICIAL.resolve():
        return
    if event == "call":
        starts[name] = time.perf_counter()
    elif event == "return" and name in starts:
        times[name] = times.get(name, 0.) + time.perf_counter() - starts.pop(name)


sys.setprofile(observe)
try:
    runpy.run_path(str(OFFICIAL), run_name="__main__")
finally:
    sys.setprofile(None)
    OUTPUT.write_text(json.dumps({
        "official_score_sha256": hashlib.sha256(OFFICIAL.read_bytes()).hexdigest(),
        "seconds": times,
        "method": "sys.setprofile entry/return wall times; untouched official script. "
                  "run_submission includes child process launch, import, model load, "
                  "predict, output serialization and collection; excludes environment build.",
    }, indent=2) + "\n", encoding="utf-8")
