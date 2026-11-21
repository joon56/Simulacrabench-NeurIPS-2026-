"""Focused local regression, sequential workers, all transport fake."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import time

from launcher import launch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
started = time.monotonic()
out = Path(sys.argv[1])
out.mkdir()
rows = []

# Installer AST and source bytes (normalized line endings) remain unchanged.
old = (HERE.parent / "modal-full-path1-resume2/build_once.py").read_text(encoding="utf-8")
new = (HERE / "controller.py").read_text(encoding="utf-8-sig")
def installer(text):
    node = next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == "install_pins")
    return ast.get_source_segment(text, node)
assert installer(old) == installer(new)

cases = [("success", "pipe"), ("success", "file"), ("unicode_error", "pipe"), ("unicode_error", "file")]
cases += [(x, "pipe") for x in ("cancel_resistant", "stop_timeout", "stop_failure", "ack_running",
           "terminal_tasks", "terminal_zero", "create_lost", "construct_error", "prepare_error", "query_timeout", "blocked_loop")]
for index, (scenario, mode) in enumerate(cases):
    assert time.monotonic()-started < 40
    directory = out / f"{index:02d}-{scenario}-{mode}"
    receipt = launch(scenario, directory, mode, timeout=1 if scenario == "blocked_loop" else 3)
    row = {"scenario": scenario, "mode": mode, "launcher": receipt}
    if scenario == "blocked_loop":
        assert receipt["watchdog_timeout"] and receipt["termination"] == "UNCONFIRMED_WATCHDOG"
        partial = receipt["partial_journal"]
        assert partial["owned_app_id"] == "ap-FAKE-OWNED" and partial["build_attempts"] == 1
        assert receipt["wall_seconds"] < 3
        row["passed"] = True
        rows.append(row)
        continue
    assert not receipt["watchdog_timeout"], row
    result = json.loads((directory / "result.json").read_text(encoding="utf-8"))
    audit = json.loads((directory / "worker-audit.json").read_text(encoding="utf-8"))
    assert audit["blocked_operations"] == [] and audit["live_rpc_calls"] == 0
    assert not audit["sdk_imported"] and not audit["model_imported"]
    assert audit["stdout_encoding"] == audit["stderr_encoding"] == "utf-8"
    counts = {name: sum(c["call"] == name for c in audit["fake_calls"])
              for name in ("App.lookup", "Image.build", "AppStop", "AppGetInfo", "TaskList")}
    assert all(value <= 1 for value in counts.values()), counts
    assert result["cleanup_seconds"] < 0.5
    if scenario in {"success", "unicode_error", "terminal_zero"}:
        stdout = (directory / "stdout.bin").read_bytes().decode("utf-8", errors="strict")
        stderr = (directory / "stderr.bin").read_bytes().decode("utf-8", errors="strict")
        assert "• 한글 로그 stdout" in stdout and "• 한글 로그 stderr" in stderr
    if scenario == "unicode_error":
        assert "retained exception • 한글" in result["traceback"] and "retained exception • 한글" in stderr
        assert receipt["returncode"] == 2
    if scenario in {"stop_timeout", "stop_failure", "ack_running", "terminal_tasks", "query_timeout"}:
        assert result["termination"] == "UNCONFIRMED"
    elif scenario == "create_lost":
        assert result["termination"] == "ID_UNKNOWN" and result["owned_app_id"] is None
        assert counts["App.lookup"] == 1 and counts["Image.build"] == counts["AppStop"] == 0
    elif scenario == "prepare_error":
        assert result["termination"] == "NO_CREATE_ATTEMPT" and sum(counts.values()) == 0
    else:
        assert result["termination"] == "TERMINAL_TASK0_CONFIRMED"
    if scenario == "construct_error":
        assert counts["AppStop"] == 1 and counts["Image.build"] == 0
    if scenario == "cancel_resistant":
        assert result["outcome"] == "BUILD_FAILED" and audit["pending_tasks_at_exit"] >= 1
    if scenario == "ack_running":
        assert result["stop_ack"] is True
    row.update(passed=True, result=result, audit=audit, counts=counts)
    rows.append(row)
report = {"passed": True, "cases": rows, "case_count": len(rows), "seconds": time.monotonic()-started,
          "installer_source_equal": True, "remote_calls": 0, "sdk_imports": 0, "scientific_runs": 0}
(out / "regression.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({key: value for key, value in report.items() if key != "cases"}))
