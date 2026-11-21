# Reproduction map (not new authority)

Installed interpreter:
tmp/a040-modal-full-path1/sdk-venv/Scripts/python.exe
Supervisor: run_check.ps1; child: check_boundary.py.
All old attempts are immutable. The supervisor's original absolute work cutoff
is expired. Do not change it or rerun without a new authorized bounded scope.

Original C1 baseline evidence: c1-baseline-preflight/process/stderr and
attempts/c1-baseline/{trace.jsonl,check-result.json}.
Reduced failing invocation: -Case minimal_build (C2,C4,C5 records).
Clean control: -Case definition (C3); import_loop is an earlier clean control.
These use actual installed SDK, guarded fake external transport, no installers/
models/real service. Their tiny metadata is not output-array evidence.

Current script additionally has an UNEXECUTED protobuf_graph branch from C6.
It is not validated. Current sdk_endpoint.py lacks enable_output as the C5
negative diagnostic only; original bytes retained in sdk_endpoint.c5-before.txt.
Current boundary_transport.py omits await-chain observer as C4 diagnostic;
preceding bytes in boundary_transport.c4-before.txt. Neither removal is repair.
Current main source is not byte-identical to every historical preflight. Read
per-attempt hashes and registered change history, not just the latest manifest.

reduced() is the smallest completed failing scope in this session, not proof
of globally minimal reproduction or a particular native-library cause.
No successful full lifecycle or120s test was repeated.