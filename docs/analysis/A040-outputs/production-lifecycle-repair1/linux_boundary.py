"""Future model-free Linux target boundary. Never executed by local regression."""
import ctypes
import errno
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CAP = 15999172608


def cgroup_limits():
    # Unknown/nonvisible cgroup enforcement is a blocker, never silently guessed.
    root = Path("/sys/fs/cgroup")
    cpu = (root / "cpu.max").read_text().split()
    if cpu[0] == "max":
        raise RuntimeError("CPU hard limit unverified")
    quota = int(cpu[0]) / int(cpu[1])
    memory = int((root / "memory.max").read_text().strip())
    swap = int((root / "memory.swap.max").read_text().strip())
    # Modal bills/limits physical cores; Linux quota is logical CPU equivalents.
    if quota != 2 or memory != CAP or swap != 0:
        raise RuntimeError("Target cgroup contract mismatch")
    return {"physical_cpu_limit": quota/2, "memory_limit_bytes": memory,
            "logical_cpu_quota": quota, "swap_disabled": swap == 0,
            "cgroup_memory_current": int((root / "memory.current").read_text())}


def native_network_probe():
    # libc syscall path, independent of Python socket monkeypatches.
    libc = ctypes.CDLL(None, use_errno=True)
    class Address(ctypes.Structure):
        _fields_ = [("family", ctypes.c_ushort), ("port", ctypes.c_ushort),
                    ("address", ctypes.c_ubyte * 4), ("pad", ctypes.c_ubyte * 8)]
    fd = libc.socket(2, 1 | 2048, 0)  # AF_INET, SOCK_STREAM|SOCK_NONBLOCK
    if fd < 0:
        if ctypes.get_errno() in (errno.EPERM, errno.EACCES, errno.ENETUNREACH):
            return True
        raise RuntimeError("Native socket probe unavailable")
    address = Address(2, 0xBB01, (ctypes.c_ubyte*4)(1, 1, 1, 1), (ctypes.c_ubyte*8)())
    try:
        status = libc.connect(fd, ctypes.byref(address), ctypes.sizeof(address))
        code = ctypes.get_errno()
        if status == -1 and code in (errno.EPERM, errno.EACCES, errno.ENETUNREACH, errno.EHOSTUNREACH):
            return True
        # EINPROGRESS/timeout/refused is not proof of native outbound denial.
        raise RuntimeError("Native network denial not established: " + str(code))
    finally:
        libc.close(fd)


def main():
    if sys.platform != "linux":
        raise RuntimeError("Actual target must be Linux")
    config = json.loads((HERE / "target-contract.json").read_text())
    if config["scope"] != "LIVE":
        raise PermissionError("Protocol fixture must never execute boundary")
    (HERE / "boundary-started.json").open("x").close()
    for row in config["files"]:
        path = (ROOT / row["path"]).resolve()
        if ROOT not in path.parents or hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            raise RuntimeError("Transferred source/payload mismatch")
    result = cgroup_limits()
    available = sorted(os.sched_getaffinity(0))
    if len(available) < 2:
        raise RuntimeError("Two logical CPUs unavailable")
    os.sched_setaffinity(0, available[:2])
    result["two_logical_affinity"] = len(os.sched_getaffinity(0)) == 2
    if sys.version_info[:3] != (3, 13, 14):
        raise RuntimeError("Pinned Python mismatch")
    for line in config["pins"].splitlines():
        if line.strip():
            name, version = line.strip().split("==")
            if importlib.metadata.version(name) != version:
                raise RuntimeError("Pinned dependency mismatch: " + name)
    # No CUDA/torch import; query driver/hardware via system utility.
    query = subprocess.run(["nvidia-smi", "--query-gpu=name,uuid,driver_version,memory.total", "--format=csv,noheader"],
                           capture_output=True, text=True, check=True, timeout=10)
    rows = [line for line in query.stdout.splitlines() if line.strip()]
    if len(rows) != 1 or "H100" not in rows[0]:
        raise RuntimeError("Single H100 identity not established")
    result["gpu_identity"] = rows
    result["native_network_blocked"] = native_network_probe()
    probe = HERE / "duplicate-probe.latch"
    probe.open("x").close()
    try:
        probe.open("x").close()
    except FileExistsError:
        duplicate = True
    else:
        raise RuntimeError("Exclusive latch not enforced")
    # Record all installed distribution metadata, without importing model packages.
    inventory = sorted((d.metadata["Name"], d.version) for d in importlib.metadata.distributions())
    (HERE / "linux-requirements.json").write_text(json.dumps(inventory), encoding="utf-8")
    result.update(outcome="BOUNDARY_PASS", source_payload_verified=True, gpu_h100_single=True,
                  python_pins_match=True, duplicate_latch_guard=duplicate, platform=sys.platform,
                  measurement="Linux cgroup and /proc, not Windows private commitment")
    return result


if __name__ == "__main__":
    try:
        value = main()
    except BaseException as exc:
        value = {"outcome": "BOUNDARY_FAIL", "error": repr(exc)}
    (HERE / "boundary-result.json").write_text(json.dumps(value, indent=2), encoding="utf-8")
    print(json.dumps(value))
    sys.exit(0 if value["outcome"] == "BOUNDARY_PASS" else 1)
