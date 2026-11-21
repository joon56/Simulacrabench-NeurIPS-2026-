# A040 local orchestration: call and evidence map

2026-10-04 KST. Scope: local protocol contract only. SDK1.6.0 installed source
and actual protobuf messages were used. External endpoints were injected.

| Stage | Production path and source evidence | Local evidence | Still unverified |
|---|---|---|---|
| Entry | `live_launcher.load_contract` → `contract.verify_sources`; `live_worker.run` repeats closure gate before endpoint calls | All12 modules compiled; missing/hash/placeholder defects refused before injected client; unauthorized LIVE refused | Fresh authorized LIVE config, launcher OS process kill behavior |
| Authentication | `sdk_endpoint.Endpoint.connect`; raw `_Client` loop identity; `WorkspaceNameLookup` response | Injected client on the same actual event loop; real Empty/protobuf response; wrong workspace refused | Current account/credits/access; real authentication was blocked |
| Base | `protocol.validate_base` consumes `ImageJoinStreamingResponse`; `GenericResult.GENERIC_STATUS_SUCCESS`; `ImageFromId` | Original missing module enum reproduced; success/failure/unspecified/empty/wrong type/hash/ID/timeout exercised; bad response creates0 | Actual base result/identity, complete runtime image |
| Preparation | Real `_App.lookup` and `_Image.from_id/run_function` handles; `controller_core.install_pins`; image build endpoint injected | Fixed installer AST identical; actual App request and response; image failure/timeout stops before science | Actual image build, dependency wheels/native libraries, build charges |
| Payload | `payload.Payload.verify/transfer`; `_SandboxFilesystem.write_bytes(data,remote_path)` | 26 meaningless bytes, exact size/hash, mutation/transport failure tested | Original112files/145542095bytes current parity; no payload read/hash here |
| Sandbox | `Endpoint.sandbox_create`; real SDK signature binding | `H100!`,2400s,cpu(1,1),15258MiB,gVisor,block_network,thread2,no secrets/OIDC,ports validated | Resource availability, actual CPU/RAM/GPU/native enforcement |
| Boundary | `sandbox_stage.command` → `linux_boundary.py` | Recorder validates60s command; incomplete native-boundary report blocks science; code compiled only | Actual Linux cgroups/swap0/affinity/native libc probe/driver/Python34pins |
| Science | Same `sandbox_stage.execute` → `linux_watchdog.py` → mechanically ported `linux_runner.py` | Exactly reference then candidate command recordings; failed reference blocks candidate; output completeness/time gates | Neither script body executed; E041/TabICL/all3/H100900s remain unmeasured |
| Export | `export_mode`: fixed logs/results/resources and named outputs with runner hashes | Normal export, absent result and mismatched output bytes exercised | Real target output bytes and measured resources |
| Cleanup | `live_worker.cleanup`: owned name/ID recovery, terminate, AppStop, AppGetInfo + TaskList + poll | Actual protobuf response handling; ID loss, stop/query failures, nonterminal state/tasks>0 cannot PASS | Actual remote cancellation/termination/billing lag |

The same `live_worker.run`, `build`, `cleanup`, `sandbox_stage.execute` and SDK
adapter are the production path and the regression path. No second controller
implements a fake successful flow. Only client RPC, image build, Sandbox/process/
filesystem and tiny payload endpoints differ. Real `_App`/`_Image` objects are used;
Sandbox/process/filesystem test doubles have restricted attributes and bind calls
against installed SDK signatures. Remote process results are explicitly invented
protocol messages, not measured scientific results. Their vector-count metadata
does not mean189649 vectors were computed; exported protocol output bytes are `[]`.

SDK source references (installed under `tmp/a040-modal-full-path1/sdk-venv/Lib/site-packages`):
`modal/app.py:340` lookup; `_image.py:2695` run_function and nested result enum;
`modal/sandbox.py:1346` name recovery,2027 terminate,2067 poll,2190 exec;
`modal/sandbox_fs.py:278` read_bytes,559 write_bytes; `modal/config.py:366` default
Sandbox V2; `modal_proto/api_pb2.pyi` real request/response fields. Source was read;
no provider facts were inferred from advertising or fetched anew.

Source completeness precedes App creation. There is no `continue-sandbox.json`
wait. Future extra transfer list must contain the exact12 hashed source modules;
the original allowlist is separate. Existing scientific source and policy remain
in `full-path-resume1`; new runner changes only local paths/manifest pointer and
single-H100 identity assertion. Tests compare the full mechanically transformed
text, and the installer AST, with their old sources.

Fixed future limits remain reference/candidate900s each, Sandbox2400s, physical
CPU1/two logical threads,15258MiB host cap, one GPU, preparation build900s/installer
600s, cleanup60s, parent15s grace. Cgroup layout or native denial uncertainty causes
STOP. Linux RSS/private/cgroup accounting is explicitly not Windows commitment.
Parent emergency kill records remote termination UNCONFIRMED; it cannot certify
that an unreachable remote resource stopped. That failure requires owned-resource
resolution under the future session's authority, not a new science invocation.

Local guards block Client.from_env/client opening, network/child-process endpoints,
protected file patterns and model imports. SDK configuration points to an absent
file in this session's tmp directory; known Modal token variables are removed in
the child without reading or printing values. The SDK default V2 name-recovery
token endpoint is also injected with a literal noncredential marker. No actual
token discovery occurs. Windows event-loop local self-pipe is initialized before
the guard; this is not native outbound-enforcement evidence.
