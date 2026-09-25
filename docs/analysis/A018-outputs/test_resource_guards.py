"""Small real-process tests: no model fit and no survey/proxy data access."""
import ctypes
from ctypes import wintypes
import importlib.util
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("release", HERE / "verify_release.py")
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


def test_exhausted_budget_refuses_even_to_launch():
    try:
        release.run_with_tree_timeout(["deliberately-nonexistent-command"], timeout=0)
    except subprocess.TimeoutExpired:
        pass
    else:
        raise AssertionError("Exhausted budget must refuse launch")


def test_memory_watchdog_stops_a_live_worker_before_completion():
    program = (
        "import sys,time; sys.path.insert(0,sys.argv[1]); import verify_release as v; "
        "v.start_memory_watchdog(limit_bytes=1, interval=.02); time.sleep(30)"
    )
    start = time.monotonic()
    done = subprocess.run([sys.executable, "-c", program, str(HERE)], timeout=4)
    assert done.returncode == 125
    assert time.monotonic() - start < 4


def test_timeout_stops_owned_child_tree(tmp_path):
    child_pid = tmp_path / "child.pid"
    program = (
        "import pathlib,subprocess,sys,time; "
        "p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)']); "
        "pathlib.Path(sys.argv[1]).write_text(str(p.pid)); time.sleep(30)"
    )
    try:
        release.run_with_tree_timeout([sys.executable, "-c", program, str(child_pid)], timeout=2)
    except subprocess.TimeoutExpired:
        pass
    else:
        raise AssertionError("Timeout was not enforced")
    pid = int(child_pid.read_text())
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.GetExitCodeProcess.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    handle = kernel.OpenProcess(0x1000, False, pid)
    if handle:
        code = wintypes.DWORD()
        assert kernel.GetExitCodeProcess(handle, ctypes.byref(code))
        kernel.CloseHandle(handle)
        assert code.value != 259, "Owned grandchild still running"
    else:
        assert ctypes.get_last_error() == 87, "Unexpected process-query error"
