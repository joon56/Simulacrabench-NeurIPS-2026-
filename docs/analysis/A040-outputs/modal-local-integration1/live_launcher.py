"""Future explicit-authority launcher; never an entry point for local regression."""
import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from contract import Plan, MODULES, verify_sources, sha


def load_contract(path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    plan = Plan(**config["plan"])
    plan.check()
    if plan.scope != "LIVE":
        raise PermissionError("CLI is reserved for a fresh authorized LIVE session")
    manifest = json.loads((HERE / "source-manifest.json").read_text(encoding="utf-8"))
    if sha((HERE / "source-manifest.json").read_bytes()) != config["source_manifest_sha256"]:
        raise ValueError("External source-freeze identity mismatch")
    verify_sources(HERE, manifest)
    prefix = "docs/analysis/A040-outputs/modal-local-integration1/"
    additions = {row["path"]: row for row in config["extra_files"]}
    if len(additions) != len(config["extra_files"]) or set(additions) != {prefix + name for name in MODULES}:
        raise ValueError("Complete transferred port/source closure required")
    for row in manifest["files"]:
        extra = additions[prefix + row["path"]]
        if extra["sha256"] != row["sha256"] or extra["bytes"] != (HERE / row["path"]).stat().st_size or not extra.get("reason"):
            raise ValueError("Transferred port/source identity mismatch")
    return config, plan, manifest


def child(config_path):
    # SDK import alone is permitted, authentication only after all local gates.
    config, plan, manifest = load_contract(config_path)
    from payload import Payload, FileReader
    from sdk_endpoint import Endpoint
    from live_worker import Context, run, cleanup
    import asyncio
    allow_bytes = Path(config["allowlist_path"]).read_bytes()
    if sha(allow_bytes) != config["allowlist_sha256"]:
        raise ValueError("Original allowlist identity mismatch")
    original = json.loads(allow_bytes)["files"]
    extra = config["extra_files"]
    pins = Path(config["pins_path"]).read_bytes()
    if sha(pins) != "6c6f0d0fc5db943eb1cb95ff4610ddea5df724bc50031b883a0dd67656771b70":
        raise ValueError("Fixed pins mismatch")
    payload = Payload(original, extra,
        FileReader(config["staging_root"], [r["path"] for r in original], plan),
        FileReader(config["extra_root"], [r["path"] for r in extra], plan), plan.scope)
    context = Context(config["output_directory"], plan, Endpoint(), payload, pins.decode("utf-8-sig"))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(run(context, manifest, HERE))
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0 if result["outcome"] == "H100_FULL_PATH_PASS" else 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("contract")
    parser.add_argument("--child", action="store_true")
    args = parser.parse_args()
    if args.child:
        child(args.contract)
    config, plan, _ = load_contract(args.contract)
    # Parent never extends the contract. Exact child ownership, bounded wait.
    receipt_dir = Path(config["launcher_directory"])
    receipt_dir.mkdir(parents=True, exist_ok=False)
    with (receipt_dir / "launcher-started.json").open("x", encoding="utf-8") as stream:
        json.dump(asdict(plan), stream)
        stream.flush()
        os.fsync(stream.fileno())
    with (receipt_dir / "stdout.txt").open("xb") as stdout, (receipt_dir / "stderr.txt").open("xb") as stderr:
        process = subprocess.Popen([sys.executable, "-X", "utf8", "-B", str(HERE / "live_launcher.py"), args.contract, "--child"],
                                   stdout=stdout, stderr=stderr, cwd=HERE)
        try:
            code = process.wait(timeout=max(1, plan.whole_deadline-time.time()+15))
        except subprocess.TimeoutExpired:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], timeout=10, check=False,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                process.kill()
            code = process.wait(timeout=10)
            (receipt_dir / "forced-stop.json").write_text(json.dumps({"pid": process.pid,
                "remote_termination": "UNCONFIRMED", "reason": "Parent absolute deadline"}), encoding="utf-8")
    (receipt_dir / "exit.json").write_text(json.dumps({"exit_code": code}), encoding="utf-8")
    return code


if __name__ == "__main__":
    sys.exit(main())
