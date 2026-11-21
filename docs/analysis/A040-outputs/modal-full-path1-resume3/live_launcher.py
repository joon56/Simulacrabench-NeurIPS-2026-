"""Single live worker, UTF-8 binary logs, bounded own-tree parent watchdog."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
entry = json.loads((HERE / "entry.json").read_text(encoding="utf-8-sig"))
deadline = datetime.fromisoformat(entry["whole_deadline_utc"].replace("Z", "+00:00")).timestamp()
env = os.environ.copy()  # Local normal SDK auth only; never forwarded to science.
env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
started = time.monotonic()
with (HERE / "launcher-started.json").open("x", encoding="utf-8") as stream:
    json.dump({"utc": datetime.now(timezone.utc).isoformat(), "pid": os.getpid(), "worker_invocations": 1}, stream)
with (HERE / "live-stdout.txt").open("xb") as stdout, (HERE / "live-stderr.txt").open("xb") as stderr:
    child = subprocess.Popen([sys.executable, "-X", "utf8", "-u", str(HERE / "live_worker.py")],
                             stdout=stdout, stderr=stderr, env=env,
                             creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    (HERE / "owned-local-worker.json").write_text(json.dumps({"pid": child.pid,
        "parent_pid": os.getpid(), "helpers": "Worker audit denies subprocess spawn; launcher owns venv interpreter tree"}), encoding="utf-8")
    timed_out = False
    try:
        child.wait(timeout=max(1, deadline-time.time()-15))
    except subprocess.TimeoutExpired:
        timed_out = True
        # Only the PID returned by this Popen and its descendants; never search/kill others.
        subprocess.run(["taskkill", "/PID", str(child.pid), "/T", "/F"], timeout=10,
                       stdout=stderr, stderr=stderr, check=False,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        child.wait(timeout=5)
receipt = {"child_pid": child.pid, "returncode": child.returncode, "watchdog_timeout": timed_out,
           "wall_seconds": time.monotonic()-started, "remote_termination_claim": False,
           "known_ids": "live-state.json", "cleanup_only_required_if_unconfirmed": True}
(HERE / "launcher-result.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
print(json.dumps(receipt))
sys.exit(child.returncode or int(timed_out))
