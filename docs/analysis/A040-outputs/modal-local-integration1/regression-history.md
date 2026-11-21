# Focused regression history

Two cycles,8.5363744s cumulative outer process wall (limit180s/max3).
Cycle1:2.7751595s outer /2.4243631s internal, exit1. Cycle2:5.7612149s outer /
5.3821113s internal, exit0. No timeout. No third or unchanged successful rerun.

Cycle1 completed20 checks including the normal production orchestration path.
The Sandbox ID-loss recovery assertion failed: installed SDK1.6.0 defaults to V2
name lookup, which requires the client's `_auth_token_manager` interface. The
injected client omitted it. Cleanup remained UNCONFIRMED, and the worker did not
claim PASS. No forbidden endpoint was attempted; the injected client failed on
attribute access before any real credential discovery.

After inspecting `sandbox.py:1386` and `config.py:366`, only the test endpoint was
completed: `TokenEndpoint.get_token()` returns a literal noncredential marker,
and `SandboxGetFromNameV2` verifies that marker and the actual protobuf request.
Production source/manifest did not change between cycles. No fictitious protobuf
constant was introduced; no SDK configuration was changed to bypass default V2.

Cycle2 passed39 cases. The previous15-case controller suite and successful
scientific/schema fixtures were not repeated. This suite exercises the newly
connected orchestration, real message handling, order, gates, export and cleanup.

Preserved raw artifacts: [cycle1 result](regression/cycle1-result.json),
[cycle2 result](regression/cycle2-result.json), their outer receipts/stdout/stderr.
Exact failed/final source snapshots and per-case detailed artifacts remain at
`tmp/a040-modal-local-integration1/cycle1-source`, `cycle2-source`, `cycle1`, `cycle2`.
The snapshots are not executable retry authorization. Test source hashes and
snapshot identity are recorded in the contract/artifact manifests.

Reproduction command, only within a fresh explicitly authorized local regression
scope and a new empty output path:

```powershell
& '.\tmp\a040-modal-full-path1\sdk-venv\Scripts\python.exe' -X utf8 -B `
  '.\docs\analysis\A040-outputs\modal-local-integration1\tests_integration.py' `
  '.\tmp\a040-modal-local-integration1\NEW_AUTHORIZED_CYCLE'
```

The executed commands used a hidden PowerShell Start-Process wrapper, redirected
UTF-8 stdout/stderr, a60s outer limit and an explicit exit-code/process-time receipt.
No package installation, fixture regeneration, scientific command or remote CLI
was part of these commands. The old remote latches/deadlines remain unchanged.
