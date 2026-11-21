"""Actual UTF-8 local launcher and hard process deadline. Fake worker only."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def launch(scenario, output, mode="pipe", timeout=3):
    output = Path(output)
    output.mkdir()  # Exclusive output directory; no latch overwrite/reuse.
    env = os.environ.copy()
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1",
               OMP_NUM_THREADS="2", MKL_NUM_THREADS="2")
    command = [sys.executable, "-X", "utf8", "-u", str(Path(__file__).with_name("fake_worker.py")),
               scenario, str(output)]
    started = time.monotonic()
    files = []
    if mode == "file":
        files = [(output / name).open("xb") for name in ("stdout.bin", "stderr.bin")]
        destinations = files
    else:
        destinations = [subprocess.PIPE, subprocess.PIPE]
    proc = subprocess.Popen(command, env=env, stdout=destinations[0], stderr=destinations[1],
                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    timed_out = False
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        proc.kill()  # Worker audit guard prohibits grandchildren; own PID only.
        stdout, stderr = proc.communicate(timeout=2)
    finally:
        for stream in files:
            stream.close()
    if mode == "pipe":
        (output / "stdout.bin").write_bytes(stdout)
        (output / "stderr.bin").write_bytes(stderr)
    receipt = {"pid": proc.pid, "returncode": proc.returncode, "watchdog_timeout": timed_out,
               "wall_seconds": time.monotonic()-started, "mode": mode,
               "remote_termination_claim": False, "command": command,
               "utf8_env": {key: env[key] for key in ("PYTHONUTF8", "PYTHONIOENCODING")}}
    if timed_out:
        # A partial journal is evidence of intent/known ID only, never termination.
        journal = output / "result.json"
        receipt["partial_journal"] = json.loads(journal.read_text(encoding="utf-8")) if journal.exists() else None
        receipt["termination"] = "UNCONFIRMED_WATCHDOG"
    (output / "launcher.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    return receipt
