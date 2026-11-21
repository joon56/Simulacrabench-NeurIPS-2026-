"""Future Linux single-mode900s watchdog, unchanged scientific runner policy."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CAP = 15999172608


def sample_tree(pid):
    # Process-group ownership and /proc private/RSS; never Windows commitment.
    rss = private = 0
    pids = []
    for directory in Path("/proc").iterdir():
        if not directory.name.isdigit():
            continue
        candidate = int(directory.name)
        try:
            if candidate != os.getpid() and os.getpgid(candidate) != pid:
                continue
            values = {}
            for line in (directory / "smaps_rollup").read_text().splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    if value.strip().endswith("kB"):
                        values[key] = int(value.split()[0])*1024
            rss += values.get("Rss", 0)
            private += values.get("Private_Clean", 0)+values.get("Private_Dirty", 0)
            pids.append(candidate)
        except (ProcessLookupError, FileNotFoundError):
            continue
    return {"rss": rss, "private_bytes": private, "pids": pids,
            "cgroup_current": int(Path("/sys/fs/cgroup/memory.current").read_text())}


def main(mode):
    if sys.platform != "linux" or mode not in ("reference", "candidate"):
        raise PermissionError("Linux named mode only")
    config = json.loads((HERE / "target-contract.json").read_text())
    boundary = json.loads((HERE / "boundary-result.json").read_text())
    if config["scope"] != "LIVE" or boundary.get("outcome") != "BOUNDARY_PASS":
        raise PermissionError("Actual target boundary required")
    if config["gpu_deadline"]-time.time() < (1900 if mode == "reference" else 950):
        raise TimeoutError("Insufficient entire fixed mode window")
    if mode == "candidate":
        ref = json.loads((HERE / "reference/resources.json").read_text())
        if ref["outcome"] != "REFERENCE_PASS" or ref["child_exit"] != 0:
            raise PermissionError("Reference gate failed")
    out = HERE / mode
    out.mkdir(exist_ok=True)
    with (out / "scientific-started.json").open("x") as stream:
        json.dump({"mode": mode, "cap_seconds": 900}, stream)
        stream.flush()
        os.fsync(stream.fileno())
    target = ROOT / "tmp/a040-modal-local-integration1" / mode
    target.mkdir(parents=True, exist_ok=True)
    affinity = sorted(os.sched_getaffinity(0))[:2]
    if len(affinity) != 2:
        raise RuntimeError("Two logical CPUs unavailable")
    os.sched_setaffinity(0, affinity)
    # Explicit environment, no inherited SDK/account/token variables in science.
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "HOME": "/tmp/a040-empty-home",
           "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2", "OPENBLAS_NUM_THREADS": "2",
           "NUMEXPR_NUM_THREADS": "2", "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"}
    started = time.monotonic()
    reason = None
    samples = []
    with (out / "stdout.txt").open("xb") as stdout, (out / "stderr.txt").open("xb") as stderr:
        child = subprocess.Popen([sys.executable, "-I", "-B", "-u", str(HERE / "linux_runner.py"), mode],
                                 cwd=ROOT, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
        try:
            while child.poll() is None:
                elapsed = time.monotonic()-started
                row = dict(elapsed=elapsed, **sample_tree(child.pid))
                samples.append(row)
                with (out / "resource-samples.jsonl").open("a") as stream:
                    stream.write(json.dumps(row)+"\n")
                if elapsed >= 900 or time.time() >= config["gpu_deadline"]-60:
                    reason = "Scientific process time cap"
                    break
                if max(row["rss"], row["private_bytes"], row["cgroup_current"]) > CAP:
                    reason = "Linux memory cap"
                    break
                time.sleep(min(1, max(.001, 900-elapsed)))
        except BaseException as exc:
            reason = "Measurement/controller failure: " + repr(exc)
        finally:
            if reason and child.poll() is None:
                os.killpg(child.pid, signal.SIGKILL)
            child.wait(timeout=10)
    elapsed = time.monotonic()-started
    result = json.loads((out / "result.json").read_text()) if (out / "result.json").exists() else {}
    outcome = result.get("outcome", "INCOMPLETE")
    if reason or elapsed > 900:
        outcome = "LOCAL_RESOURCE_LIMIT"
    record = {"mode": mode, "outcome": outcome, "child_exit": child.returncode, "elapsed_seconds": elapsed,
              "reason": reason, "sample_count": len(samples), "sample_interval_seconds": 1,
              "rss_peak_sampled": max((r["rss"] for r in samples), default=0),
              "private_peak_sampled": max((r["private_bytes"] for r in samples), default=0),
              "cgroup_peak_sampled": max((r["cgroup_current"] for r in samples), default=0),
              "memory_cap": CAP, "measurement": "Linux private/RSS/cgroup; not Windows commitment",
              "includes_controller": True, "affinity": affinity}
    (out / "resources.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps(record))
    return 0 if outcome in ("REFERENCE_PASS", "LOCAL_FULL_PATH_PASS") and child.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
