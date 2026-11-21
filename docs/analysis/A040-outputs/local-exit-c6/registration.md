# C6 single measurement, frozen before invocation

Scope: user-delivered S1-A040-C6. Conservative entry2026-10-26 21:22KST;
compute cutoff21:47, closeout deadline21:52. No extension or old allowance reuse.
One valid protobuf_graph measurement; at most3 diagnostic/impact starts and90s
supervised total, each30s including cleanup. Execution cutoff25s, remaining5s for
owned-tree cleanup/reaping. CPU affinity3(two logical CPUs), GPU0, cash0;
sampled owned supervisor+descendant RSS/private each2GiB. No C1-C5 replay.

C3 comparison identity is not inferred from latest source. Removing the C6-only
graph block and case selectors reconstructs check_boundary.py exactly to C3's
ad09dfec45b528a069849aa37e1748ec5987e891f7ba77fccc4b6d9e358ca196.
Reinstating the preserved endpoint row reconstructs the full C3 source manifest
07a5e5076625f59b69d89a91dfc4a27cfbc5b68abf7adf11efb25721328c8d50.
Boundary/endpoint C3 bytes are taken from preserved c4-before/c5-before snapshots;
no old file is restored/modified. Direct dependency hashes match that C3 manifest.
Source.diff identifies C6 argument restriction, new work path and parser-entry
observation; supervisor.diff separately identifies timing/process/resource changes.

Same recorded Python3.13.14/Modal1.6.0/synchronicity0.12.5/protobuf6.33.6/
grpclib0.4.9 and installed venv path. Current20 direct environment files are frozen.
Historical full interpreter/native binary hashes are absent: version/path/source
correspondence, not an invented retrospective complete binary identity. No known
version change, reinstall or source modification; installed files remain read-only.

Guard/fixture reuse: local_guard installs before SDK imports, redirects Modal
config to a nonexistent local path, clears credential variables without reading
their values, blocks real SDK authentication/control transport, external sockets,
model imports and protected suffixes. Fixture Client overrides return local tiny
protocol messages. Windows stdlib event-loop socketpair IPC is explicitly distinct
from external traffic. No guard removal, os._exit or GC/backend/version workaround.
No Image.build/resolve, mount pool, installer body, actual Sandbox or model call.

The only causal addition to C3's executed definition path is the registered
Function/FunctionData/RankedFunction/FunctionCreateResponse graph and actual
FunctionInfo._from_function_proto consumption. Existing dummy metadata dictionaries
in fixture_transport are protocol scaffolding, not loaded model inputs or predictions.
Frozen parser source is installed modal/types.py; not a fake parser.

Native exit, not assertion JSON, decides:
- Parser return witnessed plus native c0000005: SUFFICIENT_TRIGGER_REPRODUCED,
  sufficient within this environment/path only; no upstream/root-cause attribution.
- Parser return/assertions plus actual Python and launcher exit0: NOT_REPRODUCED.
  Build/resolve interaction remains unresolved; A040 HOLD retained.
- Identity/boundary error: BLOCKED_IDENTITY/BLOCKED_BOUNDARY; other failure or
  missing native-process observation: INCONCLUSIVE; resource/time/remaining PID: LIMIT.
Parser-entry marker alone does not certify successful parser consumption. Any
reached-parser or unobservable attempt consumes the measurement; no result rescue.

Pre-parser ordinary entry/observer errors alone may be repaired within the same
remaining aggregate budget. No scientific/model execution. Valid result ends
diagnostic work; only closeout/status/log/S0 handoff follow. No C7/S2/S3/ZIP/git.
