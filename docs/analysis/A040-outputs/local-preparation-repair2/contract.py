"""Fixed A040 execution contract and pre-RPC complete-source gate."""
import ast
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import time

MODULES = ("contract.py", "protocol.py", "controller_core.py", "live_binding.py",
           "sdk_endpoint.py", "payload.py", "sandbox_stage.py", "linux_boundary.py",
           "linux_watchdog.py", "linux_runner.py", "live_worker.py", "live_launcher.py")
REMOTE_DIR = "/work/docs/analysis/A040-outputs/local-preparation-repair2"
CAP_BYTES = 15258 * 1024 * 1024
GPU_PLAN = 2.965933453125


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_relative(name):
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name:
        raise ValueError("Unsafe relative path")
    return path


def verify_sources(directory, manifest):
    indexed = {row["path"]: row for row in manifest["files"]}
    if len(indexed) != len(manifest["files"]) or set(indexed) != set(MODULES):
        raise ValueError("Incomplete or duplicate source closure")
    for name in MODULES:
        raw = (Path(directory) / name).read_bytes()
        if sha(raw) != indexed[name]["sha256"]:
            raise ValueError("Source identity mismatch: " + name)
        tree = ast.parse(raw.decode("utf-8-sig"), filename=name)
        for node in ast.walk(tree):
            if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name):
                if node.exc.func.id == "NotImplementedError":
                    raise ValueError("Placeholder source: " + name)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                body = [n for n in node.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str))]
                if len(body) == 1 and (isinstance(body[0], ast.Pass) or (isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and body[0].value.value is Ellipsis)):
                    raise ValueError("Placeholder function: " + name)
    return {"source_complete": True, "modules": len(MODULES), "manifest_sha256": sha(json.dumps(manifest, sort_keys=True).encode())}


@dataclass(frozen=True)
class Plan:
    scope: str
    app_name: str
    base_id: str
    base_result_sha256: str
    prepare_deadline: float
    gpu_latest_end: float
    whole_deadline: float
    execution_authorized: bool = False
    operation_timeout: float = 30
    build_timeout: float = 900
    cleanup_timeout: float = 60
    cancel_grace: float = 2
    poll_seconds: float = 2

    def check(self):
        if self.scope not in ("LOCAL_PROTOCOL_FIXTURE", "LIVE"):
            raise ValueError("Unknown execution scope")
        if self.scope == "LIVE" and not self.execution_authorized:
            raise PermissionError("Fresh remote authorization required")
        if not self.prepare_deadline < self.gpu_latest_end < self.whole_deadline:
            raise ValueError("Invalid stage deadlines")
        if self.whole_deadline-time.time() <= 75:
            raise TimeoutError("Expired whole deadline")
        if not self.app_name or not self.base_id or len(self.base_result_sha256) != 64:
            raise ValueError("Missing explicit identity")
        if self.scope == "LIVE" and (self.operation_timeout < 10 or self.build_timeout != 900 or self.cleanup_timeout != 60):
            raise ValueError("Test-scaled timeouts cannot enter live execution")

    def require_time(self, seconds, stage="prepare"):
        end = self.prepare_deadline if stage == "prepare" else self.gpu_latest_end
        if end-time.time() < seconds:
            raise TimeoutError("Insufficient entire next-stage time: " + stage)


class Costs:
    def __init__(self):
        self.posted = .00001152
        self.prepare_started = None
        self.gpu_started = None
    def observe(self, summary):
        if float(summary.billed_cost) != 0:
            raise RuntimeError("Cash billing contradiction")
        self.posted = max(self.posted, float(summary.metered_cost),
                          sum(max(0, float(v)) for v in summary.metered_cost_breakdown.values()))
    def value(self):
        prep = max(0, time.monotonic()-self.prepare_started) if self.prepare_started else 0
        gpu = max(0, time.monotonic()-self.gpu_started) if self.gpu_started else 0
        return max(self.posted, .00001152+.65+prep*(.0000131+8*.00000222)+gpu*.00123580560546875)
    def gate(self, next_plan=0):
        value = self.value()
        if value+next_plan >= 4:
            raise RuntimeError("Cumulative cost planning gate")
        return {"management": value, "next_plan": next_plan, "threshold": 4,
                "observed_invoice": False, "unknown_prior_posting": True}
